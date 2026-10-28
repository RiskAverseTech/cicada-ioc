# Phase 6 (word-edge events) on the nine short pages: 5-gram rescoring (README §37)

Rule: z_uni >= 3.5 and z_5 >= 6.0 (5-gram over 400 random keystreams through the same decoder) and readable; controls planted at short lengths.

## Controls

| n | set | key | F | z_uni | z_5 | rank | pass |
|---|---|---|---|---|---|---|---|
| 196 | adv sub | INSTAR TUNNELING | False | 10.4 | 24.2 | 1 | yes |
| 137 | advline sub | PILGRIM TO THE GREAT ʳ | False | 8.5 | 25.5 | 1 | yes |
| 159 | nulli sub | THAT IS WHAT | False | 8.6 | 7.4 | 1 | yes |
| 131 | nullf sub | AFTER A MOMENT OF THOUGHT THE  | False | 10.5 | 21.2 | 1 | yes |
| 121 | adv add | AND BE RIGHT OR | False | 8.9 | 28.4 | 1 | yes |
| 66 | advline add | YOUR INNOCENCE ʳ | False | 6.1 | 33.9 | 1 | yes |
| 92 | nulli add | FOR ALL THAT LIVES IS HOLY | False | 5.7 | 9.0 | 1 | yes |
| 179 | nullf add | THE WORDS OR ʳ | False | 7.0 | 7.3 | 1 | yes |
| 76 | adv beaufort | ALL IS | False | 5.4 | 21.8 | 1 | yes |
| 196 | advline beaufort | HIS HAND TO TELL ʳ | False | 11.9 | 40.8 | 1 | yes |
| 137 | nulli beaufort | MASTER HIS NAME | False | 8.8 | 18.3 | 1 | yes |
| 159 | nullf beaufort | IF WE LOSE THEM WE WILL NOT BE | False | 9.3 | 12.7 | 1 | yes |
| 131 | adv sub | p[n+75]-1 | True | 7.8 | 25.4 | 1 | yes |
| 121 | advline sub | YOUʳ | True | 8.5 | 31.9 | 1 | yes |
| 66 | nulli sub | p[n+56]+1 | True | 4.8 | 11.3 | 2 | no |
| 92 | nullf sub | MIND | True | 5.6 | 6.4 | 1 | yes |
| 179 | adv add | p[n+87] | True | 9.9 | 25.0 | 1 | yes |
| 76 | advline add | n²+22 | True | 6.2 | 18.2 | 1 | yes |
| 196 | nulli add | L[n+13] | True | 8.9 | 11.4 | 1 | yes |
| 137 | nullf add | s=20 | True | 8.1 | 9.0 | 1 | yes |
| 159 | adv beaufort | F[n+1] | True | 10.6 | 20.0 | 1 | yes |
| 131 | advline beaufort | plaintext@2698 | True | 9.5 | 31.0 | 1 | yes |
| 121 | nulli beaufort | 2·n+19 | True | 7.9 | 12.8 | 1 | yes |
| 66 | nullf beaufort | p[n+89]-1 | True | 5.0 | 6.4 | 3 | no |

Controls passing: 22 of 24.

## Best cell per page

| page | set | F | family | key | z_uni | z_5 | transliteration |
|---|---|---|---|---|---|---|---|
| LP2-06 | nulli sub | False | sentence-rev | IF WE LOSE THEM WE WILL NOT BE STRONG ENOUGH TO GAIN THEM AG ʳ | 3.86 | -0.3 | CAIPRDXSMAEEATEAEXTHLUIAMRUNDITSNYDIAWDAPSTHSWOEAH |
| LP2-14 | nulli add | True | self running key | plaintext@450 | 4.75 | -0.6 | WBRPIESAWLUGEANMHTRGSUEONUITHNGDYBLNLTHUECGFHEUWAE |
| LP2-15 | nulli beaufort | True | phrase-4-rev | MY HEAD THOUGHT THE ʳ | 5.19 | -2.1 | EUAEEAWRIWOIATBCEBNSTTICLTHUOYFUEGRMODNRORDRCLFHNN |
| LP2-22 | adv sub | False | affine position | 12·n+18 | 4.23 | -0.3 | OEYIOSTHBRHNGNFMIRHTRCMENFICDAPDFOERAMSEEORBXMIPIU |
| LP2-32 | nulli beaufort | False | self running key | plaintext@2948 | 3.93 | -1.7 | ATHROAEHIRPTEOEONGLUREFROEOWTNGIAMTHBEFURHSCEIYSGY |
| LP2-49 | adv sub | True | phrase-3 | WHO WISHES TO | 3.98 | 2.2 | LSRFIWTHTACOATHSLTIOWNANDPUTFDEOSUMNMBNOWTGPLODLOH |
| LP2-51 | advline sub | False | self running key | plaintext@1248 | 4.11 | -2.1 | TITYYTEARLFNLEICSESHLAABOUDTIONNGXNGFTHLSTNNHRREAL |
| LP2-53 | adv add | False | primes+1 | p[n+75]+1 | 4.39 | -0.9 | MNLNGUSGIPSIAYLNIIYYOEDANUOEAITLHDIIPPOEFTHIURSGTS |
| LP2-55 | advline add | True | phrase-3-rev | TO STUDY HERE ʳ | 5.11 | 0.8 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWURDSN |

## Candidates

None.

Largest z_uni 5.19; largest z_5 2.22.

