# Decoder consistency under runs of identical key symbols

## 1. Minimal case (plaintext [5, 6], key 2 1 1 1 2 ..., three rejections at the second rune)

| decoder max_skip | decode, English unigrams | decode, unigrams biased to rune 6 | path with 3 rejections reachable |
|---|---|---|---|
| 2 | [5, 7] | [5, 7] | no |
| 3 | [5, 7] | [5, 6] | yes |
| 4 | [5, 7] | [5, 6] | yes |

With max_skip 2 the correct path does not exist in the decoder.  With max_skip >= 3 it exists; on a two-rune text the unigram model still prefers rune 7 to rune 6 (both decodes are valid encryptions), which is a tie-break, not a coverage gap.

## 2. English plaintext (160 runes), hard rule, keys with injected runs of equal symbols

Runs injected by copying the previous key symbol with probability r. 240 trials per r, signs and F variants cycled; 'needs >= 3' is the share of plants where the true path has a position with three or more rejections.

| r | plants needing >= 3 rejections | exact recovery, max_skip 2 | max_skip 4 | max_skip 6 | mean recovery 2 / 4 / 6 |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.658 | 0.658 | 0.658 | 0.991 / 0.991 / 0.991 |
| 0.05 | 0.050 | 0.521 | 0.550 | 0.554 | 0.975 / 0.989 / 0.990 |
| 0.15 | 0.179 | 0.512 | 0.621 | 0.629 | 0.938 / 0.988 / 0.992 |

## 3. Runs of three or more equal symbols in the repository's key library

Counted over the first 327 symbols of every key (the decoder's reach on the longest page).

| family | keys | keys with a run >= 3 | runs >= 3 per 1,000 symbols | longest run |
|---|---|---|---|---|
| phrase-2 | 474 | 0 | 0.00 | 2 |
| phrase-2-rev | 473 | 0 | 0.00 | 2 |
| phrase-3 | 486 | 0 | 0.00 | 2 |
| phrase-3-rev | 486 | 0 | 0.00 | 2 |
| phrase-4 | 432 | 2 | 0.35 | 3 |
| phrase-4-rev | 432 | 2 | 0.35 | 3 |
| sentence | 61 | 0 | 0.00 | 2 |
| sentence-rev | 61 | 0 | 0.00 | 2 |
| affine position | 812 | 0 | 0.00 | 1 |
| fibonacci | 14 | 0 | 0.00 | 2 |
| lucas | 14 | 0 | 0.00 | 2 |
| primes | 101 | 0 | 0.00 | 1 |
| primes+1 | 101 | 0 | 0.00 | 1 |
| primes-1 (totient) | 101 | 0 | 0.00 | 1 |
| self running key | 2977 | 0 | 0.00 | 2 |
| shift | 29 | 29 | 3.06 | 327 |
| square position | 29 | 0 | 0.00 | 2 |
| vigenere-word | 269 | 7 | 0.08 | 327 |
| vigenere-word-rev | 269 | 7 | 0.08 | 327 |

Decoder default is now max_skip = 4. Every sweep before 2026-10-27 ran with max_skip = 2; a key needing three or more rejections at one position lost that position and, under the soft rule, the following ones until the paths re-synchronised.

