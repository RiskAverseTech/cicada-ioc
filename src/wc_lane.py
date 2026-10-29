"""§61 part C (2026-10-29): the small libraries under the word-constrained filler decoder.  Pre-registered in
results/wc_lane_registration.md (commit 8ff95b0); the prior comes from part A (results/wc_power.json), the nulls and the
margin from part B (results/wc_nulls.json, results/wc_margin.json).

LIBRARIES.  (1) "book": families.ALLSETS, 7,621 keys x 3 sign conventions (phase-3 families incl. DIVINITY and FIRFUMFERENFE
and every other Vigenère word of the book both directions; phase-4 phrases and sentences), x 2 F, every page at full
length.  (2) "prime": p[n+s], p[n+s]-1, p[n+s]+1 for s = 0..19,999, 3 signs, 2 F, every page at full length (the literal-F
variant is the solved pages' own rule).  (3) "text": the sixteen external texts in §55 C's units (ten at every offset both
directions, six at sentence starts forward); tier 1 on the first 160 runes of LP2-00/01/02 x 3 signs x 2 F at z >= 4.5 over
the window null (2,000 random keystreams through this decoder); offsets within +-3 one hypothesis.
CANDIDATE RULE (full page): z >= 6 over the page's 2,000-key null (part B), AND gain over the plain decoder >= M(page, F, mode)
unless part B dropped the arm, AND readable English (judged by eye from the recorded transliteration).
CONTROLS (6, shard 0): 262-rune English under the §59 form (p = 0.4, soft rule q 0.81): two book Vigenère words, two prime
streams at random offsets (one with literal F), two running keys at random offsets; pass = rank 1 in its family and the
candidate rule met (margin against the control's own 2,000-key 99.9th percentile).
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/wc_lane.py -> results/wc_lane_shard{k}.json; MERGE=1 -> results/wc_lane.md;
       SMOKE=1 quick check; CONTROLS_ONLY=1.
"""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import *
from score import decode, translit, S_MAX
from skip_decrypt import combine
from wc_decode import decode_wc, word_starts, word_prior
import families as F, corpus

SMOKE = os.environ.get("SMOKE") == "1"; MERGE = os.environ.get("MERGE") == "1"; CONTROLS_ONLY = os.environ.get("CONTROLS_ONLY") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(6161 + SHARD)
lu = F.lu; RES = RESULTS; CORP = Path(__file__).resolve().parent.parent / "data" / "corpus"
pages = [(p, C) for p, C in F.pages if len(C) > 0]
A = json.loads((RES / "wc_power.json").read_text()) if (RES / "wc_power.json").exists() else {}
B = json.loads((RES / "wc_margin.json").read_text()) if (RES / "wc_margin.json").exists() else {}
NUL = json.loads((RES / "wc_nulls.json").read_text()) if (RES / "wc_nulls.json").exists() else {}
CHOSEN = A.get("chosen", "wc -2.2"); P_WORD = 0.4
ARM = bool(B.get("claims", {}).get("B2", False))                     # margin arm kept only if B2 held
T1_PAGES = [0, 1, 2]; WIN = 160; Z_T1, Z_UNI = 4.5, 6.0
NREPS = 200 if SMOKE else 2000; NEIGH = 512 if SMOKE else 4096; CHUNK = 300 if SMOKE else 5000
LIMIT = 60_000; S_OFFS = 300 if SMOKE else 20_000; Q_SOFT, CTRL_N = 0.81, 262
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
LMAX = max(len(C) for _, C in pages) + S_MAX + 2

# ---------- word edges of the real pages (§42's convention)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
LPW = [parse(chunks[k]) for k in range(16, 72)]; LPW = [(c, w) for c, w in LPW if len(c)]
assert all(np.array_equal(c, C) for (c, _), (_, C) in zip(LPW, pages))
WS = {pid: word_starts(w) for (pid, _), (_, w) in zip(pages, LPW)}


def pen_of(ws): return -2.2 if CHOSEN == "wc -2.2" else word_prior(ws, P_WORD)
def wc(C, Ks, ws, f_rule, mode): s, _, d, nl = decode_wc(C, Ks, lu, ws, f_rule, mode, pen_of(ws)); return s, d, nl
def plain(C, Ks, f_rule, mode): return decode(C, Ks, lu, f_rule, mode)[0]


