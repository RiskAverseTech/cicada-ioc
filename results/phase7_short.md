# Phase 7 (skip-by-two) on the nine short pages: 5-gram rescoring (README §37)

Rule: z_uni >= 3.5 and z_5 >= 6.0 (5-gram over 400 random keystreams through the same decoder) and readable; controls planted at short lengths.

## Controls

| n | set | key | F | z_uni | z_5 | rank | pass |
|---|---|---|---|---|---|---|---|
| 92 | sub | A LONG | False | 5.9 | 32.4 | 1 | yes |
| 137 | add | ELSE TO SAY SO ʳ | False | 8.3 | 36.6 | 1 | yes |
| 159 | beaufort | CIRCUMFERENCE PRACTICES THREE | False | 9.0 | 49.9 | 1 | yes |
| 196 | sub | p[n+26]+1 | False | 9.3 | 44.8 | 1 | yes |
| 92 | add | TOLD | False | 6.1 | 28.4 | 1 | yes |
| 137 | beaufort | p[n+22] | False | 7.9 | 35.8 | 1 | yes |
| 159 | sub | MOST THINGS ARE NOT WORTH PRESERVING | True | 9.7 | 44.5 | 1 | yes |
| 196 | add | WORDS OR THEIR ʳ | True | 12.2 | 45.0 | 1 | yes |
| 92 | beaufort | OF THOUGHT | True | 7.5 | 25.5 | 1 | yes |
| 137 | sub | F[n+2] | True | 9.0 | 38.2 | 1 | yes |
| 159 | add | plaintext@765 | True | 10.2 | 38.5 | 1 | yes |
| 196 | beaufort | 12·n+27 | True | 12.7 | 43.4 | 1 | yes |
| 92 | sub | BELIEVE NOTHING FROM THIS | False | 6.4 | 31.2 | 1 | yes |
| 137 | add | LUCK AND ʳ | False | 8.5 | 44.5 | 1 | yes |
| 159 | beaufort | DURING A LESSON THE MASTER EXPLAINED THE I | False | 8.3 | 41.2 | 1 | yes |
| 196 | sub | PREPARED | False | 10.1 | 39.2 | 1 | yes |
| 92 | add | p[n+31] | False | 6.2 | 31.5 | 1 | yes |
| 137 | beaufort | n²+20 | False | 7.4 | 34.4 | 1 | yes |
| 159 | sub | OR THE MESSAGE | True | 10.6 | 29.2 | 1 | yes |
| 196 | add | THE MAN WAS GETTING IRRITATED ʳ | True | 10.6 | 33.8 | 1 | yes |
| 92 | beaufort | RIGHT ABOUT TO BELONG | True | 7.9 | 29.4 | 1 | yes |
| 137 | sub | plaintext@2887 | True | 9.0 | 33.1 | 1 | yes |
| 159 | add | 25·n+1 | True | 9.5 | 36.5 | 1 | yes |
| 196 | beaufort | p[n+71]-1 | True | 11.2 | 37.6 | 1 | yes |

Controls passing: 24 of 24.

## Best cell per page

| page | set | F | family | key | z_uni | z_5 | transliteration |
|---|---|---|---|---|---|---|---|
| LP2-06 | beaufort | True | primes-1 (totient) | p[n+32]-1 | 4.07 | 0.2 | GBTYBCWICIWWDFMUAETHSBLNDTHEAMWUNAOXPRWTHGRTHDHBOB |
| LP2-14 | sub | True | self running key | plaintext@2424 | 4.43 | -3.0 | GNFXIPDRTMONDPEAEORRNGWIADRHSHLWCIRALRDEGNTLLROFUF |
| LP2-15 | beaufort | True | phrase-2 | INSIDE YOUR | 4.00 | -2.5 | FNEAESANGRHIOEFINGNIONDNEAXBUNGUHNONGPERCMXUBNLAAT |
| LP2-22 | sub | True | sentence-rev | THAT IS NOT WHO YOU ARE THAT IS ONLY WHAT YOU ARE CALLED ʳ | 3.70 | 0.0 | IAUMSTUTEAWBSTEFAHLESSRATRTOHIACUAROATWHHTWNLTNGEA |
| LP2-32 | add | True | self running key | plaintext@2528 | 3.52 | -1.0 | DOFSAADNGHTHTTHEHIDNGEAHTHYEATTNGGMOFFNIACHRUHBRFF |
| LP2-49 | beaufort | True | phrase-4-rev | BEHAVIORS WHICH CAUSE THE ʳ | 3.19 | -1.2 | LPWSITHAOAETHCAEETHAFNEAWURTHGNCONGHXYEWFNFAFEHDRS |
| LP2-51 | sub | True | self running key | plaintext@141 | 3.90 | 0.4 | YCOFETHRSLUBLYTRHILWSNSHIAEJWADIAIHLGEHHHRFJEUNGTO |
| LP2-53 | beaufort | False | phrase-2-rev | YOU KNOW ʳ | 3.71 | -0.6 | AWINRTHWDEEARNGFRIAYSOOWMPILUJDHEAYNGRMTHABXSPNUGC |
| LP2-55 | add | True | phrase-3-rev | TO STUDY HERE ʳ | 4.69 | 0.3 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWFEAIA |

## Candidates

None.

Largest z_uni 4.69; largest z_5 2.56.

