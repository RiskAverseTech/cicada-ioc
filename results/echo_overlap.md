# Word sharing between the two echoes: pooled and length-stratified

Words of length ≥ 7 on the 55 unsolved pages: 554; with a within-word lag-5 equality 83; with a within-word lag-6 relation 72; with both **18**.

- Pooled (§42's calculation): expected 10.8; permutation of the lag-6 labels over all 554 words, 20,000 draws: mean 10.8, one-sided p = **0.011**.
- Stratified by exact word length (labels permuted within each length): expected 14.0, permutation mean 14.0, one-sided p = **0.111**.

| word length | words | lag-5 echo | lag-6 relation | both | expected both |
|---|---|---|---|---|---|
| 7 | 214 | 18 | 8 | 1 | 0.7 |
| 8 | 159 | 18 | 21 | 5 | 2.4 |
| 9 | 77 | 15 | 17 | 3 | 3.3 |
| 10 | 51 | 16 | 6 | 1 | 1.9 |
| 11 | 28 | 6 | 12 | 3 | 2.6 |
| 12+ | 25 | 10 | 8 | 5 | 3.2 |

Reading: once each pattern's rate is allowed to depend on word length, the shared-word excess is 18 against 14, p about 0.1. The sharing stands as a description, not as evidence that one word-level process produces both echoes; §42, §45 and the summary are worded accordingly from 2026-10-29. [stated]

Runtime 1 s. Reproduce: `.venv/bin/python -I src/echo_overlap.py`.
