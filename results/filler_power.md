# Decoder power when a tenth of the runes are fillers (§55 part B)

Plants: English (Emerson) under the soft rule q = 0.81 with a filler after each emitted rune w.p. 0.1 (uniform over the 28 runes other than the previous cipher rune), and the same plaintext and key without fillers (r = 0). 12 plants per cell, signs and F variants cycled. Statistic: z of the true key over 400 random keystreams through the same decoder, rank among the family (vigenere words both directions: 538 keys; prime streams of three families: 303; running key: the 4096 neighbouring offsets of the text). **Recovered = z >= 6 and rank 1.**

| n | family | r | plain: power / median z | free-null -0.8: power / median z | free-null -2.2: power / median z |
|---|---|---|---|---|---|
| 100 | vigenere-word | 0.00 | 0.92 / 6.9 | 0.92 / 8.1 | 1.00 / 9.8 |
| 100 | vigenere-word | 0.10 | 0.00 / 2.4 | 0.75 / 6.8 | 0.83 / 7.0 |
| 100 | primes | 0.00 | 0.92 / 6.9 | 0.75 / 8.7 | 0.92 / 10.3 |
| 100 | primes | 0.10 | 0.00 / 1.5 | 0.75 / 6.7 | 0.58 / 6.8 |
| 100 | running key | 0.00 | 0.92 / 6.9 | 0.83 / 8.2 | 0.83 / 9.7 |
| 100 | running key | 0.10 | 0.00 / 1.3 | 0.25 / 6.2 | 0.25 / 5.8 |
| 160 | vigenere-word | 0.00 | 1.00 / 9.1 | 1.00 / 11.0 | 1.00 / 13.0 |
| 160 | vigenere-word | 0.10 | 0.00 / 2.9 | 1.00 / 9.0 | 1.00 / 8.9 |
| 160 | primes | 0.00 | 1.00 / 9.1 | 0.83 / 11.0 | 1.00 / 13.5 |
| 160 | primes | 0.10 | 0.00 / 1.0 | 0.75 / 9.4 | 0.83 / 9.9 |
| 160 | running key | 0.00 | 0.92 / 9.2 | 0.75 / 10.8 | 0.92 / 13.3 |
| 160 | running key | 0.10 | 0.00 / 1.5 | 0.50 / 8.3 | 0.58 / 8.1 |
| 230 | vigenere-word | 0.00 | 1.00 / 11.9 | 1.00 / 14.6 | 1.00 / 16.9 |
| 230 | vigenere-word | 0.10 | 0.00 / 3.3 | 1.00 / 11.5 | 1.00 / 12.0 |
| 230 | primes | 0.00 | 1.00 / 11.5 | 0.75 / 13.1 | 0.92 / 16.0 |
| 230 | primes | 0.10 | 0.08 / 0.7 | 0.67 / 10.5 | 0.75 / 10.7 |
| 230 | running key | 0.00 | 0.92 / 11.8 | 0.83 / 13.9 | 0.92 / 16.6 |
| 230 | running key | 0.10 | 0.00 / 1.4 | 0.75 / 11.1 | 0.75 / 11.7 |

## Decisions (rules fixed in the registration)

- Running-key plants with fillers recovered: 18 under prior −0.8, 19 under prior −2.2 (of 36). **Prior for part C: -2.2.**
- Power at n = 230, running key, r = 0.1, under that prior: **0.75** (12 plants). Threshold 0.50 → **part C runs.**
- Free-null minus plain score for the true key (median nats): +86 with fillers, +0 without; §22's candidate rule asks for +20.

Columns read: power is the recovered fraction, median z the true key's typical z. The plain decoder's power under fillers is the power the plain-decoder lanes (§25, §40, §53 and the plain tiers of §54) had in a filler world; the free-null columns are what the sweep of part C has. [stated]
