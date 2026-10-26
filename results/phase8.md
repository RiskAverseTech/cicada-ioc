# Phase 8 sweep: the hypothesis loop's short list (LCG seeds; word keys with a position-walking multiplier)

15834 configurations per page (lcg(a=1033,c=0,m=3301) add: 3,301, lcg(a=3,c=0,m=3301) add: 3,301, lcg(a=7,c=1,m=3301) add: 3,301, lcg(a=7,c=1,m=3301) beaufort: 3,301, lcg(a=2,c=24,m=29) add: 29, lcg(a=3301,c=29,m=1033) add skip2: 1,033, word keys × position multiplier: 1,568), 55 pages, 2 F variants: **1,741,740 tests**. Chance maximum about 5.4.
Per page, variant, decoder mode and rejection width the null is 2,000 random keystreams through the same decoder (a random key through a multiplier schedule is still a random key, so one null serves every schedule). Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.

## Planted controls

| control | set | key | F | z | rank in set | runes recovered |
|---|---|---|---|---|---|---|
| control-00 | lcg(a=1033,c=0,m=3301) add | seed=3029 | False | 10.8 | 1 | 1.000 |
| control-01 | lcg(a=3,c=0,m=3301) add | seed=1590 | False | 11.1 | 1 | 1.000 |
| control-02 | lcg(a=7,c=1,m=3301) add | seed=3104 | False | 10.8 | 1 | 1.000 |
| control-03 | lcg(a=7,c=1,m=3301) beaufort | seed=418 | False | 11.7 | 1 | 1.000 |
| control-04 | lcg(a=2,c=24,m=29) add | seed=24 | False | 11.8 | 1 | 0.992 |
| control-05 | lcg(a=3301,c=29,m=1033) add skip2 | seed=512 | False | 11.5 | 1 | 0.992 |
| control-06 | word keys × position multiplier | m=(5i+23)%28+1 | False | 10.9 | 1 | 0.983 |
| control-07 | lcg(a=1033,c=0,m=3301) add | seed=878 | True | 12.4 | 1 | 0.988 |
| control-08 | lcg(a=3,c=0,m=3301) add | seed=1950 | True | 13.1 | 1 | 0.975 |
| control-09 | lcg(a=7,c=1,m=3301) add | seed=667 | True | 11.9 | 1 | 1.000 |
| control-10 | lcg(a=7,c=1,m=3301) beaufort | seed=2717 | True | 12.4 | 1 | 0.925 |
| control-11 | lcg(a=2,c=24,m=29) add | seed=8 | True | 12.4 | 1 | 0.996 |
| control-12 | lcg(a=3301,c=29,m=1033) add skip2 | seed=962 | True | 14.4 | 1 | 0.988 |
| control-13 | word keys × position multiplier | m=(19i+21)%28+1 | True | 12.2 | 1 | 1.000 |
| control-14 | lcg(a=1033,c=0,m=3301) add | seed=710 | False | 12.0 | 1 | 1.000 |
| control-15 | lcg(a=3,c=0,m=3301) add | seed=2214 | False | 11.5 | 1 | 1.000 |

Controls recovered at z ≥ 6 and rank 1: 16 of 16 (z 10.8–14.4).

## Unsolved pages: top 20 configurations overall

