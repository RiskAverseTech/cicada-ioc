# Exact reachability of the solved-page rule

Rule: c = p ± k, a ciphertext F is a literal F (no key consumed) or an encrypted rune, no encrypted rune decrypts to F. Streams reduced mod 29; offsets 0..19999; per page (fresh offset each page) and continuous (one offset for all 12,956 runes). A page survives an offset if any skip assignment keeps every encrypted rune off F.

| stream | sign | pages with ≥1 surviving offset (of 55) | total surviving (page, offset) pairs | continuous section: surviving offsets | plant: true offset found | plant: wrong offsets surviving |
|---|---|---|---|---|---|---|
| prime - 1 (phi) | + | 55 | 39633 | 0 | yes | 13102 |
| prime - 1 (phi) | − | 55 | 41350 | 0 | yes | 5022 |
| prime | + | 55 | 37189 | 0 | yes | 5257 |
| prime | − | 55 | 37280 | 0 | yes | 5703 |
| prime + 1 | + | 55 | 40789 | 0 | yes | 5082 |
| prime + 1 | − | 55 | 40594 | 0 | yes | 3331 |
| Fibonacci | + | 15 | 70002 | 0 | yes | 7144 |
| Fibonacci | − | 10 | 50001 | 0 | yes | 9999 |
| Lucas | + | 7 | 29998 | 0 | yes | 7141 |
| Lucas | − | 10 | 38572 | 0 | yes | 2857 |

Reading: a surviving offset is necessary, not sufficient, for the rule; a page with zero surviving offsets is excluded exactly for that stream and sign. The plant column shows how many wrong offsets survive by chance for a 300-rune page, i.e. the test's selectivity.

