"""Irrational-digit streams under the soft re-draw rule (2026-10-28).

ItIsCuthNotCup ran the digits of pi, e, sqrt(2) and phi rigidly at 200 offsets; pnotisdev's p60-irrationals
(four-way sums, partial) and hyp-streams cover other readings.  Nobody has run the digit streams at every
offset under a skip-aware decoder.  Streams (data/processed/irrational_digits.json, 40,000 digits each):
  b10   base-10 digit as the key value (0-9);  b10p  digit pairs d1*10+d2 mod 29;  b29  base-29 digits.
Offsets 0..OFFMAX-1 (fresh offset per page); 3 signs x 2 F.  Two tiers as in src/generator_lane.py: tier 1
decodes the first 80 runes of LP2-00/01/02 and keeps cells at z >= 4.5; tier 2 decodes the full page,
candidate at z_uni >= 6 and 5-gram z_5 >= 6 and readable.  Controls: one plant per constant (4), random
offset, reading, sign and F, 262 runes of solved English under the soft rule; pass = tier-1 rank 1 among
4,096 neighbouring offsets, tier-2 z_uni >= 6 and z_5 >= 6.  Writes results/digits.md / .json.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX
from skip_decrypt import encrypt
import families as F, ngram

SMOKE = os.environ.get("SMOKE") == "1"
rng = np.random.default_rng(314159)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
T1_PAGES = [0, 1, 2]; WIN = 80
Z_T1, Z_UNI, Z_5, NREPS = 4.5, 6.0, 6.0, (200 if SMOKE else 2000)
OFFMAX = 6000 if SMOKE else 30000
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
dig = json.loads((PROCESSED / "irrational_digits.json").read_text())
STREAMS = {}
for name, d in dig.items():
    b10 = np.array([int(ch) for ch in d["b10"]]); b29 = np.array(d["b29"])
    STREAMS[f"{name} b10"] = b10
    STREAMS[f"{name} b10p"] = (b10[:-1] * 10 + b10[1:]) % N
    STREAMS[f"{name} b29"] = b29
T5 = ngram.load_dense(); t0 = time.time()

def keys_for(S, offs, L):
    idx = np.asarray(offs)[:, None] + np.arange(L)[None, :]
    return S[idx] % N

def null_stats(C, f_rule, mode, with5=False):
    Kr = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2)); sc, _, dec = decode(C, Kr, lu, f_rule, mode)
    if not with5: return sc.mean(), sc.std()
    s5 = ngram.score_batch(dec, T5); return sc.mean(), sc.std(), s5.mean(), s5.std()

W = {}; FULL = {}
for pi_ in T1_PAGES:
    pid, C = pages[pi_]
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            W[(pi_, f_rule, mode)] = null_stats(C[:WIN], f_rule, mode); FULL[(pi_, f_rule, mode)] = null_stats(C, f_rule, mode, with5=True)
print(f"nulls ready [{time.time()-t0:.0f}s]", flush=True)

def tier1(S, offs, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; Ks = keys_for(S, offs, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
    m0, s0 = W[(pi_, f_rule, mode)]; return (decode(C[:WIN], Ks, lu, f_rule, mode)[0] - m0) / s0

def tier2(S, off, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; K = keys_for(S, [off], len(C) + S_MAX + 2); K = (-K) % N if sign == "add" else K
    m0, s0, m5, s5 = FULL[(pi_, f_rule, mode)]; sc, _, dec = decode(C, K, lu, f_rule, mode)
    return float((sc[0] - m0) / s0), float((ngram.score_batch(dec, T5)[0] - m5) / s5), translit(dec[0][:80])

# controls
controls = []
names = list(STREAMS)
for ci, const in enumerate(dig):
    sname = f"{const} {['b10', 'b10p', 'b29'][ci % 3]}"; S = STREAMS[sname]
    sign, mode = SIGNS[ci % 3]; f_rule = bool(ci % 2); off = int(rng.integers(2048, OFFMAX - 2048))
    n = 262; K = keys_for(S, [off], n + S_MAX + 2)[0]
    o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
    C = encrypt(P, K, f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
    block = np.arange(off - 2048, off + 2048); pos = 2048
    Ks = keys_for(S, block, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
    m0, s0 = null_stats(C[:WIN], f_rule, mode); z1 = (decode(C[:WIN], Ks, lu, f_rule, mode)[0] - m0) / s0; rank1 = int((z1 > z1[pos]).sum()) + 1
    m0f, s0f, m5, s5 = null_stats(C, f_rule, mode, with5=True); Kf = keys_for(S, [off], n + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
    sc, _, dec = decode(C, Kf, lu, f_rule, mode); z2 = float((sc[0] - m0f) / s0f); z5 = float((ngram.score_batch(dec, T5)[0] - m5) / s5)
    passed = z1[pos] >= Z_T1 and rank1 == 1 and z2 >= Z_UNI and z5 >= Z_5
    controls.append(dict(stream=sname, offset=off, sign=sign, F=f_rule, z1=float(z1[pos]), rank1=rank1, z2=z2, z5=z5, passed=bool(passed)))
    print(f"  control {sname} off {off} {sign} F={f_rule}: tier1 z {z1[pos]:.1f} rank {rank1}; tier2 z_uni {z2:.1f} z_5 {z5:.1f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

survivors, candidates, nt1, nt2, zmax = [], [], 0, 0, {}
BATCH = 2048
for sname, S in STREAMS.items():
    offs_all = np.arange(0, min(OFFMAX, len(S) - 600))
    for b in range(0, len(offs_all), BATCH):
        offs = offs_all[b:b + BATCH]
        for pi_ in T1_PAGES:
            for sign, mode in SIGNS:
                for f_rule in (False, True):
                    z = tier1(S, offs, pi_, sign, mode, f_rule); nt1 += len(offs); zmax[sname] = max(zmax.get(sname, -9), float(z.max()))
                    for k in np.where(z >= Z_T1)[0]:
                        z2, z5, tr = tier2(S, int(offs[k]), pi_, sign, mode, f_rule); nt2 += 1
                        row = dict(stream=sname, offset=int(offs[k]), page=pages[pi_][0], sign=sign, F=f_rule, z1=float(z[k]), z2=z2, z5=z5, translit=tr); survivors.append(row)
                        if z2 >= Z_UNI and z5 >= Z_5: candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    print(f"  {sname} done: {nt1:,} tier-1 tests, max tier-1 z {zmax[sname]:.2f}, {len(survivors)} survivors, {len(candidates)} candidates  [{time.time()-t0:.0f}s]", flush=True)

out = [f"# Irrational-digit streams under the soft rule: pi, e, sqrt 2, phi in three readings, offsets 0..{OFFMAX-1:,}", "",
       f"Tier 1: {nt1:,} window decodes (80 runes, pages LP2-00/01/02, 6 cells); survivors at z >= {Z_T1}: {len(survivors)}. Tier 2: {nt2:,} full-page decodes; candidates at z_uni >= {Z_UNI} and z_5 >= {Z_5}: {len(candidates)}.", "",
       "## Controls", "", "| stream | offset | sign | F | tier-1 z (rank) | tier-2 z_uni | z_5 | pass |", "|---|---|---|---|---|---|---|---|"]
for c in controls: out.append(f"| {c['stream']} | {c['offset']} | {c['sign']} | {c['F']} | {c['z1']:.1f} ({c['rank1']}) | {c['z2']:.1f} | {c['z5']:.1f} | {'yes' if c['passed'] else 'no'} |")
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Largest tier-1 z per stream", "", "| stream | max tier-1 z |", "|---|---|"] + [f"| {k} | {v:.2f} |" for k, v in zmax.items()]
out += ["", "## Tier-1 survivors (top 20 by tier-2 z_uni)", "", "| stream | offset | page | sign | F | tier-1 z | tier-2 z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|---|"]
for s_ in sorted(survivors, key=lambda r: -r["z2"])[:20]: out.append(f"| {s_['stream']} | {s_['offset']} | {s_['page']} | {s_['sign']} | {s_['F']} | {s_['z1']:.2f} | {s_['z2']:.2f} | {s_['z5']:.1f} | {s_['translit'][:50]} |")
out += ["", "## Candidates", ""] + ([f"- {c}" for c in candidates] or ["None."]) + ["", f"Largest tier-2 z_uni: {max((s_['z2'] for s_ in survivors), default=0):.2f}; largest z_5: {max((s_['z5'] for s_ in survivors), default=0):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / ("digits_smoke.md" if SMOKE else "digits.md")).write_text("\n".join(out) + "\n")
json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests_t1=nt1, ntests_t2=nt2, zmax=zmax, seconds=time.time() - t0), open(RESULTS / ("digits_smoke.json" if SMOKE else "digits.json"), "w"), indent=1)
print("\n".join(out[:3] + out[-3:]))
