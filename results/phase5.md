# Phase 5 sweep: phases 3 and 4 rerun under Latin and Old English plaintext models

22863 configurations per page (phase 3's 4716 book keystreams and phase 4's 2905 phrase/sentence keys, each under three sign conventions), 55 pages, 2 F variants, 2 registers: **5,029,860 tests**. Chance maximum about 5.6.
Per page, register, variant and decoder mode the null is 2,000 random keystreams through the same decoder with the same model. Positive rule (pre-registered): z ≥ 6 over that null and readable in that language on inspection.

## Planted controls (decoded with the register's own model, and with the English model)

| control | register | sign | family | key | F | z own | rank own | rec own | z English | rank English | rec English |
|---|---|---|---|---|---|---|---|---|---|---|---|
| la-control-00 | la | sub | phrase-2 | HE SAID | False | 11.5 | 1 | 1.000 | 10.8 | 1 | 1.000 |
| la-control-01 | la | add | sentence-rev | THAT IS WHAT YOU DO NOT WHO YO | False | 11.0 | 1 | 1.000 | 10.3 | 1 | 1.000 |
| la-control-02 | la | beaufort | sentence | FINALLY HE ANSWERED I AM A HUM | False | 11.8 | 1 | 1.000 | 10.0 | 1 | 1.000 |
| la-control-03 | la | sub | vigenere-word-rev | FOLLWNGʳ | False | 11.8 | 1 | 1.000 | 11.1 | 1 | 1.000 |
| la-control-04 | la | add | self running key | plaintext@2510 | False | 11.9 | 2 | 1.000 | 10.8 | 2 | 1.000 |
| la-control-05 | la | beaufort | lucas | L[n+9] | False | 12.3 | 1 | 1.000 | 11.2 | 1 | 1.000 |
| la-control-06 | la | sub | phrase-3 | HE STARTED BUT | True | 12.9 | 1 | 0.996 | 11.3 | 1 | 0.996 |
| la-control-07 | la | add | phrase-2-rev | AFTER A ʳ | True | 13.9 | 1 | 1.000 | 11.9 | 1 | 0.983 |
| la-control-08 | la | beaufort | phrase-2 | A STUDENT | True | 15.0 | 1 | 0.971 | 12.9 | 1 | 0.954 |
| la-control-09 | la | sub | square position | n²+4 | True | 14.0 | 1 | 0.992 | 12.6 | 1 | 0.992 |
| la-control-10 | la | add | primes+1 | p[n+58]+1 | True | 14.0 | 1 | 1.000 | 12.1 | 1 | 1.000 |
| la-control-11 | la | beaufort | affine position | 11·n+28 | True | 14.0 | 1 | 1.000 | 11.8 | 1 | 1.000 |
| ang-control-00 | ang | sub | phrase-2 | BY LUCK | False | 9.4 | 1 | 1.000 | 8.4 | 1 | 1.000 |
| ang-control-01 | ang | add | sentence-rev | IT IS THE BEHAVIORS OF CONSUMP | False | 8.7 | 1 | 0.975 | 9.0 | 1 | 0.963 |
| ang-control-02 | ang | beaufort | sentence | WHO ARE YOU WHO WISHES TO STUD | False | 8.1 | 1 | 1.000 | 7.0 | 1 | 0.912 |
| ang-control-03 | ang | sub | vigenere-word-rev | WORTHʳ | False | 9.6 | 1 | 1.000 | 8.0 | 1 | 1.000 |
| ang-control-04 | ang | add | self running key | plaintext@2742 | False | 8.7 | 1 | 1.000 | 8.9 | 1 | 1.000 |
| ang-control-05 | ang | beaufort | lucas | L[n+2] | False | 8.7 | 1 | 1.000 | 6.9 | 1 | 1.000 |
| ang-control-06 | ang | sub | phrase-3 | NOT WHO YOU | True | 10.5 | 1 | 1.000 | 8.4 | 1 | 0.933 |
| ang-control-07 | ang | add | phrase-2-rev | PRIMALITY AND ʳ | True | 11.0 | 1 | 0.971 | 9.3 | 1 | 0.971 |
| ang-control-08 | ang | beaufort | phrase-2 | FOR A | True | 11.4 | 1 | 0.971 | 10.6 | 1 | 0.988 |
| ang-control-09 | ang | sub | square position | n²+18 | True | 9.8 | 1 | 0.967 | 8.6 | 1 | 0.988 |
| ang-control-10 | ang | add | primes+1 | p[n+60]+1 | True | 9.2 | 3 | 0.967 | 7.9 | 3 | 0.929 |
| ang-control-11 | ang | beaufort | affine position | 13·n+12 | True | 10.0 | 1 | 0.933 | 8.2 | 1 | 0.863 |

