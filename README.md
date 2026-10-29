# Liber Primus (Cicada 3301): pre-registered cryptanalysis of the unsolved pages

**Status (2026-10-29; one-screen box in `STATUS.md`; everything of the book that has been read, set as a page, in `docs/liber-primus-as-read.html`).** Eight pre-registered analyses on the 56 unsolved pages, each with planted
controls, each a negative result reported as one; a three-model hypothesis loop gated on the pages'
own statistics (§17); and a ledger against the other public 2026 labs (`results/ledger_diff.md`).
The loop's remaining short-list families are swept in §19 (null); cumulative-Gematria ciphertext
feedback and the book's streams run globally with no per-page reset in §20 (null); §21 checks a
Quorum panel's claim that the remaining mechanisms are indistinguishable (they are not), and §22 sweeps
the one survivor that was still breakable, a hard rule with nulls at unknown positions (null). §23
records an external review of 2026-10-27 and what it changed: the z ≥ 6 rule reaches 80 % power
only at 92 runes under the soft rule and at 200 runes in the null lane, so exclusions on the 2 and 9
pages shorter than that are inconclusive, not negative; the decoder's rejection bound was raised;
two calibration statements were corrected. §24 runs a pre-registered secondary rule on those nine
pages over the phase 3–4 key library (null; it sees a planted soft-rule solution about nine times in
ten at these lengths and a null-lane one about two times in three, under half at 66–76 runes; the
phase 6–9 mechanisms were not carried to those pages). §25 decodes the texts Cicada pointed at exactly at every offset (null,
153 million tests); §26 tests the page images (null); §27 adds a rune 5-gram that lifts short-page
detection to 99 % and reruns the short pages (null); §28 records a hand-versus-machine test with no
power; §29 tries the two "Know This" magic squares as keys (null). §30 verifies Cicada's signed messages by full fingerprint (the 2017
"hoax" claim is false); §31 sweeps eight seeded generators no ledger lists (null, 113 million window
decodes). §32 runs keyword-mixed alphabets (quagmire I–IV) under the book's keys, the
one named non-additive class every additive decoder is blind to (null, 25.6 million window decodes);
§33 shows the 86 repeats are boundary-blind, excluding reset-chain ciphers and transcription artefacts. §34 replicates, with controls, the direct and pointer readings of the three-page
base-60 payload (null). §35 hashes every archived artefact against the page-73 hash (no match);
§36 measures the key-reuse test's power with planted clusters (about 20 aligned pages needed; blind
under key-skip drift); §37 gives the repeat spectrum to lag 120, the null models and the boundary
convention; §38 re-reads the unsolved pages blind from the images: 0 disagreements at 12,807 aligned
glyphs, 149 positions unread. §39 carries phases 6–8 to the nine short pages with the 5-gram rule (null);
§40 runs the pilgrim texts, Bunyan and Chaucer, as running keys (null). §41–§54 (2026-10-28/29) are the field survey and what it prompted: the word-edge correction that exposed two within-word echoes and the S carrier (§42, §45–§47, §50), the gated echo rule and its out-of-sample predictions (§47, §49), echo-aware decoding (§48, null), the layout, hint-reading and Cicada's-own-words lanes (§51–§53, null), and pnotisdev's 1,439 keystreams under this repository's three decoders (§54, null, 421.7 million window decodes, 18/18 controls). §55 (2026-10-29) is the filler lane: the unsolved pages' word lengths are not English prose, a plain decoder has no power if a tenth of the runes are fillers, and a free-null sweep of the external texts and pnotisdev's remaining offsets is null (19.5 million window decodes, 5/6 controls). §57 tests E56w+R4n out of sample, in §49's form: fifteen of sixteen cells hold, and the failing cell is the lag-6 count in long words, the hold repair's own signature. §58 runs the rule that §57 pointed at, the two echoes with a filler in half the words on the spend repair and no T-writing: it is the first rule inside every pre-registered band, ten statistics and sixteen out-of-sample cells, and it still predicts five S pairs against eleven. §59 runs three registered follow-ups: the filler rate fitted to the word lengths is 0.40 and fits inside the English bootstrap band, the per-length echo profiles hold on thirteen of thirteen cells, the solved pages carry no lag-4 excess, and at the fitted rate the S cell fails the band (z +3.2). Totals as of 2026-10-29: 883 million decoder tests, 29 of 47 lanes closed null, none running. Nothing here is a solve. The oldest real structure in the ciphertext, a fivefold deficit of doubled runes,
was known to the community a decade ago, and the three within-word structures (§42–§50) were first reported by other labs in 2026; this repository's contribution is independent
replication with controls, the exclusion of every key family anyone has named for it on the pages
long enough for the detector to see a planted solution (§23), and the tooling to test the next one in
minutes. None of this shows that the key was never published; it shows that no accepted decoding
exists within the tested configurations, at the stated detection limits. Sources and pinned revisions: `SOURCES.md`. Licence: MIT.
The transcription in `data/raw/` is rtkd/iddqd's; the Latin and Old English corpora are public domain.