| page | set | F | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|
| LP2-47 | lcg(a=7,c=1,m=3301) add | True | seed=15 | 4.51 | 6 | NNGSFASNEAPTNJEADRIAIAONGFNOHRSAAOEAEDTNJRLIPNEMCMDADEUHPNWLRCTTIOFEAETGTFRXHLOEYEAEANGHEFEJ |
| LP2-15 | word keys × position multiplier | True | m=(4i+6)%28+1 | 4.44 | -1 | FSOUUIEAPSRAJMNGWBEPFEAPIMAMLEFTSRTOOAYERPBIAAMPTGPYIICESYSNNGULTHFUIMIIFLSLASYUUSNGWH |
| LP2-24 | word keys × position multiplier | True | m=(12i+12)%28+1 | 4.44 | -1 | FTFTGEEABMAWJWMTHNGNRIOEMINOAYTHIALCGPIMYPOMSCNHTHEOAHEOGRGRJYPSTHMTAIAHAELUFASTSBUNNGHDABW |
| LP2-23 | word keys × position multiplier | True | m=(14i+3)%28+1 | 4.43 | 0 | NRTEANGYNSRTHAPNTHPFDODBHXLESWSTXMAENFRHREBTHPRLUFNOAWGMJFYNETHCSOEJMHCIPTHDPMIARCMBWTHRM |
| LP2-21 | lcg(a=7,c=1,m=3301) beaufort | True | seed=1139 | 4.40 | 0 | RLEAOAASNGOUTILRMESIRIDDHLOEFFMEABAEDTHAPIDGOFFSGMIAMGGHPBSPIRRIABGPAEYPIRCAOAERTEALPJMTHPI |
| LP2-25 | lcg(a=3,c=0,m=3301) add | True | seed=2319 | 4.39 | 1 | UBUJTUTHXHTRMXHDYIAYFHOSDTNGLINNGEOTSBYTHIEAGEMCRTHBGFTIASAMOEEACFSNGAIAFOHGTLNGLSCWULOFPREAJ |
| LP2-21 | lcg(a=1033,c=0,m=3301) add | True | seed=630 | 4.29 | 6 | CNNGERCYTHASRBCATEORIBWRTEAHDUDIRHEAUARSEJSFIEAFITHMRTHSUTHROSNWDJXPYINOATNRMGTHAYTHGNGGPCFY |
| LP2-21 | lcg(a=7,c=1,m=3301) beaufort | True | seed=2992 | 4.28 | 1 | OPBRNGASNGOUTILRMESIRIDDHLOEFFMEABAEDTHAPIDGOFFSGMIAMGGHPBSPIRRIABGPAEYPIRCAOAERTEALPJMTHPI |
| LP2-12 | lcg(a=3,c=0,m=3301) add | False | seed=150 | 4.27 | 10 | MDNLPBADEAYYSMAWSBHCYSAAUOWCHSIWELINRJTHGOEOCXIAUWOGMFSOENMFFWRYXFCXIADFXFICRATHMEALSE |
| LP2-23 | word keys × position multiplier | True | m=(0i+3)%28+1 | 4.27 | 0 | NETINGUNARNASNNPFDEADRHCLDSBSXXPADNFRWRDBNPELMFYONGWIAMGFUNDTHHSEAEGMWCTPNDSMLRHMRWNRP |
| LP2-43 | lcg(a=3,c=0,m=3301) add | True | seed=2234 | 4.26 | -6 | AUNSYDEBARMRFYCSMTHHYCNGUMMYWBDATHDTAFCREFWTNFJYMPAUGBMTHMANGDRXSEAWWARDCTHIAEGFDIAWFEAS |
| LP2-47 | lcg(a=3,c=0,m=3301) add | True | seed=1167 | 4.22 | 4 | THHLHLSTPPREHSNFENGAEWMYDTHNGEOFALETHROSYLIYEAUIAMTRGEIWGIDFOYIAOGAEAYAPUURASNANIAEAWNGGORNGNC |
| LP2-30 | word keys × position multiplier | True | m=(2i+8)%28+1 | 4.21 | 3 | FAENGTRBBTIOBSLDETYJCIBEMIRNRREMDROIXWTJEOOENTHJJBNGAETHIOTHURSSOAETHATTHYTHULDESNLNESLEDHXH |
| LP2-41 | lcg(a=3,c=0,m=3301) add | True | seed=2633 | 4.21 | -2 | WFDWYNBOROFFMLYNEDSEAHNEAMTHFRDSORTHHUPUMELAOFNLNTHITHNETCEADHAATFOYIAAEAYHEAOHRXSOEAJINGW |
| LP2-47 | lcg(a=3,c=0,m=3301) add | True | seed=200 | 4.20 | 3 | HHLHLSTPPREHSNFENGAEWMYDTHNGEOFALETHROSYLIYEAUIAMTRGEIWGIDFOYIAOGAEAYAPUURASNANIAEAWNGGORNGNC |
| LP2-25 | lcg(a=7,c=1,m=3301) beaufort | True | seed=463 | 4.18 | 3 | SNGLORWJPUBEBSNGSIASINGIARTHEFEDRWYEOIINXPLATMPWNGWCFUUPEACANGHYYEFIWNWTHYEMAUCNGPPTHPEATHDR |
| LP2-44 | lcg(a=7,c=1,m=3301) beaufort | False | seed=1443 | 4.18 | 3 | YUMUTRCFRUJOSTHUWHRTNGHYTXTHFEETBHTHYSIBMUNGUPEHFERREAEACOEURGNYTTHIYNGECWESJEPMIMUTOOFHSEA |
| LP2-47 | lcg(a=7,c=1,m=3301) add | True | seed=106 | 4.17 | 5 | IDXPDIAAEAFWDFEADRIAIAONGFNOHRSAAOEAEDTNJRLIPNEMCMDADEUHPNWLRCTTIOFEAETGTFRXHLOEYEAEANGHEFEJ |
| LP2-46 | lcg(a=1033,c=0,m=3301) add | True | seed=1490 | 4.15 | 3 | OANXWFIYFHLJYFWPPEOUNHTHNGETHHARDDICHWOGDTHFBEFMWETFBDATHHWGSOELCOARHPBTHTBURAXNGHUDFPYTH |
| LP2-54 | lcg(a=7,c=1,m=3301) add | False | seed=1107 | 4.15 | 14 | WCDWLIIIBYARWOMAHLNGPTHPTLEEAEADETGEOSIEAERSTSOEAOIADFLFOSEOPAEYAEOAEJSOECALOINGGHBGSIEOEAOEOIE |

Largest z per set: lcg(a=1033,c=0,m=3301) add 4.29; lcg(a=3,c=0,m=3301) add 4.39; lcg(a=7,c=1,m=3301) add 4.51; lcg(a=7,c=1,m=3301) beaufort 4.40; lcg(a=2,c=24,m=29) add 3.77; lcg(a=3301,c=29,m=1033) add skip2 4.14; word keys × position multiplier 4.44.

Largest z over all 1,741,740 tests: 4.51 (LP2-47, lcg(a=7,c=1,m=3301) add, seed=15).

## Verdict

**No page decrypts.** The LCG families at every seed (five moduli/multiplier pairs, add and Beaufort, single and double skip) and the two solved word keys under every position-walking affine multiplier schedule, each with and without the F rule under the soft reject-on-repeat rule, are excluded at the sensitivity the controls demonstrate. This says nothing about other LCG parameters, other words under the multiplier, or the loop's larger feedback families, which were not run.

