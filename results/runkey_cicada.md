# External running-key lane: exact decoding at every offset

1 texts exact (every offset, both directions, V1 and V2) and 0 long texts at sentence starts (V1); 3 signs x 2 F; 7,812,750 tests over 55 pages; 2000 random-keystream nulls per page, F and mode; decoder max_skip 4. Rule: z_uni >= 7 and z_big >= 3 and readable (module docstring). Chance maximum of z over this many tests about 5.6.

## Controls (soft rule 0.81, corpus text at a random offset, signs/F/direction random)

| text | variant | n | sign | F | reversed | planted offset | top offset | z_uni | z_big | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| cicada_own_words | runes | 262 | add | False | True | 1324 | 1324 | 11.8 | 23.4 | yes |
| cicada_own_words | runes_nodigraph | 137 | add | False | True | 2646 | 2646 | 8.3 | 16.7 | yes |

Controls passing: 2 of 2.

## Best cell per page (over every text, direction, variant, sign and F)

| page | runes | z_uni | z_big | text | variant | reversed | sign | F | offset | transliteration (first 60) |
|---|---|---|---|---|---|---|---|---|---|---|
| LP2-00 | 262 | 4.63 | 1.0 | cicada_own_words | V1 | True | add | True | 4423 | ONAINGACFHTHHYXCHTGSYIFAWXGUOOUYBTYNGMXMELEHBRMIAYSCNOAFHDNO |
| LP2-01 | 266 | 4.04 | 3.4 | cicada_own_words | V1 | False | sub | True | 7757 | NSSYWYEADYEIRFPNWOIEARMTHOABPYSCTHFDPUTEWIEOXAEIUDMENGUEAOBC |
| LP2-02 | 201 | 3.65 | 3.1 | cicada_own_words | V1 | False | sub | True | 4646 | EAPRMURHAETUYXPXWMHJWGNGHNTHYGTYXPTYEDLREWPXIEOUTHASTNFRCELT |
| LP2-03 | 217 | 4.15 | 2.0 | cicada_own_words | V2 | False | sub | True | 2768 | SIHOEOEDIAIHWEACTMMERUTHEEANJWTLDPHSFANYCHBWTIAUAOUTNEAXFHEL |
| LP2-04 | 261 | 4.39 | 0.1 | cicada_own_words | V1 | True | sub | True | 5920 | SEEAYUPOXTTTHRFREAUYNXTHWTHAWROAAYPBTHIAEEWAYNTHFREORDNDWGWR |
| LP2-05 | 263 | 3.90 | 1.0 | cicada_own_words | V2 | False | sub | False | 3327 | AURWWLTHNTEAHWPHSFUWENGEAUMUHFMHUEASANLAEGDWAPTHOTHOECEYGAET |
| LP2-06 | 196 | 3.94 | 2.3 | cicada_own_words | V1 | True | add | True | 6424 | THFWEEPNGMYOXESNGWEOTHPADDAMENRMUSFRRIAEONSUEIATSOCAHPOSGEAD |
| LP2-07 | 208 | 4.18 | -0.4 | cicada_own_words | V1 | True | sub | True | 5775 | OERSXGTYITHADHOENGTHWRMEEEANFPCOUUPTYAINRIBEAFRNNINMIECRYSPT |
| LP2-08 | 255 | 3.74 | 2.5 | cicada_own_words | V1 | False | beaufort | False | 1824 | TWGLRBEAPWNGUNSWTHACCJENGUMLDOTEATYDUUBCIOONJUWULDSJILWHUROE |
| LP2-09 | 268 | 4.43 | 0.6 | cicada_own_words | V2 | False | add | True | 2632 | PIOUSSHRIADUNAETHWNWONIBEIOLPENOYNDHETSNEAEEUMJLIFGBDOSCTHWA |
| LP2-10 | 263 | 3.88 | 0.8 | cicada_own_words | V1 | True | sub | True | 6357 | TUCIUMSXMEUTPYNOGHEAFAHEEAHEASYCCLHHMNTDPSJLEAMFLTICAELBIHPL |
| LP2-11 | 273 | 4.49 | 2.3 | cicada_own_words | V2 | False | add | True | 414 | UNGSNGTURNGWLOTTHRGEATECJMNMCNEAIAEADNGIOAAROPLFYMFUCIAEYBNN |
| LP2-12 | 261 | 4.16 | 2.1 | cicada_own_words | V1 | False | add | True | 7787 | CPCXUEATMNGPYCTITHNPFHTHNTBNGFDRECAIOEFTNGSHEALJWDSYFSYCJFXH |
| LP2-13 | 272 | 3.96 | 1.4 | cicada_own_words | V2 | False | beaufort | True | 1574 | COFSRADNMSAHIALNHPOFEAMAEAHAEYEDTHTHMRYXAEODPRIESSOEYECTDIMN |
| LP2-14 | 137 | 4.18 | 1.5 | cicada_own_words | V1 | False | sub | True | 192 | THFEAECUOXDFSRNGIWNGGNWOWTTHDGJCTHECXUYGABFUFBRTINSMOUYYNGNN |
| LP2-15 | 159 | 4.26 | 2.2 | cicada_own_words | V2 | False | beaufort | False | 2539 | AHGBFIAMSFERCDAEEASAIONDEODSBNEAPEASREYOEMNMLEBAERAAHTHPSTHU |
| LP2-16 | 267 | 4.07 | 1.3 | cicada_own_words | V2 | False | sub | False | 7048 | SLUCSIADIIDXTHPTHMTMEAAEJWBUSEPHGIISSEEDDMYNUTHNGRCIATHUFLBW |
| LP2-17 | 273 | 4.18 | 1.5 | cicada_own_words | V1 | True | sub | False | 4279 | FNGHEYNNRPEOINRISUIAAEECNCNOEGCAEEOTUSJTEAIUNGNPOHMATNAABTNI |
| LP2-18 | 260 | 4.25 | 2.5 | cicada_own_words | V1 | False | sub | True | 3553 | AEDUOLSPTHITHDTHAEWUONEUOCECCUFLOOAEATTHMFEBAESMOWNTTHAAEAOF |
| LP2-19 | 271 | 3.70 | 3.2 | cicada_own_words | V1 | True | add | False | 3781 | EHODPOJDTHTPNDTHAEEANNNNGFHMETTRMANGSUEAWEIMSEALENUNAMNGFLWC |
| LP2-20 | 269 | 4.42 | 1.2 | cicada_own_words | V2 | False | sub | True | 2063 | ABGTYFCAAHIAWWBSIMDAXUTHXASIAXUDORFNGFWAEHCEYLFNORHTOEGWOFLD |
| LP2-21 | 273 | 4.20 | 0.6 | cicada_own_words | V2 | False | beaufort | True | 3801 | FSMUGLTHTENBEPINGAEJNGLTHTMRATHTHWEANEDWFPHYDYOEACSREAABAITH |
| LP2-22 | 131 | 3.87 | 2.8 | cicada_own_words | V2 | False | beaufort | False | 6469 | PDROPXGYIAARSDRGFGSUROROSSCMIEYOEOBUATHTRTNODWPURHEAUCODPNTH |
| LP2-23 | 213 | 3.72 | 0.2 | cicada_own_words | V1 | False | add | False | 2363 | RAESTWOBAFLMIAONGCPBFBLFILRWLEAAYYIFOBSTHPAWRAGGCSHEWPLFXAUI |
| LP2-24 | 270 | 3.86 | 2.6 | cicada_own_words | V1 | True | beaufort | False | 2125 | FXCLNGPNESOCGMTOWODDHMLDPTHIYYYOLTNIAAITYMMAESXUTYRAEPEATHEO |
| LP2-25 | 273 | 4.20 | 3.4 | cicada_own_words | V2 | False | beaufort | False | 3289 | ENJYNFFXDNGTHAESPMHESTUIAEOREAPTRPDAEOAENGYPNGJLDAYDTHUPWOEA |
| LP2-26 | 265 | 4.43 | 1.0 | cicada_own_words | V2 | False | add | True | 1434 | TIARMIAEABUAHFJRONYMNBORJNGGTHFTBLBHYRGEFLXDNPFIBDWTTNGIPNCT |
| LP2-27 | 234 | 4.52 | 3.4 | cicada_own_words | V2 | False | sub | True | 7196 | UOGFYYFCPSTHTHNNRIYMINPFYAWBUFSTXNDALNESDPISTHMROBREFSENGOOI |
| LP2-28 | 269 | 4.06 | 2.3 | cicada_own_words | V2 | False | add | False | 3945 | UXYNGCMREABOINTAESMFBIANUTHWEAERMNUJOYNHWSENGSSDSHUERBNMUCIU |
| LP2-29 | 277 | 4.30 | 2.2 | cicada_own_words | V1 | True | sub | True | 3541 | YPEYCCOEAESCTUUGUTIRIANTHUDEEHMISTHCNGYRJNREOIIYLIATGOHAGTNE |
| LP2-30 | 263 | 3.63 | 0.8 | cicada_own_words | V2 | False | add | True | 5985 | XAEEDLOFXEWNGLMFCWHTHBLNGRYIOMNGAUIANSNGROEGMDIWENGPDOSNGSIB |
| LP2-31 | 269 | 3.80 | 1.7 | cicada_own_words | V1 | True | sub | False | 1568 | CRTUSLOEXRYEAENGPEAFMRORTIADRWAUMSCNFDAUEADYXLOWTHCTEFTONLMH |
| LP2-32 | 121 | 4.29 | 2.4 | cicada_own_words | V1 | True | beaufort | True | 5234 | ITHWUNBEEPPAATHUXNSYPJTHNHEASOETTIATNSBUSYMNGOYDOFIOMLEOFAEI |
| LP2-33 | 214 | 3.97 | 2.0 | cicada_own_words | V2 | False | beaufort | True | 6775 | ARRNFGFYIEOAFTHTHIHNGIOOWRNGHIAXPIEADMUMNNTYOCAHSEOTHTIDSLPE |
| LP2-34 | 261 | 4.02 | 1.1 | cicada_own_words | V2 | False | add | False | 2526 | HIAEDEAIANAWLTHEAELIAIADYNTHNGOBBTHTHYDDMEPJHFWOOEYTEYTHNOIH |
| LP2-35 | 271 | 4.01 | 0.7 | cicada_own_words | V1 | True | add | True | 4784 | ULCFRTHBTHEOFPIAAECLEEAHNINENYMIOENIYTCAWWPPSTHTHTHPTIAUFCRC |
| LP2-36 | 238 | 4.51 | 2.6 | cicada_own_words | V2 | False | add | False | 2959 | SATTHIAYWSHELDELERYGFTHCRCMADIDTRENSTHYPJNTHLEOEUMHHEOYTHTXI |
| LP2-37 | 228 | 4.23 | 0.8 | cicada_own_words | V1 | False | sub | True | 3868 | FTROHMNATNMPXNGIEAYYMOOEOORYNGTHTNGLRRPENAOWFIWBDDIRRUITWEFT |
| LP2-38 | 228 | 4.01 | -0.5 | cicada_own_words | V1 | False | sub | True | 4123 | ITHTCANGMGSWCFIRILTAETNBODTHBIATHRTSFOIJAXLOHTHTHDSWUMPGRIEG |
| LP2-39 | 240 | 3.96 | 1.9 | cicada_own_words | V2 | False | beaufort | True | 3611 | ETHCANNNBNGTYFTHGURTHTOLWICOENRXIANGUIAMCNGDJSTHUNYMOFTHCAWI |
| LP2-40 | 231 | 4.33 | 2.3 | cicada_own_words | V2 | False | add | True | 3420 | IRFCGNIAXTEIYWDEDDCRAECLCRDGHCPIINIATMALELRDACOUFEOTMUCAEGSA |
| LP2-41 | 273 | 4.17 | 2.3 | cicada_own_words | V1 | True | beaufort | False | 7701 | GCNORXAEJUJCTTNSEIADAELXTHEMBSSSIAOTHSRFIGAEDICWTHLIAHNCHEUL |
| LP2-42 | 272 | 3.92 | 1.6 | cicada_own_words | V1 | False | beaufort | True | 3485 | LTHAEYAEGCLIAEIRNGWSEOFTTHMAEIAHMHRHDOEIDDHOHULHBNDNHSIARDHA |
| LP2-43 | 274 | 4.59 | -0.2 | cicada_own_words | V2 | False | beaufort | False | 4108 | HCHSDCBTXGJEANIWFCGFAHUTHYTHIEPTLOYTHYRCSEIATHIASIADNRSPFNGI |
| LP2-44 | 273 | 4.39 | 0.4 | cicada_own_words | V2 | False | beaufort | True | 3179 | IXNAEWWEWRLWOMTTUHTDHEDORHPOEFEHJEFHRFSOTTNYNGDLBOTHCYLWYSOE |
| LP2-45 | 270 | 3.82 | 0.4 | cicada_own_words | V1 | True | beaufort | False | 3569 | IELBYHPTHOMTAJHUDXAFPEOLAETAMIWTNGWCYMTHNGTCSNGNGUGUPFIIANEO |
| LP2-46 | 270 | 4.27 | 2.1 | cicada_own_words | V2 | False | sub | True | 198 | NGTJNGDOEOSFACEROYOEAEAAIIFYWIXLMTREBSTHGEINAECRTHGOEOCEAAEO |
| LP2-47 | 274 | 3.90 | 2.1 | cicada_own_words | V2 | False | beaufort | False | 3886 | HCETAYSPSDUIFMFLAWSAETCBABOWDTHCAPOWUEAODFNGAUHNNGIBTEMBHTTH |
| LP2-48 | 271 | 4.04 | 2.9 | cicada_own_words | V1 | False | beaufort | False | 365 | TRTEEAOYYTHTHSHXFMCRDGUGNGYPNGTHEFEETHTHSFIHHJFHOEHWCCSWNAYT |
| LP2-49 | 66 | 4.40 | 4.0 | cicada_own_words | V2 | False | sub | True | 556 | YPOFRMDYAHONGIEAEBBRIDUMIANGORSWDNAIMFAASRTOCIUXIUDTHTAWETTH |
| LP2-51 | 92 | 3.52 | 1.7 | cicada_own_words | V2 | False | sub | True | 5608 | MIRADBAEAUAREAEICSNMIEALWERIIAHAEWSCGLFEIAOUENGTHAIWJCIEACGS |
| LP2-52 | 263 | 4.18 | 0.7 | cicada_own_words | V1 | False | beaufort | True | 3255 | TCTSGJRPORLFMSDWUEMDBUPNICURLOECTPOJHXICMHRTWNGTHNGHSEXSTHOD |
| LP2-53 | 179 | 3.69 | 1.9 | cicada_own_words | V2 | False | add | True | 2869 | OXSRSCTENUNGAEJBAEWRGRGTRNSLIARCSTONFTMLCEYRNGGWCIRSSEANCHNW |
| LP2-54 | 232 | 3.81 | 2.2 | cicada_own_words | V1 | True | sub | True | 5037 | SNSMBUIASBWOETROGJJHOUTYNNIAMTNGACJMSWSEFPOXFAWAEUUDASJFIATH |
| LP2-55 | 76 | 3.78 | 2.4 | cicada_own_words | V1 | True | sub | True | 7642 | YEEASNGLNBUIDREYAFWUXTHAEOUAFRNASAAOEOTHTHOLITCAWYTAETHAITHA |

## Candidates meeting (1)-(2), for the readability check

None.

Largest z_uni over all tests: 4.63. Cells at z_uni >= 5: 0. Runtime, longest shard: 67 minutes on 2 shards.