def null_ms(C, ws, f_rule, mode, reps=NREPS):
    sc = []
    for b in range(0, reps, 1000):
        Kr = rng.integers(0, N, size=(min(1000, reps - b), len(C) + S_MAX + 2)); sc.append(wc(C, Kr, ws, f_rule, mode)[0])
    sc = np.concatenate(sc); return float(sc.mean()), float(sc.std())


def page_null(pi, f_rule, mode):
    key = f"{pages[pi][0]}|{int(f_rule)}|{mode}"
    if key in NUL.get("nulls", {}): return NUL["nulls"][key][CHOSEN], NUL.get("margin", {}).get(key, float("inf"))
    if key not in FALLBACK: FALLBACK[key] = (list(null_ms(pages[pi][1], WS[pages[pi][0]], f_rule, mode)), float("inf"))
    return FALLBACK[key]
FALLBACK = {}

# ---------- key material
_, _, Kp3, Lp3 = F.ALLSETS[3]
VW = np.array([i for i, (f, _) in enumerate(Lp3) if f in ("vigenere-word", "vigenere-word-rev")])
def sieve(n):
    s = np.ones(n, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)
PR = sieve(400_000)[:S_OFFS + LMAX + 10]; assert len(PR) >= S_OFFS + LMAX
PRS = sliding_window_view(PR, LMAX)[:S_OFFS]                                   # (S_OFFS, LMAX): p[n+s]
PRIME_VARIANTS = (("p-1", -1), ("p", 0), ("p+1", 1))
texts = {}
for f in ("corpus.json", "corpus_pilgrim.json", "corpus_cicada.json"):
    for k, v in json.loads((CORP / f).read_text()).items(): texts[k] = (np.asarray(v["runes"], dtype=np.int64), np.asarray(v["sentence_starts"], dtype=np.int64))
EXACT = [k for k, (s, _) in texts.items() if len(s) <= LIMIT]; SENT = [k for k in texts if k not in EXACT]
def windows(s, offs, L):
    offs = np.asarray(offs, dtype=np.int64)
    if len(s) < offs.max() + L + 1: s = np.concatenate([s, s[:L + 1]])
    return sliding_window_view(s, L)[offs]
def signed(K, sign): return (-K) % N if sign == "add" else K % N

units = [("book", si, pi) for si in range(len(F.ALLSETS)) for pi in range(len(pages))]
units += [("prime", pi, vi) for pi in range(len(pages)) for vi in range(3)]
for k in EXACT:
    n = len(texts[k][0])
    for rev in (False, True):
        for a in range(0, n, CHUNK): units.append(("text", k, rev, np.arange(a, min(a + CHUNK, n))))
for k in SENT: units.append(("text", k, False, texts[k][1]))
if SMOKE: units = [u for u in units if u[0] == "book"][:1] + [u for u in units if u[0] == "prime"][:1] + [u for u in units if u[0] == "text"][:1]
mine = [u for j, u in enumerate(units) if j % NSHARD == SHARD]

# ---------- plants (controls): §60's writer under the §59 form
text = corpus.TEXTS["emerson_essays1"][0](); EWORDS = [np.array(english_to_runes(w), dtype=np.int64) for w in re.findall(r"[A-Za-z']+", text)]; EWORDS = [w for w in EWORDS if len(w)]
def plant(K, f_rule, sign, n, p=P_WORD):
    C, W, j, prev, k0 = [], [], 0, None, int(rng.integers(0, len(EWORDS) - 3 * n))
    def real(pch):
        nonlocal j, prev
        if f_rule and pch == 0: c = 0
        else:
            c = combine(int(pch), K[j], sign)
            while prev is not None and c == prev and rng.random() < Q_SOFT: j += 1; c = combine(int(pch), K[j], sign)
            j += 1
        C.append(int(c)); prev = int(c)
    def fill():
        nonlocal prev
        f = int(rng.integers(0, N - 1)); f = f if (prev is None or f < prev) else f + 1; C.append(f); prev = f
    for k, w in enumerate(EWORDS[k0:]):
        pos = int(rng.integers(0, len(w) + 1)) if (len(w) >= 2 and rng.random() < p) else -1; start = len(C)
        for i, pch in enumerate(w):
            if i == pos: fill()
            real(pch)
        if pos == len(w): fill()
        W += [k] * (len(C) - start)
        if len(C) >= n: break
    return np.array(C[:n]), word_starts(np.array(W[:n]))

