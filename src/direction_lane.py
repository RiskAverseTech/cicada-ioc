"""Numbers as directions (lane D1, instrument 2; 2026-10-31).  Registration: results/d1_registration.md.

"Their numbers are the direction" (2016, signed), read with the warning page's "the words or their numbers": every word has a
number, its Gematria sum, and a number can be a direction (a shift, a step, an offset) rather than a key value.
Part A, keyless: the cipher word's own number, or the previous cipher word's, directs its decryption: g in {sum mod 29,
sum mod 28 + 1, sum of (v - 1) mod 29, product mod 29, length, index of the largest rune}, applied as a constant shift over
the word, a step j*g, an offset into a prime stream (p, p-1, p+1), or an offset into the solved plaintext; 3 signs x 2 F.
Every page decoded under every configuration; 5-gram z against 2,000 uniform pages and the §72 z*; chance level from the same
configurations on uniform pages, recorded first.
Part B, the words as the map: the solved pages' words in order with numbers W_k; streams (i) W_k mod 29 per rune, (ii) W_k
mod 29 as the k-th unsolved word's shift, (iii) the k-th word keyed by a prime stream from offset W_k, (iv) by the solved text
from word W_k mod n, (v) the cumulative sum of W_k as a running direction; every alignment 0..n-1 of the map against the
section's words (counted through the page joins, §71); §62's free-null decoder unchanged (prior -2.2, tier 1 on the first
160 runes at z >= 4.5, tier 2 on the full page at z_uni >= 6, free - plain >= 20, readable); six plants under (ii), (iii), (v).
Stages (STAGE=): chance, keyless, map (SHARD/NSHARD over alignments), merge.  SMOKE=1 shrinks everything.
"""
import os, sys, re, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, english_to_runes, to_latin
from score import decode, translit, S_MAX
from skip_decrypt import combine
import families as F, corpus

t0 = time.time(); STAGE = os.environ.get("STAGE", "chance"); SMOKE = os.environ.get("SMOKE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(31337 + SHARD); lu = F.lu
PEN = -2.2; WIN = 160; Z_T1, Z_UNI, FREE_BASE = 4.5, 6.0, 20.0; NREPS = 200 if SMOKE else 2000; N5 = 200 if SMOKE else 2000
R_FILL, Q_SOFT = 0.10, 0.81; SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort")); OUT = "direction_smoke" if SMOKE else "direction"
PRIMEVAL = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109])
SEP = set('-.&$§')


def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


# ---------- the pages with word ids and the section-wide word index (words cross page joins)
def parse_chunk(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, np.int64), np.array(wid, np.int64)


CHUNKS = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8").split("%")
PAGES, GW, GR = [], [], []; wcount = 0; rcount = 0; prev_open = False
for k in range(16, 72):
    C, wid = parse_chunk(CHUNKS[k])
    if len(C) == 0: continue
    body = re.sub(r"[\s/]", "", CHUNKS[k]); starts_mid = bool(body) and body[0] in IDX
    cont = prev_open and starts_mid                                  # this page continues the previous page's last word
    gw = wid + (wcount - 1 if cont else wcount); PAGES.append((f"LP2-{k-16:02d}", C, wid)); GW.append(gw); GR.append(rcount)
    wcount = int(gw.max()) + 1; rcount += len(C); prev_open = bool(body) and body[-1] in IDX
assert len(PAGES) == 55
NWORDS_SECTION = wcount


# ---------- the solved words (the map) in book order, with their numbers
TR = (RAW / "iddqd__liber-primus__translation.txt").read_text(encoding="utf-8")
SOLVED = [np.array(english_to_runes(w)) for l in TR.splitlines() if re.match(r"\s*\d+\.\d+\.\d+\.\d+\s", l) for w in re.findall(r"[A-Za-z']+", l) if english_to_runes(w)]
WNUM = np.array([int(PRIMEVAL[w].sum()) for w in SOLVED]); NW = len(SOLVED)
SOLVED_RUNES = np.concatenate(SOLVED); SOLVED_START = np.concatenate([[0], np.cumsum([len(w) for w in SOLVED])[:-1]])


def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)


PR = sieve(400000)[:30000]; PRIME_STREAMS = {"p": PR % N, "p-1": (PR - 1) % N, "p+1": (PR + 1) % N}


# ---------- numbers of words
def word_runs(wid):
    starts = np.flatnonzero(np.r_[True, wid[1:] != wid[:-1]]); ends = np.r_[starts[1:], len(wid)]; return list(zip(starts, ends))


