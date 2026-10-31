# Registration: two checks prompted by the 2026-10-31 Quorum debate (rows C9 and C10)

*Written and committed 2026-10-31 before either script ran. The debate (quorumsays.com/q/36o14sRgY65E; Claude, GPT, Gemini, Grok) asked two things of the record: whether the lag-5 excess survives once the lag-6 relation is conditioned on, since a fixed lag-6 echo could manufacture lag-5 coincidences; and whether the page is the right unit, since every decoder here treats it as one. Its second "ask next", whether one fixed insertion rule restores about 447 doublets and ordinary word lengths, is §58–§59's result (E56w+n reproduces the deficit by the spend repair, the word lengths by the filler share) and is not rerun.*

## C9. Lag-5 equality conditional on the lag-6 relation (`src/lag5_given_lag6.py` → `results/lag5_given_lag6.md`)

**Definitions (as in §42, §45 and `src/kfixed_echo.py`).** Within-word pairs only. A lag-6 site is a pair (i−6, i) with c_i = 24 − 2·c_(i−6) mod 29; a lag-5 site is a pair (j−5, j) with c_j = c_(j−5). A lag-5 pair *touches* the lag-6 relation when either of its positions is an endpoint of a lag-6 site; otherwise it is *free*. The converse strata are defined the same way for lag-6 pairs against lag-5 sites. The S..S subset of lag-5 equalities is reported in each stratum.

**Null.** The K-fixed Metropolis null of §42/§56 (`src/kfixed.py`): per page, arrangements with the page's rune multiplicities, word structure and adjacent-repeat count held fixed; 20 burn-in and 4 thinning attempted transpositions per rune; 999 replicates; seed 1034. The strata are recomputed inside every null arrangement, so the null is joint.

**Predictions, written before the run.**
- C9-P1 (the two echoes are separate events, as E56w+n models them): the free lag-5 stratum carries the excess: observed / null mean ≥ 1.25 and z ≥ +2.5 (the whole-set figures are 102 / 71.8, z +3.66; the free stratum holds roughly 97 % of the 2,073 pairs, so its power is nearly the whole set's).
- C9-P2: the touching lag-5 stratum holds fewer than 10 equalities and cannot carry the excess on its own.
- C9-P3 (converse): the free lag-6 stratum shows the lag-6 relation at z ≥ +3.
- Falsifier, the panel's conjecture: free lag-5 stratum z < +1.5 while the touching stratum holds ≥ 15 of the equalities.

**What each outcome means.** P1–P3 hold: the lag-5 and lag-6 effects are not one effect seen twice; §58's two gated events stand; nothing in the record changes. P1 fails: the lag-5 excess is a shadow of the lag-6 relation; §58's lag-5 component and the S-carrier reading (§45, §47, §50; row C1) are re-examined; the S carrier would then be a property of the lag-6 sites.

## C10. Is the page a unit? (`src/page_joins.py` → `results/page_joins.md`)

**Fact noticed while preparing this registration, not in the record in these words.** In the master transcription a page that ends on a rune with no word separator continues its word on the next page: the solved page 0.3 ends ADHEREN and page 0.4 begins CE (chunks 11 and 12), and chunk 30 begins with a separator where the previous page's word ended. By that convention 32 of the 54 unsolved page joins fall inside a word (`results/lag_spectrum.md` already records 0 doublets at the 54 joins against 1.9 if random). Every within-word statistic in the record has treated the two halves of such a word as two words; the cross-join pairs (at most a few dozen per lag) were never counted.

**Statistics.** (a) The 32 joined words' lengths against the lengths of words lying wholly inside a page (KS). (b) The page-join split rate (32/54) against the line-break split rate (452/630, §33). (c) Doublets at the 32 mid-word joins: 0 known; expected 1.10 under per-page reset (32/29) and 0.16 at the within-word repeat rate; the likelihood ratio is reported. (d) Cross-join within-word pairs at lags 2–6: equalities and lag-6 affine hits against chance (1/29) and against the within-page within-word rates of §42 (lag-5 equality 102/2,073, lag-6 relation 77/1,267).

**Predictions, written before the run.**
- C10-P1: the joined words are ordinary words split by the layout: KS p > 0.05 against within-page word lengths, and the join split rate is of the order of the line split rate (both are a greedy fill).
- C10-P2: (c) and (d) have no power at these counts (expected equalities per lag ≈ 1–2 under either reading) and are reported as description, not evidence. Registered so that no count among them is later read as a finding.

**What the fact itself means, whatever (c) and (d) show.** The plaintext runs across page joins, so the page is a typographic unit like the line (§65), not a unit of the text. Whether the *key* also runs across pages is a decode question, not a statistic: a stream key continuous through the section sits at each page's cumulative position (≈ 235·k runes, less the fillers, which consume no key, plus the skips), and the filler-aware lanes covered stream offsets 0–1,999 only (§55 part C, §62); §54 covered 0–19,672 under the plain decoder, whose power against the filler form is 0.02 (§60). That window, offsets from about 0.90·cum_k to cum_k + 50 for each page k, under the free-null decoder over the 580 non-periodic streams and the three prime streams, with the E56 lattice decoder on anything above the free-null line, is registered here as the follow-on lane **C11** (row B2 reopened with a pointer). It is not run tonight. Acceptance for C11 when run: the §62 rule unchanged (free-null z ≥ 6, rank 1 in its stream and sign, above the empirical null maximum, readable), controls = six plants at cumulative offsets.

## Notes after the run (C10, 2026-10-31)

C10-P1 failed as registered and the registered null was wrong: a page break at a uniform position falls inside a word with probability proportional to the word's internal gaps, so the split words are length-biased by selection (mean 6.5 against 4.5 for all within-page words). Against the length-biased distribution the split words are ordinary (KS p 0.72). The corrected comparison is reported in `results/page_joins.md` as post hoc. Lesson seven for the registration list: a null for a selected subset must carry the selection that defined the subset. The split rate among non-paragraph-final joins (0.70) equals the line-break split rate (0.72), which is the supporting fact P1 was meant to establish and did not need a KS test for.
