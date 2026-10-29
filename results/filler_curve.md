# The filler power curve (§60)

Plants: English (Emerson) under the soft rule q = 0.81; one plaintext and key per plant, shared by its eight filler cells. Per-rune fillers at r (a filler after each emitted rune w.p. r) and the §59 per-word form at p (one filler at a uniform position in a fraction p of the words of two or more runes). 12 plants per (n, family), signs and F cycled; z over 400 random keystreams through the same decoder; rank in the family (538 Vigenère keys, 303 prime streams, 4096 neighbouring offsets). **Recovered = z ≥ 6 and rank 1.** Cells: power / median z of the true key; fillers = mean count in the window.

## plain decoder

| n | family | r=0.00 | r=0.01 | r=0.02 | r=0.05 | r=0.10 | p=0.2 | p=0.4 | p=0.6 |
|---|---|---|---|---|---|---|---|---|---|
| 100 | vigenere-word | 1.00 / 7.2 | 0.58 / 6.5 | 0.50 / 6.1 | 0.33 / 5.1 | 0.00 / 2.8 | 0.08 / 2.5 | 0.00 / 2.5 | 0.00 / 2.6 |
| 100 | primes | 0.92 / 7.0 | 0.67 / 6.7 | 0.50 / 6.5 | 0.08 / 0.8 | 0.00 / 1.0 | 0.08 / 1.2 | 0.00 / 1.0 | 0.00 / 0.5 |
| 100 | running key | 0.83 / 6.8 | 0.50 / 6.1 | 0.50 / 6.1 | 0.17 / 4.3 | 0.00 / 2.0 | 0.00 / 2.6 | 0.00 / 1.4 | 0.00 / 0.6 |
| 160 | vigenere-word | 1.00 / 9.2 | 0.83 / 8.4 | 0.75 / 7.6 | 0.25 / 4.2 | 0.00 / 3.1 | 0.17 / 4.2 | 0.08 / 4.1 | 0.00 / 1.8 |
| 160 | primes | 0.92 / 9.7 | 0.75 / 8.8 | 0.50 / 6.4 | 0.00 / 1.7 | 0.00 / 1.0 | 0.50 / 6.1 | 0.00 / 1.2 | 0.00 / 0.3 |
| 160 | running key | 0.92 / 9.5 | 0.67 / 8.9 | 0.67 / 7.8 | 0.25 / 3.8 | 0.00 / 1.6 | 0.17 / 3.3 | 0.00 / 0.6 | 0.00 / 1.1 |
| 230 | vigenere-word | 1.00 / 12.1 | 1.00 / 10.4 | 0.75 / 8.8 | 0.50 / 5.9 | 0.08 / 3.5 | 0.25 / 4.8 | 0.08 / 2.5 | 0.00 / 2.4 |
| 230 | primes | 0.92 / 10.9 | 0.67 / 9.5 | 0.50 / 8.3 | 0.17 / 2.6 | 0.00 / 0.9 | 0.08 / 3.3 | 0.00 / 1.2 | 0.00 / 0.7 |
| 230 | running key | 0.83 / 12.5 | 0.67 / 11.6 | 0.50 / 7.2 | 0.08 / 3.7 | 0.00 / 1.8 | 0.00 / 3.3 | 0.00 / 2.4 | 0.00 / 1.1 |

## free-null -2.2 decoder

| n | family | r=0.00 | r=0.01 | r=0.02 | r=0.05 | r=0.10 | p=0.2 | p=0.4 | p=0.6 |
|---|---|---|---|---|---|---|---|---|---|
| 100 | vigenere-word | 1.00 / 10.2 | 1.00 / 10.0 | 1.00 / 9.3 | 1.00 / 9.4 | 0.75 / 7.8 | 1.00 / 8.9 | 0.83 / 8.5 | 0.67 / 6.3 |
| 100 | primes | 0.92 / 9.1 | 0.92 / 9.0 | 0.92 / 9.0 | 0.75 / 8.3 | 0.42 / 6.7 | 0.67 / 7.8 | 0.42 / 6.3 | 0.17 / 5.1 |
| 100 | running key | 0.92 / 9.6 | 0.92 / 9.8 | 0.92 / 9.3 | 0.75 / 8.3 | 0.42 / 6.9 | 0.58 / 8.1 | 0.75 / 7.3 | 0.17 / 5.2 |
| 160 | vigenere-word | 1.00 / 14.0 | 1.00 / 13.2 | 1.00 / 12.8 | 1.00 / 11.6 | 1.00 / 9.3 | 1.00 / 11.7 | 1.00 / 10.2 | 0.92 / 7.7 |
| 160 | primes | 0.75 / 14.2 | 0.75 / 13.6 | 0.67 / 13.4 | 0.67 / 12.1 | 0.75 / 9.9 | 0.75 / 12.4 | 0.67 / 10.0 | 0.67 / 8.2 |
| 160 | running key | 0.83 / 13.6 | 0.83 / 13.0 | 0.83 / 13.2 | 0.75 / 10.9 | 0.67 / 9.4 | 0.67 / 11.1 | 0.67 / 9.4 | 0.42 / 7.8 |
| 230 | vigenere-word | 1.00 / 16.9 | 1.00 / 16.1 | 1.00 / 15.4 | 1.00 / 14.0 | 1.00 / 11.5 | 1.00 / 13.6 | 1.00 / 11.1 | 1.00 / 9.0 |
| 230 | primes | 0.92 / 15.9 | 0.92 / 15.7 | 0.92 / 14.6 | 0.83 / 13.4 | 0.67 / 10.2 | 0.83 / 13.6 | 0.75 / 11.7 | 0.50 / 9.1 |
| 230 | running key | 0.83 / 17.2 | 0.75 / 16.8 | 0.83 / 15.5 | 0.92 / 14.8 | 0.42 / 11.8 | 0.83 / 13.6 | 0.67 / 11.6 | 0.50 / 9.3 |

Mean fillers per window (all families): r=0.01: 1.6, r=0.02: 3.3, r=0.05: 7.4, r=0.10: 14.8, p=0.2: 8.1, p=0.4: 14.2, p=0.6: 21.0

## The seven claims (results/filler_curve_registration.md, commit 92af8b9)

- C1 plain power ≤ 0.50 at every r ≥ 0.02: **fails** (max 0.75).
- C2 plain power ≤ 0.10 at r = 0.05, 0.10 and every p: **fails** (max 0.50).
- C3 plain power in [0.15, 0.65] in ≥ 6 of 9 cells at r = 0.01: **fails** (2 of 9; cells 0.58, 0.67, 0.50, 0.83, 0.75, 0.67, 1.00, 0.67, 0.67).
- C4 free-null power ≥ 0.75 at r ≤ 0.02, n ≥ 160: **fails** (min 0.67).
- C5 free-null power at p = 0.4 within ±0.25 of r = 0.10, same cell: **fails** (max gap 0.33).
- C6 plain power crosses 0.5 between r = 0 and r = 0.02 in every (n, family): **fails**.
- C7 Spearman(z_plain, first-filler position) ≥ 0.5 over 718 filler plants: **holds** (ρ = 0.62).

Runtime: 293 CPU-minutes over 8 shards. Reproduce: `for k in 0..7: SHARD=$k NSHARD=8 .venv/bin/python -I src/filler_curve.py`, then `MERGE=1`.
