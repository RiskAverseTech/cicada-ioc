# Seeded generators no ledger lists: 8 generators x 3 reductions, seeds 1..262,144 plus 35 named seeds

Tier 1: 113,261,328 window decodes (80 runes, pages LP2-00/01/02, 6 cells); survivors at z >= 4.5: 31. Tier 2: 31 full-page decodes; candidates at z_uni >= 6.0 and z_5 >= 6.0: 0. Rule and coverage in the module docstring; prior coverage by other labs listed there.

## Controls

| generator | reduction | seed | sign | F | tier-1 z (rank) | tier-2 z_uni | z_5 | pass |
|---|---|---|---|---|---|---|---|---|
| xorshift32 | mod29 | 220975 | sub | False | 6.4 (1) | 12.6 | 60.5 | yes |
| xorshift64 | top | 259893 | add | False | 5.4 (1) | 11.7 | 53.0 | yes |
| xorshift128 | rej | 49669 | beaufort | False | 5.5 (1) | 10.8 | 38.9 | yes |
| pcg32 | mod29 | 17295 | sub | True | 4.8 (1) | 14.2 | 42.5 | yes |
| minstd16807 | top | 192467 | add | True | 7.2 (1) | 15.6 | 55.9 | yes |
| minstd48271 | rej | 145074 | beaufort | True | 6.1 (1) | 12.8 | 57.7 | yes |
| randu | mod29 | 221402 | sub | False | 6.7 (1) | 12.8 | 57.7 | yes |
| splitmix64 | top | 177370 | add | False | 6.4 (1) | 13.3 | 62.0 | yes |

Controls passing: 8 of 8.

## Tier-1 survivors (top 20 by tier-2 z_uni)

| generator | reduction | seed | page | sign | F | tier-1 z | tier-2 z_uni | z_5 | transliteration |
|---|---|---|---|---|---|---|---|---|---|
| xorshift128 | rej | 63113 | LP2-00 | beaufort | True | 4.83 | 4.72 | -1.2 | IATHAAELROFNLYADLIATHFYTOUAEDOTHEOOOCTIBOAPADCWRNL |
| xorshift64 | top | 104742 | LP2-00 | sub | True | 5.02 | 4.26 | -1.4 | SHTUMEGOHSTHAFITCOIFEHDLEMIATORTOCCOEEAFBOCYOIAUYC |
| xorshift128 | rej | 63113 | LP2-00 | beaufort | False | 4.63 | 4.15 | -0.5 | IATHAAELROFNLYADLIATHFYTOUAEDOTHEOOOCTIBOAPADCWRNL |
| xorshift128 | top | 199034 | LP2-01 | add | True | 4.85 | 4.12 | -2.1 | IACEABTHDUUITONOWLTOEMIENGIAYHELSNWHYEDTHTHLHLBECL |
| xorshift32 | rej | 47096 | LP2-00 | beaufort | True | 4.64 | 4.05 | -1.0 | NGYTIDWICDRIHCLRIANATOCPAIICSSPMITEIFIUUEFTSRDULSU |
| splitmix64 | top | 78402 | LP2-00 | beaufort | True | 4.75 | 3.96 | -1.6 | GWYEOGARWUUSUENBTHFGTAEIFEATHWPTCMFRSIAWESOAHSWIAI |
| xorshift64 | top | 104742 | LP2-00 | sub | False | 4.79 | 3.89 | -0.7 | SHTUMEGOHSTHAFITCOIFEHDLEMIATORTOCCOEEAFBOCYOIAUYC |
| xorshift128 | mod29 | 120862 | LP2-01 | beaufort | True | 4.59 | 3.84 | -2.1 | OAHAAHUNGOAEETHCPRUOIANGXOSGINENINGRTFTHPUNGFBEFDR |
| xorshift64 | mod29 | 99813 | LP2-00 | sub | True | 4.58 | 3.65 | -1.8 | YREIANCGONGHSRTHIWFNWFNRRAPPEDROIDNAOGCRBMBUWUYIPA |
| xorshift128 | top | 199034 | LP2-01 | add | False | 4.73 | 3.61 | -2.6 | IACEABTHDUUITONOWLTOEMIENGIAYHELSNWHYEDTHTHLHLBECL |
| splitmix64 | top | 67145 | LP2-00 | sub | True | 4.66 | 3.54 | -2.0 | ANGDLIELFUOUILPRIEIAGOYRHNSTTHPWMRNEAELTOCNGNLIAOC |
| xorshift128 | top | 165963 | LP2-02 | beaufort | True | 4.60 | 3.51 | -1.6 | HCNDIMFGSARFGARIOXTHDOUETHHPNPDNEWTXLUMNNIHJSNDHES |
| pcg32 | top | 34827 | LP2-00 | add | True | 4.53 | 3.50 | -0.7 | TROTHIBNGIATERTTPDYIADPDUSEPIIHOPHHPTHOSEHSISRLOGE |
| xorshift32 | top | 104519 | LP2-00 | sub | False | 4.71 | 3.46 | -1.7 | GPENNGNGSHGUUDWOTTTEGWRITHOOUOIRYOLTUSTLHFDEOOISID |
| minstd48271 | mod29 | 219270 | LP2-00 | beaufort | True | 4.56 | 3.08 | 0.5 | BNGTHWWIXFSLODRNEHMNGCMUHAEOWNLPEATENENNOPLPWEODBL |
| xorshift32 | top | 104519 | LP2-00 | sub | True | 4.92 | 3.07 | -1.8 | GPENNGNGSHGUUDWOTTTEGWRITHOOUOIRYOLTUSTLHFDEOOISID |
| xorshift128 | rej | 186411 | LP2-00 | beaufort | True | 4.87 | 2.89 | -0.5 | THEEANPEWFUERTTSFORAXTHEMSFSNIIANIERHATLHNEAITSNEH |
| splitmix64 | top | 192541 | LP2-00 | add | True | 4.58 | 2.72 | 1.1 | EEAULEEAINIATSNGWSIACHWBNGPEEPLDRECWDDPUTFFMINGRNG |
| xorshift32 | mod29 | 49318 | LP2-00 | add | True | 4.54 | 2.69 | -1.1 | USTHUNGNOEFWETRTHDTAHOWOIATJCDDITHTITIIFTSTEWSSHCA |
| pcg32 | top | 20614 | LP2-01 | beaufort | True | 4.53 | 2.67 | -0.6 | INAPNGHEOAHMAEOSNETHFCDTRURLTHFFWYWGEALIAOETHIAATH |

## Candidates

None.

Largest tier-2 z_uni: 4.72; largest z_5: 1.68. Runtime, longest shard: 122 minutes on 7 shards.

