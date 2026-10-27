# Detection power of the z >= 6 rule by page length and key family

20 plants per cell, 400 random-keystream nulls per plant, signs and F variants cycled; decoder max_skip 4; lane A soft rule 0.81 with the base decoder; lane B hard rule + uniform nulls at 0.22 with the free-null decoder at prior -0.8. Power = share of correct keys at z >= 6; median z and median plaintext recovery in brackets.

## Lane A: soft anti-repeat rule, base decoder (phases 3-9)

| length | vigenere-word | phrase-3 | primes | self running key | all |
|---|---|---|---|---|---|
| 66 | **0.25** (z 5.5, rec 1.00) | **0.15** (z 5.4, rec 1.00) | **0.25** (z 5.7, rec 1.00) | **0.25** (z 5.5, rec 1.00) | **0.23** |
| 92 | **0.90** (z 6.5, rec 1.00) | **0.90** (z 6.6, rec 0.99) | **0.90** (z 6.6, rec 1.00) | **0.95** (z 6.8, rec 1.00) | **0.91** |
| 120 | **1.00** (z 7.9, rec 1.00) | **1.00** (z 8.0, rec 1.00) | **1.00** (z 7.8, rec 1.00) | **1.00** (z 8.0, rec 1.00) | **1.00** |
| 160 | **1.00** (z 9.3, rec 1.00) | **1.00** (z 9.2, rec 1.00) | **1.00** (z 9.0, rec 1.00) | **1.00** (z 9.5, rec 1.00) | **1.00** |
| 200 | **1.00** (z 10.4, rec 1.00) | **1.00** (z 10.6, rec 1.00) | **1.00** (z 10.3, rec 1.00) | **1.00** (z 10.5, rec 1.00) | **1.00** |
| 240 | **1.00** (z 12.1, rec 1.00) | **1.00** (z 12.3, rec 0.99) | **1.00** (z 11.6, rec 1.00) | **1.00** (z 12.0, rec 0.99) | **1.00** |
| 277 | **1.00** (z 12.9, rec 1.00) | **1.00** (z 13.4, rec 1.00) | **1.00** (z 12.9, rec 1.00) | **1.00** (z 13.1, rec 0.99) | **1.00** |

## Lane B: hard rule + 22 % nulls, free-null decoder (phase 10)

| length | vigenere-word | phrase-3 | primes | self running key | all |
|---|---|---|---|---|---|
| 66 | **0.10** (z 4.0, rec 0.74) | **0.05** (z 3.9, rec 0.78) | **0.00** (z 4.4, rec 0.79) | **0.05** (z 3.8, rec 0.76) | **0.05** |
| 92 | **0.25** (z 5.5, rec 0.76) | **0.25** (z 5.4, rec 0.69) | **0.20** (z 5.4, rec 0.78) | **0.40** (z 5.4, rec 0.80) | **0.28** |
| 120 | **0.50** (z 6.0, rec 0.75) | **0.55** (z 6.1, rec 0.69) | **0.50** (z 6.0, rec 0.78) | **0.55** (z 6.1, rec 0.79) | **0.53** |
| 160 | **0.85** (z 6.9, rec 0.76) | **0.85** (z 7.0, rec 0.73) | **0.65** (z 6.5, rec 0.75) | **0.75** (z 7.1, rec 0.70) | **0.78** |
| 200 | **0.90** (z 7.7, rec 0.68) | **0.85** (z 7.3, rec 0.73) | **0.85** (z 7.9, rec 0.70) | **0.95** (z 8.6, rec 0.73) | **0.89** |
| 240 | **0.95** (z 8.6, rec 0.71) | **1.00** (z 8.9, rec 0.74) | **0.95** (z 8.4, rec 0.72) | **0.95** (z 9.2, rec 0.73) | **0.96** |
| 277 | **1.00** (z 10.0, rec 0.75) | **1.00** (z 10.0, rec 0.73) | **1.00** (z 9.6, rec 0.73) | **1.00** (z 9.9, rec 0.74) | **1.00** |

## Lane A rank within family

| length | share of plants ranked first | median rank |
|---|---|---|
| 66 | 0.91 | 1 |
| 92 | 0.96 | 1 |
| 120 | 0.93 | 1 |
| 160 | 0.90 | 1 |
| 200 | 0.90 | 1 |
| 240 | 0.95 | 1 |
| 277 | 0.91 | 1 |

## Pages below the power threshold

- Lane A: the weakest family reaches 80 % power at 92 runes; 2 of 55 pages are shorter: LP2-49 (66), LP2-55 (76).
- Lane B: the weakest family reaches 80 % power at 200 runes; 9 of 55 pages are shorter: LP2-49 (66), LP2-55 (76), LP2-51 (92), LP2-32 (121), LP2-22 (131), LP2-14 (137), LP2-15 (159), LP2-53 (179), LP2-06 (196).

Pages below the threshold for a lane are **inconclusive** for that lane's exclusions, not negative: the correct key can be recovered there and still fail the pre-registered rule. The page-length distribution: 3 under 100, 6 under 150, 9 under 200, 20 under 240 runes of 55.

