# The S rate at within-word lag-5 cipher coincidences under English running keys

Plaintext: Emerson's essays in rune spelling, 17,726 words of more than 5 runes, 46,035 within-word lag-5 pairs. Each running key is read from 20 random offsets; counts are pooled. The rune at an equal cipher pair is S with probability 1/29 = 3.45 % when the key is uniform given its own lag-5 difference (iid uniform keys, periodic uniform keys); under an English running key the key repeats are English's repeated letters and the rate moves off 1/29 by the amount shown. The pages' own figure for comparison is 11 of 102 = 10.8 % (§45).

| key | sign | equal cipher pairs | of which S | S rate | z against 1/29 |
|---|---|---|---|---|---|
| kybalion as running key | sub | 33,292 | 2,073 | 6.23 % | +27.8 |
| kybalion as running key | add | 33,282 | 668 | 2.01 % | -14.4 |
| kybalion as running key | beaufort | 33,273 | 1,957 | 5.88 % | +24.3 |
| king_in_yellow as running key | sub | 32,894 | 2,036 | 6.19 % | +27.2 |
| king_in_yellow as running key | add | 33,244 | 593 | 1.78 % | -16.6 |
| king_in_yellow as running key | beaufort | 32,777 | 1,802 | 5.50 % | +20.3 |
| mabinogion_guest as running key | sub | 33,160 | 2,178 | 6.57 % | +31.1 |
| mabinogion_guest as running key | add | 33,186 | 579 | 1.74 % | -17.0 |
| mabinogion_guest as running key | beaufort | 33,125 | 1,992 | 6.01 % | +25.6 |
| iid uniform key (control) | add | 31,759 | 1,142 | 3.60 % | +1.4 |
| zero key (plaintext in clear) | — | 2,904 | 456 | 15.70 % | +36.2 |

Reading: the largest S rate under an English running key is 6.57 %, against 3.45 % for a uniform key and 10.8 % on the pages. The §47 theorem's condition is corrected to 'uniform given the key difference'; running keys from text are outside the theorem and are measured here instead, and they do not reach the pages' rate. [stated]

Runtime 2 s. Reproduce: `.venv/bin/python -I src/s_runkey_check.py`.
