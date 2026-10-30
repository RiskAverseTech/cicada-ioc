"""Rule-selected subsequences: the sparse-message world (2026-10-30; registration in results/selection_lane_registration.md).

A designer who meant only some runes of a page to be read, by a deterministic position rule, leaves the rest as cover.
Every rule here is a function of position and layout only (never of the rune values):
  index sets, from the page start and from its end:  primes, composites, squares, triangular, fibonacci,
                                                       every k-th rune at residue r for k = 2..7 (27 sets)       -> 2 x 32
  complements of the five named index sets (from the start)                                                     -> 5
  layout sets: first rune of each line, last of each line, first of each word, last of each word, word interiors,
               the one- and two-rune words                                                                      -> 6
S1  pooled IoC (x 29) and adjacent-repeat rate of the selected stream against 1,000 per-page shuffles.
S2  in-clear: rune 5-gram log-probability of each page's selected stream against 2,000 random strings of its length;
    pooled z over pages (sum z / sqrt(pages)) and the largest page z.
S3  decode: each page's selected stream (>= 40 runes) under the book's 7,621 keys x 3 signs x 2 F, plain decoder with
    the soft rule; z by 400 random keystreams through the same decoder; hit = z >= 6, rank 1 in family, readable.
Controls: six plants (three in clear, three under a book Vigenere word), each at one rule's positions in a 263-rune
page with uniform cover elsewhere.
Usage: STAGE=stats -> S1, S2, controls (minutes); SHARD=k NSHARD=m STAGE=decode -> S3 shards; MERGE=1 -> results/selection_lane.md
"""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, primes, english_to_runes
from score import decode, translit, S_MAX
from skip_decrypt import combine
import families as F, ngram

STAGE = os.environ.get("STAGE", "stats"); MERGE = os.environ.get("MERGE") == "1"; SMOKE = os.environ.get("SMOKE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(4400 + SHARD); t0 = time.time()
NSHUF, NRAND, NULLK, MIN_DEC, Z_HIT = (100, 200, 100, 40, 6.0) if SMOKE else (1000, 2000, 400, 40, 6.0)
SEP = set('-.&$§'); SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))

# ---------- pages with layout
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")


def parse(s):
    runes, wid, lid = [], [], []; w = l = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w); lid.append(l)
        elif ch in SEP: pending = True
        elif ch == "/": l += 1
    return np.array(runes, int), np.array(wid, int), np.array(lid, int)


PAGES = [(f"LP2-{k-16:02d}",) + parse(chunks[k]) for k in range(16, 72)]
PAGES = [p for p in PAGES if len(p[1]) > 0]
assert [p[0] for p in PAGES] == [pid for pid, C in F.pages if len(C)] and all(np.array_equal(p[1], C) for p, (_, C) in zip(PAGES, [q for q in F.pages if len(q[1])]))

