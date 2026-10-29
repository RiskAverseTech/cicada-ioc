# Status box

| | |
|---|---|
| **Breakthroughs** | **0** (a page decoding to readable English at a pre-registered bar, reproduced by someone else) |
| Decoder tests run | 426 million, all pre-registered, all with planted controls |
| Lanes closed null | 24 of 39 (none running) |
| Pages | 55 unsolved with runes (12,956 runes); coverage limits listed per lane |
| The structures | 86 doubled runes where 445 are expected (0.19 of uniform; solved pages sit at 0.86); inside words, a lag-5 echo that copies equality in runs (102 vs 71 pairs, 9 vs 1.5 bigrams), 11 of the pairs S (3.5 expected, p 0.003), and a lag-6 relation c = 24 − 2c′ (77 vs 44); the two echoes share words; flat in every other statistic |
| Best current reading | a gated word-internal echo (plaintext repeat at lag 5 → copy the cipher rune; at lag 6 → 24 − 2c) in about half the words reproduces nine of ten statistics; the S weighting is outside every additive mechanism and is the open fact |
| External reviews adopted | 2 (2026-10-27), 8 corrections, no fact overturned |
| Repository | 51 numbered sections, 58 commits as of 2026-10-28 |

## Lanes

| § | lane | tests | controls | verdict | coverage limit |
|---|---|---|---|---|---|
| §1–3 | Key reuse between pages (IC, pooled offsets) | — | planted 12/12 | null, large-scale | clusters under ~12 pages not excluded |
| §4–7 | Doublet deficit and twenty constructions | — | — | 86 vs 445; soft re-draw 0.81 survives | mechanism inference, not a key |
| §9 | Phase 3: book streams + skip rule | 0.5 M | 20/20 | null |  |
| §12 | Phase 4: phrase and sentence keys | 2.0 M | 26/26 | null |  |
| §13 | Phase 5: Latin and Old English registers | 5.0 M | 24 (12 per register) | null |  |
| §14 | Phase 6: word-edge events | 10.1 M | 24/24 | null |  |
| §16 | Phase 7: skip-by-two rule | 2.5 M | 24 plants | null |  |
| §18 | Phase 8: LCG seeds, position multipliers | 1.7 M | 16/16 | null |  |
| §19 | Short-list lane (panel's finite families) | 24.8 M | 14 (12 rank 1) | null |  |
| §20 | Phase 9: Gematria feedback, global streams | 27.3 M | 18 (3 exposed a bug, fixed) | null |  |
| §22 | Phase 10: unknown-position nulls, hard rule | 2.5 M | 15/18 | null | inconclusive on 9 short pages (§23) |
| §24 | Short-page secondary rule, 9 pages | 2.5 M | A 39/45, B 31/45 | null | phase 3–4 library only |
| §25 | External running key, exact every offset | 153.1 M | 15/17 | null | 12 texts; edition differences near mid-page cost ~1 sigma per rune |
| §26 | Page images: container, chroma, geometry | 75 | 19 controls | null | archive JPEGs only |
| §27 | 5-gram rescoring of short pages | 2.5 M | A 39/45; B 6/45 (fillers break n-grams) | null | soft-rule exclusion now 99 % power on all 55 pages |
| §28 | Windowed dispersion (hand vs machine) | — | — | no power | recorded so it is not re-proposed |
| §29 | The two Know This magic squares as keys | 0.0 M | 8/8 | null | direct use only; seeds and indices open |
| §30 | Provenance: signed messages verify (2012, 2016, 2017) | — | 3 of 3 verify | genuine | the 2017 'hoax' claim is false |
| §31 | Seeded generators no ledger lists (8 PRNGs, 2^18 seeds) | 113.3 M | 8/8 | null | seeds above 2^18 and unnamed generators open |
| §32 | Keyword-mixed alphabets (quagmire I-IV) under the book's keys | 25.6 M | 7/8 (8th rank 2, equivalent alphabet) | null | book words and streams only; other labs' key families under mixed alphabets open |
| §33 | Where the 86 repeats sit | — | — | boundary-blind | excludes reset-chain ciphers and transcription artefacts |
| §34 | The 256-byte payload of LP2-49/50/51 as key (direct, pointer readings; +all 6 page orderings and base-59, 2026-10-28) | 0.1 M | 4/4 | null | replication; PRF expansions are wazar's negatives |
| §35 | Every archived artefact against the page-73 hash | 0.0 M | — | no match | public archives only |
| §36 | Planted-cluster power of the key-reuse test | — | 30 reps per cell | measured | ~20 aligned pages for 90 %; blind under key-skip |
| §37 | Repeat spectrum to lag 120, null models, boundary convention | — | — | deficit at lag 1 only |  |
| §38 | Blinded glyph re-reading of the unsolved pages | 0.0 M | 99.7 % held-out | 0 disagreements; 149 unread | pre-registered count criterion failed by the segmenter |
| §39 | Phases 6-8 on the nine short pages, 5-gram rule | — | 22/24, 24/24, 15/16 | null | phase 9 not yet carried there |
| §40 | Pilgrim texts (Bunyan, Chaucer) as running keys | 40.1 M | 3/3 | null | The Way of a Pilgrim not run (no free text) |
| §41 | Closure bundle: solved-page repeat rate, parity, repeat context, cross-page n-grams, word-length repeats, ICC | — | — | measured: rule specific to the unsolved section; all else at null | statistics, not decodes |
| §42 | Within-word echoes: lag-5 equality (S), lag-6 affine 24−2c; word-edge correction | — | — | measured: both present (z +3.7 K-fixed; z +5.1, best of 812) | two further laws of the stream; mechanism open |
| §43 | Exact reachability of the solved-page rule, every offset; linear complexity | 1.1 M | plants recovered | null: continuous section excluded for 5 streams; pages at n/2 complexity | per-page reachability has no power (literal-F realignment) |
| §45 | Word-aware mechanism simulation: 8 rules x 9 pre-registered statistics | — | 3 sanity controls | measured: every rule fails; the S carrier breaks all eight; R4+extra rune fits the other eight | English plaintext and iid key only; hold-aware decoding = §22 |
| §46 | Lag-5 echo runs in pairs (bigrams 9 vs 1.5); multiplier autokey and lag-1 affine closed; per-word period-5 key mixture | — | — | measured: f = 0.5 fits equality and S exactly, fails the difference flatness by 3 sd | first hypothesis producing the S carrier; lag 6 unexplained |
| §47 | Echo rules in the mechanism simulator (14 rules x 10 statistics) | — | 3 sanity controls | measured: gated lag-5/lag-6 echo (E56w) fits 9 of 10; S carrier outside every additive mechanism | English plaintext, iid key; one gate parameter fitted to one count |
| §48 | Echo-aware decoding (spent and held echoes) of the phase 3-4 library | 5.0 M | 11/12 | null | echoes cost an unaware decoder ~nothing when key-spending; held echoes cost only when several fall on one page |
| §49 | E56w out-of-sample predictions (8 statistics, 14 cells, committed before the look); echoes on the image-derived stream | — | — | measured: 14/14 cells hold; image stream reproduces 101 / 11 / 75 exactly | consistency, not confirmation; S weighting still outside the rule |
| §50 | S carrier: the eleven sites in the images; line-break dependence of the lag-5 echo; RS5 second traces | — | controls at lags 4, 6 | measured: nothing in ink; lag-5 echo 2x on line-wrapping pairs (z +2.2), lag 6 not; RS5 7/7 but near-unfalsifiable | post-hoc cut found by eye; eleven events |
| §51 | Layout follow-up to the line-wrap lead (split position, distance to line edge; registered before the check) | — | lag-4, lag-6 controls | null: no layout signature; wrap excess stands at z +2.2 and is not word length | a layout step is not supported |
| §44 | Irrational digits (pi, e, sqrt 2, phi; three readings) under the soft rule, offsets to 30,000 | 6.5 M | 4/4 | null | base-10, digit pairs, base-29; fresh offset per page |

## Open

- Filler (null) lane on LP2-49, LP2-55, LP2-51: below power at any rule tried
- Mixed alphabets under the other labs' key families (external texts, PRNG seeds): the quagmire lane covered the book's own keys only
- Phase 9 mechanisms on the nine short pages
- 149 unread positions of the blind re-reading (merged ᚳ pairs, drop caps): a better splitter or the eye
- Red-text key schedule (the red initials and first words), ledger check first
- wazar's R12-C2 esoteric texts: Dukotah R26-B ran 33 of them at 4–8 offsets, sign −1 only (pages 20/22/25/27/29, sign +1, reversed texts unrun; Gutenberg ids wrong)
- LP2-50, the two-character-code page, as a cipher of its own
- Key source, not key search: the page behind the AN END SHA-512 (the one place a key is said to exist) is unfound; archived onion corpora (Dukotah 2026-07-27), 1,962 documents (ItIsCuthNotCup), raw bytes/IPv4/phones (hashcat), 124,017 onion-capture digests (pnotisdev) and 502 artefacts x 3,977 readings here (§35) do not contain it; Tor v2 is gone, so only an archive nobody has indexed can
- Cross-library decoding: pnotisdev's 1,447 number streams have met only IoC/bigram screens and the R4 engine, the book's phrase library here only the skip Viterbi (+ §22 hold nulls, + §48 echoes); each library under the other lab's decoder is untested
- The S carrier (11 of 102 lag-5 pairs): a step acting on the written rune S, or a fluctuation; no additive mechanism carries it (§47); the lag-5 echo prefers line-wrapping words (§50) but shows no layout signature (§51): a fluctuation or an unnamed property of those words
- §39's phase-6 part (the nine short pages) under the corrected word edges: not rerun; §14's full rerun moved maxima by tenths of a sigma

## Value so far

- Every exclusion above is reproducible from `src/` with a planted control that shows the test can see a solution; that is what the other 2026 ledgers mostly lack.
- Instrument gains this week: bounded multi-rejection decoder, power curves by page length, a rune 5-gram that lifts short-page detection from 21 % to 99 %, an exact every-offset running-key scanner, an image lane.
- `results/ledger_diff.md` lets a new idea be checked against five labs' prior work in minutes.

*Generated by `src/status.py`; the lane table is maintained by hand in that file, the counts are read from `results/`.*
