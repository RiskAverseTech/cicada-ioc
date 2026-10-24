# Phase 6: word-edge events under the skip rule (pnotisdev registry item `open-unkeyed`, run independently)

Kinds adv / advline / nulli / nullf at event rate nu = 0.42; 22863 configurations (phase 3 book families and phase 4 phrase keys, three sign conventions) x 55 pages x 2 F variants x 4 kinds = **10,059,720 tests**; chance maximum about 5.7.
Per page, kind, variant and decoder mode the null is 2,000 random keystreams through the same edge decoder. Pre-registered hit rule: z >= 6 over that null AND edge score minus base score for the same configuration >= 20 nats AND readable English.

## Planted controls (nu = 0.42, skip 0.81)

| control | kind | sign | family | key | F | page | events | edge z | rank | edge − base (nats) | base-decoder z | runes recovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | adv | sub | phrase-2 | INSTAR TUNNELING | False | LP2-00 | 29 | 12.9 | 1 | +206.4 | 1.9 | 0.905 |
| control-01 | advline | sub | phrase-4-rev | AND THUS OUR DIVINITY ʳ | False | LP2-01 | 4 | 13.5 | 1 | +16.5 | 11.5 | 0.921 |
| control-02 | nulli | sub | phrase-3 | EXPLAIN WHAT THAT | False | LP2-02 | 18 | 9.8 | 1 | +143.3 | 1.5 |  |
| control-03 | nullf | sub | sentence-rev | WHEN ASKED BY A STUDENT TO EXP | False | LP2-03 | 22 | 9.4 | 1 | +191.3 | 0.2 |  |
| control-04 | adv | add | phrase-4 | THE MAN THOUGHT FOR | False | LP2-04 | 25 | 12.3 | 1 | +179.4 | 3.1 | 0.904 |
| control-05 | advline | add | phrase-2-rev | HERE HE ʳ | False | LP2-05 | 7 | 12.8 | 1 | +75.6 | 8.1 | 0.970 |
| control-06 | nulli | add | sentence | IT IS THE BEHAVIORS OF CONSUMP | False | LP2-06 | 24 | 10.1 | 1 | +184.7 | 0.2 |  |
| control-07 | nullf | add | phrase-3-rev | VOICE INSIDE YOUR ʳ | False | LP2-07 | 21 | 9.1 | 1 | +137.8 | 2.5 |  |
| control-08 | adv | beaufort | phrase-2 | TO COME | False | LP2-08 | 16 | 12.6 | 1 | +129.7 | 5.4 | 0.922 |
| control-09 | advline | beaufort | phrase-4-rev | AND BE RIGHT OR ʳ | False | LP2-09 | 4 | 15.3 | 1 | +113.8 | 7.4 | 0.993 |
| control-10 | nulli | beaufort | phrase-3 | ANYTHING ELSE TO | False | LP2-10 | 34 | 15.0 | 1 | +248.8 | 0.2 |  |
| control-11 | nullf | beaufort | sentence-rev | WE CONSUME TOO MUCH BECAUSE WE | False | LP2-11 | 15 | 14.6 | 1 | +160.3 | 5.4 |  |
| control-12 | adv | sub | primes-1 (totient) | p[n+59]-1 | True | LP2-12 | 33 | 13.5 | 1 | +196.0 | 0.6 | 0.897 |
| control-13 | advline | sub | vigenere-word-rev | THNGSʳ | True | LP2-13 | 6 | 15.0 | 1 | +27.1 | 12.2 | 0.890 |
| control-14 | nulli | sub | primes+1 | p[n+13]+1 | True | LP2-14 | 15 | 8.5 | 1 | +97.9 | 1.7 |  |
| control-15 | nullf | sub | vigenere-word | ONE | True | LP2-15 | 16 | 7.0 | 24 | +24.1 | 6.7 |  |
| control-16 | adv | add | primes | p[n+6] | True | LP2-16 | 26 | 11.8 | 1 | +156.4 | 3.5 | 0.925 |
| control-17 | advline | add | square position | n²+6 | True | LP2-17 | 4 | 14.0 | 1 | +32.1 | 11.4 | 0.974 |
| control-18 | nulli | add | lucas | L[n+4] | True | LP2-18 | 25 | 11.0 | 1 | +161.4 | 1.4 |  |
| control-19 | nullf | add | shift | s=22 | True | LP2-19 | 33 | 11.5 | 1 | +22.3 | 11.1 |  |
| control-20 | adv | beaufort | fibonacci | F[n+3] | True | LP2-20 | 32 | 12.8 | 1 | +172.5 | 2.8 | 0.833 |
| control-21 | advline | beaufort | self running key | plaintext@2624 | True | LP2-21 | 3 | 15.0 | 1 | +62.7 | 10.4 | 0.996 |
| control-22 | nulli | beaufort | affine position | 15·n+16 | True | LP2-22 | 10 | 8.6 | 1 | +71.9 | 3.4 |  |
| control-23 | nullf | beaufort | primes-1 (totient) | p[n+55]-1 | True | LP2-23 | 24 | 8.5 | 1 | +131.9 | 1.2 |  |

