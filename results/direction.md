# Numbers as directions (lane D1, instrument 2)

Registration: `results/d1_registration.md`.

## Part A, keyless: the word's own number as its direction

432 configurations (number source × function × application × sign × F) on the 55 pages. Chance level (8640 configuration-sets on uniform pages): largest median page 5-gram z 0.94, largest page 5.34. Largest median here **0.60**, largest page 5.91, largest z\* 10.34. Hits: **0**.

| source | number | applied as | sign | F | median page z5 | best page z5 | best page | z\* | text |
|---|---|---|---|---|---|---|---|---|---|
| self | prod29 | shift | add | 1 | 0.60 | 2.63 | LP2-26 | 6.16 | EONEAOIAEJPIADYNDNGHFSAXBBRIANIYRTHEIAWLTHEFEWFEOX |
| prev | prod29 | solved | sub | 1 | 0.51 | 3.18 | LP2-52 | 5.13 | EFUELWUIASDEOTHEMMPEOFAFBLEOCTHOERIMNGNGNGPECDMIMI |
| self | tot29 | prime p+1 | beaufort | 0 | 0.49 | 2.99 | LP2-34 | 3.17 | FHPEUNGHOGOEDBOEWOEXNFNGAUHXXIAEOMNPLTRNWEAWIARULO |
| self | argmax | solved | sub | 1 | 0.49 | 3.61 | LP2-44 | 8.85 | RDEPGOEGLCOXCOEEOSNGPIOEONAEPONYOAEFJAEWTFLLFMRLCH |
| self | prod29 | prime p-1 | sub | 1 | 0.47 | 2.47 | LP2-51 | 8.27 | XHEOFAETHWYRBCIANSOATFAETHSRACIAJMOESIDEACOEHJOGFR |
| prev | len | shift | sub | 1 | 0.46 | 2.43 | LP2-01 | 5.27 | AIMSNIBEAAETHISOEXTBPWSCHYAEDMFPEAMIAFLHRIEGFEUFAE |
| self | prod29 | shift | add | 0 | 0.45 | 2.88 | LP2-02 | 3.15 | EAAERTHIOIAGNDOCFCENHBEGEOPIYTHBOOENMFHJCJNJEOEWNX |
| prev | len | prime p-1 | add | 0 | 0.44 | 2.57 | LP2-31 | 3.01 | OWNGIAYYXEOHYWGBARIAYOYYTHLCATHTWGGULUDGOEGOIANGHA |
| prev | tot29 | solved | sub | 1 | 0.43 | 2.57 | LP2-46 | 6.50 | PNMNGUMPDFAGPFNGRIMRTHMCCHEOTLWFXWXIAXAEGHJJIAEINL |
| prev | tot29 | prime p+1 | beaufort | 1 | 0.42 | 1.84 | LP2-33 | 6.39 | NNGEAIFSWYTHHEIFRGHRXSFPBMJOECEANTEABTPPLEAGOEOETR |
| self | prod29 | shift | sub | 0 | 0.42 | 2.89 | LP2-11 | 4.50 | JEAETHHENLNGTHNIEALUWONGPINFMUGNMEAPEORNYIAWCTYBRE |
| self | prod29 | shift | sub | 1 | 0.40 | 2.80 | LP2-11 | 6.05 | JEAETHHENLNGTHNIEALUWFNGPINFMUGNMEAPEORNYIAWCTYBRE |

## Part B, the solved words as the map

7 schemes × 726 alignments × 55 pages × 3 signs × 2 F; **1,677,060 window decodes** under the free-null decoder; tier 1 at z ≥ 4.5 on 160 runes, tier 2 at z_uni ≥ 6 above the full-page null maximum and readable (free − plain reported, not required: amendment in the registration).

| control | scheme | page | sign | F | planted alignment | top | z1 | rank | z2 | free − plain | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | word-shift | LP2-07 | sub | 0 | 66 | 66 | 9.3 | 1 | 11.0 | +15 | yes |
| control-01 | word-shift | LP2-30 | add | 1 | 52 | 52 | 9.9 | 1 | 14.7 | +5 | yes |
| control-02 | word-prime p | LP2-12 | beaufort | 0 | 503 | 503 | 3.7 | 1 | 8.1 | +22 | no |
| control-03 | word-prime p | LP2-44 | sub | 1 | 500 | 500 | 5.7 | 1 | 9.8 | +58 | yes |
| control-04 | cumulative | LP2-20 | add | 0 | 692 | 692 | 10.6 | 1 | 14.1 | +26 | yes |
| control-05 | cumulative | LP2-51 | beaufort | 1 | 308 | 308 | 5.3 | 1 | 5.5 | +0 | no |

