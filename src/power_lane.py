"""Detection power of the pre-registered rule by page length and key family (2026-10-27, after
external review: the z >= 6 bar was calibrated on 240-rune plants, but the unsolved pages run from
66 to 277 runes, so a family can be "excluded" on a page too short for the detector to see it).

Two lanes, both with the correct key planted and scored exactly as the sweeps score it:
  A. soft anti-repeat rule (re-draw 0.81), base decoder (phases 3-9 setting);
  B. hard rule with uniform nulls at 0.22, free-null decoder at the §22 prior (phase 10 setting).
For each length x family x REPS plants: z of the true key over 400 random-keystream nulls through
the same decoder, rank within its family (lane A), share of plaintext positions recovered.
Power = share of plants at z >= 6.  Output: results/power.md, results/power.json.
Usage: .venv/bin/python -I src/power_lane.py   (REPS env, default 20).
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, null_scores, S_MAX, MAX_SKIP
from skip_decrypt import encrypt, combine
import families as F

rng = np.random.default_rng(2301)
lu, plain, pages = F.lu, F.plain, F.pages
LENGTHS = [66, 92, 120, 160, 200, 240, 277]
FAMS = ["vigenere-word", "phrase-3", "primes", "self running key"]
REPS = int(os.environ.get("REPS", 20))
NULL_REPS = 400
PEN, Q, SOFT = -0.8, 0.22, 0.81
SETS = F.ALLSETS
Z_RULE = 6.0


def encrypt_nulls(P, K, f_rule, sign, q):
    """Same plant as null_lane.encrypt_nulls: hard skip rule, uniform null after each rune w.p. q."""
    n = len(P); C, placed, j, pi, prev = [], [], 0, 0, None
    while len(C) < n and pi < len(P):
        p = P[pi]; pi += 1
        if f_rule and p == 0:
            C.append(0); prev = 0
        else:
            c = combine(p, K[j], sign)
            while prev is not None and c == prev:
                j += 1; c = combine(p, K[j], sign)
            C.append(c); j += 1; prev = c
        placed.append(int(p))
        if len(C) < n and rng.random() < q:
            C.append(int(rng.integers(0, N))); prev = C[-1]; placed.append(-1)
    return np.array(C), np.array(placed)


rows = []
t0 = time.time()
for n in LENGTHS:
    for fam in FAMS:
        sets_with = [s for s in SETS if any(f == fam for f, _ in s[3])]
        for r in range(REPS):
            sign, mode, Ks, labs = sets_with[r % 3]
            f_rule = bool((r // 3) % 2)
            cand = np.array([i for i, (f, _) in enumerate(labs) if f == fam])
            # a constant key (one-letter Vigenère words) cannot be used under a hard rule: a collision never
            # resolves; it is skipped as a plant (the sweeps score such keys, but no hard-rule page can arise from one)
            while True:
                ki = int(rng.choice(cand))
                if not np.all(Ks[ki] == Ks[ki][0]): break
            pos = int(np.where(cand == ki)[0][0])
            Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
            o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
            # lane A: soft rule, base decoder, rank within family
            C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=SOFT, mode=sign)
            nul = null_scores(C, lu, f_rule, rng, NULL_REPS, mode)
            sc, _, dec = decode(C, Ks[cand], lu, f_rule, mode)
            z = (sc - nul.mean()) / nul.std(); zA = float(z[pos]); rankA = int((z > z[pos]).sum()) + 1
            accA = float((dec[pos] == P).mean())
            # lane B: hard rule + nulls, free-null decoder at the phase 10 prior
            Cn, placed = encrypt_nulls(P, Ktrue, f_rule, sign, Q)
            nm = np.ones(len(Cn), bool); nm[0] = False
            KsR = rng.integers(0, N, size=(NULL_REPS, len(Cn) + S_MAX + 2))
            nulB = decode(Cn, KsR, lu, f_rule, mode, None, nm, PEN)[0]
            scB, _, decB = decode(Cn, Ks[ki:ki + 1], lu, f_rule, mode, None, nm, PEN)
            zB = float((scB[0] - nulB.mean()) / nulB.std())
            real = placed >= 0; accB = float((decB[0][real] == placed[real]).mean())
            rows.append(dict(n=n, fam=fam, rep=r, sign=sign, F=f_rule, key=labs[ki][1][:30], zA=zA, rankA=rankA, accA=accA, zB=zB, accB=accB, nulls=int((~real).sum())))
        zs = [x["zA"] for x in rows if x["n"] == n and x["fam"] == fam]; zb = [x["zB"] for x in rows if x["n"] == n and x["fam"] == fam]
        print(f"n={n:3d} {fam:17s} A: z>=6 {np.mean(np.array(zs) >= Z_RULE):.2f} median z {np.median(zs):4.1f} | B: z>=6 {np.mean(np.array(zb) >= Z_RULE):.2f} median z {np.median(zb):4.1f}  [{time.time()-t0:.0f}s]", flush=True)

# ---------- summary ----------
def cellstat(lane, n, fam):
    v = np.array([x[f"z{lane}"] for x in rows if x["n"] == n and x["fam"] == fam]); a = np.array([x[f"acc{lane}"] for x in rows if x["n"] == n and x["fam"] == fam])
    return float((v >= Z_RULE).mean()), float(np.median(v)), float(np.median(a))

out = ["# Detection power of the z >= 6 rule by page length and key family", "",
       f"{REPS} plants per cell, {NULL_REPS} random-keystream nulls per plant, signs and F variants cycled; decoder max_skip {MAX_SKIP}; "
       f"lane A soft rule {SOFT} with the base decoder; lane B hard rule + uniform nulls at {Q} with the free-null decoder at prior {PEN}. "
       f"Power = share of correct keys at z >= {Z_RULE:.0f}; median z and median plaintext recovery in brackets.", ""]
for lane, title in (("A", "Lane A: soft anti-repeat rule, base decoder (phases 3-9)"), ("B", "Lane B: hard rule + 22 % nulls, free-null decoder (phase 10)")):
    out += [f"## {title}", "", "| length | " + " | ".join(FAMS) + " | all |", "|---|" + "---|" * (len(FAMS) + 1)]
    for n in LENGTHS:
        cells = [cellstat(lane, n, f) for f in FAMS]
        allv = np.array([x[f"z{lane}"] for x in rows if x["n"] == n])
        out.append(f"| {n} | " + " | ".join(f"**{p:.2f}** (z {mz:.1f}, rec {ma:.2f})" for p, mz, ma in cells) + f" | **{(allv >= Z_RULE).mean():.2f}** |")
    out.append("")
if rows and len(rows) == len(LENGTHS) * len(FAMS) * REPS:
    out += ["## Lane A rank within family", "", "| length | share of plants ranked first | median rank |", "|---|---|---|"]
    for n in LENGTHS:
        rk = np.array([x["rankA"] for x in rows if x["n"] == n]); out.append(f"| {n} | {(rk == 1).mean():.2f} | {np.median(rk):.0f} |")
    out.append("")

# which pages are below the length where power reaches 0.8 in the weakest family
L = sorted(((pid, len(C)) for pid, C in pages if len(C) > 0), key=lambda x: x[1])
out += ["## Pages below the power threshold", ""]
thr = {}
for lane in ("A", "B"):
    ok = [n for n in LENGTHS if min(cellstat(lane, n, f)[0] for f in FAMS) >= 0.8]
    thr[lane] = min(ok) if ok else None
    short = [(p, l) for p, l in L if thr[lane] is None or l < thr[lane]]
    out.append(f"- Lane {lane}: the weakest family reaches 80 % power at {thr[lane]} runes" + (f"; {len(short)} of {len(L)} pages are shorter: " + ", ".join(f"{p} ({l})" for p, l in short) if thr[lane] else "; no tested length reaches it") + ".")
out += ["", "Pages below the threshold for a lane are **inconclusive** for that lane's exclusions, not negative: the correct key can be recovered there and still fail the pre-registered rule. "
        "The page-length distribution: " + ", ".join(f"{sum(1 for _, l in L if l < t)} under {t}" for t in (100, 150, 200, 240)) + " runes of 55.", ""]
(RESULTS / "power.md").write_text("\n".join(out) + "\n")
json.dump({"config": dict(reps=REPS, null_reps=NULL_REPS, prior=PEN, q=Q, soft=SOFT, max_skip=MAX_SKIP, lengths=LENGTHS, fams=FAMS, z_rule=Z_RULE), "threshold_80": thr, "plants": rows, "seconds": time.time() - t0}, open(RESULTS / "power.json", "w"), indent=1)
print("\n".join(out)); print(f"done in {time.time()-t0:.0f}s")
