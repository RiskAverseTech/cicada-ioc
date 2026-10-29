# Shed the circumferences: word edges and page rings written in clear (word, ring)

22863 configurations x 55 pages x 2 F variants x 2 kinds = 5,029,860 tests; null per cell 2000 random keystreams through the same mask; rule z_uni >= 6.0 and z_5 >= 6.0 and readable.

## Controls

| kind | sign | F | family | key | literal runes / page | decoder z (rank) | base-decoder z | plaintext recovered | pass |
|---|---|---|---|---|---|---|---|---|---|
| word | sub | False | phrase-2-rev | LOSE OUR ʳ | 131/262 | 8.7 (1) | 0.4 | 0.958 | yes |
| ring | add | False | phrase-4 | WHO WISHES TO STUDY | 47/266 | 7.3 (1) | 5.7 | 0.827 | yes |
| word | beaufort | False | phrase-2-rev | DO NOT ʳ | 80/201 | 2.2 (301) | 1.2 | 0.687 | no |
| ring | sub | False | vigenere-word-rev | ABOUTʳ | 43/217 | 6.6 (1) | 8.8 | 0.894 | yes |
| word | add | False | self running key | plaintext@2411 | 128/261 | 6.9 (3) | 1.3 | 0.966 | no |
| ring | beaufort | False | self running key | plaintext@504 | 43/263 | 9.7 (4) | 1.4 | 0.924 | no |
| word | sub | True | phrase-3-rev | CIRCUMFERENCE PRACTICES THREE  | 100/196 | 7.8 (1) | -0.1 | 0.949 | yes |
| ring | add | True | phrase-2-rev | AMASS GREAT ʳ | 34/208 | 10.8 (1) | 7.5 | 0.923 | yes |
| word | beaufort | True | phrase-2 | LAW UNTO | 128/255 | 7.5 (1) | -1.4 | 0.863 | yes |
| ring | sub | True | vigenere-word-rev | ASCEDʳ | 44/268 | 12.8 (1) | 12.5 | 0.993 | yes |
| word | add | True | self running key | plaintext@1474 | 138/263 | 9.6 (2) | -0.9 | 1.000 | no |
| ring | beaufort | True | self running key | plaintext@1936 | 47/273 | 13.6 (2) | -0.1 | 0.974 | no |

Controls passing: 7 of 12.

## Best cell per page and kind

