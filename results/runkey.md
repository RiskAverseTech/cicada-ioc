# External running-key lane: exact decoding at every offset

8 texts exact (every offset, both directions, V1 and V2) and 4 long texts at sentence starts (V1); 3 signs x 2 F; 153,149,370 tests over 55 pages; 2000 random-keystream nulls per page, F and mode; decoder max_skip 4. Rule: z_uni >= 7 and z_big >= 3 and readable (module docstring). Chance maximum of z over this many tests about 6.1.

## Controls (soft rule 0.81, corpus text at a random offset, signs/F/direction random)

| text | variant | n | sign | F | reversed | planted offset | top offset | z_uni | z_big | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| liber_al | runes | 262 | add | False | True | 3892 | 3892 | 12.1 | 23.5 | yes |
| liber_al | runes_nodigraph | 137 | beaufort | True | True | 2807 | 2807 | 8.3 | 16.2 | yes |
| blake_mhh | runes | 92 | add | False | True | 18130 | 18130 | 6.4 | 13.8 | no |
| blake_mhh | runes_nodigraph | 200 | beaufort | False | False | 3734 | 3734 | 10.0 | 18.7 | yes |
| rune_poem | runes | 277 | sub | False | False | 6989 | 6989 | 12.4 | 22.2 | yes |
| rune_poem | runes_nodigraph | 159 | beaufort | True | True | 13286 | 13286 | 10.7 | 16.2 | yes |
| self_reliance | runes | 262 | sub | True | False | 23494 | 23494 | 14.4 | 23.9 | yes |
| lady_fountain_guest | runes | 137 | add | False | False | 19320 | 19321 | 8.1 | 15.9 | yes |
| lady_fountain_bulfinch | runes | 92 | add | False | False | 28353 | 28352 | 6.6 | 13.7 | no |
| cypherpunk_manifesto | runes | 200 | sub | True | True | 3585 | 3585 | 13.8 | 22.9 | yes |
| cypherpunk_manifesto | runes_nodigraph | 277 | beaufort | False | True | 230 | 230 | 12.8 | 25.4 | yes |
| agrippa_gibson | runes | 159 | add | False | True | 1515 | 1515 | 9.0 | 18.8 | yes |
| agrippa_gibson | runes_nodigraph | 262 | add | True | True | 5593 | 5593 | 13.5 | 21.6 | yes |
| emerson_essays1 | runes | 137 | sub | True | False | 46244 | 46244 | 9.4 | 16.7 | yes |
| mabinogion_guest | runes | 92 | sub | True | False | 259650 | 259650 | 7.5 | 13.6 | yes |
| kybalion | runes | 200 | add | True | False | 131845 | 131845 | 11.1 | 18.8 | yes |
| king_in_yellow | runes | 277 | beaufort | False | True | 204057 | 204057 | 11.9 | 24.2 | yes |

Controls passing: 15 of 17.

## Best cell per page (over every text, direction, variant, sign and F)

