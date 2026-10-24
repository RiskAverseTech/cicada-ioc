# Phase 4 sweep: phrase and sentence keys from the book, all key signs, under the skip-on-repeat rule

2905 distinct phrase/sentence keys (2-, 3- and 4-word contiguous phrases and whole lines of the solved text, forwards and reversed) under three sign conventions, plus phase 3's 4716 keystreams under the two sign conventions phase 3 did not run: 18147 configurations per page, 55 pages, 2 F-rule variants: **1,996,170 tests**.
Per page, variant and decoder mode, the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection. Chance maximum for this many tests: about 5.4.

## Planted controls

| control | sign | family | key | F rule | z of true key | rank in its set | runes recovered |
|---|---|---|---|---|---|---|---|
| control-00 | sub | phrase-2 | FOR ALL | False | 11.9 | 1 | 0.979 |
| control-01 | sub | phrase-3 | SO THAT WE | False | 11.0 | 1 | 0.996 |
| control-02 | sub | phrase-4 | YOU WILL ARRIVE OUTSIDE | False | 11.5 | 1 | 0.938 |
| control-03 | sub | phrase-3-rev | WHAT WE HAVE ʳ | True | 13.7 | 1 | 1.000 |
| control-04 | sub | phrase-4-rev | MASTER REPLIED THEN YOU ʳ | True | 13.8 | 1 | 1.000 |
| control-05 | sub | sentence-rev | IT IS THROUGH THIS PILGRIMAGE THAT WE SHAPE OURSELVES AND OU ʳ | True | 12.7 | 1 | 0.988 |
| control-06 | add | sentence | BE PREPARED TO DESTROY ALL THAT YOU OWN | False | 11.7 | 1 | 1.000 |
| control-07 | add | phrase-2 | THE MESSAGE | False | 11.7 | 1 | 1.000 |
| control-08 | add | phrase-3 | THROUGH THIS PILGRIMAGE | False | 12.1 | 1 | 1.000 |
| control-09 | add | phrase-2-rev | AND WE ʳ | True | 13.0 | 1 | 0.983 |
| control-10 | add | phrase-3-rev | WITHIN AND EMERGE ʳ | True | 13.4 | 1 | 0.946 |
| control-11 | add | phrase-4-rev | ALL THAT YOU OWN ʳ | True | 12.9 | 1 | 1.000 |
| control-12 | beaufort | phrase-4 | THE STUDENTS WERE ENLIGHTENED | False | 11.4 | 1 | 1.000 |
| control-13 | beaufort | sentence | FIND THE DIVINITY WITHIN AND EMERGE | False | 12.0 | 1 | 1.000 |
| control-14 | beaufort | phrase-2 | FOLLOW REASON | False | 12.1 | 1 | 1.000 |
| control-15 | beaufort | sentence-rev | THAT IS ONLY YOUR SPECIES NOT WHO YOU ARE ʳ | True | 16.3 | 1 | 0.996 |
| control-16 | beaufort | phrase-2-rev | WITHIN THE ʳ | True | 14.9 | 1 | 0.988 |
| control-17 | beaufort | phrase-3-rev | TO STUDY HERE ʳ | True | 12.6 | 1 | 0.921 |
| control-18 | add | shift | s=15 | False | 11.6 | 1 | 1.000 |
| control-19 | add | vigenere-word | LIUES | False | 11.5 | 1 | 0.992 |
| control-20 | add | vigenere-word | INHABITNG | True | 14.2 | 1 | 1.000 |
| control-21 | add | affine position | 18·n+18 | True | 13.5 | 1 | 1.000 |
| control-22 | beaufort | affine position | 27·n+6 | False | 10.9 | 1 | 0.992 |
| control-23 | beaufort | lucas | L[n+10] | False | 10.6 | 2 | 0.992 |
| control-24 | beaufort | lucas | L[n+0] | True | 15.1 | 2 | 0.988 |
| control-25 | beaufort | primes+1 | p[n+55]+1 | True | 12.2 | 1 | 0.925 |

Controls recovered at z ≥ 6 and rank 1: 24 of 26; all at z ≥ 6: 26 of 26.

## Unsolved pages: top 20 configurations overall

