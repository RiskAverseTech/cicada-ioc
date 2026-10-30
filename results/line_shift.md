# Is the line-first rune plaintext under one fixed key value?

Column 0 of the 55 unsolved pages against English profiles (Emerson, rune spelling) shifted by k under three signs; statistic: log-likelihood gain over the page's own rune distribution, maximised over 87 (sign, k) cells; p from 5,000 multinomial draws from the page distribution with the same maximisation. Registration: `results/line_shift_registration.md`.

| pairing | observed | profile | best cell | gain | p | best cell's top runes: observed vs predicted |
|---|---|---|---|---|---|---|
| T1a | all 594 (594) | all | beaufort k=0 | -315.5 (null median -405.0) | 0.000 | J 16 vs 74, C 26 vs 45, Y 24 vs 45, X 24 vs 44, L 21 vs 42, P 33 vs 41 |
| control for T1a | synthetic (594) from sub k=7 | all | sub k=7 | +234.6 | 0.0000 | found |
| T1b | all 594 (594) | word-initial | beaufort k=2 | -638.7 (null median -769.5) | 0.001 | W 13 vs 74, F 20 vs 70, NG 27 vs 51, EA 38 vs 48, T 14 vs 39, A 17 vs 38 |
| control for T1b | synthetic (594) from sub k=7 | word-initial | sub k=7 | +305.9 | 0.0000 | found |
| T2 | word-initial lines (206) | word-initial | beaufort k=2 | -158.7 (null median -230.5) | 0.002 | W 6 vs 26, F 7 vs 24, NG 10 vs 18, EA 12 vs 17, T 1 vs 14, A 7 vs 13 |
| control for T2 | synthetic (206) from sub k=7 | word-initial | sub k=7 | +109.9 | 0.0000 | found |
| T3 | mid-word lines (388) | interior | beaufort k=0 | -266.7 (null median -282.4) | 0.206 | J 13 vs 61, L 12 vs 33, X 15 vs 30, P 17 vs 30, AE 15 vs 29, Y 9 vs 29 |
| control for T3 | synthetic (388) from sub k=7 | interior | sub k=7 | +193.2 | 0.0000 | found |

## Claims

- T0 controls 4/4: **holds**.
- T1 all 594 against both profiles, p ≥ 0.01: **fails**.
- T2 word-initial lines against the word-initial profile, p ≥ 0.01: **fails**.
- T3 mid-word lines against the interior profile, p ≥ 0.01: **holds**.

Reading: T1 and T2 fail as written and the failure is the registration's. The statistic was the gain of the best shifted profile over the page's own distribution, and the null drew columns from the page distribution; a column that is more peaked than the page (column 0 is, IoC 1.090) fits any peaked prediction less badly than a flat draw does, so a small p says only that column 0 is not the page distribution, which §63 established. The sign of the gain answers the question the registration asked: in every pairing the best shifted English profile is worse than the page's own distribution by 159 to 639 nats (it predicts J 74 against 16 observed, W 74 against 13, F 70 against 20), while the four planted controls come back positive by 110 to 306 nats at the planted sign and shift. The line-first rune is not plaintext under one fixed key value under any sign, in the clear included. The claim should have been written on the sign of the gain; it is recorded as failed and the reading as rejected. [stated — the table; the diagnosis of the null inferred]

Runtime 33 s. Reproduce: `.venv/bin/python -I src/line_shift.py`.