| page | runes | z_uni | z_big | text | variant | reversed | sign | F | offset | transliteration (first 60) |
|---|---|---|---|---|---|---|---|---|---|---|
| LP2-00 | 262 | 5.13 | 2.4 | liber_al | V2 | False | beaufort | True | 13865 | AIAMIAORLSAWFTHXURIIAERBUSSJFOWASLHFHSNIAREAGTHNGNICWARPWEAA |
| LP2-01 | 266 | 4.90 | 2.2 | lady_fountain_guest | V1 | True | add | True | 37800 | EEADRTUTHEAROEEXEPCOTHTHNTHDHPWEAWMMERTSTHEAEALWFPAGWGFAHIAE |
| LP2-02 | 201 | 4.44 | 1.3 | self_reliance | V1 | False | beaufort | True | 1899 | IMEATEULEAYLCCLBWITXOGGRIARNGJTHIYLDIAGNCOTWEEASOYYEOIFXXLNR |
| LP2-03 | 217 | 5.46 | 3.2 | lady_fountain_guest | V1 | True | sub | True | 19307 | UWNHBTEPNBEOMFIAPTHAOYMTHWIASHOMOFDNUERASBGSUDALLNGAHNWTIBRT |
| LP2-04 | 261 | 5.29 | 1.1 | agrippa_gibson | V1 | True | sub | True | 6948 | MIHDRDWTSNOSCROJJHRXOEABIIAIOXODHNRGERNGUGIASRYEOATMJDIYHUAE |
| LP2-05 | 263 | 5.44 | 0.1 | liber_al | V2 | False | sub | True | 5339 | YUIRUOESIFEPYAOEARLGOTPOPCWLTFJBYFICAOEREAAWRLWNOHAOGESCOWRR |
| LP2-06 | 196 | 4.78 | 0.6 | kybalion | V1 | False | sub | True | 141610 | RMEAPHDLTSOEFAADEAODEERYIBIFTNGSIUXOHETRDNPRNGELNYDAWCABYITA |
| LP2-07 | 208 | 4.85 | 2.0 | king_in_yellow | V1 | True | sub | True | 273834 | MMIHEAGTBTHNEAETCLGEEAEALIAATFYRHTLNGSYDSNCIOBEAYRSEARAOEYEA |
| LP2-08 | 255 | 4.64 | 0.5 | lady_fountain_guest | V1 | True | beaufort | True | 18590 | NIETEAERMSINGSGHHTIDRHWOHMJWAMSOCLFNFEAOGLNSUYEASUTOEPXIAUMH |
| LP2-09 | 268 | 4.69 | 1.4 | lady_fountain_guest | V1 | True | beaufort | True | 25375 | EFWODBEAGNGAEABFCSPFDUITCESOWXIHLAEYULBUUATTHPPOFNGGETBWTMTH |
| LP2-10 | 263 | 4.59 | 0.4 | rune_poem | V1 | False | beaufort | True | 8493 | PNDLEPOPWTHCAAOCETHPNNEOYTUGUDOUMSHPEWTHTHBFLANGIOGONGGDSATC |
| LP2-11 | 273 | 4.84 | 4.1 | mabinogion_guest | V1 | True | beaufort | False | 354128 | LTHRFATHUBBURLMBJANGFLJAEAYTHINNYMPTHDTBIAECEREAEATHXASFUXAD |
| LP2-12 | 261 | 4.92 | 2.2 | self_reliance | V1 | False | add | True | 14809 | SIAADNNNGNGLNOINGTHIANTLRBWIARNPDHDOETDDODJSSEAIAUTFPEDXUAIO |
| LP2-13 | 272 | 4.73 | 2.7 | rune_poem | V2 | False | add | True | 10874 | SLFCDTHREFGTHDPEGWTHYRORLWTWEEANGFTHAMNGDFDAYBBIYTHWGDLOENAI |
| LP2-14 | 137 | 4.55 | 0.5 | blake_mhh | V1 | False | add | True | 17039 | EXSNGUONTSWANTHOINOEHFIAOEOOFEEUPDNECCHTHNGEAIAIAOEWBLACOTHW |
| LP2-15 | 159 | 5.26 | 1.3 | king_in_yellow | V1 | True | beaufort | True | 110470 | AEMENGRGSLFMCNYSNGDWFEMNTTXWNFADDNRTHRNWILEPTHJUSIARLRDPACBS |
| LP2-16 | 267 | 4.69 | 1.2 | lady_fountain_guest | V1 | False | beaufort | False | 33051 | NGSWOEEAPRLMTMTHRPURAGMHRHEGCHSHFOENGTNSMNGTNGJIDDTHDIAIADNR |
| LP2-17 | 273 | 4.51 | 1.7 | blake_mhh | V1 | False | sub | True | 12301 | DNGYMOHEARRWMLAUEAANGEETIAECYRUHDTOEDFDMABFELGEHFOISCHEIINSE |
| LP2-18 | 260 | 4.57 | 2.7 | lady_fountain_guest | V1 | True | sub | True | 30781 | FLBBLRDSCLDTUEFANGXUSUIANMHLBUBLDONGDENAXPTHSADPTTHUYIAMDWCD |
| LP2-19 | 271 | 4.53 | 0.6 | liber_al | V1 | True | sub | True | 15322 | EHRMYIADMGWNLSCTHCSTHDAXEADEUGRAIGYTNAOGTDEEAHWFHIMTHCTSAHCL |
| LP2-20 | 269 | 4.59 | 1.5 | rune_poem | V1 | False | add | False | 3958 | IIARCAISXDLDTHYPEAOIGHRNGDSBGDAXTHWUDOACATYLEWAISBOGYLTUARTH |
| LP2-21 | 273 | 4.85 | 3.3 | self_reliance | V1 | True | sub | True | 23408 | OTETTHIATWOTHMYNGTAMPRTNNPEOCOEEENGLHTHACOBAECNNMOFSEOJIAORU |
| LP2-22 | 131 | 4.27 | 1.8 | rune_poem | V2 | False | beaufort | True | 17845 | TEADIYERPUEATSWNTSEBNGCRNITNJGFWGASRTRSNGCYFHEAPTHYOUTRYEFUW |
| LP2-23 | 213 | 5.10 | 2.5 | emerson_essays1 | V1 | False | sub | True | 31725 | SSRCRBCOISNGRSIASBITIANGTRGADBTHTHNGHBHWAENGAOHYUSAOFECCTHES |
| LP2-24 | 270 | 4.91 | 1.6 | blake_mhh | V2 | False | beaufort | True | 10124 | AUFGMOESRSAERILTBREOYTOIJUNGTHSIBRSBTXRFFSIAIBRATHBPEOMRXUIY |
| LP2-25 | 273 | 4.62 | 1.6 | rune_poem | V1 | True | add | False | 4589 | SIAHWBAEFSNGLOLYSTTEAMUMGFLGIFIHBDRWATHBRMOUUFAMEGYAOETEBTNI |
| LP2-26 | 265 | 4.79 | 0.8 | blake_mhh | V1 | False | beaufort | True | 3654 | OSAESDGWRAELESAAILITHEAEEWHWEFMIYNFOTLOWPADOOARNGAFNGIAINDGT |
| LP2-27 | 234 | 5.27 | 3.0 | lady_fountain_guest | V1 | True | sub | True | 973 | BIESTNGMRAEIWPUERLOOTHXYGEMEAUMFTHLBTHWTFYCEDEEBOEAIAONRTHDG |
| LP2-28 | 269 | 4.93 | 2.1 | blake_mhh | V1 | True | sub | True | 18431 | AETYTHURRBEDNTSYACFAOECUTPDTEFWNGDIBEEBATTFIOCYOLIAFORBPMSYX |
| LP2-29 | 277 | 4.51 | 2.1 | blake_mhh | V2 | False | sub | True | 8529 | WHMPIACSNMOUGHPADHXMBTHCDLENXPTPWFSUESYGNSFTAERAENNGEALEODCL |
| LP2-30 | 263 | 4.47 | 1.8 | lady_fountain_bulfinch | V1 | True | beaufort | True | 17459 | ODWNGYACTGRCNGIDTRTHJIAEHSGIUEAAEAENEOEONGEBYAESRUCRSIAIAXTG |
| LP2-31 | 269 | 5.31 | 0.4 | self_reliance | V1 | False | sub | True | 37403 | PAHGSIOEOIAOFOPCCUSGNDOEGAOJHCTCXIHCNLTTHNDXNGGRHHETHTHEARGW |
| LP2-32 | 121 | 4.55 | 0.8 | mabinogion_guest | V1 | False | beaufort | True | 105221 | PTGDMTCIIAPTHIYUEADDFDLUBEAIUGLUEFECUTUWMXTAHRFSOLCYADEATAAU |
| LP2-33 | 214 | 4.42 | 1.8 | self_reliance | V1 | True | beaufort | False | 12522 | UOEAPECDPSBGLTDYYCFTHURELMXWRRBMHUEAONTYXUNEOEAOELEYHDROEHTI |
| LP2-34 | 261 | 4.95 | 2.9 | blake_mhh | V1 | True | beaufort | False | 7048 | CMNFOEUAMRMRWDIAFSEAHAUCDUIATBLTAREIAASTHLTHYEEPTHARSAEOTTHS |
| LP2-35 | 271 | 5.06 | 1.6 | blake_mhh | V1 | True | sub | True | 5828 | UNGJSETHTTIAHEIFGNGEAALJAEASWTERTHNTNGFLDYTHICFEATTHCNGREEHE |
| LP2-36 | 238 | 4.73 | 2.0 | lady_fountain_guest | V1 | True | sub | True | 20812 | THIALOEONGBFURDMUTHIFYNUUAELPPWFEUTHPYTHBAEBOEEAAEXRNGASRDEN |
| LP2-37 | 228 | 4.74 | 0.6 | agrippa_gibson | V1 | False | sub | True | 6082 | REDCEASAUEEAIPEHAEPAODAAPSNGAOWFBMAXDIOAWEEIISAGETHSEAHIAXFT |
| LP2-38 | 228 | 4.77 | 1.0 | emerson_essays1 | V1 | True | sub | True | 27909 | LCICFHESWDMMYRYTHWOESWOBLNNGEWSLTMFMYNGWIAIEAYUPSAIAIDAUETHD |
| LP2-39 | 240 | 4.07 | 3.0 | rune_poem | V2 | False | add | True | 12956 | SYLENGIEYDEAENGTWOREACHIAREFTYWJETHFTHDTNGSDNSDOFFWBUUOFGINA |
| LP2-40 | 231 | 4.44 | 1.1 | rune_poem | V2 | False | beaufort | False | 745 | WACRESIAEATHLUHEUMNGLWSCXEAHREEEOMUUEAHCUIHUMEABEANTHTHAIAEO |
| LP2-41 | 273 | 4.77 | 2.4 | lady_fountain_guest | V1 | False | sub | False | 35623 | AUGNGITDTNNWNCYJWRINRSGCTHOEEOLUEADOEIWWYNGAEMRAAAERXNTSNTHF |
| LP2-42 | 272 | 4.44 | 0.7 | lady_fountain_bulfinch | V1 | True | add | True | 20817 | EUAPLTHXATHTHMTEOFGWFPDHISRDEAINGTWSRIARNJIFAEWGUINLNGLDITHJ |
| LP2-43 | 274 | 4.69 | 1.8 | lady_fountain_guest | V1 | True | sub | True | 11650 | WDDXSAUNGUGEIAMOIGUBEOMNEWYYMFWSOOBAMGPFXGTHNLNGNEAIAATTHNGR |
| LP2-44 | 273 | 4.46 | -0.4 | king_in_yellow | V1 | False | add | False | 135101 | DIFBIOEOEBIAOTEAMYNGNFPTTHGEAUBURGWOTHBAEPXLCEAENSUBYUIBIDYN |
| LP2-45 | 270 | 4.99 | -0.1 | lady_fountain_guest | V1 | False | sub | True | 25460 | UTHTHTHCYSWEAIAWHSNLFWDLEAYIEGBOGIXAEOFXFGCFLIAOCONLYOETCTHE |
| LP2-46 | 270 | 4.70 | 1.1 | self_reliance | V1 | True | beaufort | False | 13580 | AFRNGTPEASCBELGYWDCEATHUYOMNYNGSTTTYWAETHGTHNGXXXULBAEAGOYWN |
| LP2-47 | 274 | 4.79 | 2.3 | lady_fountain_bulfinch | V1 | True | sub | True | 20177 | ITPNATHUTTWRLIACENWSTYUXPENYHUMDTHEAAEDOREEFNLBEODUGATHPUAPS |
| LP2-48 | 271 | 4.92 | 3.3 | self_reliance | V1 | True | sub | True | 32173 | IENSUMGNLNXIBBIRFDIMIAEAMEGAEFMEFORTHWUHOFFTSWCIAHECTHIANLCO |
| LP2-49 | 66 | 4.29 | 1.8 | king_in_yellow | V1 | True | sub | True | 108870 | EAIYDGNBOEYUTEEOSCISTAMEUUSFDTBFRCUBMDTHTCIIAUEUDHTIPMAEHDUD |
| LP2-51 | 92 | 4.74 | 1.9 | lady_fountain_guest | V1 | False | sub | True | 13208 | ROYAYFDWTHIRESOHWCOIRATNFALSERODALFRDIPRTPERYGOIAIGFMRFTFFRC |
| LP2-52 | 263 | 5.16 | 2.4 | lady_fountain_bulfinch | V1 | True | sub | True | 3737 | EPIOBEFIAIALOEUGHGAEAHFIAUIARITHDIIATLFPTHSYTHDCRUFSSFIIGTOA |
| LP2-53 | 179 | 4.31 | 2.7 | self_reliance | V1 | False | beaufort | False | 41321 | GHMLROMMSTTHNGUTHHNAWERYTAELMPAYAPUTHLBTHIGWJTELTFHFWEOEPDEA |
| LP2-54 | 232 | 4.43 | 1.1 | lady_fountain_bulfinch | V1 | True | sub | True | 13413 | LEOMNDEATIOMAPIALUUWNGTTPINGFMDAEAILBUXCFUNIATHFYGWIATHULMII |
| LP2-55 | 76 | 4.47 | 3.1 | king_in_yellow | V1 | True | add | True | 265975 | TOFAEGALUCNUIAENLEAFODOWWROAIACHEHFTHIIUHUIHFAMDUNGWEBLINOSE |

## Candidates meeting (1)-(2), for the readability check

None.

Largest z_uni over all tests: 5.46. Cells at z_uni >= 5: 15. Runtime, longest shard: 383 minutes on 7 shards.

