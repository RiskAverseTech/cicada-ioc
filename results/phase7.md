# Phase 7 sweep: book families and phrase keys under the skip-by-two rejection rule

22863 configurations per page (phase 3's 4716 book keystreams and phase 4's 2905 phrase/sentence keys, each under three sign conventions), 55 pages, 2 F variants: **2,514,930 tests**, decoder in rejection="two" mode. Chance maximum about 5.4.
Per page, variant and decoder mode the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.

## Planted controls (skip-by-two plants, decoded with the skip-by-two decoder and with the single-advance decoder)

| control | sign | family | key | F | z (skip-by-two) | rank | rec | z (single-advance) | rank | rec |
|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | sub | phrase-2 | A LONG | False | 10.8 | 1 | 1.000 | 6.3 | 1 | 0.679 |
| control-01 | add | phrase-4-rev | CAN BELONG AND BE ʳ | False | 11.6 | 1 | 1.000 | 7.4 | 1 | 0.554 |
| control-02 | beaufort | phrase-3 | NOTHING FROM THIS | False | 11.7 | 1 | 0.996 | 5.3 | 1 | 0.529 |
| control-03 | sub | primes+1 | p[n+91]+1 | False | 11.7 | 1 | 1.000 | -1.5 | 4264 | 0.062 |
| control-04 | add | vigenere-word | SO | False | 10.3 | 1 | 1.000 | 10.3 | 1 | 0.979 |
| control-05 | beaufort | primes | p[n+92] | False | 11.1 | 1 | 1.000 | 1.0 | 430 | 0.233 |
| control-06 | sub | sentence | WELCOME PILGRIM TO THE GREAT J | True | 13.7 | 1 | 1.000 | 0.9 | 1260 | 0.104 |
| control-07 | add | phrase-3-rev | INSTRUCTION COMMAND YOUR ʳ | True | 14.2 | 1 | 1.000 | 9.5 | 1 | 0.725 |
| control-08 | beaufort | phrase-2 | AND THUS | True | 13.2 | 1 | 0.983 | 8.9 | 1 | 0.708 |
| control-09 | sub | fibonacci | F[n+9] | True | 9.5 | 11 | 0.592 | 5.1 | 5 | 0.408 |
| control-10 | add | self running key | plaintext@2207 | True | 12.2 | 1 | 1.000 | 11.9 | 2 | 0.938 |
| control-11 | beaufort | affine position | 28·n+28 | True | 13.7 | 1 | 0.992 | 5.3 | 1 | 0.546 |
| control-12 | sub | phrase-4 | YOUR CERTAINTY AND YOUR | False | 12.1 | 1 | 0.996 | 5.1 | 2 | 0.454 |
| control-13 | add | phrase-2-rev | ATTACHED TO ʳ | False | 11.6 | 1 | 1.000 | 7.2 | 1 | 0.733 |
| control-14 | beaufort | sentence | THAT IS ONLY YOUR SPECIES NOT  | False | 10.9 | 1 | 0.983 | 1.9 | 222 | 0.117 |
| control-15 | sub | vigenere-word | XXXXXXXXXXX | False | 11.6 | 1 | 1.000 | 11.2 | 1 | 1.000 |
| control-16 | add | primes | p[n+47] | False | 11.9 | 1 | 0.996 | 0.3 | 1658 | 0.050 |
| control-17 | beaufort | square position | n²+2 | False | 11.2 | 1 | 0.963 | 4.0 | 1 | 0.458 |
| control-18 | sub | phrase-3 | THAT WE SHAPE | True | 13.0 | 1 | 0.996 | 6.9 | 1 | 0.579 |
| control-19 | add | sentence-rev | I AM HE STARTED BUT HE COULD N | True | 12.8 | 1 | 0.992 | 7.1 | 1 | 0.579 |
| control-20 | beaufort | phrase-4 | YOUR CERTAINTY AND YOUR | True | 14.9 | 1 | 0.971 | 2.8 | 137 | 0.225 |
| control-21 | sub | self running key | plaintext@999 | True | 12.5 | 2 | 0.979 | 5.2 | 8 | 0.412 |
| control-22 | add | affine position | 27·n+7 | True | 14.8 | 1 | 0.983 | -0.3 | 2031 | 0.071 |
| control-23 | beaufort | primes-1 (totient) | p[n+17]-1 | True | 13.4 | 1 | 1.000 | 2.2 | 139 | 0.300 |

Skip-by-two decoder recovers 22 of 24 at z ≥ 6 and rank 1 (z 9.5–14.9, rune recovery 0.59–1.00); the single-advance decoder used by every earlier phase and ledger scores the same plants at z -1.5–11.9 (rune recovery 0.05–1.00).

## Unsolved pages: top 20 configurations overall

