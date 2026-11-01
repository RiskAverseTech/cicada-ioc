# Lag laws or word-position laws: the two-dimensional word-position table

Registration: `results/word_position_registration.md`. Pairs inside words with both positions below 12; 66 cells per table; K-fixed null 999 arrangements per page; family-wise p from the largest cell z of each table; held-out halves A (even pages) and B (odd pages).

## Cells at family-wise p < 0.05 on the full set

| table | cell (earlier, later) | lag | observed | null mean ± sd | z | family-wise p |
|---|---|---|---|---|---|---|
| equality, from start | none | | | | | |
| affine 24−2c, from start | none | | | | | |
| equality, from end | none | | | | | |
| affine 24−2c, from end | (1, 7) | 6 | 27 | 11.7 ± 3.4 | +4.49 | 0.017 |

Largest cell z per table and its family-wise p: equality, from start +3.32 (0.218); affine 24−2c, from start +3.75 (0.064); equality, from end +2.98 (0.313); affine 24−2c, from end +4.49 (0.017).

## Sharpening along the lag diagonal

| table | diagonal cells (earlier position …) | observed counts | null-share expectation | χ² | multinomial p |
|---|---|---|---|---|---|
| equality, from start | lag 5, 7 cells, n = 102 | [35, 27, 18, 10, 7, 2, 3] | [39.8, 27.3, 17.1, 8.9, 5.2, 2.6, 1.2] | 4.2 | 0.641 |
| affine 24−2c, from start | lag 6, 6 cells, n = 76 | [32, 18, 12, 6, 7, 1] | [33.6, 20.4, 10.8, 6.3, 3.3, 1.5] | 4.9 | 0.423 |
| equality, from end | lag 5, 7 cells, n = 101 | [36, 29, 16, 8, 8, 3, 1] | [39.6, 26.8, 16.8, 8.8, 5.2, 2.6, 1.1] | 2.1 | 0.908 |
| affine 24−2c, from end | lag 6, 6 cells, n = 76 | [31, 27, 8, 5, 5, 0] | [33.6, 20.5, 11.0, 6.2, 3.1, 1.6] | 6.0 | 0.287 |

## Held-out halves

| table | cells family-wise < 0.05 on A | lag | replication on B (one-sided p) |
|---|---|---|---|
| equality, from start | none | | |
| affine 24−2c, from start | none | | |
| equality, from end | none | | |
| affine 24−2c, from end | none | | |

## Registered predictions

- W1 (no off-diagonal cell at family-wise p < 0.05): none → holds.
- W2 (no sharpening along the diagonals): multinomial p 0.641, 0.423, 0.908, 0.287 → holds.
- W3 (off-diagonal cells on A do not replicate on B): 0 cells significant on A → holds.

Runtime 239 s. Reproduce: `.venv/bin/python -I src/word_position.py`.
