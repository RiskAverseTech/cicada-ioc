# Within-word lag echo under a K-fixed null

12,956 runes on the 55 unsolved pages; null = 999 arrangements per page with the page's own rune multiplicities, word structure and adjacent-repeat count (K = 86) held fixed, sampled by a Metropolis walk on transpositions (20 burn-in and 4 thinning attempted transpositions per rune; the clock counts attempts, see src/kfixed.py).

| lag d | within-word equal pairs observed | K-fixed null mean ± sd | z | one-sided p |
|---|---|---|---|---|
| 2 | 250 | 252.1 ± 15.6 | -0.13 | 0.563 |
| 3 | 179 | 165.6 ± 12.5 | +1.07 | 0.146 |
| 4 | 131 | 109.8 ± 10.2 | +2.08 | 0.029 |
| 5 | 102 | 71.8 ± 8.3 | +3.66 | 0.002 |
| 6 | 31 | 43.6 ± 6.5 | -1.93 | 0.978 |
| 7 | 30 | 24.5 ± 5.0 | +1.08 | 0.166 |
| 8 | 10 | 13.0 ± 3.7 | -0.82 | 0.829 |
| 9 | 5 | 6.5 ± 2.5 | -0.60 | 0.775 |
| 10 | 2 | 3.0 ± 1.8 | -0.60 | 0.819 |
| 11 | 1 | 1.2 ± 1.1 | -0.19 | 0.704 |
| 12 | 0 | 0.4 ± 0.6 | -0.63 | 1.000 |

Family-wise over d = 2..12: largest z is +3.66 at lag 5; the null's largest z is 1.70 ± 0.70; p = 0.011.

