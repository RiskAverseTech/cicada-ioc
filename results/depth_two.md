# Depth-two key-reuse scan: results

Pages: 55 unsolved pages (LP2-00..LP2-55 minus the image-only page), 1485 pairs, offsets -200..+200, lags 1..200, min overlap 60 runes.

Comparisons: 507789 pair-offset tests + 9376 page-lag tests = 517165. Expected maximum of 517165 independent N(0,1) draws ~ 4.63 sigma; Bonferroni 5% threshold = 5.21 sigma. The IC statistic has a heavier right tail than N(0,1) at these overlaps, so the permutation null below is the calibration that counts.

## Top 20 pair/offset hits (R1)

| rank | page A | page B | offset | N overlap | IC of difference | sigma |
|---|---|---|---|---|---|---|
| 1 | LP2-38 | LP2-49 | -41 | 66 | 0.0606 | 6.63 |
| 2 | LP2-14 | LP2-35 | +140 | 131 | 0.0472 | 6.44 |
| 3 | LP2-25 | LP2-52 | +151 | 112 | 0.0491 | 6.30 |
| 4 | LP2-10 | LP2-14 | +60 | 77 | 0.0557 | 6.29 |
| 5 | LP2-15 | LP2-34 | +191 | 70 | 0.0576 | 6.21 |
| 6 | LP2-28 | LP2-42 | +0 | 269 | 0.0404 | 6.18 |
| 7 | LP2-07 | LP2-37 | +20 | 208 | 0.0421 | 6.15 |
| 8 | LP2-10 | LP2-14 | +37 | 100 | 0.0501 | 6.02 |
| 9 | LP2-00 | LP2-44 | -137 | 125 | 0.0468 | 5.96 |
| 10 | LP2-19 | LP2-36 | +153 | 85 | 0.0527 | 5.95 |
| 11 | LP2-06 | LP2-07 | -81 | 115 | 0.0477 | 5.89 |
| 12 | LP2-51 | LP2-54 | +92 | 92 | 0.0509 | 5.82 |
| 13 | LP2-25 | LP2-35 | -56 | 217 | 0.0414 | 5.79 |
| 14 | LP2-02 | LP2-25 | +110 | 163 | 0.0436 | 5.76 |
| 15 | LP2-04 | LP2-45 | +1 | 261 | 0.0401 | 5.68 |
| 16 | LP2-20 | LP2-30 | -182 | 87 | 0.0513 | 5.65 |
| 17 | LP2-05 | LP2-17 | +172 | 101 | 0.0489 | 5.62 |
| 18 | LP2-10 | LP2-36 | -75 | 188 | 0.0422 | 5.62 |
| 19 | LP2-11 | LP2-53 | +40 | 139 | 0.0449 | 5.61 |
| 20 | LP2-44 | LP2-47 | -190 | 83 | 0.0520 | 5.60 |

Pairs at or above 5 sigma: **74** (R1 needs >= 3 disjoint pairs with consistent offsets). Permutation null gives 58-87 such hits per replicate (median 70), i.e. the count is what chance produces.

Offset consistency: the 74 hits sit at 68 distinct offsets; the most repeated offset is +126 with 3 hit(s). Hits at |offset| <= 1: 3 (LP2-28/LP2-42 @ +0, LP2-04/LP2-45 @ +1, LP2-35/LP2-38 @ -1); expected under null ~ 0.55.

Observed maximum pair sigma 6.63; permutation-null maxima over 30 replicates: min 6.65, median 7.54, max 8.11.

## Top 10 within-page lag hits

| rank | page | lag | N | IC | sigma |
|---|---|---|---|---|---|
| 1 | LP2-55 | 3 | 73 | 0.0525 | 5.07 |
| 2 | LP2-09 | 53 | 215 | 0.0404 | 4.94 |
| 3 | LP2-53 | 110 | 69 | 0.0529 | 4.88 |
| 4 | LP2-00 | 138 | 124 | 0.0446 | 4.83 |
| 5 | LP2-18 | 51 | 209 | 0.0404 | 4.81 |
| 6 | LP2-52 | 99 | 164 | 0.0419 | 4.70 |
| 7 | LP2-25 | 33 | 240 | 0.0395 | 4.63 |
| 8 | LP2-52 | 3 | 260 | 0.0389 | 4.45 |
| 9 | LP2-16 | 176 | 91 | 0.0471 | 4.44 |
| 10 | LP2-52 | 59 | 204 | 0.0401 | 4.42 |

Observed maximum lag sigma 5.07; permutation-null maxima: min 4.38, median 5.34, max 8.81.

## Pooled statistics (R2)

Pooled z at offset k = sum over pairs of sigma / sqrt(#pairs). If every page re-used one keystream from the same start, offset 0 would show z of order 65.

| statistic | observed | permutation null (mean, sd, max over replicates) |
|---|---|---|
| pooled z at offset 0 | 0.08 | 0.16, 0.89, 1.89 |
| max pooled z over all offsets | 2.96 (offset -181) | 2.99, 0.37, 4.07 |
| mean pooled z over offsets | 0.23 | 0.00, 0.03, - |
| max pooled z over lags (autocorrelation) | 6.39 (lag 1) | 2.79, 0.43, 3.87 |
| mean pooled z over lags | 0.27 | 0.01, 0.09, - |

Top 5 pooled offsets:

| offset | pooled z | #pairs |
|---|---|---|
| -181 | 2.96 | 983 |
| +13 | 2.94 | 1436 |
| +68 | 2.79 | 1300 |
| -86 | 2.70 | 1382 |
| +140 | 2.70 | 1191 |

Top 5 pooled lags:

| lag | pooled z | #pages |
|---|---|---|
| 1 | 6.39 | 55 |
| 13 | 3.47 | 54 |
| 10 | 3.21 | 54 |
| 88 | 2.85 | 49 |
| 103 | 2.49 | 48 |

## Decision

- R1 (per-pair, panel rule), literal reading: triggers (74 pairs at >= 5 sigma) - but the permutation null produces 58-87 such pairs with no key reuse at all, and the observed maximum (6.63) is below every null replicate's maximum (6.65-8.11). Calibrated R1: **NULL**.
- R2 (pooled): POSITIVE - max pooled z 6.39 vs permutation-null max 4.07.

