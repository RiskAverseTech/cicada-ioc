# Status box

| | |
|---|---|
| **Breakthroughs** | **0** (a page decoding to readable English at a pre-registered bar, reproduced by someone else) |
| Decoder tests run | 421 million, all pre-registered, all with planted controls |
| Lanes closed null | 22 of 34 (none running) |
| Pages | 55 unsolved with runes (12,956 runes); coverage limits listed per lane |
| The structures | three: 86 doubled runes where 445 are expected (0.19 of uniform; solved pages sit at 0.86); inside words, a lag-5 equality carried by S (z +3.7, K-fixed null) and a lag-6 relation c = 24 − 2c′ (z +5.1); flat in every other statistic |
| Best current reading | one word-aware rule that removes repeats and leaves the two echoes (pnotisdev's mech25 fits one); the echoes are the first implementation leaks |
| External reviews adopted | 2 (2026-10-27), 8 corrections, no fact overturned |
| Repository | 46 numbered sections, 43 commits as of 2026-10-28 |

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
| §44 | Irrational digits (pi, e, sqrt 2, phi; three readings) under the soft rule, offsets to 30,000 | 6.5 M | 4/4 | null | base-10, digit pairs, base-29; fresh offset per page |

## Open

- Filler (null) lane on LP2-49, LP2-55, LP2-51: below power at any rule tried
- Mixed alphabets under the other labs' key families (external texts, PRNG seeds): the quagmire lane covered the book's own keys only
- Phase 9 mechanisms on the nine short pages
- 149 unread positions of the blind re-reading (merged ᚳ pairs, drop caps): a better splitter or the eye
- Red-text key schedule (the red initials and first words), ledger check first
- wazar's R12-C2 esoteric texts: Dukotah R26-B ran 33 of them at 4–8 offsets, sign −1 only (pages 20/22/25/27/29, sign +1, reversed texts unrun; Gutenberg ids wrong)
- LP2-50, the two-character-code page, as a cipher of its own
- A word-aware mechanism that yields the deficit, the lag-5 S echo (now: lag-5 runs), the lag-6 relation together; a rule that copies plaintext equality at lag 5 without copying differences is the shape the data ask for (§46)
- Phase 6 (§14) and §39's phase-6 part under the corrected word edges (rerun 2026-10-28, see §42)

## Value so far

- Every exclusion above is reproducible from `src/` with a planted control that shows the test can see a solution; that is what the other 2026 ledgers mostly lack.
- Instrument gains this week: bounded multi-rejection decoder, power curves by page length, a rune 5-gram that lifts short-page detection from 21 % to 99 %, an exact every-offset running-key scanner, an image lane.
- `results/ledger_diff.md` lets a new idea be checked against five labs' prior work in minutes.

*Generated by `src/status.py`; the lane table is maintained by hand in that file, the counts are read from `results/`.*
