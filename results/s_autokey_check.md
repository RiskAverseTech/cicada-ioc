# The S carrier against a plaintext autokey

Pages: 102 within-word lag-5 cipher coincidences, 11 of them S. Prediction: English (Emerson in runes, 46,035 within-word lag-5 pairs) under a plaintext autokey of lag d, key = the plaintext d runes back, primer uniform. Columns: the rule's IoC, repeat rate and S share (× uniform; pages 1.00, 0.19, 0.97), its S share at coincidences (× uniform; pages 3.1), and the chi-square of the pages' 29-value coincidence profile against the rule's predicted profile (cells with expectation < 1 pooled).

| lag | sign | IoC | repeats × | S share × | S at coincidences × | χ² of the pages' profile | df | p |
|---|---|---|---|---|---|---|---|---|
| 1 | sub | 1.12 | 1.32 | 1.20 | 1.75 | 213 | 26 | 3.2e-31 |
| 1 | beaufort | 1.12 | 1.32 | 1.91 | 2.32 | 59 | 26 | 0.00022 |
| 1 | add | 1.12 | 1.25 | 0.96 | 0.51 | 174 | 24 | 1.3e-24 |
| 2 | sub | 1.04 | 1.04 | 1.47 | 1.50 | 77 | 28 | 1.8e-06 |
| 2 | beaufort | 1.04 | 1.04 | 1.51 | 2.01 | 49 | 28 | 0.0074 |
| 2 | add | 1.09 | 1.09 | 0.88 | 0.56 | 111 | 26 | 2e-12 |
| 3 | sub | 1.06 | 1.11 | 1.61 | 2.33 | 67 | 28 | 5.3e-05 |
| 3 | beaufort | 1.06 | 1.11 | 1.44 | 1.89 | 52 | 28 | 0.0043 |
| 3 | add | 1.06 | 1.05 | 0.67 | 0.49 | 87 | 27 | 3e-08 |

The pages' profile against uniform: χ² 41.9 on 28 df, p = 0.045 (the S cell carries it).

Lag-1 sub, the rule that matches the S weight, predicts these values at coincidences (expected of 102 against observed):

| value | predicted share | expected | observed |
|---|---|---|---|
| X | 8.0 % | 8.2 | 2 |
| L | 8.0 % | 8.2 | 2 |
| A | 7.1 % | 7.2 | 7 |
| Y | 6.9 % | 7.1 | 2 |
| G | 6.5 % | 6.6 | 3 |
| S | 6.0 % | 6.1 | 11 |
| J | 5.4 % | 5.5 | 3 |
| C | 4.6 % | 4.7 | 2 |

Reading (corrected 2026-10-31: the first run read the file from character 20,000 to its end, and the Project Gutenberg licence there repeats GUTENBERG, whose U-T and E-R stand five apart and each fifteen apart in Gematria order, so one word made 98 of 196 S coincidences and the table said 3.1 ×; this table is the essay body): a lag-1 plaintext autokey puts S at 1.75 × uniform at within-word lag-5 coincidences under the sub sign and 2.32 × under beaufort, against the pages' 3.1 ×, for the stated reason (E-R, N-A, A-I, U-T, R-M fifteen apart) at its true size, which does not reach the pages. It is excluded in any case: it predicts TH, X, L and Y enriched beside S, and the pages show them at or below uniform (χ² 213 on 26 df); and it predicts an IoC of 1.12, a repeat rate 1.32 × and an S share 1.20 × where the pages read 1.00, 0.19 and 0.97. The S carrier is not a plaintext-difference effect. What remains of §47's residual class is a key that reads the written rune S itself. [stated — the tables; inferred — the last two sentences]

Runtime 2 s. Reproduce: `.venv/bin/python -I src/s_autokey_check.py`.
