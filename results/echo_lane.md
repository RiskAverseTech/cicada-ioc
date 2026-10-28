# Echo-aware decoding of the phase 3-4 library (spent, held echoes)

22863 configurations x 55 pages x 2 F variants x 2 decoders = 5,029,860 tests; null per cell 2000 random keystreams through the same decoder; rule z_uni >= 6.0 and z_5 >= 6.0 and readable. Echo gain -0.106 (r = 0.5).

## Controls

| variant | sign | F | family | key | echoes in plant | eligible positions | echo-decoder z (rank) | base-decoder z | plaintext recovered | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| spent | sub | False | phrase-3-rev | THOUGHT FOR A ʳ | 3 | 5 | 11.3 (1) | 11.7 | 0.992 | yes |
| held | add | False | phrase-4-rev | TO DESTROY ALL THAT ʳ | 3 | 6 | 12.9 (1) | 11.0 | 0.989 | yes |
| spent | beaufort | False | phrase-3-rev | CONSUMPTION PRESERVATION AND ʳ | 2 | 3 | 11.0 (1) | 11.8 | 0.992 | yes |
| held | sub | False | affine position | 22·n+16 | 0 | 1 | 13.2 (1) | 12.9 | 1.000 | yes |
| spent | add | False | self running key | plaintext@1011 | 0 | 2 | 11.6 (1) | 10.8 | 1.000 | yes |
| held | beaufort | False | affine position | 18·n+21 | 3 | 6 | 12.5 (1) | 5.5 | 0.985 | yes |
| spent | sub | True | phrase-2-rev | REPLIED THE ʳ | 0 | 0 | 14.1 (1) | 12.3 | 1.000 | yes |
| held | add | True | phrase-4 | WE PRESERVE THINGS BECAUSE | 1 | 4 | 13.9 (1) | 13.9 | 0.985 | yes |
| spent | beaufort | True | phrase-3-rev | YOU ARE REPLIED ʳ | 3 | 4 | 14.9 (1) | 15.3 | 0.935 | yes |
| held | sub | True | self running key | plaintext@1739 | 0 | 2 | 13.4 (1) | 13.8 | 0.935 | yes |
| spent | add | True | self running key | plaintext@107 | 1 | 5 | 13.7 (1) | 13.4 | 0.989 | yes |
| held | beaufort | True | affine position | 28·n+9 | 1 | 3 | 13.4 (2) | 13.7 | 0.992 | no |

Controls passing: 11 of 12.

## Best cell per page and decoder

