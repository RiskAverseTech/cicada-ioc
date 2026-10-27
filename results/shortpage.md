# Short-page lane: z >= 4, rank first within family, bigram z >= 3, readable

Pages below the §23 power threshold, scored with a secondary rule fixed before scoring (module docstring; rule (2) was re-worded after the controls and before any page result was read, see docstring). 2000 random-keystream nulls per cell; decoder max_skip 4; lane B prior -0.8. A hypothesis is a key; its z_uni is the best of its six sign x F cells.

## Controls (one plant per page length per lane)

| lane | length | family | sign | F | key | z_uni | z_big | passes (1)-(4) | other cells passing |
|---|---|---|---|---|---|---|---|---|---|
| A | 66 | vigenere-word | sub | False | GAIN | 5.6 | 12.4 | yes | 1 |
| A | 66 | phrase-3 | add | False | THAT IS WHAT | 5.7 | 12.8 | yes | 1 |
| A | 66 | primes | beaufort | False | p[n+65] | 5.2 | 10.5 | yes | 1 |
| A | 66 | self running key | sub | True | plaintext@599 | 6.0 | 11.6 | no | 2 |
| A | 66 | phrase-2 | add | True | FINALLY HE | 5.4 | 12.7 | yes | 1 |
| A | 76 | fibonacci | beaufort | True | F[n+7] | 6.0 | 12.1 | yes | 1 |
| A | 76 | affine position | sub | False | 15·n+21 | 6.3 | 13.1 | yes | 3 |
| A | 76 | sentence | add | False | THE CIRCUMFERENCE PRACTICES TH | 6.2 | 12.8 | yes | 1 |
| A | 76 | primes+1 | beaufort | False | p[n+47]+1 | 6.8 | 14.6 | yes | 1 |
| A | 76 | vigenere-word | sub | True | WORDS | 5.9 | 12.6 | yes | 0 |
| A | 92 | phrase-3 | add | True | HEAD IS THE | 7.2 | 13.2 | yes | 0 |
| A | 92 | primes | beaufort | True | p[n+1] | 7.5 | 14.1 | yes | 1 |
| A | 92 | self running key | sub | False | plaintext@950 | 6.3 | 13.9 | no | 2 |
| A | 92 | phrase-2 | add | False | WE SHAPE | 6.7 | 13.7 | yes | 1 |
| A | 92 | fibonacci | beaufort | False | F[n+7] | 8.1 | 15.8 | yes | 1 |
| A | 121 | affine position | sub | True | 18·n+1 | 8.8 | 15.2 | yes | 3 |
| A | 121 | sentence | add | True | THE CIRCUMFERENCE PRACTICES TH | 7.9 | 16.1 | yes | 1 |
| A | 121 | primes+1 | beaufort | True | p[n+69]+1 | 7.5 | 12.5 | yes | 0 |
| A | 121 | vigenere-word | sub | False | GETTNG | 8.1 | 17.4 | yes | 1 |
| A | 121 | phrase-3 | add | False | THE STUDENTS WERE | 9.5 | 15.1 | yes | 1 |
| A | 131 | primes | beaufort | False | p[n+55] | 9.0 | 17.2 | yes | 1 |
| A | 131 | self running key | sub | True | plaintext@1754 | 7.3 | 16.4 | no | 2 |
| A | 131 | phrase-2 | add | True | BELEIVE THE | 8.7 | 15.9 | yes | 1 |
| A | 131 | fibonacci | beaufort | True | F[n+5] | 8.0 | 14.9 | yes | 1 |
| A | 131 | affine position | sub | False | 19·n+8 | 7.9 | 15.5 | yes | 3 |
| A | 137 | sentence | add | False | ULTIMATELY YOU WILL DISCOVER A | 9.9 | 18.0 | yes | 1 |
| A | 137 | primes+1 | beaufort | False | p[n+88]+1 | 8.0 | 15.7 | yes | 1 |
| A | 137 | vigenere-word | sub | True | BEHAUIARS | 9.8 | 18.8 | yes | 0 |
| A | 137 | phrase-3 | add | True | IS THROUGH THIS | 9.8 | 16.3 | yes | 1 |
| A | 137 | primes | beaufort | True | p[n+20] | 9.1 | 15.6 | yes | 0 |
| A | 159 | self running key | sub | False | plaintext@1711 | 9.2 | 18.5 | no | 2 |
| A | 159 | phrase-2 | add | False | YOU WHO | 9.0 | 15.2 | yes | 1 |
| A | 159 | fibonacci | beaufort | False | F[n+13] | 9.5 | 18.6 | yes | 1 |
| A | 159 | affine position | sub | True | 12·n+6 | 10.9 | 16.6 | yes | 3 |
| A | 159 | sentence | add | True | FIND THE DIVINITY WITHIN AND E | 10.3 | 19.3 | yes | 1 |
| A | 179 | primes+1 | beaufort | True | p[n+32]+1 | 12.2 | 21.4 | no | 2 |
| A | 179 | vigenere-word | sub | False | ABOUT | 10.3 | 19.7 | yes | 1 |
| A | 179 | phrase-3 | add | False | YOU HAVE NO | 10.3 | 18.9 | yes | 1 |
| A | 179 | primes | beaufort | False | p[n+69] | 10.3 | 18.9 | yes | 1 |
| A | 179 | self running key | sub | True | plaintext@648 | 11.3 | 21.2 | yes | 1 |
| A | 196 | phrase-2 | add | True | THE WAY | 11.3 | 16.9 | yes | 1 |
| A | 196 | fibonacci | beaufort | True | F[n+4] | 12.0 | 19.9 | yes | 1 |
| A | 196 | affine position | sub | False | 4·n+23 | 12.0 | 21.0 | yes | 3 |
| A | 196 | sentence | add | False | FOR ALL THAT LIVES IS HOLY | 10.1 | 17.9 | yes | 1 |
| A | 196 | primes+1 | beaufort | False | p[n+81]+1 | 10.2 | 18.4 | no | 2 |
| B | 66 | vigenere-word | sub | False | SACRED | 5.3 | 4.0 | yes | 1 |
| B | 66 | phrase-3 | add | False | THAT JUST SAID | 4.3 | 4.1 | yes | 1 |
| B | 66 | primes | beaufort | False | p[n+74] | 5.7 | 2.9 | no | 0 |
| B | 66 | self running key | sub | True | plaintext@298 | 3.6 | 3.1 | no | 0 |
| B | 66 | phrase-2 | add | True | FOLLOW DOGMA | 3.6 | 4.3 | no | 0 |
| B | 76 | fibonacci | beaufort | True | F[n+7] | 5.8 | 4.1 | no | 2 |
| B | 76 | affine position | sub | False | 17·n+17 | 3.8 | 3.1 | no | 0 |
| B | 76 | sentence | add | False | AFTER A MOMENT OF THOUGHT THE  | 5.8 | 5.5 | yes | 1 |
| B | 76 | primes+1 | beaufort | False | p[n+88]+1 | 3.4 | 2.5 | no | 0 |
| B | 76 | vigenere-word | sub | True | CONSCIAUSNESS | 4.8 | 5.0 | yes | 1 |
| B | 92 | phrase-3 | add | True | WITHIN THAT WE | 6.5 | 7.3 | yes | 1 |
| B | 92 | primes | beaufort | True | p[n+47] | 3.4 | 4.2 | no | 0 |
| B | 92 | self running key | sub | False | plaintext@792 | 5.2 | 4.8 | yes | 1 |
| B | 92 | phrase-2 | add | False | SOME WISDOM | 5.2 | 6.9 | yes | 1 |
| B | 92 | fibonacci | beaufort | False | F[n+8] | 4.6 | 6.4 | yes | 1 |
| B | 121 | affine position | sub | True | 13·n+24 | 5.2 | 3.1 | no | 0 |
| B | 121 | sentence | add | True | ULTIMATELY YOU WILL DISCOVER A | 4.8 | 5.1 | yes | 1 |
| B | 121 | primes+1 | beaufort | True | p[n+5]+1 | 6.0 | 4.1 | yes | 1 |
| B | 121 | vigenere-word | sub | False | CIRCUMFERENCE | 6.3 | 6.3 | yes | 1 |
| B | 121 | phrase-3 | add | False | LONG PAUSE THE | 5.7 | 3.2 | yes | 1 |
| B | 131 | primes | beaufort | False | p[n+6] | 7.4 | 5.6 | yes | 1 |
| B | 131 | self running key | sub | True | plaintext@491 | 6.4 | 6.0 | no | 2 |
| B | 131 | phrase-2 | add | True | CONSUME TOO | 6.5 | 6.4 | yes | 1 |
| B | 131 | fibonacci | beaufort | True | F[n+12] | 5.4 | 7.0 | no | 2 |
| B | 131 | affine position | sub | False | 25·n+14 | 3.4 | 4.6 | no | 0 |
| B | 137 | sentence | add | False | THE MAN THOUGHT FOR A MOMENT A | 6.2 | 5.4 | yes | 1 |
| B | 137 | primes+1 | beaufort | False | p[n+36]+1 | 4.5 | 4.0 | yes | 1 |
| B | 137 | vigenere-word | sub | True | AN | 7.0 | 6.8 | yes | 1 |
| B | 137 | phrase-3 | add | True | SAY SO HE | 6.7 | 6.4 | yes | 1 |
| B | 137 | primes | beaufort | True | p[n+87] | 6.1 | 6.0 | yes | 1 |
| B | 159 | self running key | sub | False | plaintext@342 | 8.4 | 6.9 | yes | 1 |
| B | 159 | phrase-2 | add | False | OR THE | 6.2 | 5.9 | yes | 1 |
| B | 159 | fibonacci | beaufort | False | F[n+6] | 6.9 | 6.2 | yes | 1 |
| B | 159 | affine position | sub | True | 17·n+4 | 4.6 | 4.3 | yes | 3 |
| B | 159 | sentence | add | True | THE CIRCUMFERENCE PRACTICES TH | 6.0 | 4.2 | yes | 1 |
| B | 179 | primes+1 | beaufort | True | p[n+79]+1 | 7.4 | 5.6 | yes | 1 |
| B | 179 | vigenere-word | sub | False | PRACTICES | 5.3 | 5.4 | yes | 1 |
| B | 179 | phrase-3 | add | False | PILGRIM TO THE | 6.9 | 4.5 | yes | 1 |
| B | 179 | primes | beaufort | False | p[n+47] | 7.2 | 6.8 | yes | 1 |
| B | 179 | self running key | sub | True | plaintext@1732 | 9.2 | 6.4 | no | 2 |
| B | 196 | phrase-2 | add | True | INTELLIGENCE IS | 8.3 | 7.2 | yes | 1 |
| B | 196 | fibonacci | beaufort | True | F[n+13] | 9.2 | 8.1 | no | 2 |
| B | 196 | affine position | sub | False | 15·n+7 | 8.8 | 6.3 | yes | 3 |
| B | 196 | sentence | add | False | ULTIMATELY YOU WILL DISCOVER A | 9.8 | 10.7 | yes | 1 |
| B | 196 | primes+1 | beaufort | False | p[n+37]+1 | 8.5 | 9.0 | no | 2 |