GFUNCS = {"sum29": lambda w: int(PRIMEVAL[w].sum() % N), "sum28+1": lambda w: int(PRIMEVAL[w].sum() % (N - 1)) + 1,
          "tot29": lambda w: int((PRIMEVAL[w] - 1).sum() % N), "prod29": lambda w: int(np.prod(PRIMEVAL[w] % N, dtype=np.int64) % N),
          "len": lambda w: int(len(w)), "argmax": lambda w: int(np.argmax(w))}
APPS = ("shift", "step", "prime p", "prime p-1", "prime p+1", "solved")


def keystream_from_numbers(nums, runs, L, app):
    """per-rune key for a page from one number per word; j counts the rune's position in its word"""
    K = np.zeros(L + S_MAX + 2, np.int64)
    for (a, b), g in zip(runs, nums):
        j = np.arange(b - a)
        if app == "shift": K[a:b] = g % N
        elif app == "step": K[a:b] = (j * g) % N
        elif app.startswith("prime"): K[a:b] = PRIME_STREAMS[app.split()[1]][g + j]
        else: K[a:b] = SOLVED_RUNES[(SOLVED_START[g % NW] + j) % len(SOLVED_RUNES)]
    K[L:] = K[L - 1]; return K


def plain_decode(C, K, sign, f_rule):
    """every rune keyed by its own position's key (no skips); F rule: a cipher F is a literal F"""
    Kc = K[:len(C)]
    P = (C - Kc) % N if sign == "sub" else ((C + Kc) % N if sign == "add" else (Kc - C) % N)
    if f_rule: P[C == 0] = 0
    return P


# ---------- scorers: the rune 5-gram z against uniform pages, and the §72 z*
_T5 = None
def t5():
    global _T5
    if _T5 is None:
        import ngram; _T5 = ngram.load_dense()
    return _T5


NULL5 = {}
def z5(P):
    import ngram
    L = len(P)
    if L not in NULL5:
        s = ngram.score_batch(rng.integers(0, N, size=(N5, L)), t5()); NULL5[L] = (float(s.mean()), float(s.std()))
    mu, sd = NULL5[L]; return float((ngram.score_batch(P[None, :], t5())[0] - mu) / sd)


import nonprose_lane as NP
MOM = {}
def zstar(P, wid, key):
    if key not in MOM: MOM[key] = NP.moments(P * 0 + rng.integers(0, N, size=len(P)), wid, False, rng) if False else NP.moments(PAGES[key][1], PAGES[key][2], False, rng)
    st, ln = NP.word_slots(wid); return float(NP.zify(NP.stats(P[None, :], st, ln), MOM[key]).max())


# ---------- Part A, keyless
def keyless_configs():
    return [(src, gname, app, sign, f) for src in ("self", "prev") for gname in GFUNCS for app in APPS for sign, _ in SIGNS for f in (False, True)]


def keyless_numbers(C, wid, src, gname):
    runs = word_runs(wid); g = GFUNCS[gname]; nums = [g(C[a:b]) for a, b in runs]
    if src == "prev": nums = [0] + nums[:-1]
    return nums, runs


def run_keyless(pages, with_star):
    rows = []
    for ci, (src, gname, app, sign, f) in enumerate(keyless_configs()):
        zs, stars, best = [], [], (-1e9, None, "")
        for k, (pid, C, wid) in enumerate(pages):
            nums, runs = keyless_numbers(C, wid, src, gname); K = keystream_from_numbers(nums, runs, len(C), app); P = plain_decode(C, K, sign, f)
            z = z5(P); zs.append(z); stars.append(zstar(P, wid, k) if with_star else float("nan"))
            if z > best[0]: best = (z, pid, to_latin(P)[:80])
        rows.append(dict(src=src, g=gname, app=app, sign=sign, F=f, med5=float(np.median(zs)), max5=float(np.max(zs)), maxstar=float(np.nanmax(stars)) if with_star else float("nan"), best_page=best[1], text=best[2]))
        if ci % 50 == 0 or rows[-1]["med5"] >= 3: log(ci, src, gname, app, sign, f, "med", round(rows[-1]["med5"], 2), "max", round(rows[-1]["max5"], 2))
    return rows


def dump(name, obj): (RESULTS / f"{OUT}_{name}.json").write_text(json.dumps(obj, indent=1)); log("wrote", name)


