# Phase 9 sweep: cumulative-Gematria ciphertext feedback, and global streams with no per-page reset

Family A: 1827 configurations (3 value maps × 3 index maps × base stream totient/prime at offsets 0..100 or none); family B: 6 streams × 13,501 global offsets; 3 signs; 55 pages; 2 F variants: **27,334,890 tests**. Chance maximum about 5.9.
Per page, variant and decoder mode the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.

## Planted controls

| control | key | sign | F | z | rank in family | runes recovered |
|---|---|---|---|---|---|---|
| control-00 | A prime-sum → p_S mod 29 + totient@0 | add | False | 11.5 | 1 | 1.000 |
| control-01 | B totient@75 | sub | False | 11.4 | 1 | 1.000 |
| control-02 | A prime-sum → p_S mod 29 + totient@99 | beaufort | False | 12.5 | 1 | 0.967 |
| control-03 | B prime gap@6574 | add | True | 12.7 | 1 | 0.967 |
| control-04 | A index-sum → sum mod 29 + prime@31 [first run: offset sign bug, superseded by redo rows] | sub | True | 0.8 | 545 | 0.046 |
| control-05 | B lucas@12308 | beaufort | True | 13.7 | 1 | 1.000 |
| control-06 | A totient-sum → sum mod 29 + prime@96 | add | False | 11.5 | 1 | 0.983 |
| control-07 | B totient@11589 | sub | False | 10.9 | 1 | 0.996 |
| control-08 | A index-sum → sum mod 29 + prime@86 | beaufort | False | 11.8 | 1 | 1.000 |
| control-09 | B prime gap@5226 | add | True | 13.5 | 1 | 1.000 |
| control-10 | A index-sum → phi(p_S) mod 29 + totient@24 [first run: offset sign bug, superseded by redo rows] | sub | True | -0.5 | 1396 | 0.037 |
| control-11 | B lucas@1927 | beaufort | True | 11.7 | 1 | 0.958 |
| control-12 | A index-sum → p_S mod 29 + totient@65 | add | False | 11.6 | 1 | 1.000 |
| control-13 | B totient@4793 | sub | False | 11.9 | 1 | 1.000 |
| control-14 | A prime-sum → p_S mod 29 + totient@92 | beaufort | False | 12.3 | 1 | 1.000 |
| control-15 | B prime gap@11659 | add | True | 13.0 | 1 | 1.000 |
| control-16 | A totient-sum → phi(p_S) mod 29 + prime@92 [first run: offset sign bug, superseded by redo rows] | sub | True | -0.6 | 1311 | 0.037 |
| control-17 | B lucas@11761 | beaufort | True | 14.0 | 1 | 0.992 |
| redo-00 | A prime-sum → p_S mod 29 + totient@0 | sub | False | 12.0 | 1 | 1.000 |
| redo-01 | B lucas@13267 | sub | True | 14.2 | 1 | 0.988 |
| redo-02 | A totient-sum → sum mod 29 + prime@19 | sub | False | 10.6 | 1 | 0.983 |
| redo-03 | B totient@12201 | sub | True | 12.3 | 1 | 0.983 |

Controls recovered at z ≥ 6 and rank 1: 19 of 19 (z 10.6–14.2). The three rows marked *offset sign bug* are the first run's family-A `sub` controls: the decoder was given the cumulative offset un-negated for that sign, so family A × sub was effectively testing C = P + O − K. The sign was fixed, family A × sub was rerun for every page and both F variants with fresh nulls, and the four `redo-*` rows are its new controls.

## Unsolved pages: top 20 configurations overall

