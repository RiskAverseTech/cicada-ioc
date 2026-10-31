# Post hoc nulls for §70: keys with the library's structure, and a null as large as the library

Written after the §70 sweep (`results/e56_lattice_registration.md`, notes after the run). Part (a): for the five cells with the largest sweep z and two reference pages, the top library key's score is re-nulled against 2,000 uniform keystreams (the registered null, redrawn), 2,000 library keys with their runes permuted (unigram-matched to the library) and 2,000 English windows from the corpus in rune spelling (fully structured running keys). Part (b), `src/e56_bignull.py`: 46,000 uniform keystreams per (page, F) for the three top pages, as many draws as the library has configurations per page.

## (a) Structured nulls, 2,000 keys each

| page | sign | F | library | top key | top z under uniform | under permuted library | under English windows | null keys ≥ top (u / p / e) | null max z on the uniform scale (u / p / e) |
|---|---|---|---|---|---|---|---|---|---|
| LP2-22 | beaufort | 0 | book | self running key plaintext@2824 | 7.48 | 7.23 | 7.32 | 0 / 0 / 0 | 4.9 / 5.7 / 4.5 |
| LP2-02 | add | 1 | book | self running key plaintext@2679 | 7.02 | 6.49 | 6.24 | 0 / 0 / 0 | 3.6 / 4.4 / 4.7 |
| LP2-34 | beaufort | 0 | book | phrase-2 THE MASTER | 7.14 | 6.90 | 6.78 | 0 / 0 / 0 | 4.8 / 4.1 / 4.3 |
| LP2-49 | beaufort | 0 | book | self running key plaintext@314 | 6.72 | 7.36 | 7.76 | 0 / 0 / 0 | 5.1 / 4.4 / 4.0 |
| LP2-14 | add | 1 | primes | prime p-1 s=84 | 6.30 | 6.19 | 6.34 | 0 / 0 / 0 | 4.5 / 4.7 / 3.9 |
| LP2-42 | sub | 0 | book | phrase-4 BY A STUDENT TO | 4.44 | 4.22 | 4.26 | 0 / 1 / 1 | 3.9 / 4.5 / 4.6 |
| LP2-11 | sub | 0 | book | vigenere-word-rev WITHINʳ | 5.27 | 5.52 | 5.96 | 1 / 0 / 0 | 6.0 / 3.8 / 3.8 |

Reading (a): the structured nulls have the same mean, spread and maximum as the uniform null, within a few tenths of a sigma, on every cell; the library's top key stands at the same z under all three. Structured keys do not score higher than random ones under this decoder, so the first explanation offered after the sweep (§69's unigram artefact) is wrong here. What the table does show is the shape of the null: the maximum of 2,000 draws sits at 3.6–5.7 sd across the cells (4.5–5.1 on the top five), where a Gaussian would put it at 3.5. The score distribution is right-skewed, as a lattice decoder that occasionally strings dictionary words together must be. [stated — the table]

## (b) A null as large as the library

| page | F | uniform draws | null maximum (z on the 2,000-draw scale) | draws with z ≥ 6 | z ≥ 5 | z ≥ 4.5 | library top (z) | null draws ≥ library top |
|---|---|---|---|---|---|---|---|---|
| LP2-22 | 0 | 46,000 | 6.14 | 1 | 8 | 16 | 7.32 | 0 |
| LP2-02 | 1 | 46,000 | 6.91 | 1 | 6 | 25 | 7.24 | 0 |
| LP2-49 | 0 | 46,000 | 6.17 | 3 | 16 | 34 | 6.94 | 0 |

Reading (b): a uniform null as large as the library reaches z 6.1–6.9 on its own, with 1–3 draws at z ≥ 6 and 16–34 at z ≥ 4.5 per page, so the registered clauses "z ≥ 6" and "above the maximum of 2,000 draws" are met by chance in any sample the size of a page's library (45,726 configurations). The library's tail is lighter than the null's: 507 of 2,514,930 book decodes at z ≥ 4.5 (2.0e-04 per decode) and 25 at z ≥ 6 (9.9e-06) against 75 of 138,000 null draws (5.4e-04) and 5 (3.6e-05) on the three heaviest-tailed pages; the prime library, 308 of 990,000 at z ≥ 4.5 (3.1e-04), the same. The three library maxima stand 0.3–1.2 sd above their 46,000-draw null maxima, which is what the largest of 55 pages' maxima does under the null when each page's library is itself a sample of 45,726, and none of the three reads. The 29 sweep rows are the tail of the null, not candidates. Registration lesson eight: under a right-skewed score, "above the maximum of n null draws" is a clause about n, not about the page; register a null as large as the library, or a tail-rate comparison, from the start. [stated — the tables; all of this post hoc]

Runtime: part (a) about 3 minutes per cell, part (b) about 1 minute per page on 8 cores. Reproduce: `CELL=k .venv/bin/python -I src/e56_structured_null.py` (k = 0..6); `PAGE=LP2-22 F=0 SHARD=k NSHARD=8 .venv/bin/python -I src/e56_bignull.py`.

