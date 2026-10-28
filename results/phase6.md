# Phase 6: word-edge events under the skip rule (pnotisdev registry item `open-unkeyed`, run independently)

Kinds adv / advline / nulli / nullf at event rate nu = 0.42; 22863 configurations (phase 3 book families and phase 4 phrase keys, three sign conventions) x 55 pages x 2 F variants x 4 kinds = **10,059,720 tests**; chance maximum about 5.7.
Per page, kind, variant and decoder mode the null is 2,000 random keystreams through the same edge decoder. Pre-registered hit rule: z >= 6 over that null AND edge score minus base score for the same configuration >= 20 nats AND readable English.

## Planted controls (nu = 0.42, skip 0.81)

| control | kind | sign | family | key | F | page | events | edge z | rank | edge − base (nats) | base-decoder z | runes recovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | adv | sub | phrase-2 | INSTAR TUNNELING | False | LP2-00 | 25 | 12.6 | 1 | +190.9 | 2.4 | 0.893 |
| control-01 | advline | sub | phrase-4-rev | DOGMA SO THAT WE ʳ | False | LP2-01 | 4 | 13.7 | 1 | +237.6 | 1.3 | 1.000 |
| control-02 | nulli | sub | phrase-3 | BUT HE COULD | False | LP2-02 | 16 | 11.9 | 1 | +199.5 | -0.2 |  |
| control-03 | nullf | sub | sentence-rev | ULTIMATELY YOU WILL DISCOVER A | False | LP2-03 | 23 | 10.9 | 1 | +191.3 | 0.7 |  |
| control-04 | adv | add | phrase-4 | DOOR OF THE MASTER | False | LP2-04 | 19 | 12.8 | 1 | +200.0 | 2.4 | 0.962 |
| control-05 | advline | add | phrase-2-rev | HAND TO ʳ | False | LP2-05 | 5 | 13.9 | 1 | +90.7 | 8.0 | 1.000 |
| control-06 | nulli | add | sentence | WE HAVE WHAT WE HAVE NOW BY LU | False | LP2-06 | 19 | 10.5 | 1 | +113.2 | 3.8 |  |
| control-07 | nullf | add | phrase-3-rev | HERE ASKED THE ʳ | False | LP2-07 | 23 | 11.2 | 1 | +122.7 | 3.8 |  |
| control-08 | adv | beaufort | phrase-2 | THIS BOOK | False | LP2-08 | 19 | 14.6 | 1 | +141.4 | 5.9 | 0.988 |
| control-09 | advline | beaufort | phrase-4-rev | NEVER BECOME ATTACHED TO ʳ | False | LP2-09 | 5 | 13.7 | 1 | +132.4 | 6.5 | 1.000 |
| control-10 | nulli | beaufort | phrase-3 | YOU DO NOT | False | LP2-10 | 25 | 12.9 | 1 | +151.3 | 4.5 |  |
| control-11 | nullf | beaufort | sentence-rev | DO NOT EDIT OR CHANGE THIS BOO | False | LP2-11 | 24 | 11.4 | 1 | +198.4 | 1.9 |  |
| control-12 | adv | sub | primes-1 (totient) | p[n+1]-1 | True | LP2-12 | 25 | 12.2 | 3 | +276.1 | -3.1 | 0.870 |
| control-13 | advline | sub | vigenere-word-rev | YOUʳ | True | LP2-13 | 5 | 16.7 | 1 | +57.4 | 12.1 | 0.963 |
| control-14 | nulli | sub | primes+1 | p[n+13]+1 | True | LP2-14 | 9 | 9.9 | 1 | +47.6 | 5.6 |  |
| control-15 | nullf | sub | vigenere-word | PRIMALITY | True | LP2-15 | 16 | 8.4 | 1 | +88.4 | 2.7 |  |
| control-16 | adv | add | primes | p[n+50] | True | LP2-16 | 16 | 11.9 | 1 | +165.5 | 2.7 | 0.966 |
| control-17 | advline | add | square position | n²+9 | True | LP2-17 | 4 | 14.1 | 1 | +19.6 | 12.6 | 0.967 |
| control-18 | nulli | add | lucas | L[n+10] | True | LP2-18 | 21 | 13.0 | 1 | +134.8 | 4.7 |  |
| control-19 | nullf | add | shift | s=10 | True | LP2-19 | 35 | 11.7 | 1 | +33.1 | 11.5 |  |
| control-20 | adv | beaufort | fibonacci | F[n+6] | True | LP2-20 | 34 | 13.7 | 1 | +170.9 | 3.7 | 0.903 |
| control-21 | advline | beaufort | self running key | plaintext@119 | True | LP2-21 | 3 | 13.3 | 1 | +136.8 | 5.0 | 0.993 |
| control-22 | nulli | beaufort | affine position | 10·n+25 | True | LP2-22 | 11 | 6.8 | 2 | +59.9 | 3.1 |  |
| control-23 | nullf | beaufort | primes-1 (totient) | p[n+11]-1 | True | LP2-23 | 22 | 10.2 | 1 | +170.8 | -0.2 |  |