def stage_chance():
    meds, maxs = [], []
    for rep in range(3 if SMOKE else 20):
        fake = [(pid, rng.integers(0, N, size=len(C)), wid) for pid, C, wid in PAGES]
        rows = run_keyless(fake, False); meds += [r["med5"] for r in rows]; maxs += [r["max5"] for r in rows]
    dump("chance", {"n": len(meds), "median_max": float(max(meds)), "median_p99": float(np.percentile(meds, 99)), "best_max": float(max(maxs))})


def stage_keyless():
    rows = run_keyless(PAGES, True); dump("keyless", {"rows": rows})


# ---------- Part B, the words as the map
SCHEMES = ("stream", "word-shift", "word-prime p", "word-prime p-1", "word-prime p+1", "word-solved", "cumulative")


def map_keystream(scheme, a, k, L, wid, gw, gr):
    """per-rune key for page k (word structure wid, section word index gw, section rune index gr) at alignment a"""
    K = np.zeros(L + S_MAX + 2, np.int64)
    if scheme == "stream":
        K[:] = WNUM[(gr + a + np.arange(L + S_MAX + 2)) % NW] % N; return K
    runs = word_runs(wid); nums = [int(WNUM[(gw[s] + a) % NW]) for s, _ in runs]
    if scheme == "word-shift": app = "shift"
    elif scheme.startswith("word-prime"): app = "prime " + scheme.split()[1]
    elif scheme == "word-solved": app = "solved"
    else:
        cum = np.cumsum([int(WNUM[(m + a) % NW]) for m in range(int(gw.max()) + 1)]) % N        # running direction over the section's words up to this page
        nums = [int(cum[gw[s]]) for s, _ in runs]; app = "shift"
    return keystream_from_numbers(nums, runs, L, app)


def dec(C, Ks, f_rule, mode, free=True):
    if not free: return decode(C, Ks, lu, f_rule, mode)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, None, nm, PEN)


def null_ms(C, f_rule, mode, reps=NREPS, batch=500):
    sc = []
    for b in range(0, reps, batch):
        Kr = rng.integers(0, N, size=(min(batch, reps - b), len(C) + S_MAX + 2)); sc.append(dec(C, Kr, f_rule, mode)[0])
    sc = np.concatenate(sc); return float(sc.mean()), float(sc.std()), float(sc.max())


text = corpus.TEXTS["emerson_essays1"][0](); EW = [np.array(english_to_runes(w)) for w in re.findall(r"[A-Za-z']+", text) if english_to_runes(w)]


def plant(scheme, a0, k, sign, f_rule):
    """Emerson laid into page k's length with its own words, keyed by the scheme at alignment a0 with §62's filler form"""
    pid, Cref, _ = PAGES[k]; L = len(Cref); wi = int(rng.integers(0, len(EW) - 500)); P, W = [], []; w = 0
    while len(P) < L + 40:
        word = EW[wi]; wi += 1; P += list(word); W += [w] * len(word); w += 1
    P, W = np.array(P), np.array(W); gw = W + int(GW[k][0]); K = map_keystream(scheme, a0, k, len(P), W, gw, GR[k])
    C, Wc, prev = [], [], None; runs = word_runs(W); pos = 0
    for (s, e) in runs:
        j = 0
        for i in range(s, e):
            p = int(P[i])
            if f_rule and p == 0: C.append(0); Wc.append(W[i]); prev = 0; continue
            c = combine(p, int(K[min(s + j, len(K) - 1)]), sign)
            while prev is not None and c == prev and rng.random() < Q_SOFT: j += 1; c = combine(p, int(K[min(s + j, len(K) - 1)]), sign)
            C.append(int(c)); Wc.append(W[i]); prev = int(c); j += 1
            if rng.random() < R_FILL and i < e - 1:
                fch = int(rng.integers(0, N - 1)); fch = fch if fch < prev else fch + 1; C.append(fch); Wc.append(W[i]); prev = fch
        if len(C) >= L: break
    C, Wc = np.array(C[:L]), np.array(Wc[:L]); return C, Wc, Wc + int(GW[k][0])


def tier1(C, wid, gw, gr, k, scheme, aligns, sign, mode, f_rule, m0, s0):
    Ks = np.stack([map_keystream(scheme, a, k, WIN, wid[:WIN], gw[:WIN], gr) for a in aligns]); Ks = (-Ks) % N if sign == "add" else Ks
    return (dec(C[:WIN], Ks, f_rule, mode)[0] - m0) / s0


