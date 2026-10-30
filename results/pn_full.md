# pnotisdev's full keystream library at offsets 0–999 under the free-null decoder (`pn_full`)

Decoder: free-null at prior -2.2 (part B: power 0.75 at 230 runes for running keys with fillers at 0.10). Key material: 1439 pnotisdev streams (859 periodic, below their period only) at offsets 0–999: 588,835 offsets in 1439 work units. Tier 1: first 160 runes of LP2-00/01/02 × 3 signs × 2 F = 18 cells per offset, **10,599,030 window decodes**; survive at z ≥ 4.5. Tier 2: full page, candidate at z_uni ≥ 6 and free − plain ≥ 20 nats and readable. Chance maximum of z over 10,599,030 tests about 5.7.

## Controls (soft rule 0.81, fillers at 0.10, corpus text at a random offset)

| control | text | reversed | sign | F | planted offset | tier-1 top offset | tier-1 z | rank | tier-2 z_uni | free − plain | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | liber_al | False | sub | False | 22658 | 22658 | 10.4 | 1 | 13.6 | +210 | yes |
| control-01 | blake_mhh | True | add | False | 13501 | 13501 | 9.6 | 1 | 9.5 | +166 | yes |
| control-02 | rune_poem | False | beaufort | False | 5750 | 5749 | 8.8 | 1 | 13.8 | +223 | yes |
| control-03 | self_reliance | True | sub | True | 24400 | 24400 | 10.1 | 1 | 13.5 | +139 | yes |
| control-04 | lady_fountain_guest | False | add | True | 36309 | 36309 | 7.7 | 1 | 12.9 | +158 | yes |
| control-05 | lady_fountain_bulfinch | True | beaufort | True | 5714 | 5709 | 6.8 | 2 | 9.9 | +123 | no |

Controls passing: 5 of 6.

## Tier-1 survivors (top 25 by tier-2 z_uni)

| source | reversed | page | sign | F | offset | tier-1 z | tier-2 z_uni | free − plain | transliteration (first 60) |
|---|---|---|---|---|---|---|---|---|---|
| pn:md5-ctr reject :PILGRIM | False | LP2-02 | beaufort | False | 834 | 5.26 | 5.75 | +116 | OFTHLABAULHELEFHTLBSGROBSNURNMMWEARFTCASHSUTHEGBIDFSAEIENUDR |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | False | 394 | 5.04 | 5.74 | +135 | PUSUECOEORUBBBSLEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHB |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | True | 394 | 4.89 | 5.72 | +103 | PUSUECOEORUBBBSLEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHB |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | True | 433 | 6.83 | 5.62 | +112 | YTLUUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:p_n - n | False | LP2-02 | sub | True | 562 | 4.86 | 5.61 | +79 | OEACUDDSECEIEEEUPHLJMLUERAOEEAORWIRRTNLISTDLEMDTLGIITDUADTHW |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | False | 395 | 4.88 | 5.61 | +137 | SISUECOEORUBBBSLEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHB |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | True | 395 | 4.73 | 5.58 | +109 | SISUECOEORUBBBSLEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHB |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | False | 433 | 7.06 | 5.55 | +171 | YTLUUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | True | 432 | 6.74 | 5.54 | +112 | OMYCUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:md5-ctr reject :PILGRIM | False | LP2-02 | beaufort | False | 836 | 5.02 | 5.52 | +135 | INUOLRTHSTNTGYABAHNMTNCYCSIAAOHBSYTROHASHSUTHEGBIDFSAEIENUDR |
| pn:p_n - n | False | LP2-02 | sub | True | 563 | 4.72 | 5.48 | +84 | THDDSTDSECEIEEEUPHLJMLUERAOEEAORWIRRTNLISTDLEMDTLGIITDUADTHW |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | False | 397 | 4.72 | 5.48 | +152 | IMNSHETRORSILEAEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHBE |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | False | 432 | 6.97 | 5.47 | +162 | OMYCUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | True | 397 | 4.57 | 5.45 | +114 | IMNSHETRORSILEAEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTHBE |
| pn:sha512-ctr mod :INSTAR | False | LP2-02 | sub | False | 688 | 4.70 | 5.44 | +100 | RLEBTOLMWHAIREUAUPSANYBUAAMAIIWEARHGLEEAEAFRPUGIATERUNALNNED |
| pn:p_n - n | False | LP2-02 | sub | False | 562 | 4.94 | 5.44 | +91 | OEACUDDSECEIEEEUPHLJMLUERAOEEAORWIRRTNLISTDLEMDTLGIITDUADTHW |
| pn:emirps | False | LP2-02 | add | False | 964 | 5.09 | 5.44 | +83 | UNRMLIAAPBIFTAANWOLSNGJPOIDTHGLISECHLFNBCOTOEAORCNNHTHSYTDUB |
| pn:emirps | False | LP2-02 | add | True | 964 | 4.82 | 5.43 | +39 | UNRMLIAAPBIFTAANWOLSNGJPOIDTHGLISECHLFNBCOTOEAORCNNHTHSYTDUB |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | True | 434 | 6.57 | 5.39 | +120 | DITOUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:md5-ctr reject :PILGRIM | False | LP2-02 | beaufort | False | 835 | 4.85 | 5.36 | +107 | YMTHLABAULHELEFHTLBSGROBSNURNMMWEARFTCASHSUTHEGBIDFSAEIENUDR |
| pn:sha256-chain mod :deep web | False | LP2-01 | sub | False | 393 | 4.57 | 5.35 | +129 | HEAISCUTHDFINBBSLEEEANELSTTHTHIDNCYUNDILASAEILIEWLCSYGNGADTH |
| pn:md5-ctr reject :FIRFUMFERENFE | False | LP2-00 | add | False | 434 | 6.80 | 5.33 | +175 | DITOUESFAENSWCSTAEFDAOCSEUCEHRIOOFSFSYRECBRNSMLATHDNNYEBRIWT |
| pn:p_n - n | False | LP2-02 | sub | False | 563 | 4.80 | 5.32 | +95 | THDDSTDSECEIEEEUPHLJMLUERAOEEAORWIRRTNLISTDLEMDTLGIITDUADTHW |
| pn:sha512-ctr mod :INSTAR | False | LP2-02 | sub | True | 688 | 4.64 | 5.31 | +85 | RLEBTOLMWHAIREUAUPSANYBUAAMAIIWEARHGLEEAEAFRPUGIATERUNALNNED |
| pn:sha512-ctr mod :INSTAR | False | LP2-02 | sub | False | 689 | 4.53 | 5.28 | +97 | DWIDATEORDHAIREUAUPSANYBUAAMAIIWEARHGLEEAEAFRPUGIATERUNALNNE |

Survivors: 377; largest tier-1 z 7.06; largest tier-2 z_uni 5.75.

## Candidates

None. No accepted decoding within the tested configurations at the stated detection limits.

Coverage limits: window power at 160 runes from part B; pnotisdev offsets outside 0–999; the free-null decoder at one prior. Runtime, longest shard: 4.8 h on 8 shards.
