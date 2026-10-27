"""Rescoring power (2026-10-27): does a rune 5-gram rescoring of the decoder's output raise detection
power on short pages?  Same plants as the §23 power lane (soft rule 0.81, base decoder, four families,
signs and F cycled, 20 per cell) at the nine short-page lengths; for each plant z_uni (decoder score
over 400 random keystreams) and z_5 (5-gram log-probability of the decoded text over the 5-gram
score of the same 400 random keystreams' decodes).  Power = share at z_5 >= 6 (the rescoring rule
for §27), reported next to the share at z_uni >= 6 (the §23 rule).
Usage: .venv/bin/python -I src/rescore_power.py
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F, ngram

T5 = ngram.load_dense()
rng = np.random.default_rng(5150)
lu, plain = F.lu, F.plain
LENGTHS = [66, 76, 92, 121, 137, 159, 196]
FAMS = ["vigenere-word", "phrase-3", "primes", "self running key"]
REPS, NULL_REPS, SOFT = 20, 400, 0.81
rows = []; t0 = time.time()
for n in LENGTHS:
    for fam in FAMS:
        sets_with = [s for s in F.ALLSETS if any(f == fam for f, _ in s[3])]
        for r in range(REPS):
            sign, mode, Ks, labs = sets_with[r % 3]; f_rule = bool((r // 3) % 2)
            cand = [i for i, (f, _) in enumerate(labs) if f == fam]
            while True:
                ki = int(rng.choice(cand))
                if not np.all(Ks[ki] == Ks[ki][0]): break
            Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
            o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
            C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=SOFT, mode=sign)
            KsR = rng.integers(0, N, size=(NULL_REPS, n + S_MAX + 2))
            sc0, _, dec0 = decode(C, KsR, lu, f_rule, mode); s5_0 = ngram.score_batch(dec0, T5)
            sc, _, dec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode); s5 = ngram.score_batch(dec, T5)[0]
            rows.append(dict(n=n, fam=fam, sign=sign, F=f_rule, zu=float((sc[0] - sc0.mean()) / sc0.std()), z5=float((s5 - s5_0.mean()) / s5_0.std()), acc=float((dec[0] == P).mean())))
        zu = np.array([x["zu"] for x in rows if x["n"] == n and x["fam"] == fam]); z5 = np.array([x["z5"] for x in rows if x["n"] == n and x["fam"] == fam])
        print(f"n={n:3d} {fam:17s} z_uni>=6 {np.mean(zu>=6):.2f} (median {np.median(zu):.1f}) | z_5>=6 {np.mean(z5>=6):.2f} (median {np.median(z5):.1f})  [{time.time()-t0:.0f}s]", flush=True)

out = ["# Rescoring power: rune 5-gram on the decoder's output, by page length", "",
       f"{REPS} plants per cell, {NULL_REPS} nulls, soft rule {SOFT}, base decoder, max_skip {MAX_SKIP}; 5-gram trained on the running-key corpus (results/ngram5.npz, held-out solved plaintext −1.96 nats/rune against −3.37 uniform).", "",
       "| length | share z_uni ≥ 6 (median) | share z_5 ≥ 6 (median) | share z_5 ≥ 7 | median recovery |", "|---|---|---|---|---|"]
for n in LENGTHS:
    zu = np.array([x["zu"] for x in rows if x["n"] == n]); z5 = np.array([x["z5"] for x in rows if x["n"] == n]); ac = np.array([x["acc"] for x in rows if x["n"] == n])
    out.append(f"| {n} | {np.mean(zu>=6):.2f} ({np.median(zu):.1f}) | **{np.mean(z5>=6):.2f}** ({np.median(z5):.1f}) | {np.mean(z5>=7):.2f} | {np.median(ac):.2f} |")
out += ["", "Per family at the two shortest lengths:", "", "| length | family | z_uni ≥ 6 | z_5 ≥ 6 |", "|---|---|---|---|"]
for n in LENGTHS[:3]:
    for fam in FAMS:
        zu = np.array([x["zu"] for x in rows if x["n"] == n and x["fam"] == fam]); z5 = np.array([x["z5"] for x in rows if x["n"] == n and x["fam"] == fam])
        out.append(f"| {n} | {fam} | {np.mean(zu>=6):.2f} | {np.mean(z5>=6):.2f} |")
out.append("")
(RESULTS / "rescore_power.md").write_text("\n".join(out) + "\n")
json.dump(dict(rows=rows, seconds=time.time() - t0), open(RESULTS / "rescore_power.json", "w"), indent=1)
print("\n".join(out)); print(f"done in {time.time()-t0:.0f}s")
