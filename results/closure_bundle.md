# Closure bundle: five cheap checks from the 2026-10-28 field survey

## (a) Repeats on the solved pages' ciphertext

Mechanism per chunk from the published keys (as in §4), with a six-rule decryption detector as a check. Only the polyalphabetic pages (Vigenère, totient stream) carry a uniform-like ciphertext whose repeat rate can be compared with the unsolved section; plain and Atbash pages carry English's own doublets.

| chunk | mechanism (published key) | detector agrees | runes | within-page pairs | repeats | expected /29 | ratio | binomial p |
|---|---|---|---|---|---|---|---|---|
| 1 | Atbash | yes | 184 | 183 | 5 | 6.3 | 0.79 | 0.838 |
| 2 | Vigenère DIVINITY | yes | 251 | 250 | 8 | 8.6 | 0.93 | 1.000 |
| 3 | Vigenère DIVINITY | yes | 264 | 263 | 8 | 9.1 | 0.88 | 0.866 |
| 4 | plain | yes | 157 | 156 | 7 | 5.4 | 1.30 | 0.504 |
| 5 | shift 3 + Atbash | yes | 209 | 208 | 4 | 7.2 | 0.56 | 0.337 |
| 6 | shift 3 + Atbash | yes | 210 | 209 | 3 | 7.2 | 0.42 | 0.128 |
| 7 | shift 3 + Atbash | yes | 218 | 217 | 5 | 7.5 | 0.67 | 0.457 |
| 8 | shift 3 + Atbash | yes | 141 | 140 | 2 | 4.8 | 0.41 | 0.248 |
| 9 | plain | yes | 187 | 186 | 7 | 6.4 | 1.09 | 0.690 |
| 10 | plain | yes | 207 | 206 | 5 | 7.1 | 0.70 | 0.565 |
| 11 | plain | yes | 192 | 191 | 3 | 6.6 | 0.46 | 0.228 |
| 12 | plain | yes | 169 | 168 | 3 | 5.8 | 0.52 | 0.391 |
| 13 | Vigenère FIRFUMFERENFE | yes | 226 | 225 | 6 | 7.8 | 0.77 | 0.713 |
| 14 | Vigenère FIRFUMFERENFE | no (atbash) | 93 | 92 | 3 | 3.2 | 0.95 | 1.000 |
| 15 | plain | yes | 89 | 88 | 3 | 3.0 | 0.99 | 1.000 |
| 72 | totient prime stream | yes | 85 | 84 | 2 | 2.9 | 0.69 | 1.000 |
| 73 | plain | yes | 95 | 94 | 1 | 3.2 | 0.31 | 0.385 |

Polyalphabetic solved pages pooled: 27 repeats in 914 pairs (919 runes), expected 31.5 under uniform; ratio 0.86. Unsolved section: 86 in 12,900 pairs, expected 444.8, ratio 0.19. Two-sample test of the two rates (Fisher exact): p = 3.45e-09.

## (b) Position parity of the repeats

| modulus | repeats per residue | expected from all pairs | chi-square p |
|---|---|---|---|
| 2 | 35 51 | 43.1 42.9 | 0.08 |
| 3 | 25 32 29 | 28.8 28.7 28.5 | 0.64 |
| 4 | 13 20 22 31 | 21.6 21.5 21.5 21.4 | 0.05 |
| 5 | 20 22 15 11 18 | 17.3 17.3 17.2 17.1 17.1 | 0.38 |
| 6 | 10 21 14 15 11 15 | 14.5 14.5 14.4 14.3 14.2 14.2 | 0.39 |
| 7 | 11 11 11 13 15 12 13 | 12.4 12.4 12.4 12.3 12.2 12.2 12.1 | 0.98 |
| 8 | 5 11 9 19 8 9 13 12 | 10.9 10.9 10.8 10.8 10.7 10.7 10.6 10.6 | 0.12 |

A fixed-frame digraphic cipher would concentrate the repeats on one residue mod 2. Flat at every modulus: replicates Leo-Y-Zhang.

## (c) Identical n-gram windows across pages

Observed count of distinct n-grams that occur on two or more pages, and the number of page pairs sharing one, against 999 nulls in which every page is shuffled independently.

