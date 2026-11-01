# Quorum's ask: the joint discovery replay and the word-end anchoring check

Registration: `results/discovery_replay_registration.md`. 55 pages; K-fixed null 999 arrangements per page (seed 1034, burn-in 20, thinning 4); every scan recomputed inside every arrangement; each cell standardized by its own null mean and sd.

## R. The replay

| scan | cells | observed winner | observed max z | family-wise p over the scan |
|---|---|---|---|---|
| (i) within-word equality, lags 2–12 | 11 | lag 5 (102 against 71.0 ± 8.3) | 3.73 | 0.015 |
| (ii) affine maps a·c′ + b, lags 2–8 | 5,684 | lag 6, map a = 27, b = 24 | 5.13 | 0.008 |
| (iii) rune concentration at the winning equality lag's sites | 29 | S (11 of 102) | 4.17 | 0.085 |

Joint: arrangements with all three maxima at least the observed: **0 of 999** (share 0.0000); with the winning lags of (i) and (ii) adjacent as well: **0** (share 0.0000); the winning lags are adjacent in 0.185 of arrangements regardless. Observed winners adjacent: yes. Null maxima: scan (i) median 1.60, 99th percentile 4.18; scan (ii) median 3.93, 99th 5.03; scan (iii) median 2.45, 99th 5.55.

## E. Word-end anchoring

| echo | sites | later rune at distance 0 or 1 from the word's end | null share, central 95 % | one-sided p (excess) | distance histogram 0, 1, 2, 3, ≥4 |
|---|---|---|---|---|---|
| lag-5 equality | 102 | 65 (0.637) | 0.539–0.768 | 0.623 | [36, 29, 16, 8, 13] |
| lag-6 affine hit | 77 | 58 (0.753) | 0.567–0.838 | 0.251 | [31, 27, 8, 5, 6] |

## Registered predictions

- R1 (scan (i) family-wise p < 0.05): 0.015 → holds.
- R2 (scan (ii) family-wise p < 0.05): 0.008 → holds.
- R3 (scan (iii) family-wise p < 0.05): 0.085 → fails.
- R4 (joint share < 0.005; joint-and-adjacent share < 0.002): 0.0000, 0.0000 → holds.
- E1 (lag-6 final-or-penultimate share inside the null's 95 %): 0.753 in 0.567–0.838 → holds.
- E2 (lag-5 likewise): 0.637 in 0.539–0.768 → holds.

Runtime 274 s. Reproduce: `.venv/bin/python -I src/discovery_replay.py`.
