# Short-page lane: z >= 4, rank first within family, bigram z >= 3, readable

Pages below the §23 power threshold, scored with a secondary rule fixed before scoring (module docstring; rule (2) was re-worded after the controls and before any page result was read, see docstring). 2000 random-keystream nulls per cell; decoder max_skip 4; lane B prior -0.8. A hypothesis is a key; its z_uni is the best of its six sign x F cells.

## Controls (one plant per page length per lane)

| lane | length | family | sign | F | key | z_uni | z_big | passes (1)-(4) | other cells passing |
|---|---|---|---|---|---|---|---|---|---|
| A | 66 | vigenere-word | sub | False | GAIN | 5.6 | 12.4 | yes | 0 |
| A | 76 | phrase-3 | add | False | THAT IS WHAT | 6.2 | 13.6 | yes | 0 |
| A | 92 | primes | beaufort | False | p[n+75] | 6.2 | 13.3 | yes | 0 |
| A | 121 | self running key | sub | True | plaintext@508 | 7.2 | 15.8 | no | 1 |
| A | 131 | phrase-2 | add | True | TO SAY | 9.4 | 15.0 | yes | 0 |
| A | 137 | fibonacci | beaufort | True | F[n+13] | 9.9 | 18.5 | no | 1 |
| A | 159 | affine position | sub | False | 24·n+6 | 9.6 | 18.3 | yes | 1 |
| A | 179 | sentence | add | False | AFTER A LONG PAUSE THE MASTER  | 10.1 | 19.8 | yes | 0 |
| A | 196 | primes+1 | beaufort | False | p[n+71]+1 | 11.1 | 20.7 | yes | 0 |
| B | 66 | vigenere-word | sub | False | TOWARD | 4.4 | 1.4 | no | 0 |
| B | 76 | phrase-3 | add | False | SEEK OUT THIS | 4.2 | 4.7 | no | 0 |
| B | 92 | primes | beaufort | False | p[n+17] | 2.8 | 1.8 | no | 0 |
| B | 121 | self running key | sub | True | plaintext@1825 | 6.3 | 6.0 | yes | 0 |
| B | 131 | phrase-2 | add | True | IT IS | 8.2 | 10.7 | yes | 0 |
| B | 137 | fibonacci | beaufort | True | F[n+12] | 6.9 | 6.1 | no | 1 |
| B | 159 | affine position | sub | False | 24·n+15 | 7.5 | 6.9 | yes | 1 |
| B | 179 | sentence | add | False | WE DO NOT HAVE ENOUGH OR THERE | 7.0 | 8.8 | yes | 0 |
| B | 196 | primes+1 | beaufort | False | p[n+62]+1 | 6.4 | 5.4 | yes | 0 |

Lane A: 7 of 9 controls pass (1)-(4).

Lane B: 5 of 9 controls pass (1)-(4).

## Pages

| page | runes | lane | cells at z_uni >= 4 | null max | best z_uni (family) | candidates after (1)-(4) |
|---|---|---|---|---|---|---|
| LP2-49 | 66 | A | 0 | 3.1 | 3.36 (affine position) | 0 |
| LP2-49 | 66 | B | 1 | 21.8 | 4.07 (phrase-3-rev) | 0 |
| LP2-55 | 76 | A | 1 | 0.5 | 4.79 (phrase-3-rev) | 0 |
| LP2-55 | 76 | B | 4 | 20.8 | 4.21 (self running key) | 0 |
| LP2-51 | 92 | A | 0 | -2.8 | 3.62 (self running key) | 0 |
| LP2-51 | 92 | B | 24 | 22.3 | 4.43 (self running key) | 0 |
| LP2-32 | 121 | A | 0 | -17.5 | 3.73 (phrase-3) | 0 |
| LP2-32 | 121 | B | 0 | 33.4 | 3.87 (phrase-4-rev) | 0 |
| LP2-22 | 131 | A | 0 | -15.8 | 3.31 (affine position) | 0 |
| LP2-22 | 131 | B | 0 | 30.6 | 3.91 (phrase-2-rev) | 0 |
| LP2-14 | 137 | A | 0 | -22.1 | 3.61 (primes) | 0 |
| LP2-14 | 137 | B | 50 | 33.4 | 5.35 (self running key) | 0 |
| LP2-15 | 159 | A | 2 | -23.6 | 4.14 (self running key) | 0 |
| LP2-15 | 159 | B | 42 | 36.7 | 4.56 (affine position) | 0 |
| LP2-53 | 179 | A | 0 | -38.3 | 3.68 (self running key) | 0 |
| LP2-53 | 179 | B | 3 | 39.2 | 4.11 (primes-1 (totient)) | 0 |
| LP2-06 | 196 | A | 1 | -48.9 | 4.02 (primes-1 (totient)) | 0 |
| LP2-06 | 196 | B | 5 | 42.6 | 4.32 (affine position) | 0 |

## Candidates meeting (1)-(4), for the readability check (5)

None.

Runtime 14 minutes.

