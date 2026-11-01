# Does the K-fixed sampler mix? Four chains

Registration: `results/kfixed_mixing_registration.md`. 999 draws per chain over the 55 pages; statistics pooled per draw.

| chain | seed | burn-in | thinning | lag-5 equalities: mean ± sd, ρ₁, ESS, z | S..S pairs: mean ± sd, ρ₁, ESS, z | lag-6 hits: mean ± sd, ρ₁, ESS, z |
|---|---|---|---|---|---|---|
| base | 1034 | 20 | 4 | 71.01 ± 8.30, -0.012, 1023, +3.73 | 2.24 ± 1.46, -0.012, 1023, +6.00 | 43.72 ± 6.49, +0.009, 982, +5.13 |
| seed | 2027 | 20 | 4 | 71.07 ± 8.33, -0.028, 1056, +3.71 | 2.15 ± 1.42, -0.043, 1089, +6.24 | 43.87 ± 6.44, -0.046, 1096, +5.15 |
| slow | 1034 | 40 | 8 | 71.52 ± 8.23, -0.014, 1026, +3.70 | 2.24 ± 1.50, +0.006, 987, +5.82 | 43.62 ± 6.27, -0.060, 1127, +5.33 |
| long | 1034 | 100 | 4 | 71.05 ± 8.50, -0.020, 1040, +3.64 | 2.28 ± 1.48, +0.042, 919, +5.91 | 43.24 ± 6.44, +0.074, 861, +5.24 |

Observed counts: 102, 11, 77. Standard error of a null mean at 999 draws: 0.26, 0.05, 0.21; largest spread of the four chains' means: 0.51, 0.12, 0.63; largest spread of z: 0.09, 0.42, 0.20.

Rare-event uncertainty: the joint replay's 0 of 999 (§82) bounds the joint probability at about 3 in 1,000 at 95 % (rule of three); the Bonferroni margin against a wider search is therefore about sixteenfold, as §81 and §82 state.

## Registered predictions

- M1 (null means agree within two standard errors across chains): spreads 0.51, 0.12, 0.63 against 2·SE·√2 = 0.74, 0.13, 0.58 → fails.
- M2 (base chain ρ₁ < 0.10 and ESS > 800 for every statistic): ρ₁ -0.012, -0.012, +0.009, ESS 1023, 1023, 982 → holds.
- M3 (z varies by less than 0.3 across chains): 0.09, 0.42, 0.20 → fails.

Reproduce: `CHAIN=base|seed|slow|long .venv/bin/python -I src/kfixed_mixing.py`, then `CHAIN=merge`.