FULL = {}
def tier2(C, Kf, f_rule, mode, key):
    if key not in FULL: FULL[key] = null_ms(C, f_rule, mode)
    m0, s0, mx = FULL[key]; s2, _, d = dec(C, Kf, f_rule, mode); s1 = dec(C, Kf, f_rule, mode, free=False)[0]
    return float((s2[0] - m0) / s0), float(s2[0] - s1[0]), translit(d[0][:80]), bool(s2[0] > mx)


def stage_map():
    aligns_all = np.arange(NW) if not SMOKE else np.arange(0, NW, 97)
    mine = aligns_all[SHARD::NSHARD]; res = {"controls": [], "survivors": [], "candidates": [], "ntests": 0, "zmax1": -9.0}
    WN = {}
    for k, (pid, C, wid) in enumerate(PAGES):
        for f_rule in (False, True):
            for mode in ("sub", "beaufort"): WN[(k, f_rule, mode)] = null_ms(C[:WIN], f_rule, mode)
    log("window nulls ready;", len(mine), "alignments on this shard")
    if SHARD == 0:
        for ci, (scheme, k) in enumerate([("word-shift", 7), ("word-shift", 30), ("word-prime p", 12), ("word-prime p", 44), ("cumulative", 20), ("cumulative", 50)]):
            sign, mode = SIGNS[ci % 3]; f_rule = bool(ci % 2); a0 = int(rng.choice(aligns_all)); C, Wc, gwc = plant(scheme, a0, k, sign, f_rule)
            m0, s0, _ = null_ms(C[:WIN], f_rule, mode); z = tier1(C, Wc, gwc, GR[k], k, scheme, aligns_all, sign, mode, f_rule, m0, s0)
            near = np.abs(aligns_all - a0) <= 1; zt = float(z[near].max()); rank = int((z[~near] > zt).sum()) + 1; top = int(aligns_all[int(z.argmax())])
            Kf = map_keystream(scheme, a0, k, len(C), Wc, gwc, GR[k])[None, :]; Kf = (-Kf) % N if sign == "add" else Kf
            z2, fb, tr, above = tier2(C, Kf, f_rule, mode, ("ctrl", ci)); ok = bool(rank == 1 and zt >= Z_T1 and z2 >= Z_UNI and above)      # amendment: free - plain reported, not required (word-aligned keys realign the plain decoder at every word)
            res["controls"].append(dict(id=f"control-{ci:02d}", scheme=scheme, page=PAGES[k][0], sign=sign, F=f_rule, align=a0, top=top, z1=zt, rank=rank, z2=z2, fb=fb, tr=tr, **{"pass": ok}))
            log("control", ci, scheme, PAGES[k][0], sign, f_rule, "planted", a0, "top", top, "z1", round(zt, 1), "rank", rank, "z2", round(z2, 1), "fb", round(fb), "PASS" if ok else "miss")
    for scheme in SCHEMES:
        for k, (pid, C, wid) in enumerate(PAGES):
            for f_rule in (False, True):
                for sign, mode in SIGNS:
                    m0, s0, _ = WN[(k, f_rule, mode)]
                    for b in range(0, len(mine), 500):
                        al = mine[b:b + 500]; z = tier1(C, wid, GW[k], GR[k], k, scheme, al, sign, mode, f_rule, m0, s0); res["ntests"] += len(al); res["zmax1"] = max(res["zmax1"], float(z.max()))
                        for j in np.flatnonzero(z >= Z_T1):
                            a = int(al[j]); Kf = map_keystream(scheme, a, k, len(C), wid, GW[k], GR[k])[None, :]; Kf = (-Kf) % N if sign == "add" else Kf
                            z2, fb, tr, above = tier2(C, Kf, f_rule, mode, (k, f_rule, mode))
                            row = dict(scheme=scheme, page=pid, sign=sign, F=f_rule, align=a, z1=float(z[j]), z2=z2, fb=fb, tr=tr, above_max=above); res["survivors"].append(row)
                            if z2 >= Z_UNI and above: res["candidates"].append(row); log("CANDIDATE", row)
        log("scheme", scheme, "done:", res["ntests"], "tests, zmax1", round(res["zmax1"], 2), "survivors", len(res["survivors"]))
    res["seconds"] = time.time() - t0; dump(f"map_{SHARD}", res)


