# The S carrier against a plaintext autokey

Pages: 102 within-word lag-5 cipher coincidences, 11 of them S. Prediction: English (Emerson in runes, 46,991 within-word lag-5 pairs) under a plaintext autokey of lag d, key = the plaintext d runes back, primer uniform. Columns: the rule's IoC, repeat rate and S share (× uniform; pages 1.00, 0.19, 0.97), its S share at coincidences (× uniform; pages 3.1), and the chi-square of the pages' 29-value coincidence profile against the rule's predicted profile (cells with expectation < 1 pooled).

| lag | sign | IoC | repeats × | S share × | S at coincidences × | χ² of the pages' profile | df | p |
|---|---|---|---|---|---|---|---|---|
| 1 | sub | 1.12 | 1.32 | 1.21 | 3.13 | 167 | 25 | 5.4e-23 |
| 1 | beaufort | 1.12 | 1.32 | 1.88 | 2.07 | 64 | 25 | 3.1e-05 |
| 1 | add | 1.12 | 1.24 | 0.95 | 0.52 | 151 | 25 | 5e-20 |
| 2 | sub | 1.04 | 1.01 | 1.47 | 1.43 | 83 | 28 | 2.8e-07 |
| 2 | beaufort | 1.04 | 1.01 | 1.52 | 1.75 | 55 | 28 | 0.0015 |
| 2 | add | 1.09 | 1.09 | 0.87 | 0.57 | 109 | 25 | 1.8e-12 |
| 3 | sub | 1.06 | 1.11 | 1.60 | 2.35 | 64 | 28 | 0.00012 |
| 3 | beaufort | 1.06 | 1.11 | 1.45 | 1.94 | 54 | 28 | 0.002 |
| 3 | add | 1.06 | 1.05 | 0.67 | 0.51 | 85 | 28 | 1.2e-07 |

The pages' profile against uniform: χ² 41.9 on 28 df, p = 0.045 (the S cell carries it).

Lag-1 sub, the rule that matches the S weight, predicts these values at coincidences (expected of 102 against observed):

| value | predicted share | expected | observed |
|---|---|---|---|
| S | 10.8 % | 11.0 | 11 |
| TH | 8.3 % | 8.5 | 5 |
| X | 7.1 % | 7.3 | 2 |
| L | 7.0 % | 7.1 | 2 |
| G | 6.4 % | 6.5 | 3 |
| A | 6.2 % | 6.3 | 7 |
| Y | 6.0 % | 6.1 | 2 |
| J | 4.7 % | 4.8 | 3 |

Reading: a lag-1 plaintext autokey under the sub sign reproduces the S weight at coincidences exactly (3.1 × uniform) and for a stated reason, the Gematria order's placement of E-R, N-A, A-I, U-T and R-M fifteen apart. It is excluded all the same: it predicts TH, X, L and Y enriched beside S, and the pages show them at or below uniform (χ² 167 on 25 df); and it predicts an IoC of 1.12, a repeat rate 1.32 × and an S share 1.21 × where the pages read 1.00, 0.19 and 0.97. The S carrier is not a plaintext-difference effect. What remains of §47's residual class is a key that reads the written rune S itself. [stated — the tables; inferred — the last two sentences]

Runtime 3 s. Reproduce: `.venv/bin/python -I src/s_autokey_check.py`.
