"""Stream keys at the cumulative page position (lane C11, 2026-10-31; registered in results/quorum_checks_registration.md).

Words run across page joins (§71), so if a stream key runs through the whole unsolved section, page k reads it at its
cumulative position cum_k = runes of the pages before k, less the fillers (which consume no key) plus the skips.  The
filler-aware lanes reached stream offsets 0-1,999 only (§55 C, §62); §54 reached 19,672 with the plain decoder, whose power
against the filler form is 0.02 (§60).  This lane runs the free-null decoder (§62's instrument, unchanged: prior -2.2, tier 1
on the first 160 runes at z >= 4.5, tier 2 on the full page at z_uni >= 6 and free - plain >= 20 nats, readable) over the
580 non-periodic pnotisdev streams and the three prime streams (p, p-1, p+1 mod 29) at offsets 0.90*cum_k - 50 .. cum_k + 50
for every page k, 3 signs x 2 F.  Acceptance: §62's rule unchanged (z_uni >= 6, rank 1 in its stream and sign, above the
empirical null maximum, readable).  Controls: six plants (§62's filler form, r 0.10, q 0.81) at the cumulative offset of six
pages, one per sign x F, each decoded over its page's registered window.  Work units are streams; SHARD/NSHARD split them.
Reproduce: SHARD=k NSHARD=8 .venv/bin/python -I src/cumulative_lane.py (controls on shard 0), then MERGE=1.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import N, RESULTS, english_to_runes
from score import decode, translit, S_MAX
from skip_decrypt import combine
import families as F, corpus, pnotisdev_library as PL

t0 = time.time(); SMOKE = os.environ.get("SMOKE") == "1"; MERGE = os.environ.get("MERGE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(7777 + SHARD); lu = F.lu
pages = [(p, C) for p, C in F.pages if len(C) > 0]; assert len(pages) == 55
PEN = -2.2; WIN = 160; Z_T1, Z_UNI, FREE_BASE = 4.5, 6.0, 20.0; NREPS = 200 if SMOKE else 2000
R_FILL, Q_SOFT = 0.10, 0.81; SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort")); OUT = "cumulative_lane"
CUM = np.concatenate([[0], np.cumsum([len(C) for _, C in pages])[:-1]])          # cumulative rune position of each page's first rune within the section


def window_of(k):
    lo = max(0, int(np.floor(0.90 * CUM[k])) - 50); hi = int(CUM[k]) + 50
    return np.arange(lo, hi + 1)


WINDOWS = [window_of(k) for k in range(55)]
if SMOKE: WINDOWS = [w[-60:] for w in WINDOWS]

# ---------- key material: the 580 non-periodic pnotisdev streams and the three prime streams
names, fams, periods, KP = PL.load(); NONPER = [i for i, p in enumerate(periods) if not p]


def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)


PR = sieve(300000)[:20000]
STREAMS = [(f"pn:{names[i]}", KP[i].astype(np.int64)) for i in NONPER] + [("prime p", PR % N), ("prime p-1", (PR - 1) % N), ("prime p+1", (PR + 1) % N)]
NEED = int(CUM[-1]) + 50 + max(len(C) for _, C in pages) + S_MAX + 2
STREAMS = [(n, s) for n, s in STREAMS if len(s) >= NEED]
if SMOKE: STREAMS = STREAMS[:3] + STREAMS[-3:]
mine = [u for j, u in enumerate(STREAMS) if j % NSHARD == SHARD]


def windows(s, offs, L): return sliding_window_view(s, L)[np.asarray(offs, dtype=np.int64)]


def dec(C, Ks, f_rule, mode, free=True):
    if not free: return decode(C, Ks, lu, f_rule, mode)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, None, nm, PEN)


def null_ms(C, f_rule, mode, reps=NREPS, batch=500):
    sc = []
    for b in range(0, reps, batch):
        Kr = rng.integers(0, N, size=(min(batch, reps - b), len(C) + S_MAX + 2)); sc.append(dec(C, Kr, f_rule, mode)[0])
    sc = np.concatenate(sc); return float(sc.mean()), float(sc.std()), float(sc.max())


# ---------- plants (§62's form)
text = corpus.TEXTS["emerson_essays1"][0](); EP = np.array(english_to_runes(text), dtype=np.int64)
def encrypt_fill(P, K, f_rule, sign, r, n):
    C, j, pi, prev = [], 0, 0, None
    while len(C) < n:
        p = int(P[pi]); pi += 1
        if f_rule and p == 0: C.append(0); prev = 0
        else:
            c = combine(p, K[j], sign)
            while prev is not None and c == prev and rng.random() < Q_SOFT: j += 1; c = combine(p, K[j], sign)
            C.append(int(c)); j += 1; prev = int(c)
        if len(C) < n and rng.random() < r:
            f = int(rng.integers(0, N - 1)); f = f if f < prev else f + 1; C.append(f); prev = f
    return np.array(C[:n])


# ---------- merge
if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RESULTS.glob(f"{OUT}_shard*.json"))] or [json.loads((RESULTS / f"{OUT}_smoke.json").read_text())]
    ctr = [c for d in shards for c in d["controls"]]; surv = sorted([s for d in shards for s in d["survivors"]], key=lambda r: -r["z2"])
    cands = [c for d in shards for c in d["candidates"]]; nt = sum(d["ntests"] for d in shards); zmax1 = max(d["zmax1"] for d in shards)
    nstreams = sum(d["nstreams"] for d in shards); secs = max(d["seconds"] for d in shards); noffs = sum(len(w) for w in WINDOWS)
    out = ["# Stream keys at the cumulative page position (lane C11) under the free-null decoder", "",
           f"Registration: `results/quorum_checks_registration.md` (C11). {nstreams} streams (580 non-periodic pnotisdev streams, three prime streams) at offsets 0.90·cum_k − 50 … cum_k + 50 for each page k ({noffs:,} page-offsets; cum_54 = {int(CUM[-1]):,}), 3 signs × 2 F; tier 1 on the first {WIN} runes at z ≥ {Z_T1}, tier 2 on the full page at z_uni ≥ {Z_UNI:.0f} and free − plain ≥ {FREE_BASE:.0f} nats and readable. **{nt:,} window decodes.** Chance maximum of z over that many tests about {np.sqrt(2*np.log(max(nt,2))):.1f}.", "",
           "## Controls (six plants at the cumulative offset of a page, §62's filler form)", "", "| id | page | stream | sign | F | planted offset | top offset | z1 | rank | z2 | free − plain | pass |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    out += [f"| {c['id']} | {c['page']} | {c['stream']} | {c['sign']} | {int(c['F'])} | {c['offset']} | {c['top']} | {c['z1']:.1f} | {c['rank']} | {c['z2']:.1f} | {c['fb']:+.0f} | {'yes' if c['pass'] else 'no'} |" for c in ctr]
    out += ["", f"Controls passing: {sum(c['pass'] for c in ctr)} of {len(ctr)}.", "", "## Sweep", "", f"Largest tier-1 z: {zmax1:.2f}. Tier-1 survivors (z ≥ {Z_T1}): {len(surv):,}. Candidates: {len(cands)}.", ""]
    out += [f"- **{c['name']}** page {c['page']} {c['sign']} F={c['F']} offset {c['offset']}: z_uni {c['z2']:.2f}, free − plain {c['fb']:+.0f}: `{c['tr']}`" for c in cands] or ["None. No accepted decoding within the tested configurations at the stated detection limits."]
    out += ["", "Top tier-1 survivors by full-page z:", "", "| stream | page | sign | F | offset | cum_k | z1 | z2 | free − plain | above null max | transliteration |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    out += [f"| {s['name']} | {s['page']} | {s['sign']} | {int(s['F'])} | {s['offset']} | {s['cum']} | {s['z1']:.1f} | {s['z2']:.2f} | {s['fb']:+.0f} | {'yes' if s['above_max'] else 'no'} | `{s['tr'][:48]}` |" for s in surv[:15]]
    out += ["", f"Coverage limits: the window is 0.90·cum_k − 50 … cum_k + 50 (a filler share above 10 % or skips beyond 50 fall outside); the 580 non-periodic streams and three prime streams only; the free-null decoder at one prior; tier-1 power at 160 runes from §55 part B. Runtime, longest shard: {secs/3600:.1f} h on {len(shards)} shards.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(out)); print("\n".join(out)); sys.exit(0)

# ---------- nulls per page window (the first WIN runes) and per full page
WNULL, FULL = {}, {}
for k, (pid, C) in enumerate(pages):
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"): WNULL[(k, f_rule, mode)] = null_ms(C[:WIN], f_rule, mode)
print(f"window nulls ready [{time.time()-t0:.0f}s]; {len(mine)} of {len(STREAMS)} streams on this shard; {sum(len(w) for w in WINDOWS):,} page-offsets", flush=True)


def tier2(C, Kfull, f_rule, mode, key):
    if key not in FULL: FULL[key] = null_ms(C, f_rule, mode)
    m0, s0, mx = FULL[key]; s2, _, d = dec(C, Kfull, f_rule, mode); s1 = dec(C, Kfull, f_rule, mode, free=False)[0]
    return float((s2[0] - m0) / s0), float(s2[0] - s1[0]), translit(d[0][:80]), bool(s2[0] > mx)


# ---------- controls: six plants at cum_k on six pages, one per sign x F, decoded over the page's registered window
controls = []
if SHARD == 0 or SMOKE:
    for ci in range(6 if not SMOKE else 2):
        sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 3) % 2); k = [5, 14, 23, 32, 41, 50][ci]; pid, Cpage = pages[k]; n = len(Cpage)
        sname, s = STREAMS[int(rng.integers(len(STREAMS)))]; o = int(CUM[k]); K = windows(s, [o], n + S_MAX + 2)[0]
        p0 = int(rng.integers(0, len(EP) - 2 * n)); C = encrypt_fill(EP[p0:p0 + 2 * n], K, f_rule, sign, R_FILL, n)
        offs = WINDOWS[k]; m0, s0, _ = null_ms(C[:WIN], f_rule, mode); Ks = windows(s, offs, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
        z = (dec(C[:WIN], Ks, f_rule, mode)[0] - m0) / s0; top = int(offs[int(z.argmax())])
        near = np.abs(offs - o) <= 3; zt = float(z[near].max()); rank = int((z[~near] > zt).sum()) + 1
        Kf = windows(s, [o], n + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
        z2, fb, tr, _ = tier2(C, Kf, f_rule, mode, ("ctrl", ci)); ok = bool(rank == 1 and zt >= Z_T1 and z2 >= Z_UNI and fb >= FREE_BASE)
        controls.append(dict(id=f"control-{ci:02d}", page=pid, stream=sname, sign=sign, F=f_rule, offset=o, top=top, z1=zt, rank=rank, z2=z2, fb=fb, tr=tr, **{"pass": ok}))
        print(f"  control {ci} {pid} {sname} {sign} F={int(f_rule)} planted {o}: top {top} z1 {zt:.1f} rank {rank} | z2 {z2:.1f} fb {fb:+.0f} -> {'PASS' if ok else 'miss'} [{time.time()-t0:.0f}s]", flush=True)
    print(f"controls: {sum(c['pass'] for c in controls)}/{len(controls)}", flush=True)

# ---------- the sweep: every stream on this shard, every page at its own window, 3 signs x 2 F
survivors, candidates, ntests, zmax1 = [], [], 0, -9.0
for ui, (sname, s) in enumerate(mine):
    for k, (pid, C) in enumerate(pages):
        Cw = C[:WIN]; offs = WINDOWS[k]
        for f_rule in (False, True):
            for sign, mode in SIGNS:
                m0, s0, _ = WNULL[(k, f_rule, mode)]
                for b in range(0, len(offs), 1000):
                    ob = offs[b:b + 1000]; Ks = windows(s, ob, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
                    z = (dec(Cw, Ks, f_rule, mode)[0] - m0) / s0; ntests += len(ob); zmax1 = max(zmax1, float(z.max()))
                    for j in np.flatnonzero(z >= Z_T1):
                        off = int(ob[j]); Kf = windows(s, [off], len(C) + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
                        z2, fb, tr, above = tier2(C, Kf, f_rule, mode, (k, f_rule, mode))
                        row = dict(name=sname, page=pid, cum=int(CUM[k]), sign=sign, F=f_rule, offset=off, z1=float(z[j]), z2=z2, fb=fb, tr=tr, above_max=above); survivors.append(row)
                        if z2 >= Z_UNI and fb >= FREE_BASE: candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    print(f"  stream {ui+1}/{len(mine)} {sname}: {ntests:,} tests, zmax1 {zmax1:.2f}, survivors {len(survivors)} [{time.time()-t0:.0f}s]", flush=True)

json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests=ntests, zmax1=zmax1, nstreams=len(mine), seconds=time.time() - t0, prior=PEN),
          open(RESULTS / (f"{OUT}_smoke.json" if SMOKE else f"{OUT}_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD}: {ntests:,} tests, {len(survivors)} survivors, {len(candidates)} candidates, {time.time()-t0:.0f}s", flush=True)
