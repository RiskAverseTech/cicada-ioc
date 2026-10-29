# Layout follow-up: registration

Written 2026-10-28 20:07:10. Null shares come from the pair populations only; no equality count was read.

| A: split position s | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| wrapping lag-5 pairs | 80 | 78 | 81 | 101 | 88 |
| null share | 0.187 | 0.182 | 0.189 | 0.236 | 0.206 |

| B: distance to line edge d | 0 | 1 | 2 | 3-4 | 5+ |
|---|---|---|---|---|---|
| same-line lag-5 pairs | 197 | 172 | 173 | 388 | 715 |
| null share | 0.120 | 0.105 | 0.105 | 0.236 | 0.435 |

Decision rule: simulated chi-square p < 0.01 on A or on B counts as support for a layout step.