Controls passing: 4 of 6. Largest tier-1 z 5.58; survivors 48; candidates **0**.

None. No accepted decoding within the tested configurations at the stated detection limits.

| scheme | page | sign | F | alignment | z1 | z2 | free − plain | above null max | transliteration |
|---|---|---|---|---|---|---|---|---|---|
| word-solved | LP2-15 | add | 0 | 119 | 5.6 | 5.54 | +100 | yes | `ALSCTHNYPSFOAADILRTHCIRHEROEAEEOAEUUCOIBIAOADFNN` |
| word-solved | LP2-15 | add | 1 | 119 | 5.2 | 5.49 | +74 | yes | `ALSCTHNYPSFOAADILRTHCIRHEROEAEEOAEUUCOIBIAOADFNN` |
| word-prime p+1 | LP2-03 | sub | 0 | 199 | 4.7 | 5.06 | +117 | yes | `TASORCHISANYEIPYNNRMTHITMPFSOENNSEAWTTHULUOLEADY` |
| word-solved | LP2-15 | beaufort | 1 | 709 | 5.2 | 4.98 | +91 | yes | `FREMHHFIGXHADISMNIONDNHHULDEHSEEEOUPAOHAITHMTPTH` |
| word-solved | LP2-15 | beaufort | 0 | 709 | 4.8 | 4.88 | +106 | yes | `CUEMHHFIGXHADISMNIONDNHHULDEHSEEEOUPAOHAITHMTPTH` |
| word-prime p+1 | LP2-15 | beaufort | 0 | 2 | 4.6 | 4.85 | +96 | yes | `CHARCODRATAIACERETRNGRRUMRWJWSETHRLIANWWMNGEAOSH` |
| word-prime p+1 | LP2-03 | sub | 1 | 199 | 4.8 | 4.85 | +95 | yes | `TASORCHISANYEIPYNNRMTHITMPFSOENNSEAWTTHULUOLEADY` |
| word-prime p+1 | LP2-55 | beaufort | 1 | 524 | 4.8 | 4.83 | +41 | yes | `GYCAITHGEMAFIATHOFSSBNSWENRSNNTHAYAHUHNREEAOFCET` |
| word-prime p | LP2-25 | beaufort | 0 | 407 | 4.7 | 4.81 | +181 | yes | `TNGWLDXYAODHSNRJSLNUTHHOABRGDNLOESRSATNCOAIAGTTH` |
| word-prime p+1 | LP2-55 | beaufort | 0 | 524 | 4.9 | 4.71 | +39 | yes | `GYCAISBORSLOTILEUEBCPNENRSNNTHAYAHUHNREEAOFCETCL` |
| word-prime p+1 | LP2-37 | add | 1 | 594 | 5.0 | 4.63 | +117 | yes | `ALTXNEXIDWAASBPEAWEWOAODEASRUDSEEONYOIHMIUINHIEO` |
| word-prime p+1 | LP2-15 | beaufort | 1 | 2 | 4.6 | 4.63 | +64 | yes | `CHARCODRATAIACERETRNGRRUMRWJWSETHRLIANWWMNGEAOSH` |
| word-solved | LP2-32 | beaufort | 0 | 293 | 4.6 | 4.54 | +77 | yes | `MAWDXSYBMHATWTYOUEWODUTHIBSTDAOUUHIGRHEDIEHLTANE` |
| word-prime p | LP2-55 | add | 0 | 720 | 4.6 | 4.42 | +58 | yes | `IATMIWEUITHRDMAWWMDYTHTUTHDCHXUTTHEOGDUSASONWUAD` |
| stream | LP2-19 | beaufort | 1 | 378 | 4.8 | 4.36 | +37 | yes | `CONCTHDRFRDCIAWRITSWHYSTHRHOEAISTRCTSIAEADNGTRNL` |

## Registered predictions

- D1 (plants): 4 of 6 → fails.
- D2 (no tier-2 candidate): 0 → holds.
- D3 (no Part A hit): 0 → holds.

Runtime, longest map shard: 0.5 h. Reading: README §75. Part A at chance; Part B null with 4 of 6 plants (the two misses located at rank 1 at the planted alignment, below the bar), so D1 fails as written and the detection limit on the prime-offset and cumulative schemes is partial. The solved text parsed into 726 words; alignments 0–725 are every start. [stated — the tables]

Reproduce: `STAGE=chance|keyless|map|merge .venv/bin/python -I src/direction_lane.py`.