**What is new here.** Most of this repository is replication and exclusion, and each section says so where it applies. Seven things are not in any other public lab's record, as of 2026-10-29:
1. *The S carrier is outside every additive mechanism whose key is independent of the plaintext at the echoed position.* In such a cipher an equal cipher pair takes a value uniform over the key, so no plaintext-blind key structure, periodic key or copy rule can weight the lag-5 echo to one rune; a weak or absent key inside some words is capped by the book's share of S at 8 % of words, which yields at most 3.8 of the 11 S pairs (§47). A key that reads the plaintext or the written rune (an autokey on S, a marker) is additive and escapes the argument; that is the class left open. (Narrowed 2026-10-29 after the second external review, §56.)
2. *A gated echo rule that reproduces the stream's geometry and survived prediction.* In about half the words, a plaintext repeat at lag 5 copies the cipher rune and at lag 6 writes 24 − 2c; nine of ten pre-registered statistics within 3 sd, then fourteen of fourteen cells of eight predictions written and committed before the check (§47, §49). It does not produce the S weighting.
3. *The two echoes share words* (18 against 10.8 among words that can host both, p 0.012 pooled), but only descriptively: stratified by exact word length the expectation is 14.0 and p 0.11 (§42, `results/echo_overlap.md`; corrected 2026-10-29, §56). It no longer counts as evidence for one word-level process.
4. *A blinded machine re-reading of the page images* that agrees with the transcription at 12,807 positions with zero disagreements, and reproduces the three structures to the digit (§38, §49).
5. *Detection power by page length*, and a rune 5-gram that lifts short-page detection at 66 runes from 21 % to 100 % of 80 plants (99 % before the model's lower orders were repaired, §56); every exclusion here carries its page-length limit because of it (§23, §27).
6. *Line breaks fall inside words 452 times of 630*; any lab that read the transcription's `/` as a word boundary over-split by 12 %. Correcting it turned "one structure" into four in this repository (§42).
7. *The first cross-lab decode.* pnotisdev's 1,439 keystreams had met only their own flat-IoC engine, and this repository's English Viterbi, free-null and echo-aware decoders had met only this repository's keys; §54 runs their library under all three at every offset (null, 421.7 million window decodes, 18 of 18 planted controls found) and exports this repository's 7,621 keys as a table for their engine.

Not ours, and credited in place: the repeat deficit (community, 2014), the two within-word echoes and the S carrier's existence (pnotisdev, ZzNible), the lag-5 bigram runs (pnotisdev), the soft re-draw model (found independently at least twice in 2026), the OTP-class framing (Dukotah), the ledger discipline (pnotisdev, Dukotah).

**Read it.** The companion site [liber-primus-site.vercel.app](https://liber-primus-site.vercel.app) shows the solved pages as text and as runes, the unsolved pages as transcribed, the status box, and an animated explainer of the measurements; it is built from this repository's `main` at each deploy and lives in its own repository, [RiskAverseTech/liber-primus-site](https://github.com/RiskAverseTech/liber-primus-site).

**Use it.** `pip install -r requirements.txt`; `python -I src/corpus.py` builds `data/corpus/corpus.json` from the public-domain texts in `data/corpus/raw` (the key library and the 5-gram model read it; the 5-gram's dense tables, `results/ngram5.npz`, are built on first use, about five minutes; both are gitignored, so a clean checkout needs this step before `check_solve.py`); `python -m pytest tests/` runs the fast checks (decoder bound, soft-rule round trip under all signs, noise calibration, the squares, the page counts, the cross-library manifest, and since 2026-10-29 the n-gram lower orders, the R4n rule and the K-fixed sampler; CI runs them on every push); `python -I src/check_solve.py --page LP2-03 --key DIVINITY --sign sub` adjudicates a claimed key or plaintext against the pre-registered bar; `ledger.json` is the lane table in machine-readable form (regenerated with `STATUS.md` by `src/status.py`); `benchmarks/plants.json` holds 25 planted ciphertexts with their keys for any decoder to recover; `src/verify_pgp.py` verifies Cicada's signed messages by full fingerprint.

<!-- toc:start -->
**Sections.** [Phase 1: key reuse](#phase-1-is-any-keystream-reused-across-the-unsolved-pages) · [4](#4-is-the-doublet-deficit-cipher-structure-resultsdoublet_auditmd) Is the doublet deficit cipher structure? · [5](#5-which-constructions-reproduce-it-resultsdoubletsmd) Which constructions reproduce it? · [6](#6-a-better-detector-and-the-scan-again-resultsdiff_scoremd) A better detector, and the scan again · [7](#7-what-the-data-supports-phase-2-conclusion) What the data supports (phase 2 conclusion) · [8](#8-phase-3-proposed) Phase 3, proposed · [9](#9-phase-3-the-books-keystream-families-with-the-skip-on-repeat-rule-resultsphase3md) Phase 3 · [10](#10-where-this-leaves-the-puzzle) Where this leaves the puzzle · [11](#11-prior-work-checked-2026-10-23) Prior work (checked 2026-10-23) · [12](#12-phase-4-phrase-and-sentence-keys-from-the-book-all-key-signs-resultsphase4md) Phase 4 · [13](#13-phase-5-latin-and-old-english-plaintext-models-resultsphase5md) Phase 5 · [14](#14-phase-6-word-edge-events-under-the-skip-rule-pnotisdevs-open-lane-run-independently-resultsphase6md) Phase 6 · [15](#15-within-word-lag-echo-not-replicated-with-the-uncorrected-word-edges-superseded-by-42-srcword_lagpy-resultsword_lagmd) Within-word lag echo · [16](#16-phase-7-the-skip-by-two-rejection-rule-srcskip2_lanepy-resultsphase7md) Phase 7 · [17](#17-hypothesis-loop-a-model-panel-proposes-a-statistical-gate-kills-srchypothesis_looppy-resultshypothesesmd-docshypothesis-loopmd) Hypothesis loop · [18](#18-phase-8-the-hypothesis-loops-short-list-swept-srcphase8_lanepy-resultsphase8md) Phase 8 · [19](#19-short-list-lane-phase-8-replicated-prime-gap-multiplier-and-feedback-families-added-srcshortlist_lanepy-resultsshortlistmd) Short-list lane · [20](#20-phase-9-cumulative-gematria-ciphertext-feedback-and-global-streams-with-no-per-page-reset-srcphase9_lanepy-resultsphase9md) Phase 9 · [21](#21-verdict-check-a-quorum-panels-mechanism-question-tested-srcverdict_checkpy-resultsverdict_checkmd) Verdict check · [22](#22-phase-10-unknown-position-nulls-under-a-hard-anti-repeat-rule-srcnull_lanepy-resultsphase10md) Phase 10 · [23](#23-external-review-2026-10-27-detection-power-by-page-length-decoder-coverage-calibration-srcpower_lanepy-srctest_skippy-resultspowermd-resultsskip_consistencymd) External review (2026-10-27) · [24](#24-short-page-lane-a-secondary-pre-registered-rule-for-the-pages-the-z--6-rule-cannot-see-srcshortpage_lanepy-resultsshortpagemd) Short-page lane · [25](#25-external-running-key-lane-the-texts-cicada-pointed-at-decoded-exactly-at-every-offset-srcrunkey_lanepy-srccorpuspy-resultsrunkeymd-datacorpus) External running-key lane · [26](#26-page-image-lane-is-there-information-in-the-images-that-the-transcription-does-not-carry-srcimage_lanepy-resultsimagesmd-docshuman-vs-machine-keymd) Page-image lane · [27](#27-rune-5-gram-rescoring-the-short-page-power-fix-measured-and-applied-srcngrampy-srcrescore_powerpy-resultsrescore_powermd-resultsshortpage_rescoremd) Rune 5-gram rescoring · [28](#28-windowed-dispersion-a-test-for-a-human-hand-that-turned-out-to-have-no-power-srcdispersionpy-resultsdispersionmd) Windowed dispersion · [29](#29-the-two-know-this-squares-as-key-material-srcsquare_lanepy-resultssquaresmd) The two "Know This" squares as key material · [30](#30-provenance-the-signed-messages-verify-by-full-fingerprint-srcverify_pgppy-docspgp-verificationmd-datarawpgp) Provenance · [31](#31-seeded-generators-no-ledger-lists-xorshift-pcg32-minstd-randu-splitmix64-srcgenerator_lanepy-resultsgeneratorsmd) Seeded generators no ledger lists · [32](#32-keyword-mixed-alphabets-under-the-books-keys-quagmire-iiv-srcquagmire_lanepy-resultsquagmiremd) Keyword-mixed alphabets under the book's keys · [33](#33-where-the-86-repeats-sit-boundary-blind-srcdoublet_boundariespy-resultsdoublet_boundariesmd) Where the 86 repeats sit · [34](#34-the-three-page-base-60-payload-as-key-material-a-controlled-replication-srcpayload_lanepy-dataprocessedpayloadjson-resultspayloadmd) The three-page base-60 payload as key material · [35](#35-every-archived-artefact-against-the-page-73-hash-srchash_sweeppy-resultshash_sweepmd) Every archived artefact against the page-73 hash · [36](#36-planted-cluster-power-of-the-key-reuse-test-srcreuse_powerpy-resultsreuse_powermd) Planted-cluster power of the key-reuse test · [37](#37-repeat-spectrum-null-models-and-the-boundary-convention-srclag_spectrumpy-resultslag_spectrummd) Repeat spectrum, null models and the boundary convention · [38](#38-blinded-glyph-level-re-reading-of-the-unsolved-pages-srcreread_lanepy-resultsrereadmd) Blinded glyph-level re-reading of the unsolved pages · [39](#39-phases-68-carried-to-the-nine-short-pages-with-the-5-gram-rule-srcrescore5py-resultsphase6_shortmd-resultsphase7_shortmd-resultsphase8_shortmd) Phases 6–8 carried to the nine short pages with the 5-gram rule · [40](#40-the-pilgrim-texts-as-running-keys-srccorpuspy-with-corpus_setpilgrim-resultsrunkey_pilgrimmd) The pilgrim texts as running keys · [41](#41-field-survey-2026-10-28-and-the-closure-bundle-it-prompted-resultsfield_survey_2026-10-28md-srcclosure_bundlepy-resultsclosure_bundlemd-srcwordlen_repeatspy) Field survey (2026-10-28) and the closure bundle it prompted · [42](#42-the-two-within-word-echoes-replicated-and-the-word-edge-correction-that-exposed-them-srckfixed_echopy-resultskfixed_echomd-srcecho_dissectpy-resultsecho_dissectmd-srcedgespy) The two within-word echoes, replicated, and the word-edge correction that exposed them · [43](#43-exact-reachability-of-the-solved-page-rule-and-linear-complexity-srcreachability_lanepy-resultsreachabilitymd-srclinear_complexitypy-resultslinear_complexitymd) Exact reachability of the solved-page rule, and linear complexity · [44](#44-irrational-digit-streams-under-the-soft-rule-srcirrationalspy-srcdigits_lanepy-resultsdigitsmd-dataprocessedirrational_digitsjson) Irrational-digit streams under the soft rule · [45](#45-word-aware-mechanism-lane-no-single-rule-reproduces-the-three-structures-and-the-s-carrier-is-the-one-that-breaks-every-rule-srcmechanism_lanepy-resultsmechanismmd-srcs_carrierpy-resultss_carriermd) Word-aware mechanism lane · [46](#46-the-lag-5-echo-runs-in-pairs-a-per-word-period-5-key-fits-the-equality-count-and-fails-the-rest-srcecho_sitespy-resultsecho_sitesmd-srcngram_lagpy-resultsngram_lagmd-srcperiod5_mixturepy-resultsperiod5_mixturemd) The lag-5 echo runs in pairs; a per-word period-5 key fits the equality count and fails the rest · [47](#47-echo-rules-a-gated-lag-5lag-6-echo-reproduces-nine-of-ten-statistics-and-the-s-carrier-is-shown-to-be-outside-every-additive-mechanism-with-a-plaintext-independent-key-srcmechanism_lanepy-resultsmechanismmd) Echo rules · [48](#48-echo-aware-decoding-of-the-phase-34-library-null-and-the-echoes-turn-out-to-cost-an-unaware-decoder-almost-nothing-srcscorepy-echo_mask-srcecho_lanepy-resultsecho_lanemd) Echo-aware decoding of the phase 3–4 library · [49](#49-two-untouched-tests-e56ws-out-of-sample-predictions-and-the-echoes-on-the-image-derived-stream-srce56w_predictionspy-resultse56w_predictionsmd-srcreread_echoespy-resultsreread_echoesmd) Two untouched tests · [50](#50-the-s-carrier-three-ways-the-eleven-sites-in-the-page-images-a-line-break-dependence-found-by-eye-and-an-s-triggered-rules-second-traces-resultss_sites-srclinebreak_echopy-resultslinebreak_echomd-srcs_rule_predictionspy-resultss_rule_predictionsmd) The S carrier, three ways · [51](#51-layout-follow-up-the-line-wrap-excess-is-not-a-layout-effect-srclayout_followuppy-resultslayout_followupmd) Layout follow-up · [52](#52-the-hint-reading-family-shed-our-own-circumferences-as-an-operation-null-srcshed_lanepy-resultsshed_lanemd) The hint-reading family · [53](#53-cicadas-own-words-20122017-as-key-material-null-datacorpusrawcicada_own_words_2012_2017txt-srccorpuspy-with-corpus_setcicada-resultsrunkey_cicadamd-srccicada_words_lanepy-resultscicada_wordsmd) Cicada's own words, 2012–2017, as key material · [54](#54-cross-library-lane-pnotisdevs-1439-keystreams-under-this-repositorys-three-decoders-srcpnotisdev_librarypy-srccross_library_lanepy-srcexport_book_librarypy-resultscross_librarymd-dataprocessedpnotisdev_library_manifesttsv-dataprocessedbook_librarytsv) Cross-library lane · [55](#55-the-filler-lane-the-word-length-fingerprint-decoder-power-under-fillers-and-the-sweep-srcwordlen_fingerprintpy-resultswordlen_fingerprintmd-srcfiller_powerpy-resultsfiller_powermd-srcfiller_lanepy-resultsfiller_lanemd-resultsfiller_lane_registrationmd) The filler lane · [56](#56-validation-release-2026-10-29-the-second-external-review-three-code-defects-fixed-the-affected-statistics-rerun) Validation release (2026-10-29) · [57](#57-e56wr4n-out-of-sample-fifteen-of-sixteen-cells-hold-and-the-one-that-fails-is-the-hold-repairs-signature-srce56w_r4n_predictionspy-resultse56w_r4n_predictionsmd-resultse56w_r4n_predictionsjson) E56w+R4n out of sample · [58](#58-e56w-with-fillers-on-the-spend-base-the-first-rule-inside-every-pre-registered-band-and-still-not-the-s-count-srce56w_n_lanepy-resultse56w_nmd-resultse56w_njson-srcmechanism_lanepy-rule-e56wn) E56w with fillers on the spend base · [59](#59-three-registered-follow-ups-to-e56wn-the-filler-rate-fitted-to-the-words-puts-the-s-cell-over-the-bar-the-length-profiles-hold-the-solved-pages-carry-no-lag-4-excess-srce56w_n_followupspy-resultse56w_n_followupsmd-resultse56w_n_followupsjson) Three registered follow-ups to E56w+n
<!-- toc:end -->

---

# Phase 1: is any keystream reused across the unsolved pages?

A depth-two (key-reuse) index-of-coincidence test on the 56 unsolved pages of Cicada
3301's Liber Primus, preceded by the computation that decides whether such a test can
work at all. Everything here is reproducible from `src/` with numpy; sources and pinned
revisions are in `SOURCES.md`; tables are in `results/`.

**Short answer.** The test the panel described is underpowered on single page pairs
(q − 1/29 = 0.0019, about 1.8 sigma per aligned pair of 250 runes), so I ran it anyway
and added a pooled version that sums all 1,485 pairs. Both are null for aligned reuse
at any offset within ±200 runes and for any within-page period from 2 to 200. The one
real non-randomness found is at lag 1: the unsolved pages contain 86 doubled runes
where 445 are expected (z = −17). That is a property of the cipher, not evidence of a
reused key.

## 1. Data

- Transcription: the rtkd/iddqd master file (pinned commit in `SOURCES.md`), confirmed
  rune-for-rune against Taiiwo/cicada and page-for-page against LiberPrimusSolver's
  `unsolved.txt`. The book has 74 pages; pages 1–15 and 72–73 are solved, chunks 16–71
  are the 56 unsolved LP2 pages (`LP2-00`..`LP2-55`), one of which (LP2-50) is image-only.
- Alphabet: Gematria Primus, 29 runes, index 0..28 = F U TH O R C G W H N I J EO P X S T
  B E M L NG OE D A AE Y IA EA.
- Plaintext: the solved pages were *decrypted with their published keys* (Atbash,
  Vigenère DIVINITY and FIRFUMFERENFE with the "plaintext F is left unencrypted" rule,
  shift-3-then-Atbash, the totient prime stream, and plain Gematria) and every section
  was verified rune-for-rune against the rtkd English translation. This gives 2,977
  plaintext runes in the book's own spelling (`data/processed/solved_plaintext_latin.txt`),
  avoiding the English-to-rune ambiguities (NG vs N+G, EA vs E+A, IA/IO, C/K) that a
  back-mapping would introduce. Script: `src/prepare.py`.

## 2. q and the power of the test (`src/q.py`, `results/q.md`)

With p the rune frequency vector of the plaintext, q = Σ_d (Σ_a p_a p_{(a−d) mod 29})² is
the coincidence rate of the difference of two independent plaintext streams, i.e. what
C − C' leaves behind when the keystream cancels.

| quantity | value |
|---|---|
| plaintext runes | 2,977 |
| IC of the plaintext itself | 0.0614 |
| **q** | **0.0364** (bootstrap 95% CI 0.0361–0.0368) |
| 1/29 | 0.0345 |
| **q − 1/29** | **0.0019** |
| empirical IC of page-minus-page differences, 200-rune windows | 0.0364 |

Under the null (independent iid uniform keystreams) the difference stream is iid
uniform, E[IC] = 1/29, and because pairs of positions sharing one index are uncorrelated
for a uniform alphabet, Var[IC] = 2π(1−π)/(N(N−1)) exactly (π = 1/29), i.e. sd ≈ 0.258/N.
Monte Carlo agrees to three digits.

| N | sd of IC under null (exact / MC) | sigma per aligned pair if the key is reused |
|---|---|---|
| 150 | 0.00173 / 0.00173 | 1.1 |
| 250 | 0.00103 / 0.00104 | 1.8 |
| 400 | 0.00065 / 0.00065 | 2.9 |

**Verdict on power: underpowered.** The excess is 0.0019, well under the 0.005 the panel
said it needed. A fully reused key would move a single 250-rune pair by under 2 sigma,
while the scan below makes half a million comparisons whose null maximum is 7–8 sigma.
Per-pair 5-sigma detection is therefore impossible for this plaintext distribution.

What *is* powered is pooling: if every page restarted the same generator from the same
state, all 1,485 pairs would be elevated at offset 0 and the pooled z would be about
65. If a quarter of the pages shared a stream, roughly 4 sigma pooled. So the pooled
test can still rule out the "identical reset on every page" hypothesis decisively.

## 3. The scan (`src/depth_two.py`, `results/depth_two.md`, `results/depth_two.png`)

Pre-registered before running (text in the script header):

- **R1 (panel rule, per pair):** a positive needs ≥ 3 disjoint page pairs each at or
  above 5 sigma with mutually consistent offsets.
- **R2 (pooled, added because of section 2):** pooled z(k) = Σ_pairs sigma / √(#pairs) at
  each offset k and each within-page lag L; a positive needs z ≥ 5 *and* above the
  maximum seen in every within-page permutation replicate (runes shuffled inside each
  page, which keeps every page's rune frequencies so a non-flat ciphertext cannot fake
  a positive).

Setup: 55 pages with runes, 1,485 pairs, offsets −200..+200, lags 1..200, minimum
overlap 60 runes; 507,789 pair-offset tests and 9,376 page-lag tests; 30 permutation
replicates of the whole scan.

![depth-two scan vs null](results/depth_two.png)

**Per pair (R1).** Top 20 hits are in `results/depth_two.md`. The strongest is
LP2-38/LP2-49 at offset −41, 6.63 sigma, on an overlap of only 66 runes. There are 74
hits at or above 5 sigma, at 68 distinct offsets, the most repeated offset having 3.
The shuffled-page null gives 58–87 such hits per replicate (median 70), and the observed
maximum 6.63 is *below* every one of the 30 null maxima (6.65–8.11). The histogram of
observed sigmas lies on top of the null's. R1 does not trigger once calibrated; read
literally ("some pair ≥ 5 sigma") it would trigger on shuffled data just as often.

A post-hoc note for honesty: three hits sit at |offset| ≤ 1 (LP2-28/42 at 0, LP2-04/45
at +1, LP2-35/38 at −1) where about 0.55 are expected, a ~2% coincidence after the fact.
Their difference-stream ICs (0.040) are also about 4 sigma *above* what a reused key
predicts (q = 0.0364), and the pooled z at offset 0 over all pairs is 0.08. I do not
count them as evidence.

**Pooled (R2), cross-page offsets.** Pooled z at offset 0 is 0.08 (null: 0.16 ± 0.89).
The largest pooled z over all 401 offsets is 2.96 (offset −181) against a null maximum of
2.99 ± 0.37 (max 4.07). Null. Nothing resembling the ~65 an identical reset would give,
nor the ~4 a quarter-sized shared subset would give.

**Pooled (R2), within-page lags.** The largest pooled z is 6.39 at **lag 1**, above the
null maximum 3.87, so R2 triggers there. Lags 2–200 are null (next largest 3.47 at lag 13,
3.21 at lag 10, both inside the null range). `src/lag1.py` shows what lag 1 is: of 12,901
adjacent rune pairs, only **86 are doublets (same rune twice) against 445 expected,
z = −17.3**; a few other difference classes are mildly over-represented (d = 20, 27, 16,
19 at +2.5 to +3.1). This is a deficit of repeats spread across pages (5 pages above +2
sigma, none below −2, mean +0.86), not a short-period generator: a period-1 generator
means a constant key, which would make every page's lag-1 structure that of plaintext
(lag-1 IC 0.0388) and give a pooled z near 29, not 6.4. The doublet deficit in the
unsolved pages is, to my knowledge, already known in the Cicada community; here it is
simply the only thing in the ciphertext that is not consistent with iid uniform
keystreams. It also explains the one other oddity in the tables: the mean sigma over all
pair-offset tests is +0.0065 (null ≈ 0), the same at every offset. Adjacent index pairs
are 2/N of all pairs, and two pages sharing the same non-uniform lag-1 difference
distribution match on those with an excess of about 9 × 10⁻⁴, which predicts a mean
sigma of about +0.007. Offset-independent, so unrelated to aligned reuse.

## 4. Decision

- Aligned keystream reuse between any two unsolved pages at any offset in ±200 runes:
  **not detected**; the pooled test excludes a shared reset generator across all or a
  large fraction of pages, and the per-pair test could not have seen a single reused
  pair anyway (section 2).
- Within-page periodic keystream with period 2–200: **not detected**.
- Lag 1: a real, strong deficit of doubled runes; a cipher property, not key reuse.
- A null here rules out aligned reuse at the tested offsets and short-period resets
  only. It says nothing about a long-period generator, about reuse at offsets beyond
  200, about autokey or transposition schemes, or about whether the pages are stream
  ciphers at all.

## 5. For the debate

My take: the depth-two test cannot settle this. I computed q from the 2,977 runes of
verified Liber Primus plaintext and got 0.0364, only 0.0019 above 1/29, so even a page
pair that shared its entire keystream would show up at under 2 sigma, while the scan
needs to survive half a million comparisons whose chance maximum is 7 to 8 sigma. I ran
it anyway over all 1,485 pairs of unsolved pages at every offset within ±200 and every
within-page lag up to 200: the per-pair hits are exactly what shuffled pages produce, the
pooled signal at offset 0 is zero against a prediction of about 65 if every page reset the
same generator, and no offset or lag from 2 to 200 stands out. The only real structure is
that the unsolved pages almost never repeat a rune twice in a row (86 doublets where
445 are expected, 17 sigma), which is a property of the cipher and not a reused key. So
aligned key reuse and short-period page resets are off the table; everything else,
including a long-period stream or a non-stream cipher, is untouched by this test.

## Reproduce

```
python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
.venv/bin/python -I src/prepare.py      # decrypt + verify solved pages -> data/processed/
.venv/bin/python -I src/q.py            # results/q.md, q.json
.venv/bin/python -I src/depth_two.py 30 # results/depth_two.md, *.npz, summary.json (~3 min)
.venv/bin/python -I src/lag1.py         # results/lag1.md
.venv/bin/python -I src/plot.py         # results/depth_two.png
.venv/bin/python -I src/word_lag.py     # results/word_lag.md (phase 7 lane: src/skip2_lane.py, ~11 min)
```

Layout: `data/raw/` downloaded sources (never executed), `data/processed/` verified
pages, `src/` scripts (`lp.py` holds the alphabet and parsers), `results/` outputs.

---

# Phase 2: the doublet deficit, which ciphers produce it, and a better reuse detector

Phase 1 left one real signature in the unsolved pages, a shortage of doubled runes, and one
weak test. Phase 2 asks whether the signature is real, what makes it, and whether a better
scorer changes the key-reuse verdict. Scripts: `src/doublet_audit.py`, `src/doublets.py`,
`src/diff_score.py`; tables in `results/`.

## 4. Is the doublet deficit cipher structure? (`results/doublet_audit.md`)

Doublet = the same rune twice in a row. Two nulls: iid uniform (rate 1/29 = 0.0345) and a
within-page shuffle that keeps each page's rune frequencies.

| text | adjacent pairs | doublets | rate | z vs uniform | z vs shuffle |
|---|---|---|---|---|---|
| solved plaintext (decrypted with the published keys) | 2,968 | 77 | 0.0259 | −2.5 | −8.6 |
| solved ciphertext (as transcribed) | 2,960 | 75 | 0.0253 | −2.7 | −7.2 |
| **unsolved ciphertext** | 12,901 | **86** | **0.0067** | **−17.3** | **−17.1** |

- The plaintext has the mild deficit ordinary English has (letters repeat less than
  independence predicts), nothing like fivefold.
- The solved *encrypted* pages sit at the uniform rate page by page (Atbash, both Vigenères,
  the totient stream: z between −1.6 and −0.1); the "plain" unencrypted pages inherit the
  plaintext's mild deficit, which is what pulls the solved-ciphertext row slightly below uniform.
- The transcription drops word, line and paragraph separators identically for the observed
  pages and the shuffle, and writes doubled letters as two runes. Inside words the unsolved
  rate is 0.0062; across separators 0.0080. Same deficit either side of a boundary, so it is
  not a word-level writing rule.
- Ciphertext autokey at lags 1 to 5 decrypts the pages to a flat stream with one hole where F
  would be (IC 0.0353, nothing like plaintext's 0.0614), so the simplest feedback cipher is out.

**The deficit is cipher structure.** Whatever generates these pages makes each rune avoid the
previous one about four times out of five more often than an additive cipher with an
independent, uniform key can.

## 5. Which constructions reproduce it? (`results/doublets.md`)

Twenty constructions encipher resampled solved-page plaintext cut into the 55 real page
lengths, 200 replicates each, and are scored on the pages' four statistics: doublets (86),
non-uniformity of the other lag-1 difference classes (chi² 42 on 27 dof), unigram flatness
(chi² 26 on 28 dof) and IC (0.0345).

| family | doublets | verdict |
|---|---|---|
| independent key with uniform differences: iid uniform, running key from English, hand pad with no repeated key symbol, the book's own Vigenère and totient streams | 430–506 | ruled out: a key with uniform successive differences hits a doublet one time in 29 (independence alone is not enough; a constant key keeps every plaintext doublet) |
| plaintext autokey, lags 1–5 | 481–698 | ruled out, and leaves heavy lag-1 structure |
| ciphertext autokey, lags 1–5 | 207–445 | ruled out (lag 1 makes a doublet a plaintext F, 1.6%) |
| ciphertext feedback with an offset chosen so a doublet means EA | 86 | matches the count, but its lag-1 stream is plaintext-shaped (chi² 9,629 vs 42): ruled out |
| Vigenère that steps its key when a doublet would form | 15 | ruled out |
| uniform key + "add one" when a doublet would form, 81% of the time | 84 | matches the count, but dumps the removed doublets into one class (chi² 299 vs 42): ruled out |
| uniform key re-drawn until no doublet (hard rule) | 0 | ruled out |
| **uniform key re-drawn when it would repeat, ~81% of the time** | **87 ± 10** | **consistent on all four** (70% and 90% are not) |

So the only construction found that reproduces the pages is: a keystream that is otherwise
indistinguishable from random, with the next key symbol rejected and redrawn about four times
in five exactly when it would make the ciphertext repeat the previous rune. The 81% is just
1 − 86/445 and carries a few points of sampling error. This describes the *statistics* of the
generator, not its identity: a hand-made key by someone who disliked writing the same rune
twice, a program with an explicit anti-repeat step, or any feedback rule whose only visible
effect is this one, would all look the same here.

## 6. A better detector, and the scan again (`results/diff_score.md`)

Four scorers for "these two aligned pages share a keystream", with the difference-of-plaintext
model trained on half the solved plaintext and tested on the other half, both members of a
simulated pair drawn from disjoint text. Cells are sigma per pair / power at the false-positive
rate implied by the phase-1 scan size (2 × 10⁻⁶):

| overlap n | difference-stream IC (phase 1) | match count (kappa) | unigram LLR | bigram LLR |
|---|---|---|---|---|
| 60 | 0.44 / 0.4% | 1.17 / 0.1% | 1.73 / 0.5% | 1.58 / 0.4% |
| 100 | 0.73 / 0.7% | 1.49 / 0.3% | 2.21 / 1.4% | 2.02 / 0.8% |
| 150 | 1.10 / 1.4% | 1.82 / 0.4% | 2.70 / 3.6% | 2.46 / 1.9% |
| 250 | 1.86 / 4.8% | 2.38 / 1.1% | 3.51 / 14.1% | 3.19 / 8.0% |

The unigram log-likelihood ratio is the best scorer, 1.89× the phase-1 IC per pair at n = 250,
because it uses the whole shape of the difference distribution rather than only its collision rate.
The bigram model adds nothing: adjacent differences of two independent texts are nearly
independent. Even so, per-pair power at this false-positive rate is 14% on a 250-rune overlap, so
single-pair detection stays weak; the pooled test is where the power is.

**Rescan with the unigram LLR**, same 1,485 pairs, offsets ±200, same pre-registered rules,
20 within-page permutation replicates: no pair reaches 5 sigma (null gives 0–1 per replicate),
the observed maximum 4.96 sits inside the null range 4.57–5.47, and the pooled z at offset 0 is
−2.31 against a null of −1.75 ± 0.81. If every page shared one keystream the pooled z would be
about 135; if 13 of the 55 pages did, about 7, since shared pairs scale with the square of the
page fraction (78 of 1,485 pairs; "about 34" stood here until 2026-10-27 and was wrong). Those are
expected values, not detection guarantees; the planted-cluster simulation of §36 measured detection
directly: under an aligned mechanism the pooled rule reaches 90 % only at about 20 shared pages (63 %
at 13, 7 % at 11), and under the key-skip mechanism, where shared pages drift apart after the first
skip, it detects nothing below the whole book.
**Null for large-scale aligned reuse, with a stronger detector than phase 1.**

## 7. What the data supports (phase 2 conclusion)

The unsolved pages of the Liber Primus show no detected large-scale aligned keystream reuse at any
alignment within 200 runes (by the planted-cluster simulation of §36: about 20 pages sharing an
aligned key are needed for reliable detection, and a key shared under the key-skip rule is invisible
to this test at any cluster size below the whole book), and no page restarts a short-period generator, now tested with a
detector 1.9× stronger than before. Their one departure from randomness, 86 doubled runes
where 445 are expected, is a property of the cipher: the plaintext, the transcription and the
book's own known ciphers all sit at the normal rate. Of twenty candidate constructions, the only
one that reproduces every measured statistic is a keystream that is otherwise random and is
redrawn about four times in five exactly when it would make a rune repeat its predecessor.
That rules out a precomputed pad used naively, every autokey tried, and every independent-key
cipher whose successive key differences are uniform (independence alone is not enough: a constant
key is independent of the text and keeps its doublets), and it says the generator looks at its own
previous output. It does not identify the
generator.

Plain-English version for a debate take: *Measured on the transcriptions, the unsolved pages
share no keystream with each other (pooled test null at 135-sigma sensitivity for full reuse).
The only non-random feature is a fivefold shortage of doubled runes, which is cipher structure,
not plaintext or transcription. Of twenty constructions simulated, exactly one reproduces all
the page statistics: a random key redrawn about 81% of the time when it would repeat the
previous rune. Independent uniform keys, autokeys, running keys and the book's own methods are all
ruled out.*

## 8. Phase 3, proposed

Cicada's solved pages already use a skip rule (plaintext F is left unencrypted and consumes
no key symbol). A sibling rule, "if the ciphertext would repeat the previous rune, skip to the
next key symbol", reproduces the phase-2 statistics and is decryptable: given a candidate
keystream K, a skip occurred at position i exactly when C_i − C_{i−1} ≡ K_{j+1} − K_j, which
the decryptor can check. So every keystream family the book has used (primes, totients,
Vigenère on words from the solved text, Fibonacci, Gematria sums) can be retried on the
unsolved pages with this rule and scored on English against the solved-page baseline, with
planted controls. Earlier community sweeps of those families did not include the rule. This is
the first experiment in this series with a real chance of producing plaintext rather than
another exclusion.

## 9. Phase 3: the book's keystream families with the skip-on-repeat rule (`results/phase3.md`)

Hypothesis: the unsolved pages use a keystream family the book has used before, plus a rule
that skips a key symbol whenever the ciphertext would repeat the previous rune (the sibling of
the book's own "plaintext F consumes no key symbol" rule). Decryption is a dynamic program
over "skips so far", because a skip is forced exactly when C_i − C_{i−1} ≡ K_{j+1} − K_j and
that condition also holds by chance at about one position in 29; the literal-F ambiguity is
carried the same way. Scoring is unigram English-in-runes likelihood, calibrated per page
against 2,000 random keystreams run through the identical decoder.

Families: constant shifts (29); Vigenère with every word of the solved text and the known
headlines, forwards and reversed; prime streams p, p−1 (the
totient stream) and p+1 from 101 starting points; Fibonacci and Lucas; affine (a·n + b) and
square (n² + b) position formulas; the solved plaintext as a running key at every one of its
2,977 offsets; and each page's neighbours as running keys, both directions. 4,716 shared
configurations per page, two F-rule variants, 55 pages: **519,200 tests**.

**Controls.** Twenty windows of solved plaintext enciphered with those families plus the skip
rule (soft, 81%) and both F-rule variants: all twenty recovered at z between 10.5 and
15.2, 17 ranked first among all configurations and none worse than
6th (the exceptions are keys with near-duplicates in the family, e.g. a shift beside the
affine formulas). The sweep finds what it is looking for by a margin of six sigma or more.

**Result: null.** The largest z over all 519,200 tests is 4.67, against a chance
maximum of about 4.8 for that many tests; the top transliterations are gibberish. The best
"hit" (LP2-35, self running key plaintext@882) reads IAMIAXYTHTITTHLYTHWOEOELRTHGMLHUTBBGNGHN…

So the book's own key families, with the one rule that reproduces the pages' statistics, do
not decrypt any page, at a sensitivity where planted keys stand out at ten sigma. What that
excludes: shifts, every single-word Vigenère from the book's vocabulary, the prime and
totient streams at any start, Fibonacci, position formulas, the book as its own running key,
and page-on-page keys, each with and without the F rule, under the skip rule. What it does
not exclude: keystreams from outside these families, multi-word or phrase keys, keys
derived through the Gematria prime values, or a generator with ciphertext feedback through a
permutation other than the identity.

## 10. Where this leaves the puzzle

Three phases, all on the real transcription, with pre-registered rules and planted controls:

1. The unsolved pages share no keystream with each other (phase 1, confirmed with a stronger
   detector in phase 2).
2. Their only non-random feature is a fivefold shortage of doubled runes, which is cipher
   structure; of twenty constructions, only a keystream re-drawn about four times in five when
   it would repeat the previous rune reproduces every page statistic (phase 2).
3. That rule, combined with every keystream family the book is known to have used, decrypts
   nothing (phase 3).

The generator looks at its own previous output and avoids repeats, and it is not one of
Cicada's published mechanisms with that rule bolted on. The next cheap families are feedback
through the Gematria prime table and short-phrase keys; beyond those, the remaining mass sits
on key material outside anything tested here, published or not (wording qualified 2026-10-27, §23).

## 11. Prior work (checked 2026-10-23)

None of the main findings here are new. They are independent replications, which is worth
something, but the record should say so.

- **The doublet deficit has been known since about 2014.** The Uncovering Cicada wiki's
  [Ideas and Suggestions](https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Ideas_and_Suggestions)
  page reports the same count (86 same-rune pairs in about 13,000 runes), calls it "the only
  solid clue towards cipher/key found in runes", notes that doublets are made "~5 times less
  likely", and already proposes the mechanisms tested in phases 2 and 3: enciphering
  algorithms that include the previous rune's value, and a key that "jumps to the (n+1)th
  number in the stream key" to avoid a repeat. The wiki's
  [Frequency Analysis](https://uncovering-cicada.fandom.com/wiki/Frequency_Analysis_Unsolved_Pages)
  page gives the per-chapter doublet table and the 1/29 baseline.
- **The soft anti-repeat rule has been found independently at least twice in 2026.**
  [jens-wedin/liber-primus](https://github.com/jens-wedin/liber-primus) describes an
  output-stage key-skip that keeps a would-be doublet about one time in five
  (p_keep ≈ 0.19), models re-roll against key-skip, finds collision resolution to be uniform
  (ruling out a deterministic bump, our "+1 rule"), and sweeps prime/totient streams, running
  keys from candidate texts, short and coined word keys, affine, autokey, PRNG and OEIS
  keystreams under the rule with a 98% self-test as control.
  [wazar/cicada3301](https://github.com/wazar/cicada3301) reaches the same filter
  (≈83% suppression, p_keep ≈ 0.18), calls the deficit "the only real structure in the entire
  corpus", uses a skip-aware beam decoder with plant-and-recover controls, and keeps a ledger
  of excluded attacks including derived keystreams and public randomness pads.
- **Exclusion ledgers with positive controls already exist.**
  [Leo-Y-Zhang/LiberPrimusAnalysis](https://github.com/Leo-Y-Zhang/LiberPrimusAnalysis)
  reports the same 86 vs 447 doublets, excludes periodic keys with and without the F-interrupt
  and key-skip rules, integer sequences, autokeys, prime-value feedback, running keys and
  shared keys between sections, each with a detector proven on synthetic ciphertext.

What this repository adds is a third implementation that agrees with the others on the
mechanism parameter (81% here, 81–82% there), a within-page permutation null for the key-reuse
scan, a twenty-construction comparison on four statistics at once, and an exact dynamic
program over skip count that carries the literal-F ambiguity as state. Three independent
methods converging on one mechanism is the result; the mechanism itself was proposed by the
community a decade ago.

Consequence for further work: before any new sweep, diff the candidate family against the
three ledgers above. The proposed phase 4 (Gematria prime-value feedback, phrase keys) overlaps
at least partly with families those ledgers already close.

**Ledger diff (2026-10-23).** `results/ledger_diff.md` tabulates every family against the three
ledgers above. Of the four phase-4 candidates named earlier, prime-value feedback, page-derived
keys and the lag-2-to-50 profile are already closed with controls (LZ and WZ; JW §34; all three).
The one family nobody has run under the anti-repeat rule is multi-word phrase and sentence keys
drawn from the book itself (about one million tests, chance maximum ≈ 5.2σ against our 10–15σ
controls). Two instrument gaps follow: our phase 3 decrypts with one key sign only, and no
project has scored the book families under a Latin or Old English model.

## 12. Phase 4: phrase and sentence keys from the book, all key signs (`results/phase4.md`)

The ledger diff (§11) left one family untested by anyone under the anti-repeat rule: keys longer
than a word, drawn from the book's own text, which is where both solved word keys came from.
`src/phrases.py` takes every 2-, 3- and 4-word contiguous phrase and every full line of the solved
translation (94 numbered lines, 726 words), forwards and reversed, 2,905 distinct keys, and
runs each under the skip rule with all three sign conventions (C = P + K, C = P − K, and
Beaufort C = K − P), with and without the F rule. The same run also closes this repository's own
instrument gap by taking phase 3's 4,716 keystreams through the two sign conventions phase 3 had
not used. The decoder gained a double-skip transition (two consecutive key symbols both reproducing
the previous rune, which doubled letters in a phrase key force) and a Beaufort mode; the forced-skip
condition is the same under every sign. 18,147 configurations per page, 55 pages, two F
variants: **1,996,170 tests**, chance maximum about 5.4σ.

**Controls.** Twenty-six planted keys spanning every family, sign and F variant: all recovered at
z between 10.6 and 16.3, 24 of 26 ranked first in their set, the other two
(Lucas streams under Beaufort) second behind a neighbouring Lucas offset. Rune recovery 0.92 to 1.00.

**Result: null.** The largest z over all 1,996,170 tests is 5.10 (LP2-09, sign
sub, phrase-2 'CERTAINTY AND'), below the chance maximum and the pre-registered bar of 6;
its transliteration is gibberish. Nothing among the phase 3 families changes sign.

What this excludes: every phrase of two to four words and every line of the solved text, in either
direction, as a periodic key under the soft anti-repeat rule, at any of the three sign conventions,
with or without the F rule, at a sensitivity where planted phrase keys stand out at ten sigma or
more. What it does not exclude: phrases from text outside the book, keys applied to a non-English
plaintext (the scorer is English), a rejection loop that consumes two key draws per rejection
(wazar's skip_by_two), or any keystream that is not periodic.

**Prior-art correction (2026-10-23, after a wider survey).** pnotisdev/cicada3301 had already tested
1,841 word, phrase, title and line keys of up to 24 runes from the solved pages, in eight spellings,
both signs, with and without the F rule, at the eight section starts (its `solved-phrase-keys`
entry, excluded) and 1,940 keywords of length 3–30 under its collision-repair model on all windows.
Phase 4's additions over that are keys longer than 24 runes, reversed keys, and every page rather
than section starts. See the field survey at the end of `results/ledger_diff.md`.

With this, the book-internal key space under the anti-repeat rule is closed by at least one
controlled analysis for every family any of the four projects could name. The remaining lanes are
the non-English rescoring of these same families and the external hunts (an untried text, a seed,
the "AN END" page), none of which this repository can finish on its own.

## 13. Phase 5: Latin and Old English plaintext models (`results/phase5.md`)

Every lab's negatives were English-register negatives, and wazar showed that under its quadgram
scorer a correct key over a Latin or Old English plaintext scores as noise. `src/registers.py`
builds rune-unigram models from public-domain corpora transliterated with the book's own rules:
Latin from Caesar's Gallic War and Cicero's Catilinarians (68,000 words, 379,331 runes); Old
English from Beowulf and eighteen prose and verse texts of Bright's Anglo-Saxon Reader (36,863
words, 159,508 runes; thorn and eth to TH, ash to AE, length marks dropped). `src/sweep_registers.py`
reruns every phase 3 and 4 family (22,863 configurations, three signs) on all 55 pages, both F
variants, with the decoder's model set to each language: **5,029,860 tests**.

**Controls.** Twelve planted keys per register on windows of that language's corpus, decoded
with the register's own model and, separately, with the English model. Latin: own model
z 11.0–15.0, 11 of 12 rank 1; English model z 10.0–12.9,
11 of 12 rank 1. Old English: own model z 8.1–11.4,
11 of 12 rank 1; English model z 6.9–10.6,
11 of 12 rank 1. So the English unigram scorer loses little power
on either register: the blind spot wazar reported belongs to quadgram scorers, and phases 3 and 4
already covered Latin and Old English plaintexts at only slightly reduced sensitivity.

**Result: null.** Largest z under the Latin model 4.88, under the Old English model
4.53, both inside the chance range for this many tests; the top transliterations
are gibberish in either language. The book families and phrase keys under the skip rule are
excluded for Latin and Old English plaintexts at the controls' sensitivity.

Context from the wider survey (§11, `results/ledger_diff.md`): the October 2026 campaign's
language lane found Latin ten to thirty times worse than English on word-length statistics and
could not fetch Old English prose at all, so the Old English prose lane here was the only
genuinely untested register; it is now closed for these families.

## 14. Phase 6: word-edge events under the skip rule, pnotisdev's open lane run independently (`results/phase6.md`)

> **Correction 2026-10-28.** The edge file this lane used counted every line break as a word boundary; 452 of the 630 line breaks on the unsolved pages fall inside a word, so 12 % of the "word edges" were not word edges (3,261 instead of 2,873). The builder is fixed and the lane rerun; see §42 for the rerun and what changed.

The field survey (§11) found that pnotisdev/cicada3301's registry item `open-unkeyed` (its priority 2:
"unkeyed insertions and extra key advance at word separators / line / page breaks") had an engine,
a one-window pilot and a written campaign queue, but the campaign was never launched for want of a
free CPU, and its line-break part was never built. `src/edges.py` aligns the master transcription's
word and line separators to every unsolved page (3,261 word edges, 539 line edges); `score.decode`
gained two event transitions (an extra key advance before a candidate rune; a candidate rune as an
unencrypted uniform null that consumes no key) with a per-event log prior ln(0.42/0.58), the
default path left bit-identical; `src/edges_lane.py` runs four kinds (adv, advline, nulli, nullf)
over the phase 3 and 4 key families under all three signs and both F variants: **10,059,720
tests**. The hit rule was written before any page was scored: z ≥ 6 over the page's own
random-keystream null under the same kind, edge score at least 20 nats above the base decoder's
score for the same configuration (pnotisdev's edge-versus-base margin), and readable English.

**Controls.** Twenty-four plants at the 42 % event rate on the pages' own edge masks: the edge
decoder recovers them at z 7.0–15.3, 23 of 24 ranked first (the exception a three-rune
key with aliases), while the base decoder without events scores the same plants at z
0.2–12.2; for the advance kinds the base decoder is blind (z 0.6–12.2), which is
why an event-aware decoder was needed at all.

**Result.** Largest z 5.24 (LP2-15, nulli, beaufort, phrase-4-rev 'MY HEAD THOUGHT THE ʳ'); per kind adv 5.17, advline
5.18, nulli 5.24, nullf 4.77; chance maximum about 5.7. Cells meeting the rule: 0.
**Null.** Extra key advances at word or line starts and unencrypted
nulls at word starts or ends, at pnotisdev's fitted rate, over the book's own key families under the
skip rule, are excluded at the controls' sensitivity. The entry in pnotisdev's registry format is
`results/pnotisdev_open-unkeyed_entry.toml`, written to be pasted into their `docs/registry.toml`
with the gaps stated (max-path decoder, emitted-rune anti-repeat check, no in-word nulls, their
1,447-stream library not run).

## 15. Within-word lag echo: not replicated with the uncorrected word edges (superseded by §42) (`src/word_lag.py`, `results/word_lag.md`)

> **Superseded 2026-10-28.** This section's null result came from the same over-split word edges as §14. With line breaks no longer counted as word boundaries, the lag-5 echo is present at z +3.66 (rerun 2026-10-29 with the attempt-clock sampler, §56) and survives a null that also fixes the repeat count; §42 has the replication, the dissection and the lag-6 relation that goes with it.

The field survey (§11) lists a lag-5/lag-6 within-word echo at about 2.5σ as one of the two
"frontier" observations in the most thorough public labs. `src/word_lag.py` measures it on this
transcription: for lags 1–12, pairs of runes k apart inside the same word (word boundaries from
the master file), pooled over the 55 pages, scored by the chi-square of the 29 difference classes
and by the d = 0 count, against 300 within-page shuffles with the word boundaries held fixed.
Lag 1 shows the doublet deficit (chi-square z +32, d = 0 at −16). Lags 2–12 are null on the
chi-square (|z| ≤ 1.4). The d = 0 count sits at +2.1σ at lags 4 and 5 (110 vs 91 and 72 vs 57),
which, over twelve lags and two statistics, is what chance gives. The echo is not a feature
this transcription supports; a 2.5σ reading at one of a dozen lags is a selection effect.

## 16. Phase 7: the skip-by-two rejection rule (`src/skip2_lane.py`, `results/phase7.md`)

The ledger diff (§11, item 4) left one instrument variant untested on the book's families: wazar's
skip_by_two, where a rejected key draw discards two key symbols (the second unread) instead of one.
wazar validated a decoder for it but ran it only on PRNG seeds. `src/score.py` now has a
`rejection="two"` mode (the forced-skip condition becomes C_i − C_{i−1} ≡ K_j − K_{j−2}, the same
under every sign; the default path is bit-identical to before) and `src/skip_decrypt.py` encrypts
with `skip_by=2`. The lane reruns every family of phases 3 and 4 (22,863 configurations: book
keystreams and phrase/sentence keys under three signs) on all 55 pages, both F variants:
**2,514,930 tests**, chance maximum about 5.4, pre-registered rule z ≥ 6 and readable English.

**The blind spot is real.** Twenty-four skip-by-two plants (soft 81 %) decoded with the single-advance
decoder that every earlier phase and every public ledger used score z −1.5 to 11.9 with rune recovery
5 % to 100 %; half of them sit below z = 6. The same plants under the skip-by-two decoder score
z 9.5–14.9, 22 of 24 ranked first in their set (the other two are a Fibonacci offset ranked 11th and a
running-key offset ranked 2nd behind neighbouring offsets of the same stream, both above z = 6). So the
earlier negatives covered this variant only when the window happened to contain few rejections.

**Result: null.** Largest z over all 2.5 million tests is 4.99 (LP2-35, self running key at offset 878,
gibberish), inside the chance range. The book's keystream families and phrase keys are now excluded
under both rejection widths. Runtime 11 minutes.

## 17. Hypothesis loop: a model panel proposes, a statistical gate kills (`src/hypothesis_loop.py`, `results/hypotheses.md`, `docs/hypothesis-loop.md`)

A panel of three models (Claude Fable 5.1, GPT-6.1 Sol, Grok 4.7) was given an 11k-token brief of this repository's results, the ledger diff and the book's own methods, plus a fixed menu of cipher constructions (key source × combining rule × repeat-avoidance rule × F rule), and asked for ranked constructions in a JSON schema, two rounds, the second after seeing the first round's gate table. Proposals are data: the gate assembles each one from the menu and enciphers 200 replicates of solved-page English cut to the 55 real page lengths, scoring doublets, lag-1 class χ², unigram χ² and IC against the pages (pass = |z| < 3 on all four; a strict reading rescales by the iid-null sd). Survivors that are decryptable finite families are checked against the ledgers and sized. The gate reproduces the phase 2 table row for row before any proposal is scored.

Result: 58 proposals, 45 pass the pre-registered rule, 24 pass strict. All three proposers converged on the soft reject-on-repeat at p ≈ 0.81, so the gate separated families on the other three statistics: stream-plus-ciphertext-feedback keys pass loosely but sit 4–8 null sigmas high on the lag-1 class χ² (the difference stream inherits the base stream's residues); position-walking affine multipliers lift unigram and lag-1 χ²; independent streams of any source pass trivially, since an independent key with the right rejection rate is the phase 2 survivor, and the gate cannot tell a Cicada-flavoured generator from a one-time pad. No construction reproduces the pages by another route. The usable output is a short list of small finite families no ledger names (13 under ten million decoder tests; 3 more are LCGs with 2³¹ seeds, too large to sweep blind): lcg(a=1033,c=0,m=3301); add; redraw p=0.81; F=none (3,301 configurations); lcg(a=2,c=24,m=29); add; skip k=1 p=0.81; F=none (29 configurations); C-feedback lag 1 map prime_value + running_text; add; redraw p=0.81; F=none (86,333 configurations); prime_gap[n+3301]; affine m=position; skip k=1 p=0.81; F=none (82,012 configurations); lcg(a=3,c=0,m=3301); add; redraw p=0.81; F=none (3,301 configurations); C-feedback lag 1 map totient_value + lcg; beaufort; skip k=1 p=0.81; F=none (95,729 configurations); lcg(a=3301,c=29,m=1033); add; skip k=2 p=0.81; F=none (1,033 configurations); C-feedback lag 1 map totient_value + running_text; add; skip k=1 p=0.81; F=none (86,333 configurations); lcg(a=7,c=1,m=3301); add; skip k=1 p=0.81; F=none (3,301 configurations); word 'DIVINITY'; affine m=position; skip k=1 p=0.81; F=none (812 configurations); lcg(a=7,c=1,m=3301); beaufort; skip k=1 p=0.81; F=none (3,301 configurations); C-feedback lag 1 map prime_value + lcg; add; skip k=1 p=0.81; F=none (95,729 configurations); C-feedback lag 1 map prime_value + running_text; add; skip k=2 p=0.81; F=none (86,333 configurations). Each is a cheap lane for the existing skip decoder. Cost of the run: $4.16 (87,383 input and 113,218 output tokens, one failed attempt included).

## 18. Phase 8: the hypothesis loop's short list, swept (`src/phase8_lane.py`, `results/phase8.md`)

The loop (§17) left a short list of small, decryptable families no ledger names. Phase 8 runs the
ones the owner picked: linear congruential generators with Cicada-flavoured parameters at every
seed (a = 1033, c = 0 and a = 3, c = 0 and a = 7, c = 1 modulo 3301, add and Beaufort; a = 2,
c = 24 modulo 29; a = 3301, c = 29 modulo 1033 with skip-by-two), key = x_n mod 29, soft
reject-on-repeat; and the two solved word keys DIVINITY and FIRFUMFERENFE under an affine combine
C = m_i·P + K with a position-walking multiplier m_i = ((a·i + b) mod 28) + 1, all 784 schedules.
`src/score.py` gained a per-position multiplier inverse (`mult_inv`); the forced-skip condition is
unchanged. 15,834 configurations per page, 55 pages, both F variants: **1,741,740 tests**, chance
maximum about 5.4, pre-registered rule z ≥ 6 and readable English.

**Controls.** Sixteen plants spanning every set, sign, rejection width and F variant: all recovered at
z 10.8–14.4, all ranked first in their set, rune recovery 0.93–1.00.

**Result: null.** Largest z over all tests 4.51 (LP2-47, LCG a = 7, c = 1, seed 15, gibberish);
per set 3.8–4.5, all inside the chance range. The named LCG families at every seed and the solved
word keys under every position-walking multiplier are excluded. Not run from the loop's list: the
feedback families (rune-prime or totient feedback on a running-text or LCG base, 86k–96k
configurations each) and the prime-gap stream with a multiplier schedule. Runtime 15 minutes.

## 19. Short-list lane: phase 8 replicated, prime-gap multiplier and feedback families added (`src/shortlist_lane.py`, `results/shortlist.md`)

A second, independently written sweep of the hypothesis loop's short list (§17), run as three page shards. Families: the LCG seed sets of phase 8 at a wider parameter net (mod 3301 with three (a, c) pairs; mod 1033 under skip-by-one and skip-by-two; mod 29 at every a in 2..28 and every c), the two solved word keys under all 812 position-walking multipliers, and two families phase 8 did not run: the prime-gap stream (p_{n+o+1} − p_{n+o}, offsets 0..100 and 3301) under every multiplier schedule, and Gematria prime-value or totient-value ciphertext feedback added to the book's own plaintext at all 2,977 offsets. Soft reject-on-repeat, three signs, both F variants, 225,183 configurations per page: **24,770,130 tests**, chance maximum about 5.8, pre-registered rule z ≥ 6 and readable English. The decoder hook (multiplier inverse and feedback correction inside the Viterbi) is asserted identical to `score.decode` without hooks, and the random-keystream null is unchanged by it.

**Controls.** Fourteen plants, two per family, spanning sign, rejection width and F variant: all recovered at z 10.1–14.1, twelve ranked first (one tied at rank 2 with an equivalent seed, one skip-by-two plant at rank 4, the §16 desync).

**Result: null.** Largest z over all tests 5.21 (LP2-33, LCG mod 1033 seed 241 under skip-by-two, gibberish); per family 4.55–5.21. The LCG and word-key families replicate phase 8's null with a separate decoder; the prime-gap stream under every clock multiplier and the prime-value and totient-value feedback over the book's text are excluded for the first time. Still unrun from the loop's list: feedback over an LCG base (86k–96k configurations each). Wall time 69 minutes on three cores.

## 20. Phase 9: cumulative-Gematria ciphertext feedback, and global streams with no per-page reset (`src/phase9_lane.py`, `results/phase9.md`)

Two families nobody's ledger had closed. **Family A** keys each rune by the cumulative Gematria value of the ciphertext before it: three value maps (rune index, rune prime, totient of the prime), three maps from the running sum S to a key component (S mod 29, p_S mod 29, φ(p_S) mod 29, primes sieved to 26 million), with the totient or prime stream added at offsets 0..100 or no base stream at all: 1,827 configurations. The offset is known from the ciphertext, so it rides inside the Viterbi as a per-position correction (`score.decode(..., offset=)`, asserted bit-identical to the plain decoder when absent). **Family B** drops the per-page restart every phase so far assumed: the prime, totient, prime+1, prime-gap, Fibonacci-mod-29 and Lucas-mod-29 streams run continuously through the book, so a page is tried at every global offset 0..13,500 (the unsolved text is 12,956 runes; page 30 sits near offset 7,000). Soft reject-on-repeat, three signs, both F variants, 55 pages: **27,334,890 tests**, chance maximum about 5.9, pre-registered rule z ≥ 6 over 2,000 random keystreams per page, variant and decoder mode, and readable English. Four page shards, about 62 minutes each.

**Controls.** Eighteen plants spanning both families, all signs and F variants. Fifteen recovered at z 10.9–14.0, rank 1. The three family-A `sub` plants failed outright (z ≈ 0, 4 % of runes), and the cause was a bug, not the decoder: for that sign the cumulative offset was passed un-negated, so family A × sub was testing C = P + O − K instead of C = P − O − K. The sign was fixed, family A × sub was rerun for every page and both F variants with fresh nulls (a minute per shard), and six fresh A × sub plants, two of them F = true, all recover at z 10.2–13.5, rank 1 (`results/phase9.md`, `results/phase9_redo_controls.log`). The first-run rows stay in the table, marked. Family B and the other two family-A signs were never affected.

**Result: null.** Largest z over all tests 5.44 (LP2-40, totient stream at global offset 11,571, gibberish); family A 4.38, family B 5.44. Keys driven by the cumulative value of the preceding ciphertext, and the book's six streams with no per-page reset, are excluded at the sensitivity the controls show. Not covered: cumulative sums of the *plaintext* (an autokey the Viterbi state cannot carry; it needs a different decoder), sums that include the current rune, and streams outside these six.

## 21. Verdict check: a Quorum panel's mechanism question, tested (`src/verdict_check.py`, `results/verdict_check.md`)

After §20 the question was put to a five-model Quorum panel in a different form: not "which key" but
"what mechanism leaks 19% of repeats in an anti-repeat rule", with four new ciphertext-only premises
computed first (`results/verdict_check.md`, premises): the deficit is homogeneous across pages
(dispersion chi² 59 on 55 dof), rune-blind (chi² 28 on 28), position-blind, and the ciphertext
conditioned on the previous rune has IC 0.0358 against 0.0357 uniform, which excludes any fixed table
indexed by the previous ciphertext rune, additive or not. The panel (quorumsays.com/q/8gvLyrvHouBK,
2026-10-26) answered that a soft keep constant, a hard rule plus about 10% uniform nulls, and a hard
rule over a memoryless sticky key are equivalent on every figure, and named lag-2 repeats as the one
discriminator.

**Checked by simulation** (200 replicates of solved-page English at the real page lengths, five
statistics): the three are not equivalent. Hard rule plus 10% nulls gives 40 ± 6 doublets (z +7.8);
it needs about 22% nulls to reach 86. A sticky key at the rate that gives 86 doublets lifts the lag-1
difference chi² to 74 ± 16 against the observed 42 (z −2.0), because the key's repeats copy a
0.17-weighted image of the plaintext difference distribution into the ciphertext; a rate low enough
to keep the differences flat gives 49 doublets. Lag-2 repeats land within one sigma of the observed
435 under every construction, including an independent key, so they discriminate nothing (hard-rule
expectation 458 ± 22, not the panel's 463).

**What survives:** the soft re-draw of §5 and a hard rule with about 22% uniform nulls, which no decoder
here modelled until §22 (nulls at unknown positions need an insertion state at every position; §14 ran
nulls at word edges only). The observed difference chi² of 42 sits two sigma above every flat model and two
sigma below the sticky model, the faint excess §5 noted, now bracketed from both sides. The panel's
useful contributions were negative: the 19%-repeating key of the asker's take collapses into a
generator constant and is not a nameable family, and its claim scorer flagged two figures stated
without a source (a "2.8-sigma" doublet excess, really 17 sigma; a solved-page runes-per-page norm,
which is typesetting). Runtime 6 minutes.

## 22. Phase 10: unknown-position nulls under a hard anti-repeat rule (`src/null_lane.py`, `results/phase10.md`)

§21 left one mechanism that fits every page statistic and could still be breakable: a hard rule (the
key is skipped until the rune differs from the previous one) with uniform null runes inserted at
unknown positions at about one in five. If that were the cipher, the key under the nulls could be
one of the book's own families, so this lane lets the §9 decoder call any rune a null: the null
transition of `score.decode` (no key consumed, gain 0) is enabled at every position with a fixed log
prior, and the Viterbi chooses where the nulls sit. Key library: the phase 3 book families and the
phase 4 phrase keys, 22,863 configurations over three sign conventions, both F variants, 55 pages:
**2,514,930 tests**, chance maximum about 5.4. Null for z: 2,000 random keystreams per page, F
variant and decoder mode through the same free-null decoder. Pre-registered rule: z ≥ 6, free-null
score at least 20 nats above the base decoder for the same key, and readable English.

**The prior was fixed on the controls before any page was scored.** Eighteen plants (hard rule, nulls at
0.15, 0.22 and 0.30, all signs, both F variants, families cycled) were decoded under five null priors:
−3.0, −2.0, −1.27 (the Bayesian value ln(0.22/0.78)), −0.8 and −0.4 recovered 8, 11, 14, 15 and 14 of
18 at z ≥ 6 and rank 1. A stiffer prior hurts because the random keystreams lose less freedom than the
true key does. The sweep ran at −0.8. Its three misses are honest limits: a prime-stream Beaufort plant
at 30 % nulls (z 3.1, rank 13), a four-word phrase key at 22 % (z 5.2, rank 1), and a self-running-key
plant at rank 3 behind two equivalent offsets. Recovered plants read at 60–88 % of real positions.
The base decoder scored the same plants at z −0.9 to 6.8: without the insertion state it is blind.

**Result: null.** Largest z over all tests 5.64 (LP2-14, the book's own text at offset 366 as a running
key, gibberish; the decoder spent 21 nulls to get there); per sign 4.98, 5.64, 4.72. No cell meets
the rule. A hard anti-repeat rule over this repository's key families with uniform nulls at unknown
positions is excluded at the sensitivity the controls show. Not covered: non-uniform nulls, nulls
that consume a key value, rates outside 0.15–0.30, key streams outside these families. Runtime 48
minutes on four shards.

**Where this leaves §21's bracket (reworded 2026-10-27 after external review, §23).** Of the two
mechanisms that reproduce every ciphertext statistic, the breakable one has no accepted decoding
within this key library, at the sensitivity the controls show, on pages long enough for the rule to
have power (§23: lane B reaches 80 % power only at about 200 runes, so this sweep is inconclusive on
the shorter pages). The earlier wording, that what remains is "key material that was never
published", claimed more than a search over one library and one mechanism can show: untested texts,
encodings, start states and mechanisms remain open, and two planted controls scored below the cutoff.

## 23. External review (2026-10-27): detection power by page length, decoder coverage, calibration (`src/power_lane.py`, `src/test_skip.py`, `results/power.md`, `results/skip_consistency.md`)

An independent reviewer read commit f58489d, reran the preparation, the q estimate and the doublet
audit (checksums, 12,956 runes, 12,901 pairs, 86 doublets against 444.86, q ≈ 0.0364 all reproduced),
and raised five objections. Checked against the code, all five hold. The data facts stand; several
conclusions were stated more strongly than the searches support, and this section records what
changed. The reviewer's point that the detector's blind spots should be measured before any further
key search was taken in that order.

**1. Power of the z ≥ 6 rule by page length (high).** The rule was calibrated on 240-rune plants; the
pages run from 66 to 277 runes. `power_lane.py` plants the correct key at seven lengths in four
families (Vigenère word, three-word phrase, primes, self-running key), 20 plants per cell with signs
and F variants cycled, 400 random-keystream nulls per plant, and scores it exactly as the sweeps do.
Lane A is the soft rule with the base decoder (phases 3–9); lane B is the hard rule with 22 % nulls
and the free-null decoder at the §22 prior (phase 10).

| length | lane A: share at z ≥ 6 (median z) | lane B: share at z ≥ 6 (median z) | pages at or below this length |
|---|---|---|---|
| 66 | 0.23 (5.5) | 0.05 (4.0) | 1 |
| 92 | 0.91 (6.6) | 0.28 (5.4) | 3 |
| 120 | 1.00 (7.9) | 0.53 (6.0) | 3 |
| 160 | 1.00 (9.3) | 0.78 (6.9) | 7 |
| 200 | 1.00 (10.5) | 0.89 (7.8) | 10 |
| 240 | 1.00 (12.0) | 0.96 (8.7) | 20 |
| 277 | 1.00 (13.0) | 1.00 (9.9) | 55 |

Median plaintext recovery of the correct key is 0.99–1.00 at every length in lane A and 0.68–0.80 of
the real positions in lane B, and the correct key ranks first within its family 90–96 % of the time
at every length in lane A: the correct plaintext is recovered on short pages and still fails the
rule, exactly the reviewer's finding (their 1/20, 14/20, 20/20 at 66, 92 and 240 runes with
DIVINITY matches this table). The weakest family reaches 80 % power at **92 runes in lane A** and
**200 runes in lane B**. So the phase 3–9 exclusions are **inconclusive on LP2-49 (66) and LP2-55
(76)**, and the phase 10 exclusion is **inconclusive on nine pages: LP2-49, LP2-55, LP2-51 (92),
LP2-32 (121), LP2-22 (131), LP2-14 (137), LP2-15 (159), LP2-53 (179), LP2-06 (196)**. The phase 10
control that missed at z 3.1 sat on LP2-15, the shortest control page. Every "excluded" in §§8–22
now reads with that qualification; the tables in `results/power.md` give the per-family numbers.
A secondary rule for short pages (z ≥ 4, rank first within family, readable) would have power there,
since rank is not length-limited, but it is not pre-registered and has not been run.

**2. The closing claim did not follow (high).** §22 ended by saying that what remains is "key material
that was never published". A search over one key library and one mechanism cannot show that:
untested texts, encodings, start states and mechanisms remain open, and two of the lane's own
planted controls scored below its cutoff. The status header, §7, §11 and §22 are reworded to what the
evidence supports: no accepted decoding exists within the tested configurations, at the stated
detection limits, on pages long enough for the rule to have power.

**3. The decoder could take at most two consecutive rejections (medium).** Under a hard rule a run of
k equal key symbols that all collide forces k rejections at one position; `score.decode` allowed one
skip plus the doubled-letter double skip. It now takes `max_skip` (default 4). `test_skip.py` confirms
the reviewer's minimal case (plaintext 5 6, key 2 1 1 1 2: the three-rejection path did not exist; it
does now, and on a two-rune text the unigram model then prefers rune 7 to rune 6, a tie-break between
two valid encryptions, not a coverage gap) and on 160-rune English with runs injected at 15 % the old
bound lost 5 % of plaintext positions (0.938 against 0.988 recovered). A census of the key library
(`results/skip_consistency.md`) finds runs of three or more equal symbols only in the 29 constant
"shift" keys and 14 one-letter Vigenère words, which a hard rule cannot use at all (a collision never
resolves), and in two four-word phrase keys. Every sweep before this date ran with the two-rejection
bound; given that census, none is materially affected, and they have not been rerun.

**4. Reuse-detector calibration (medium).** Two errors in §6 and `results/diff_score.md`: the null
moments were interpolated only up to 250 runes, so overlaps of 251–277 runes used the 250-rune
moments (the permutation null is computed the same way, so the verdict stands, but the longest
pairs' sigmas carry a small bias; the table now extends to 300 and the scan has not been rerun); and
"a quarter of the pages sharing a stream gives a quarter of the pooled signal" was wrong, since
shared pairs scale with the square of the page fraction: 13 of 55 pages is 78 of 1,485 pairs, about
7 sigma pooled rather than 34, and a cluster of seven or fewer pages is below two sigma pooled and
below five sigma per pair, and these are expected values rather than detection guarantees. Phase 2's
conclusion now says no detected large-scale aligned reuse; the planted-cluster simulation the second
review asked for was run on 2026-10-28 (§36): about 20 aligned pages for 90 % detection, none under
key-skip drift.

**5. "Independent key" overstated (medium).** The doublets note said an independent key hits a doublet
one time in 29 "whatever it does". That needs the key's successive differences to be uniform, not
independence alone: a constant key is independent of the text and keeps every plaintext doublet. §4,
§5, §7 and `results/doublets.md` now say so; what is rejected is the simulated constructions, not
every independent-key cipher.

**Reproducibility.** Phase 10 ran at a null prior of −0.8 while the code default was the Bayesian
−1.27. The default is now the run value, and the prior and decoder bound are written into every
result file (`results/phase10.json` carries the values the run used). Runtime of this section: the
power lane 11 minutes, the consistency test under a minute.

The reviewer's summary is the right one for the repository as a whole: a reproducible investigation
with strong foundations, and no support for calling the key families exhausted or the missing
material unpublished.

## 24. Short-page lane: a secondary pre-registered rule for the pages the z ≥ 6 rule cannot see (`src/shortpage_lane.py`, `results/shortpage.md`)

§23 left nine pages on which the main rule has under 80 % power. The correct key's rank within its
family did not fall with page length in the power lane, so a second rule was written into the lane's
docstring before any of the nine pages was scored. A cell counts as a candidate only if all of:
(1) z_uni ≥ 4 over the page's own null of 2,000 random keystreams through the identical decoder;
(2) the key leads its family: a hypothesis is one key, its z_uni the best of its six sign × F cells,
and it must have the largest such z_uni among the family's keys on that page; (3) z_big ≥ 3, the
bigram log-likelihood ratio of the decoded text against the bigram LLR of the random keystreams'
decodes, a statistic the unigram decoder does not maximise; (4) for the null lane, the §22 margin of
20 nats over the base decoder; (5) it reads as English to a human. Lane A is the soft rule with the
base decoder, lane B the hard rule with 22 % nulls and the free-null decoder at −0.8. Key library:
`families.ALLSETS` only, the phase 3 book streams and phase 4 phrase keys, 22,863 configurations,
about 45,700 tests per page and lane. The mechanisms of phases 6–9 (word-edge events, skip-by-two,
LCG and feedback families, cumulative-Gematria offsets) are not in this lane.

**Two amendments, both recorded in the docstring, both looser than the wording they replaced.** Rule
(2) was first written as rank among cells; the controls failed it 16 times in 18 because the same
key decoded under the other F variant, whose null is tighter, outscored the planted cell, so it was
changed to rank among keys before any page result was read. A second external review of commit
2b2456f then found that the implementation still required the candidate to be the key's
highest-z_uni cell, so a key whose best-unigram cell failed the bigram test while another cell passed
both was dropped; any cell of the leading key may now pass, and the whole lane was rerun with
controls raised from one to five plants per page length and lane.

**Controls, five plants per length per lane** (66, 76, 92, 121, 131, 137, 159, 179, 196 runes;
nine families, signs and F variants cycled; `results/shortpage.md` has every plant):

| lane | 66 | 76 | 92 | 121 | 131 | 137 | 159 | 179 | 196 | all |
|---|---|---|---|---|---|---|---|---|---|---|
| A (soft rule) | 4/5 | 5/5 | 4/5 | 5/5 | 4/5 | 5/5 | 4/5 | 4/5 | 4/5 | 39/45 |
| B (hard rule + nulls) | 2/5 | 2/5 | 4/5 | 4/5 | 2/5 | 5/5 | 5/5 | 4/5 | 3/5 | 31/45 |

All six lane A misses are self-running-key or primes+1 plants at z_uni 6–12 that lost rank (2) to
the neighbouring offset of the same stream, which passed (1)–(4) in their place; the rule finds the
stream and not always the exact offset. In lane B, 6 of the 14 misses are the same neighbour effect
and 8 are genuine power limits (z_uni or z_big below threshold, all but one at 66–92 runes). So on
these lengths the rule sees a planted soft-rule solution from this library about nine times in ten,
and a planted null-lane solution about two times in three, falling to under half at 66–76 runes.

**Result: null.** No page in either lane produces a candidate meeting (1)–(4), so (5) was never
reached. The chance load was real: 128 cells at z_uni ≥ 4 across the nine pages, 48 of them on LP2-14
and 42 on LP2-15 in lane B; every one failed rank, bigram or margin. Largest z_uni on a page: lane A
4.71 (LP2-55, a reversed three-word phrase), lane B 5.41 (LP2-14, the self-running key the §22 sweep
also ranked first there, gibberish). Runtime 23 minutes.

**What this adds, and no more.** It is a further negative search over the phase 3–4 library on the
nine short pages under two mechanisms, with the detection rates above. It does not carry the
phase 6–9 mechanisms to those pages, which remain inconclusive there as §23 states; it does not make
the null lane conclusive at 66–92 runes, where the rule sees a plant less than half the time; and
with five plants per cell the rates are estimates with wide intervals, not power curves.

## 25. External running-key lane: the texts Cicada pointed at, decoded exactly at every offset (`src/runkey_lane.py`, `src/corpus.py`, `results/runkey.md`, `data/corpus/`)

The ledger check that opened this lane (`results/ledger_diff.md`) showed the community's main
hypothesis had already been run: wazar's Campaign XVIII swept about 200 texts with a validated
skip-tolerant beam through a prefilter (recall 7 of 8 per page, signs c ± k, atbash variants), and
jens-wedin ran eight texts forward and reversed with controls. What neither documents is exact
scoring at every offset, the Beaufort convention, both F-rule variants and a reversed text on every
text, a second transliteration, or power by page length. This lane closes those gaps; it does not
test a new idea, and it was expected to be null.

**Corpus** (`data/corpus/`, SHA-256 and URLs in `SOURCES.md`, built by `src/corpus.py` with the book's
digraph transliteration V1 and a letter-by-letter V2): the four texts with documented book-cipher use,
Crowley's *Liber AL*, Guest's and Bulfinch's *Lady of the Fountain*, Emerson's *Self-Reliance* and
Gibson's *Agrippa* (copyrighted, hashed, not committed), with Blake's *Marriage of Heaven and Hell*,
the Anglo-Saxon Rune Poem and the Cypherpunk Manifesto; the full *Essays*, the full *Mabinogion*,
*The King in Yellow* and the *Kybalion* at sentence-start offsets only. A Quorum panel asked the same
day (quorumsays.com/q/JOkSnnZ5csJf) named the same four book-cipher texts and nothing outside this set.

**Pre-registered rule**, committed before any page was scored (f893b77): z_uni ≥ 7 over the page's own
2,000-keystream null (the chance maximum over 1.5 × 10⁸ tests is about 6.1), bigram z ≥ 3 as in §24,
readable. **Controls:** 17 plants of solved English under the soft rule with a corpus text at a random
offset, signs, F and direction random; 15 pass. The two misses are 92-rune plants whose correct offset
was found at z 6.4 and 6.6, under the bar, the short-page limit of §23. **Edition sensitivity**, measured
on *Liber AL*: a one-rune difference inside the page window costs about one sigma, a five-rune
difference at mid-page drops the correct key to about 6.6, so a key text whose online transcription
differs from the author's by a few runes near the middle of a page sits at the bar. A second
transcription of each short text would remove that limit and has not been fetched.

**Result: null.** 153,149,370 tests over 55 pages, 3 signs × 2 F, both directions; largest z_uni
5.46 (LP2-03, Guest's *Lady of the Fountain* at offset 19,307, gibberish); 15 cells at z ≥ 5, none
at 6, none meeting the rule. The best cell per page is spread across the texts (Guest 12 pages,
Self-Reliance 8, Blake 8, the Rune Poem 7), which is what noise looks like. Runtime 383 minutes on
the longest of seven shards. Not covered: the 29 esoteric texts wazar fetched and never ran, the
long texts away from sentence starts, transcriptions other than the ones hashed here.

## 26. Page-image lane: is there information in the images that the transcription does not carry? (`src/image_lane.py`, `results/images.md`, `docs/human-vs-machine-key.md`)

The 75 page images of the scream314 archive (2400 × 3600 JPEG; SHA-256 of every file in
`data/images/SHA256SUMS.txt`, files themselves gitignored) were tested with the 19 solved or
decorative pages as the control group, the tests and flag margins fixed in the module docstring
before any unsolved image was measured. Four tests. **Container:** bytes after the JPEG end marker,
marker segments, quantization tables, embedded profiles. **Chroma:** share of pixels that are
coloured but are not the book's red ink. **LSB:** the classic least-significant-bit chi-square on
the paper background. **Glyph geometry:** Otsu binarisation, connected components inside the text
column, rows by y-clustering, then per page the dispersion of letter gaps and of baselines and the
kurtosis of the gap residuals (a one-bit channel in the spacing would be bimodal), with the
component count checked against the transcription's rune count.

**What the first run found, and the one amendment.** Every one of the 58 second-part images carries
an identical 2,576-byte sRGB ICC profile that none of the 17 first-part images has, and the 23
second-part pages with no red ink or border art were saved as grayscale. That flagged 26 unsolved
pages on the container test against a control group that was mostly first-part pages. It is an
export-batch difference, not a per-page signal: the two solved second-part pages (An End, Parable)
carry the same profile, and the profile bytes are identical on all 58. The container test was
restratified to the second-part controls and the lane rerun; the LSB test is kept but recorded as
uninformative, since JPEG-decoded pixels saturate it on every image, control or not.

**Result: null.** No trailing bytes on any page; no marker set or quantization table that the matching
controls lack; non-red chroma lower on unsolved pages (0.06 % of pixels) than on controls (0.12 %);
component counts within 5 % of the rune counts on the text pages (LP2-00: 276 components, 262
runes, the rest separators). The geometry is the informative part: unsolved pages are *more* regular
than the decorated solved ones, letter-gap sd 9.4 ± 1.5 px against 11.9 ± 4.6, baseline sd 2.5 against
11.8 (the controls include pages where art intrudes on the text column), and baseline residuals on
plain text pages sit at 0.2–0.3 px, which is what a page rendered from a PDF should give and leaves no
room for a spacing channel. Gap kurtosis is positive everywhere (heavy tails from word separators),
never bimodal. The only geometry flag in the first run was LP2-50, the page that carries no runes
but a grid of two-character codes; it is excluded from the geometry tests as a non-text page. Runtime
64 seconds.

**What this does and does not cover.** It covers the archive's JPEGs as distributed. It does not
cover the PDF or PostScript source that wazar's finding (a Ghostscript and ImageMagick pipeline)
implies existed, which is not public; nor the two-character-code page LP2-50 as a cipher in its own
right; nor steganography robust to JPEG recompression, for which the only test with power would
need the original files. Leo-Y-Zhang's scan of the raw image bytes as running keys and wazar's
OutGuess sweep are the other image negatives on record. **The machine-versus-person question** the
doublet statistic raises is written up separately in `docs/human-vs-machine-key.md`: the lag-2,
lag-3 and lag-4 repeat counts at chance, the homogeneity across pages and the rune-blindness of the
suppression all favour a one-lag mechanical rule over a hand, which is the case for finishing the
generator families rather than the key-text families.

## 27. Rune 5-gram rescoring: the short-page power fix, measured and applied (`src/ngram.py`, `src/rescore_power.py`, `results/rescore_power.md`, `results/shortpage_rescore.md`)

§23 left the main rule underpowered below about 92 runes because the decoder judges English by letter
frequencies. An interpolated Kneser-Ney 5-gram over runes, trained on the 1.34 million runes of the
§25 corpus (`results/ngram5.npz`, rebuilt in 30 s), scores held-out solved plaintext at −1.96 nats per
rune against −3.37 for uniform, roughly three times the per-rune discrimination of the unigram model.
It cannot run inside the Viterbi, which must stay memoryless, but it can rescore what the Viterbi
decodes. On the §23 plants (soft rule, four families, 20 per cell, 400 nulls):

| length | share at z_uni ≥ 6 (§23 rule) | share at z_5 ≥ 6 (rescored) | median z_uni → z_5 |
|---|---|---|---|
| 66 | 0.21 | **0.99** | 5.6 → 26 |
| 76 | 0.54 | **1.00** | 6.0 → 27 |
| 92 | 0.94 | **1.00** | 6.8 → 30 |
| 121–196 | 1.00 | **1.00** | 8–10 → 35–45 |

**Applied to the nine short pages** with a rule written before the run (`shortpage_lane.py`, `RESCORE=1`:
z_uni ≥ 3.5, key leads family by z_5, z_5 ≥ 6 against a chance ceiling near 4.6, the §22 margin for
the null lane, readable; five controls per page length and lane). Lane A, the soft rule: 39 of 45
controls pass, every miss a neighbouring offset of the same stream passing instead; **zero candidates
on all nine pages.** Lane B, the hard rule with fillers: 6 of 45 controls pass, because inserted
filler runes break the n-gram context, so the 5-gram is the wrong second statistic for that lane and
the §24 bigram rule (31 of 45) stands for it; zero candidates there too. Runtime 60 minutes.

**Where the exclusions stand after this.** Within the phase 3–4 key library: the soft-rule exclusion now
holds on all 55 pages at measured power of 99 % or better; the filler-lane exclusion holds on 52 pages
and remains inconclusive on LP2-49, LP2-55 and LP2-51. The phase 6–9 mechanisms were not carried to the
short pages. The 5-gram is also the readability statistic for §25 and §29.

## 28. Windowed dispersion: a test for a human hand that turned out to have no power (`src/dispersion.py`, `results/dispersion.md`)

`docs/human-vs-machine-key.md` proposed one more discriminator between a hand-made and a
program-made anti-repeat key: people keep short windows of a "random" sequence more evenly
populated than chance, so the key's 50-rune windows should be under-dispersed if a hand made it.
The key is masked by the plaintext, so the note proposed the ciphertext difference stream as the
observable. Three generators were simulated at the real page lengths with solved-page English and
the soft re-draw, each producing the observed doublet count: an iid key, a permutation-bag key
(every 29 symbols a permutation, the strongest balancing) and a recent-avoid key (a draw rejected
half the time if seen in the last six).

**The proposal was wrong and the test has no power.** A key's local balance does not survive
differencing: on the difference-stream statistic the three generators give windowed chi² 29.12,
29.18 and 29.10 with sd 0.45. A statistic on the ciphertext itself, added after that was seen and
before its observed value was read, separates the bag key from iid by only 1.5 sd through the
plaintext. The observed pages sit at z −0.1 to −0.5 from the iid generator on all three statistics,
consistent with a machine and saying nothing against a hand. No verdict; the lag-2 repeat count of
§21 remains the one measurement that bears on the question. Recorded here so the proposal is not
made again. Runtime 3 minutes.

## 29. The two "Know This" squares as key material (`src/square_lane.py`, `results/squares.md`)

Page 16 of the book carries a 5 × 5 square of numbers whose rows, columns and diagonals sum to 3301;
page 5 a 5 × 5 square mixing numbers with eleven rune words (SHADOWS, AETHEREAL, BUFFERS, VOID, CARNAL,
OBSCURA, FORM, MOBIUS, ANALOG, MOURNFUL, CABAL) whose Gematria values complete a square summing to
1033, which is 3301 reversed; both are prime, and the 1033 matrix was handed to solvers out of band
during the 2014 onion stage before the book was reached. The words were chosen for their values. They
are the only numeric objects in the readable part of the book and the most literal reading of "their
numbers are the direction".

**Pre-registered lane** (docstring written before scoring): the two value matrices in six reading orders
and concatenated, as periodic keys mod 29 and as decimal digits; the 50 values as offsets into the
prime and totient streams; the eleven words and three phrase orders as Vigenère keys; 92 keys
× 3 signs × 2 F × 55 pages = 30,360 tests, soft-rule decoder, 2,000-keystream nulls, rule z_uni
≥ 5 and 5-gram z_5 ≥ 6 and readable. Not run, with the reason recorded: the squares' values as LCG
seeds, because §19 ran those generators at every seed; transposition keyed by the squares, because the
detection statistic is blind to symbol order, so scrambled English under any key tested in §§9–25 would
already have scored as a hit. **Controls:** eight plants across the three families at 262, 137 and 92
runes, all signs and F; 8 of 8 pass at rank 1 (the first run failed every `add` plant at z ≈ 0, a sign
convention error in the planting code, fixed and rerun; the decoder side was right throughout).

**Result: null, and not close.** Largest z_uni 3.60, largest z_5 2.61, against a chance maximum near 4.6;
no cell meets the rule. The squares do not key the pages under the anti-repeat rule in any direct
form. What remains open for them is indirect use: as a seed to a generator not in §19's set, or as an
index into the page the hash on page 73 names. Runtime 4 minutes.

## 30. Provenance: the signed messages verify by full fingerprint (`src/verify_pgp.py`, `docs/pgp-verification.md`, `data/raw/pgp/`)

A 2026-10-27 claim that the April 2017 "Beware false paths" message was a PGP hoax was checked
directly: Cicada's key fetched by its 160-bit fingerprint (6D85 4CD7 9333 22A6 01C3 286D 181F 01E5
7A35 090F, RSA-4096, created 2012-01-05), three messages from the pinned archive verified with an
independent OpenPGP implementation. The April 2012 denial, the January 2016 "Liber Primus is the way"
message and the April 2017 warning all verify with that one key. Some archived copies carry a
trailing space on a line and fail in a verifier that does not canonicalise whitespace as RFC 4880
requires; that is a property of the copy, and the likely seed of the hoax story. Nothing signed by
Cicada after January 2014 is a puzzle; the unsigned 2016 "Pi Mobi" puzzle is what the 2017 message
warned about.

## 31. Seeded generators no ledger lists: xorshift, PCG32, MINSTD, RANDU, SplitMix64 (`src/generator_lane.py`, `results/generators.md`)

The ledger check that opened this lane narrowed it before it ran. pnotisdev has swept ten common
generators (php, glibc, .NET, Python 3 and 2.7, mt32/mt31, Java, MSVC, drand48, Ruby) over every
32-bit seed on a GPU with a skip-aware score, small seeds per page, timestamp seeds, 199,088 OEIS
sequences, 19.2 million passphrase hash streams and 719,280 KDF streams; wazar ran a 2.5 × 10⁹-decode
seed sweep, the Python 2.7 word-seed space, Perl and TeX generators, 323 semantic seeds including 3301,
and the Marsaglia CD-ROM. So the squares and 3301 as seeds for the common generators, and book words
through hashes, were not run again here. **Run here:** eight generators no ledger lists, each a
one-screen routine a 2012–14 programmer might have pasted: xorshift32, xorshift64, xorshift128,
PCG32, MINSTD (16807 and 48271), RANDU and SplitMix64, each under three reductions of a 32-bit output
to a rune (mod 29, top bits, rejection), seeds 1 to 262,144 densely plus 35 named seeds (3301, 1033,
809, the 50 values of the two Know This squares, the puzzle dates, 509, 503, 845145127). Two keying
modes are covered by construction, a stream restarted on every page and one global stream.

**Pre-registered two-tier rule.** Tier 1: the first 80 runes of LP2-00, LP2-01 and LP2-02 under every
seed × reduction × 3 signs × 2 F with the soft-rule Viterbi, survivor at z ≥ 4.5 over the window's
random-keystream null (about 90 % of true keys at 80 runes, §23). Tier 2: the survivor's full page at
z_uni ≥ 6 and 5-gram z_5 ≥ 6, then readable. **Controls:** one plant per generator, random seed,
reduction, sign and F; 8 of 8 pass, found at rank 1 in tier 1 among 4,096 neighbouring seeds and at
z_uni 11–16 in tier 2. **Calibration:** the tier-1 maximum per block of 674,172 real-page tests ran
4.1–4.9, the chance level.

**Result: null.** 113,261,328 tier-1 window decodes; 31 survivors at z ≥ 4.5 (about the 30
chance expects); 31 tier-2 decodes; largest full-page z_uni 4.72 (xorshift128, rejection reduction,
seed 63113, LP2-00, gibberish), largest z_5 1.68; no candidate. Runtime 122 minutes on seven shards.
Not covered: seeds above 2^18 for these eight generators (a dense sweep to 2^32 would take the GPU
pipeline pnotisdev built), other reductions, generators nobody has named. With this, the generator
family is closed to the extent anyone has named a generator; what remains open on the mechanical
side is non-additive constructions, above all a keyword-mixed alphabet under a Vigenère-style key,
which every additive decoder in every lab is blind to and which pnotisdev lists as open.

## 32. Keyword-mixed alphabets under the book's keys: quagmire I–IV (`src/quagmire_lane.py`, `results/quagmire.md`)

Every decoder in every lab, this one included, assumes the key is added to the plaintext in the fixed
rune order. If the author mixed the alphabet with a keyword on either side, the classical quagmire
constructions, every additive sweep was blind to the correct key and the anti-repeat fingerprint is
unchanged, because the rule acts on the output. pnotisdev lists a keyword-mixed outer alphabet as open;
no ledger records a run. A Quorum panel asked the same day (quorumsays.com/q/EmEfDcbkkmyy) made the one
sound objection: under a short *periodic* key, positions at the same phase share one substitution
whether or not the alphabet is mixed, so pnotisdev's drift-aware periodic test already constrains that
part; the panel's claim that only a running-key quagmire survives was marked overstated by its own
scorer. What no test touched is a mixed alphabet under the book's *non-periodic* streams.

**Model and library.** A mixed alphabet is a keyword's runes without repeats followed by the rest in
Gematria order. Q1 mixes the plaintext side, Q2 the ciphertext side, Q3 both with one keyword, Q4 both
with two. Keywords: the 255 distinct words of three or more runes in the solved pages, the eleven
Know-This words and a dozen Cicada terms; Q4 pairs from the 30 most salient (870 pairs); 1,635
alphabet configurations. Keys: the §9 word keys forward and reversed and the prime, totient, prime+1,
Fibonacci and Lucas streams at every start, 869 keys, 331 of them non-periodic. Decoding is the
additive decoder on the relabelled ciphertext with the unigram model relabelled by the plaintext
alphabet; the random-keystream null moves by under 0.1 sigma under a mixed ciphertext alphabet
(measured on five keywords per shard) and is shared.

**Pre-registered two-tier rule**, as §31: tier 1 on the first 80 runes of LP2-00, LP2-01 and LP2-02 at
z ≥ 4.5; tier 2 full page at z_uni ≥ 6 and z_5 ≥ 6, then readable. **Controls:** eight plants, two per
form, random alphabets and keys, signs and F cycled; 7 of 8 pass at rank 1 among all 1,635 × 869
configurations, and the eighth (Q4, KOAN/MOBIUS, a totient stream) clears both tier-2 bars at rank 2
behind an equivalent alphabet pair, the same near-duplicate effect as the neighbouring offsets of §24.

**Result: null.** 25,574,670 tier-1 window decodes, 8 survivors at z ≥ 4.5 (chance expects about 85;
the shortfall reflects the correlation between alphabets sharing most of their order), 8 tier-2
decodes, largest full-page z_uni 5.15 with z_5 −2.1 (Q4, TOTIENT/FIRFUMFERENFE, the word key SOME on
LP2-00, gibberish), no candidate. Runtime 42 minutes on seven shards. Not covered: alphabets mixed by
words outside the book, mixed alphabets with the other labs' key families (external texts, PRNG seeds),
alphabets built by rules other than keyword-then-remainder. With this the one named non-additive class
is closed for the book's own keys and words.

## 33. Where the 86 repeats sit: boundary-blind (`src/doublet_boundaries.py`, `results/doublet_boundaries.md`)

The §32 panel's useful residue was a test, not a mechanism: a chain or stepping cipher that resets at
word, line or page starts cannot emit an adjacent repeat except across a reset, so its 86 repeats would
sit at boundaries, and a transcription artefact at line ends would cluster there too. Against the master
transcription's own separators: repeats inside words 60 (64.3 expected if boundary-blind), across word
boundaries 21 (17.3), across clause boundaries 1 (0.9), across line boundaries 4 (3.6); every class
within one sigma; positions within pages uniform (Kolmogorov–Smirnov p = 0.63). The reset-chain family
and the artefact reading are excluded; the anti-repeat mechanism acts uniformly on the stream. The
panel's own summary stands as the cleanest statement of where this leaves things: a stream whose only
structure is a uniform, rune-blind one-lag ban carries exactly one law, every mechanism tuned to that
law yields the same distribution, and only implementation leaks are testable. Sections 21, 28 and this
one have now tested the leaks anyone has named.

## 34. The three-page base-60 payload as key material: a controlled replication (`src/payload_lane.py`, `data/processed/payload.json`, `results/payload.md`)

Pages LP2-49, LP2-50 and LP2-51 carry, beside or instead of runes, 80 + 104 + 72 = 256 two-character
tokens, a digit 0–4 and a character from [0-9A-Za-z], read by the community as base 60 (digit × 60 +
index) and giving 256 values all below 256: a byte string. Six positions are contested where the glyphs
I/l and O/0 cannot be told apart, and both readings are carried here. **Ledger first:** wazar has
tested this payload as a PRF seed expanded by RC4, AES-CTR, SHA counters, HMAC-DRBG and ChaCha20, as
an RSA signature under every known Cicada modulus, as meta-parameters, as a direct numeric key at every
offset, and in a pointers track. So this lane is a replication under this repository's exact decoder
with controls of the direct and pointer readings; the PRF expansions are not repeated.

**Readings** (341 keys, all under 3 signs × 2 F on all 55 pages): byte mod 29, rejection (bytes ≥ 232
dropped), bit-reversed bytes, the base-60 index and digit components, each forward and reversed and for
both readings of the contested bytes; each distinct byte as an offset into the prime and totient
streams; the solved plaintext's rune at each byte, and the solved text's word at each byte as a
256-word phrase key. Rule: z_uni ≥ 5 and 5-gram z_5 ≥ 6 and readable. **Controls:** four plants across
the reading families at 262 and 137 runes, 4 of 4 at rank 1.

**Result: null.** 112,530 tests; largest z_uni 4.86 (LP2-43, prime offset p[n+112], gibberish), largest
z_5 1.95; no candidate. Runtime 4 minutes. The direct and pointer readings of the payload do not key the
pages under the anti-repeat rule; wazar's PRF-expansion negatives stand beside this one. What remains
for the payload is what remains for the hash on page 73: its meaning, if any, is outside the book.

## 35. Every archived artefact against the page-73 hash (`src/hash_sweep.py`, `results/hash_sweep.md`)

Page 73 gives the SHA-512 of a deep-web page and tells the pilgrim to find it; the page was never found
and the Tor v2 network that served it is gone. What can still be checked is the archives. 502 distinct
files from the scream314 archive (every non-image file: onion mirrors, HTML, text, binaries, decoded
outputs), wazar's primary artefacts (signed messages, payloads, mirrors), the 75 page images, the signed
messages and the transcription were hashed under 3,977 readings of "the page": raw bytes, hex, base64,
newline and trailing-whitespace normalisations with and without a final newline, HTML stripped to text
and collapsed, lower-cased, plus the 256-byte payload in seven forms. **No reading of any held artefact
hashes to the target.** wazar's whole-file sweep over its own holdings had reached the same result; this
one enumerates the readings. The page, if it exists anywhere, is not in the public archives.

## 36. Planted-cluster power of the key-reuse test (`src/reuse_power.py`, `results/reuse_power.md`)

The second external review asked for this: §6 had stated expected pooled sigmas for clusters of pages
sharing one keystream, not detection rates. Here k of the 55 pages are enciphered with one shared stream
(solved-page English at the real page lengths, the others independent), under two anti-repeat mechanisms
that differ for this test: in-place REWRITE, where the output rune is resampled and the key stays in step,
so shared pages stay aligned; and KEY-SKIP, the §5 re-draw, where the key index advances and shared pages
drift apart after the first skip. The §6 pooled statistic at offset 0, 30 replicates per cell.

| pages sharing one key | rewrite: pooled z | detected (pooled ≥ 5) | key-skip: pooled z | detected |
|---|---|---|---|---|
| 2 | 0.5 ± 1.0 | 0.00 | 0.7 ± 0.9 | 0.00 |
| 3 | 0.6 ± 0.8 | 0.00 | 0.5 ± 1.1 | 0.00 |
| 4 | 0.7 ± 1.0 | 0.00 | 0.4 ± 1.0 | 0.00 |
| 6 | 1.6 ± 0.9 | 0.00 | 0.8 ± 1.1 | 0.00 |
| 8 | 2.3 ± 1.1 | 0.00 | 0.9 ± 1.1 | 0.00 |
| 11 | 3.7 ± 1.2 | 0.07 | 1.4 ± 1.0 | 0.00 |
| 13 | 5.4 ± 1.2 | 0.63 | 1.6 ± 1.0 | 0.00 |
| 20 | 11.5 ± 1.4 | 1.00 | 3.2 ± 0.9 | 0.03 |
| 55 | 88.4 ± 2.5 | 1.00 | 21.1 ± 2.6 | 1.00 |

**Reading.** Under an aligned mechanism the pooled rule reaches 90 % detection only at about 20 shared
pages (63 % at 13, 7 % at 11); under key-skip drift it detects nothing short of the whole book. §6, §7
and §23 now say so. pnotisdev's ledger records the same limit as "pad reuse under skip drift: untestable".
A shared key under the key-skip rule is a hypothesis no test in any lab has power against; it is also one
with nothing pointing at it, since the pages' difference streams show no structure at any offset.

## 37. Repeat spectrum, null models and the boundary convention (`src/lag_spectrum.py`, `results/lag_spectrum.md`)

Two Quorum panels (quorumsays.com/q/1CHmMxwoj6rH, OHUxs3Jget6b) asked whether the deficit is uniform in
lag, what null produced the expectation, and whether it survives the page-boundary conventions.
Repeats at lags 1–120 within pages: lag 1 at z −17.3; lags 2–120 mean z −0.17, sd 0.98, one lag of 119
at |z| ≥ 3 (lag 11, −3.1; chance expects 0.3 such lags). The deficit is at lag 1 only, which also answers
the panel's lag-spectrum check. **Null models:** 12,901 pairs / 29 = 445 under uniform runes; 12,901 ×
Σ p_i² = 446 under the observed rune frequencies (index of coincidence 0.0346); the "447" seen elsewhere
is the second with a different pair count. **Boundary convention:** the 54 page joins carry 0 doublets
(1.9 expected), so counting them changes nothing, and no 55-, 56- or 58-page convention can move the count
by more than the joins it adds. **Per-page uniformity** was established in §21 and is restated: chi²
58.5 on 54 degrees of freedom, 14 zero-doublet pages against 13.5 expected.

## 38. Blinded glyph-level re-reading of the unsolved pages (`src/reread_lane.py`, `results/reread.md`)

Every lab's negatives rest on one transcription. Two panels independently put a blinded re-reading
first (§37's and quorumsays.com/q/Gt7EN7uFnoNk), because a stateful cipher test on a misread string is a
test of a different object. **Method:** glyphs are connected components of the binarised page inside the
text column, ordered into rows (§26's pipeline, with a rune drawn as two overlapping strokes merged);
training labels come from the solved pages, first by rows whose glyph count equals a transcription
line's, then re-aligned twice by reading each row with a model trained on the other pages and pairing it
with the line it agrees with best; classifier 3-nearest-neighbour by cosine similarity on 32 × 32 crops,
2,763 labelled glyphs from 17 solved images, all 29 runes present. **Validation before reading:**
leave-one-page-out accuracy 99.71%; a component is resolved if its nearest training glyph
is at least as similar as 99.5 % of held-out glyphs were (T = 0.986), which keeps 99.5 % of held-out
glyphs at error 0.07%. **Blind reading:** the 55 unsolved pages with runes (the base-60
grid rows of LP2-49 and LP2-51 excluded by layout). **Reconciliation after reading**, by sequence
alignment of the resolved reading against the community string.

**Result.** At the **12,807 aligned glyphs the blind reading disagrees with the transcription
0 times** (held-out classifier error would predict about 9); adjacent repeats on the blind reading **84**
against the transcription's 86; **149 positions (1.2%) could not be read**, every one a
transcription rune the segmenter failed to isolate (never a glyph the transcription lacks), 64 of them ᚳ,
which touches its neighbour in this font and merges into one component the classifier declines. A
width-based splitter was tried and withdrawn (it cut wide runes such as ᛠ in two). **Pre-registered
verdict: NOT confirmed**, because criterion (a), resolved-glyph count within 3 of the transcription on at
least 50 pages, held on only 32 pages; criteria (b) and (c) held. That criterion was
written to catch a transcription that invents or drops runes, and what it caught instead is the
segmenter's merges, so the honest statement is narrower than "confirmed" and stronger than "not
confirmed": at 98.85 % of positions the independent reading reproduces the community transcription
exactly, and the remaining 1.15 % are unread, not disputed. They are listed by page and position in
`results/reread.md` for the eye. The first run, before the stroke-merge fix and with position-wise
comparison, is kept as `results/reread_run1.md`.

## 39. Phases 6–8 carried to the nine short pages with the 5-gram rule (`src/rescore5.py`, `results/phase6_short.md`, `results/phase7_short.md`, `results/phase8_short.md`)

§23 left the phase 6–9 mechanisms inconclusive on the nine pages under about 200 runes. The phase 6
(word-edge events), phase 7 (skip-by-two rejection) and phase 8 (LCG seeds and position-walking
multipliers) lanes gained a short-page mode: pages restricted to the nine, controls planted at 92–196
runes instead of 240, and every recorded top cell rescored with the rune 5-gram against 400 random
keystreams through the same decoder; the §27 rule, z_uni ≥ 3.5 and z_5 ≥ 6 and readable.

| lane | controls passing (short lengths) | largest z_uni on the nine pages | largest z_5 | candidates |
|---|---|---|---|---|
| phase 6, word-edge events | 22/24 | 5.19 | 2.2 | 0 |
| phase 7, skip-by-two | 24/24 | 4.69 | 2.6 | 0 |
| phase 8, LCG seeds and multipliers | 15/16 | 4.45 | 2.0 | 0 |

**Result: null** on all three, with the controls showing the rule sees a planted solution at these
lengths. The phase 6 misses are the kinds whose events the 5-gram cannot see through (unkeyed nulls break
n-gram context, as in §27's lane B). Of the mechanisms in this repository only phase 9's, the
cumulative-Gematria offsets and the global streams, have not been carried to the short pages.

## 40. The pilgrim texts as running keys (`src/corpus.py` with `CORPUS_SET=pilgrim`, `results/runkey_pilgrim.md`)

The book calls its reader a pilgrim twice and no lab had run the texts that word points at. Bunyan's
*The Pilgrim's Progress* (Project Gutenberg #131; its first 50,000 runes exactly at every offset in both
directions and both transliterations, the whole at sentence starts) and Chaucer's *Canterbury Tales*
(#2383, Middle English, sentence starts only) went through the §25 lane unchanged: 3 signs × 2 F, 2,000
random-keystream nulls per cell, the pre-registered rule z_uni ≥ 7 and z_big ≥ 3 and readable. *The Way of
a Pilgrim* was not run: no free text was found. **Controls** 3 of 3. **Result: null.** 40,083,780 tests;
largest z_uni 5.21 (LP2-44, Chaucer at offset 692,709, gibberish), six cells at z ≥ 5, none at 6, no
candidate. Runtime 105 minutes on seven shards. The corpus files and hashes are in `data/corpus/` and
`SOURCES.md`.


## 41. Field survey (2026-10-28) and the closure bundle it prompted (`results/field_survey_2026-10-28.md`, `src/closure_bundle.py`, `results/closure_bundle.md`, `src/wordlen_repeats.py`)

A GitHub search over eight query variants returned 213 repositories; 45 carry analysis or claims about the unsolved pages and were read as data (never executed). The survey file has the lab table, the field consensus, the claims that can be dismissed, a cross-reference of every section here against pnotisdev's 148-row registry, and three corrections to `ledger_diff.md`. Its ranked list of checks done elsewhere but not here was then worked through cheapest first; this section and the next three are the results.

**The anti-repeat rule is specific to the unsolved section.** The five solved polyalphabetic pages (Vigenère DIVINITY ×2, FIRFUMFERENFE ×2, the totient-stream page) carry 27 adjacent repeats in 914 pairs, 0.86 of the uniform rate; the unsolved pages carry 86 in 12,900, 0.19 of it (Fisher exact p = 3 × 10⁻⁹). §4 had the per-page figures; the pooled comparison says the mechanism that removes repeats was not used when Cicada encrypted the pages we can read. [stated — `results/closure_bundle.md` (a)]

**Position parity, repeat context, cross-page n-grams.** The 86 repeats are flat at every modulus 2–8 (chi-square p 0.05–0.98), which excludes a fixed-frame digraphic cipher and replicates Leo-Y-Zhang. Nothing in a repeat's neighbourhood predicts it: the repeated rune's identity (G-test p 0.48), the rune before the pair (0.33), the step into the pair (0.17) and the gaps between repeats (KS p 0.66 against geometric) all sit at their marginals, replicating invictustitan2. Identical 3-, 4- and 5-gram windows across pages exceed a plain within-page shuffle at n = 3 (2,446 against 2,364 ± 32, p 0.005) but not a null that keeps the lag-1 deficit (2,428 ± 29, p 0.27): the deficit concentrates n-grams on the doublet-free types and raises collisions by itself, so the excess is the null's artefact, not the text's. farfromexact's single 4-gram figure (121 against 112) is reproduced exactly. [stated — `results/closure_bundle.md` (b)–(d)]

**Repeated word-length n-grams.** TheronEagle reports a word-length 8-gram shared by pages 22 and 47. Under a shuffle of the 2,896-word length sequence the expected number of identical 8-gram pairs is 1.5 ± 1.5 and the observed is 2 (p 0.41); lengths 5–10 are all at their nulls. [stated — `results/wordlen_repeats.md`]

**The ICC profile.** Every LP2 page image embeds the same 2,576-byte profile, "Artifex Software sRGB ICC Profile, Copyright Artifex Software 2011"; it differs from Ghostscript's current `iccprofiles/srgb.icc` in two low-order bytes of the header illuminant and nowhere else. Dukotah's R30-A3 attribution to Ghostscript 9.06 is consistent with this; the exact release was not pinned here because the tagged files were not retrievable from Ghostscript's git. The pages were rendered through Ghostscript. Separately, all 58 LP2 images used here are byte-identical by SHA-1 to the files of the Internet Archive item `ky2khlqdf7qdznac.onion`, the 2014 hidden service that released them (`data/images/PROVENANCE.md`), so the image lane ran on the originals. [stated — profile bytes compared 2026-10-28, archive metadata checked 2026-10-28; inferred — the release]

**IoC null spread.** Leo-Y-Zhang corrected their index-of-coincidence null from 0.75/√n to the exact form. The nulls here (`src/q.py`, `src/depth_two.py`) already use the exact iid variance √(2π(1−π)/(n(n−1))) with a Monte Carlo check, so no figure in §1–§3 or §36 moves. [stated]

Items from the survey's list that turned out to be covered already: PHP `mt_rand` and glibc `random()` are in pnotisdev's `prng-bg` and `open-bg-sections` rows (all 2^32 seeds, every section, skip-aware), unkeyed insertions are §22 and pnotisdev's `nulledge`, and the 27×27 grid claim is pnotisdev's `layout27` row. A doublet-triggered second key as a mechanism for the deficit is bounded before any decode: a deterministic replacement coincides with the rejected symbol 86/445 = 19 % of the time, while two independent keys coincide 3–4 % of the time, so the family predicts about 15 repeats, not 86, unless it is combined with the nulls of §22.

## 42. The two within-word echoes, replicated, and the word-edge correction that exposed them (`src/kfixed_echo.py`, `results/kfixed_echo.md`, `src/echo_dissect.py`, `results/echo_dissect.md`, `src/edges.py`)

**The bug.** The field's word counts (2,928 in anon5376, 2,896 by the master transcription's word marks) did not match the 3,316 words used by §14, §15 and §39. The transcription marks line ends with `/` and word ends with `-`; 452 of the 630 line ends on the unsolved pages have no `-` before them, so a word continues across the line. The edge builder (`src/edges.py`) and the two new scripts of §41 had treated every `/` as a word boundary. Fixed on 2026-10-28; the edge file now lists 2,873 word edges (was 3,261) and 539 line edges. §33's classes are relabelled (a `/` with no `-` is now "line-wrap inside a word", 388 pairs, 3 repeats against 2.6 expected) and its conclusion is unchanged. [stated]

**Lag 5.** With the correct words, pairs five apart inside a word are equal 102 times among 2,073 pairs. Under a Metropolis null that keeps each page's rune multiplicities, word structure and adjacent-repeat count K = 86 fixed, the expectation is 71.2 ± 8.2: z +3.663, one-sided p 0.001, family-wise p 0.011 over lags 2–12. ZzNible reported 104/2,105, z 3.75, family-wise 0.0116 under the same kind of null; pnotisdev reports the same count. §15's "not replicated" was the over-split segmentation. The rune S carries it: 11 of the 102 echoed runes are S against 3.5 expected (z +4.0), the same 11 pnotisdev found; no other rune exceeds z +2. The echo is not tied to word position (35 at position 0 against 39.7 expected) and under-uses words of exactly six runes (8 whole-word spans against 12.4). [stated — `results/kfixed_echo.md`, `results/echo_dissect.md`]

**Lag 6.** pnotisdev's registry row `obs-lag6` names the relation c_i = 24 − 2·c_(i−6) inside words. Here it holds 77 times among 1,267 pairs against 43.7 ± 6.5 (z +5.1), and it is the best of all 812 affine maps c_i = a·c_(i−6) + b, whose maximum under 999 word-preserving shuffles is 65.7 ± 2.8 (p 0.003 at this lag; about 0.02 over the seven lags tested). At every other lag the best affine map sits where the null puts it. The rune W leads the lag-6 sites (6 against 1.9) but the 29-cell chi-square is flat (p 0.21). [stated — `results/closure_bundle.md` (e)]

**The two echoes share words, descriptively.** Among the 554 words long enough to host both, 83 carry a lag-5 site and 72 a lag-6 site; 18 carry both against 10.8 expected if independent of each other across all those words (hypergeometric p 0.012). The second external review (2026-10-29) pointed out the word-length confound: longer words have more pairs of both kinds. Stratified by exact word length, the expectation is 14.0 and the permutation p 0.11 (`src/echo_overlap.py`, `results/echo_overlap.md`). The sharing stands as a description, not as evidence for a common word-level process, and §45's docstring and the summary were reworded accordingly. Neither echo shares words with the 86 adjacent repeats beyond chance (p 0.74, 0.95). [stated — `results/echo_dissect.md`, `results/echo_overlap.md`]

**What this changes.** Since 2026-10-23 this repository has said the stream has one law, the lag-1 deficit. It has three: the deficit, a lag-5 equality carried by S, and a lag-6 affine relation, the last two confined to the inside of words and correlated with each other but not with the deficit. A word-aware mechanism that produces all three is what pnotisdev's `mech25` row fits and what the next lanes here must target. Nothing in §1–§40 that decodes is affected by the word-edge bug except §14 and §39's phase-6 part, which used the edges as event positions; §14 was rerun with the corrected file.

**The §14 rerun (2026-10-28, corrected edges).** Same 22,863 configurations × 55 pages × 2 F variants × 4 event kinds, 10,059,720 tests, event rate 0.42, with 2,873 word edges in place of 3,261. Controls 22 of 24 at z ≥ 6 and rank 1 (23 of 24 before). Largest z over all tests 5.51 (adv), against 5.24 before; per kind adv 5.51, advline 5.24, nulli 4.88, nullf 5.15; no cell meets the pre-registered rule (z ≥ 6 and edge − base ≥ 20 nats). The conclusion of §14 stands on the right edge set, and the 12 % of false edges moved the maxima by a few tenths of a sigma, which is what a position error that leaves 88 % of events in place should do. [stated — `results/phase6.md`]

## 43. Exact reachability of the solved-page rule, and linear complexity (`src/reachability_lane.py`, `results/reachability.md`, `src/linear_complexity.py`, `results/linear_complexity.md`)

**Reachability.** The solved polyalphabetic pages obey one rule: c = p ± k from a stream, a ciphertext ᚠ is either a literal plaintext F that consumes no key value or an encrypted rune, and no encrypted rune decrypts to F. For a page, a stream and an offset this is a yes/no question with no score: does any skip assignment keep every encrypted rune off F? farfromexact asked it at offset 0 (H007). Here it is asked at every offset 0–19,999 of five streams (prime − 1, prime, prime + 1, Fibonacci, Lucas, all mod 29), both signs, per page and for the section as one continuous stream. One offset for the whole section is excluded exactly for all ten stream-sign cells. Per page the test has no power: a planted 300-rune page leaves 2,857–13,102 wrong offsets alive, because each literal F lets the key realign, and every page survives thousands of offsets under the prime streams. Fibonacci and Lucas mod 29 have period 14, so they are short periodic keys; under the rule they are excluded at every offset on 40–48 of the 55 pages. [stated — `results/reachability.md`]

**Linear complexity.** Berlekamp–Massey over GF(29) gives the shortest linear recurrence generating each page, each page reversed, and the whole stream. Every unit sits at the random expectation n/2 (smallest ratio 0.498; iid null 0.499 ± 0.001) and the whole stream at 6,478 of 12,956. Raw LFSR plants of order 8–64 are recovered at their order; an LFSR added to English is indistinguishable from random, so this excludes only keystream-only pages (pages with no plaintext), which completes farfromexact's H030. [stated — `results/linear_complexity.md`]

## 44. Irrational-digit streams under the soft rule (`src/irrationals.py`, `src/digits_lane.py`, `results/digits.md`, `data/processed/irrational_digits.json`)

ItIsCuthNotCup ran the digits of π, e, √2 and φ as keys rigidly at 200 offsets; pnotisdev's `p60-irrationals` row covers four-way sums and is marked partial. Nobody had run the digit streams skip-aware at every offset. 40,000 digits of each constant were computed here with integer arithmetic (Machin's formula, the factorial series, integer square roots; the first fifteen digits checked against the known values) in base 10 and base 29. Three readings per constant: the base-10 digit as the key value, consecutive digit pairs mod 29, and the base-29 digit. Every offset 0–29,999 as a fresh start per page, 3 signs × 2 F variants, in the two-tier form of §31: tier 1 decodes an 80-rune window of LP2-00/01/02 under the soft-rule Viterbi and keeps cells at z ≥ 4.5 over the window's random-keystream null; tier 2 decodes the survivor's full page with the rule z_uni ≥ 6 and 5-gram z_5 ≥ 6 and readable. [stated — module docstrings]

**Result: null.** 6,480,000 tier-1 window decodes; two survivors (largest tier-1 z 4.68, sqrt 2 digit pairs; 4.66, φ base 29), both failing tier 2 (z_uni 3.27, z_5 0.2). Four planted controls (one per constant, random reading, sign, F and offset, 262 runes of solved English under the soft rule) pass at tier-1 rank 1 among 4,096 neighbouring offsets with tier-2 z_uni 12.1–13.2 and z_5 49–54. Coverage: the first 30,000 digits of each constant, these three readings, one offset per page; digit sums, interleavings and other reductions are not run. [stated — `results/digits.md`]

## 45. Word-aware mechanism lane: no single rule reproduces the three structures, and the S carrier is the one that breaks every rule (`src/mechanism_lane.py`, `results/mechanism.md`, `src/s_carrier.py`, `results/s_carrier.md`)

**Ledger first.** pnotisdev's registry rows `mech25`, `mechanism-search`, `skeleton5`, `echo-mechanisms`, `lag6-dissect`, `s-echo-dissect`, `signal-interactions` and `keywords-r4` cover this ground: nine hand-designed rules simulated on English with a random key; their best fit, "R4" (on a would-be repeat keep the key position and write 24 − 2·c six back; plus one extra rune in about 45 % of words, which their word-length fit needs), reproduces the deficit, the lag-6 count and the lag-5 count but not the S carrier (2–3 against 11); a periodic per-word key is excluded by the absent lag-3/4 excess; literal-F, a collision twist and an autokey chain are excluded for lag 6; 1,940 keywords and the totient stream decoded under R4 are null. What no lab had run is a pre-registered survival test with the two discriminators found in §42, the S carrier scored jointly and the sharing of words between lag-5 and lag-6 sites. [stated — registry rows read 2026-10-28]

**Pre-registration.** Statistics, rules and the criterion were fixed in the module docstring before the first replicate: English plaintext (Emerson, book spelling, its own words) laid into the 55 pages' exact rune counts, iid uniform key, q = 0.81, 200 replicates per rule; nine judged statistics (adjacent repeats, repeats inside words, within-word equal pairs at lags 3, 4 and 5, lag-5 pairs that are S, lag-6 hits of 24 − 2c, lag-5/lag-6 word sharing above its hypergeometric expectation, and the share of S); a rule survives only if LP2 lies within |z| ≤ 3 on all nine. Eight rules: no repair (Rq0), this repository's spend repair (R0), hold repair with a uniform rune (R0h), R4, R4 with the extra rune (R4n), a repair copying the rune five back (Rc5), R0 plus literal S (RS), R0 plus literal F (RF). Controls: the measurement code returns LP2's 86 / 63 / 102 / 11 / 77 / 18 exactly; Rq0 gives 446 ± 21 repeats and 43 ± 7 lag-6 hits; R0 at q 0.81 gives 84 ± 9 repeats. [stated — `results/mechanism.md`]

**Result: every rule fails.** The S carrier fails all eight (2.2–4.0 ± 1.6 against 11; z +3.6 to +5.7), and literal S overshoots it instead (33 ± 6) while tripling the share of S, which LP2 does not have (3.35 % against 3.45 % uniform). R4 with the extra rune is the only rule within |z| ≤ 3 on the other eight statistics (repeats z +1.2, lag-5 +2.9, lag-6 −0.6, word sharing +1.6); R4 without it misses lag 5 (+4.3); every rule without a lag-6 repair misses lag 6 (+4.5 to +5.4); the copy-five rule reproduces lag 5 but not S and not lag 6. The word-sharing statistic does not discriminate at this replicate count (LP2 +7.2 against 1–3 ± 2–3 under every rule). [stated — `results/mechanism.md`]

**The S carrier, calibrated.** Eleven events decide the verdict, so they were calibrated against the whole table they were picked from: within-word equal pairs by rune and lag, 29 runes × lags 2–12, under the K-fixed null of §42. The z maximum is the wrong instrument (a count of 1 in a cell whose null is 0.0 ± 0.2 scores z +5, so sparse high-lag cells dominate), so the statistic is the smallest Poisson tail probability over the 319 cells. LP2's is 2.4 × 10⁻⁵, at the S-at-lag-5 cell (11 against a mean of 2.24); the null's smallest tail reaches that in 3 of 1,000 replicates. The S carrier survives the look-elsewhere correction at p 0.005. It is a real property of the stream, it is strictly word-internal, and no rule any lab has written down produces it. [stated — `results/s_carrier.md`]

**What this means for decoding.** A hold repair (key position kept, plaintext rune consumed) is not a key skip: a decoder that models skips only, as every lane in §9–§40 does, loses alignment at each hold repair (pnotisdev's M04 plants: 15 % plaintext accuracy for an unaware engine). The hold-aware decoder in this repository is §22's null lane, which lets any position be an unencrypted rune that consumes no key value under a hard anti-repeat rule; in likelihood terms that is the hold repair with a uniform replacement, and it was run against the book's key families with the result null above 200 runes and inconclusive below. A T-valued repair adds a prior at positions where c equals 24 − 2c six back, which is a tenth of repairs, so no new decode lane was built here; the lanes that would see an R4-encrypted page are §22 and the §14 rerun. [stated for §22's scope; inferred — the power statement]

## 46. The lag-5 echo runs in pairs; a per-word period-5 key fits the equality count and fails the rest (`src/echo_sites.py`, `results/echo_sites.md`, `src/ngram_lag.py`, `results/ngram_lag.md`, `src/period5_mixture.py`, `results/period5_mixture.md`)

**Two closures first.** A Quorum panel proposed a word-internal multiplier autokey c_i = k·c_(i−5) + p_i; at the true k the residual c_i − k·c_(i−5) would be the plaintext and its histogram English-shaped. Over the 2,073 within-word lag-5 pairs no multiplier k = 1..28 gives a peaked residual (best chi-square 42.8 against 28 ± 7.5, top residue 4.9 %, p 1.0 after the 28 trials); at lag 6 only k = −2 stands out and its excess is the single known cell. The panel's alternative, a count-preserving swap, requires a compensating S deficit at other lags, and S sits at its null at every lag but 5. Both closed. The 811 non-identity affine maps at lag 1 inside words, never scanned because the deficit lives there, are also at their null (best z +3.6 against a maximum-of-811 null of 405 ± 7, p 0.20). [stated — `results/echo_sites.md` (1)]

**The sites, by eye.** `results/echo_sites.md` lists the eleven S..S words and the 77 lag-6 words in Latin transliteration. Two of the S words carry a repeated run five apart, not a single rune: SDNGGLSDNG (SDNG at positions 0 and 5) and ESEOTHTHES (ES at 0 and 5). Counted properly, repeated bigrams at lag 5 inside words number 9 against 1.5 ± 1.2 under a word-preserving shuffle (p 0.001), the one repeated trigram at lag 5 is SDNG (0.0 expected), and page-wide bigram repeats at lag 5 are 28 against 15 ± 4 (z +3.3); every other lag from 2 to 12 is at its null for bigrams and trigrams alike. pnotisdev's branch `research/word-internal-lag5` reported the same 9 against 1.5 and it was not followed up. The lag-5 structure acts on runs of runes. [stated — `results/ngram_lag.md`]

**A key with period 5 inside a word.** The simplest generator of runs that recur five apart is a key that repeats every five runes within a word, so that c_(i+5) − c_i = p_(i+5) − p_i and every lag-5 statistic inside that word is the plaintext's own. pnotisdev's `per-word-keys` row excludes one period-5 key shared by every word (it would make equal plaintext words equal ciphertext words); a different period-5 key per word, drawn from a stream, was not tested there or anywhere. Its prediction is a mixture: a fraction f of the long words carry English's lag-5 statistics and the rest carry uniform ones. English's own, measured on Emerson in rune spelling over 47,730 within-word lag-5 pairs: equal 6.31 %, S..S 0.96 %, repeated bigrams 0.68 %, and a 29-cell difference histogram whose chi-square per 2,073 pairs is 131. At f = 0.5 the mixture predicts 101 equal pairs; LP2 has 102. It predicts 5.1 repeated bigrams; LP2 has 9 (Poisson p 0.07). It predicts a difference chi-square of 61; LP2's is 38.9 (about 3 sd below, with the whole excess in the equality cell and the 28 non-zero cells flat). And it predicts 3.5 S..S pairs, not 11: an equal cipher pair under any key takes the value p + k, which is uniform over the key, so it is S with probability 1/29 whatever the plaintext. (The first version of this section used English's own S..S rate here and claimed an exact fit of the S carrier; that was an error, found by the §47 simulation the same evening and corrected.) So a plain period-5 key in half the words reproduces the equality excess with one parameter, is compatible with the bigram runs, over-predicts the non-zero differences, does not touch the S carrier, and says nothing about lag 6. [stated — `results/period5_mixture.md`]

**Where that leaves it.** The equality cell behaves as English, the other 28 difference cells do not. A mechanism that copies plaintext equality at lag 5 without copying plaintext differences is what the lag-5 data ask for, and that is not a periodic key; it is closer to a rule that writes the rune five back when the plaintext repeats at lag 5. §47 builds that rule. [inferred]

## 47. Echo rules: a gated lag-5/lag-6 echo reproduces nine of ten statistics, and the S carrier is shown to be outside every additive mechanism with a plaintext-independent key (`src/mechanism_lane.py`, `results/mechanism.md`)

**The rules.** Added to the §45 simulator and run with the eight earlier rules under the same pre-registered criterion, now with a tenth judged statistic, the repeated bigrams at lag 5 inside words (LP2: 9). In a word selected with probability r = 0.5 (fixed before the run from §46's fit to the equality count, so that count is spent and the other nine statistics are the test), a plaintext rune equal to the plaintext rune five back is written as the ciphertext rune five back; in the E56 variants a plaintext rune equal to the one six back is written as 24 − 2·c six back; an echo that would make an adjacent repeat is skipped; the base repair is R0 (q 0.81). Variants: key spent or held at the echo, every word instead of half (E5all), and the echoes on top of R4n. [stated — module docstring]

**Result.** E56w (both echoes, half the words, key spent) lands within |z| ≤ 3 on nine of the ten statistics: repeats 83 ± 9 (LP2 86), inside words 63 ± 8 (63), lag 3 and 4 at +1.9 and +2.7, lag-5 equality 126 ± 13 (102, z −1.9), repeated bigrams 8.0 ± 3.1 (9), lag-6 hits 80 ± 10 (77), word sharing 3.4 ± 3.3 (7.2, z +1.1), S share at its value. The held-key variant is the same. It fails the S carrier: 4.6 ± 2.1 against 11 (z +3.1). The lag-5-only rule reproduces the bigram runs but not lag 6; echoing in every word over-shoots lag-5 equality (183) and under-shoots nothing else; the echoes on top of R4n over-shot lag 6 (119) in the 2026-10-28 run. Of the fourteen rules run that day, E56w was the only one within 3 sd on repeats, both echo counts, the bigram runs and the word sharing at once, with one gate parameter fitted to one count. [stated — `results/mechanism.md`]

**Rerun 2026-10-29 (§56): the R4n base was broken in the 2026-10-28 run.** Standalone R4n had silently been R4. With the filler branch restored, the regenerated table reads: R4n (hold repair plus one extra rune in 45 % of words) fits eight of ten, failing only the S carrier (2.5 ± 1.6) and the bigram runs (1.6 ± 1.3); E56w is unchanged (nine of ten, S at 4.1 ± 1.9, z +3.6); and **E56w+R4n, the two echoes on top of R4n, is inside the pre-registered |z| ≤ 3 band on all ten statistics**, with two cells at the band's edge: the S carrier at 4.5 ± 2.3 against 11 (z +2.9) and the lag-6 count at 117.5 ± 13.9 against 77 (z −2.9). It passes the S cell on the width of its standard deviation, not by producing the S weight (it predicts four or five S pairs, like every other rule), and it over-produces the lag-6 relation by forty. It is also the rule whose extra rune in about half the words matches, without having been fitted to it, the word-length fingerprint of §55 (about one filler per two words). Its out-of-sample test is §57: fifteen of sixteen cells hold and the lag-6 count in long words fails, the hold repair's signature. So the honest reading is: a hold-repair with fillers plus the two echoes is the first rule to clear the pre-registered bar, it clears it narrowly, and the S weighting is still not reproduced by it. Its out-of-sample predictions on the §49 statistics have not been run; that is the next check if the rule is pursued. [stated — `results/mechanism.md`; inferred — the reading]

**Why no rule of this kind can carry S.** An equal cipher pair produced by a key, by a period-5 key, or by copying an earlier cipher rune has the value p + k at the copied position, and that value is uniform over the key whatever the plaintext. So under every rule above, and under every additive cipher whose key value at the echoed position is independent of the plaintext there (which makes it uniform conditional on the coincidence; a marginally uniform key is not enough, as the second external review noted, §56), the rune at a lag-5 coincidence is S with probability 1/29: 3.5 of 102, as the simulations give (2.2–6.4 across all fourteen rules). LP2 has 11, at p 0.005 after the look-elsewhere correction of §45 (0.003 before the sampler-clock fix of §56). The S carrier is therefore not a property of plaintext equality, key structure or ciphertext copying. It requires a step that acts on the cipher value S itself (a marker, a swap keyed on the rune, a nomenclator element) or on plaintext S without consuming key (literal S, which the S share excludes at any useful rate), or it is an eleven-event fluctuation that three labs have now each found at the 0.003–0.02 level under different nulls. [stated — the uniformity argument is exact for additive ciphers whose key at the echo positions is independent of the plaintext, hence uniform conditional on the coincidence; a plaintext-reading key, i.e. an autokey or a rule keyed on the written rune, is additive and NOT excluded; inferred — the classification of what remains]

**Correction from a Quorum panel (same evening, quorumsays.com/q/XoHCqqb6ziaf).** The argument needs the key uniform, not merely independent of the plaintext: a key that is zero or constant inside the gated words would let plaintext S..S pairs show through as cipher S..S. The loophole is bounded by the S share. With the plaintext in clear inside a fraction f of the words, the overall share of S rises from 3.35 % toward English's 7.4 %; the observed share allows f ≤ 0.08 at two standard deviations, which predicts at most 3.8 S..S pairs against 11, and a constant non-zero key gives no S preference at all. The panel's other point, that a count-preserving swap would leave an S hole at donor positions while an overwrite would not, is recorded in `results/s_loophole.md`: the eleven echo words carry 1 further S against 2.5 expected, a deficit in the swap's direction with no power at eleven words. [stated — `results/s_loophole.md`]

**What changes.** §46's claim that the period-5 mixture fitted the S carrier was an error of this same kind and is corrected there. The stream's structures now read: a repeat deficit; a lag-5 echo that copies equality in runs (bigrams, one trigram), carried in part by S; a lag-6 affine echo; both echoes word-internal and word-sharing. A gated echo rule reproduces all of it except the S weighting. Decoding under E56w needs a decoder that, at a lag-5 or lag-6 plaintext repeat, expects the echoed cipher value instead of the keyed one; that is a different transition from a skip or a null and no decoder here or in the other ledgers has it. It would be the next instrument to build, and the open question before building it is whether the gate (which words echo) is random or a property of the word. [inferred]

## 48. Echo-aware decoding of the phase 3–4 library: null, and the echoes turn out to cost an unaware decoder almost nothing (`src/score.py` `echo_mask`, `src/echo_lane.py`, `results/echo_lane.md`)

**Instrument.** `score.decode` gained an echo transition: at a position where an echo could have happened (inside a word, c_i equal to the rune five back, or equal to 24 − 2 times the rune six back; 173 such positions on the 55 pages), the decoder may treat the rune as copied, the key symbol consumed unused, with gain ln(r·P_English(repeat)) − ln(1/29) = −0.11 (the "spent" form of E56w); the "held" form uses the existing null transition at the same positions. Everything else is the phase 3–4 Viterbi. Pre-registered rule: z_uni ≥ 6 over 2,000 random keystreams through the same decoder, 5-gram z_5 ≥ 6, readable. [stated — module docstring]

**Controls.** Twelve plants, 262 runes of English in its own words encrypted under E56w with a key drawn from the library (six spent, six held, signs and F cycled): eleven recovered at rank 1 with z 11.0–14.9 and plaintext accuracy 0.935–1.000; the twelfth (held, Beaufort, affine-position key 28·n + 9) at rank 2 behind an alias of its own family with z 13.4 and accuracy 0.992. The base decoder's z on the same plants is the measurement that matters: spent plants 10.8–15.3 against the echo decoder's 11.0–14.9, no loss; held plants 5.5–13.9 against 12.5–13.9, one plant with three held echoes dropping to 5.5. An echo touches 0–3 positions in 262 runes, so a key-spending echo is invisible to the phase 3–4 decoders and a key-holding one costs them only when several fall in one page. [stated — `results/echo_lane.md`]

**Result: null.** 22,863 configurations × 55 pages × 2 F variants × 2 decoders = 5,029,860 tests; no cell at z_uni ≥ 6 (largest 4.99, LP2-09, spent, phrase "CERTAINTY AND", against a chance maximum of about 5.4 for this many cells); 85 minutes. Within the stated limits, the book's own words, phrases, sentences, number streams and self-running keys do not decode any page under the gated echo mechanism either. [stated]

**What it settles.** The echo rule of §47, if it is the machine, does not rescue any key family already tried: the phase 3–4 negatives were already echo-robust in their spent form, and are now run in both forms. The decoder is in place for any new key library, which is the one input the echo rule changes nothing about. The lane that remains open on the key side is the cross-library one named in the status box: pnotisdev's number streams have never met this decoder. [inferred]

## 49. Two untouched tests: E56w's out-of-sample predictions, and the echoes on the image-derived stream (`src/e56w_predictions.py`, `results/e56w_predictions.md`, `src/reread_echoes.py`, `results/reread_echoes.md`)

An outside review of §41–§48 made three objections that are right: the echo rule was designed after looking at the ciphertext, so fitting the statistics it was designed around is description, not prediction; the test count measures work, not coverage; and the S weighting is an exploratory finding from one manuscript whose calculation should be checked without this repository's intermediate files. The first and third have cheap answers, run here in the order that makes them honest.

**Predictions before the look.** Eight statistics that played no part in fitting or judging E56w were named, the rule was simulated 300 times (r = 0.5, q = 0.81, English plaintext, iid key, the 55 pages' lengths), and the predicted means and spreads were written and committed (53e3c5f, 18:14) before the same statistics were computed on LP2. What was already known from other labs is declared in the file: pnotisdev had reported the lag-6 length profile, and §46's page-wide bigram count had touched the across-gap question. The eight: lag-6 hits by word length (7, 8–9, 10+); lag-5 equal pairs by word length (6, 7–8, 9+); words with two or more echo sites, and with three or more; within-word equality at lag 10; the share of lag-6 sites starting at word position 0; adjacent repeats inside echo-bearing words against other words of the same lengths; lag-5 equality across word gaps; lag-6 hits across word gaps. Rule: a prediction holds within |z| ≤ 2.5. **All fourteen cells hold**, with |z| from 0.17 to 1.55 and no systematic sign: 8 lag-6 hits in 7-rune words against 10.9 ± 3.5, 39 in 8–9-rune words against 31.9 ± 7.2; 28 multi-site words against 34.3 ± 6.3; 2 lag-10 equalities against 3.6 ± 1.9; repeats inside echo words 0.45 per 100 pairs against 0.61 ± 0.23 and outside them 0.72 against 0.65 ± 0.16; across word gaps 361 lag-5 equalities against 368 ± 19 and 389 lag-6 hits against 392 ± 21. [stated — `results/e56w_predictions.md`]

What that does and does not show. The rule survives eight checks it was not built to pass; that is the test the review asked for, and a rule that fitted by accident would have been expected to fail one or two. It is consistency, not confirmation: several of the predictions are also made by simpler rules (any word-internal mechanism predicts nothing across gaps), the discriminating ones are the length profiles, the multi-site counts and lag 10, and the S weighting remains outside the rule. [inferred]

**The echoes from the images.** §38's blind re-reading classified every glyph on the unsolved page images with no access to the transcription of those pages. Its resolved readings aligned to 12,807 of the 12,956 positions (98.8 %) and disagree with the transcription at none of them, so on the pairs where both runes are blind-read the statistics are the transcription's to the digit: 101 lag-5 equal pairs of 2,022 (69.7 expected), 11 of them S (2.4), 75 lag-6 hits of 1,242 (42.8), 84 adjacent repeats of 12,675 (437). The word structure is the transcription's, which pnotisdev audited against the images separately (0 of 2,334 word dots missing). Typography, transcription lineage and rune indexing are therefore not the source of any of the three structures; an independent recomputation from the images by another lab's code would add the last layer, and the scripts, the plants file and the site exist to make that easy. [stated — `results/reread_echoes.md`]

## 50. The S carrier, three ways: the eleven sites in the page images, a line-break dependence found by eye, and an S-triggered rule's second traces (`results/s_sites/`, `src/linebreak_echo.py`, `results/linebreak_echo.md`, `src/s_rule_predictions.py`, `results/s_rule_predictions.md`)

§47 says the S weighting must come from a step that acts on the written rune S, not on the letters beneath it. The three cheapest things that follow from that were done in order: look at the eleven sites in ink, test what the looking suggested, and give the simplest S-triggered rule a prediction it could fail.

**The sites in the images.** Using the glyph boxes of §38's re-reading, the two S glyphs of each pair were outlined on the authentic page scans and cropped (`results/s_sites/`, eleven files, 0.6 MB). Nothing is visible at any site: the runes are a clean typeface at uniform weight and spacing, the S glyphs are ordinary, there is no mark, colour change or spacing anomaly near them. That is itself a fact about the production: the pages are set in a rune font and rendered through Ghostscript (§41), so any step that acts on written runes happened in the text source or the typesetting, not in a hand. One thing did show: four of the eleven pairs wrap a line, the word broken between the two S's, where the share of within-word lag-5 pairs that wrap is 21 %. [stated — the crops; the 4 of 11 count]

**The line-break cut, with controls.** Within-word pairs at lags 4, 5 and 6, and the lag-6 T relation, split by whether a line break lies between the two runes, each against a shuffle null that keeps every word and line boundary in place; the same split for pairs across a word gap. Lag-5 equality on pairs that wrap a line: 30 of 428 against 14.6 ± 3.6 (p 0.001); on same-line pairs 72 of 1,645 against 56.2 ± 7.1 (p 0.02); two-proportion z between them +2.24. The controls are flat: lag-4 equality (−0.07), lag-6 equality (−0.59), and the lag-6 T relation (+0.18, 19 of 302 against 10.6 wrapping, 58 of 965 against 33.2 same-line) show no line-break dependence, and across word gaps nothing moves at a line break at any lag. So the lag-5 echo, and it alone, is about twice as strong where the word wraps a line, at p about 0.03 for the difference. Line breaks are a layout fact: the text was flowed into a fixed measure with words broken wherever the line ended, which is a step applied to the finished rune string. This is the first measurement that ties one of the echoes to the production of the pages rather than to the cipher. It is a post-hoc cut found by eye, reported with that status; it is not independent of the S sites that prompted it, and a 2.2-sigma difference with eleven S events behind part of it will not bear weight on its own. [stated — `results/linebreak_echo.md`; inferred — the production reading]

**RS5's second traces.** The simplest rule that acts on written S, "inside a gated word, when the rune five back is S, write S", was added to E56w with its rate set so the simulated S pair count is the eleven; that fit is spent, and the rule was judged only on seven second traces named and committed before the check (e9908b9): S..S..S chains at lag 5, S..S at lag 10, S..S at lag 5 across word gaps, S..S at lags 4 and 6, the overall share of S, and lag-5 P..P pairs (the next-strongest rune). All seven hold, with |z| ≤ 1.35. The honest reading is that this is weak: the rule predicts near-uniform values everywhere except at the eleven pairs and a 0.13-point rise in the share of S, so the data could hardly have failed it. RS5 is consistent and nearly unfalsifiable with this book, and it has no reason to exist. [stated — `results/s_rule_predictions.md`]

**Where the S question stands after this.** Real at p 0.005 after look-elsewhere, identical on the image-derived reading, outside every additive mechanism with a plaintext-independent key, invisible in ink, and now with one thread leading away from the cipher: the lag-5 echo prefers words that the typesetting broke across lines. If that thread is real, the operation is in the pipeline that turned text into pages, and the thing to look for is how a line-filling step could copy or echo a rune five places back. [inferred]

**Addendum (2026-10-29): the lag-6 constant points at S too.** A Quorum panel noticed that 24, the constant in c = 24 − 2c′, is the Gematria prime of S (53) reduced mod 29, and S is the only rune whose prime reduces to 24. Both echoes therefore carry a pointer to S: the lag-5 echo in the rune it prefers, the lag-6 relation in its constant. It is a post-hoc coincidence at about 1 in 29, noticed after S was already singled out, and the related facts that S is the inverse of 2 mod 29 and that 2 is a primitive root are properties of 29, not of the data. The relation does not improve in the prime domain: all 812 affine maps on prime residues at lags 5 and 6 sit at their permutation null (p 0.20, 0.22), so it lives in the index domain. [stated — `results/s_prime.md`]

## 51. Layout follow-up: the line-wrap excess is not a layout effect (`src/layout_followup.py`, `results/layout_followup.md`)

**Registered before the check (e7b7695, 20:07):** if a line-filling step were behind the lag-5 echo's preference for wrapping words, the echo should care where the break falls. Two statistics with null predictions taken from the pair populations alone: (A) the split position of a wrapping pair, s = 1..5 (how many of the five positions lie on the new line), with the 30 equal wrapping pairs predicted to follow the 428 wrapping pairs' shares; (B) for same-line pairs, the echo rate by distance from the nearest line edge (0, 1, 2, 3–4, 5+), predicted flat. Decision rule: simulated p < 0.01 on either counts as support for a layout step; the lag-6 T relation and lag-4 equality run as controls. [stated — `results/layout_followup.json`]

**Result: no support.** Split position is flat (7, 5, 5, 7, 6 against 5.6, 5.5, 5.7, 7.1, 6.2; p 0.98). Distance to the line edge is not flat in the direction a layout step would need: the rate is lowest at the edge (2.5 % at d = 0, 2.9 % at d = 1) and highest in mid-line (5.6 % at d ≥ 5), trend z −2.16 away from the edge, chi-square p 0.28. Controls flat. So the pairs that wrap have twice the echo rate, but among them the break can fall anywhere, and among same-line pairs being near a line edge lowers the rate rather than raising it. A step applied at the line break would do the opposite. [stated — `results/layout_followup.md`]

**Not a word-length confound either.** Wrapping words are longer (6.03 runes against 4.18) and the echo rate rises with word length (3.2 % in 6-rune words to 6.4 % in 9–10-rune words), so the wrap excess could have been length in disguise. Stratified by word length, wrapping pairs still carry 30 equal pairs against 21.0 expected from each length's own rate (Mantel–Haenszel z +2.25). The excess is real as a contrast between wrapping and same-line pairs of the same length, and it has no structure inside the wrap. [stated]

**Line geometry, for the record:** 594 lines, 21.8 ± 2.6 runes each (min 3, max 26); 388 line breaks (65 %) fall inside a word. The measure is fixed in runes, not justified in pixels, and words were broken wherever the count ran out. [stated]

**Reading.** The §50 lead goes back to being a 2.2-sigma cut found by eye: a real contrast in the data, with nothing that a layout mechanism would predict attached to it, and nothing that word length explains. The honest options are a fluctuation, or a property of the words that wrap that is not their length and not the position of the break, and the second has no candidate. The pre-registered test was the right one to run and it came back negative. [inferred]

## 52. The hint-reading family: "shed our own circumferences" as an operation, null (`src/shed_lane.py`, `results/shed_lane.md`)

**The cells.** The parable on the last solved page maps to six operations on the ciphertext (the table in the 2026-10-28 discussion is reproduced in the module docstring); four were already tested null across the labs. The two that were not: WORD, the first and last rune of every word written in clear and consuming no key value (the solved pages' literal-F rule applied to word edges; one- and two-rune words entirely literal), and RING, the first and last line of every page written in clear. Decoder: the §9 Viterbi with the null transition forced at those positions; library `families.ALLSETS`, 3 signs × 2 F variants, all 55 pages; rule z_uni ≥ 6 over 2,000 keystreams through the same mask, z_5 ≥ 6, readable. [stated — module docstring]

**Controls, and what they say about power.** Twelve plants, six per kind. Seven pass at rank 1 with z 6.6–12.8. The five that do not are informative rather than alarming: under WORD, half the runes of a page are literal (80–138 of about 260), so the encrypted remainder is a short page by §23's measure, and a two-word reversed key fell to z 2.2 and rank 301; three self-running-key plants (two WORD, one RING) were recovered at z 6.9–13.6 but ranked 2–4 behind offset aliases of their own stream, the alias effect already noted in §48. Plaintext recovery on the passing plants is 0.86–0.99. So the WORD kind has power for keys of three words or more and for streams, and little for short keys; the RING kind has full power. [stated — `results/shed_lane.md`]

**Result: null.** 5,029,860 tests, no cell at z_uni ≥ 6, largest 5.08; 376 minutes. Within those limits, writing the word edges or the page rings in clear does not make any of the book's key families decode a page. The six operations the parable can be read as prescribing are now all tested, and the honest summary is the one the solved pages' own history suggests: the parable is a 2013 poem reused as an ending, and its words were not written about the 2014 mechanism. [stated; inferred — the last sentence]

## 53. Cicada's own words, 2012–2017, as key material: null (`data/corpus/raw/cicada_own_words_2012_2017.txt`, `src/corpus.py` with `CORPUS_SET=cicada`, `results/runkey_cicada.md`, `src/cicada_words_lane.py`, `results/cicada_words.md`)

**Why this cell was empty.** The group quotes itself: the page-74 parable is their 2013 poem, the 2014 welcome echoes 2012, and "the key has always been right in front of your eyes" is a sentence they signed in 2012. Of all the habit-derived key sources (§ "habits" discussion, 2026-10-29), their own earlier prose was the one nobody had run. Ledger: pnotisdev's `solved-phrase-keys` covers the solved pages' words and the 2014 signed messages as short keys, `signed-streams` the 2014 payload bytes, `p60-lp1-key` the solved translation as a book key; wazar's and jens-wedin's running-key texts are literature. Nothing covers 2012 and 2013. [stated — registry rows read 2026-10-29]

**Corpus.** Every PGP-signed Cicada message body from 2012 to 2017 (25 distinct) and four quoted unsigned texts (the 2012 and 2013 opening images, the 2013 parable from the 761.mp3 tag, the 2016 outguess text), extracted by script from scream314's year narratives as data: 29 texts, 1,592 words, 7,792 runes in the book's spelling, provenance and hash in `SOURCES.md`. The signed bodies carry their embedded strings too (an RSA modulus, the 2014 cipher groups, coordinates), so the key library includes those fragments as well as prose. [stated]

**Running keys.** The corpus as one stream at every offset, both directions, both spellings, 3 signs × 2 F, all 55 pages, under §25's rule (z_uni ≥ 7, bigram z ≥ 3, readable): 7,812,750 tests, 2 of 2 planted controls recovered at the planted offset (z 12), largest z_uni 4.63, no cell at 5. Null. [stated — `results/runkey_cicada.md`]

**Words and phrases.** Every distinct word of two or more runes, every contiguous 2-, 3- and 4-word phrase and every line, forwards and reversed: 8,916 keys × 3 signs × 2 F × 55 pages = 2,942,280 tests under the §9 Viterbi, rule z_uni ≥ 6 and z_5 ≥ 6 and readable; 6 of 6 planted controls at rank 1 (z 12.0–16.4, z_5 38–56). Largest z_uni 4.59 (LP2-19, a reversed line). Null. The first run's six controls were built with the sign convention wrong for the two "add" plants (the §29 lesson again: the encryptor applies the sign, the decoder negates); the sweep was unaffected and the controls were rerun with the construction fixed, both runs recorded in the JSON. [stated — `results/cicada_words.md`]

**What it closes.** Their own words, as a running key or as a keyword, do not decode any page within these limits. The habit list of 2026-10-29 is now fully converted into tested cells, and every one is null at the stated detection limits. [stated; inferred — the generalisation to the habit list]

## 54. Cross-library lane: pnotisdev's 1,439 keystreams under this repository's three decoders (`src/pnotisdev_library.py`, `src/cross_library_lane.py`, `src/export_book_library.py`, `results/cross_library.md`, `data/processed/pnotisdev_library_manifest.tsv`, `data/processed/book_library.tsv`)

**Ledger first.** Every lab's key material had met only its own decoder. pnotisdev's registry rows `lib-sections`, `multipliers`, `hyp-streams`, `sacred`, `sacred2`, `sacred3`, `keywords-r4` and `open-h1` (read 2026-10-28, commit 15200c6) describe a library of 1,447 streams (number-theoretic sequences, digits of constants in base 10 and 29, the book's numbers, hash counter and chain streams of Cicada strings and of the payload, keyword and two-word keys from the solved pages) screened at every start offset on the first 300 runes of the 8 unsolved sections with their flat-IoC Rust engine under two anti-repeat models and 28 key multipliers (409 million and 5.7 billion decodes; rule IoC ≥ 1.40 on the window, then whole-window re-decode; 15 of 15 planted windows recovered; 0 of 15 hits verified), plus 1,097 LLM-proposed streams (`sacred*`), the library decimated by d = 2..29 (`hyp-streams`), and an unrun "library × keyword" campaign (`open-h1`, 581 flat streams × 2,000 offsets). Their engine scores the decoded window's index of coincidence and bigrams, language-agnostic by design; it never saw an English Viterbi. This repository's three decoders (the skip Viterbi of §9, the free-null decoder of §22, the echo-aware decoder of §48) had never seen their streams. [stated — registry rows and `results/field_survey_2026-10-28.md` §7]

**Their library, rebuilt as data.** The binary export (`library.ksb`, "KSB1") is not in their repository; its generator is (`work/kscreen/export.py`, `work/keystreams.py`, `work/prng_screen.py`, `work/grid60.py`, `work/lp.py`, `work/ref/errata.tsv`). Those files were downloaded into `data/external/pnotisdev/` (gitignored; commit, paths and SHA-256 in `SOURCES.md`) and read; nothing of theirs is executed. `src/pnotisdev_library.py` rebuilds every stream from the definitions on this repository's copy of the master transcription with their six errata applied: 1,439 streams of 20,000 values, 580 non-periodic and 859 periodic (801 keyword keys, the cycles and squares), the count their 2026-10-18 registry note gives for the export (the 1,447 of the first screen log counted eight duplicate hash streams of the seeds "3301" and "1033"). Checks: the first runes of all six model-0 decodes published in their `library_segments_verify.txt` reproduce from the rebuilt streams (two of them for the full 40 published runes), and the π, e, √2 and φ digit streams agree with §44's integer-arithmetic digits at every one of 2,900 positions in both bases. `data/processed/pnotisdev_library_manifest.tsv` carries a SHA-256 per stream so the other lab can confirm that what was decoded here is what they screened. [stated — `tests/test_cross_library.py`]

**Pre-registration** (module docstring, before the run). Non-periodic streams at every start offset 0–19,672 (the longest page plus the decoder's key margin keeps the same offset decodable on the full page), periodic streams at every offset of one period: 11,419,175 (stream, offset) rows. Three decoders in the two-tier form of §31: **plain** (soft skip rule) and **echo** (spent echoes at the 3, 1 and 2 eligible positions of the three windows) on the first 80 runes of LP2-00, LP2-01 and LP2-02; **hold** (§22's free-null decoder, prior −0.8) on the first 160 runes of the same pages, since it needs 160 runes for 80 % power (§23) and runs three to four times slower, over every offset of the periodic streams and offsets 0–999 of the non-periodic ones (a stream started at the section's first rune reaches LP2-02 at offset 528 plus skips; pnotisdev's own H1 slice used 2,000 offsets). Every cell: 3 signs × 2 F variants; survivor at z ≥ 4.5 over the window's null of 2,000 random keystreams through the same decoder; tier 2 decodes the survivor's full page under all three decoders; candidate at z_uni ≥ 6 and 5-gram z_5 ≥ 6 and readable (hold: z_uni ≥ 6 and the free-null score at least 20 nats above the plain decoder's, §22's rule, since §27 showed the 5-gram fails when nulls break the n-grams); a candidate stream is then run on every page. Controls: six per decoder, 262 runes of English encrypted under the matching mechanism (soft rule q 0.81; E56w spent echoes; hard rule with nulls at 0.22) with a stream from their library at a random offset, four non-periodic and two keyword streams each, signs and F cycled; a control passes at tier-1 rank 1 among the stream's 4,096 neighbouring offsets (keywords: among every offset of every periodic stream) with z ≥ 4.5 and at the tier-2 rule. [stated — module docstring]

**Controls.** Eighteen plants, all eighteen found: tier-1 z 5.3–6.8 (plain), 5.3–6.9 (echo), 6.9–10.2 (hold); tier-2 z_uni 11.6–15.4, 10.7–15.3, 7.8–13.5, 5-gram z_5 39–73 for the plain and echo plants, free − base 97–263 nats for the hold plants; every plant meets the tier-2 rule. At rank 1 in tier 1: plain 5 of 6, echo 6 of 6, hold 3 of 6. The 4 plants not at rank 1 are outranked only by their own stream at neighbouring offsets (+1, −4, −3, −1, +1, −2): an early skip or null shifts the key index, and the shifted offset decodes all but the first runes. Under the pre-registered wording (rank 1) they are misses; under the generator lane's reading (rank 1 among distinct keys) they pass. Both counts are reported. [stated — `results/cross_library.md`]

**Result: null.** Tier 1: 205,545,150 plain, 205,545,150 echo and 10,599,030 hold window decodes over 11,419,175 (plain, echo) and 588,835 (hold) stream-offset rows; largest tier-1 z 5.28 (plain), 5.14 (echo), 5.84 (hold) against a chance maximum of about 6.2 for the plain and echo grids. 293 cells survived tier 1 at z ≥ 4.5 (a Gaussian tail over the 421,689,330 window decodes would give about 1,433, so the survivors are not in excess of chance) and went to the full page under all three decoders: 293 tier-2 decodes; largest full-page z_uni 5.87 (sha512-ctr mod :command your own self, offset 178, LP2-02, hold; z_5 -0.3, transliteration ECTHSTTHUSDMBRLRUOEUAOEODISEOH…); candidates meeting the pre-registered rule: 0. The hold survivors' free − base margins run 91–266 nats, the same range as the hold plants (97–263): on random survivors the free-null decoder gains that much by inserting nulls, so §22's 20-nat margin does not discriminate here and the hold rule rests on z_uni ≥ 6 [inferred]. Runtime 13.0 hours on the longest of three shards. [stated — `results/cross_library.md`]

**Coverage limit.** Decoded here: their 1,439-stream library (every stream of `lib-sections` and `multipliers`; the multipliers are this repository's three signs only for m = 1 and 28, so the other 26 multipliers of their `multipliers` row are not covered), at every offset for the plain and echo decoders and at the stated offsets for the hold decoder, on windows of the three longest first pages at tier 1 and on the full page at tier 2; the `sacred`, `sacred2`, `sacred3` and `hyp-streams` libraries (decimations, text sums, deep digits, LLM-proposed combinations) and their hash streams of 12,944 solved-text words (`kscreen-hashwords`) were not rebuilt. No accepted decoding within the tested configurations at the stated detection limits. [stated]

**The other half of the exchange.** `data/processed/book_library.tsv` exports this repository's 7,621 keys (`families.ALLSETS`: 2,905 phrase and sentence keys, 4,716 phase-3 streams; one period for the 4,341 periodic keys, the first 327 values otherwise) so the other lab can run them under its engine. It was not run here. [stated]

## 55. The filler lane: the word-length fingerprint, decoder power under fillers, and the sweep (`src/wordlen_fingerprint.py`, `results/wordlen_fingerprint.md`, `src/filler_power.py`, `results/filler_power.md`, `src/filler_lane.py`, `results/filler_lane.md`, `results/filler_lane_registration.md`)

**Why this lane.** Every one of the 864 million decoder tests before it shares one shape: an additive cipher, key plus plaintext mod 29, key restarting per page, few or no inserted runes. The question of 2026-10-29 was where that shape could be wrong, and the cheapest place to look was the one unit of the ciphertext nobody's ledger quantifies: the words. With the corrected word edges (§42) the 55 unsolved pages hold 2,928 words. [stated]

**Part A, the fingerprint (descriptive, computed before the registration and recorded as such).** The solved pages' ciphers preserve word boundaries, so their 698 cipher words are an English sample in the book's own spelling: mean length 4.01 runes, 23.9 % of them two runes long; English prose spelled in runes (five public-domain books, 177,798 words) gives 4.02 and 25.4 %. The unsolved pages give 4.42 and **15.9 %**. The chi-square of the unsolved histogram against the prose reference is 183; 2,000 bootstrap samples of 2,928 English words give median 13, 99th percentile 30, maximum 42 (p 0.0005), and the solved pages score 11 on the same test (p 0.60). Latin (1,476), Old English (2,930) and Chaucer (345) fit worse, as does English with a fraction of its word separators dropped (148 at best: merging words thins the two-rune cell but overloads the tail). English with filler runes inserted fits best: Poisson(0.5) fillers per word scores 54 and a filler after each rune with probability 0.10 scores 83, both still outside the bootstrap range, so the fit is partial and a different register (verse, a list) is not excluded. (§59, 2026-10-29: the E56w+n form of the filler, one extra rune at a uniform position in a fraction p of words of two or more runes, fits at p = 0.40 with chi-square 25, inside this bootstrap band.) Two more facts close a family while they are at it: the index of coincidence by word position, from either end, is flat (15 of 16 cells within 1.5 sigma of the per-page shuffle null, one cell of 340 runes at +3.6), and no cipher word of four or more runes occurs twice anywhere on the 55 pages (null 0.2), where English prose of that length repeats hundreds; so there is no key that restarts at each word with a fixed keyword, the one additive family that could have carried the S weighting through a constant key at a word position. [stated — `results/wordlen_fingerprint.md`]

**What was already covered.** §22 ran the free-null decoder (a rune may be an unkeyed filler that consumes no key value) over the book's 7,621 keys on all 55 pages with plants at filler rates 0.15, 0.22 and 0.30 (15 of 18 controls, null), and §54 ran it over pnotisdev's streams at every offset of the periodic ones and offsets 0–999 of the rest (null, 6/6). What had never met a filler-aware decoder: the 16 external running-key texts of §25, §40 and §53 (2.7 million runes, decoded there with the plain decoder only) and pnotisdev's non-periodic streams beyond offset 999. [stated]

**Part B, decoder power under fillers (pre-registered).** English of 100, 160 and 230 runes under the repository's standard mechanism (soft rule q 0.81) with a filler after each emitted rune with probability 0.10, the filler uniform over the 28 runes other than the previous cipher rune so that it adds no doublets; three families (a Vigenère word of ≥ 8 runes, a prime stream, a running key at a random offset of a corpus text), signs and F cycled, 12 plants per cell, each also encrypted without fillers; recovered = z ≥ 6 over 400 random keystreams and rank 1 in the family (every word key, every prime stream, the 4,096 neighbouring offsets). **The plain decoder recovers nothing in any filler cell** (power 0.00 in eight cells and 0.08 in the ninth; median z of the true key 0.7–3.3, where it is 6.9–11.9 without fillers). The free-null decoder keeps the key: at prior ln(0.1/0.9) = −2.2 it recovers 0.83, 1.00 and 1.00 of the Vigenère plants, 0.58, 0.83 and 0.75 of the prime plants and 0.25, 0.58 and 0.75 of the running-key plants at 100, 160 and 230 runes, and costs little when there are no fillers (0.83–1.00 against the plain decoder's 0.92–1.00). The free-null score sits a median 86 nats above the plain score for the true key with fillers and 0 nats without, so §22's 20-nat margin separates the two worlds. Decisions, taken by the rules written in the registration: prior −2.2 (19 running-key plants recovered against 18 at −0.8), and part C runs (power 0.75 at 230 runes against the 0.50 threshold). [stated — `results/filler_power.md`]

**What part B says about the record.** If the pages carry fillers at about this rate, every plain-decoder lane (§9–§20, §25, §31, §40, §44, §53, the plain and echo tiers of §54) had no power against the true key, whatever its planted controls showed, because those controls were planted without fillers. The lanes that did see that world are §22 and the hold tier of §54. This is the outside reviewer's "test count is not coverage" in its sharpest form, and it is why the lane below exists. [inferred from part B]

**Part C, the sweep (pre-registered).** Free-null decoder at prior −2.2 over the 10 texts of up to 60,000 runes at every offset in both directions, the 6 longer texts at their sentence starts, and pnotisdev's 580 non-periodic streams at offsets 1,000–1,999: about 1.08 million offsets, 18 cells each (3 signs × 2 F variants × the first 160 runes of LP2-00, LP2-01, LP2-02), tier 1 at z ≥ 4.5 over the window's null of 2,000 random keystreams through the same decoder; tier 2 the full page at z_uni ≥ 6 and free-null score ≥ 20 nats above the plain decoder's for the same key and readable English; six controls planted under the part-B mechanism. Coverage limits stated in advance: window power at 160 runes is 0.58 for running keys (part B), the longer texts at sentence starts only, pnotisdev offsets ≥ 2,000 open, one prior. [stated — registration]

**Result: null.** 1,082,712 offsets in 692 work units, **19,488,816 window decodes**, 4.8 hours on eight shards. Tier 1 passed 685 keys (363 from the texts, 322 from pnotisdev's streams; largest window z 5.96 against a chance maximum of about 5.8 over that many tests). On the full page their z_uni has median 4.0; eleven sit at 5.5 or above and two cross 6: pnotisdev's sha256-ctr "program your mind" stream on LP2-02 (Beaufort, F literal, offset 1,417, z 6.00) and the Mabinogion's Lady of the Fountain on LP2-00 (Beaufort, offset 6,261, z 6.07). Both read as rune salad (`AEXUOTHANAEDLOERLFUIEOEOOSOC…`, `NEFLAEAIERNGLASAPOIAACSWGSAG…`), so neither meets the readable arm of the tier-2 rule, and two values at the bar among 685 keys pre-selected on the same first 160 runes is what the null gives. Controls: five of six planted running keys recovered at rank 1 (window z 7.7–10.4); the sixth, a reversed Beaufort plant, was found at z 6.8 but ranked second behind an offset five positions away in the same text, an alias the ±3 rule does not cover. [stated — `results/filler_lane.md`, `results/filler_lane_shard0..7.json`]

**One instrument lesson, recorded so the rule is not reused as written.** The tier-2 arm "free-null score at least 20 nats above the plain decoder's" was taken from part B, where it separates a true key with fillers (median +86) from one without (0). On a wrong key over a full page it does not discriminate: all 685 survivors clear it (median +111 nats, minimum +43), because a decoder free to drop any rune at −2.2 nats gains that much on noise. The arm did no filtering here; the z_uni bar and the readable arm did all of it. A future filler lane should calibrate the margin on wrong keys at page length, or drop the arm. [stated]

**What §55 leaves.** The filler world is now tested for the sixteen external texts and pnotisdev's non-periodic streams to offset 1,999, with the window power part B measured (0.58 for running keys at 160 runes, so a true running key at an unlucky offset had a two-in-five chance of passing unseen). Still blind to fillers: the six long texts away from sentence starts, pnotisdev's streams at offsets ≥ 2,000 and their sacred and hyp libraries, and every phase 5–9 family. The register reading of the fingerprint (verse or a list rather than prose with fillers) is untouched by any decoder. [stated]

## 56. Validation release (2026-10-29): the second external review, three code defects fixed, the affected statistics rerun

**The review.** A second outside review of the snapshot at commit f74f4ab (received 2026-10-29; the reviewer rebuilt all 1,439 cross-library streams against the manifest, reproduced the 25 benchmarks at 89–100 % recovery and the core counts 12,956 / 86 / 102 / 11 / 77, and rated the repository 7 of 10) found three implementation defects, one statistical confound, one over-broad claim and several summary statements that outran their experiments. Every point was checked here and every one held. This section records what changed; the review's wording is its author's and is not reproduced. [stated]

**1. The 5-gram model's lower orders were dead** (`src/ngram.py`). The Kneser-Ney continuation table for level k is keyed by (k−1)-rune contexts, and `prob_vec` looked level k up in the table of level k−1, so every context shorter than four runes missed and fell through: the scorer was unigram plus 5-gram, not the advertised interpolation. Fixed to `cont[k]`; the dense cache was deleted and rebuilt; held-out log-likelihood on the solved plaintext moved from −1.963 to −1.870 nats per rune (uniform −3.367); a test now checks that one-, two- and three-rune contexts move the distribution. What this touches: every z_5 in the record was computed with the weaker scorer, whose power was measured as it was, so those measurements stand for that instrument; the §27 power curve was rerun with the fixed model (figures below) and the "What is new" item 5 carries the new number. [stated]

**2. Standalone R4n was R4** (`src/mechanism_lane.py`). When the echo variants were added in §47, the base-rule switch recognised `+R4n` as a suffix and gave the standalone rule the base R0, so its filler branch never ran; the published R4 and R4n rows of `results/mechanism.md` were the same mechanism within noise. Fixed, the lane's run section moved under a main guard so the simulator can be imported, a test checks that R4 and R4n differ under the same seed, and the fourteen-rule table was regenerated (figures below). [stated]

**3. The K-fixed sampler's clock counted acceptances** (`src/kfixed_echo.py`, `src/s_carrier.py`, now `src/kfixed.py`). Both scripts advanced their burn-in and thinning counters only on accepted transpositions, which samples the embedded jump chain and weights each arrangement by its acceptance rate rather than uniformly. On a 24-state toy case the old clock's visit counts give a chi-square of about 100 against the uniform law where the attempt clock gives 20–27 (test added). Both calibrations, the within-word lag echo (§42: z +3.7, family-wise p 0.008) and the S-carrier look-elsewhere p (§45: 0.003), were rerun with the attempt clock (figures below). [stated]

**4. The shared-words claim had a word-length confound.** §42's 18 shared words against 10.8 expected (p 0.012) pooled every word of length ≥ 7; longer words carry more pairs of both kinds. Stratified by exact length the expectation is 14.0 and the permutation p 0.11 (`src/echo_overlap.py`). The claim is downgraded to a description in §42, in the summary and in the status box. [stated]

**5. "Outside every additive mechanism" was too broad.** The §47 argument needs the key value at the echoed position to be uniform conditional on the coincidence, which holds when the key is independent of the plaintext there and fails for a key that reads the plaintext or the written rune (an autokey on S, a marker), which is still additive. The heading, the argument, the summary item and the status rows now say "with a plaintext-independent key"; the open class is named. [stated]

**6. Summaries that outran their experiments.** The §27 status row said "99 % power on all 55 pages"; that is the 5-gram's power on planted soft-rule solutions at 66 runes, while the short-page lane's own controls pass 39 of 45 (4 of 5 at 66 runes), a different measurement; the row now says both. The §46 status row still carried the retracted "fits S exactly"; corrected. The §54 status row states its three-page tier-1 scope. `mpmath` is declared, and "Use it" now gives the two build steps a clean checkout needs before `check_solve.py`. [stated]

**Rerun figures.** (1) 5-gram power by page length, §27's table regenerated with the repaired model: share of plants at z_5 ≥ 6 is 1.00 at every length from 66 to 196 runes (80 of 80 at 66 runes; 0.99 before), median z_5 at 66 runes 21.1. (2) Mechanism table: see the rerun paragraph in §47; standalone R4n fits eight of ten, E56w+R4n is inside the band on all ten with the S cell at z +2.9. (3) Within-word lag echo under the attempt-clock K-fixed null: lag 5 at 102 against 71.8 ± 8.3, z +3.66, family-wise p over lags 2–12 **0.011** (0.008 before); lag 6 equality 31 against 43.6 ± 6.5 as before. (4) S carrier look-elsewhere: S at lag 5 at Poisson mean 2.31, min-tail p 3.1e-05, reached by **0.005** of null replicates (0.003 before). Both p-values moved by less than a factor of two and neither crosses a line the record uses. [stated — `results/rescore_power.md`, `results/mechanism.md`, `results/kfixed_echo.md`, `results/s_carrier.md`]

**What did not change.** None of the six points touches a decode negative: the lanes do not use the n-gram interpolation levels that were broken, their planted controls were recovered with the scorer as it was, and the exclusions hold at the detection limits they state. The corrections bear on the mechanism story (two rows of one table, one p-value that was never load-bearing, one sharpened sentence) and on how the summaries are worded. [inferred]

## 57. E56w+R4n out of sample: fifteen of sixteen cells hold, and the one that fails is the hold repair's signature (`src/e56w_r4n_predictions.py`, `results/e56w_r4n_predictions.md`, `results/e56w_r4n_predictions.json`)

**Why.** After §56 restored the R4n base, E56w+R4n was the only rule inside the pre-registered |z| ≤ 3 band on all ten judged statistics, at the band's edge on two of them, and its filler rate matched the §55 word-length fingerprint without having been fitted to it. Those are the statistics the rule was built or judged on. §49 asked E56w the out-of-sample question; this section asks it of E56w+R4n, in the same form.

**Registered before the look** (commit 3ee66a5, 2026-10-29 15:32, predictions in the JSON with their timestamp): the fourteen cells of §49 unchanged, plus two statistics never computed before, within-word lag-12 hits of T∘T (c = 4c′ − 24, two chained lag-6 echoes) and within-word lag-11 hits of T (a lag-5 and a lag-6 echo chained in either order); two word-length cells (two-rune share, mean length) are declared known from §55 and §56 and are not counted. 300 simulated books of the rule exactly as `src/mechanism_lane.py` defines it after the fix (r = 0.5, q = 0.81, one extra rune in 45 % of words). Rule: a cell holds within |z| ≤ 2.5; the sixteen out-of-sample cells are judged as a set, with about 0.2 chance failures expected. [stated — script header]

**Result: 15 of 16 hold; the lag-6 count in words of ten or more runes fails.** LP2 has 30 such hits; E56w+R4n predicts 59.2 ± 9.3 (z −3.15), where E56w had predicted 36.9 ± 7.1 (z −0.98, §49). The other two length cells hold: 8 hits in 7-rune words against 14.2 ± 3.7, 39 in 8–9-rune words against 43.0 ± 7.3. The two new chained-echo cells hold with nothing to see (lag-12 T∘T: 0 against 1.1 ± 1.0; lag-11 T: 2 against 2.3 ± 1.5), the across-gap cells sit on the prediction (361 lag-5 equalities against 361.6 ± 18.2; 389 lag-6 hits against 384.7 ± 19.2), and the declared word-length cells confirm the §56 remark (two-rune share 0.159 against 0.152 ± 0.008; mean 4.42 against 4.53 ± 0.07). The signs lean negative throughout: the rule makes more echo sites than the pages carry (words with two or more sites 28 against 42.6 ± 6.6, z −2.2; lag-5 pairs in words of nine or more runes 53 against 75.9 ± 10.6, z −2.2), the same over-production that put its lag-6 total at z −2.9 in §47. [stated — `results/e56w_r4n_predictions.md`]

**Reading.** The failing cell is where the rule's two components part. The echo writes 24 − 2c₋₆ only when the plaintext repeats at lag 6, and English puts most of those repeats in words of eight or nine runes; the hold repair writes the same value on every repaired collision at word position six or later, collisions scale with word length, and so its hits pile into the long words. LP2's lag-6 profile by word length, 8 / 39 / 30, is the echo's profile, not the repair's. Put beside §47 and §49: E56w passes the out-of-sample set and fails the S cell; E56w+R4n passes the S cell on the width of its spread and fails an out-of-sample length cell. No rule in the simulator does both. What survives of R4n is its filler, which the fingerprint supports and which the lag-6 profile does not touch. What does not survive is the T-writing hold repair as the source of the lag-6 relation. [inferred]

**Next, to be registered before it is run.** The two echoes on the spend-repair base with the same filler and no T-writing repair (E56w with fillers), scored on §47's ten statistics and these sixteen cells. It is one line in the simulator. It was not run here because it was thought of after the look, and the point of §49 and §57 is that the order is kept. Run as §58.

## 58. E56w with fillers on the spend base: the first rule inside every pre-registered band, and still not the S count (`src/e56w_n_lane.py`, `results/e56w_n.md`, `results/e56w_n.json`, `src/mechanism_lane.py` rule `E56w+n`)

**The rule.** §57 left one named follow-up: keep E56w's two gated echoes and R4n's filler (one extra neighbour-checked rune at a uniform position in 45 % of words of two or more runes), drop R4n's T-writing hold repair, and put the echoes on this repository's own spend repair (q = 0.81). One line in the simulator; registered in the script header before any replicate was run, with the expectation written down: D below E56w's 84, L3 and L4 up toward R4n's, L6T back near E56w's 80, and the S cell expected to fail as E56w's does. Two sets, predicted and committed (3f9f827, 2026-10-29) before the check: §47's ten judged statistics over 200 replicates at §47's |z| ≤ 3, where LP2's values are public, and §57's sixteen out-of-sample cells plus the two declared word-length cells over 300 replicates at |z| ≤ 2.5. [stated — script header]

**Result: survives set A, 16 of 16 in set B.** §47's statistics: D 86 against 76.2 ± 8.3 (z +1.2), D_in 63 against 59.3 ± 7.0, L3 179 against 172.9 ± 12.2, L4 131 against 113.2 ± 10.9 (z +1.6), L5 102 against 132.1 ± 13.4 (z −2.3), BIG 9 against 7.2 ± 3.1, L6T 77 against 85.1 ± 9.8 (z −0.8), SHARE 7.2 against 4.4 ± 3.2, Sfreq on the line, and **L5S 11 against 4.8 ± 2.2 (z +2.7)**. §57's cells: every one holds, with |z| from 0.01 to 2.0; the cell E56w+R4n failed, lag-6 hits in words of ten or more runes, reads 30 against 43.9 ± 7.6 (z −1.8); the length profiles, the multi-site counts, lag 10, the chained-echo lags 11 and 12, the across-gap rates and the repeat rates inside and outside echo words all sit inside the band, and the declared word-length cells match (0.159 against 0.152 ± 0.007; 4.42 against 4.53 ± 0.07). [stated — `results/e56w_n.md`]

**What that is and is not.** It is the first rule in this record inside every pre-registered band at once: ten fitted-or-judged statistics and sixteen it was not built around. Three of its four parts were each fixed before the look (q from the repeat count in §5, r from the equality count in §46, the filler rate from pnotisdev's R4 and confirmed by the §55 fingerprint), and the fourth, dropping the hold repair, was the one change §57 pointed at. The expectation written in the registration was wrong in one place: the S cell did not fail. It passes at z +2.7 on the width of its spread, exactly as E56w+R4n did at +2.9, while predicting five S pairs where the pages have eleven; the rule reproduces the lag-5 echo's count, runs, length profile and word sharing without any S preference, and the S weighting remains the one fact outside it, as §47 and §50 left it. Nor is a generative description a decryption: E56w+n says what the ciphertext looks like under an iid key and English plaintext, and the §48 echo-aware decoder, which is this rule's decoder without the filler, found nothing in the phase 3–4 library; the filler-aware free-null decoder of §55 is its decoder with the filler and found nothing in the external texts or pnotisdev's streams. The practical consequence is for anyone planting controls: a plant under E56w+n is now the most defensible test ciphertext for a Liber Primus decoder, and §55's part B shows what a plain decoder does to it. [inferred]

**Where the rule can still be broken.** Three cheap tests not yet run: (1) the filler rate fitted to the word-length histogram directly rather than taken as 0.45, with the lag-5 and lag-6 counts then predicted; (2) the lag-5 length profile at finer resolution (per exact word length 6 to 12), where set B pools; (3) the rule's prediction of the L4 excess (131 against 113, the one cell at +1.6 in set A besides S) on the solved pages, which have no filler. Each is an afternoon and each should be registered first. Run as §59.

## 59. Three registered follow-ups to E56w+n: the filler rate fitted to the words puts the S cell over the bar, the length profiles hold, the solved pages carry no lag-4 excess (`src/e56w_n_followups.py`, `results/e56w_n_followups.md`, `results/e56w_n_followups.json`)

The three tests named at the end of §58, registered in the script header with their expectations and committed with their predictions (f686ace, 2026-10-29) before the check. [stated]

**T1, the filler rate fitted to the word lengths, then the lag counts predicted.** §58 took the rate 0.45 from pnotisdev's R4. Fitting it to LP2's 2,928 word lengths alone (one filler at a uniform position in a fraction p of words of two or more runes; chi-square of LP2's histogram against 100 simulated books at each p from 0.20 to 0.70) gives a clean minimum at **p* = 0.40**, chi-square 24.7, with 31.4 at 0.35 and 28.6 at 0.45 and the curve rising steeply either side (87 at 0.20, 238 at 0.70). That value sits inside the band §55 measured for random English samples against English itself (median 13, 99th percentile 30), where §55's best simple distortion scored 54: the unsolved pages' word lengths are what English looks like with one extra rune in two words out of five. At p* the lag counts move little (D 77.0 ± 9.4, L3 171, L4 111, L5 128.6, L6T 83.1) and all hold, except that **the S cell fails: 11 against 4.6 ± 2.0, z +3.17**. The expectation in the registration (p* a little below 0.45, L5S near 5) was right; what it did not say is that the slightly narrower spread at p* takes the S cell across §47's bar. [stated — `results/e56w_n_followups.md`]

**T2, the lag-5 and lag-6 profiles per exact word length.** Thirteen cells at the registered rate 0.45 (p* beside them, not judged): lag-5 equal pairs in words of exactly 6 to 11 runes and 12 or more, lag-6 T hits in words of exactly 7 to 11 and 12 or more. **All thirteen hold**, |z| from 0.09 to 1.94; the largest departures are fewer lag-5 pairs in 9- and 11-rune words (15 against 25.1 ± 5.7; 6 against 13.2 ± 4.2) and, at lag 6, more hits in 8-rune words (21 against 14.1 ± 4.0) and fewer in 10-rune words (7 against 16.6 ± 5.0). §57's pooled bins hid no shape. [stated]

**T3, the solved pages.** On the five solved polyalphabetic chunks (919 runes; two Vigenère keys and the totient stream, §41's selection) the within-word equal-pair counts at lags 3, 4, 5 and 6 are 6, 2, 5 and 1, against 11.7 ± 3.7, 8.3 ± 2.9, 5.1 ± 2.3 and 3.3 ± 1.9 from English laid into the same layouts under the same keys: all four inside the band, lag 4 if anything low (z −2.2). The unsolved section's lag-4 rate is 1.19 times uniform (131 of 3,197 pairs); the solved pages' is 0.32 times (2 of 182). The sample is small, as the registration said, so this excludes only a large solved-page excess; within that limit the lag-4 excess joins the repeat deficit and the two echoes as a property of the unsolved section alone. [stated]

**What the three change.** One thing each. T1 turns §58's "passes the S cell on spread" into a failure once the one free rate is set by the data the rule was not fitted to; E56w+n is the best generative description in the record on every other count and does not make the S weighting, which stands as it did in §47 and §50. T1 also closes §55's open "partial fit": the register alternatives (verse, a list) are no longer needed to explain the word lengths, though they are not excluded by them. T2 and T3 add thirteen and four cells to the rule's out-of-sample record without a failure. The simulator's filler rate should be read as 0.40 from here; the §58 table at 0.45 is kept as run. [inferred]
