# Word-aware mechanism lane: which rule reproduces the three structures together?

English plaintext (Emerson) in the 55 pages' rune counts, iid uniform key, q = 0.81, 200 replicates per rule; statistics, rules and the survival criterion are in the module docstring and were fixed before the run. LP2's own values: D 86, D_in 63, L3 179, L4 131, L5 102, L5S 11, L6T 77, L6best 77, SHARE 7.21, Sfreq 0.0335, U 26.4.

| rule | D | D_in | L3 | L4 | L5 | L5S | L6T | SHARE | Sfreq | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Rq0 | 446.0±20.9 (z -17.2) | 338.1±17.4 (z -15.8) | 157.2±13.4 (z +1.6) | 105.0±10.9 (z +2.4) | 67.8±8.2 (z +4.2) | 2.3±1.5 (z +5.7) | 43.3±7.2 (z +4.7) | 1.3±2.2 (z +2.7) | 0.0343 (z -0.5) | fails: D, D_in, L5, L5S, L6T |
| R0 | 84.2±8.7 (z +0.2) | 64.1±7.1 (z -0.2) | 156.5±12.9 (z +1.7) | 103.3±11.8 (z +2.4) | 67.9±8.6 (z +4.0) | 2.5±1.5 (z +5.5) | 42.6±7.0 (z +4.9) | 0.9±2.0 (z +3.2) | 0.0345 (z -0.7) | fails: L5, L5S, L6T, SHARE |
| R0h | 83.9±9.7 (z +0.2) | 63.3±8.9 (z -0.0) | 158.2±12.5 (z +1.7) | 103.9±10.5 (z +2.6) | 68.5±8.5 (z +3.9) | 2.5±1.9 (z +4.5) | 42.5±6.4 (z +5.4) | 1.0±2.1 (z +3.0) | 0.0345 (z -0.7) | fails: L5, L5S, L6T, SHARE |
| R4 | 84.9±9.3 (z +0.1) | 64.2±8.0 (z -0.1) | 156.6±12.8 (z +1.8) | 103.3±11.1 (z +2.5) | 67.6±8.1 (z +4.3) | 2.5±1.6 (z +5.3) | 74.0±9.7 (z +0.3) | 1.5±2.7 (z +2.1) | 0.0344 (z -0.6) | fails: L5, L5S |
| R4n | 76.1±8.4 (z +1.2) | 59.8±7.0 (z +0.5) | 171.8±13.0 (z +0.6) | 115.3±12.0 (z +1.3) | 76.2±8.9 (z +2.9) | 2.7±1.6 (z +5.2) | 82.7±9.6 (z -0.6) | 2.6±2.9 (z +1.6) | 0.0347 (z -0.7) | fails: L5S |
| Rc5 | 85.1±9.3 (z +0.1) | 64.9±7.9 (z -0.2) | 157.4±12.9 (z +1.7) | 103.1±11.5 (z +2.4) | 119.3±11.3 (z -1.5) | 4.0±1.9 (z +3.6) | 41.4±6.8 (z +5.2) | 1.7±2.6 (z +2.1) | 0.0345 (z -0.7) | fails: L5S, L6T |
| RS | 166.1±12.3 (z -6.5) | 122.0±10.7 (z -5.5) | 175.3±14.4 (z +0.3) | 123.9±12.7 (z +0.6) | 85.3±10.3 (z +1.6) | 33.1±6.4 (z -3.4) | 41.1±6.8 (z +5.2) | 1.1±2.3 (z +2.7) | 0.1042 (z -25.3) | fails: D, D_in, L5S, L6T, Sfreq |
| RF | 109.8±10.7 (z -2.2) | 82.5±8.5 (z -2.3) | 157.3±12.6 (z +1.7) | 105.9±11.8 (z +2.1) | 68.0±8.8 (z +3.9) | 2.4±1.6 (z +5.5) | 42.8±7.3 (z +4.7) | 0.9±2.2 (z +2.9) | 0.0335 (z -0.0) | fails: L5, L5S, L6T |

Cells are the rule's mean ± sd over replicates and the z of LP2's value against them. L6best (largest hit count over the 812 affine maps at lag 6) is reported in the JSON; LP2's is 77, equal to its L6T, so T is LP2's best map.

