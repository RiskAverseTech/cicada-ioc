# Cross-library lane: pnotisdev's 1439 keystreams under this repository's three decoders

Library rebuilt from their generator definitions (`src/pnotisdev_library.py`, manifest `data/processed/pnotisdev_library_manifest.tsv`): 580 non-periodic streams of 20,000 values and 859 periodic ones. Streams swept: 1439.
(stream, offset) rows: plain 11,419,175, echo 11,419,175, hold 588,835 (hold: periodic streams at every offset, non-periodic at offsets 0-999).
Tier 1 (first 80 runes of LP2-00/01/02, 160 for hold; 3 signs x 2 F): plain 205,545,150, echo 205,545,150, hold 10,599,030 window decodes; survivors at z >= 4.5: 293. Tier 2: 293 full-page decodes (three decoders each). Candidates: 0. Rule in the module docstring.

## Controls

| decoder | stream | offset | sign | F | tier-1 z (rank) | outranked by | tier-2 z_uni | z_5 | free − base | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| plain | sha256-ctr mod :7 | 18399 | sub | False | 6.1 (2) | own offset +1 | 11.9 | 55.0 | +0.0 | no |
| plain | md5-ctr mod :firfumferenfe | 8828 | add | False | 5.3 (1) | — | 11.6 | 47.6 | +0.0 | yes |
| plain | sha256-chain reject :firfumferenfe | 14862 | beaufort | False | 6.2 (1) | — | 13.1 | 60.2 | +0.0 | yes |
| plain | sha256-chain mod :question all things | 9986 | sub | True | 6.6 (1) | — | 13.8 | 39.4 | +0.0 | yes |
| plain | kw:LIBERPRIMUS | 3 | add | True | 5.5 (1) | — | 14.4 | 46.1 | +0.0 | yes |
| plain | kw:BEHAUIARS | 3 | beaufort | True | 6.8 (1) | — | 15.4 | 47.9 | +0.0 | yes |
| echo | sha256-chain reject :emergence | 14102 | sub | False | 6.7 (1) | — | 11.5 | 72.7 | +0.0 | yes |
| echo | sha512-ctr mod :some wisdom | 17761 | add | False | 5.3 (1) | — | 10.7 | 59.5 | +0.0 | yes |
| echo | sha256-chain reject :3301 | 2177 | beaufort | False | 6.1 (1) | — | 11.6 | 61.4 | +0.0 | yes |
| echo | sha256-chain mod :DIVINITY | 11201 | sub | True | 6.3 (1) | — | 14.7 | 55.1 | +0.0 | yes |
| echo | kw:MASTER HE | 4 | add | True | 6.6 (1) | — | 13.8 | 47.3 | +0.0 | yes |
| echo | kw:RIGHT THERE | 7 | beaufort | True | 6.9 (1) | — | 15.3 | 55.1 | +0.0 | yes |
| hold | sha256-ctr reject :question all things | 527 | sub | False | 10.2 (4) | own offset -4; own offset -3; own offset -1 | 13.1 | 14.5 | +262.7 | no |
| hold | sha256-chain mod :Cicada 3301 | 874 | add | False | 6.9 (1) | — | 7.8 | 5.4 | +165.0 | yes |
| hold | sha512-ctr mod :FIRFUMFERENFE | 31 | beaufort | False | 9.9 (2) | own offset +1 | 13.5 | 8.9 | +231.1 | no |
| hold | sha256-chain reject :the totient functio | 845 | sub | True | 9.1 (1) | — | 11.7 | 13.2 | +170.7 | yes |
| hold | kw:NUMBERS FOR | 5 | add | True | 7.0 (1) | — | 9.3 | 7.3 | +96.6 | yes |
| hold | kw:INNOCENCE | 8 | beaufort | True | 7.5 (2) | own offset -2 | 8.1 | 6.6 | +117.2 | no |

Controls passing: 14 of 18 (plain 5/6, echo 6/6, hold 3/6).

## Tier-1 survivors (top 25 by tier-2 z_uni of the finding decoder)

