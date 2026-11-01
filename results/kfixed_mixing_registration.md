# Registration: does the K-fixed sampler mix? Written before any run

Date 2026-11-01 (night, EDT). Every null since §42 (the two echo laws, the S carrier, §80's audit, §82's replay, §83's table)
comes from one Metropolis sampler, `src/kfixed.py`, run from the observed arrangement with one seed (1034), 20 burn-in and 4
thinning attempted transpositions per rune, 999 draws per page. Nobody has shown that this chain mixes. The fourth external
review named sampler calibration as the strongest statistical claim's weakest support. Nothing below has been run.

## Method (`src/kfixed_mixing.py`, `results/kfixed_mixing.md`)

The three core statistics per draw, pooled over the 55 pages: within-word lag-5 equalities, S..S pairs among them, and
within-word lag-6 hits of c = 24 − 2c′. Four chains: **base** (seed 1034, burn-in 20, thinning 4, the record's setting);
**seed** (seed 2027, 20, 4); **slow** (seed 1034, burn-in 40, thinning 8); **long** (seed 1034, burn-in 100, thinning 4).
For each chain: the null mean and sd of each statistic over its 999 draws; the lag-1 autocorrelation of each statistic's
draw sequence and the effective sample size N(1 − ρ)/(1 + ρ); the z of the observed count. Rare-event uncertainty: for the
joint replay's 0 of 999, the 95 % upper bound by the rule of three, stated beside it.

## Predictions

- **M1** the four chains' null means of each statistic agree within two standard errors of each other (SE = sd/√999 ≈ 0.26
  for the lag-5 count, 0.05 for S..S, 0.21 for lag 6).
- **M2** the lag-1 autocorrelation of every statistic in the base chain is below 0.10, and its effective sample size above 800.
- **M3** the z of each observed count varies by less than 0.3 across the four chains.

Expected: all hold. If M2 fails, every null mean in the record is still unbiased but its sd is understated by the
autocorrelation factor, and the affected z's are re-stated with the corrected sd before the release is tagged.

## Reproduce

`CHAIN=base|seed|slow|long .venv/bin/python -I src/kfixed_mixing.py`, then `CHAIN=merge`.

## Outcome (2026-11-01, night; README §84)

M2 holds (ρ₁ between −0.06 and +0.07 across all chains and statistics; ESS 861–1,127). M1 fails as written on the lag-6 cell (range 0.63 against a two-chain threshold of 0.58); the 95 % range of four means is 0.76, 0.18, 0.76 and all spreads fall inside it (lesson fifteen: a k-chain criterion is a range criterion). M3 fails as written on the S..S cell alone (z 5.82–6.24), a z at six sigma being sensitive to the sd's second decimal; the two laws' z move by 0.09 and 0.20. The nulls stand.
