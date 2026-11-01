# Registration: an audit of the two foreground facts, written before any run

Date 2026-11-01 (afternoon, EDT). Nothing below has been run.

## Why

Every mechanism lane since §73 has been judged against two facts measured once, in §42, under one null: eleven S pairs among
the 102 within-word lag-5 equalities (z +3.66 K-fixed for the count, S at z +4.0), and 77 within-word lag-6 hits of the map
c = 24 − 2c′ against 43.7 ± 6.5 (z +5.1). Five constructions now stop at exactly those two cells, and the record reads that as
a wall with a missing part behind it. Yesterday one word in a licence file made half of a published signal and nobody had
looked (§77, lesson twelve). Before another instrument is aimed at the two facts, they are stress-tested the same way: by
removal, by concentration, and under a second null. The audit does not add a fact; it decides whether the existing two carry
the weight the record has put on them. [stated — the sections cited]

## Method (`src/foreground_audit.py`, `results/foreground_audit.md`)

Definitions as §42 and `src/lag5_given_lag6.py`: the 55 pages parsed with the transcription's word marks, within-word pairs
only. Two nulls: the **K-fixed** Metropolis null of §42 (999 arrangements per page keeping rune multiplicities, word structure
and the adjacent-repeat count; 20 burn-in and 4 thinning attempted transpositions per rune; attempt-counting clock), and the
**word-preserving shuffle** (999 within-page permutations of the runes, word structure kept, K free).

1. **Reproduction.** The four §42 numbers under the K-fixed null: lag-5 equalities, S..S pairs, lag-6 hits, with z and p.
2. **Leave one page out.** For each of the 55 pages, both facts' z over the other 54 (per-page null samples are independent, so
   the subset null is the sum over the remaining pages); the smallest and largest z over the 55 leaves, and the five pages with
   the largest contributions (observed minus null mean).
3. **Concentration at lag 6.** The 77 hits by (earlier rune, later rune) pair: the largest pair's share, the number of distinct
   pairs, the share through the fixed point H → H, each against the K-fixed null's distribution of the same quantity among its
   own hits (the null has about 44 hits per arrangement, so shares and ratios are compared, not counts).
4. **Concentration at lag 5.** The 102 equalities by rune value (the largest value's share beside S's), by page and by word.
5. **Word forms.** The words that carry sites, listed; how many site words are exact repeats of another site word, and the
   largest number of sites any one word form carries, against the same quantities for words of the same lengths drawn at random
   from the pages (the GUTENBERG question asked of the pages).
6. **The eleven S pairs in full**: page, word, position, the word's form, and whether the form recurs.
7. **Second null.** Items 1 and 2 again under the word-preserving shuffle.

## Predictions

- **F1 (stability).** For both facts, every leave-one-page-out z lies within 1.0 of the full z, and no page contributes more
  than a fifth of either excess.
- **F2 (spread at lag 6).** The most frequent (earlier, later) pair holds under 15 % of the 77 hits; the number of distinct
  pairs is at least 45 % of the hit count; the H → H share is inside the null's central 95 %.
- **F3 (word forms).** No word form carries more than three sites, pooled over both echoes, and fewer than 15 % of site words
  are exact repeats of another site word.
- **F4 (the S pairs).** The eleven lie in at least eight distinct word forms on at least six pages.
- **F5 (second null).** Under the word-preserving shuffle both facts stand at z ≥ 3.

Expected: all five hold; §42 found the lag-6 value profile flat and §50 looked at the eleven S sites in the images, so partial
checks exist, but leave-one-out, pair concentration and word-form repeats have never been run. If any prediction fails, the
fact is restated with its concentration, the odds table is amended, and the "five constructions at one wall" sentence of §79 is
re-examined before any new lane. Cost: an afternoon.

## Reproduce

`.venv/bin/python -I src/foreground_audit.py`

## Outcome (2026-11-01, afternoon; README §80)

F1 holds (leave-one-out z 3.19–3.96, 5.35–6.25, 4.62–5.40; no page over 15 % of any excess). F2 fails as written on a clause built against a ratio with a ceiling the clause ignored: 77 hits on 27 of the map's 29 pairs, 27.1 expected if uniform; largest pair 6 of 77; H→H 2 of 77 inside the null (lesson thirteen). F3 fails on one word: SDNGGLSDNG (LP2-50, §46's trigram run) carries four sites; no site word's form recurs anywhere on the pages (0.000; the first computation, 0.346, counted a word's own second site and was corrected before anything was written: lesson fourteen). F4 holds (eleven words on eleven pages). F5 holds (shuffle z +3.84, +5.66, +5.02). The two facts stand.