Controls recovered at z >= 6 and rank 1 under the edge decoder: 23 of 24; the base decoder (no events) would have scored them at z 0.2 to 12.2.

## Unsolved pages: top 20 configurations overall

| page | kind | sign | F | family | key | z | edge − base | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|---|---|
| LP2-15 | nulli | beaufort | True | phrase-4-rev | MY HEAD THOUGHT THE ʳ | 5.24 | +106.7 | -14 | EUAEEAWRIWOIATBCEBNSTTICLTHUOYFUEGRMODNRORDRCLFHNNAUUADEIEAATBNGERMLSMEEATHDTWGAIAOSAILR |
| LP2-07 | advline | sub | True | self running key | plaintext@456 | 5.18 | +30.5 | 9 | THOEWUHTSYHXTHTHIINLNGPIARWTFMABEDFRNGSPTWREACFFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMALDWWA |
| LP2-23 | adv | add | False | phrase-3 | THE FOLLWING TWO | 5.17 | +138.4 | 27 | OPWAYCUIAYAPUTLUBGIATHOTNHEAOTHMDSPAEALHEARANMREDEWMSYALMHFCUDCJSWPJEPHEALDELRTFAMOUITM |
| LP2-55 | advline | add | True | phrase-3-rev | TO STUDY HERE ʳ | 5.17 | +5.2 | 0 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWURDSNGTWWSRWUNGECRTLISNONLTHYHNOTHHAERP |
| LP2-19 | adv | sub | True | affine position | 7·n+1 | 5.14 | +113.1 | 29 | HAWTFEEUATHEEANSNSWFUWIAIMBNWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-19 | adv | add | True | affine position | 22·n+28 | 5.14 | +113.1 | 29 | HAWTFEEUATHEEANSNSWFUWIAIMBNWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-19 | adv | sub | True | affine position | 7·n+8 | 4.95 | +118.2 | 28 | UBFNFEEUATHEEANSNSWFUWIAIMBNWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-19 | adv | add | True | affine position | 22·n+21 | 4.95 | +118.2 | 28 | UBFNFEEUATHEEANSNSWFUWIAIMBNWEDDLFRLUBEALTIWIAWEATHAOCTTISMHACBGPTHSGUOFLUARREAYUGDAWOAJ |
| LP2-15 | nulli | beaufort | False | phrase-4-rev | MY HEAD THOUGHT THE ʳ | 4.93 | +105.5 | -14 | EUAEEAWRIWOIATBCEBNSTTICLTHUOYYDUGRMODNRORDRCLFHNNAUUADEIEAATBNGERMLSMEEATHDTWGAIAOSAILR |
| LP2-03 | advline | sub | True | self running key | plaintext@1512 | 4.92 | +46.4 | 3 | AETHSGFTJUWAPEAPMSMWABTHTHEARBEENWFTHNUIDEEDOTHATHNYNLHTHBLTASWFHEAPWMIOMTYFGLBTHWPFAEWNXDEIA |
| LP2-42 | advline | add | False | vigenere-word | WISDOM | 4.91 | +76.3 | 19 | UAAPCFEXEAHRSNIASCCMTHTHRUITUGRTTMETEAXUAIDLAXWEESLNGGRAPUTHCIOOFGHDNYNDOLSEACNEBMEDITHMA |
| LP2-07 | advline | sub | False | self running key | plaintext@456 | 4.88 | +27.1 | 9 | THOEWUHTSYHXTHTHIINLNGPIRENGAEYMABEDFRNGSPTWREACFFNIATHEOENOMIAETHCRWGTHRSERAAMIIYIDFYNMALDWWA |
| LP2-27 | adv | beaufort | False | primes+1 | p[n+53]+1 | 4.84 | +134.2 | 29 | UPGLTHEEAHITHGTOFNSYSPIAPMOTEIANGSREOWIYSBEAPCSTHWOOTTHSIDIAYHOAPELEHEAOLRSALLTOTHODUGPIFHU |
| LP2-55 | adv | add | False | phrase-4 | THOUGHT FOR A MOMENT | 4.83 | +48.5 | 9 | DEALTSSLENETHAOEIAURORCRTHDLEEDYNGRGMTHLSDIPUOERISGEYSEPINAEEHRNGERNGTINHOCNAOIPREAE |
| LP2-17 | adv | sub | True | phrase-4-rev | MUST SHED OUR OWN ʳ | 4.82 | +136.5 | 30 | JAIMUNDMNUNMITHCBAPOHECIMOUCDLASIAEDFDEAODEMIFUCULNNIASINNOCFNYSFEAETHERNHOERNNGRUEAOETHH |
| LP2-01 | nulli | sub | True | phrase-3 | MEANT THE MASTER | 4.80 | +107.7 | -35 | CJIEAWYONSLYTHDSNMYREUESIAHREDWFFHASUOEDFTHEAIFATLUEALYMAERMREAIOEPTHNTAETHOEMUTHWNGUDTAYENWTEA |
| LP2-34 | advline | beaufort | True | vigenere-word-rev | ANSWEREDʳ | 4.79 | +37.8 | 7 | RUAIANGUCOHCNYMLDWTNGODWUEOEMHATFBXTDEASLOBEETEMFGDETTSNGDDNYCOWETHTIAESHYEADIFINORJMHFTH |
| LP2-14 | nulli | add | True | self running key | plaintext@450 | 4.78 | +105.6 | -19 | WBRPIESAWLUGEANMHTRGSUEONUITHNGDYBLNLTHUECGFHEUWAERROEHAEATHUSUUNBCIAENGNHSYIWETHSATIHICTXG |
| LP2-21 | advline | sub | True | self running key | plaintext@2018 | 4.77 | +42.0 | 8 | OWCCFBMDXFMLIOIMWSHRNGUIREAACIAIEAHTHEETHAHDHIUFSLTHTSTHEOIPNORORHSOAOHHAEUMYLRUOSHUXWAENPI |
| LP2-07 | nullf | sub | True | self running key | plaintext@666 | 4.77 | +134.6 | -25 | CUDWBGANGMTDMFATSRNAEAFEUIFYTHETIIBAAPNMCOEASRNNCRCHPNLNEOIAYEAYFTHAHPISAARALIRADCSDNTE |

Largest z over all 10,059,720 tests: 5.24. Cells meeting the pre-registered rule (z >= 6 and edge − base >= 20): 0.
Largest z per kind: adv 5.17; advline 5.18; nulli 5.24; nullf 4.77.

## Verdict

**No page decrypts under any word-edge or line-edge event kind.** Extra key advances at word or line starts and unencrypted null runes at word starts or ends, at the 42 % rate pnotisdev's word-length fit implies, combined with this repository's key families under the skip rule, all three sign conventions and both F variants, are excluded at the sensitivity the controls demonstrate. Not covered: nulls inside words, non-uniform null runes, more than one event per position, event rates far from 0.42, key streams outside these families, and pnotisdev's own 1,447-stream library.

