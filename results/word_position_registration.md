# Registration: are the echoes lag laws or word-position laws? The two-dimensional word-position table, written before any run

Date 2026-11-01 (evening, EDT). The last test before the pause, named first by a Quorum ranking panel (the debate is kept
privately): re-index every rune by its position in the word, from the start and from the end, and ask whether the two echoes
sharpen into particular position cells or lie along the lag diagonals as lag laws should. §42 tested the lag-5 sites against
position from the word's start and §82 against the end, one dimension at a time; the two-dimensional table, with a held-out
page split and a family-wise correction, has not been built. Nothing below has been run.

## Method (`src/word_position.py`, `results/word_position.md`)

Pairs (i, j), i < j, inside a word, with both positions at most 11 from the word's start (66 cells, (p_i, p_j)); and the same
pairs indexed by distance from the word's end (66 cells, (d_j, d_i)). Two counts per cell: equalities (c_j = c_i) and affine
hits (c_j = 24 − 2c_i), any lag. Null: the audit's K-fixed arrangements (999 per page, seed 1034, burn-in 20, thinning 4),
every cell recomputed inside every arrangement and standardized by its own null mean and sd; family-wise level per table from
the permutation distribution of the largest cell z over its 66 cells. Four tables: equality and affine, start- and
end-indexed.

**Sharpening.** Along the lag-5 diagonal of the equality table (p_j − p_i = 5) and the lag-6 diagonal of the affine table,
the observed counts' distribution across the diagonal's cells against the null's cell shares, by a chi-square whose p comes
from 10,000 multinomial draws of the observed total at the null shares; the same for the end-indexed tables. A lag law
spreads its excess along the diagonal in the null's proportions; a position law concentrates it.

**Held-out split, fixed now.** Half A = the 28 pages with even index (LP2-00, 02, …), half B = the 27 with odd index. Any
cell at family-wise p < 0.05 on A is tested on B at one-sided nominal p < 0.05; a cell counts as replicated only then.

## Predictions

- **W1 (no off-diagonal cell).** On the full set, every cell at family-wise p < 0.05 in the equality tables lies on the
  lag-5 diagonal and in the affine tables on the lag-6 diagonal; no cell at another lag reaches it, under either indexing.
- **W2 (no sharpening).** The diagonal chi-square p is at least 0.05 for the lag-5 equality diagonal and the lag-6 affine
  diagonal, under both indexings.
- **W3 (held-out).** No off-diagonal cell is family-wise significant on half A; if any is, it fails to replicate on B.
  Diagonal cells significant on A replicate on B or not, reported either way.

Expected: W1, W2, W3 hold, and the echoes are lag laws as §42 described them. If W2 fails, the echo in question is restated as
a word-position law in §0 and §81 before the pause, since that would change the process reading; if W1 fails, the new cell is
reported first with its replication.

## Reproduce

`.venv/bin/python -I src/word_position.py`
