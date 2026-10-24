# Can a better scorer rescue the key-reuse test?

Difference-of-plaintext model trained on 1488 runes of solved plaintext, tested on the other 1489. KL(q ‖ uniform) per rune = 0.0244 nats.
Threshold at FPR 2e-06 (the phase-1 scan size). Power = fraction of true shared-key pairs that clear it. sigma = (mean under reuse − mean under null) / null sd.

| overlap n | scorer | sigma per pair | power at FPR 2e-6 | empirical 1e-4 tail vs normal fit |
|---|---|---|---|---|
| 60 | ic | 0.64 | 0.007 | 0.05876 vs 0.05059 |
| 60 | kappa | 1.21 | 0.003 | 9 vs 7.315 |
| 60 | uni | 1.84 | 0.008 | 5.018 vs 4.67 |
| 60 | bigram | 1.81 | 0.012 | 5.506 vs 5.369 |
| 100 | ic | 1.05 | 0.011 | 0.04788 vs 0.04412 |
| 100 | kappa | 1.55 | 0.005 | 12 vs 10.24 |
| 100 | uni | 2.36 | 0.022 | 5.778 vs 5.498 |
| 100 | bigram | 2.33 | 0.026 | 6.382 vs 6.179 |
| 150 | ic | 1.39 | 0.020 | 0.04313 vs 0.04091 |
| 150 | kappa | 1.89 | 0.007 | 15 vs 13.49 |
| 150 | uni | 2.88 | 0.057 | 6.464 vs 6.14 |
| 150 | bigram | 2.82 | 0.056 | 6.822 vs 6.688 |
| 250 | ic | 2.64 | 0.065 | 0.03974 vs 0.03833 |
| 250 | kappa | 2.49 | 0.015 | 21 vs 19.34 |
| 250 | uni | 3.75 | 0.197 | 6.489 vs 6.582 |
| 250 | bigram | 3.69 | 0.182 | 6.634 vs 6.732 |

Best scorer at n = 250: **uni**, 3.75 sigma per pair against 2.64 for the phase-1 IC (1.42×).
The match count works because a shared key cancels in C − C' and leaves plaintext coincidences at rate 0.061 instead of 0.034, a gap of 0.027; the
difference-stream IC squares and sums the whole difference distribution and keeps only a 0.0019 gap. The bigram model adds little: adjacent
differences of two independent texts are nearly independent of each other.

## Rescan with uni (same pairs, offsets ±200, min overlap 60, within-page permutation null, 20 replicates)

- Per pair (R1): hits at or above 5 sigma: observed 0, null 0–2 per replicate; observed maximum 4.88 vs null maxima 4.59–5.67.
- Pooled (R2): z at offset 0 = -1.91 (null -1.78 ± 0.79); largest pooled z over all offsets 2.43 at offset -37 vs null maxima 2.38–4.13.

Top per-pair hits:

| pair | offset | sigma | overlap |
|---|---|---|---|
| LP2-25/LP2-53 | -104 | 4.88 | 169 |
| LP2-17/LP2-44 | -138 | 4.65 | 135 |
| LP2-21/LP2-29 | +102 | 4.59 | 175 |
| LP2-01/LP2-20 | -75 | 4.49 | 191 |
| LP2-12/LP2-46 | -61 | 4.48 | 200 |
| LP2-46/LP2-49 | -68 | 4.47 | 66 |
| LP2-00/LP2-55 | -80 | 4.45 | 76 |
| LP2-29/LP2-37 | -109 | 4.41 | 168 |
| LP2-03/LP2-30 | -65 | 4.40 | 152 |
| LP2-15/LP2-18 | +48 | 4.33 | 159 |

**Rescan verdict: null.** A shared keystream reused across pages would put pooled z at offset 0 near 0+ (see text); the observed value is indistinguishable from the permutation null.