| n | distinct n-grams on 2+ pages | shuffle null | p | re-draw null (0.81) | p | page pairs sharing | shuffle null | p | re-draw null | p |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 2446 | 2364.4 ± 32.3 | 0.005 | 2427.6 ± 29.4 | 0.267 | 3428 | 3286.5 ± 59.0 | 0.010 | 3439.1 ± 60.1 | 0.554 |
| 4 | 121 | 112.6 ± 10.7 | 0.227 | 120.3 ± 11.6 | 0.495 | 123 | 114.0 ± 11.0 | 0.214 | 121.8 ± 11.8 | 0.481 |
| 5 | 6 | 3.9 ± 2.0 | 0.217 | 4.2 ± 2.1 | 0.269 | 6 | 3.9 ± 2.0 | 0.218 | 4.2 ± 2.1 | 0.269 |

Two nulls: a within-page shuffle (keeps rune counts, loses the lag-1 deficit) and iid uniform pages of the same lengths with the fitted 0.81 re-draw (keeps the deficit). The deficit concentrates n-grams on the doublet-free types, which raises collisions by itself, so the re-draw null is the right one for the lag-1-aware comparison.

## (d) Context of the repeats

- Identity of the repeated rune against the unigram marginal: G-test p = 0.48 (29 cells, 86 repeats).
- Rune immediately before the pair against the marginal of runes before any pair: p = 0.33.
- Step into the pair (c_i − c_(i−1) mod 29) against the marginal step: p = 0.17.
- Gaps between successive repeats against a geometric law at the observed rate: KS p = 0.66 (mean gap 151, max 712).

Nothing about a repeat's neighbourhood predicts it: replicates invictustitan2 (p 0.47–0.78 there).

## (e) The within-word lag-6 relation c_i = 24 − 2 c_(i−6) (pnotisdev `obs-lag6`)

Within-word pairs at lag d; hits of the named map, of the identity map (the lag-d echo), and of the best of all 812 affine maps c_i = a·c_(i−d) + b (a = 1..28, b = 0..28). The last two columns give the maximum over the 812 maps under 999 within-page shuffles and the permutation p of the observed maximum.

| lag d | within-word pairs | expected per map | hits of 24 − 2c | identity (echo) | best affine map | null max over 812 maps | p(max) |
|---|---|---|---|---|---|---|---|
| 2 | 7,199 | 248.2 ± 15.5 | 253 (z +0.31) | 250 (z +0.11, p 0.399) | 298 (a=2, b=0, z +3.21) | 298.6 ± 5.4 | 0.537 |
| 3 | 4,835 | 166.7 ± 12.7 | 191 (z +1.91) | 179 (z +0.97, p 0.135) | 202 (a=3, b=18, z +2.78) | 208.8 ± 5.1 | 0.957 |
| 4 | 3,197 | 110.2 ± 10.3 | 118 (z +0.75) | 131 (z +2.01, p 0.020) | 151 (a=24, b=28, z +3.95) | 144.7 ± 4.0 | 0.096 |
| 5 | 2,073 | 71.5 ± 8.3 | 58 (z -1.62) | 102 (z +3.67, p 0.001) | 104 (a=23, b=15, z +3.91) | 99.4 ± 3.3 | 0.108 |
| 6 | 1,267 | 43.7 ± 6.5 | 77 (z +5.13) | 31 (z -1.95, p 0.977) | 77 (a=27, b=24, z +5.13) | 65.7 ± 2.8 | 0.003 |
| 7 | 713 | 24.6 ± 4.9 | 22 (z -0.53) | 30 (z +1.11, p 0.170) | 39 (a=11, b=4, z +2.96) | 41.4 ± 2.0 | 0.958 |
| 8 | 373 | 12.9 ± 3.5 | 10 (z -0.81) | 10 (z -0.81, p 0.802) | 23 (a=4, b=8, z +2.88) | 25.4 ± 1.5 | 0.992 |

Source rune of the 58 lag-6 hits of 24 − 2c (which rune six back carries the relation), observed against hits spread in proportion to that rune's share of the 965 pairs:

| rune | F | U | TH | O | R | C | G | W | H | N | I | J | EO | P | X | S | T | B | E | M | L | NG | OE | D | A | AE | Y | IA | EA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hits | 1 | 3 | 5 | 5 | 4 | 4 | 1 | 6 | 2 | 2 | 1 | 2 | 3 | 4 | 2 | 3 | 5 | 3 | 2 | 3 | 0 | 2 | 2 | 1 | 0 | 4 | 4 | 1 | 2 |
| expected | 2.0 | 2.0 | 2.1 | 2.1 | 1.9 | 2.2 | 1.6 | 1.5 | 2.1 | 2.3 | 1.9 | 2.0 | 1.4 | 2.0 | 2.1 | 1.8 | 1.8 | 2.8 | 2.6 | 1.6 | 1.8 | 2.3 | 2.3 | 1.9 | 2.4 | 1.9 | 1.6 | 2.2 | 2.0 |