def stage_merge():
    ch = json.loads((RESULTS / f"{OUT}_chance.json").read_text()); kl = json.loads((RESULTS / f"{OUT}_keyless.json").read_text())["rows"]
    parts = [json.loads(p.read_text()) for p in sorted(RESULTS.glob(f"{OUT}_map_*.json"))]
    ctr = sum((p["controls"] for p in parts), []); surv = sorted(sum((p["survivors"] for p in parts), []), key=lambda r: -r["z2"]); cands = sum((p["candidates"] for p in parts), [])
    nt = sum(p["ntests"] for p in parts); zmax1 = max(p["zmax1"] for p in parts); secs = max(p["seconds"] for p in parts)
    hits = [r for r in kl if r["med5"] >= 6 and r["max5"] >= 10]
    o = ["# Numbers as directions (lane D1, instrument 2)", "", "Registration: `results/d1_registration.md`.", "",
         "## Part A, keyless: the word's own number as its direction", "",
         f"{len(kl)} configurations (number source × function × application × sign × F) on the 55 pages. Chance level ({ch['n']} configuration-sets on uniform pages): largest median page 5-gram z {ch['median_max']:.2f}, largest page {ch['best_max']:.2f}. Largest median here **{max(r['med5'] for r in kl):.2f}**, largest page {max(r['max5'] for r in kl):.2f}, largest z\\* {max(r['maxstar'] for r in kl):.2f}. Hits: **{len(hits)}**.", "",
         "| source | number | applied as | sign | F | median page z5 | best page z5 | best page | z\\* | text |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(kl, key=lambda r: -r["med5"])[:12]: o.append(f"| {r['src']} | {r['g']} | {r['app']} | {r['sign']} | {int(r['F'])} | {r['med5']:.2f} | {r['max5']:.2f} | {r['best_page']} | {r['maxstar']:.2f} | {r['text'][:50]} |")
    o += ["", "## Part B, the solved words as the map", "", f"{len(SCHEMES)} schemes × {NW:,} alignments × 55 pages × 3 signs × 2 F; **{nt:,} window decodes** under the free-null decoder; tier 1 at z ≥ {Z_T1} on {WIN} runes, tier 2 at z_uni ≥ {Z_UNI:.0f} above the full-page null maximum and readable (free − plain reported, not required: amendment in the registration).", "",
          "| control | scheme | page | sign | F | planted alignment | top | z1 | rank | z2 | free − plain | pass |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    o += [f"| {c['id']} | {c['scheme']} | {c['page']} | {c['sign']} | {int(c['F'])} | {c['align']} | {c['top']} | {c['z1']:.1f} | {c['rank']} | {c['z2']:.1f} | {c['fb']:+.0f} | {'yes' if c['pass'] else 'no'} |" for c in ctr]
    o += ["", f"Controls passing: {sum(c['pass'] for c in ctr)} of {len(ctr)}. Largest tier-1 z {zmax1:.2f}; survivors {len(surv):,}; candidates **{len(cands)}**.", ""]
    o += [f"- **{c['scheme']}** page {c['page']} {c['sign']} F={c['F']} alignment {c['align']}: z_uni {c['z2']:.2f}, free − plain {c['fb']:+.0f}: `{c['tr']}`" for c in cands] or ["None. No accepted decoding within the tested configurations at the stated detection limits."]
    o += ["", "| scheme | page | sign | F | alignment | z1 | z2 | free − plain | above null max | transliteration |", "|---|---|---|---|---|---|---|---|---|---|"]
    o += [f"| {s['scheme']} | {s['page']} | {s['sign']} | {int(s['F'])} | {s['align']} | {s['z1']:.1f} | {s['z2']:.2f} | {s['fb']:+.0f} | {'yes' if s['above_max'] else 'no'} | `{s['tr'][:48]}` |" for s in surv[:15]]
    o += ["", "## Registered predictions", "", f"- D1 (plants): {sum(c['pass'] for c in ctr)} of {len(ctr)} → {'holds' if ctr and all(c['pass'] for c in ctr) else 'fails'}.", f"- D2 (no tier-2 candidate): {len(cands)} → {'holds' if not cands else 'fails'}.", f"- D3 (no Part A hit): {len(hits)} → {'holds' if not hits else 'fails'}.", "",
          f"Runtime, longest map shard: {secs/3600:.1f} h. Reading: written after the run, below. [stated — the tables]", "", "Reproduce: `STAGE=chance|keyless|map|merge .venv/bin/python -I src/direction_lane.py`.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"chance": stage_chance, "keyless": stage_keyless, "map": stage_map, "merge": stage_merge}[STAGE]()