| decoder | stream | offset | page | sign | F | tier-1 z | tier-2 z_uni plain / echo / hold | z_5 | free − base | transliteration |
|---|---|---|---|---|---|---|---|---|---|---|
| hold | sha512-ctr mod :command your own self | 178 | LP2-02 | sub | True | 4.94 | -0.99 / -1.19 / 5.87 | -0.3 | +163.6 | ECTHSTTHUSDMBRLRUOEUAOEODISEOHWOHUGWTHAOAUSFESEBNA |
| hold | sha512-ctr mod :command your own self | 178 | LP2-02 | sub | False | 4.96 | -0.85 / -1.00 / 5.74 | -0.3 | +183.0 | ECTHSTTHUSDMBRLRUOEUAOEODISEOHWOHUGWTHAOAUSFESEBNA |
| hold | composites | 70 | LP2-02 | sub | True | 4.76 | 1.50 / 1.50 / 5.28 | -2.5 | +120.4 | PHEAUBATHRTDAOGENHTTOHELUEOLPAHNEAIRIATSHNLABSEECA |
| hold | sha512-ctr mod :all things should be enc | 643 | LP2-02 | add | False | 4.65 | 1.71 / 1.74 / 5.27 | -0.6 | +130.7 | REUTADSIOYSMTRBETBETEOOLUEOIAOAHEEAODTDHSEEUTHXTEO |
| hold | primes from 3301 | 713 | LP2-02 | add | True | 4.81 | -1.47 / -1.38 / 5.27 | -1.2 | +169.3 | WEIHHSELDEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPON |
| hold | sha512-ctr reject :INSTAR | 702 | LP2-02 | sub | False | 5.00 | 1.05 / 0.98 / 5.24 | -1.6 | +143.6 | CMUETHAEADHAWNNHEHCNSEOAWHEOLASYWMWNHTEITHRTEEIANL |
| hold | primes from 3301 | 712 | LP2-02 | add | True | 4.76 | -0.44 / -0.51 / 5.21 | -1.3 | +152.1 | UMSHSYREFEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPON |
| hold | primes from 3301 | 713 | LP2-02 | add | False | 4.72 | -1.15 / -1.11 / 5.21 | -1.2 | +187.9 | WEIHHSELDEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPON |
| hold | primes from 3301 | 711 | LP2-02 | add | True | 4.73 | -0.37 / -0.42 / 5.19 | -1.4 | +150.8 | EIASHSYREFEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPO |
| hold | composites | 70 | LP2-02 | sub | False | 4.76 | 0.85 / 1.07 / 5.16 | -2.7 | +146.7 | PHEAUBATHRTDAOGENHTTOHELUEOLPAHNEAIRIATSHNLABSEECA |
| hold | primes from 3301 | 712 | LP2-02 | add | False | 4.67 | 0.13 / 0.06 / 5.15 | -1.3 | +162.3 | UMSHSYREFEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPON |
| hold | primes from 3301 | 711 | LP2-02 | add | False | 4.64 | -0.74 / -0.82 / 5.13 | -1.3 | +179.4 | EIASHSYREFEBWUEHRNLRIOTDETRTHOOEEAWNNRRNTHSIDORJPO |
| hold | sha512-ctr reject :INSTAR | 703 | LP2-02 | sub | False | 4.87 | 1.18 / 1.11 / 5.12 | -1.2 | +140.6 | OMTHTAEADHAWNNHEHCNSEOAWHEOLASYWMWNHTEITHRTEEIANLE |
| hold | sha512-ctr mod :AN END | 574 | LP2-02 | add | True | 5.36 | -0.06 / -0.17 / 5.11 | -1.2 | +145.0 | OLEECLOHDSETHURBEARNSEDLWEIAHEHTHUSROOOCSRYNTRTRIU |
| hold | sha512-ctr reject :INTUS | 581 | LP2-02 | sub | True | 5.83 | -0.60 / -0.80 / 5.08 | -1.7 | +153.6 | NMRNTIONYILMUERNREETWAIEROTRSESWTHRIHITHTOEXBEFDET |
| hold | sha256-chain reject :INSTAR | 362 | LP2-02 | add | True | 4.51 | -0.43 / -0.55 / 5.07 | 0.0 | +151.3 | EOSHUMATAHANOROGCTSINDAWEOTPIYWASWAFNTHCWNSCBOWOOO |
| hold | sha512-ctr mod :all things should be enc | 643 | LP2-02 | add | True | 4.61 | 0.81 / 0.92 / 5.04 | -0.6 | +130.8 | REUTADSIOYSMTRBETBETEOOLUEOIAOAHEEAODTDHSEEUTHXTEO |
| hold | sha512-ctr reject :INSTAR | 702 | LP2-02 | sub | True | 4.95 | 0.91 / 0.81 / 5.02 | -1.7 | +129.0 | CMUETHAEADHAWNNHEHCNSEOAWHEOLASYWMWNHTEITHRTEEIANL |
| hold | sha512-ctr mod :AN END | 574 | LP2-02 | add | False | 5.36 | 0.29 / 0.65 / 4.99 | -1.3 | +156.8 | OLEECLOHDSETHURBEARNSEDLWEIAHEHTHUSROOOCSRYNTRTRIU |
| hold | md5-ctr mod :LIBER PRIMUS | 148 | LP2-00 | beaufort | True | 4.73 | 0.91 / 0.84 / 4.97 | 0.7 | +152.7 | EHUWDMTHECMATEHTGNGENOEERGNIEESEOENIUTHEAGIEUBIIAP |
| hold | sha512-ctr reject :INSTAR | 700 | LP2-02 | sub | False | 4.70 | 0.33 / 0.32 / 4.96 | -1.3 | +156.7 | EJPETHAEADHAWNNHEHCNSEOAWHEOLASYWMWNHTEITHRTEEIANL |
| hold | md5-ctr mod :LIBER PRIMUS | 148 | LP2-00 | beaufort | False | 4.57 | 1.11 / 1.08 / 4.96 | 0.7 | +182.1 | EHUWDMTHECMATEHTGNGENOEERGNIEESEOENIUTHEAGIEUBIIAP |
| hold | sha512-ctr reject :INTUS | 581 | LP2-02 | sub | False | 5.84 | -0.63 / -0.78 / 4.95 | -1.8 | +175.0 | NMRNTIONYILMUERNREETWAIEROTRSESWTHRIHITHTOEXBEFDET |
| hold | catalan G digits (base 29) | 175 | LP2-02 | add | False | 5.27 | 1.94 / 1.76 / 4.91 | -1.0 | +124.4 | ROANTUCESHBNIEBNEIWNGUDLOUENOAHLOHEERUIMRRTAHSOOUE |
| hold | md5-ctr reject :0x7A35090F | 180 | LP2-02 | add | True | 4.72 | 2.59 / 2.51 / 4.91 | -0.7 | +101.0 | NTHIORFEDESAWISUDEAWDCMAADTNMTHSEOHIMRHTEHOTLLOFCF |

## Candidates

None.

Largest tier-1 z per decoder: plain 5.28, echo 5.14, hold 5.84. Largest tier-2 z_uni: 5.87; largest z_5: 2.58.
Runtime, longest shard: 13.0 hours on 3 shards.