# ---------- merge
if MERGE:
    shards = sorted(RES.glob("wc_lane_shard*.json")); D = [json.loads(p.read_text()) for p in shards]
    surv = [r for d in D for r in d["survivors"]]; cand = [r for d in D for r in d["candidates"]]; ctrl = [c for d in D for c in d["controls"]]
    nt = {lib: sum(d["ntests"].get(lib, 0) for d in D) for lib in ("book", "prime", "text")}; zmax = {lib: max([d["zmax"].get(lib, -9) for d in D]) for lib in nt}
    secs = max(d["seconds"] for d in D)
    out = [f"# The small libraries under the word-constrained filler decoder (§61 part C)", "",
           f"Decoder: {CHOSEN} (part A). Nulls and margins from part B; margin arm {'kept' if ARM else 'dropped (B2 failed)'}. Libraries: (1) the book's {sum(len(L) for _, _, _, L in F.ALLSETS):,} key-sign configurations × 2 F × {len(pages)} pages at full length; (2) prime streams p[n+s], p[n+s]−1, p[n+s]+1, s = 0…{S_OFFS-1:,}, × 3 signs × 2 F × {len(pages)} pages; (3) {len(EXACT)} texts at every offset both directions and {len(SENT)} longer texts at sentence starts, tier 1 on the first {WIN} runes of LP2-00/01/02 × 3 signs × 2 F at z ≥ {Z_T1}. Candidate: z ≥ {Z_UNI:.0f} over the page's {NREPS:,}-key null{' and gain ≥ M(page, F, mode)' if ARM else ''} and readable.", "",
           "| library | tests | largest z | survivors (z ≥ bar) | candidates |", "|---|---|---|---|---|"]
    for lib in nt: out.append(f"| {lib} | {nt[lib]:,} | {zmax[lib]:.2f} | {sum(r['lib'] == lib for r in surv)} | {sum(r['lib'] == lib for r in cand)} |")
    out += ["", f"Controls: **{sum(c['pass'] for c in ctrl)}/{len(ctrl)}**.", "", "| control | family | sign | F | z | rank | gain | M | pass |", "|---|---|---|---|---|---|---|---|---|"]
    for c in ctrl: out.append(f"| {c['id']} | {c['fam']} | {c['sign']} | {int(c['F'])} | {c['z']:.1f} | {c['rank']} | {c['gain']:+.0f} | {c['M']:+.0f} | {'PASS' if c['pass'] else 'miss'} |")
    if surv:
        out += ["", "## Survivors (full page, z ≥ 6 by the decoder's own null; the text column is the decoded page's first 80 runes, for the readability judgement)", "", "| lib | key | page | sign | F | z | gain | M | text |", "|---|---|---|---|---|---|---|---|---|"]
        for r in sorted(surv, key=lambda r: -r["z"])[:60]: out.append(f"| {r['lib']} | {r['key']} | {r['page']} | {r['sign']} | {int(r['F'])} | {r['z']:.2f} | {r['gain']:+.0f} | {r['M'] if r['M'] != float('inf') else '—'} | {r['tr']} |")
    out += ["", f"Runtime, longest shard: {secs/3600:.1f} h on {len(shards)} shards. Reproduce: `for k in 0..7: SHARD=$k NSHARD=8 .venv/bin/python -I src/wc_lane.py`, then `MERGE=1`.", ""]
    (RES / "wc_lane.md").write_text("\n".join(out)); json.dump(dict(ntests=nt, zmax=zmax, survivors=surv, candidates=cand, controls=ctrl, chosen=CHOSEN, arm=ARM, ntests_total=sum(nt.values())), open(RES / "wc_lane.json", "w"), indent=1)
    print("\n".join(out)); sys.exit(0)

t0 = time.time(); survivors, candidates, controls = [], [], []; ntests = {"book": 0, "prime": 0, "text": 0}; zmax = {"book": -9.0, "prime": -9.0, "text": -9.0}


