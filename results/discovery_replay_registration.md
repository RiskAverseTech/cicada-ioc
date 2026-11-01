# Registration: the joint discovery replay and the word-end anchoring check (Quorum's ask), written before any run

Date 2026-11-01 (late afternoon, EDT). A Quorum panel on the closing statement (question 2 of the brief; the debate is kept
privately) returned one objection and one diagnostic. The objection, GPT's: the K-fixed null corrects each fact for its own
cell but not for the search that found the facts, over offsets, affine relations and rune identities; decoder pre-registration
and leave-one-page-out do not substitute for a discovery-level correction; the decisive test is a replay of the whole discovery
procedure on matched null corpora. The diagnostic, Claude's: if the lag-6 relation is a plaintext-side check rune appended to
the word, the hits should anchor to the word's end. Both are cheap on the 999 K-fixed arrangements per page the audit already
samples, and both are run here before the work is parked. Nothing below has been run.

**What the record already holds.** The lag-5 equality and its S carrier were found by ZzNible and pnotisdev before this record
measured them, and the lag-6 relation is pnotisdev's registry row `obs-lag6`; each fact carries its own look-elsewhere (lag 5:
family-wise p 0.011 over lags 2–12, §42; lag 6: p 0.003 at the lag and about 0.02 over seven lags and all 812 affine maps,
§42; S: no other rune above z +2 of 29, §42). What it lacks is the joint accounting: the three facts came from different scans
by different people, and nobody has asked how often one null corpus yields all three at once. [stated]

## R. The joint discovery replay (`src/discovery_replay.py`, `results/discovery_replay.md`)

The discovery procedure, as the field actually ran it, reduced to three scans: (i) within-word equality at lags 2–12, the
largest z over the eleven lags; (ii) within-word affine relations c_i = a·c_(i−d) + b for a = 1 … 28, b = 0 … 28 (812 maps)
at lags 2–8, the largest z over the 5,684 cells; (iii) at the equality sites of the lag that won scan (i), the concentration
on one rune, the largest over the 29 runes of (count − n·f_r) / √(n·f_r(1 − f_r)) with f_r the rune's share of the pages.
Null: the audit's K-fixed arrangements (999 per page, seed 1034, burn-in 20, thinning 4), every scan recomputed inside every
arrangement, each cell standardized by its own null mean and sd over the 999. For the observed pages and for every arrangement
the three maxima are recorded, with the lags that won (i) and (ii) and whether they are adjacent.

Predictions: **R1** scan (i)'s family-wise p over the eleven lags is below 0.05 (§42 found 0.011). **R2** scan (ii)'s
family-wise p over the 5,684 cells is below 0.05. **R3** scan (iii)'s family-wise p over the 29 runes is below 0.05. **R4**
the share of arrangements in which all three maxima are at least as large as the observed three is below 0.005 (fewer than 5 of
999), and the share in which the winning lags of (i) and (ii) are adjacent *and* all three maxima are as large is below 0.002.
Expected: all hold. If R4 fails, the two laws are restated in §81 as candidates for a discovery artefact and the odds are
lowered; if it holds, the panel's objection is answered with a number and recorded in §81.

## E. Word-end anchoring (`src/discovery_replay.py`, same output)

For every lag-5 equality site and every lag-6 hit, the distance of the later rune from the end of its word (0 for the last
rune). Statistic: the share of sites at distance 0 or 1 (final or penultimate rune), for each echo, against the same share in
the K-fixed arrangements (one-sided p for an excess); and the full distance distribution against the null's, pooled over
words of the same length, as a descriptive table.

Predictions: **E1** the lag-6 hits' final-or-penultimate share is inside the null's central 95 %. **E2** the same for the lag-5
sites. Expected: both hold (§42 found the lag-5 echo untied to position from the word's start; position from the end was
never tabulated). If E1 fails, the check-rune reading gets a registered follow-up before parking; if it holds, it is closed at
this resolution.

## Reproduce

`.venv/bin/python -I src/discovery_replay.py`

## Outcome (2026-11-01, late afternoon, 274 s; README §82)

R1 holds (lag 5 wins scan (i), family-wise p 0.015). R2 holds (lag 6, map a = 27, b = 24, family-wise p 0.008 over 5,684 cells). **R3 fails**: S wins scan (iii) at z 4.17 but the best of 29 runes reaches that in 8.5 % of null corpora (family-wise p 0.085); the S carrier is restated in §81 as the softest datum, an open question rather than a law. R4 holds: 0 of 999 arrangements reach all three observed maxima, 0 with the winning lags adjacent (adjacent in 18.5 % regardless). E1 holds (lag-6 final-or-penultimate share 0.753 in 0.567–0.838); E2 holds (lag-5 share 0.637 in 0.539–0.768). The check-rune reading closes at this resolution.
