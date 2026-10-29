# The filler sweep (§55 part C): external running-key texts and pnotisdev's remaining offsets under the free-null decoder

Decoder: free-null at prior -2.2 (part B: power 0.75 at 230 runes for running keys with fillers at 0.10). Key material: 10 texts at every offset in both directions (239,876 runes), 6 longer texts at 22,960 sentence starts (forward), and 580 non-periodic pnotisdev streams at offsets 1,000–1,999: 1,082,712 offsets in 692 work units. Tier 1: first 160 runes of LP2-00/01/02 × 3 signs × 2 F = 18 cells per offset, **19,488,816 window decodes**; survive at z ≥ 4.5. Tier 2: full page, candidate at z_uni ≥ 6 and free − plain ≥ 20 nats and readable. Chance maximum of z over 19,488,816 tests about 5.8.

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
| lady_fountain_guest | False | LP2-00 | beaufort | False | 6261 | 5.78 | 6.07 | +133 | NEFLAEAIERNGLASAPOIAACSWGSAGMRWOTHYIEESANIOTTHNEMENEOLTNOEAB |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | True | 1417 | 4.93 | 6.00 | +117 | AEXUOTHANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHAW |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | False | 1417 | 4.93 | 5.90 | +143 | AEXUOTHANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHAW |
| pn:sha256-ctr reject :INTUS | False | LP2-00 | beaufort | False | 1858 | 5.74 | 5.76 | +128 | EIPYHMATHWWNHCIAIGWEAYUSTCEATDGIABDTIUHDOICPUTHETHOYEMCATEAO |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | True | 1418 | 4.63 | 5.74 | +123 | SAEUUOTHANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHA |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | False | 1418 | 4.65 | 5.64 | +186 | SAEUUOTHANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHA |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | True | 1420 | 4.52 | 5.64 | +106 | NMEHOBANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHAWT |
| rune_poem | False | LP2-00 | beaufort | False | 17079 | 5.46 | 5.56 | +141 | SUTYIJSPOWSEEEWNAEOENSNTCFNUNTHILANGUSAEOPCEWWEMOXGIEAEEDTTI |
| pn:sha256-ctr mod :program your mind | False | LP2-02 | beaufort | False | 1420 | 4.54 | 5.54 | +131 | NMEHOBANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHAWT |
| lady_fountain_guest | False | LP2-00 | beaufort | False | 6263 | 5.17 | 5.53 | +163 | OSEOAEAIERNGLASAPOIAACSWGSAGMRWOTHYIEESANIOTTHNEMENEOLTNOEAB |
| pn:sha256-chain reject :INTUS | False | LP2-02 | sub | True | 1625 | 4.83 | 5.53 | +74 | CLLHCWTIILEOHIBDUIRWROREABMISAANGDNGUOUIEEAMYEEWUWNGEBUIRDEU |
| pn:sha256-chain reject :INTUS | False | LP2-02 | sub | True | 1624 | 4.78 | 5.47 | +66 | BTHTHIACWTIILEOHIBDUIRWROREABMISAANGDNGUOUIEEAMYEEWUWNGEBUIR |
| pn:sha256-ctr reject :INTUS | False | LP2-00 | beaufort | False | 1859 | 5.42 | 5.47 | +152 | ODEYHMATHWWNHCIAIGWEAYUSTCEATDGIABDTIUHDOICPUTHETHOYEMCATEAO |
| bunyan_head | False | LP2-00 | add | False | 28082 | 4.90 | 5.39 | +152 | THDEDNYMOAYNECTHSNSTHFOEOFLAESOOEDORFAEIIAADGYERETHBEBHNCDCA |
| lady_fountain_guest | False | LP2-00 | add | False | 25920 | 5.83 | 5.36 | +136 | IEYNGIHHSERETSTHLPROMBEIYEDWACUUUISLNASRNEHFWTRREOTLNGTURODO |
| lady_fountain_bulfinch | True | LP2-02 | add | False | 12979 | 5.05 | 5.33 | +146 | IINGEIYEOLEANGLTHNOPHELIWYWIEERPSENUUWEYTOJCAEEHSHUASHSMDETN |
| rune_poem | False | LP2-00 | beaufort | False | 17080 | 5.20 | 5.32 | +142 | DYJPADSEEYSEEEWNAEOENSNTCFNUNTHILANGUSAEOPCEWWEMOXGIEAEEDTTI |
| lady_fountain_guest | False | LP2-00 | beaufort | True | 6261 | 5.51 | 5.32 | +96 | NEFLAEAIERNGLASAPOIAACSWGSAGMRWOTHYIEESANIOTTHNEMENEOLTNOEAB |
| pn:sha256-chain reject :INTUS | False | LP2-02 | sub | True | 1626 | 4.59 | 5.30 | +88 | DNUHCWTIILEOHIBDUIRWROREABMISAANGDNGUOUIEEAMYEEWUWNGEBUIRDEU |
| rune_poem | False | LP2-00 | beaufort | False | 17081 | 5.17 | 5.30 | +146 | MNGEPADSEEYSEEEWNAEOENSNTCFNUNTHILANGUSAEOPCEWWEMOXGIEAEEDTT |
| pn:sha256-chain reject :INTUS | False | LP2-02 | sub | True | 1623 | 4.59 | 5.30 | +66 | OXTHIACWTIILEOHIBDUIRWROREABMISAANGDNGUOUIEEAMYEEWUWNGEBUIRD |
| pn:sha512-ctr reject :1311 | False | LP2-00 | beaufort | False | 1383 | 4.58 | 5.28 | +131 | TOONOHCWWLPWHOJBRFUDSNSNRIBUTCURIENAEAARRHOUTSITGUEDSTHEDEME |
| pn:sha256-ctr reject :20140104 | False | LP2-02 | add | False | 1868 | 4.55 | 5.27 | +84 | THUTHOTRLRIALSUWAWOOOTEDYEAWPPBTHUTHIDOWUTHESITHLNITHHNGEFLT |
| pn:sha256-ctr reject :1729 | False | LP2-02 | add | True | 1206 | 4.97 | 5.27 | +110 | YEULSHHRRGTHELETHBGYARDWYYICTATUTHSNBSTHOTHAERMAETHUARFEAEDA |
| lady_fountain_guest | False | LP2-00 | beaufort | False | 6262 | 4.85 | 5.25 | +166 | JIELAEAIERNGLASAPOIAACSWGSAGMRWOTHYIEESANIOTTHNEMENEOLTNOEAB |

Survivors: 685; largest tier-1 z 5.96; largest tier-2 z_uni 6.07.

## Candidates

- **pn:sha256-ctr mod :program your mind** page LP2-02 beaufort F=True offset 1417: z_uni 6.00, free − plain +117: `AEXUOTHANAEDLOERLFUIEOEOOSOCDYMOEIDUDAARDHYTEUCTAUNUFAUNGHAWTHDRNOEOITOMTIGDTIOTRGUPN`
- **lady_fountain_guest** page LP2-00 beaufort F=False offset 6261: z_uni 6.07, free − plain +133: `NEFLAEAIERNGLASAPOIAACSWGSAGMRWOTHYIEESANIOTTHNEMENEOLTNOEABWPULREASNTHSETHSOWEBLEYNUNFE`

Coverage limits: window power at 160 runes from part B; the longer texts at sentence starts only; pnotisdev offsets ≥ 2,000; the free-null decoder at one prior. Runtime, longest shard: 4.8 h on 8 shards.