| page | decoder | eligible positions | best z | sign | F | family | key |
|---|---|---|---|---|---|---|---|
| LP2-00 | spent | 4 | 4.04 | add | True | phrase-3-rev | HERE IT IS ʳ |
| LP2-00 | held | 4 | 4.12 | add | True | self running key | plaintext@1792 |
| LP2-01 | spent | 3 | 3.97 | add | True | phrase-4 | HAVE A VOICE IN |
| LP2-01 | held | 3 | 4.38 | add | True | phrase-4 | HAVE A VOICE IN |
| LP2-02 | spent | 6 | 4.22 | add | True | phrase-2 | HASHES TO |
| LP2-02 | held | 6 | 3.95 | sub | True | phrase-3 | STUDY WITH A |
| LP2-03 | spent | 3 | 4.00 | sub | True | vigenere-word | EITHER |
| LP2-03 | held | 3 | 4.06 | sub | True | self running key | plaintext@1309 |
| LP2-04 | spent | 2 | 4.48 | sub | True | phrase-3-rev | THE PROFESSOR REPLIED ʳ |
| LP2-04 | held | 2 | 4.50 | sub | True | phrase-3-rev | THE PROFESSOR REPLIED ʳ |
| LP2-05 | spent | 4 | 4.46 | sub | True | phrase-2 | THE WAY |
| LP2-05 | held | 4 | 4.27 | sub | True | phrase-2 | THE WAY |
| LP2-06 | spent | 1 | 4.11 | beaufort | True | primes-1 (totient) | p[n+33]-1 |
| LP2-06 | held | 1 | 4.00 | beaufort | True | primes-1 (totient) | p[n+33]-1 |
| LP2-07 | spent | 1 | 4.17 | sub | True | self running key | plaintext@2791 |
| LP2-07 | held | 1 | 4.05 | sub | False | self running key | plaintext@2791 |
| LP2-08 | spent | 1 | 3.78 | add | True | phrase-3 | WE ARE WEAK |
| LP2-08 | held | 1 | 3.73 | add | False | phrase-3 | WE ARE WEAK |
| LP2-09 | spent | 7 | 4.99 | sub | True | phrase-2 | CERTAINTY AND |
| LP2-09 | held | 7 | 4.68 | sub | True | phrase-2 | CERTAINTY AND |
| LP2-10 | spent | 4 | 3.59 | add | False | self running key | plaintext@2307 |
| LP2-10 | held | 4 | 3.87 | add | True | self running key | plaintext@242 |
| LP2-11 | spent | 5 | 4.53 | add | True | self running key | plaintext@1132 |
| LP2-11 | held | 5 | 4.60 | add | True | self running key | plaintext@1132 |
| LP2-12 | spent | 4 | 3.93 | beaufort | True | self running key | plaintext@716 |
| LP2-12 | held | 4 | 4.16 | beaufort | True | self running key | plaintext@716 |
| LP2-13 | spent | 7 | 4.15 | add | True | vigenere-word-rev | PRESERUATIANʳ |
| LP2-13 | held | 7 | 4.09 | beaufort | False | self running key | plaintext@2874 |
| LP2-14 | spent | 0 | 3.59 | beaufort | True | phrase-4 | ENOUGH TO GAIN THEM |
| LP2-14 | held | 0 | 3.68 | sub | True | primes | p[n+81] |
| LP2-15 | spent | 0 | 4.09 | add | False | self running key | plaintext@538 |
| LP2-15 | held | 0 | 4.14 | beaufort | True | self running key | plaintext@2696 |
| LP2-16 | spent | 8 | 4.61 | sub | False | phrase-2 | OBTAIN WHAT |
| LP2-16 | held | 8 | 4.54 | beaufort | True | affine position | 20·n+12 |
| LP2-17 | spent | 2 | 4.17 | sub | True | phrase-3-rev | ADHERENCE THAT HAVE ʳ |
| LP2-17 | held | 2 | 3.94 | sub | True | phrase-3-rev | ADHERENCE THAT HAVE ʳ |
| LP2-18 | spent | 6 | 4.10 | beaufort | False | self running key | plaintext@168 |
| LP2-18 | held | 6 | 4.09 | sub | True | sentence | AFTER A MOMENT OF THOUGHT THE PROFESSOR  |
| LP2-19 | spent | 1 | 4.26 | sub | True | sentence | WHEN ASKED BY A STUDENT TO EXPLAIN WHAT  |
| LP2-19 | held | 1 | 4.00 | sub | True | sentence | WHEN ASKED BY A STUDENT TO EXPLAIN WHAT  |
| LP2-20 | spent | 3 | 4.13 | sub | False | self running key | plaintext@2094 |
| LP2-20 | held | 3 | 3.87 | sub | True | vigenere-word-rev | ILLUSIANSʳ |
| LP2-21 | spent | 3 | 3.90 | beaufort | True | affine position | 7·n+20 |
| LP2-21 | held | 3 | 3.92 | beaufort | True | affine position | 7·n+20 |
| LP2-22 | spent | 5 | 3.78 | beaufort | True | affine position | 26·n+10 |
| LP2-22 | held | 5 | 3.25 | add | False | self running key | plaintext@1667 |
| LP2-23 | spent | 2 | 3.72 | beaufort | True | phrase-2 | RIGHT OR |
| LP2-23 | held | 2 | 3.89 | beaufort | True | phrase-2 | RIGHT OR |
| LP2-24 | spent | 1 | 3.76 | beaufort | False | phrase-4 | EITHER THE WORDS OR |
| LP2-24 | held | 1 | 3.82 | add | True | self running key | plaintext@2104 |
| LP2-25 | spent | 4 | 3.54 | add | False | phrase-4-rev | OR THE MESSAGE CONTAINED ʳ |
| LP2-25 | held | 4 | 4.08 | beaufort | False | affine position | 16·n+21 |
| LP2-26 | spent | 4 | 4.06 | beaufort | False | self running key | plaintext@895 |
| LP2-26 | held | 4 | 4.54 | add | True | self running key | plaintext@1043 |
| LP2-27 | spent | 6 | 4.34 | sub | True | self running key | plaintext@1449 |
| LP2-27 | held | 6 | 4.31 | add | True | phrase-4-rev | ALL STRUGGLE AND SUFFERING ʳ |
| LP2-28 | spent | 4 | 4.01 | sub | True | self running key | plaintext@1237 |
| LP2-28 | held | 4 | 4.09 | add | False | phrase-4 | BELONG AND BE RIGHT |
| LP2-29 | spent | 6 | 4.17 | sub | True | phrase-2-rev | THE STUDENT ʳ |
| LP2-29 | held | 6 | 4.37 | sub | True | self running key | plaintext@1603 |
| LP2-30 | spent | 1 | 3.53 | add | False | phrase-4-rev | DO FOUR UNREASONABLE THINGS ʳ |
| LP2-30 | held | 1 | 3.57 | add | False | phrase-4-rev | DO FOUR UNREASONABLE THINGS ʳ |
| LP2-31 | spent | 1 | 3.93 | sub | True | phrase-4 | VOICE IN MY HEAD |
| LP2-31 | held | 1 | 3.91 | sub | True | phrase-4 | VOICE IN MY HEAD |
| LP2-32 | spent | 2 | 3.65 | beaufort | True | phrase-3 | ALL THAT LIVES |
| LP2-32 | held | 2 | 3.71 | beaufort | False | affine position | 5·n+15 |
| LP2-33 | spent | 0 | 4.04 | beaufort | True | phrase-3 | THE MASTER EXPLAINED |
| LP2-33 | held | 0 | 4.10 | beaufort | True | phrase-3 | THE MASTER EXPLAINED |
| LP2-34 | spent | 2 | 3.68 | add | True | phrase-4-rev | DOGMA SO THAT WE ʳ |
| LP2-34 | held | 2 | 3.91 | beaufort | False | self running key | plaintext@218 |
| LP2-35 | spent | 3 | 4.31 | sub | True | self running key | plaintext@882 |
| LP2-35 | held | 3 | 4.66 | sub | True | self running key | plaintext@878 |
| LP2-36 | spent | 6 | 3.37 | sub | False | self running key | plaintext@748 |
| LP2-36 | held | 6 | 3.33 | sub | True | phrase-2-rev | WILL NOT ʳ |
| LP2-37 | spent | 3 | 3.88 | add | False | affine position | 25·n+6 |
| LP2-37 | held | 3 | 4.37 | add | False | affine position | 25·n+27 |
| LP2-38 | spent | 4 | 3.66 | sub | True | phrase-4-rev | MUCH BECAUSE WE BELEIVE ʳ |
| LP2-38 | held | 4 | 3.95 | sub | True | phrase-3 | OF THE CIRCUMFERENCE |
| LP2-39 | spent | 2 | 4.53 | sub | True | phrase-3 | YOU WHO WISHES |
| LP2-39 | held | 2 | 4.56 | sub | True | phrase-3 | YOU WHO WISHES |
| LP2-40 | spent | 1 | 3.86 | add | True | primes+1 | p[n+13]+1 |
| LP2-40 | held | 1 | 3.79 | add | True | primes+1 | p[n+13]+1 |
| LP2-41 | spent | 3 | 4.06 | sub | True | primes-1 (totient) | p[n+53]-1 |
| LP2-41 | held | 3 | 4.18 | add | False | sentence | IT IS THE DUTY OF EVERY PILGRIM TO SEEK  |
| LP2-42 | spent | 3 | 3.89 | sub | True | phrase-3 | TOWARD THE END |
| LP2-42 | held | 3 | 3.75 | beaufort | False | phrase-3-rev | HAVE US LOSE ʳ |
| LP2-43 | spent | 6 | 3.81 | add | False | phrase-3-rev | YOU WILL FIND ʳ |
| LP2-43 | held | 6 | 3.77 | add | False | phrase-3-rev | YOU WILL FIND ʳ |
| LP2-44 | spent | 5 | 4.28 | beaufort | True | vigenere-word-rev | HOLYʳ |
| LP2-44 | held | 5 | 4.39 | beaufort | False | vigenere-word-rev | HOLYʳ |
| LP2-45 | spent | 6 | 3.73 | add | True | sentence-rev | ALONG THE WAY YOU WILL FIND AN END TO AL |
| LP2-45 | held | 6 | 3.85 | beaufort | False | phrase-3-rev | FINALLY HE ANSWERED ʳ |
| LP2-46 | spent | 1 | 3.62 | sub | True | sentence-rev | IT IS THE DUTY OF EVERY PILGRIM TO SEEK  |
| LP2-46 | held | 1 | 3.84 | beaufort | True | vigenere-word | OURSELUES |
| LP2-47 | spent | 3 | 4.21 | sub | True | primes+1 | p[n+32]+1 |
| LP2-47 | held | 3 | 4.27 | sub | True | primes+1 | p[n+32]+1 |
| LP2-48 | spent | 1 | 3.93 | add | True | affine position | 2·n+1 |
| LP2-48 | held | 1 | 3.85 | sub | True | affine position | 27·n+28 |
| LP2-49 | spent | 0 | 3.30 | sub | True | phrase-3 | OF THE MASTER |
| LP2-49 | held | 0 | 3.34 | beaufort | True | affine position | 24·n+2 |
| LP2-51 | spent | 3 | 3.49 | sub | True | phrase-4 | HERE IT IS A |
| LP2-51 | held | 3 | 3.94 | sub | True | self running key | plaintext@1248 |
| LP2-52 | spent | 5 | 4.26 | beaufort | True | phrase-2-rev | YOUR HEAD ʳ |
| LP2-52 | held | 5 | 4.70 | add | False | phrase-2 | MEANT THE |
| LP2-53 | spent | 2 | 3.83 | add | True | primes-1 (totient) | p[n+43]-1 |
| LP2-53 | held | 2 | 3.54 | sub | True | self running key | plaintext@2583 |
| LP2-54 | spent | 1 | 3.59 | beaufort | True | phrase-4-rev | WE HAVE WHAT WE ʳ |
| LP2-54 | held | 1 | 3.59 | beaufort | True | phrase-4-rev | WE HAVE WHAT WE ʳ |
| LP2-55 | spent | 2 | 4.82 | add | True | phrase-3-rev | TO STUDY HERE ʳ |
| LP2-55 | held | 2 | 4.63 | add | True | phrase-3-rev | TO STUDY HERE ʳ |

## Cells at z_uni >= 6.0 (0)

None.

## Hits (also z_5 >= 6.0): 0

None.

Largest z_uni over all cells: 4.99. Runtime 85 minutes.

