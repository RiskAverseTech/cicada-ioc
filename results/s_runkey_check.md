# The S rate at within-word lag-5 cipher coincidences under English running keys

Plaintext: Emerson's essays in rune spelling, 17,940 words of more than 5 runes, 46,991 within-word lag-5 pairs. Each running key is read from 20 random offsets; counts are pooled. The rune at an equal cipher pair is S with probability 1/29 = 3.45 % when the key is uniform given its own lag-5 difference (iid uniform keys, periodic uniform keys); under an English running key the key repeats are English's repeated letters and the rate moves off 1/29 by the amount shown. The pages' own figure for comparison is 11 of 102 = 10.8 % (§45).

| key | sign | equal cipher pairs | of which S | S rate | z against 1/29 |
|---|---|---|---|---|---|
| kybalion as running key | sub | 34,028 | 2,057 | 6.05 % | +26.3 |
| kybalion as running key | add | 33,678 | 654 | 1.94 % | -15.2 |
| kybalion as running key | beaufort | 33,867 | 2,064 | 6.09 % | +26.7 |
| king_in_yellow as running key | sub | 33,615 | 2,172 | 6.46 % | +30.3 |
| king_in_yellow as running key | add | 33,620 | 626 | 1.86 % | -15.9 |
| king_in_yellow as running key | beaufort | 33,922 | 1,953 | 5.76 % | +23.3 |
| mabinogion_guest as running key | sub | 33,741 | 2,299 | 6.81 % | +33.9 |
| mabinogion_guest as running key | add | 33,462 | 613 | 1.83 % | -16.2 |
| mabinogion_guest as running key | beaufort | 33,934 | 2,000 | 5.89 % | +24.7 |
| iid uniform key (control) | add | 32,090 | 1,093 | 3.41 % | -0.4 |
| zero key (plaintext in clear) | — | 2,968 | 457 | 15.40 % | +35.7 |

Reading: the largest S rate under an English running key is 6.81 %, against 3.45 % for a uniform key and 10.8 % on the pages. The §47 theorem's condition is corrected to 'uniform given the key difference'; running keys from text are outside the theorem and are measured here instead, and they do not reach the pages' rate. [stated]

Runtime 7 s. Reproduce: `.venv/bin/python -I src/s_runkey_check.py`.
