# Short-list lane: the hypothesis loop's surviving finite families under the skip decoder

Families and sizes: A lcg mod 3301 (9,902 keystreams, signs add/sub/beaufort, rejection one); B lcg mod 1033 (1,033 keystreams, signs add/sub/beaufort, rejection one/two); C lcg mod 29 (21,953 keystreams, signs add/sub/beaufort, rejection one); D word keys with clock multiplier (1,624 keystreams, signs add/sub/beaufort, rejection one); E prime-gap stream with clock multiplier (82,824 keystreams, signs add, rejection one); F prime_value ciphertext feedback over the book text (2,977 keystreams, signs add/sub/beaufort, rejection one/two); F totient_value ciphertext feedback over the book text (2,977 keystreams, signs add/sub/beaufort, rejection one/two).
225,183 configurations per page x 55 pages x 2 F variants = **24,770,130 tests** (55 of 55 pages done); chance maximum about 5.8. Per page, F variant, decoder mode and rejection mode the null is 2,000 random keystreams through the same decoder. Pre-registered rule: z >= 6 over that null and readable English.

Decoder: `decode_lane` in `src/shortlist_lane.py`, score.decode's Viterbi with a per-position multiplier inverse and a feedback-corrected ciphertext; identical to score.decode without the hooks (asserted at run time). The random-keystream null is unchanged by either hook (checked on one page at run time, see `results/shortlist.log`).

## Planted controls (soft skip 0.81, two per family)

| family | sign | F | rejection | planted key | z of true key | rank in family | runes recovered | best z in family |
|---|---|---|---|---|---|---|---|---|
| A lcg mod 3301 | add | False | one | lcg3301(a=7,c=1)@2500 | 10.7 | 2 | 1.000 | 10.7 |
| A lcg mod 3301 | sub | True | one | lcg3301(a=1033,c=0)@2665 | 14.1 | 1 | 0.992 | 14.1 |
| B lcg mod 1033 | sub | True | one | lcg1033(a=202,c=29)@737 | 12.8 | 1 | 0.992 | 12.8 |
| B lcg mod 1033 | beaufort | False | two | lcg1033(a=202,c=29)@95 | 10.9 | 1 | 1.000 | 10.9 |
| C lcg mod 29 | beaufort | False | one | lcg29(a=23,c=7)@4 | 10.6 | 1 | 1.000 | 10.6 |
| C lcg mod 29 | add | True | one | lcg29(a=16,c=11)@5 | 11.8 | 1 | 0.954 | 11.8 |
| D word keys with clock multiplier | add | True | one | FIRFUMFERENFE m=(((3i+19) mod 28)+1) | 13.3 | 1 | 1.000 | 13.3 |
| D word keys with clock multiplier | sub | False | one | DIVINITY m=(((14i+17) mod 28)+1) | 10.1 | 1 | 1.000 | 10.1 |
| E prime-gap stream with clock multiplier | add | False | one | gap[n+87] m=(((11i+26) mod 28)+1) | 11.1 | 1 | 1.000 | 11.1 |
| E prime-gap stream with clock multiplier | add | True | one | gap[n+55] m=(((4i+11) mod 28)+1) | 13.8 | 1 | 0.971 | 13.8 |
| F prime_value ciphertext feedback over the book text | beaufort | True | one | plaintext@589 | 12.3 | 1 | 1.000 | 12.3 |
| F prime_value ciphertext feedback over the book text | add | False | two | plaintext@1994 | 11.8 | 1 | 0.996 | 11.8 |
| F totient_value ciphertext feedback over the book text | add | False | one | plaintext@234 | 11.2 | 1 | 0.979 | 11.2 |
| F totient_value ciphertext feedback over the book text | sub | True | two | plaintext@1752 | 11.7 | 4 | 0.938 | 12.9 |

Controls recovered at z >= 6 and rank 1: 12 of 14.

## Unsolved pages: top 25 configurations overall

