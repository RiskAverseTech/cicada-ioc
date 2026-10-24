# Phase 3 sweep: the book's keystream families with the skip-on-repeat rule

4716 shared keystream configurations (+ up to 4 neighbour-page keys per page), 55 pages, 2 F-rule variants: about 519,200 tests.
Per page and variant, the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.

## Planted controls

| control | family | key | F rule | z of true key | rank among all configs | runes recovered |
|---|---|---|---|---|---|---|
| control-00 | vigenere-word | IS | False | 11.6 | 5 | 0.996 |
| control-01 | primes-1 (totient) | p[n+24]-1 | True | 12.7 | 1 | 0.979 |
| control-02 | affine position | 27·n+0 | False | 11.7 | 1 | 1.000 |
| control-03 | self running key | plaintext@1746 | True | 13.0 | 2 | 1.000 |
| control-04 | shift | s=22 | False | 12.0 | 1 | 1.000 |
| control-05 | vigenere-word | DUTY | True | 12.2 | 1 | 0.992 |
| control-06 | primes-1 (totient) | p[n+99]-1 | False | 13.0 | 1 | 1.000 |
| control-07 | affine position | 10·n+14 | True | 15.2 | 1 | 1.000 |
| control-08 | self running key | plaintext@2325 | False | 11.0 | 1 | 0.988 |
| control-09 | shift | s=16 | True | 11.7 | 6 | 0.988 |
| control-10 | vigenere-word | BELONG | False | 11.2 | 1 | 1.000 |
| control-11 | primes-1 (totient) | p[n+72]-1 | True | 12.3 | 1 | 1.000 |
| control-12 | affine position | 23·n+28 | False | 10.5 | 1 | 1.000 |
| control-13 | self running key | plaintext@1855 | True | 12.9 | 1 | 1.000 |
| control-14 | shift | s=27 | False | 12.0 | 1 | 1.000 |
| control-15 | vigenere-word | WITH | True | 12.8 | 1 | 0.992 |
| control-16 | primes-1 (totient) | p[n+14]-1 | False | 10.9 | 1 | 0.992 |
| control-17 | affine position | 14·n+1 | True | 13.1 | 1 | 0.979 |
| control-18 | self running key | plaintext@2840 | False | 12.6 | 1 | 1.000 |
| control-19 | shift | s=12 | True | 12.5 | 1 | 0.975 |

Controls recovered at z ≥ 6 and rank 1: 17 of 20.

## Unsolved pages: top 15 configurations overall

| page | F rule | family | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|
| LP2-35 | True | self running key | plaintext@882 | 4.67 | 3 | IAMIAXYTHTITTHLYTHWOEOELRTHGMLHUTBBGNGHNWNGEAYXFSTHENGSMNGEBBBMHIFTHXGNNGEASFMHOPMFHEWSLNTBOEAO |
| LP2-47 | True | primes+1 | p[n+32]+1 | 4.40 | 4 | GSYISUHCBTHDFIMECEGIAPJNGTIHREARSFNGNBEALUIACALAWRERSTHXHAUIAPDORHAEFCLIABEEDWYJYOEOPJWNGOETHMIA |
| LP2-35 | True | self running key | plaintext@878 | 4.25 | 7 | IAUEDCFEAAFDMGANNGYMEPTEAYWHOUDTNGWFANGNGPNWFTHHEORMSNHDNGYIAHAEHHTHPWWNLOWAERTHTFIATHUMIGNREUEO |
| LP2-07 | True | self running key | plaintext@2791 | 4.21 | 12 | EAEPFWFINGTDRPANRSWDLIUGEOTHIATHAOORARTNSORTUMTHSOUWUPAIEGBIFPWYSNGGAWIUDSOWLCFUJATWWGAE |
| LP2-35 | True | self running key | plaintext@883 | 4.17 | 2 | ANAOERWJMSFCOENGENGNGJLBOMMLHUTBBGNGHNWNGEAYXFSTHENGSMNGEBBBMHIFTHXGNNGEASFMHOPMFHEWSLNTBOEAO |
| LP2-20 | False | self running key | plaintext@2094 | 4.13 | 8 | AWLJIADNNWHPMJOUNGLEAGAHCCAWNIATWDDTHWCTWNPJMSNGBCRPUAEHFANGONGDASTHLRNGRSFEBCIREAAEFUTBTHHTHA |
| LP2-41 | True | primes-1 (totient) | p[n+53]-1 | 4.12 | 5 | ISDHBRRCPUOEYNGNGETAGYOUYTBCBIGSLNGMXDDFLHHMWAEASCRATEONFNYORXTOIAEAEPRTOHTEAHXFNINSMCB |
| LP2-07 | True | self running key | plaintext@499 | 4.12 | -1 | MOWAWPANGIDRDTHIWXENGMASOFUFBIACTHRTTHJDDNHTOECOWOEOCOEAEIMTHUDIARWWREONGUEOIMJOITHNGUOPTGDCMT |
| LP2-07 | True | self running key | plaintext@456 | 4.11 | 9 | THMAESIYMOEIMNBRWAERHDEARIMIAEFTAOEYRDIPEBANUDAENGFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMFWDEATM |
| LP2-47 | True | primes+1 | p[n+30]+1 | 4.09 | 6 | TDNOEDPESFIRJIMECEGIAPJNGTIHREARSFNGNBEALUIACALAWRERSTHXHAUIAPDORHAEFCLIABEEDWYJYOEOPJWNGOETHMIA |
| LP2-07 | True | self running key | plaintext@457 | 4.08 | 8 | MMAESIYMOEIMNBRWAERHDEARIMIAEFTAOEYRDIPEBANUDAENGFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMFWDEATM |
| LP2-07 | False | self running key | plaintext@2791 | 4.08 | 12 | EAEPFWFINGTDRPANRSWDLIUGEOTHIATHAOORARTNSORTUMTHSOUWUPAIEGBIFPWYSNGGAWIUDSOWLCFUJATWWGAE |
| LP2-17 | True | vigenere-word | OWN | 4.07 | -3 | BARLAOXLSXBFTIAFSLIAENAEEJMOODXEGNAWHSSCNGETTHFUNGIAEBTINLSNYGFOFACYOXURPCAELHRPWTWOEGR |
| LP2-01 | True | self running key | plaintext@842 | 4.03 | -1 | ANEAMWYECITHLOOTHFLELXEYIAHNEAWNCHPDHWNGPTFCTFIAIGSNGATEOENMCAMMRGROEODHEATHXTHNGERGTPLIIAAEN |
| LP2-29 | True | self running key | plaintext@1608 | 4.02 | -6 | HLGIASTSBYOELMSNGDJHDTNETDWNIAWCMEICOEGPFTTFSFRESABXEECOYAETHTHGDNGNGESYYYNFSLWOYPOYOIAOEHCEA |

Largest z over all 519,200 tests: 4.67. Expected chance maximum for this many tests: about 4.8.

## Verdict

**No page decrypts.** The families tested (constant shifts, Vigenère with every word of the solved text and headlines, prime streams p, p−1, p+1 at 101 starting points, Fibonacci and Lucas, affine and square position formulas, the solved plaintext as a running key at every offset, and neighbouring pages as running keys), each with and without the F rule and with the skip-on-repeat rule, are excluded at the sensitivity the controls demonstrate. This says nothing about keystreams outside these families.