la: own model recovers 11 of 12 at z ≥ 6 and rank 1 (z 11.0–15.0); the English model would have recovered 11 of 12 (z 10.0–12.9).

ang: own model recovers 11 of 12 at z ≥ 6 and rank 1 (z 8.1–11.4); the English model would have recovered 11 of 12 (z 6.9–10.6).

## Unsolved pages: top 20 configurations overall

| register | page | sign | F | family | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|---|
| la | LP2-04 | sub | True | phrase-3 | THE INSTAR TUNNELING | 4.88 | 0 | ENTRIASOORUJBNBAETRRBBORAEPCOIIAIIAEEOGLITCFCTHFRIXYURSNGRGINEXEOMPCGGAEUXMINGCIOCNEISEOUANG |
| la | LP2-00 | add | True | phrase-2-rev | HE WENT ʳ | 4.82 | -2 | THBWIAIAXFASAEIPELAOFFUMELTWSRRRFUEHIIAOAEEBGTTNGREUELOHGOAEONGCWFOPEDFAEELMFPUOCSTRIAING |
| la | LP2-05 | sub | True | self running key | plaintext@179 | 4.59 | 3 | NLIMBEUFFFERNGOEOFEOOFPEOBATHPBHSPBSAESWOHIARUPTIADLBMEMOEEROPELURFTEOICBRRADTHFHSJNLFIFD |
| la | LP2-11 | sub | True | phrase-3-rev | UNREASONABLE THINGS EACH ʳ | 4.56 | 1 | MIGOSSLFRWFWPEDAEAICHDFIAEABEDAEAEUGOECXTBCEAPSWFIWDSRCIWCWDNLCBTIAUXFDIARIAAELTOEAYGEIAMASAEIA |
| ang | LP2-24 | beaufort | False | self running key | plaintext@2420 | 4.53 | 2 | AMTHFEAGNCTHHMLBROSIAAEWAMIUNFGPNTTSTHREOBEFTUNSEFWDDWCYTEOENNWPOWEEMPMIMCNARJTFEAEAYEAEFFO |
| ang | LP2-27 | sub | True | self running key | plaintext@1342 | 4.48 | -2 | GNDLYBNNGRTHCNGFUYIAEIHGEALAEFWSHFCAESWNTHUFAESYINIAEUFAEISRPEANGEAAEOAEREWLGFFWSEOGNCUGNORFIYSRC |
| la | LP2-11 | sub | True | affine position | 26·n+22 | 4.40 | -4 | CAEECYICMDWBNGPCEIAFSIISNTHTAUGEGHEAWIATHXSFPWOERFEONGSUBNXLBXFHEORTBAENCTBNMFBDIOLNCRUGWCR |
| la | LP2-11 | add | True | affine position | 3·n+7 | 4.40 | -4 | CAEECYICMDWBNGPCEIAFSIISNTHTAUGEGHEAWIATHXSFPWOERFEONGSUBNXLBXFHEORTBAENCTBNMFBDIOLNCRUGWCR |
| ang | LP2-09 | sub | True | self running key | plaintext@637 | 4.34 | -3 | TUWYGONNEAIRRNIDAIAOLSDBEFABNGEASFOEERELGRFUNAAGYDWWXEDWAOPTEIAISWEAFFWRLTHMOXUMILRPNGHU |
| ang | LP2-27 | sub | True | self running key | plaintext@1343 | 4.34 | -3 | SIYTHFFLNGMWIATHNGAEIAEAEIHGEALAEFWSHFCAESWNTHUFAESYINIAEUFAEISRPEANGEAAEOAEREWLGFFWSEOGNCUGNORFIYSRC |
| la | LP2-38 | sub | True | phrase-4-rev | HAVE US LOSE OUR ʳ | 4.28 | 7 | YATHDMDWISFRCWRXUEOTWAGECAGLYDGOMSIAGAEFMBCEOTHMEDTCPSTABNGDXMNEAOEWPWNESMEAEOEHRFATCBRGTMG |
| la | LP2-19 | sub | True | self running key | plaintext@1806 | 4.27 | 6 | WXELMBUFIAEALXRIAGCYXATDRCLTDSOESGRODUXIAXMEONPEAUSEOUIARDWDCMXLNINOCIALLBCTNAEOMWLUIADROENTM |
| ang | LP2-32 | add | True | self running key | plaintext@848 | 4.27 | -1 | AUTEOLEHEFEOAOTEONITHEOEAOOULTHRUIMYNDEENYTAEANECSFNHGTGNTHAEOAEEOBESPNCJBIARAEWIMUTETHNLOOAEERN |
| la | LP2-46 | add | True | phrase-4 | YOU WHO WISHES TO | 4.26 | 0 | CMSOEXHRSGXUYIETLNGMTUFWLNNPFGLAWTLNAEUFCXGCBAATEOPNTTHCAEEHNGXIALDONADPUPFHLLBEONNMMEAEOO |
| la | LP2-13 | sub | True | self running key | plaintext@2967 | 4.26 | 2 | YWLBBTPRUAECROFRMBEOIAGSLTHDMAIABIAPIATRPXPAAMIAAEMCIINGTBDEFNNFEMDOXAEFJADONWLWXAEIASOEPTHOEGEA |
| ang | LP2-09 | sub | True | self running key | plaintext@636 | 4.25 | -2 | GYMBTHTUNEAIRRNIDAIAOLSDBEFABNGEASFOEERELGRFUNAAGYDWWXEDWAOPTEIAISWEAFFWRLTHMOXUMILRPNGHU |
| la | LP2-29 | sub | True | phrase-4-rev | OF THOUGHT THE PROFESSOR ʳ | 4.22 | -3 | IALLSIALPOEBORGTIIEAAAECLXGTEORNGCINGMNEOMCRHBDCOEFCFEAPMLNCRGEHCBPEAWUMATPRICEOLAPNFEOIAAETNCL |
| la | LP2-36 | beaufort | True | phrase-3-rev | FUNCTION IS SACRED ʳ | 4.20 | 5 | YNOIAOWNPCAGXFTLLCFCNEAEOUUDCLXFCIAOEMWNJCONCTOEOIAGHITLIOEAEBAISEYJIOEHIMEGPUTCMOSCXOEEN |
| la | LP2-38 | sub | True | phrase-2 | VOICE IN | 4.20 | 5 | FOEAWTTEAPHFJCEAXULYNGCEOELSAEILSHEAFOIAPIARLLORCDNGEICOXNLRTDRNNOWROETMGBEUTIATMLTAEOWRNOO |
| la | LP2-05 | sub | True | self running key | plaintext@181 | 4.17 | 1 | FWLUOELTUFTXCMTFSYNHGTRLTWROEFNTHOEPOLPWMMPSIWTHDENGDOOEEROPELURFTEOICBRRADTHFHSJNLFIFD |

Largest z over all 5,029,860 tests: 4.88 (la, LP2-04, phrase-3 'THE INSTAR TUNNELING').
Largest z per register: la 4.88; ang 4.53.

## Verdict

**No page decrypts under either register.** Every family of phases 3 and 4, under the skip-on-repeat rule, all three sign conventions and both F variants, is excluded for a Latin plaintext and for an Old English plaintext at the sensitivity the controls demonstrate. This says nothing about other languages or about keys from outside these families.

