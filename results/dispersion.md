# Windowed dispersion: do the pages show a hand's local balancing?

S1: mean chi-square (28 dof) of the 29 difference classes over 50-rune windows of D = C_i − C_{i−1}; S2: the same on the ciphertext itself over 29- and 58-rune windows. All 55 pages; 200 replicates per generator, solved-page English at the real page lengths, soft re-draw 0.81. Observed doublets 86.

| statistic | observed | A iid (mean ± sd) | B bag | C recent-avoid | separation A vs B/C (sd) | observed z vs A |
|---|---|---|---|---|---|---|
| S1_D50 | 29.08 | 29.12 ± 0.48 | 29.18 | 29.10 | 0.1 | -0.1 |
| S2_C29 | 26.34 | 26.49 ± 0.31 | 26.04 | 26.41 | 1.4 | -0.5 |
| S2_C58 | 26.23 | 26.46 ± 0.43 | 25.86 | 26.38 | 1.4 | -0.5 |

Statistics with power (separation ≥ 3 sd): none.

**Reading (pre-registered rule): NO VERDICT: neither statistic separates a balanced key from an iid key through the plaintext.**

S1 was the note's proposal; it has no power because a key's local balance does not carry into its successive differences. S2 was added after that was seen and before its observed value was read. Where a statistic has power, the observed value is compared with generator A's 1st percentile and the balancing generators' central 95 %. A balancing weaker than generator C would not be visible on any of these.

