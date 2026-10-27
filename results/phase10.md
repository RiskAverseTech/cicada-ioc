# Phase 10: unknown-position uniform nulls under a hard anti-repeat skip rule

Free-null decoder (a uniform null allowed at every rune, log prior -0.80 per null, i.e. an implied rate of 0.31, chosen on the planted controls before any page was scored: priors −3.0, −2.0, −1.27 (= ln(0.22/0.78)), −0.8 and −0.4 recovered 8, 11, 14, 15 and 14 of 18 controls at z ≥ 6 and rank 1); 22863 configurations (phase 3 book families and phase 4 phrase keys, three sign conventions) x 55 pages x 2 F variants = **2,514,930 tests**; chance maximum about 5.4.
Per page, F variant and decoder mode the null is 2,000 random keystreams through the same free-null decoder. Pre-registered hit rule: z >= 6 over that null AND free-null score minus base score for the same configuration >= 20 nats AND readable English.

## Planted controls (hard rule, nulls at 0.15 / 0.22 / 0.30; decoder prior fixed at -0.80)

| control | sign | family | key | F | page | null rate | nulls | free-null z | rank | free − base (nats) | base-decoder z | runes recovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | sub | phrase-2 | DOGMA SO | False | LP2-00 | 0.15 | 31 | 10.7 | 1 | +166.7 | 3.3 | 0.861 |
| control-01 | add | phrase-4-rev | THE MASTER REPLIED THEN ʳ | False | LP2-03 | 0.22 | 46 | 5.2 | 1 | +180.8 | -0.1 | 0.673 |
| control-02 | beaufort | phrase-3 | THE MASTER SAID | False | LP2-06 | 0.3 | 40 | 7.3 | 1 | +136.5 | 1.8 | 0.801 |
| control-03 | sub | primes+1 | p[n+60]+1 | False | LP2-09 | 0.15 | 40 | 12.7 | 1 | +243.0 | 0.6 | 0.842 |
| control-04 | add | vigenere-word | SHED | False | LP2-12 | 0.22 | 42 | 11.9 | 1 | +187.7 | 2.4 | 0.799 |
| control-05 | beaufort | primes | p[n+62] | False | LP2-15 | 0.3 | 38 | 3.1 | 13 | +112.9 | 0.7 | 0.669 |
| control-06 | sub | sentence | THE CIRCUMFERENCE PRACTICES TH | False | LP2-18 | 0.15 | 28 | 12.0 | 1 | +218.3 | 0.9 | 0.875 |
| control-07 | add | phrase-3-rev | A LESSON THE ʳ | False | LP2-21 | 0.22 | 48 | 11.2 | 1 | +194.9 | 2.3 | 0.809 |
| control-08 | beaufort | phrase-2 | DEEP WITHIN | False | LP2-24 | 0.3 | 63 | 10.2 | 1 | +198.6 | 1.9 | 0.604 |
| control-09 | sub | fibonacci | F[n+0] | True | LP2-27 | 0.15 | 33 | 10.9 | 1 | +137.8 | 2.4 | 0.801 |
| control-10 | add | self running key | plaintext@2662 | True | LP2-30 | 0.22 | 50 | 10.9 | 3 | +198.7 | -0.9 | 0.657 |
| control-11 | beaufort | affine position | 18·n+1 | True | LP2-33 | 0.3 | 44 | 6.4 | 1 | +134.0 | 1.4 | 0.676 |
| control-12 | sub | phrase-4 | DO NOT HAVE ENOUGH | True | LP2-36 | 0.15 | 28 | 8.3 | 1 | +99.8 | 4.6 | 0.795 |
| control-13 | add | phrase-2-rev | PRESERVE THINGS ʳ | True | LP2-39 | 0.22 | 38 | 8.6 | 1 | +108.3 | 3.8 | 0.673 |
| control-14 | beaufort | sentence | IT IS THE BEHAVIORS OF CONSUMP | True | LP2-42 | 0.3 | 70 | 8.0 | 1 | +209.7 | -0.8 | 0.629 |
| control-15 | sub | vigenere-word | CAN | True | LP2-45 | 0.15 | 35 | 13.6 | 1 | +100.2 | 6.8 | 0.851 |
| control-16 | add | primes | p[n+79] | True | LP2-48 | 0.22 | 55 | 10.6 | 1 | +194.5 | 1.0 | 0.745 |
| control-17 | beaufort | square position | n²+15 | True | LP2-52 | 0.3 | 65 | 8.4 | 1 | +191.2 | 0.6 | 0.788 |

