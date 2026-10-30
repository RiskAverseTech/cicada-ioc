# False gain on wrong keys at page length (§61 part B)

220 cells (page × F × mode), 2,000 random keystreams each through the plain, free-null (−2.2) and both word-constrained decoders. Gain = decoder score − plain score on the same random key. Columns: median over cells of each gain quantile; the margin M(page, F, mode) used by part C is the 99.9th percentile of the chosen decoder's gain on that cell.

| decoder | q50 | q90 | q99 | q99.9 | max |
|---|---|---|---|---|---|
| free-null -2.2 | +95 | +120 | +142 | +158 | +168 |
| wc -2.2 | +87 | +112 | +134 | +150 | +159 |
| wc word0.4 | +97 | +121 | +144 | +159 | +170 |

By page length (chosen decoder, 99.9th percentile gain, median over cells):

- 60–119 runes: +72 nats (12 cells)
- 120–199 runes: +119 nats (24 cells)
- 200–277 runes: +159 nats (184 cells)

## Claims (registration, commit 8ff95b0); chosen decoder from part A: wc -2.2

- B1 median 99.9th-percentile gain, chosen ≤ 0.6 × free-null: **fails** (+150 against +158).
- B2 true-key gain at n = 230, p = 0.4 (part A median 135) exceeds the median margin on pages of 200–277 runes (+159): **fails**. **Margin arm in part C: dropped.**

Runtime: 370 CPU-minutes.