# ---------- rules
PR = set(primes(400)); SQ = {i * i for i in range(20)}; TRI = {i * (i + 1) // 2 for i in range(30)}
FIB = set(); a, b = 1, 2
while a < 400: FIB.add(a); a, b = b, a + b
NAMED = {"primes": lambda i: i in PR, "composites": lambda i: i >= 4 and i not in PR, "squares": lambda i: i in SQ,
         "triangular": lambda i: i in TRI, "fibonacci": lambda i: i in FIB}


def first_last(ids):
    f = np.ones(len(ids), bool); f[1:] = ids[1:] != ids[:-1]; l = np.ones(len(ids), bool); l[:-1] = ids[1:] != ids[:-1]; return f, l


def rules():
    R = []
    for nm, fn in NAMED.items():
        R.append((nm, lambda n, w, l, fn=fn: np.array([fn(i) for i in range(n)])))
        R.append((nm + " from end", lambda n, w, l, fn=fn: np.array([fn(i) for i in range(n)])[::-1]))
        R.append(("not " + nm, lambda n, w, l, fn=fn: ~np.array([fn(i) for i in range(n)])))
    for k in range(2, 8):
        for r in range(k):
            R.append((f"every {k}th, residue {r}", lambda n, w, l, k=k, r=r: np.arange(n) % k == r))
            R.append((f"every {k}th, residue {r}, from end", lambda n, w, l, k=k, r=r: (np.arange(n) % k == r)[::-1]))
    R += [("line-first", lambda n, w, l: first_last(l)[0]), ("line-last", lambda n, w, l: first_last(l)[1]),
          ("word-first", lambda n, w, l: first_last(w)[0]), ("word-last", lambda n, w, l: first_last(w)[1]),
          ("word-interior", lambda n, w, l: ~(first_last(w)[0] | first_last(w)[1])),
          ("short words (1-2 runes)", lambda n, w, l: np.bincount(w)[w] <= 2)]
    return R


RULES = rules(); RES = RESULTS; T5 = None


def t5():
    global T5
    if T5 is None: T5 = ngram.load_dense()
    return T5


def ioc(v):
    c = np.bincount(v, minlength=N); n = len(v); return (c * (c - 1)).sum() / (n * (n - 1)) * N if n > 1 else float("nan")


def select(rule, C, w, l):
    m = rule(len(C), w, l); return C[m]


# ---------- S1 + S2 on the pages, and the controls
def stats_stage():
    out = {"rules": [], "controls": []}
    shuf = [[rng.permutation(C) for _, C, _, _ in PAGES] for _ in range(NSHUF)]
    z5cache = {}
    def z5(P):
        n = len(P)
        if n not in z5cache: z5cache[n] = ngram.score_batch(rng.integers(0, N, size=(NRAND, n)), t5())
        nul = z5cache[n]; return float((ngram.score_batch(P[None, :], t5())[0] - nul.mean()) / nul.std())
    for ri, (nm, rule) in enumerate(RULES):
        sel = [select(rule, C, w, l) for _, C, w, l in PAGES]; pooled = np.concatenate(sel)
        dbl = np.mean(np.concatenate([s[1:] == s[:-1] for s in sel if len(s) > 1])) * N
        io = ioc(pooled)
        # the shuffle null: the same rule on per-page shuffles (positions kept, runes permuted)
        nio = []; ndb = []
        for S in shuf:
            ss = [C_s[rule(len(C), w, l)] for (_, C, w, l), C_s in zip(PAGES, S)]
            nio.append(ioc(np.concatenate(ss))); ndb.append(np.mean(np.concatenate([s[1:] == s[:-1] for s in ss if len(s) > 1])) * N)
        nio, ndb = np.array(nio), np.array(ndb)
        zs = [z5(s) for s in sel if len(s) >= 10]
        row = dict(rule=nm, runes=int(len(pooled)), ioc=float(io), ioc_z=float((io - nio.mean()) / nio.std()), dbl=float(dbl), dbl_z=float((dbl - ndb.mean()) / ndb.std()),
                   z5_pooled=float(np.sum(zs) / np.sqrt(len(zs))) if zs else float("nan"), z5_max=float(max(zs)) if zs else float("nan"), pages=len(zs))
        out["rules"].append(row)
        print(f"  {ri+1:2d}/{len(RULES)} {nm:34s} runes {len(pooled):6,d} IoC {io:.3f} (z {row['ioc_z']:+.1f}) dbl x{dbl:.2f} (z {row['dbl_z']:+.1f}) z5 pooled {row['z5_pooled']:+.1f} max {row['z5_max']:+.1f} [{time.time()-t0:.0f}s]", flush=True)
    # controls: English at a rule's positions, uniform cover elsewhere; three in clear (S2 must rank the rule first at z >= 6), three keyed (S3 must find the key)
    text = (RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(errors="ignore")[30000:]
    words = [np.array(english_to_runes(w)) for w in re.findall(r"[A-Za-z]+", text)]; EP = np.concatenate([w for w in words if len(w)])
    _, _, Kp3, Lp3 = F.ALLSETS[3]; VW = [i for i, (f, _) in enumerate(Lp3) if f == "vigenere-word"]
    _, C0, w0, l0 = PAGES[0]; n = len(C0)                      # the first page's layout (262 runes) carries the plants
    picks = ["primes", "every 3th, residue 1", "word-first", "composites", "every 2th, residue 0", "word-interior"]   # keyed plants need >= 100 selected runes for the plain decoder's power
    for ci, pick in enumerate(picks):
        rule = dict(RULES)[pick]; m = rule(n, w0, l0); k = int(m.sum()); p0 = int(rng.integers(0, len(EP) - k)); P = EP[p0:p0 + k]
        page = rng.integers(0, N, n); keyed = ci >= 3; sign, mode = SIGNS[ci % 3]; ki = int(rng.choice(VW)); K = Kp3[ki]
        if keyed:
            kk = np.resize(K, k); P_c = np.array([combine(int(a), int(b), sign) for a, b in zip(P, kk)])    # the repository's sign convention (skip_decrypt.combine)
            page[m] = P_c
        else: page[m] = P
        if keyed:
            Csel = page[m]; Ks = Kp3[VW][:, :k + S_MAX + 2]; Ks = (-Ks) % N if sign == "add" else Ks
            Kr = rng.integers(0, N, size=(NULLK, k + S_MAX + 2)); nul = decode(Csel, Kr, F.lu, False, mode)[0]
            sc = decode(Csel, Ks, F.lu, False, mode)[0]; z = (sc - nul.mean()) / nul.std(); pos = VW.index(ki)
            ok = bool(z[pos] >= Z_HIT and (z > z[pos]).sum() == 0)
            out["controls"].append(dict(id=ci, rule=pick, kind="keyed", sign=sign, key=Lp3[ki][1], selected=k, z=float(z[pos]), rank=int((z > z[pos]).sum()) + 1, **{"pass": ok}))
        else:
            zz = np.array([z5(select(r, page, w0, l0)) if len(select(r, page, w0, l0)) >= 10 else -9 for _, r in RULES]); j = [nm for nm, _ in RULES].index(pick)
            ok = bool(zz[j] >= Z_HIT and (zz > zz[j]).sum() == 0)
            out["controls"].append(dict(id=ci, rule=pick, kind="clear", selected=k, z=float(zz[j]), rank=int((zz > zz[j]).sum()) + 1, **{"pass": ok}))
        print(f"  control {ci} {pick} {'keyed' if keyed else 'clear'}: z {out['controls'][-1]['z']:.1f} rank {out['controls'][-1]['rank']} -> {'PASS' if ok else 'miss'}", flush=True)
    json.dump(out, open(RES / ("selection_stats_smoke.json" if SMOKE else "selection_stats.json"), "w"), indent=1)


# ---------- S3: decode the selected streams under the book's keys
def decode_stage():
    rows = []; ntests = 0; zmax = -9.0
    mine = [(ri, r) for ri, r in enumerate(RULES) if ri % NSHARD == SHARD]
    if SMOKE: mine = mine[:2]
    for ri, (nm, rule) in mine:
        for pi, (pid, C, w, l) in enumerate(PAGES if not SMOKE else PAGES[:2]):
            Cs = select(rule, C, w, l); k = len(Cs)
            if k < MIN_DEC: continue
            for f_rule in (False, True):
                nul = {}
                for si, (sign, mode, Ks, labs) in enumerate(F.ALLSETS):
                    if mode not in nul: nul[mode] = decode(Cs, rng.integers(0, N, size=(NULLK, k + S_MAX + 2)), F.lu, f_rule, mode)[0]
                    m0, s0 = nul[mode].mean(), nul[mode].std(); sc = np.empty(len(Ks))
                    for b in range(0, len(Ks), 1000): sc[b:b + 1000] = decode(Cs, Ks[b:b + 1000, :k + S_MAX + 2], F.lu, f_rule, mode)[0]
                    z = (sc - m0) / s0; ntests += len(Ks); zmax = max(zmax, float(z.max()))
                    for j in np.flatnonzero(z >= Z_HIT - 1.0):
                        fam = labs[j][0]; famz = z[[t for t, (f, _) in enumerate(labs) if f == fam]]
                        d = decode(Cs, Ks[j:j + 1, :k + S_MAX + 2], F.lu, f_rule, mode)[2][0]
                        rows.append(dict(rule=nm, page=pid, selected=k, sign=sign, F=f_rule, fam=fam, key=labs[j][1], z=float(z[j]), rank=int((famz > z[j]).sum()) + 1, tr=translit(d[:80])))
        print(f"  rule {ri+1}/{len(RULES)} {nm}: {ntests:,} tests, zmax {zmax:.2f}, rows {len(rows)} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(dict(rows=rows, ntests=ntests, zmax=zmax, seconds=time.time() - t0), open(RES / ("selection_decode_smoke.json" if SMOKE else f"selection_decode_shard{SHARD}.json"), "w"), indent=1)


def merge():
    st = json.loads((RES / "selection_stats.json").read_text()); sh = [json.loads(p.read_text()) for p in sorted(RES.glob("selection_decode_shard*.json"))]
    rows = [r for d in sh for r in d["rows"]]; nt = sum(d["ntests"] for d in sh); zmax = max(d["zmax"] for d in sh); hits = [r for r in rows if r["z"] >= Z_HIT and r["rank"] == 1]
    R = st["rules"]; ctr = st["controls"]
    out = [f"# Rule-selected subsequences (the sparse-message world): {len(R)} position rules on the 55 unsolved pages", "",
           f"Registration: `results/selection_lane_registration.md`. S1: pooled IoC (× 29) and adjacent-repeat rate of each rule's selected stream, z against {NSHUF:,} per-page shuffles. S2: rune 5-gram z of each page's selected stream against {NRAND:,} random strings of its length, pooled over pages and the largest page. S3: the selected streams of ≥ {MIN_DEC} runes under the book's 7,621 keys × 3 signs × 2 F, plain decoder, z by {NULLK} random keystreams: **{nt:,} tests, largest z {zmax:.2f}, hits (z ≥ 6, rank 1) {len(hits)}**.", "",
           f"Controls {sum(c['pass'] for c in ctr)}/{len(ctr)}: " + "; ".join(f"{c['rule']} ({c['kind']}) z {c['z']:.1f} rank {c['rank']}" for c in ctr) + ".", "",
           "| rule | selected runes | IoC | z | repeats × uniform | z | 5-gram z pooled | largest page z |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(R, key=lambda r: -abs(r["ioc_z"])): out.append(f"| {r['rule']} | {r['runes']:,} | {r['ioc']:.3f} | {r['ioc_z']:+.1f} | {r['dbl']:.2f} | {r['dbl_z']:+.1f} | {r['z5_pooled']:+.1f} | {r['z5_max']:+.1f} |")
    q1 = sum(c["pass"] for c in ctr) == len(ctr); q2 = all(r["z5_pooled"] < 6 for r in R); q3 = all(abs(r["ioc_z"]) < 4 for r in R); q4 = len(hits) == 0
    out += ["", "## Claims (registration)", "", f"- Q1 controls 6/6: **{'holds' if q1 else 'fails'}**.", f"- Q2 no rule's pooled 5-gram z ≥ 6: **{'holds' if q2 else 'fails'}** (largest {max(r['z5_pooled'] for r in R):+.1f}).",
            f"- Q3 no rule's IoC z ≥ 4 against the shuffle null: **{'holds' if q3 else 'fails'}** (largest |z| {max(abs(r['ioc_z']) for r in R):.1f}).", f"- Q4 no S3 hit: **{'holds' if q4 else 'fails'}**.", ""]
    if rows:
        out += ["## S3 rows within one sigma of the bar", "", "| rule | page | selected | sign | F | family | key | z | rank | text |", "|---|---|---|---|---|---|---|---|---|---|"]
        for r in sorted(rows, key=lambda r: -r["z"])[:40]: out.append(f"| {r['rule']} | {r['page']} | {r['selected']} | {r['sign']} | {int(r['F'])} | {r['fam']} | {r['key']} | {r['z']:.2f} | {r['rank']} | {r['tr']} |")
    out += ["", f"Runtime: S3 longest shard {max(d['seconds'] for d in sh)/60:.0f} min on {len(sh)} shards. Reproduce: `STAGE=stats`, then `SHARD=k NSHARD=8 STAGE=decode`, then `MERGE=1`.", ""]
    (RES / "selection_lane.md").write_text("\n".join(out)); json.dump(dict(rules=R, controls=ctr, ntests=nt, zmax=zmax, hits=hits, claims=dict(Q1=q1, Q2=q2, Q3=q3, Q4=q4)), open(RES / "selection_lane.json", "w"), indent=1)
    print("\n".join(out[:8]))


if __name__ == "__main__":
    print(f"{len(RULES)} rules, {len(PAGES)} pages")
    if MERGE: merge()
    elif STAGE == "stats": stats_stage()
    else: decode_stage()
