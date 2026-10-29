# Do the echoes depend on line breaks?

Within-word and across-gap pairs at lags 4, 5, 6, split by whether a line break falls between the two runes. The shuffle null keeps every word and line boundary in place and permutes the runes within the page.

| statistic | pair type | line break between | pairs | hits | uniform expected | z (uniform) | shuffle null mean ± sd | p | S..S |
|---|---|---|---|---|---|---|---|---|---|
| id4 | inside a word | no | 2,677 | 110 | 92.3 | +1.87 | 91.4 ± 9.6 | 0.028 |  |
| id4 | inside a word | yes | 520 | 21 | 17.9 | +0.74 | 18.0 ± 4.2 | 0.256 |  |
| id4 | across a word gap | no | 7,904 | 266 | 272.6 | -0.40 | 270.4 ± 16.7 | 0.596 |  |
| id4 | across a word gap | yes | 1,635 | 54 | 56.4 | -0.32 | 55.9 ± 7.3 | 0.622 |  |
| id5 | inside a word | no | 1,645 | 72 | 56.7 | +2.06 | 56.2 ± 7.1 | 0.020 | 7 |
| id5 | inside a word | yes | 428 | 30 | 14.8 | +4.04 | 14.6 ± 3.6 | 0.001 | 4 |
| id5 | across a word gap | no | 8,344 | 289 | 287.7 | +0.08 | 283.6 ± 16.7 | 0.381 |  |
| id5 | across a word gap | yes | 2,264 | 72 | 78.1 | -0.70 | 76.5 ± 8.8 | 0.709 |  |
| id6 | inside a word | no | 965 | 25 | 33.3 | -1.46 | 33.0 ± 5.7 | 0.932 |  |
| id6 | inside a word | yes | 302 | 6 | 10.4 | -1.39 | 10.1 ± 3.1 | 0.939 |  |
| id6 | across a word gap | no | 8,433 | 298 | 290.8 | +0.43 | 287.0 ± 16.2 | 0.245 |  |
| id6 | across a word gap | yes | 2,926 | 112 | 100.9 | +1.12 | 99.2 ± 10.0 | 0.112 |  |
| T6 | inside a word | no | 965 | 58 | 33.3 | +4.36 | 33.2 ± 5.8 | 0.001 |  |
| T6 | inside a word | yes | 302 | 19 | 10.4 | +2.71 | 10.6 ± 3.2 | 0.019 |  |
| T6 | across a word gap | no | 8,433 | 295 | 290.8 | +0.25 | 291.6 ± 16.6 | 0.415 |  |
| T6 | across a word gap | yes | 2,926 | 94 | 100.9 | -0.70 | 101.0 ± 9.8 | 0.785 |  |

Two-proportion z, straddling against same-line, inside words: lag-5 equality +2.24; lag-6 T +0.18; controls lag-4 equality -0.07, lag-6 equality -0.59.

Reading: the lag-5 echo is stronger on pairs that wrap a line than on pairs within a line, and the lag-6 relation is not; across word gaps neither shows anything at a line break. If the difference holds up it points at the layout step, which acts on written runes, which is where the S argument of §47 says to look. It is a post-hoc cut found by eye and is reported with that status; the pre-registered test would be the same split on any further Cicada text, which does not exist.