| page | kind | literal runes | best z | sign | F | family | key |
|---|---|---|---|---|---|---|---|
| LP2-00 | word | 115/262 | 3.49 | add | False | phrase-3-rev | YOU ARE THAT ʳ |
| LP2-00 | ring | 43/262 | 4.00 | beaufort | False | phrase-3-rev | TO SEEK OUT ʳ |
| LP2-01 | word | 125/266 | 4.23 | add | False | self running key | plaintext@1900 |
| LP2-01 | ring | 47/266 | 3.76 | sub | True | phrase-2-rev | WEB THERE ʳ |
| LP2-02 | word | 74/201 | 3.54 | beaufort | False | affine position | 23·n+16 |
| LP2-02 | ring | 40/201 | 3.68 | add | True | primes+1 | p[n+17]+1 |
| LP2-03 | word | 87/217 | 3.76 | sub | True | self running key | plaintext@106 |
| LP2-03 | ring | 43/217 | 5.08 | sub | True | vigenere-word | EITHER |
| LP2-04 | word | 118/261 | 4.26 | beaufort | True | phrase-3-rev | CONFUSED THE MAN ʳ |
| LP2-04 | ring | 46/261 | 3.82 | add | False | self running key | plaintext@28 |
| LP2-05 | word | 115/263 | 3.78 | sub | True | phrase-3-rev | LUCK AND WE ʳ |
| LP2-05 | ring | 43/263 | 4.08 | sub | True | phrase-3-rev | WHAT YOU KNOW ʳ |
| LP2-06 | word | 88/196 | 3.23 | beaufort | False | self running key | plaintext@1522 |
| LP2-06 | ring | 42/196 | 3.64 | sub | False | phrase-2 | TO ALL |
| LP2-07 | word | 99/208 | 4.26 | sub | True | phrase-4-rev | THE CIRCUMFERENCE HE SAID ʳ |
| LP2-07 | ring | 34/208 | 4.40 | sub | True | self running key | plaintext@2813 |
| LP2-08 | word | 101/255 | 3.99 | add | True | phrase-4 | I IS THE VOICE |
| LP2-08 | ring | 41/255 | 3.73 | add | False | phrase-4 | DON'T HAVE A VOICE |
| LP2-09 | word | 112/268 | 4.63 | sub | True | phrase-3 | END TO ALL |
| LP2-09 | ring | 44/268 | 4.75 | add | False | sentence | BELIEVE NOTHING FROM THIS BOOK |
| LP2-10 | word | 125/263 | 3.52 | beaufort | False | vigenere-word | DONT |
| LP2-10 | ring | 44/263 | 3.69 | sub | True | phrase-2 | AMASS GREAT |
| LP2-11 | word | 110/273 | 3.65 | add | True | phrase-4 | THAT HAVE US LOSE |
| LP2-11 | ring | 47/273 | 4.20 | add | False | self running key | plaintext@1657 |
| LP2-12 | word | 128/261 | 4.19 | sub | True | self running key | plaintext@357 |
| LP2-12 | ring | 43/261 | 4.33 | beaufort | True | self running key | plaintext@736 |
| LP2-13 | word | 119/272 | 3.66 | sub | True | phrase-3-rev | STARTED BUT HE ʳ |
| LP2-13 | ring | 48/272 | 4.27 | add | True | vigenere-word-rev | PRESERUATIANʳ |
| LP2-14 | word | 62/137 | 3.45 | beaufort | False | self running key | plaintext@683 |
| LP2-14 | ring | 29/137 | 3.78 | add | True | self running key | plaintext@1578 |
| LP2-15 | word | 73/159 | 4.36 | beaufort | True | phrase-2 | END OF |
| LP2-15 | ring | 31/159 | 4.48 | beaufort | True | self running key | plaintext@2707 |
| LP2-16 | word | 117/267 | 3.37 | sub | True | self running key | plaintext@2499 |
| LP2-16 | ring | 42/267 | 3.60 | beaufort | True | phrase-2-rev | KWESTION ALL ʳ |
| LP2-17 | word | 133/273 | 3.68 | sub | True | self running key | plaintext@113 |
| LP2-17 | ring | 47/273 | 4.77 | beaufort | True | phrase-3-rev | COMMAND YOUR OWN ʳ |
| LP2-18 | word | 119/260 | 3.81 | sub | True | self running key | plaintext@1392 |
| LP2-18 | ring | 42/260 | 4.14 | sub | True | primes+1 | p[n+64]+1 |
| LP2-19 | word | 128/271 | 3.87 | sub | True | self running key | plaintext@2822 |
| LP2-19 | ring | 46/271 | 3.90 | sub | True | phrase-2-rev | ALL STRUGGLE ʳ |
| LP2-20 | word | 129/269 | 3.91 | add | True | self running key | plaintext@881 |
| LP2-20 | ring | 42/269 | 3.94 | sub | False | self running key | plaintext@2114 |
| LP2-21 | word | 107/273 | 3.83 | sub | True | self running key | plaintext@1400 |
| LP2-21 | ring | 46/273 | 3.80 | beaufort | True | affine position | 7·n+9 |
| LP2-22 | word | 56/131 | 3.19 | sub | True | self running key | plaintext@2543 |
| LP2-22 | ring | 42/131 | 3.27 | beaufort | True | affine position | 1·n+24 |
| LP2-23 | word | 90/213 | 4.10 | add | False | affine position | 6·n+1 |
| LP2-23 | ring | 41/213 | 4.29 | add | True | affine position | 5·n+1 |
| LP2-24 | word | 127/270 | 3.89 | add | False | phrase-4 | ANYTHING ELSE TO SAY |
| LP2-24 | ring | 45/270 | 4.64 | add | True | phrase-4 | MY HEAD THOUGHT THE |
| LP2-25 | word | 114/273 | 3.68 | add | False | self running key | plaintext@2512 |
| LP2-25 | ring | 43/273 | 4.05 | add | True | phrase-3-rev | THOUGHT FOR A ʳ |
| LP2-26 | word | 117/265 | 3.87 | beaufort | False | phrase-4 | AN EASY TRIP BUT |
| LP2-26 | ring | 40/265 | 3.69 | add | True | self running key | plaintext@102 |
| LP2-27 | word | 103/234 | 4.11 | add | True | phrase-3 | MY HEAD THOUGHT |
| LP2-27 | ring | 42/234 | 3.96 | beaufort | True | affine position | 4·n+8 |
| LP2-28 | word | 114/269 | 3.44 | beaufort | False | phrase-3 | HE WENT TO |
| LP2-28 | ring | 45/269 | 3.66 | beaufort | False | self running key | plaintext@49 |
| LP2-29 | word | 140/277 | 3.74 | sub | False | self running key | plaintext@268 |
| LP2-29 | ring | 44/277 | 3.91 | sub | True | phrase-4-rev | ONLY YOUR SPECIES NOT ʳ |
| LP2-30 | word | 119/263 | 4.12 | beaufort | True | vigenere-word | YOUR |
| LP2-30 | ring | 44/263 | 3.92 | beaufort | False | phrase-4 | IN MY HEAD THOUGHT |
| LP2-31 | word | 126/269 | 4.24 | beaufort | False | self running key | plaintext@208 |
| LP2-31 | ring | 45/269 | 3.69 | beaufort | True | self running key | plaintext@698 |
| LP2-32 | word | 43/121 | 3.50 | add | False | phrase-2-rev | TO BE ʳ |
| LP2-32 | ring | 32/121 | 4.25 | beaufort | True | sentence-rev | WE FOLLOW DOGMA SO THAT WE CAN BELONG AN |
| LP2-33 | word | 104/214 | 3.47 | add | True | self running key | plaintext@2100 |
| LP2-33 | ring | 42/214 | 4.20 | beaufort | False | phrase-2-rev | THINGS ARE ʳ |
| LP2-34 | word | 120/261 | 3.78 | beaufort | False | self running key | plaintext@515 |
| LP2-34 | ring | 41/261 | 3.46 | add | False | self running key | plaintext@2060 |
| LP2-35 | word | 120/271 | 3.47 | sub | False | self running key | plaintext@643 |
| LP2-35 | ring | 45/271 | 4.59 | beaufort | True | affine position | 24·n+20 |
| LP2-36 | word | 100/238 | 3.48 | sub | True | self running key | plaintext@617 |
| LP2-36 | ring | 44/238 | 3.73 | sub | True | self running key | plaintext@2481 |
| LP2-37 | word | 105/228 | 3.28 | sub | True | self running key | plaintext@1911 |
| LP2-37 | ring | 39/228 | 3.44 | beaufort | True | primes | p[n+36] |
| LP2-38 | word | 93/228 | 3.55 | sub | False | phrase-4 | STUDENT TO EXPLAIN WHAT |
| LP2-38 | ring | 43/228 | 3.53 | sub | True | phrase-3-rev | THERE IS NOTHING ʳ |
| LP2-39 | word | 108/240 | 3.58 | beaufort | True | primes | p[n+2] |
| LP2-39 | ring | 40/240 | 4.61 | sub | True | phrase-3 | YOU WHO WISHES |
| LP2-40 | word | 109/231 | 3.53 | beaufort | True | self running key | plaintext@1293 |
| LP2-40 | ring | 38/231 | 3.66 | add | True | primes+1 | p[n+31]+1 |
| LP2-41 | word | 123/273 | 3.47 | beaufort | True | primes+1 | p[n+2]+1 |
| LP2-41 | ring | 46/273 | 4.22 | add | True | vigenere-word-rev | EXCEPTʳ |
| LP2-42 | word | 115/272 | 4.18 | sub | False | phrase-2 | OF ALL |
| LP2-42 | ring | 47/272 | 4.27 | beaufort | False | phrase-4-rev | THREE BEHAVIORS WHICH CAUSE ʳ |
| LP2-43 | word | 118/274 | 4.04 | add | True | primes-1 (totient) | p[n+94]-1 |
| LP2-43 | ring | 45/274 | 4.12 | beaufort | True | phrase-3 | THE MAN THOUGHT |
| LP2-44 | word | 113/273 | 4.18 | beaufort | False | self running key | plaintext@2778 |
| LP2-44 | ring | 44/273 | 4.12 | sub | True | affine position | 21·n+26 |
| LP2-45 | word | 124/270 | 3.52 | add | False | self running key | plaintext@1367 |
| LP2-45 | ring | 45/270 | 3.81 | beaufort | True | phrase-3-rev | FINALLY HE ANSWERED ʳ |
| LP2-46 | word | 122/270 | 3.75 | add | True | primes+1 | p[n+24]+1 |
| LP2-46 | ring | 45/270 | 3.98 | beaufort | True | vigenere-word | OURSELUES |
| LP2-47 | word | 116/274 | 4.07 | add | False | self running key | plaintext@2566 |
| LP2-47 | ring | 47/274 | 3.86 | sub | True | primes+1 | p[n+54]+1 |
| LP2-48 | word | 132/271 | 3.36 | beaufort | False | phrase-3-rev | A VOICE INSIDE ʳ |
| LP2-48 | ring | 46/271 | 3.83 | sub | True | phrase-2 | OF EVERY |
| LP2-49 | word | 35/66 | 3.00 | sub | True | self running key | plaintext@90 |
| LP2-49 | ring | 44/66 | 3.01 | beaufort | False | phrase-2 | WAY HERE |
| LP2-51 | word | 39/92 | 3.48 | add | True | self running key | plaintext@1897 |
| LP2-51 | ring | 48/92 | 4.11 | sub | True | vigenere-word | RIGHT |
| LP2-52 | word | 117/263 | 4.27 | sub | True | phrase-3-rev | WHAT YOU KNOW ʳ |
| LP2-52 | ring | 46/263 | 4.26 | add | True | sentence | WE PRESERVE THINGS BECAUSE WE BELIEVE WE |
| LP2-53 | word | 80/179 | 3.79 | sub | True | phrase-2-rev | KNOW THIS ʳ |
| LP2-53 | ring | 26/179 | 3.48 | beaufort | False | vigenere-word-rev | REALITYʳ |
| LP2-54 | word | 98/232 | 3.63 | sub | True | phrase-4-rev | TOWARD THE END OF ʳ |
| LP2-54 | ring | 40/232 | 3.63 | sub | False | self running key | plaintext@2588 |
| LP2-55 | word | 33/76 | 4.23 | sub | True | phrase-4-rev | WHAT YOU KNOW TO ʳ |
| LP2-55 | ring | 32/76 | 3.71 | add | True | phrase-3-rev | A BEING UNTO ʳ |

## Cells at z_uni >= 6.0 (0)

None.

## Hits (also z_5 >= 6.0): 0

None.

Largest z_uni over all cells: 5.08. Runtime 376 minutes.

