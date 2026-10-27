# Can a better scorer rescue the key-reuse test?

Difference-of-plaintext model trained on 1488 runes of solved plaintext, tested on the other 1489. KL(q ‖ uniform) per rune = 0.0254 nats.
Threshold at FPR 2e-06 (the phase-1 scan size). Power = fraction of true shared-key pairs that clear it. sigma = (mean under reuse − mean under null) / null sd.

| overlap n | scorer | sigma per pair | power at FPR 2e-6 | empirical 1e-4 tail vs normal fit |
|---|---|---|---|---|
| 60 | ic | 0.44 | 0.004 | 0.05876 vs 0.05059 |
| 60 | kappa | 1.17 | 0.001 | 9 vs 7.315 |
| 60 | uni | 1.73 | 0.005 | 5.079 vs 4.798 |
| 60 | bigram | 1.58 | 0.004 | 5.912 vs 5.82 |
| 100 | ic | 0.73 | 0.007 | 0.04788 vs 0.04412 |
| 100 | kappa | 1.49 | 0.003 | 12 vs 10.24 |
| 100 | uni | 2.21 | 0.014 | 5.703 vs 5.632 |
| 100 | bigram | 2.02 | 0.008 | 6.617 vs 6.591 |
| 150 | ic | 1.10 | 0.014 | 0.04313 vs 0.04091 |
| 150 | kappa | 1.82 | 0.004 | 15 vs 13.49 |
| 150 | uni | 2.70 | 0.036 | 6.674 vs 6.268 |
| 150 | bigram | 2.46 | 0.019 | 6.664 vs 6.979 |
| 250 | ic | 1.86 | 0.048 | 0.03974 vs 0.03833 |
| 250 | kappa | 2.38 | 0.011 | 21 vs 19.34 |
| 250 | uni | 3.51 | 0.141 | 6.842 vs 6.679 |
| 250 | bigram | 3.19 | 0.080 | 6.47 vs 6.703 |

Best scorer at n = 250: **uni**, 3.51 sigma per pair against 1.86 for the phase-1 IC (1.89×).
The match count works because a shared key cancels in C − C' and leaves plaintext coincidences at rate 0.061 instead of 0.034, a gap of 0.027; the
difference-stream IC squares and sums the whole difference distribution and keeps only a 0.0019 gap. The bigram model adds little: adjacent
differences of two independent texts are nearly independent of each other.

## Rescan with uni (same pairs, offsets ±200, min overlap 60, within-page permutation null, 20 replicates)

- Per pair (R1): hits at or above 5 sigma: observed 0, null 0–1 per replicate; observed maximum 4.96 vs null maxima 4.57–5.47.
- Pooled (R2): z at offset 0 = -2.31 (null -1.75 ± 0.81); largest pooled z over all offsets 2.34 at offset -52 vs null maxima 2.18–3.82.

Top per-pair hits:

| pair | offset | sigma | overlap |
|---|---|---|---|
| LP2-17/LP2-44 | -138 | 4.96 | 135 |
| LP2-25/LP2-53 | -104 | 4.90 | 169 |
| LP2-03/LP2-30 | -65 | 4.49 | 152 |
| LP2-15/LP2-18 | +48 | 4.47 | 159 |
| LP2-30/LP2-33 | -195 | 4.44 | 68 |
| LP2-05/LP2-35 | +94 | 4.40 | 177 |
| LP2-46/LP2-49 | -68 | 4.39 | 66 |
| LP2-01/LP2-20 | -75 | 4.34 | 191 |
| LP2-16/LP2-42 | +126 | 4.31 | 146 |
| LP2-08/LP2-39 | -85 | 4.25 | 170 |

**Rescan verdict: null.** If every page shared one keystream, the pooled z at offset 0 would be about 3.5 sigma per pair × √1485 ≈ 135; if 13 of the 55 pages did, about 7 (shared pairs scale with the square of the page fraction: 78 of 1,485 pairs, not a quarter; the figure 34 stated here until 2026-10-27 was wrong), and a cluster of 7 pages about 1.9, below detection. The observed -2.31 is indistinguishable from the permutation null. Note (2026-10-27): this run interpolated null moments only up to 250 runes, so overlaps of 251-277 runes used the 250-rune moments; the permutation null is computed the same way, so the comparison above is fair, but per-pair sigmas on the longest overlaps carry a small bias. The table now extends to 300; this run has not been repeated.

