# Short-page lane: z >= 4, rank first within family, bigram z >= 3, readable

Pages below the §23 power threshold, scored with a secondary rule fixed before scoring (module docstring). 200 random-keystream nulls per cell; decoder max_skip 4; lane B prior -0.8.

## Controls (one plant per page length per lane)

| lane | length | family | sign | F | key | z_uni | z_big | passes (1)-(4) | other cells passing |
|---|---|---|---|---|---|---|---|---|---|
| A | 66 | vigenere-word | sub | False | GAIN | 5.2 | 12.4 | no | 1 |
| B | 66 | vigenere-word | sub | False | MORE | 4.6 | 5.6 | yes | 0 |

Lane A: 0 of 1 controls pass (1)-(4).

Lane B: 1 of 1 controls pass (1)-(4).

## Pages

| page | runes | lane | cells at z_uni >= 4 | null max | best z_uni (family) | candidates after (1)-(4) |
|---|---|---|---|---|---|---|
| LP2-49 | 66 | A | 0 | -6.7 | 3.40 (phrase-3) | 0 |
| LP2-49 | 66 | B | 1 | 18.6 | 4.10 (phrase-3-rev) | 0 |

## Candidates meeting (1)-(4), for the readability check (5)

None.

Runtime 0 minutes.

