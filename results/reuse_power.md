# Planted-cluster power of the key-reuse test

Per-pair statistic: unigram LLR of the ciphertext difference stream under the English plaintext-difference distribution, per-rune normalised, z-scored against 8910 independent pairs (null -0.296 ± 0.209); pooled z over all 1,485 pairs; 30 replicates per cell; detection at z >= 5.

| mechanism | pages sharing one key | pooled z (mean ± sd) | detected, pooled rule | detected, any pair |
|---|---|---|---|---|
| rewrite | 2 | 0.54 ± 0.99 | 0.00 | 0.00 |
| rewrite | 3 | 0.55 ± 0.85 | 0.00 | 0.03 |
| rewrite | 4 | 0.70 ± 0.97 | 0.00 | 0.00 |
| rewrite | 6 | 1.60 ± 0.89 | 0.00 | 0.20 |
| rewrite | 8 | 2.27 ± 1.06 | 0.00 | 0.20 |
| rewrite | 11 | 3.70 ± 1.17 | 0.07 | 0.40 |
| rewrite | 13 | 5.40 ± 1.17 | 0.63 | 0.47 |
| rewrite | 20 | 11.49 ± 1.41 | 1.00 | 0.83 |
| rewrite | 55 | 88.36 ± 2.46 | 1.00 | 1.00 |
| keyskip | 2 | 0.67 ± 0.85 | 0.00 | 0.00 |
| keyskip | 3 | 0.51 ± 1.05 | 0.00 | 0.00 |
| keyskip | 4 | 0.38 ± 0.99 | 0.00 | 0.00 |
| keyskip | 6 | 0.84 ± 1.06 | 0.00 | 0.00 |
| keyskip | 8 | 0.86 ± 1.07 | 0.00 | 0.03 |
| keyskip | 11 | 1.37 ± 0.96 | 0.00 | 0.00 |
| keyskip | 13 | 1.64 ± 1.02 | 0.00 | 0.03 |
| keyskip | 20 | 3.23 ± 0.93 | 0.03 | 0.13 |
| keyskip | 55 | 21.06 ± 2.59 | 1.00 | 0.53 |

**Reading.** Under the in-place rewrite mechanism (shared pages stay aligned) the pooled rule reaches 90 % detection at 20 shared pages; under the key-skip mechanism (shared pages drift apart after the first skip) it reaches 90 % at 55 shared pages. The §6 and §7 statement 'no detected large-scale aligned reuse' is therefore a statement about aligned reuse; a shared key under the key-skip rule is invisible to this test at any cluster size, which pnotisdev's ledger also records ('pad reuse under skip drift: untestable').

