# Per-word period-5 key as a mixture: English's own lag-5 statistics against LP2's

LP2: 2,073 within-word lag-5 pairs; equal 4.92 % (102), S..S 0.53 % (11), repeated bigrams 0.71 % (9 of 1,267 adjacent pair-pairs), difference chi-square 38.9.
English (Emerson, 47,730 pairs): equal 6.31 %, S..S 0.96 %, repeated bigrams 0.68 %, difference chi-square per 2,073 pairs 130.6.

Under a period-5 key in a fraction f of the long words and a uniform-difference cipher elsewhere, the equality, bigram and difference statistics are f·English + (1−f)·uniform. The S..S count is NOT English's: an equal cipher pair takes the value p + k, which is uniform over the key, so it is S with probability 1/29 whatever the plaintext; the prediction is (equal pairs)/29. (The first version of this file used English's own S..S rate here, which was wrong; corrected 2026-10-28 after the §47 simulation showed it.) Predicted values:

| f | equal pairs | S..S pairs | repeated bigrams | difference chi-square |
|---|---|---|---|---|
| 0.0 | 71 | 2.5 | 1.5 | 28 |
| 0.1 | 77 | 2.7 | 2.2 | 29 |
| 0.2 | 83 | 2.9 | 2.9 | 33 |
| 0.3 | 89 | 3.1 | 3.7 | 40 |
| 0.4 | 95 | 3.3 | 4.4 | 49 |
| 0.5 | 101 | 3.5 | 5.1 | 61 |
| 0.6 | 107 | 3.7 | 5.8 | 75 |
| 0.7 | 113 | 3.9 | 6.5 | 92 |
| 0.8 | 119 | 4.1 | 7.2 | 112 |
| 1.0 | 131 | 4.5 | 8.7 | 159 |

LP2 observed: 102 / 11 / 9 / 38.9. The f that fits the equality excess (0.5) predicts 3.5 S..S pairs against 11 and a difference chi-square of 61 against 38.9: the mixture fits one number with one parameter and fails two.

English within-word lag-5 difference histogram (share per difference, 0 = equal):

| d | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| English | 6.3 | 4.0 | 2.7 | 3.5 | 2.9 | 4.2 | 4.0 | 2.7 | 3.6 | 4.4 | 3.3 | 3.1 | 3.5 | 3.1 | 5.1 | 4.0 | 2.6 | 2.8 | 2.4 | 2.9 | 4.2 | 3.4 | 1.7 | 3.7 | 2.8 | 3.3 | 3.2 | 3.1 | 3.6 |
| LP2 | 4.9 | 3.6 | 3.2 | 3.5 | 3.6 | 3.6 | 3.7 | 2.7 | 3.5 | 3.5 | 3.3 | 4.1 | 3.7 | 3.8 | 3.3 | 3.6 | 3.3 | 3.4 | 3.1 | 2.1 | 3.2 | 2.9 | 3.6 | 3.8 | 3.0 | 3.5 | 2.8 | 3.6 | 3.7 |