Controls recovered at z >= 6 and rank 1: 15 of 18; the base decoder (no nulls) would have scored them at z -0.9 to 6.8.

## Unsolved pages: top 20 configurations overall

| page | sign | F | family | key | z | free − base | key lag | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|---|
| LP2-14 | add | False | self running key | plaintext@366 | 5.64 | +99.5 | -21 | WTHUEEOAOCDWDRLCNOENYAEOOGEINEAFORCNGERTAEAENIAUTLTHWPDEUORTOANNTHOHSOUCYRTOAENGEETIXNGXTH |
| LP2-14 | add | False | self running key | plaintext@367 | 5.42 | +117.2 | -22 | WJUEEOAOCDWDRLCNOENYAEOOGEINEAFORCNGERTAEAENIAUTLTHWPDEUORTOANNTHOHSOUCYRTOAENGEETIXNGXTH |
| LP2-43 | add | True | primes+1 | p[n+36]+1 | 5.39 | +151.2 | -45 | NGUREATYCFEUORFIERNDLEWOEFAEEEEFYANHCTHFEGDARFETWAIPCTMNAEIATHTRONOTNJETHLEDDRFAOOEOEEON |
| LP2-43 | add | True | primes+1 | p[n+38]+1 | 5.29 | +159.7 | -47 | THJIAATYCFEUORFIERNDLEWOEFAEEEEFYANHCTHFEGDARFETWAIPCTMNAEIATHTRONOTNJETHLEDDRFAOOEOEEON |
| LP2-14 | add | True | self running key | plaintext@366 | 5.27 | +84.6 | -21 | WTHUEEOAOCDWDRLCNOENYAEOOGEINEAFORCNGERTAEAENIAUTLTHWPDEUORTOANNTHOHSOUCYRTOAENGEETIXNGXTH |
| LP2-43 | add | False | primes+1 | p[n+36]+1 | 5.23 | +175.1 | -45 | NGUREATYCFEUORFIERNDLEWOEFAEEEEFYANHCTHFEGDARFETWAIPCTMNAEIATHTRONOTNJETHLEDDRFAOOEOEEON |
| LP2-43 | add | False | primes+1 | p[n+38]+1 | 5.14 | +183.6 | -47 | THJIAATYCFEUORFIERNDLEWOEFAEEEEFYANHCTHFEGDARFETWAIPCTMNAEIATHTRONOTNJETHLEDDRFAOOEOEEON |
| LP2-52 | add | True | phrase-3 | MERELY WHAT YOU | 5.11 | +145.1 | -46 | OEDISNTBDNSYSODOEHBTAOEWTOREEWPLEACROTNEEATHTYTHRMRITNCFDREWNTEAEMJOERECERUWTINEWFCETG |
| LP2-14 | add | True | self running key | plaintext@367 | 5.06 | +90.3 | -22 | WJUEEOAOCDWDRLCNOENYAEOOGEINEAFORCNGERTAEAENIAUTLTHWPDEUORTOANNTHOHSOUCYRTOAENGEETIXNGXTH |
| LP2-52 | add | False | phrase-3 | MERELY WHAT YOU | 5.03 | +158.1 | -46 | OEDISNTBDNSYSODOEHBTAOEWTOREEWPLEACROTNEEATHTYTHRMRITNCFDREWNTEAEMJOERECERUWTINEWFCETG |
| LP2-21 | sub | False | phrase-2 | EXCEPT WHAT | 4.98 | +192.1 | -48 | TLIIEEAASDAOEUYTEEAMEEAUAHTOLONIEOAIEAETYNYCGASIALOTHSAELTBIHEAECEMOEERIEUJTHRIAAEETRGWYI |
| LP2-24 | add | False | self running key | plaintext@2114 | 4.89 | +175.3 | -53 | OMOWTLECHAUETLWMSTTAEAANPNATYIROWOAAESEADANGICEITHDONUUDIAITHEUSPDSOUMRXOEETEMEOOMON |
| LP2-21 | sub | True | phrase-2 | EXCEPT WHAT | 4.84 | +165.6 | -48 | TLIIEEAASDAOEUYTEEAMEEAUAHTOLONIEOAIEAETYNYCGASIALOTHSAELTBIHEAECEMOEERIEUJTHRIAAEETRGWYI |
| LP2-04 | sub | True | phrase-4 | ULTIMATELY YOU WILL DISCOVER | 4.82 | +162.4 | -40 | MWIOASWOTMLNONARWOORWHBNWNEUEDAGNGLTEITHUMAFRINTHTXDFIIDTHNHTCOHRDSDMTINOLSBAHAWILIY |
| LP2-05 | sub | False | phrase-3-rev | WHAT YOU DO ʳ | 4.77 | +179.2 | -46 | UTHXHJATLOEYSOENTHEGDESHUOFWDSEGCCXSXREACTUIBIORTEOEELSTHWNLRNXPOONTCEOEAOLSFEAAYEOICS |
| LP2-24 | add | False | self running key | plaintext@2115 | 4.72 | +175.5 | -54 | NROWTLECHAUETLWMSTTAEAANPNATYIROWOAAESEADANGICEITHDONUUDIAITHEUSPDSOUMRXOEETEMEOOMON |
| LP2-05 | beaufort | True | affine position | 2·n+4 | 4.72 | +134.4 | -60 | FIDTHUEYLESUOENFTHDEAEAHESDTUNSDIFXIXANTHRTHORDAEOUEOCTNERDULATAATRORNGWPEIOWFEOAEOOIRNHT |
| LP2-17 | sub | False | affine position | 17·n+11 | 4.70 | +219.3 | -52 | NOYMIOBUISANMSTHEOANGTTTOIAAEOYEWULLNYEEEUIAWHATHCYCEERFETERWFTHECPRNGAPSEOSIATELTAIXCAN |
| LP2-17 | add | False | affine position | 12·n+18 | 4.70 | +219.3 | -52 | NOYMIOBUISANMSTHEOANGTTTOIAAEOYEWULLNYEEEUIAWHATHCYCEERFETERWFTHECPRNGAPSEOSIATELTAIXCAN |
| LP2-05 | sub | True | phrase-3-rev | WHAT YOU DO ʳ | 4.70 | +163.0 | -46 | UTHXHJATLOEYSOENTHEGDESHUOFWDSEGCCXSXREACTUIBIORTEOEELSTHWNLRNXPOONTCEOEAOLSFEAAYEOICS |

Largest z over all tests: 5.64. Cells meeting the pre-registered rule (z >= 6 and free − base >= 20): 0.
Largest z per sign: sub 4.98; add 5.64; beaufort 4.72.
Wall time, longest shard: 48 minutes on 4 shards.

## Verdict

**No page decrypts with free nulls under the hard skip rule.** A hard anti-repeat rule on this repository's key families, all three sign conventions and both F variants, with uniform null runes at unknown positions at the rate the doublet count implies, is excluded at the sensitivity the controls demonstrate. Not covered: non-uniform nulls, null rates far from 0.22 (the controls bracket 0.15 to 0.30), nulls that consume a key value, key streams outside these families.

