# The word-length fingerprint of the unsolved pages (§55 part A)

Words: 2,928 on the 55 unsolved pages (corrected edges), 698 cipher words on the solved pages. Lengths are in runes (TH, NG, EO, ING are one rune). Columns are the share of words at each length; the last two columns compare each row with the unsolved pages (total-variation distance, and the chi-square the unsolved histogram would have against that row as reference, at n = 2,928).

Against English prose as reference, the unsolved pages' chi-square is **183**; 2,000 bootstrap samples of 2,928 English words give median 13, 99th percentile 30, max 42 (p 0.0005). The solved pages' cipher words give 11 at n = 698, bootstrap median 12, 99th percentile 31 (p 0.597). Mean length: unsolved 4.42, solved 4.01, English prose 4.02, Latin 6.02, Old English 4.32.

| sample | n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | TV | chi² |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **unsolved cipher words** | 2,928 | 3.4 | 15.9 | 24.8 | 17.6 | 10.9 | 8.6 | 7.3 | 5.4 | 2.6 | 1.7 | 1.0 | 0.6 | 0.000 | 0 |
| solved cipher words | 698 | 4.0 | 23.9 | 24.1 | 17.5 | 7.6 | 8.7 | 6.2 | 3.4 | 2.1 | 1.3 | 0.6 | 0.3 | 0.090 | 206 |
| LP translation (solved pages' English) | 727 | 3.9 | 24.5 | 24.3 | 17.3 | 7.7 | 8.4 | 5.9 | 3.3 | 2.2 | 1.2 | 0.6 | 0.3 | 0.092 | 211 |
| English prose (5 books) | 177,798 | 3.7 | 25.4 | 23.2 | 15.6 | 9.8 | 8.2 | 5.3 | 3.9 | 2.7 | 1.3 | 0.6 | 0.3 | 0.098 | 183 |
| Chaucer (Middle English) | 67,643 | 4.5 | 22.0 | 26.1 | 17.9 | 11.0 | 8.0 | 4.9 | 2.8 | 1.6 | 0.8 | 0.3 | 0.1 | 0.090 | 345 |
| Latin (phase 5 corpus) | 52,743 | 1.3 | 12.3 | 9.3 | 10.4 | 12.5 | 12.1 | 12.7 | 9.3 | 7.9 | 5.1 | 3.8 | 2.0 | 0.284 | 1476 |
| Old English (phase 5 corpus) | 26,574 | 0.1 | 17.1 | 22.5 | 17.6 | 18.2 | 12.4 | 6.1 | 3.3 | 1.7 | 0.5 | 0.2 | 0.1 | 0.125 | 2930 |

## English under four distortions

Each row distorts the English prose sample and compares the result with the unsolved pages.

| model | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | TV | chi² |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| separators dropped, d = 0.1 | 3.3 | 22.8 | 21.1 | 14.5 | 9.8 | 8.8 | 6.2 | 4.7 | 3.4 | 2.0 | 1.2 | 0.8 | 0.097 | 148 |
| separators dropped, d = 0.2 | 2.9 | 20.3 | 18.7 | 13.5 | 9.7 | 9.1 | 6.9 | 5.4 | 4.2 | 2.8 | 1.9 | 1.3 | 0.123 | 268 |
| separators dropped, d = 0.3 | 2.6 | 17.7 | 16.5 | 12.1 | 9.3 | 9.2 | 7.2 | 6.0 | 4.8 | 3.5 | 2.6 | 2.0 | 0.162 | 510 |
| separators dropped, d = 0.4 | 2.2 | 15.2 | 14.0 | 10.9 | 8.5 | 8.8 | 7.3 | 6.2 | 5.3 | 4.1 | 3.3 | 2.7 | 0.217 | 903 |
| Poisson(λ = 0.25) fillers per word | 2.9 | 20.6 | 22.9 | 17.4 | 11.2 | 8.8 | 6.0 | 4.3 | 3.0 | 1.6 | 0.8 | 0.4 | 0.056 | 65 |
| Poisson(λ = 0.50) fillers per word | 2.2 | 16.4 | 22.1 | 18.5 | 12.7 | 9.4 | 6.6 | 4.7 | 3.4 | 2.0 | 1.0 | 0.5 | 0.054 | 54 |
| Poisson(λ = 0.75) fillers per word | 1.7 | 13.2 | 20.5 | 19.0 | 14.1 | 10.4 | 7.4 | 5.2 | 3.7 | 2.3 | 1.3 | 0.6 | 0.088 | 143 |
| Poisson(λ = 1.00) fillers per word | 1.3 | 10.7 | 18.5 | 19.1 | 15.4 | 11.3 | 8.1 | 5.9 | 4.2 | 2.7 | 1.5 | 0.8 | 0.136 | 336 |
| a filler after each rune w.p. r = 0.05 | 3.5 | 23.0 | 22.4 | 15.8 | 10.5 | 8.1 | 5.9 | 4.1 | 3.1 | 1.7 | 0.9 | 0.5 | 0.079 | 107 |
| a filler after each rune w.p. r = 0.08 | 3.4 | 21.8 | 21.8 | 16.0 | 10.8 | 8.2 | 6.1 | 4.4 | 3.2 | 2.1 | 1.1 | 0.6 | 0.072 | 89 |
| a filler after each rune w.p. r = 0.10 | 3.3 | 20.8 | 21.6 | 16.1 | 11.0 | 8.3 | 6.2 | 4.5 | 3.3 | 2.2 | 1.3 | 0.7 | 0.071 | 83 |
| a filler after each rune w.p. r = 0.12 | 3.2 | 20.0 | 21.2 | 16.3 | 11.0 | 8.5 | 6.4 | 4.6 | 3.5 | 2.3 | 1.4 | 0.8 | 0.070 | 84 |
| a filler after each rune w.p. r = 0.15 | 3.1 | 18.8 | 20.8 | 16.2 | 11.4 | 8.5 | 6.6 | 4.9 | 3.6 | 2.5 | 1.6 | 0.9 | 0.071 | 91 |
| words of one or two runes removed | 0.0 | 0.0 | 32.7 | 21.9 | 13.8 | 11.5 | 7.5 | 5.5 | 3.7 | 1.8 | 0.8 | 0.4 | 0.196 | 451061 |

Best of the simple distortions: Poisson(λ = 0.50) fillers per word (chi² 54 against the unsolved pages, where English itself scores 183); the best per-word filler model scores 54 and the best per-rune one 83, both still outside the bootstrap range of an English sample (99th percentile 30), so the fit is partial. Reading: the unsolved pages' words are not English prose with its separators intact; of the single-parameter distortions tried, inserted runes fit best, at about one filler per two words (or one per ten runes), a different register (verse, a list) is not excluded, and Latin, Old English, Chaucer and merged words fit worse. [stated]

## Index of coincidence by word position (× 29; uniform = 1.00)

A key that restarts at each word with a fixed keyword would make each word position a monoalphabetic column (IoC ≈ 1.8 for English). Null: 200 per-page shuffles of the runes, positions kept.

| position | from the start: n | IoC | null | z | from the end: n | IoC | null | z |
|---|---|---|---|---|---|---|---|---|
| 0 | 2928 | 0.998 | 1.000 ± 0.003 | -0.7 | 2928 | 1.001 | 1.000 ± 0.002 | +0.6 |
| 1 | 2829 | 0.998 | 1.000 ± 0.002 | -1.1 | 2829 | 1.000 | 1.000 ± 0.003 | +0.0 |
| 2 | 2364 | 0.996 | 1.000 ± 0.003 | -1.3 | 2364 | 1.002 | 1.000 ± 0.003 | +0.7 |
| 3 | 1638 | 0.993 | 1.000 ± 0.005 | -1.4 | 1638 | 0.995 | 1.000 ± 0.004 | -1.2 |
| 4 | 1124 | 1.004 | 1.000 ± 0.007 | +0.7 | 1124 | 0.991 | 1.000 ± 0.006 | -1.3 |
| 5 | 806 | 0.996 | 1.000 ± 0.009 | -0.4 | 806 | 1.008 | 1.000 ± 0.008 | +1.0 |
| 6 | 554 | 0.985 | 1.000 ± 0.013 | -1.1 | 554 | 1.008 | 0.999 ± 0.014 | +0.6 |
| 7 | 340 | 0.994 | 0.996 ± 0.020 | -0.1 | 340 | 1.072 | 1.000 ± 0.022 | +3.3 |

## Repeated cipher words

- Words of ≥ 3 runes: 2,348 distinct; repeated occurrences 16 (null 10.3 ± 2.9).
- Words of ≥ 4 runes: 1,638 distinct; repeated occurrences 0 (null 0.2 ± 0.4).

English prose of 2,928 words repeats hundreds of its words of four or more runes (THAT, WITH, THIS, HAVE, ...). Zero repeats of four-rune cipher words is what any key that does not restart with the word gives; together with the flat positional IoC it excludes a per-word restarting key with a fixed keyword, the one family that could have carried the S weighting through a constant key at a word position (§47's uniform-key argument). [stated]

Runtime 3 s. Reproduce: `.venv/bin/python -I src/wordlen_fingerprint.py`.