Controls recovered at z >= 6 and rank 1 under the edge decoder: 22 of 24; the base decoder (no events) would have scored them at z -3.1 to 12.6.

## Unsolved pages: top 20 configurations overall

| page | kind | sign | F | family | key | z | edge − base | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|---|---|
| LP2-17 | adv | sub | True | phrase-4-rev | MUST SHED OUR OWN ʳ | 5.51 | +136.0 | 30 | JAIMUNDMNUNMITHCBAPOHECIMOUCDLASIAEDFDEAODEMIFUCULNNIASINNOCFNYSFEAETHERNHOERNNGRUEAOETHH |
| LP2-07 | advline | sub | True | self running key | plaintext@456 | 5.24 | +30.5 | 9 | THOEWUHTSYHXTHTHIINLNGPIARWTFMABEDFRNGSPTWREACFFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMALDWWA |
| LP2-20 | nullf | sub | True | phrase-4-rev | JUST SAID YOU HAVE ʳ | 5.15 | +145.1 | -31 | AIGNCWEOTLTEWSHOBGIALONMCCTHRIAINEOPDIFAGEUSFEFWWEAWALWHTCAWTHROLSFEIAROSEEWTRERPITHHRTEOU |
| LP2-19 | adv | sub | True | affine position | 7·n+1 | 5.13 | +108.3 | 29 | HAWTFEEUATHEEANSNSWFUFLAECITHWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-19 | adv | add | True | affine position | 22·n+28 | 5.13 | +108.3 | 29 | HAWTFEEUATHEEANSNSWFUFLAECITHWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-23 | adv | add | False | phrase-3 | THE FOLLWING TWO | 5.12 | +134.0 | 27 | OPWAYCUIAYAPUTLUBGIATHOTNHEAOTHMDSPAEALHEARANMREDEWMSYALMHFCUDCJSWPJEPHEALDELRTFAMOUITM |
| LP2-07 | nullf | sub | True | self running key | plaintext@666 | 5.05 | +133.1 | -25 | CUDWBGANGMTDMFATSRNXNFEUIFYTHETIIBAAPNMCOEASRNNCRCHPNOEAEWEOIADDNJNMPISAARALIRADCSDNTE |
| LP2-55 | advline | add | True | phrase-3-rev | TO STUDY HERE ʳ | 5.03 | +5.2 | 0 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWURDSNGTWWSRWUNGECRTLISNONLTHYHNOTHHAERP |
| LP2-05 | nullf | sub | True | phrase-3-rev | OBTAIN WHAT WE ʳ | 4.98 | +87.3 | -26 | SEIAPOEIICERLNGXTIWSNTIANGUELEBTHLIAXLMWYHIUISEGYLOPBCANGSITRRBTGNYATHECAIXORDFRESTYPNYC |
| LP2-12 | adv | add | False | phrase-3-rev | A VOICE INSIDE ʳ | 4.97 | +154.4 | 38 | DRXLTNUNGCGOMNGBHTUEJTOUSACCTSDTHWFECTHYLTHEOSTTHOOXCALOSDTHEPNGNSTTNRUINLUIIAMWIARRNFBRIO |
| LP2-19 | adv | sub | True | affine position | 7·n+8 | 4.95 | +113.4 | 28 | UBFNFEEUATHEEANSNSWFUFLAECITHWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-19 | adv | add | True | affine position | 22·n+21 | 4.95 | +113.4 | 28 | UBFNFEEUATHEEANSNSWFUFLAECITHWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-55 | adv | add | False | phrase-4 | THOUGHT FOR A MOMENT | 4.91 | +47.4 | 9 | DEALTSSLENETHAOEIAURORCRTHDLEEDYNGRGMTHLSDIPUOERISGEYSEPINAEEHRNGERNGTINHOCNHROIAOEAE |
| LP2-03 | advline | sub | True | self running key | plaintext@1512 | 4.88 | +46.4 | 3 | AETHSGFTJUWAPEAPMSMWABTHTHEARBEENWFTHNUIDEEDOTHATHNYNLHTHBLTASWFHEAPWMIOMTYFGLBTHWPFAEWNXDEIA |
| LP2-15 | nulli | beaufort | True | phrase-3-rev | GREAT JOURNEY TOWARD ʳ | 4.88 | +92.2 | -21 | DORBARMRDEONDGSBMBGTHDDYTHOELSEPOAYRSMYWONIXEEAIIAGIAUCWPIARLOXNEATGNGRRAOUTIOLGETLTO |
| LP2-23 | advline | sub | False | affine position | 24·n+23 | 4.88 | +52.9 | 11 | WGDPOTUEIAIHSAUEALIAIAIOTHMROEYOONTBSNIAEASNNFEAWDTNGEATHHPBTHASACAHFLRTHYEIAIDCWAEAWNSUPELNREAH |
| LP2-23 | advline | add | False | affine position | 5·n+6 | 4.88 | +52.9 | 11 | WGDPOTUEIAIHSAUEALIAIAIOTHMROEYOONTBSNIAEASNNFEAWDTNGEATHHPBTHASACAHFLRTHYEIAIDCWAEAWNSUPELNREAH |
| LP2-07 | nullf | sub | True | self running key | plaintext@667 | 4.88 | +151.2 | -26 | BNGDWBGANGMTDMFATSRNXNFEUIFYTHETIIBAAPNMCOEASRNNCRCHPNOEAEWEOIADDNJNMPISAARALIRADCSDNTE |
| LP2-07 | advline | sub | False | self running key | plaintext@456 | 4.88 | +27.1 | 9 | THOEWUHTSYHXTHTHIINLNGPIRENGAEYMABEDFRNGSPTWREACFFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMALDWWA |
| LP2-55 | adv | add | True | phrase-3-rev | TO STUDY HERE ʳ | 4.87 | +5.2 | 0 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWURDSNGTWWSRWUNGECRTLISNONLTHYHNOTHHAERP |

Largest z over all 10,059,720 tests: 5.51. Cells meeting the pre-registered rule (z >= 6 and edge − base >= 20): 0.
Largest z per kind: adv 5.51; advline 5.24; nulli 4.88; nullf 5.15.

## Verdict

**No page decrypts under any word-edge or line-edge event kind.** Extra key advances at word or line starts and unencrypted null runes at word starts or ends, at the 42 % rate pnotisdev's word-length fit implies, combined with this repository's key families under the skip rule, all three sign conventions and both F variants, are excluded at the sensitivity the controls demonstrate. Not covered: nulls inside words, non-uniform null runes, more than one event per position, event rates far from 0.42, key streams outside these families, and pnotisdev's own 1,447-stream library.