| page | family | sign | F | rejection | key | z | skips | transliteration (first 80 runes) |
|---|---|---|---|---|---|---|---|---|
| LP2-33 | B lcg mod 1033 | sub | True | two | lcg1033(a=202,c=29)@241 | 5.21 | 6 | NMRLOLHLBSMNSOMETHITHCCNNGDIFBATORDLPGRUNCTEISOEFIAFPRDMBNJNFNGISDITRBCYTHWNIOENGSWNUHFLN |
| LP2-52 | E prime-gap stream with clock mult | add | True | one | gap[n+28] m=(((11i+26) mod 28)+1) | 5.15 | 1 | IFOYWTTUIBIABETHSHNGESFTSRAEILXCNPDTPPOWSFNREFGTHDEAWHOTHUCUSUWIAHNWENIWHGJEOTHCTOYGPCYYU |
| LP2-52 | E prime-gap stream with clock mult | add | True | one | gap[n+27] m=(((11i+26) mod 28)+1) | 5.14 | 2 | NBOYWTTUIBIABETHSHNGESFTSRAEILXCNPDTPPOWSFNREFGTHDEAWHOTHUCUSUWIAHNWENIWHGJEOTHCTOYGPCYYU |
| LP2-33 | B lcg mod 1033 | sub | True | two | lcg1033(a=202,c=29)@160 | 4.99 | 5 | UTHFHFLHLBSMNSOMETHITHCCNNGDIFBATORDLPGRUNCTEISOEFIAFPRDMBNJNFNGISDITRBCYTHWNIOENGSWNUHFLN |
| LP2-05 | E prime-gap stream with clock mult | add | True | one | gap[n+34] m=(((24i+18) mod 28)+1) | 4.99 | -3 | DNGPNGCTHEAFAMWUPOGUDSNGWDMOMUEEYRWFPIEYDOPIAJENGPOJJNHAEOTHJNDETLOSFIAPPFUTHJAIAELWTHYWFSBL |
| LP2-20 | E prime-gap stream with clock mult | add | True | one | gap[n+89] m=(((22i+11) mod 28)+1) | 4.81 | 5 | HAWDEETMEPMGANCDSYIBICGFIATHAEGTUBUTJYOIATMYYFFAPDBGAIHTNOPWXUSNSJGMIUFFXRDDXEAWSLEFS |
| LP2-05 | E prime-gap stream with clock mult | add | True | one | gap[n+60] m=(((17i+20) mod 28)+1) | 4.79 | 7 | HRARPSBMFSTHDRAERGCNEATHARMFSMOETHGIFWEMOEONEEWYWMODDLPLRRSNTBPAATIOIATAAEGCXLTCYIRPEYFTH |
| LP2-15 | E prime-gap stream with clock mult | add | True | one | gap[n+66] m=(((21i+20) mod 28)+1) | 4.77 | 5 | HESXCEWPCYEAEIIREONOEOEAGHWCAUGTHTHMNGWSYCMNSNGEOPOTHNGYRWETHAAINRGMIPGSNCLEAEJGETEADARGTOJAF |
| LP2-04 | E prime-gap stream with clock mult | add | True | one | gap[n+4] m=(((20i+26) mod 28)+1) | 4.73 | 2 | LEEOETAEWLMAFAEBOLGOSNGAYHLGFCLGDCFEOCAESRUMHEMANOHOEATHXTERNGUONEFHNLFFFOINGYNYEADIIEWIEJ |
| LP2-20 | E prime-gap stream with clock mult | add | True | one | gap[n+87] m=(((22i+11) mod 28)+1) | 4.73 | 7 | HTOLEGTMEPMGANCDSYIBICGFIATHAEGTUBUTJYOIATMYYFFAPDBGAIHTNOPWXUSNSJGMIUFFXRDDXEAWSLEFS |
| LP2-15 | E prime-gap stream with clock mult | add | True | one | gap[n+67] m=(((21i+20) mod 28)+1) | 4.72 | 4 | FESXCEWPCYEAEIIREONOEOEAGHWCAUGTHTHMNGWSYCMNSNGEOPOTHNGYRWETHAAINRGMIPGSNCLEAEJGETEADARGTOJAF |
| LP2-27 | E prime-gap stream with clock mult | add | True | one | gap[n+95] m=(((2i+23) mod 28)+1) | 4.71 | -1 | NMCUADAEASUSIGIOCETOEAHGTHTRUCCYMWEBLGFHAATDTHOENGATHRIAOTDIENHCEMOUYFUNFGACDSEETHHFDSATB |
| LP2-19 | E prime-gap stream with clock mult | add | True | one | gap[n+16] m=(((20i+0) mod 28)+1) | 4.70 | 5 | WRBPTBDNGRUUTHWHHIETWTHTHENGAAEFHRNGCASWFNGPOWPYEASHJTONGRTHRESGDELAEHAEAAEMIAFNIDNGHLOSCDYAEFRI |
| LP2-19 | E prime-gap stream with clock mult | add | True | one | gap[n+16] m=(((20i+28) mod 28)+1) | 4.70 | 5 | WRBPTBDNGRUUTHWHHIETWTHTHENGAAEFHRNGCASWFNGPOWPYEASHJTONGRTHRESGDELAEHAEAAEMIAFNIDNGHLOSCDYAEFRI |
| LP2-45 | A lcg mod 3301 | sub | True | one | lcg3301(a=3,c=0)@2094 | 4.67 | 5 | EADGNTYMRULDEAIANPBIAPALCUUNCJYTGFRFYCIGEEAJDWOWGSILEOUMBRHIAPFPDOSSRFAEJRCWWGPPLCNNTHMEO |
| LP2-45 | A lcg mod 3301 | sub | True | one | lcg3301(a=3,c=0)@2981 | 4.65 | 4 | YBWBGUYGWNMGFSYFIAPALCUUNCJYTGFRFYCIGEEAJDWOWGSILEOUMBRHIAPFPDOSSRFAEJRCWWGPPLCNNTHMEO |
| LP2-15 | D word keys with clock multiplier | add | True | one | FIRFUMFERENFE m=(((4i+6) mod 28)+1) | 4.62 | -1 | FSOUUIEAPSRAJMNGWBEPFEAPIMAMLEFTSRTOOAYERPBIAAMPTGPYIICESYSNNGULTHFUIMIIFLSLASYUUSNGWH |
| LP2-02 | F totient_value ciphertext feedbac | sub | True | one | plaintext@1307 | 4.62 | 5 | AEOOCAROGOSCTHLLXFJCIBEDUHRNCMSBSSUDRPYRUCITNEOTRCRHSLRNYRLINTXLNGOHFONGIMIAAEJTRSDWHGR |
| LP2-01 | E prime-gap stream with clock mult | add | True | one | gap[n+62] m=(((27i+4) mod 28)+1) | 4.62 | 5 | RTHCSOAMFDGPIAHAIGJPPDIEOFBSFIAAHPENIAEIAOTHFBUFRGNGEGROWOTCLAEEAUTCUHOTHWDYEOIAICTUUAEAGEAFTHT |
| LP2-19 | A lcg mod 3301 | sub | False | one | lcg3301(a=1033,c=0)@329 | 4.61 | 10 | OTCYXLYRPTPTIHBUNFGHEANGUGSOEULTEFNGRMYWGDLITHXEOIAEWHHWPSDGIAOEEASNBEGROAMNGEFMNWOEOETHWAB |
| LP2-40 | E prime-gap stream with clock mult | add | True | one | gap[n+100] m=(((25i+11) mod 28)+1) | 4.57 | 6 | RIWHFREDCCAEATFDANGREACTHARRMBBIAUSXPFJHTNUTWRPIJHPNGUUWLLWATHIAOIAPNGONNGDTBSYATPUCMLTHONAES |
| LP2-33 | F totient_value ciphertext feedbac | beaufort | True | one | plaintext@292 | 4.57 | 0 | OERNGTNDSLCWWIYOEIOEDXCAFWOYEEUONDPNGTHAHGTAWOIAYOETHCTBEFEOBHIADDHDAENUHAIOTBTHILFSSHTTAN |
| LP2-03 | E prime-gap stream with clock mult | add | True | one | gap[n+18] m=(((17i+9) mod 28)+1) | 4.55 | 4 | MIRATHCTHDEPUFYEGGMTHWFIMRYTENGOFETHOXDOEWRTENCAERIANMXMAUOCOOBNXESESEUMWXRUFIMOUHLITRF |
| LP2-00 | C lcg mod 29 | beaufort | True | one | lcg29(a=12,c=26)@19 | 4.55 | 1 | WNGHTTIEAMWOHUAAHTRFSYMLBPJMTHCJYIMCEPRLNLNGNIATNIIEAAUOEOCGPUAFSLFRNPFPEUOCCAOETHNGDDG |
| LP2-46 | F prime_value ciphertext feedback  | sub | True | one | plaintext@337 | 4.55 | 5 | EACAHIPNSFRHYHISSWOEUPITHWRPNFAENGAPANGROURLUNLEYNGDYEPCUUAYONBHTYYWNGYTHHWPUGDMUBTIRATY |

