# E56w+n follow-ups: three registered tests against the pages

Predictions written 2026-10-29 15:42:25 (commit recorded in README §59); checked afterwards.

## T1: filler rate fitted to the word lengths, p* = 0.40; §47's statistics at p*

| p | chi-square |
|---|---|
| 0.20 | 86.9 |
| 0.25 | 63.6 |
| 0.30 | 43.3 |
| 0.35 | 31.4 |
| 0.40 | 24.7 |
| 0.45 | 28.6 |
| 0.50 | 37.1 |
| 0.55 | 59.3 |
| 0.60 | 94.5 |
| 0.65 | 152.8 |
| 0.70 | 238.2 |

| statistic | LP2 | predicted at p* | z | holds (|z| ≤ 3) |
|---|---|---|---|---|
| D | 86 | 76.98 ± 9.4 | +0.96 | yes |
| D_in | 63 | 59.8 ± 8.8 | +0.36 | yes |
| L3 | 179 | 171.1 ± 13 | +0.62 | yes |
| L4 | 131 | 111.1 ± 11 | +1.89 | yes |
| L5 | 102 | 128.6 ± 13 | -2.12 | yes |
| L5S | 11 | 4.575 ± 2 | +3.17 | NO |
| BIG | 9 | 7.685 ± 2.9 | +0.46 | yes |
| L6T | 77 | 83.08 ± 11 | -0.54 | yes |
| L6best | 77 | 83.61 ± 10 | -0.63 | not judged |
| SHARE | 7.213 | 3.951 ± 3.3 | +0.98 | yes |
| Sfreq | 0.0335 | 0.03441 ± 0.0016 | -0.55 | yes |
| U | 26.36 | 26.79 ± 7.2 | -0.06 | not judged |

T1 verdict at p*: fails: L5S.

## T2: lag-5 and lag-6 profiles per exact word length (300 books at 0.45; p* column not judged)

| cell | LP2 | predicted (0.45) | z | holds (|z| ≤ 2.5) | predicted (p*) | z |
|---|---|---|---|---|---|---|
| L5_len6 | 8 | 13.19 ± 3.56 | -1.46 | yes | 12.70 ± 3.80 | -1.24 |
| L5_len7 | 19 | 20.25 ± 4.34 | -0.29 | yes | 20.56 ± 4.53 | -0.34 |
| L5_len8 | 22 | 22.45 ± 5.25 | -0.09 | yes | 23.24 ± 5.20 | -0.24 |
| L5_len9 | 15 | 25.08 ± 5.68 | -1.77 | yes | 25.02 ± 5.42 | -1.85 |
| L5_len10 | 21 | 19.40 ± 5.05 | +0.32 | yes | 19.34 ± 4.87 | +0.34 |
| L5_len11 | 6 | 13.19 ± 4.19 | -1.72 | yes | 13.42 ± 4.74 | -1.57 |
| L5_len12p | 11 | 15.98 ± 4.56 | -1.09 | yes | 16.11 ± 4.66 | -1.10 |
| L6T_len7 | 8 | 10.60 ± 3.10 | -0.84 | yes | 10.50 ± 3.11 | -0.81 |
| L6T_len8 | 21 | 14.05 ± 3.99 | +1.74 | yes | 14.19 ± 3.72 | +1.83 |
| L6T_len9 | 18 | 16.84 ± 4.79 | +0.24 | yes | 16.76 ± 4.61 | +0.27 |
| L6T_len10 | 7 | 16.64 ± 4.97 | -1.94 | yes | 15.79 ± 4.89 | -1.80 |
| L6T_len11 | 13 | 11.02 ± 3.75 | +0.53 | yes | 10.82 ± 3.96 | +0.55 |
| L6T_len12p | 10 | 16.26 ± 4.24 | -1.48 | yes | 15.53 ± 5.01 | -1.10 |

T2: 13 of 13 cells hold.

## T3: within-word equal pairs on the solved polyalphabetic pages (chunks 2, 3, 13, 14, 72)

| lag | pairs | equal, observed | uniform pairs/29 | predicted (English under the keys) | z | holds (|z| ≤ 2.5) | LP2 for comparison: equal / pairs / per-29 ratio |
|---|---|---|---|---|---|---|---|
| 3 | 293 | 6 | 10.1 | 11.7 ± 3.7 | -1.56 | yes | 179 / 4835 / 1.07 |
| 4 | 182 | 2 | 6.3 | 8.3 ± 2.9 | -2.17 | yes | 131 / 3197 / 1.19 |
| 5 | 121 | 5 | 4.2 | 5.1 ± 2.3 | -0.03 | yes | 102 / 2073 / 1.43 |
| 6 | 72 | 1 | 2.5 | 3.3 ± 1.9 | -1.18 | yes | 31 / 1267 / 0.71 |

T3: 4 of 4 lags hold.

Reproduce: `.venv/bin/python -I src/e56w_n_followups.py --predict` then `--check`.
