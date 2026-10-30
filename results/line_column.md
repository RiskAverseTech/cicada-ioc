# The line-first rune and the line-column coincidence profile

55 unsolved pages, 594 lines. Per in-line column: pooled IoC (× 29) over all pages and the within-page same-column coincidence count; z against 2,000 within-page shuffles that keep the line lengths. Registration: `results/line_column_registration.md`.

| column | runes | pooled IoC | z | within-page coincidences | z | without first lines: pooled z | within z |
|---|---|---|---|---|---|---|---|
| start 0 | 594 | 1.090 | +7.2 | 107 | +0.3 | +5.6 | +0.2 |
| start 1 | 594 | 1.028 | +2.4 | 118 | +1.4 | +2.4 | +1.1 |
| start 2 | 594 | 1.006 | +0.5 | 128 | +2.4 | +0.9 | +2.7 |
| start 3 | 593 | 0.986 | -1.1 | 98 | -0.6 | -0.9 | -0.2 |
| start 4 | 592 | 1.002 | +0.2 | 107 | +0.4 | +0.0 | +0.2 |
| start 5 | 591 | 1.001 | +0.1 | 97 | -0.6 | +0.1 | -0.1 |
| start 6 | 591 | 1.009 | +0.7 | 107 | +0.4 | +0.7 | +0.7 |
| start 7 | 590 | 1.002 | +0.1 | 102 | -0.0 | +0.3 | -0.4 |
| start 8 | 586 | 0.987 | -1.0 | 121 | +2.0 | -1.2 | +1.7 |
| start 9 | 585 | 0.999 | -0.1 | 108 | +0.7 | +0.1 | +0.7 |
| start 10 | 585 | 1.008 | +0.6 | 107 | +0.6 | +0.3 | -0.1 |
| start 11 | 585 | 1.007 | +0.6 | 105 | +0.3 | -0.2 | +0.0 |
| start 12 | 585 | 0.990 | -0.8 | 96 | -0.6 | -1.4 | -0.1 |
| start 13 | 584 | 1.018 | +1.3 | 116 | +1.5 | +0.9 | +1.2 |
| start 14 | 582 | 0.999 | -0.0 | 88 | -1.2 | -0.0 | -1.0 |
| start 15 | 582 | 1.006 | +0.4 | 94 | -0.6 | +0.9 | -0.7 |
| end 0 | 594 | 0.998 | -0.2 | 101 | -0.3 | -0.0 | -1.1 |
| end 1 | 594 | 1.003 | +0.3 | 85 | -1.9 | -0.2 | -1.7 |
| end 2 | 594 | 0.994 | -0.5 | 104 | +0.0 | -1.0 | -0.1 |
| end 3 | 593 | 1.035 | +2.8 | 102 | -0.1 | +2.1 | -0.2 |
| end 4 | 592 | 0.994 | -0.5 | 80 | -2.4 | -1.2 | -2.0 |
| end 5 | 591 | 0.995 | -0.4 | 87 | -1.6 | -0.3 | -1.3 |

## Claims

- R1 column 0 pooled z ≥ 4: **holds** (z +7.2).
- R2 columns 1–5, pooled and within page, no cell at 4 and at most one at 3: **holds** (largest |z| 2.4).
- R3 column 0 keeps z ≥ 4 without the first line of each page: **holds** (z +5.6).
- R4 the from-end columns 0–5 by the R2 rule: **holds** (largest |z| 2.8).

## Column 0 against the pages' rune distribution

χ² 78.7 on 28 df, p 1.1e-06. Over: EA 38 vs 21.1, P 33 vs 20.4, D 32 vs 20.1, H 27 vs 19.0, IA 29 vs 21.5, NG 27 vs 20.8. Under: T 14 vs 20.3, B 12 vs 20.4, N 12 vs 20.4, O 12 vs 21.0, I 9 vs 21.6, R 6 vs 19.4.

Column streams in transliteration (first 120 runes each):

- column 0: `SOPSAEIAEBOENGEOTAIAMLUPIDMJYSOEDPDECDTHCLYBOEWBPUOCXLMUFTHEMXEIWPRGEOPCPAXEAHDNGXWGOAXCXPUHMDEADTHEWOEDXPJYOEYAXFFTHOEY`
- column 1: `HNBPHXYXHMHOEIRGOEXANNGAYHTMLUIGFWEAUJNIABCDDHHDEAIAOEGGEATWJBJOAAEDDOUIAUOEXPAECCILITEEIMHNGPIACBPNPHOIRFTHRSXCAESTWMSI`
- column 2: `ETHNTXYDGLFDNGMBPAEOEOEIAEAEXFMUWNGTHHPHEXEOAEANGFCTHTWIABYXEACIOECLSBHEOXWEOIYEJJIAFPETIAIAEAXTIAOEDPLUTLOEAYAEAEOEXYNG`

Reading: the effect is at column 0 only (z +7.2 pooled), shared across pages, absent from columns 1–15 (largest +2.4) and from the line ends, and it survives the removal of the 55 page-initial runes (z +5.6). That is reading (iii) of the registration, a line-initial effect, and it excludes a key that restarts at each line with one sequence on every page (which would raise every column) and, as the sole account, a page-specific per-line restart (which would leave the pooled statistic flat). The within-page statistic has about 3,000 pairs against the pooled 173,000 and does not separate the readings on its own. The six under-represented runes (R, I, O, N, B, T) are the simplest glyphs, a single stem with one or two branches, and the over-represented six (EA, P, D, H, IA, NG) are among the widest; whether that is a transcription effect on enlarged line-initial glyphs or the designer's own choice is for the page images. [stated — the table; the glyph remark inferred]

Runtime 29 s. Reproduce: `.venv/bin/python -I src/line_column.py`.
