# Is the page a unit? Words across page joins (row C10)

Unsolved pages: 55, joins 54. Joins that fall inside a word (page ends on a rune, next page begins on a rune, no separator between): **32**. Line breaks inside words, for comparison: 452 of 630 (§33). Words wholly inside a page: 2,864.

- C10-P1: joined-word lengths (n = 32, mean 6.5) against within-page word lengths (mean 4.5): KS p = **0.00**. Join split rate 32/54 = 0.59; line split rate 452/630 = 0.72.
- Doublets at the 32 mid-word joins: **0** (expected 1.10 under a per-page reset with a uniform first rune; 0.20 at the within-word adjacent-repeat rate 63/10,028). Likelihood ratio for continuity from this count alone: 2.5.

| lag d | cross-join within-word pairs | equal | expected at 1/29 | expected at the within-page within-word rate | lag-6 affine hits | expected at 1/29 | expected at the within-page rate |
|---|---|---|---|---|---|---|---|
| 2 | 48 | 2 | 1.66 | 1.67 | 4 | 1.66 | 1.69 |
| 3 | 47 | 2 | 1.62 | 1.74 | 1 | 1.62 | 1.86 |
| 4 | 40 | 0 | 1.38 | 1.64 | 2 | 1.38 | 1.48 |
| 5 | 32 | 2 | 1.10 | 1.57 | 1 | 1.10 | 0.90 |
| 6 | 23 | 1 | 0.79 | 0.56 | 3 | 0.79 | 1.40 |

The joined words, Latin transliteration (page | next page):

| join | page-final part | page-initial part | joined length |
|---|---|---|---|
| LP2-00 → 01 | W | AIMSN | 6 |
| LP2-01 → 02 | LXI | OEM | 5 |
| LP2-03 → 04 | HEAH | LIA | 5 |
| LP2-04 → 05 | U | RAE | 3 |
| LP2-05 → 06 | T | XCTHDEO | 7 |
| LP2-06 → 07 | S | HNG | 3 |
| LP2-08 → 09 | EO | YWAEGJ | 6 |
| LP2-09 → 10 | WIAEARAEWIADATH | C | 11 |
| LP2-16 → 17 | OEG | LTH | 4 |
| LP2-18 → 19 | G | NOOENF | 6 |
| LP2-19 → 20 | MEO | P | 3 |
| LP2-21 → 22 | IPANGSDOEO | NGM | 10 |
| LP2-23 → 24 | AHEATH | DRF | 7 |
| LP2-24 → 25 | AXEONGSEEOI | HN | 10 |
| LP2-25 → 26 | IAETEAU | IA | 6 |
| LP2-27 → 28 | NPF | PC | 5 |
| LP2-29 → 30 | GHM | DAPE | 7 |
| LP2-31 → 32 | EAMO | L | 4 |
| LP2-33 → 34 | B | MB | 3 |
| LP2-35 → 36 | AEEAEO | YN | 5 |
| LP2-40 → 41 | PIA | EAIA | 5 |
| LP2-41 → 42 | OEOECTJ | D | 6 |
| LP2-42 → 43 | DEAUNNGFNEAE | HJ | 11 |
| LP2-43 → 44 | JT | EAU | 4 |
| LP2-44 → 45 | RMDS | C | 5 |
| LP2-45 → 46 | WNG | HTXAEIJU | 9 |
| LP2-46 → 47 | NGLMCIAEOFAE | EAITH | 11 |
| LP2-47 → 48 | AOAAE | HCITH | 8 |
| LP2-48 → 49 | EOFUDYALF | IA | 9 |
| LP2-51 → 52 | PLF | P | 4 |
| LP2-52 → 53 | OEGHYH | EOAEEAAEY | 10 |
| LP2-54 → 55 | GOTTHXEEARGY | NG | 11 |

**Reading.** The page is a typographic unit like the line, not a unit of the text. 32 of the 54 joins fall inside a word; among the 45 joins where the page does not end on a paragraph or segment mark the split rate is 0.70–0.71, the same as the line-break rate (0.72) and close to what a uniform cut gives (0.77). C10-P1 **fails as registered** (KS p 0.0003 against the within-page word lengths) for a reason the registration should have foreseen: a cut at a uniform position lands inside a word with probability proportional to the word's internal gaps, so split words are long by selection. Against the length-biased distribution (P(L) ∝ (L − 1)·p(L); mean 5.99 for the within-page words, 6.53 for the 32 split words) the KS p is 0.72. That comparison was chosen after the run and is reported as a correction, not as the registered test (registration lesson seven: a null for a selected subset must carry the selection). The 32 joined words read as ordinary words of 3–11 runes. The join doublets (0 of 32) and the cross-join pairs at lags 2–6 (23–48 pairs each, equalities and lag-6 hits within one or two of both expectations) have no power, as C10-P2 registered, and are description only. What the fact changes is stated in the registration: the plaintext runs across pages, so every within-word statistic in the record has counted each split word as two words (32 words, a 1 % effect on the counts, not rerun), and a key that also runs across pages sits at each page's cumulative position, which the filler-aware lanes never reached (lane C11, registered). [stated — the table; the length-biased comparison post hoc]

Reproduce: `.venv/bin/python -I src/page_joins.py` (seconds).
