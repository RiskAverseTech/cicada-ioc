# Linear complexity over GF(29)

Berlekamp–Massey length of the shortest linear recurrence generating each unsolved page (forward and reversed) and the whole stream. A random sequence of length n has complexity about n/2; a raw LFSR output has complexity equal to its order.

| unit | n | L forward | L reversed | random expectation n/2 |
|---|---|---|---|---|
| page 1 | 262 | 131 | 131 | 131 |
| page 2 | 266 | 133 | 133 | 133 |
| page 3 | 201 | 101 | 101 | 100 |
| page 4 | 217 | 109 | 109 | 108 |
| page 5 | 261 | 131 | 131 | 130 |
| page 6 | 263 | 132 | 132 | 132 |
| page 7 | 196 | 98 | 98 | 98 |
| page 8 | 208 | 104 | 104 | 104 |
| page 9 | 255 | 128 | 128 | 128 |
| page 10 | 268 | 134 | 134 | 134 |
| page 11 | 263 | 132 | 132 | 132 |
| page 12 | 273 | 137 | 137 | 136 |
| page 13 | 261 | 131 | 131 | 130 |
| page 14 | 272 | 136 | 136 | 136 |
| page 15 | 137 | 69 | 69 | 68 |
| page 16 | 159 | 80 | 80 | 80 |
| page 17 | 267 | 134 | 134 | 134 |
| page 18 | 273 | 137 | 137 | 136 |
| page 19 | 260 | 130 | 130 | 130 |
| page 20 | 271 | 136 | 136 | 136 |
| page 21 | 269 | 135 | 135 | 134 |
| page 22 | 273 | 137 | 137 | 136 |
| page 23 | 131 | 66 | 66 | 66 |
| page 24 | 213 | 107 | 107 | 106 |
| page 25 | 270 | 135 | 135 | 135 |
| page 26 | 273 | 137 | 137 | 136 |
| page 27 | 265 | 133 | 133 | 132 |
| page 28 | 234 | 117 | 117 | 117 |
| page 29 | 269 | 135 | 135 | 134 |
| page 30 | 277 | 139 | 139 | 138 |
| page 31 | 263 | 132 | 132 | 132 |
| page 32 | 269 | 135 | 135 | 134 |
| page 33 | 121 | 61 | 61 | 60 |
| page 34 | 214 | 107 | 107 | 107 |
| page 35 | 261 | 131 | 131 | 130 |
| page 36 | 271 | 135 | 135 | 136 |
| page 37 | 238 | 119 | 120 | 119 |
| page 38 | 228 | 114 | 114 | 114 |
| page 39 | 228 | 114 | 114 | 114 |
| page 40 | 240 | 120 | 120 | 120 |
| page 41 | 231 | 116 | 116 | 116 |
| page 42 | 273 | 137 | 137 | 136 |
| page 43 | 272 | 136 | 136 | 136 |
| page 44 | 274 | 137 | 137 | 137 |
| page 45 | 273 | 137 | 137 | 136 |
| page 46 | 270 | 135 | 135 | 135 |
| page 47 | 270 | 135 | 135 | 135 |
| page 48 | 274 | 137 | 137 | 137 |
| page 49 | 271 | 136 | 136 | 136 |
| page 50 | 66 | 33 | 33 | 33 |
| page 51 | 92 | 46 | 46 | 46 |
| page 52 | 263 | 132 | 132 | 132 |
| page 53 | 179 | 90 | 90 | 90 |
| page 54 | 232 | 116 | 116 | 116 |
| page 55 | 76 | 38 | 38 | 38 |
| whole stream | 12956 | 6478 | – | 6478 |

Smallest ratio L/n over pages and directions: 0.498 (iid-uniform null over 100 draws of ten pages: smallest ratio 0.499 ± 0.001, minimum 0.496).

Plants (300 runes):

| plant | n | L |
|---|---|---|
| LFSR order 8, raw | 300 | 8 |
| LFSR order 8 + English (c = p + k) | 300 | 150 |
| LFSR order 16, raw | 300 | 16 |
| LFSR order 16 + English (c = p + k) | 300 | 150 |
| LFSR order 32, raw | 300 | 32 |
| LFSR order 32 + English (c = p + k) | 300 | 150 |
| LFSR order 64, raw | 300 | 64 |
| LFSR order 64 + English (c = p + k) | 300 | 150 |

Reading: every page and the whole stream sit at the random expectation; the raw-LFSR plants are recovered at their order, and an LFSR added to English is indistinguishable from random, which is why this test only excludes keystream-only pages (pages with no plaintext), not any keyed cipher.

