# Lag-5 equality conditional on the lag-6 relation, and the converse (row C9)

12,956 runes on 55 unsolved pages; within-word pairs; null = 999 K-fixed arrangements per page (src/kfixed.py; 20 burn-in, 4 thinning attempted transpositions per rune; seed 1034), strata recomputed inside each arrangement. A lag-5 pair is *touching* when either position is an endpoint of a lag-6 site c_i = 24 − 2·c_(i−6) inside a word, else *free*; the converse likewise.

| statistic | observed | K-fixed null mean ± sd | z | one-sided p (≥) |
|---|---|---|---|---|
| lag-5 equal, free | 93 | 68.0 ± 8.1 | +3.09 | 0.002 |
| lag-5 equal, touching | 9 | 3.1 ± 1.8 | +3.26 | 0.007 |
| lag-5 pairs, free | 1918 | 1984.1 ± 13.1 | -5.04 | 1.000 |
| lag-5 pairs, touching | 155 | 88.9 ± 13.1 | +5.04 | 0.001 |
| lag-6 hits, free | 69 | 40.7 ± 6.2 | +4.55 | 0.001 |
| lag-6 hits, touching | 8 | 3.0 ± 1.8 | +2.77 | 0.018 |
| lag-6 pairs, free | 1138 | 1179.6 ± 11.2 | -3.69 | 1.000 |
| lag-6 pairs, touching | 129 | 87.4 ± 11.2 | +3.69 | 0.001 |
| lag-5 S..S, free | 10 | 2.1 ± 1.4 | +5.50 | 0.001 |
| lag-5 S..S, touching | 1 | 0.1 ± 0.3 | +2.65 | 0.102 |

- C9-P1 (free lag-5 stratum carries the excess: ratio ≥ 1.25 and z ≥ +2.5): observed / null mean = 1.37, z = +3.09 → **holds**.
- C9-P2 (touching lag-5 stratum holds fewer than 10 equalities): 9 → **holds**.
- C9-P3 (free lag-6 stratum shows the relation at z ≥ +3): z = +4.55 → **holds**.
- Falsifier (free lag-5 z < +1.5 and touching ≥ 15): not triggered.

**Reading.** The panel's conjecture fails: the lag-5 excess is not manufactured by the lag-6 relation. Among the 1,918 lag-5 pairs that touch no lag-6 site, equalities run 93 against 68.0 ± 8.1 (z +3.09, ratio 1.37; the whole set is 102 against 71.8, ratio 1.42), and the ten S..S equalities in that stratum stand at z +5.5. Conversely the lag-6 relation holds in 69 of the 1,138 pairs that touch no lag-5 site against 40.7 ± 6.2 (z +4.55). Each echo stands without the other, which is how §58's E56w+n models them (two gated events) and how §45–§47 read the S carrier. The touching strata are small and both elevated (lag-5: 9 against 3.1; lag-6: 8 against 3.0), partly because the pages carry more lag-6 sites than the null does, so more pairs touch one; the rate inside the touching stratum (5.8 % for lag-5) is a little above the free stratum's (4.8 %), which is the same mild co-occurrence §45 reported as a description (p 0.11 once stratified by word length) and no more. Nothing in the record changes; the question the panel asked is now answered with a number rather than a model's assumption. [stated — the table]

Runtime 386 s. Reproduce: `.venv/bin/python -I src/lag5_given_lag6.py`.
