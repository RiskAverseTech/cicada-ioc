# Verdict check: are the panel's mechanisms really equivalent?

A Quorum panel (quorumsays.com/q/8gvLyrvHouBK, 2026-10-26) was asked what mechanism produces a homogeneous 19% leak in an anti-repeat rule, and answered that a soft keep constant, a hard rule plus about 10% uniform nulls, and a hard rule over a memoryless sticky key are equivalent on every statistic listed, and that lag-2 repeats (hard-rule expectation about 463) are the one discriminator. This file checks both claims by simulation: solved-page English cut to the 55 real page lengths, 200 replicates per construction, scored against the unsolved pages. z = (observed − mean) / sd.

Observed: doublets 86, lag-2 repeats 435, non-zero lag-1 difference chi² 42.1 (27 dof), unigram chi² 26.4 (28 dof), IC 0.0345.

| construction | doublets (z) | lag-2 repeats (z) | lag-1 difference chi² (z) | unigram chi² (z) |
|---|---|---|---|---|
| independent uniform key (control) | 444 ± 20 (-18.2) | 442 ± 19 (-0.4) | 27 ± 8 (+2.0) | 28 ± 8 (-0.2) |
| hard rule: never repeat | 0 ± 0 | 458 ± 22 (-1.0) | 26 ± 7 (+2.3) | 26 ± 7 (+0.0) |
| soft re-draw, 81% (phase 2 survivor, (a)) | 85 ± 9 (+0.1) | 453 ± 20 (-0.9) | 27 ± 7 (+2.1) | 26 ± 7 (+0.1) |
| hard rule + 10% uniform nulls ((c) as the verdict stated it) | 40 ± 6 (+7.8) | 458 ± 20 (-1.1) | 28 ± 8 (+1.8) | 26 ± 7 (-0.0) |
| hard rule + 20% uniform nulls | 74 ± 9 (+1.3) | 454 ± 21 (-0.9) | 27 ± 7 (+2.1) | 26 ± 7 (+0.1) |
| hard rule + 22% uniform nulls | 81 ± 10 (+0.5) | 450 ± 20 (-0.8) | 27 ± 7 (+2.2) | 26 ± 7 (+0.0) |
| sticky key s = 0.08, hard skip once | 49 ± 7 (+5.2) | 456 ± 21 (-1.0) | 37 ± 10 (+0.5) | 25 ± 7 (+0.1) |
| sticky key s = 0.17, hard skip once (GPT's (b)) | 85 ± 8 (+0.1) | 460 ± 20 (-1.3) | 74 ± 16 (-2.0) | 26 ± 8 (+0.0) |

## Reading

- **Not equivalent.** Hard rule plus 10% nulls, the rate the verdict named, gives about half the observed doublets (each null opens one chance adjacency, so the rate must be about 22% to reach 86). A sticky key at the rate that gives 86 doublets (s ≈ 0.17) raises the lag-1 difference chi² to about 72, two sigma above the observed 42: the key's repeats put a 0.17-weighted copy of the plaintext difference distribution (chi² 386 on 27 dof over 2899 solved pairs, about 1719 at page length) into the ciphertext differences. A sticky rate low enough to keep the differences flat (s ≈ 0.08) gives only about 49 doublets. No single sticky rate fits both.
- **Lag-2 does not discriminate.** Every construction, including the independent key, lands within about one sigma of the observed 435; the hard-rule expectation is 459 ± 20, not 463, and 435 does not reject it. The verdict's other suggested test, runes per page against a solved-page norm, is not a test: page density is typesetting and nulls do not change how many runes fit a page.
- **What survives.** The soft re-draw and hard-rule-plus-about-22%-nulls both fit every column. The observed lag-1 difference chi² of 42 sits about two sigma above every flat model and about two sigma below the sticky model, the same faint excess phase 2 noted, now bracketed from both sides.

## Premises computed for the question (ciphertext only, this repository's page data)

- Per-page dispersion of the 86 doublets: chi² 58.9 on 55 dof; 14 zero-doublet pages against 13.5 expected under one homogeneous rate. The rule is the same process on every page; a mixture of hard-rule pages and no-rule pages is excluded.
- Doublets by rune: chi² 27.8 on 28 dof against a rune-blind expectation (proportional to frequency squared).
- Doublet positions within pages: flat across deciles; gaps between doublets 6 to 200+, no triplets (0.6 expected).
- Off-diagonal bigram chi² 816 on 784 dof (chance 756 ± 39); mean IC of the ciphertext conditioned on the previous rune 0.0358 against 0.0357 uniform. Any fixed table indexed by the previous ciphertext rune (a 29-alphabet chain cipher, additive or not) would leave each class a monoalphabetic image of the plaintext at IC ≈ 0.061; excluded.
- Lag-2, lag-3, lag-4 repeats 435, 434, 451 against 443, 441, 439 expected (|z| < 0.7).
- First-half against second-half unigram chi² within pages: 1444 on 1534 dof. No drift.

Script: `src/verdict_check.py` (200 replicates, seed 1).
