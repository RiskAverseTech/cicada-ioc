# External running-key lane: exact decoding at every offset

1 texts exact (every offset, both directions, V1 and V2) and 2 long texts at sentence starts (V1); 3 signs x 2 F; 40,083,780 tests over 55 pages; 2000 random-keystream nulls per page, F and mode; decoder max_skip 4. Rule: z_uni >= 7 and z_big >= 3 and readable (module docstring). Chance maximum of z over this many tests about 5.9.

## Controls (soft rule 0.81, corpus text at a random offset, signs/F/direction random)

| text | variant | n | sign | F | reversed | planted offset | top offset | z_uni | z_big | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| bunyan_head | runes | 262 | add | False | True | 8511 | 8511 | 11.9 | 23.4 | yes |
| bunyan_pilgrims_progress | runes | 137 | sub | True | False | 8364 | 8364 | 9.5 | 17.6 | yes |
| chaucer_canterbury | runes | 92 | sub | True | True | 755913 | 755913 | 8.4 | 16.0 | yes |

Controls passing: 3 of 3.

## Best cell per page (over every text, direction, variant, sign and F)

| page | runes | z_uni | z_big | text | variant | reversed | sign | F | offset | transliteration (first 60) |
|---|---|---|---|---|---|---|---|---|---|---|
| LP2-00 | 262 | 4.73 | 3.4 | bunyan_head | V1 | False | add | True | 28082 | THDEDNYMOABSNGNCUHXFJPNGAIAYIESNUWJIOIANIEAOOHIAWEXTOEPICJNG |
| LP2-01 | 266 | 4.66 | 2.4 | chaucer_canterbury | V1 | True | beaufort | True | 453187 | WFBOAONMHBHIAEIHLTHOMMTHMWYOUBDAECDADSYFEWEIEAXUMTMIAMFRAGPI |
| LP2-02 | 201 | 4.47 | 1.1 | bunyan_head | V1 | True | sub | True | 23250 | IAIFUPNNCOPDIRSEAWNGHFLDSURRLITRFCYAAWOXTWWHJSLUNIANGCFFSTAR |
| LP2-03 | 217 | 4.44 | 3.0 | bunyan_head | V1 | True | sub | True | 37591 | THIHNGGATMUAEWTNGULEWHIODOGRAEYUFFTLYEYACISNGUYIUWYNWNDJITHI |
| LP2-04 | 261 | 5.00 | 1.2 | bunyan_pilgrims_progress | V1 | False | sub | True | 168538 | ROEDDUSOUONGTHMYDASAEIOTHNLUSEAEAMGOBABENGCTOBLEAGJESOAOWTRP |
| LP2-05 | 263 | 5.04 | 0.8 | bunyan_head | V1 | False | sub | True | 24899 | ENYMCAIRFTHBCEAOIAEPRPDNGEASBORATYTEXIASRCLPUHYJODBTAYWTTTHD |
| LP2-06 | 196 | 3.95 | 2.9 | bunyan_head | V1 | False | sub | True | 24998 | REWGCONNASDAUSBFHTRBFUOEACITAYOEJEAJIAEAYFBUFRPUTTHIACONNTHF |
| LP2-07 | 208 | 4.51 | 3.1 | bunyan_head | V1 | False | sub | True | 37975 | PLTHNGUAISEJWDOOEIGNNIINOSRCICEBLFMPEYANADEONGOBTYOENGAAROEW |
| LP2-08 | 255 | 4.63 | 1.5 | bunyan_head | V1 | True | sub | True | 21882 | MNAETXCNIAEEOYNDYELADPMIIJOYJYSJHMHRFPNICCUUWUEMRTHSWNGWWJBL |
| LP2-09 | 268 | 5.15 | 1.8 | bunyan_head | V1 | False | add | True | 9572 | BUFWLEHJSTHIBEOTNGCCRPUTHTAFHRBOEEREATHEOTDYDIOTAETOELJMATHS |
| LP2-10 | 263 | 4.21 | 2.5 | bunyan_head | V1 | True | add | True | 32075 | SFJXMTHMHUWPAMETFLDOEHRURRNRAENGUETYSNGDTGRCOTHOPNGXETHSUEFH |
| LP2-11 | 273 | 4.73 | 3.9 | chaucer_canterbury | V1 | True | beaufort | True | 990673 | NUAEEAMEAUXEENMCUEAEFGGHSFIBEANWAPOYIREFWEAUEOHFTHEOYSAEURRH |
| LP2-12 | 261 | 5.04 | 1.7 | chaucer_canterbury | V1 | False | add | True | 176919 | DIAHIOUICHEOUTIAPFSLIHJNGOCCTSDFWMETHDGYHCFOTEAARSSYIHFSTRTH |
| LP2-13 | 272 | 4.20 | 0.9 | chaucer_canterbury | V1 | False | beaufort | True | 301646 | HOETHIYWGPNMMGDBJUCTHINGIPYYSLIABJFHEABGRYMPGFANIAIATSOPEOEA |
| LP2-14 | 137 | 4.98 | 1.6 | bunyan_head | V1 | True | beaufort | True | 49301 | HLFYMTWTHUIYEOITURTFRDTHLSNGNYLXNMNGMEDTAREATHRWYJENEGLEYWHD |
| LP2-15 | 159 | 4.90 | 3.2 | chaucer_canterbury | V1 | False | add | True | 341864 | AHUMPNGHODCHAESLGROTHIUMAEBPAYTPRIDSPTSCNRUOCTBADEEHUHIAUWAE |
| LP2-16 | 267 | 4.18 | 1.7 | bunyan_head | V1 | True | sub | False | 8592 | ACSTGBEOEOEARHMPDTHDRTOEUNGYWNGGWSLEAUWFICTHRGIAEARRFSOEIAHS |
| LP2-17 | 273 | 4.91 | 3.0 | bunyan_head | V1 | False | sub | False | 43412 | MTEXHYXIATEDLIOLNGLEBIANUCIPINGTHTHGNGFSANSIEOPAIJAPEOILWOWC |
| LP2-18 | 260 | 4.62 | 1.2 | bunyan_head | V1 | False | beaufort | False | 17515 | BSRMMATYSEACSMAPCMNGLRJISEONGROLUANEYTISDINGRFHXWXHTDIAUSYTS |
| LP2-19 | 271 | 4.10 | 1.0 | bunyan_head | V1 | False | add | False | 40349 | MRJEMIAMYHEIOUXSSWENGPMNWSIAEAEOAIMEAHGNIRAEDRNGAYBHAGUJLYET |
| LP2-20 | 269 | 4.56 | -0.6 | bunyan_head | V1 | False | sub | True | 18576 | TWTHUMOOECOETHTLAERLRRUBTCEOEGRTMDNYAFSSIRGFTFNBRSNLRXENGGEA |
| LP2-21 | 273 | 4.75 | 0.7 | bunyan_head | V1 | False | add | False | 48620 | AELSXFPGXTHRTHFCTHSWLTPTSJNGELIROUEIAMPOGMXTEOEGSWEDHPHMHFYI |
| LP2-22 | 131 | 4.01 | 2.7 | chaucer_canterbury | V1 | False | beaufort | False | 503115 | DEAPOWNIRHTOWYNTIRMFWENETIAMRWIATMOIATEOSUYSLCBUTCWGCTGEIAAE |
| LP2-23 | 213 | 4.28 | 1.9 | chaucer_canterbury | V1 | True | sub | True | 799172 | IAHIUMEAEAGTEDYIATHWPACTHWRRIEETHBLMNGTHDTHLOMOETESSIXRLOIOC |
| LP2-24 | 270 | 4.36 | 1.0 | chaucer_canterbury | V1 | True | beaufort | True | 803066 | PFFURUSIULOOWNGBMRIATBCCFSAEDRJWSIOETHIEINWSUNSXNGFMGMNGRECI |
| LP2-25 | 273 | 4.45 | 0.9 | bunyan_pilgrims_progress | V1 | False | add | False | 103695 | PGNHNGDCBAESHDIAERFWYPIYECUNGGNGYTLEDCJUCUROUIATOEOIXYHNGINP |
| LP2-26 | 265 | 4.95 | 2.0 | bunyan_head | V1 | True | beaufort | True | 33300 | LEAAMEAEAJATHIDWGATHIETTHENTHINGAEREMLMTWNHTHAEWILFTHXTHWDFI |
| LP2-27 | 234 | 4.98 | 1.8 | bunyan_head | V1 | True | sub | True | 7900 | AYBTHAEXETHWNNTHSOTTHICIDTYEOJNYSFOIUPMIIFNGTASCSEXTGOLADIBO |
| LP2-28 | 269 | 4.43 | 1.1 | bunyan_head | V1 | True | beaufort | False | 34841 | AUMUOCMIOIACLDRAECARTLAMYFIAJTHRCCETHTUOWNGIAJOTTIAIULRHCRDT |
| LP2-29 | 277 | 4.97 | -0.1 | bunyan_head | V1 | True | sub | True | 11106 | DXAEIGBTDIOLWGSTFTEEAFIAYAGSTLCTHXUPWRWWEAOEAIASLFALNGGWCMNM |
| LP2-30 | 263 | 4.22 | 1.7 | bunyan_head | V1 | True | sub | False | 13578 | NGSSORMEOBNBNHGBUDIALCHTACDJPTHRNLLSTOEGEICIBNYUIAOEFTHYEMNO |
| LP2-31 | 269 | 4.61 | 0.4 | bunyan_head | V1 | True | sub | True | 45286 | SXYJNBNNGEAOULATHCJNRUMHIANMNELWXBRJTHFANGTHATLRAERDHTHFICCI |
| LP2-32 | 121 | 4.21 | 1.8 | bunyan_head | V1 | False | add | True | 13576 | UHRAEATHBOPJTHDDSEAUOIASTAJLONGTPMJFELOARCCNGITHRAEIIHOBNRIU |
| LP2-33 | 214 | 4.81 | 0.8 | bunyan_pilgrims_progress | V1 | True | add | True | 16975 | YNHSDMPNEAYUFRADTHNUTOYBNAEBTAIAGCHBTPACOHFMCSPETNEOEFTRCAMC |
| LP2-34 | 261 | 4.30 | 2.8 | bunyan_head | V1 | False | beaufort | False | 7649 | FWGTHAUYEAONGCDLIMUTHCIACIIAEYPTMNNTECFHEABWIAEARUGUMDTHBRYJ |
| LP2-35 | 271 | 4.77 | 0.2 | bunyan_head | V1 | False | sub | False | 12769 | CYTLFOIATIAFEANGHSAPARSIEAMDHUBEAOLIUNGDOANGMOHHYHRAAOEGDTGM |
| LP2-36 | 238 | 4.15 | 1.0 | bunyan_head | V1 | True | beaufort | True | 8862 | RDUODTNIAOSAEDUASEOUWMSEONONPMDMEOEIIAMCTGHONGCTEAABEURNJEAE |
| LP2-37 | 228 | 5.07 | 1.4 | bunyan_head | V1 | False | sub | False | 40674 | XTANUYRACERTYIYIWJTNGTHISSNGEGFINMPHEATHGBEAEOPCFIHTHETHIRJC |
| LP2-38 | 228 | 4.87 | 2.2 | chaucer_canterbury | V1 | False | sub | True | 50538 | ITHTYEJATPEOMFELFYRRYTSAWTHAINGNUANHRDNGWUDMTOPTHOTHLTLSSBEH |
| LP2-39 | 240 | 4.09 | 1.8 | chaucer_canterbury | V1 | False | add | True | 418549 | AEEOYFIJILEGFACDNMRECRGOMNOSFTHIOESAETOIOEEFBEAOHHSYTLWAUHRH |
| LP2-40 | 231 | 4.53 | 0.6 | bunyan_head | V1 | True | beaufort | True | 44816 | NNIOYWWDNGLIYADUFLHIARIADTBFRNIAEARTMUEMILUMFTDOFDNODELPBAMN |
| LP2-41 | 273 | 4.30 | 1.7 | bunyan_head | V1 | False | add | True | 21054 | UCYEIAFOEAAEOUGLIMWWNAEUGODATHWIRBSLSXLRDXETHATHOEMCOCYDWSTH |
| LP2-42 | 272 | 4.74 | -0.7 | bunyan_head | V1 | True | add | True | 6748 | AFIEAOMGLHMGLGOFCOOSYWNXNGGGINGEAOEAWGYFMFNGAGNAIAGGTYBIHEOS |
| LP2-43 | 274 | 4.43 | 2.4 | bunyan_head | V1 | False | beaufort | False | 2638 | TIAPLTHENTSWANMEOCEDMEOJIANTENBEHXOCDFAEEIOEEIAEAYSDSYWLSOWS |
| LP2-44 | 273 | 5.21 | 1.6 | chaucer_canterbury | V1 | True | sub | True | 692709 | REALUITLGTEAJNGSPNEAYLOTHGMWYPMNGSUUUYSYWBNCYEAEANORIALDUHER |
| LP2-45 | 270 | 4.07 | 0.8 | bunyan_head | V1 | True | beaufort | False | 24885 | YWBIMNFIWRBWXMGSXETBEUYHBYIDWLSUNGUDYMCSTWYDWEOEYFEOAEARMFGO |
| LP2-46 | 270 | 4.50 | 0.3 | bunyan_head | V1 | False | beaufort | False | 19770 | TOIPNGPSUPSOEHTAMFRCMDEAOEIAIFGUCAEFJTHXEERHREAGLNGOEACUONGP |
| LP2-47 | 274 | 4.19 | 0.9 | bunyan_head | V1 | True | sub | False | 34612 | HYHWRCOETNGFNGTEOICANGFTCINGNGIUGNGMLTCYBIEIMIAIABLYLUSIANAE |
| LP2-48 | 271 | 4.37 | 1.2 | bunyan_head | V1 | True | sub | True | 13973 | UOFAWOEIAUNXEFIADNTNTGBTHLTYRFEOEFYTHPANFRIAWETRUEOBDWFAEOTO |
| LP2-49 | 66 | 4.36 | 2.4 | bunyan_head | V1 | False | sub | True | 14440 | NEHFTRNMDERWOTHCUGMTUEAATWOFWIAEAWTHHFDWEDOMLPAGNHUSRTEIATHP |
| LP2-51 | 92 | 4.47 | 4.7 | bunyan_head | V1 | True | sub | True | 40060 | TNGOIANSCWDTNSUOTJCPRUATSEAEOXNOWAETDEOSEDHIGXSTACRLIPREESAE |
| LP2-52 | 263 | 4.60 | 0.8 | bunyan_head | V1 | True | beaufort | True | 24896 | RTJAELONIAAIAIOLEAAUTYSDNHPCWUROEWUTYHNPEUCNGAPMLUYREANGBMWA |
| LP2-53 | 179 | 4.33 | 1.5 | bunyan_head | V1 | False | sub | True | 45776 | YUNGSINGTDINGEALDSXLEDDSNGWANIAEAXAPYDIUADOOLTHEAJBIOSLBMBEG |
| LP2-54 | 232 | 4.49 | 3.0 | bunyan_pilgrims_progress | V1 | True | sub | True | 119618 | EFYPMYCNGFNEOUSEDEAUCOMSBFIXUINRUSOEPNGUDIACBITYILNGIAITELHM |
| LP2-55 | 76 | 4.12 | 2.4 | bunyan_head | V1 | True | beaufort | True | 11074 | OCMFNDSLPFHEFHIAFLPLFNUOUOFEPMDOTHTHTEIAUANTHMLUWOPEGONGYOIP |

## Candidates meeting (1)-(2), for the readability check

None.

Largest z_uni over all tests: 5.21. Cells at z_uni >= 5: 6. Runtime, longest shard: 105 minutes on 7 shards.