## Per family: largest z over all pages

| family | largest z | page | key |
|---|---|---|---|
| A lcg mod 3301 | 4.67 | LP2-45 | lcg3301(a=3,c=0)@2094 |
| B lcg mod 1033 | 5.21 | LP2-33 | lcg1033(a=202,c=29)@241 |
| C lcg mod 29 | 4.55 | LP2-00 | lcg29(a=12,c=26)@19 |
| D word keys with clock multiplier | 4.62 | LP2-15 | FIRFUMFERENFE m=(((4i+6) mod 28)+1) |
| E prime-gap stream with clock multiplier | 5.15 | LP2-52 | gap[n+28] m=(((11i+26) mod 28)+1) |
| F prime_value ciphertext feedback over the book text | 4.55 | LP2-46 | plaintext@337 |
| F totient_value ciphertext feedback over the book text | 4.62 | LP2-02 | plaintext@1307 |

Largest z over all 24,770,130 tests: 5.21 (LP2-33, B lcg mod 1033, 'lcg1033(a=202,c=29)@241').

## Verdict

**No page decrypts.** The six families the hypothesis loop left standing (LCG seeds mod 3301, 1033 and 29; the two published word keys and the prime-gap stream with every clock multiplier; Gematria prime-value and totient-value ciphertext feedback over the book's own text at every offset), under the soft reject-on-repeat rule at the stated sign conventions and both F variants, are excluded at the sensitivity the controls demonstrate.

Wall time 69 min (longest shard).

## Hand-over note (for the README owner)

**Relation to phase 8** (`src/phase8_lane.py`, `results/phase8.md`, README §18, commit 6ab49be). Phase 8 ran after this lane was written and overlaps families A–D: the same LCG parameter sets at every seed and the same two word keys under position-walking multipliers. This lane was written independently (its own decoder hook, `decode_lane`, with the multiplier inverse and the feedback correction applied inside the Viterbi; phase 8 used `score.py`'s `mult_inv`), casts a somewhat wider net in those families (812 multiplier schedules against 784; mod 29 at every a in 2..28 and every c rather than a = 2, c = 24 alone; mod 1033 under both rejection widths; the sub sign throughout), and reaches the same answer: A 4.67, B 5.21, C 4.55, D 4.62 against phase 8's 4.51, all inside the chance range of their test counts. Treat A–D here as an independent replication of phase 8, not a new result.

**What is new here** is what phase 8 did not run:

- **E, the prime-gap stream with every clock multiplier.** Key = (p_{n+o+1} − p_{n+o}) mod 29 at offsets 0..100 and 3301, combined as C = m_i·P + K with m_i = ((a·i + b) mod 28) + 1 over all 812 schedules, sign add, rejection one: 82,824 keystreams per page. Largest z 5.15 (LP2-52, gap[n+28], m = ((11i+26) mod 28)+1, gibberish). Null.
- **F, Gematria-value ciphertext feedback over the book's own text.** K_i = f(C_{i−1}) + T_{i+o}, with f the rune's prime value or the totient of that prime, T the 2,977 runes of verified solved-page plaintext at every offset, three signs, rejection one and two: 2 × 2,977 keystreams per page. Largest z 4.55 (prime value) and 4.62 (totient), both gibberish. Null. This is the finite, running-text form of the loop's top-ranked feedback proposals; the LCG-based forms (86k–96k configurations each) remain unrun.

Whole run: 24,770,130 tests, chance maximum about 5.8, largest z 5.21, no transliteration readable. Controls: 14 plants at z 10.1–14.1, 12 ranked first. The two that were not: the family A add/no-F plant tied at z 10.7 with another seed of the same generator (rank 2, all runes recovered), and the totient-feedback plant under skip-by-two with the F rule (rank 4 at z 11.7, 0.938 of runes), the known double-rejection desync of the skip-by-two mode (README §16); both sit far above the z ≥ 6 line.

Text to merge into README.md as the next section (adjust the number):

```markdown
## 1x. Short-list lane: phase 8 replicated, prime-gap multiplier and feedback families added (`src/shortlist_lane.py`, `results/shortlist.md`)

A second, independently written sweep of the hypothesis loop's short list (§17), run as three page shards. Families: the LCG seed sets of phase 8 at a wider parameter net (mod 3301 with three (a, c) pairs; mod 1033 under skip-by-one and skip-by-two; mod 29 at every a in 2..28 and every c), the two solved word keys under all 812 position-walking multipliers, and two families phase 8 did not run: the prime-gap stream (p_{n+o+1} − p_{n+o}, offsets 0..100 and 3301) under every multiplier schedule, and Gematria prime-value or totient-value ciphertext feedback added to the book's own plaintext at all 2,977 offsets. Soft reject-on-repeat, three signs, both F variants, 225,183 configurations per page: **24,770,130 tests**, chance maximum about 5.8, pre-registered rule z ≥ 6 and readable English. The decoder hook (multiplier inverse and feedback correction inside the Viterbi) is asserted identical to `score.decode` without hooks, and the random-keystream null is unchanged by it.

**Controls.** Fourteen plants, two per family, spanning sign, rejection width and F variant: all recovered at z 10.1–14.1, twelve ranked first (one tied at rank 2 with an equivalent seed, one skip-by-two plant at rank 4, the §16 desync).

**Result: null.** Largest z over all tests 5.21 (LP2-33, LCG mod 1033 seed 241 under skip-by-two, gibberish); per family 4.55–5.21. The LCG and word-key families replicate phase 8's null with a separate decoder; the prime-gap stream under every clock multiplier and the prime-value and totient-value feedback over the book's text are excluded for the first time. Still unrun from the loop's list: feedback over an LCG base (86k–96k configurations each). Wall time 69 minutes on three cores.
```

Files written by this session for this lane: `src/shortlist_lane.py`; `results/shortlist.md`, `results/shortlist.json`, `results/shortlist.log` (merged); `results/shortlist_shard{0,1,2}.json` and `.log` (per-shard inputs to `--merge`, keep if the merge is to be re-run); `results/shortlist_singlecore_start.log` (the abandoned single-core start, safe to delete). README.md untouched; nothing committed.

Reproduce: `.venv/bin/python -I src/shortlist_lane.py --shard I 3` for I in 0, 1, 2 (controls and the decoder checks run in shard 0), then `--merge`.