| page | sign | F | family | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|
| LP2-35 | sub | True | self running key | plaintext@878 | 4.99 | 3 | IAUEDCFEAAFDMGANNGYMEPTEAYWHOUDTNGWFANGNGPNWFTHHEORMSNHDBMAULYOUEIGAFNGSHDIFOYTHTHOYCHLLTHNT |
| LP2-35 | sub | True | self running key | plaintext@874 | 4.83 | 7 | SPISCJMRHNGTHLHULGEOLTHTUAXAETSUUHFLNGNGPNWFTHHEORMSNHDBMAULYOUEIGAFNGSHDIFOYTHTHOYCHLLTHNT |
| LP2-55 | add | True | phrase-3-rev | TO STUDY HERE ʳ | 4.76 | -1 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWFEAIAHEAWOWEWUNGECRTLISNONLTHYHNOTHHAECAE |
| LP2-14 | sub | True | self running key | plaintext@2424 | 4.58 | 10 | GNFXIPDRTMONDPEAEORRNGWIADRHSHLWCIRALRDEGNTLLROFUFTHNGOOESIODMLEWLYMEORIEGLWMEAYFTNSRIARS |
| LP2-28 | sub | False | self running key | plaintext@25 | 4.44 | 30 | ITHGPOCEILXLOLDRIRSMNWJNFBMOIAAENGMYMPBYHAGYCTHJBIUTHDLPLDOCSXECEYNXEAETHGOLGCTLWFULHTCC |
| LP2-14 | beaufort | True | self running key | plaintext@2452 | 4.43 | 4 | EWFCIANGSUOIAOCTOBUNBTHEEESNGXOWBAEXSIEAWFUIAOELIUEMGOUTHEALTHEEIAMABDBMTRRFUATHGTHCYJFOXDWNH |
| LP2-14 | sub | True | self running key | plaintext@2423 | 4.42 | 11 | IAUIAXIPDRTMONDPEAEORRNGWIADRHSHLWCIRALRDEGNTLLROFUFTHNGOOESIODMLEWLYMEORIEGLWMEAYFTNSRIARS |
| LP2-19 | sub | True | self running key | plaintext@1541 | 4.37 | 15 | NTREFFETGXDCCIOEEETXWLREAHUNGEANCNGRYEASXYLCIAFWWRTFTEATNBYINGXOTJHWDIUEAFNAIAJNGSOYOEFDISUC |
| LP2-14 | beaufort | True | self running key | plaintext@2449 | 4.37 | 7 | BWNCIANGSUOIAOCTOBUNBTHEEESNGXOWBAEXSIEAWFUIAOELIUEMGOUTHEALTHEEIAMABDBMTRRFUATHGTHCYJFOXDWNH |
| LP2-09 | sub | True | phrase-4-rev | A BEING UNTO YOURSELF ʳ | 4.34 | 5 | YTWLWLTIARYSFBAIAEORAIYTOITOEPTHXGLPDNLEWFEABHGGUCPEAPSGMPTHMOEWPFDRXCFGREOHRDLBCMOTCDTHT |
| LP2-04 | add | True | phrase-4 | DUTY OF EVERY PILGRIM | 4.33 | 19 | XEAPIBIAELDXBMIFRNAOYCXCXMJSICTOCITHJUGWERXFFDMIAEOASPAJRMLIEJRSNPIWFMSTTHUGSUNLEMSUL |
| LP2-18 | beaufort | False | phrase-2 | HAVE ENOUGH | 4.31 | 10 | NFMGMEEAALUCWLMPEANMBEREGIMEYIANGFIOWXJGMONOGXEBHTUUUFCXNNHSTCTHTEOJTHAGAIATHOSMCBUUNLWIT |
| LP2-47 | sub | True | phrase-3 | AND THE STUDENTS | 4.25 | 3 | RUHSICSRFNGOPSMGLHPIEAEHERUFNGTSTHNGTAEYITHELNGNPSNGNTPNNGAEOBAUFEOMAFSEPFIFTIACFCANTHSYYYNDD |
| LP2-26 | beaufort | True | affine position | 19·n+2 | 4.21 | 9 | RETHTHBEAOWAFDIEDSEOWBBROGTHIEATHDSEEANSDYFONGEAEPNGYHIARCWROEAFEMTOSMAEPCAUPRFEAWNOMLLFOSUFIAE |
| LP2-00 | beaufort | True | affine position | 5·n+18 | 4.18 | 3 | OSIUOANGFNOTEIEXAIFFDEBFIADICOBSUHTHIAAPEMOTHIAJIABETHRIAWSSOCRMMSENOERDUOATREEEAJONOEALLEAR |
| LP2-29 | sub | True | self running key | plaintext@1511 | 4.18 | 13 | THEAYNIAFUHXELIAIAUHDHNRFWUPWUANEAICWTUSRERTHHIFTHPEADIANGCTHEHUSIYCHTPPWNEWFIBHTHYXEFANTHYRC |
| LP2-29 | sub | True | self running key | plaintext@1509 | 4.16 | 15 | YEAYNIAFUHXELIAIAUHDHNRFWUPWUANEAICWTUSRERTHHIFTHPEADIANGCTHEHUSIYCHTPPWNEWFIBHTHYXEFANTHYRC |
| LP2-26 | beaufort | False | affine position | 19·n+2 | 4.16 | 10 | RETHTHBEAOWAFDIEDSEOWBBROGTHIEATHDSEEANSDYFONGEAEPNGYHEAAEIAAPSLNIWDGITRAESNGRALMIAFDIJJYPAEJSIAE |
| LP2-14 | add | True | phrase-3-rev | WITHIN AND YOU ʳ | 4.15 | 2 | BXYYFEETWUPLTHEAATHOEOEAHMNFNGWEIOGUSNGEOCRNPYCMFURYESTGTWEOEATMCEAEIWFDNHSATIGTHIATAPCLBEHJ |
| LP2-01 | sub | True | sentence-rev | DO NOT EDIT OR CHANGE THIS BOOK ʳ | 4.15 | 1 | MWTIADCLSNEOWSDMHSIAYWIWTHIEAIEWUCICENGPGFGTHTYMUNBTCTHLOGWTXAOOEMEAISBNDPTHDSHEOWSNISRDIAP |

Largest z over all 2,514,930 tests: 4.99 (LP2-35, sign sub, self running key 'plaintext@878').

## Verdict

**No page decrypts under the skip-by-two rule.** Every family of phases 3 and 4, with a rejection that discards two key symbols, under all three sign conventions and both F variants, is excluded at the sensitivity the controls demonstrate. This says nothing about keys outside these families or about other rejection widths.