def full_check(lib, key, pi, Kfull, f_rule, sign, mode, z=None):
    """Full-page check of one key on one page: z by part B's null, gain over plain, margin, transliteration."""
    pid, C = pages[pi]; ws = WS[pid]; (m0, s0), M = page_null(pi, f_rule, mode)
    s, d, nl = wc(C, Kfull[None, :], ws, f_rule, mode); zz = float((s[0] - m0) / s0) if z is None else z
    gain = float(s[0] - plain(C, Kfull[None, :], f_rule, mode)[0])
    row = dict(lib=lib, key=key, page=pid, sign=sign, F=f_rule, z=zz, gain=gain, M=M, nulls=int(nl[0].sum()), tr=translit(d[0][:80]))
    survivors.append(row)
    if zz >= Z_UNI and (not ARM or gain >= M): candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    return row


# ---------- controls
if SHARD == 0 or SMOKE or CONTROLS_ONLY:
    specs = [("vigenere-word", 0), ("vigenere-word", 1), ("prime", 2), ("prime", 3), ("running key", 4), ("running key", 5)]
    for fam, ci in (specs if not SMOKE else specs[::2]):
        sign, mode = SIGNS[ci % 3]; f_rule = bool(ci in (3, 5, 1)); L = CTRL_N + S_MAX + 2
        if fam == "vigenere-word":
            ki = int(rng.choice([i for i in VW if Lp3[i][0] == "vigenere-word"])); K = Kp3[ki, :L]; Kfam = Kp3[VW][:, :L]; pos = int(np.where(VW == ki)[0][0]); label = Lp3[ki][1]
        elif fam == "prime":
            vn, dv = PRIME_VARIANTS[ci % 3]; s0_ = int(rng.integers(2000, S_OFFS - 2000)) if S_OFFS > 4000 else int(rng.integers(0, S_OFFS))
            lo, hi = max(0, s0_ - 2000), min(S_OFFS, s0_ + 2000); Kfam = (PRS[lo:hi, :L] + dv) % N; pos = s0_ - lo; K = Kfam[pos]; label = f"{vn}[n+{s0_}]"
        else:
            tname = EXACT[ci % len(EXACT)]; rev = bool(ci % 2); s = texts[tname][0]; s = s[::-1] if rev else s; o = int(rng.integers(0, len(s)))
            offs = np.arange(o - NEIGH // 2, o + NEIGH // 2) % len(s); Kfam = windows(s, offs, L); pos = NEIGH // 2; K = Kfam[pos]; label = f"{tname}{' rev' if rev else ''} @{o}"
        C, ws = plant(K, f_rule, sign, CTRL_N); Kd = signed(Kfam, sign)
        Kr = [rng.integers(0, N, size=(1000, L)) for _ in range(NREPS // 1000 or 1)]
        nul = np.concatenate([wc(C, k, ws, f_rule, mode)[0] for k in Kr]); gains = np.concatenate([wc(C, k, ws, f_rule, mode)[0] - plain(C, k, f_rule, mode) for k in Kr])
        M = float(np.percentile(gains, 99.9))
        sc = np.concatenate([wc(C, Kd[b:b + 1000], ws, f_rule, mode)[0] for b in range(0, len(Kd), 1000)])
        z = (sc - nul.mean()) / nul.std(); zt = float(z[pos]); rank = int((z > zt).sum()) + 1
        gain = float(sc[pos] - plain(C, Kd[pos][None, :], f_rule, mode)[0])
        ok = bool(rank == 1 and zt >= Z_UNI and (not ARM or gain >= M))
        controls.append(dict(id=f"control-{ci}", fam=fam, key=label, sign=sign, F=f_rule, z=zt, rank=rank, gain=gain, M=M, **{"pass": ok}))
        print(f"  control {ci} {fam} {label} {sign} F={int(f_rule)}: z {zt:.1f} rank {rank} gain {gain:+.0f} M {M:+.0f} -> {'PASS' if ok else 'miss'} [{time.time()-t0:.0f}s]", flush=True)
    print(f"controls: {sum(c['pass'] for c in controls)}/{len(controls)}", flush=True)
    if CONTROLS_ONLY: json.dump(dict(controls=controls), open(RES / "wc_lane_controls.json", "w"), indent=1); sys.exit(0)

# ---------- window nulls for the text tier
WNULL = {}
if any(u[0] == "text" for u in mine):
    for pi in T1_PAGES:
        for f_rule in (False, True):
            for mode in ("sub", "beaufort"): WNULL[(pi, f_rule, mode)] = null_ms(pages[pi][1][:WIN], WS[pages[pi][0]][:WIN], f_rule, mode)
    print(f"window nulls ready [{time.time()-t0:.0f}s]", flush=True)

# ---------- the sweep
for ui, u in enumerate(mine):
    lib = u[0]
    if lib == "book":
        _, si, pi = u; sign, mode, Kset, Lset = F.ALLSETS[si]; pid, C = pages[pi]; ws = WS[pid]; L = len(C) + S_MAX + 2
        for f_rule in (False, True):
            (m0, s0), M = page_null(pi, f_rule, mode)
            for b in range(0, len(Kset), 1000):
                Ks = Kset[b:b + 1000, :L]; z = (wc(C, Ks, ws, f_rule, mode)[0] - m0) / s0; ntests["book"] += len(Ks); zmax["book"] = max(zmax["book"], float(z.max()))
                for k in np.flatnonzero(z >= Z_UNI): full_check("book", f"{Lset[b + k][0]}:{Lset[b + k][1]}", pi, Ks[k], f_rule, sign, mode, float(z[k]))
        label = f"book set {si} ({sign}) {pid}"
    elif lib == "prime":
        _, pi, vi = u; vn, dv = PRIME_VARIANTS[vi]; pid, C = pages[pi]; ws = WS[pid]; L = len(C) + S_MAX + 2; Kv = (PRS[:, :L] + dv) % N
        for sign, mode in SIGNS:
            Kd = signed(Kv, sign)
            for f_rule in (False, True):
                (m0, s0), M = page_null(pi, f_rule, mode)
                for b in range(0, len(Kd), 1000):
                    Ks = Kd[b:b + 1000]; z = (wc(C, Ks, ws, f_rule, mode)[0] - m0) / s0; ntests["prime"] += len(Ks); zmax["prime"] = max(zmax["prime"], float(z.max()))
                    for k in np.flatnonzero(z >= Z_UNI): full_check("prime", f"{vn}[n+{b + k}]", pi, Ks[k], f_rule, sign, mode, float(z[k]))
        label = f"prime {vn} {pid}"
    else:
        _, name, rev, offs = u; s = texts[name][0]; s = s[::-1] if rev else s
        for pi in T1_PAGES:
            pid, C = pages[pi]; Cw = C[:WIN]; wsw = WS[pid][:WIN]
            for f_rule in (False, True):
                for sign, mode in SIGNS:
                    m0, s0 = WNULL[(pi, f_rule, mode)]
                    for b in range(0, len(offs), 1000):
                        ob = offs[b:b + 1000]; Ks = signed(windows(s, ob, WIN + S_MAX + 2), sign)
                        z = (wc(Cw, Ks, wsw, f_rule, mode)[0] - m0) / s0; ntests["text"] += len(ob); zmax["text"] = max(zmax["text"], float(z.max()))
                        hits = np.flatnonzero(z >= Z_T1); keep = []
                        for k in hits:
                            if not keep or int(ob[k]) - keep[-1][0] > 3 or z[k] > keep[-1][1]: keep.append((int(ob[k]), float(z[k])))   # offsets within +-3: one hypothesis, best kept
                        for off, z1 in keep:
                            Kf = signed(windows(s, [off], len(C) + S_MAX + 2)[0], sign)
                            row = full_check("text", f"{name}{' rev' if rev else ''} @{off}", pi, Kf, f_rule, sign, mode); row["z1"] = z1
        label = f"text {name}{' rev' if rev else ''} ({len(offs)} offsets)"
    if ui % 3 == 0 or ui == len(mine) - 1: print(f"  unit {ui+1}/{len(mine)} {label}: tests {sum(ntests.values()):,}, zmax {max(zmax.values()):.2f}, survivors {len(survivors)}, candidates {len(candidates)} [{time.time()-t0:.0f}s]", flush=True)

json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests=ntests, zmax=zmax, seconds=time.time() - t0, chosen=CHOSEN, arm=ARM),
          open(RES / ("wc_lane_smoke.json" if SMOKE else f"wc_lane_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD}: {sum(ntests.values()):,} tests, {len(survivors)} survivors, {len(candidates)} candidates, {time.time()-t0:.0f}s", flush=True)