| page | sign | F rule | family | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|
| LP2-09 | sub | True | phrase-2 | CERTAINTY AND | 5.10 | 2 | NGENGMTJIHIESWRADODPPDBOIGAEASMPDWEECRURRPWRTHGEWBHJMJIPEYREANWWIRIAPCTPJSIBDSOABPPTHIM |
| LP2-55 | add | True | phrase-3-rev | TO STUDY HERE ʳ | 4.84 | 0 | IFHERNEUCEEAAIALRFAEENGTILGOFOETAGFDAWUDRTHAWURDSNGUOEWSRWUNGECRTLISNONLTHYHNOTHHAERP |
| LP2-11 | add | True | self running key | plaintext@1132 | 4.59 | -5 | CDHSIERAIGIADMIATIATHWFTHAFGMITMDFHIDBTTHUWNGSORETJNGIDNGOHOEYGOADEEBWLECMNNGNDIANRLXGMFUFHC |
| LP2-04 | sub | True | phrase-3-rev | THE PROFESSOR REPLIED ʳ | 4.52 | 2 | YNTOEUNGOSTHACBFNAUUAUINBIAUEIESRDEAOBHEOYOLDIAFRYTHAEREAGWBYUWBFOIAPPMLTHWFLMWNGHHUNWHEALLLE |
| LP2-35 | beaufort | True | affine position | 24·n+9 | 4.40 | 4 | BBDEAMTTHIAAERHJYGTLERSAEBWNGEAFIWFMIAURFHIRIFNAEATHANTHMLJOLRTATEOODNGPIIFNGSNHNLYTTHTTHEIRSBW |
| LP2-39 | sub | True | phrase-3 | YOU WHO WISHES | 4.40 | 7 | ERUTHWWUWEALOTHRBNGDUIAAOERTLHEANAENGHTGMULNHGLTHUJCFIANAUNGEAICTHHNGPDWENLMSIAUOTHJARSAUCEOHOIOL |
| LP2-13 | beaufort | False | self running key | plaintext@2874 | 4.34 | 8 | IFIRWMUOCPEOEPNAOEASDDDFRMOBENHGEDTHSSSETHYUSNGPUETHTTEYSDFLWAWEORYCAHOEJNGWJASHIAFCLHPAWM |
| LP2-27 | add | True | phrase-4-rev | ALL STRUGGLE AND SUFFERING ʳ | 4.29 | -4 | JBSLSRECONNETLAWUAERRFIMIAHTHOFBLAEGNTTHFXFFBAISYNGAYMFOMEYHFECJEIEOFRTHAIACNGEBOPMOEPDANYE |
| LP2-01 | add | True | phrase-4 | HAVE A VOICE IN | 4.26 | -1 | OCLRIEONMBAEAOEDPLOEERECSPIOECGIAACFWMEAYTHEFSREDCGOAYFSNGOYYRRJWIARUEXLIAJFEDNGYNOCMDHBYRL |
| LP2-05 | sub | True | phrase-2 | THE WAY | 4.25 | 2 | THWWPXDUPCOOTSAUTHIANGARUGNNGEBDEROFWEABNIUPFAWTHUICCYSMFNGEAWEDNMMASCEAIAAESDTJCUIAAOFMCY |
| LP2-13 | beaufort | False | self running key | plaintext@2875 | 4.25 | 7 | AEHSTHEUUOCPEOEPNAOEASDDDFRMOBENHGEDTHSSSETHYUSNGPUETHTTEYSDFLWAWEORYCAHOEJNGWJASHIAFCLHPAWM |
| LP2-31 | sub | True | phrase-4 | VOICE IN MY HEAD | 4.23 | 0 | UTHWTIAREREMRFMBLCCTHFEAMAAENMJIASETHIACSTTHLLRHSLPGYDMRNGEBPRASWTTBOBEXIAIAMFYEHEOHNGONNJOEAUN |
| LP2-29 | sub | True | phrase-2-rev | THE STUDENT ʳ | 4.22 | -1 | SXBWSRUHEACYRUSATHDNGSEAIAUXEGWWUOTHMNLEHUHSAPCYSYRUNGWLRAIAYTHNGIADMRHSREPTHSRNCGEOIARJPTHIRY |
| LP2-42 | sub | True | phrase-3 | TOWARD THE END | 4.20 | 3 | WJTHAIATNSACWNEAICWHIAGONPLDPBYOWSGRSLBTHNGTWSSOSNGNIRTWOBTHWBLIEATLEUIAXFMDFTHAAWPTHSYTEYG |
| LP2-44 | beaufort | True | vigenere-word-rev | HOLYʳ | 4.20 | -2 | IAMTHADUEARDFMEIBMFEHICIALBEARTTFFEIIAROEASLAOEYRJREAEAEEBBFXROBOEHUPTISHTFNGINDPEOUYASTHPEBI |
| LP2-27 | sub | True | phrase-3-rev | THERE EXISTS A ʳ | 4.18 | 3 | AIAICCEGWRTHTBAOCIUTACMRGEONGSWSCOEYEATSIFYIOBSSTHOOELIREOWLIAUFAERMULSJFWSUETHFUBTHMISABTAEY |
| LP2-35 | beaufort | True | affine position | 24·n+14 | 4.16 | 5 | OEBDEAMTTHIAAERHJYGTLERSAEBWNGEAFIWFMIAURFHIRIFNAEATHANTHMLJOLRTATEOODNGPIIFNGSNHNLYTTHTTHEIRSBW |
| LP2-18 | beaufort | False | self running key | plaintext@168 | 4.12 | 7 | CLELCRTXAHEOWACPPPWTHSEAPDEAMFEAFCISEYTHYWGECPRDTSUIEARRIDGJIAXIWGXYPIRUHGYOEEOBIALTHNGUANHUW |
| LP2-05 | sub | True | phrase-3-rev | WHAT YOU KNOW ʳ | 4.11 | 4 | YOECOIOEOERFIPTOEDFXMNGTHXUDOXTHDSEMYFGTWHMONEATIATHMCTNEOWLSTHWNEOCNJWNGONTCBCAEOBNFWANGFCFTHFS |
| LP2-19 | sub | True | sentence | WHEN ASKED BY A STUDENT TO EXPLAIN WHAT THAT MEANT THE MASTE | 4.09 | 1 | THARFXIANGGPEXHLIAEAATTHGHEAHTFPRSGEMHBTHTTHDJADHDLSRALOEDUHIFNGTHYNTHEAPTCMOFYAWDUFBMDTAESNN |

Largest z over all 1,996,170 tests: 5.10. Largest z among phrase/sentence keys: 5.10 (LP2-09, sub, phrase-2 'CERTAINTY AND').

## Verdict

**No page decrypts.** Every 2-, 3- and 4-word phrase and every full line of the solved text, forwards and reversed, as a Vigenère key under the skip-on-repeat rule, with the key added, subtracted or used Beaufort-style, with and without the F rule, is excluded at the sensitivity the controls demonstrate; so are phase 3's families under the two sign conventions phase 3 had not run. This says nothing about keys from outside the book's own text.

