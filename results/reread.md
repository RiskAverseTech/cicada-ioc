# Blinded glyph-level re-reading of the unsolved pages

Classifier: 3-NN on 32 x 32 glyph crops, trained on 2763 labelled glyphs from solved images [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 73, 74] (images with no exactly matched row: []). Leave-one-page-out accuracy **0.9971**; a component is resolved if its nearest training glyph has cosine similarity at least T = 0.986 (the 0.5th percentile of held-out glyphs), which keeps 99.5% of held-out glyphs at error 0.0728%. Most frequent held-out confusions: S→A 1, AE→U 1, IA→I 1, Y→TH 1, TH→M 1, U→EO 1.

Blind reading of 55 pages: resolved-glyph count within 3 of the transcription on **32 of 55**; at the 12,807 aligned resolved glyphs the reading disagrees with the transcription **0** times (0.0000%, against a held-out classifier error of 0.0728%); 149 glyph positions could not be aligned (insertions, deletions or runs longer than three); adjacent repeats on the resolved blind reading **84** (transcription 86).

**Pre-registered verdict: transcription NOT confirmed** (count match ≥ 50/54: False; disagreement ≤ 2 × classifier error: True; blind doublets within 10 of 86: True).

| page | runes (transcription) | components | resolved glyphs | count within 3 | aligned | disagree | unaligned | doublets blind | doublets transcription |
|---|---|---|---|---|---|---|---|---|---|
| LP2-00 | 262 | 263 | 261 | True | 261 | 0 | 1 | 2 | 2 |
| LP2-01 | 266 | 264 | 258 | False | 258 | 0 | 8 | 1 | 1 |
| LP2-02 | 201 | 206 | 197 | False | 197 | 0 | 4 | 1 | 1 |
| LP2-03 | 217 | 214 | 213 | False | 213 | 0 | 4 | 3 | 3 |
| LP2-04 | 261 | 262 | 261 | True | 261 | 0 | 0 | 2 | 2 |
| LP2-05 | 263 | 261 | 260 | True | 260 | 0 | 3 | 0 | 0 |
| LP2-06 | 196 | 196 | 194 | True | 194 | 0 | 2 | 1 | 1 |
| LP2-07 | 208 | 214 | 206 | True | 206 | 0 | 2 | 0 | 0 |
| LP2-08 | 255 | 253 | 252 | True | 252 | 0 | 3 | 3 | 3 |
| LP2-09 | 268 | 268 | 268 | True | 268 | 0 | 0 | 3 | 3 |
| LP2-10 | 263 | 264 | 263 | True | 263 | 0 | 0 | 1 | 1 |
| LP2-11 | 273 | 268 | 265 | False | 265 | 0 | 8 | 0 | 1 |
| LP2-12 | 261 | 258 | 255 | False | 255 | 0 | 6 | 1 | 1 |
| LP2-13 | 272 | 271 | 270 | True | 270 | 0 | 2 | 0 | 0 |
| LP2-14 | 137 | 138 | 137 | True | 137 | 0 | 0 | 0 | 0 |
| LP2-15 | 159 | 221 | 158 | True | 158 | 0 | 1 | 0 | 0 |
| LP2-16 | 267 | 265 | 263 | False | 263 | 0 | 4 | 1 | 1 |
| LP2-17 | 273 | 269 | 265 | False | 265 | 0 | 8 | 0 | 0 |
| LP2-18 | 260 | 258 | 256 | False | 256 | 0 | 4 | 1 | 1 |
| LP2-19 | 271 | 270 | 269 | True | 269 | 0 | 2 | 5 | 5 |
| LP2-20 | 269 | 267 | 266 | True | 266 | 0 | 3 | 1 | 1 |
| LP2-21 | 273 | 272 | 269 | False | 269 | 0 | 4 | 1 | 1 |
| LP2-22 | 131 | 140 | 131 | True | 131 | 0 | 0 | 1 | 1 |
| LP2-23 | 213 | 217 | 212 | True | 212 | 0 | 1 | 1 | 1 |
| LP2-24 | 270 | 268 | 266 | False | 266 | 0 | 4 | 5 | 5 |
| LP2-25 | 273 | 271 | 269 | False | 269 | 0 | 4 | 3 | 3 |
| LP2-26 | 265 | 263 | 261 | False | 261 | 0 | 4 | 2 | 2 |
| LP2-27 | 234 | 230 | 228 | False | 228 | 0 | 6 | 4 | 5 |
| LP2-28 | 269 | 268 | 267 | True | 267 | 0 | 2 | 0 | 0 |
| LP2-29 | 277 | 274 | 271 | False | 271 | 0 | 6 | 4 | 4 |
| LP2-30 | 263 | 261 | 259 | False | 259 | 0 | 4 | 2 | 2 |
| LP2-31 | 269 | 267 | 265 | False | 265 | 0 | 4 | 0 | 0 |
| LP2-32 | 121 | 122 | 121 | True | 121 | 0 | 0 | 2 | 2 |
| LP2-33 | 214 | 220 | 210 | False | 210 | 0 | 4 | 2 | 2 |
| LP2-34 | 261 | 266 | 259 | True | 259 | 0 | 2 | 3 | 3 |
| LP2-35 | 271 | 276 | 267 | False | 267 | 0 | 4 | 3 | 3 |
| LP2-36 | 238 | 245 | 238 | True | 238 | 0 | 0 | 3 | 3 |
| LP2-37 | 228 | 235 | 224 | False | 224 | 0 | 4 | 0 | 0 |
| LP2-38 | 228 | 233 | 224 | False | 224 | 0 | 4 | 0 | 0 |
| LP2-39 | 240 | 248 | 239 | True | 239 | 0 | 1 | 1 | 1 |
| LP2-40 | 231 | 236 | 228 | True | 228 | 0 | 3 | 0 | 0 |
| LP2-41 | 273 | 271 | 268 | False | 268 | 0 | 5 | 2 | 2 |
| LP2-42 | 272 | 278 | 272 | True | 272 | 0 | 0 | 1 | 1 |
| LP2-43 | 274 | 276 | 274 | True | 274 | 0 | 0 | 3 | 3 |
| LP2-44 | 273 | 272 | 271 | True | 271 | 0 | 2 | 4 | 4 |
| LP2-45 | 270 | 269 | 268 | True | 268 | 0 | 2 | 2 | 2 |
| LP2-46 | 270 | 269 | 268 | True | 268 | 0 | 2 | 1 | 1 |
| LP2-47 | 274 | 273 | 272 | True | 272 | 0 | 2 | 2 | 2 |
| LP2-48 | 271 | 269 | 267 | False | 267 | 0 | 4 | 1 | 1 |
| LP2-49 | 66 | 66 | 66 | True | 66 | 0 | 0 | 0 | 0 |
| LP2-51 | 92 | 91 | 91 | True | 91 | 0 | 1 | 1 | 1 |
| LP2-52 | 263 | 261 | 259 | False | 259 | 0 | 4 | 1 | 1 |
| LP2-53 | 179 | 192 | 179 | True | 179 | 0 | 0 | 0 | 0 |
| LP2-54 | 232 | 231 | 231 | True | 231 | 0 | 1 | 2 | 2 |
| LP2-55 | 76 | 85 | 76 | True | 76 | 0 | 0 | 1 | 1 |

## Resolved disagreements (page, position in the blind reading, transcription → blind reading)

None.

Runtime 1 minutes.