### Controls passing (1)-(4), by lane and page length

| lane | 66 | 76 | 92 | 121 | 131 | 137 | 159 | 179 | 196 | all |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 4/5 | 5/5 | 4/5 | 5/5 | 4/5 | 5/5 | 4/5 | 4/5 | 4/5 | 39/45 |
| B | 2/5 | 2/5 | 4/5 | 4/5 | 2/5 | 5/5 | 5/5 | 4/5 | 3/5 | 31/45 |

## Pages

| page | runes | lane | cells at z_uni >= 4 | null max | best z_uni (family) | candidates after (1)-(4) |
|---|---|---|---|---|---|---|
| LP2-49 | 66 | A | 0 | 2.3 | 3.32 (affine position) | 0 |
| LP2-49 | 66 | B | 0 | 19.4 | 3.93 (phrase-3-rev) | 0 |
| LP2-55 | 76 | A | 1 | 0.1 | 4.71 (phrase-3-rev) | 0 |
| LP2-55 | 76 | B | 6 | 20.1 | 4.28 (self running key) | 0 |
| LP2-51 | 92 | A | 0 | -7.1 | 3.59 (self running key) | 0 |
| LP2-51 | 92 | B | 19 | 23.2 | 4.31 (self running key) | 0 |
| LP2-32 | 121 | A | 0 | -7.2 | 3.66 (phrase-3) | 0 |
| LP2-32 | 121 | B | 0 | 28.6 | 3.86 (phrase-4-rev) | 0 |
| LP2-22 | 131 | A | 0 | -13.5 | 3.23 (affine position) | 0 |
| LP2-22 | 131 | B | 0 | 31.9 | 3.97 (phrase-2-rev) | 0 |
| LP2-14 | 137 | A | 0 | -18.3 | 3.64 (primes) | 0 |
| LP2-14 | 137 | B | 48 | 31.3 | 5.41 (self running key) | 0 |
| LP2-15 | 159 | A | 2 | -28.1 | 4.11 (self running key) | 0 |
| LP2-15 | 159 | B | 42 | 36.2 | 4.59 (phrase-4) | 0 |
| LP2-53 | 179 | A | 0 | -22.3 | 3.81 (self running key) | 0 |
| LP2-53 | 179 | B | 6 | 39.4 | 4.17 (primes-1 (totient)) | 0 |
| LP2-06 | 196 | A | 0 | -40.3 | 3.97 (primes-1 (totient)) | 0 |
| LP2-06 | 196 | B | 4 | 42.4 | 4.17 (affine position) | 0 |

## Candidates meeting (1)-(4), for the readability check (5)

None.

Runtime 23 minutes.