| page | family | sign | F | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|
| LP2-40 | B | add | True | totient@11571 | 5.44 | -1 | STHRCIAEIAIAHEWNFDMURPSEHNCHFBTLDLNHDGSDDMWEWRWFFTHOGYGOTHEADPAAEARGTIOAJANBTLOEATHLSTHIPIJ |
| LP2-42 | B | add | False | prime@9941 | 5.42 | 2 | SBGIETHUJHOSLEFOHERYJRTHNTHMTHNHLNNGCINBETAUEATHUAEDPRIEOONEAMNNSANUABREAONGXSEYRPENPAUPPD |
| LP2-42 | B | add | True | prime@9941 | 5.37 | 2 | SBGIETHUJHOSLEFOHERYJRTHNTHMTHNHLNNGCINBETAUEATHUAEDPRIEOONEAMNNSANUABREAONGXSEYRPENPAUPPD |
| LP2-40 | B | add | True | totient@11572 | 5.35 | -2 | FTHRCIAEIAIAHEWNFDMURPSEHNCHFBTLDLNHDGSDDMWEWRWFFTHOGYGOTHEADPAAEARGTIOAJANBTLOEATHLSTHIPIJ |
| LP2-01 | B | beaufort | True | prime gap@8392 | 5.26 | 2 | BHLTAYNGWOEAMLMPIEEATAGYTHLXTHLNCFMSMHNGBRIDUEOTHLOSTAEEMLDXREAWRSAETRATHTDJWXNGCIHNIEAONGOTHBT |
| LP2-05 | B | sub | True | prime gap@4698 | 5.20 | 1 | EGTEMFNGNFNGRHLGNJEAOAOPENEIAMPLAELIIOTHLSPXLOIALOTHAOTDTIAYJRINEHLLOTLDAEGCLOWFXTHEAIAFFOFF |
| LP2-42 | B | add | False | prime@9942 | 5.09 | 1 | YJFGDFEEATHEALLEFOHERYJRTHNTHMTHNHLNNGCINBETAUEATHUAEDPRIEOONEAMNNSANUABREAONGXSEYRPENPAUPPD |
| LP2-05 | B | sub | True | prime gap@4697 | 5.04 | 2 | HIAINGRDOEENGRHLGNJEAOAOPENEIAMPLAELIIOTHLSPXLOIALOTHAOTDTIAYJRINEHLLOTLDAEGCLOWFXTHEAIAFFOFF |
| LP2-28 | B | sub | True | prime+1@8082 | 5.02 | 2 | IANGTHANRCIFLRSYCTHPBCSMDNIEIGUHLYIAEUMYUBCRCLGTHNGCNCTHNYMROEYEOWPGBAEAOOBEFEBNNOAHYDWBF |
| LP2-55 | B | sub | True | prime@2019 | 5.01 | 3 | LUYRONGHNSPLYTMMITDEEWMEELTHEYEEODAIMPYOFGRYESNGNSDHIRTWWNXBELYRPINRRNGWYAGIEWLE |
| LP2-42 | B | add | True | prime@9943 | 4.97 | 0 | LCUNNCFEONDEOXLFHERYJRTHNTHMTHNHLNNGCINBETAUEATHUAEDPRIEOONEAMNNSANUABREAONGXSEYRPENPAUPPD |
| LP2-45 | B | add | True | prime gap@11164 | 4.94 | 8 | AFHTYHAFINTRNEAOFMSPIWLSTSTGTHALAXLTYOBNAENGHENDIUWCNXJRLRWTHPPIAGARWNGOYEYTHNWTHENINDEM |
| LP2-47 | B | beaufort | True | prime gap@3902 | 4.90 | 7 | BTHIYJSHWHTHDFONGTIADAIOTHEAEUANGHBGIRROEHMIOUPLTOATDRSSCLWPONGLGEFNEADRIRYEACREIAXEAOLIAEJNGP |
| LP2-13 | B | sub | True | prime+1@7573 | 4.88 | -3 | DTHFDYOMAEDGODLNAFNTWUREUTHPOUEUFOTHEWEEYDATWXXDIAUEOTHFOPTHNDCCNGNGSPTNEWXUNWPTHBDCHTDTHO |
| LP2-13 | B | sub | True | prime+1@7572 | 4.87 | -2 | UMFDYOMAEDGODLNAFNTWUREUTHPOUEUFOTHEWEEYDATWXXDIAUEOTHFOPTHNDCCNGNGSPTNEWXUNWPTHBDCHTDTHO |
| LP2-48 | B | add | True | prime gap@13477 | 4.82 | 2 | MORSCDMBYAERRIAANGNDNGACIAEMDUTHIALNFEALNGHEGNGXCLSTMEIAHWTDNMOWYPSYMRPIALEUHNGSYUHLEAEOUCIEPC |
| LP2-26 | B | sub | False | prime+1@8821 | 4.77 | 10 | DWMSDOYEYBGTFEABEAOAAEPTHFEOMLCSOXIABWANGTOEREANPEUAEIANGENGMEDNSUYTHTEAITNGNGWYABYIRTXTHYTPIA |
| LP2-32 | B | beaufort | True | prime gap@3085 | 4.76 | 1 | JCIOIUCGUUAGNEAEIASAERBCFIAAHTHBITHFOTHROESBEAAASFXLEIRSBJICIMRNYTHTHUHIIEAEUHRODNUTECWONGIA |
| LP2-01 | B | beaufort | True | prime gap@8393 | 4.75 | 1 | DFEOEOTBRNWONGIPSEEOEEAEMBHRIHJEAAEIRNGDFIABRFPNFTHLOSTAEEMLDXREAWRSAETRATHTDJWXNGCIHNIEAONGOTHBT |
| LP2-11 | B | sub | True | prime gap@11348 | 4.75 | 6 | IMDANGIASODLPESMHERUPPSGRCEBBOSEOTHEAADEAAHCNDTHFWYWBNADAULHYNGUBFBFGWJMDCFIAUERXRUELWEADO |

Largest z per family: A 4.38; B 5.44.

Largest z over all 27,334,890 tests: 5.44 (LP2-40, family B, add, totient@11571).

## Verdict

**No page decrypts.** Keys driven by the cumulative Gematria value of the preceding ciphertext (three value maps, three index maps, with the totient or prime stream at 101 offsets or alone), and the book's six streams run continuously through the book at every offset up to 13,500, under the soft reject-on-repeat rule, three signs and both F variants, are excluded at the sensitivity the controls demonstrate. Not covered: cumulative sums of the plaintext (an autokey the Viterbi state cannot carry), sums that include the current rune, or streams outside these six.

