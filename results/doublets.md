# Which constructions reproduce the signature?

Observed on the unsolved pages: doublets 86, non-zero lag-1 class chi² 42 (27 dof), unigram chi² 26 (28 dof), IC 0.0345.
Each construction: 200 replicates of solved-page plaintext cut into the 55 real page lengths. z = (observed − construction mean) / construction sd;
a construction is consistent with the pages when every |z| is small. Doublets is the discriminating column.

| construction | doublets (mean ± sd) | z | lag-1 class chi² | z | unigram chi² | z | IC | z | verdict |
|---|---|---|---|---|---|---|---|---|---|
| independent uniform keystream (control) | 446 ± 20 | -18.1 | 27 | +1.9 | 28 | -0.2 | 0.0345 | -0.2 | ruled out |
| running key from English (solved text, random offset) | 465 ± 22 | -17.4 | 38 | +0.4 | 739 | -13.1 | 0.0364 | -13.1 | ruled out |
| hand pad: uniform key that never repeats a symbol | 448 ± 20 | -17.9 | 30 | +1.5 | 28 | -0.2 | 0.0345 | -0.2 | ruled out |
| plaintext autokey, lag 1 | 698 ± 31 | -19.6 | 1136 | -12.3 | 1977 | -15.7 | 0.0397 | -15.7 | ruled out |
| plaintext autokey, lag 2 | 481 ± 21 | -18.5 | 230 | -6.8 | 1355 | -17.5 | 0.0380 | -17.5 | ruled out |
| plaintext autokey, lag 5 | 522 ± 29 | -14.9 | 309 | -6.1 | 930 | -18.8 | 0.0369 | -18.8 | ruled out |
| ciphertext autokey, lag 1 | 207 ± 14 | -8.9 | 9903 | -56.8 | 29 | -0.3 | 0.0345 | -0.3 | ruled out |
| ciphertext autokey, lag 2 | 445 ± 23 | -15.6 | 25 | +2.4 | 25 | +0.3 | 0.0345 | +0.3 | ruled out |
| ciphertext autokey, lag 5 | 443 ± 20 | -17.9 | 27 | +1.9 | 27 | -0.1 | 0.0345 | -0.1 | ruled out |
| ciphertext autokey, lag 1, offset so doublet⇔EA | 86 ± 9 | -0.1 | 9629 | -66.1 | 24 | +0.3 | 0.0345 | +0.3 | matches doublets, fails lag-1 structure |
| ciphertext autokey, lag 1, offset so doublet⇔EO (never) | 0 ± 0 | +86000000000.0 | 9400 | -54.5 | 24 | +0.3 | 0.0345 | +0.3 | ruled out |
| Vigenère key 8, step key when a doublet would form | 15 ± 6 | +12.2 | 32 | +1.2 | 49 | -1.5 | 0.0345 | -1.5 | ruled out |
| book Vigenère DIVINITY with F-skip | 506 ± 21 | -20.4 | 193 | -5.3 | 2583 | -27.7 | 0.0413 | -27.7 | ruled out |
| book totient prime stream with F-skip | 430 ± 22 | -15.6 | 197 | -5.1 | 144 | -4.9 | 0.0348 | -4.9 | ruled out |
| uniform key + anti-doublet rule (always +1) | 0 ± 0 | +86000000000.0 | 438 | -7.0 | 26 | +0.0 | 0.0345 | +0.0 | ruled out |
| uniform key + anti-doublet rule (81% of the time) | 84 ± 9 | +0.2 | 299 | -5.8 | 27 | -0.0 | 0.0345 | -0.0 | matches doublets, fails lag-1 structure |
| keystream re-rolled until no doublet (hard rule) | 0 ± 0 | +86000000000.0 | 27 | +2.0 | 26 | +0.1 | 0.0345 | +0.1 | ruled out |
| keystream re-rolled when it would repeat, 81% of the time (soft rule) | 87 ± 10 | -0.1 | 27 | +1.7 | 28 | -0.2 | 0.0345 | -0.2 | **consistent on all four** |
| keystream re-rolled when it would repeat, 70% of the time | 137 ± 12 | -4.2 | 26 | +2.1 | 27 | -0.0 | 0.0345 | -0.0 | ruled out |
| keystream re-rolled when it would repeat, 90% of the time | 46 ± 6 | +6.6 | 27 | +2.2 | 27 | -0.1 | 0.0345 | -0.1 | ruled out |

## Reading

- Anything additive with a key independent of the text (uniform, running key, hand pad, the book's own Vigenère and totient streams) gives
  doublets at the uniform rate: a doublet needs P_i − P_{i+1} ≡ K_{i+1} − K_i, and an independent key hits that one time in 29 whatever it does.
- Autokeys tie the key to the text and change the doublet rate, but not downward enough (plaintext autokey raises it; ciphertext autokey makes a
  doublet a plaintext F, about 1.6%) and they leave a non-flat lag-1 structure that the pages do not show.
- A ciphertext-feedback rule with a chosen offset can hit any doublet rate, including the observed one, but then the lag-1 difference stream is
  the plaintext shifted, with IC 0.06, and the pages' lag-1 stream is flat (IC 0.0353). Ruled out on that column.
- What matches is a key that is otherwise random and is rejected, most of the time, exactly when it would repeat the previous rune: a soft
  anti-repeat rule applied to about four doublets in five. A hard rule (never repeat) overshoots to zero doublets; the pages have 86.

