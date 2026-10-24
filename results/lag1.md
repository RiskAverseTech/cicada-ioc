# Lag-1 diagnostic (adjacent runes in the unsolved pages)

Adjacent pairs pooled over 55 pages: 12901. Expected count per difference class d = C[t] - C[t+1] mod 29: 444.9.

| d | count | z vs uniform |
|---|---|---|
| 0 | 86 | -17.32 |
| 20 | 510 | +3.14 |
| 27 | 503 | +2.81 |
| 16 | 499 | +2.61 |
| 19 | 497 | +2.52 |
| 12 | 401 | -2.12 |
| 6 | 485 | +1.94 |
| 2 | 472 | +1.31 |

Doublets (d = 0, same rune twice in a row): 86 observed vs 444.9 expected, z = -17.32.
Chi-square of the 29 difference classes: 343.1 on 28 dof.

## Per page

Lag-1 sigma per page (positive = non-uniform adjacent differences). Count of pages above +2: 5, below -2: 0, mean +0.86.

| page | N | lag-1 IC | sigma | doublets |
|---|---|---|---|---|
| LP2-13 | 271 | 0.0385 | +4.17 | 0 |
| LP2-21 | 272 | 0.0380 | +3.71 | 1 |
| LP2-08 | 254 | 0.0382 | +3.70 | 3 |
| LP2-54 | 231 | 0.0370 | +2.22 | 2 |
| LP2-37 | 227 | 0.0368 | +2.00 | 0 |
| LP2-05 | 262 | 0.0364 | +1.93 | 0 |
| LP2-22 | 130 | 0.0383 | +1.91 | 1 |
| LP2-00 | 261 | 0.0363 | +1.79 | 2 |
| LP2-31 | 268 | 0.0361 | +1.66 | 0 |
| LP2-15 | 158 | 0.0371 | +1.59 | 0 |

## Against a constant-key reading

The solved plaintext has lag-1 difference IC 0.0388 (doublet rate 0.0259 vs 1/29 = 0.0345). If every unsolved page were a constant-key (shift / simple substitution) cipher, the pooled lag-1 z would be about 29; the observed pooled z is 6.39.

