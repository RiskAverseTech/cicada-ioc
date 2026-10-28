# The 256-byte payload of LP2-49/50/51 as key material: 341 keys x 6 cells x 55 pages = 112,530 tests

Readings, rule and prior coverage (wazar B-05, E-01, E-02, numeric round 2, Round 8 POINTERS) in the module docstring. Contested bytes (I/l, O/0 glyphs): LP2-49 positions [25, 45, 50], LP2-50 positions [95, 102], LP2-51 positions [15, 31, 53, 62]; both readings run.

## Controls

| key | n | sign | F | z_uni | z_5 | rank | pass |
|---|---|---|---|---|---|---|---|
| archive fwd (R1 byte mod 29) | 262 | sub | False | 12.2 | 56.8 | 1 | yes |
| token-reading fwd (R2 rejection) | 137 | add | False | 8.4 | 43.1 | 1 | yes |
| p[n+5] (P prime offset) | 262 | beaufort | True | 12.5 | 35.1 | 1 | yes |
| solved words[b mod count] (W word pointer) | 137 | sub | True | 8.8 | 34.2 | 1 | yes |

Controls passing: 4 of 4.

## Top 10 cells

| page | sign | F | family | key | z_uni | z_5 | transliteration |
|---|---|---|---|---|---|---|---|
| LP2-43 | add | True | P prime offset | p[n+112] | 4.86 | -1.2 | TNGONGNGWNGTHYSSBLAYNYGLNDIFSLEFILEANYYGIAEENFESLBDNGIAEOIAU |
| LP2-43 | add | True | P prime offset | p[n+111] | 4.40 | -1.6 | EOMLJMOSAEAOSBLAYNYGLNDIFSLEFILEANYYGIAEENFESLBDNGIAEOIAULIA |
| LP2-25 | beaufort | True | P totient offset | phi(p[n+124]) | 4.32 | -4.2 | SAGSTTHEALIEUNGXSTXTNGRWLTEJUENUPSYCCMATIJNOMYEAWTFRABSTHABW |
| LP2-06 | beaufort | True | P totient offset | phi(p[n+33]) | 3.97 | 0.6 | HIAEODNPTWLNPHAGWUEAIIABLNDTHEAMWUNAOXPRWTHGRTHDHBOBJXTMPONG |
| LP2-52 | add | True | R4 index component | fwd | 3.96 | -0.5 | WFEOIULHEAISDRNNGIAAEWELMYLRWTHTHWDNNGFFSUIAXUIMYUFSLDUCRNON |
| LP2-06 | beaufort | False | P totient offset | phi(p[n+33]) | 3.94 | 0.3 | HIAEODNPTWLNPHAGWUEAIIABLNDTHEAMWUNAOXPRWTHGRTHDHBOBJXGBWEAS |
| LP2-41 | sub | True | P totient offset | phi(p[n+52]) | 3.92 | 1.1 | LNGFXMIRCPUOEYNGNGETAGYOUYTBCBIGSLNGMXDDFLHHMWAEASCRATEONFNY |
| LP2-51 | sub | True | P totient offset | phi(p[n+173]) | 3.72 | -2.3 | MPNDJTHMRNGSAENIACBCGTHNWWEANAEAEOLOSANFAEAOTROAIASNRDYEYONW |
| LP2-14 | sub | True | P prime offset | p[n+81] | 3.71 | 1.0 | USFCTSAPHNGORCRAEONGINGWTHGAEHRTTHTHRRUUGUNRIATRSNGIIUICEAAP |
| LP2-29 | beaufort | True | P totient offset | phi(p[n+133]) | 3.70 | -0.5 | FEOHBTOENUWEHDTHARSAITHBEAMBEARBNUEANGDCHRSTSHGNGFOEEOAEFLDP |

## Candidates

None.

Largest z_uni 4.86; largest z_5 1.95. Runtime 4 minutes.

