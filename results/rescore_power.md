# Rescoring power: rune 5-gram on the decoder's output, by page length

20 plants per cell, 400 nulls, soft rule 0.81, base decoder, max_skip 4; 5-gram trained on the running-key corpus (results/ngram5.npz, held-out solved plaintext −1.96 nats/rune against −3.37 uniform).

| length | share z_uni ≥ 6 (median) | share z_5 ≥ 6 (median) | share z_5 ≥ 7 | median recovery |
|---|---|---|---|---|
| 66 | 0.21 (5.6) | **0.99** (25.9) | 0.99 | 1.00 |
| 76 | 0.54 (6.0) | **1.00** (26.9) | 0.99 | 1.00 |
| 92 | 0.94 (6.8) | **1.00** (30.1) | 1.00 | 1.00 |
| 121 | 1.00 (7.9) | **1.00** (35.2) | 1.00 | 1.00 |
| 137 | 1.00 (8.4) | **1.00** (36.6) | 1.00 | 1.00 |
| 159 | 1.00 (9.2) | **1.00** (39.3) | 1.00 | 1.00 |
| 196 | 1.00 (10.4) | **1.00** (44.7) | 1.00 | 1.00 |

Per family at the two shortest lengths:

| length | family | z_uni ≥ 6 | z_5 ≥ 6 |
|---|---|---|---|
| 66 | vigenere-word | 0.30 | 1.00 |
| 66 | phrase-3 | 0.15 | 1.00 |
| 66 | primes | 0.25 | 0.95 |
| 66 | self running key | 0.15 | 1.00 |
| 76 | vigenere-word | 0.35 | 1.00 |
| 76 | phrase-3 | 0.40 | 1.00 |
| 76 | primes | 0.70 | 1.00 |
| 76 | self running key | 0.70 | 1.00 |
| 92 | vigenere-word | 0.90 | 1.00 |
| 92 | phrase-3 | 0.95 | 1.00 |
| 92 | primes | 1.00 | 1.00 |
| 92 | self running key | 0.90 | 1.00 |

