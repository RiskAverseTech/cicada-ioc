# G. The echo gate as a property of the word

Registration: `results/clue_table_registration.md` (G). Words of six runes or more: 806 (91 carry a lag-5 equality site); of seven or more: 554 (72 carry a lag-6 affine site); pooled (either site, six or more): 145 of 806. Chi-square stratified by exact word length, summed; null 2000 permutations of the site labels within each length stratum; family-wise p from the largest statistic over the ten properties.

| property | lag-5 χ² | p | family-wise p | lag-6 χ² | p | family-wise p | pooled χ² | p | family-wise p |
|---|---|---|---|---|---|---|---|---|---|
| first rune a vowel | 4.6 | 0.959 | 1.000 | 3.7 | 0.978 | 1.000 | 4.7 | 0.950 | 1.000 |
| first rune at or above S | 9.7 | 0.325 | 1.000 | 3.8 | 0.878 | 1.000 | 7.6 | 0.536 | 1.000 |
| last rune a vowel | 14.3 | 0.147 | 0.960 | 4.8 | 0.864 | 1.000 | 12.2 | 0.253 | 0.996 |
| Gematria sum even | 4.9 | 0.944 | 1.000 | 5.2 | 0.896 | 1.000 | 4.2 | 0.979 | 1.000 |
| Gematria sum mod 3 | 12.6 | 0.868 | 0.995 | 20.5 | 0.197 | 0.311 | 18.8 | 0.448 | 0.654 |
| index sum mod 29 below 15 | 4.8 | 0.853 | 1.000 | 4.9 | 0.761 | 1.000 | 4.5 | 0.885 | 1.000 |
| word index even | 5.9 | 0.711 | 1.000 | 6.4 | 0.565 | 1.000 | 8.8 | 0.413 | 1.000 |
| starts / ends a line | 13.1 | 0.635 | 0.989 | 7.5 | 0.936 | 1.000 | 9.4 | 0.922 | 1.000 |
| crosses a line end | 18.6 | 0.032 | 0.663 | 6.5 | 0.706 | 1.000 | 13.4 | 0.188 | 0.978 |
| second half of the section | 13.7 | 0.159 | 0.980 | 14.2 | 0.087 | 0.878 | 11.8 | 0.284 | 0.997 |

Power (synthetic sites on the real words, per-length counts kept, the property "first rune at or above S" raising the odds of a site; 200 draws, 400 permutations each; share of draws with family-wise p < 0.05): odds ratio 2: **0.23**; odds ratio 3: **0.90**.

## Registered predictions

- G1 (no property at family-wise p < 0.05 for either echo or pooled): smallest family-wise p 0.311 → holds.
- G2 (power at odds ratio 3 at least 0.8): 0.90 → holds.

Runtime 37 s. Reproduce: `.venv/bin/python -I src/gate_property.py`.
