# A model-free structure scorer over the small libraries (row A1, blind spot 1)

Registration: `results/nonprose_registration.md`. Scorer z\* = max of the z of U (Σ counts²), W (repeated words of ≥ 2 runes) and G (repeated rune 3-grams) against N0 = 2,000 uniform keystreams; plain decoder, three signs, F rule off and on; library rows per sign [46019] (book keys at every roll of their period ≤ 64, plus 3,000 prime streams).

## Calibration null (200,000 draws per cell, before any library row was read)

| page | runes | F | max z\* | ≥ 4 | ≥ 5 | ≥ 6 | ≥ 7 | per-statistic max (U, W, G; 20,000 draws) |
|---|---|---|---|---|---|---|---|---|
| LP2-29 | 277 | off | 5.74 | 151 | 26 | 0 | 0 | 5.9, 2.3, 3.0 |
| LP2-29 | 277 | on | 6.40 | 163 | 19 | 4 | 0 | 6.6, 2.3, 3.3 |
| LP2-49 | 66 | off | 7.22 | 235 | 37 | 11 | 2 | 5.5, 1.1, 2.3 |
| LP2-49 | 66 | on | 9.19 | 196 | 32 | 9 | 2 | 5.7, 1.1, 2.8 |

**Bar** = max(7.0, calibration max + 1.0) rounded up to 0.5 = **10.5**.

## Plants (power)

| class | sign | F | recovered (z\* ≥ 10.5, rank 1) | median z\* | median rank |
|---|---|---|---|---|---|
| P0 | sub | off | 0.00 | 0.4 | 22444 |
| P0 | add | off | 0.00 | 0.4 | 18596 |
| P0 | beaufort | off | 0.00 | 1.0 | 11622 |
| P1 | sub | off | 0.90 | 30.4 | 1 |
| P1 | sub | on | 0.20 | 16.1 | 2 |
| P1 | add | off | 1.00 | 27.0 | 1 |
| P1 | add | on | 0.10 | 10.6 | 3 |
| P1 | beaufort | off | 1.00 | 23.9 | 1 |
| P1 | beaufort | on | 0.30 | 12.3 | 3 |
| P2 | sub | off | 1.00 | 30.3 | 1 |
| P2 | add | off | 1.00 | 33.3 | 1 |
| P2 | beaufort | off | 1.00 | 34.4 | 1 |
| P3 | sub | off | 1.00 | 58.7 | 1 |
| P3 | add | off | 1.00 | 62.3 | 1 |
| P3 | beaufort | off | 1.00 | 58.9 | 1 |
| P4 | sub | off | 1.00 | 130.7 | 1 |
| P4 | add | off | 0.90 | 116.6 | 1 |
| P4 | beaufort | off | 1.00 | 126.6 | 1 |
| P5 | sub | off | 1.00 | 708.4 | 1 |
| P5 | add | off | 1.00 | 599.8 | 1 |
| P5 | beaufort | off | 1.00 | 669.1 | 1 |

## Positive controls (solved pages under their own keys, F rule on, sub library)

| page | chunk | runes | key | z\* (U, W, G) | rank | hit |
|---|---|---|---|---|---|---|

## The 55 pages

330 cells (page × F × sign). **Hits: 0.** Listed (library top above the library-sized null's max): 143 of 330.

| threshold | library rows ≥ (all cells) | library-sized null draws ≥ (same count of draws) |
|---|---|---|
| z\* ≥ 4 | 17,410 | 15,330 |
| z\* ≥ 5 | 2,564 | 2,097 |
| z\* ≥ 6 | 315 | 285 |
| z\* ≥ 7 | 37 | 51 |

Top cells by z\*:

| page | F | sign | top row | z\* (U, W, G) | null max | repeated words | repeated 3-grams |
|---|---|---|---|---|---|---|---|
| LP2-40 | on | sub | phrase-3-rev TO DESTROY ALL ʳ @6 | 8.64 (8.6, -0.1, 1.7) | 5.42 | — | FTHF×2 DRA×2 EOIATH×2 THSF×2 |
| LP2-40 | on | beaufort | phrase-3-rev TO DESTROY ALL ʳ @6 | 8.64 (8.6, -0.1, 1.7) | 5.42 | — | FIAF×2 GAEC×2 BTHIA×2 IAXF×2 |
| LP2-27 | on | sub | sentence WE PRESERVE THINGS BECAUSE WE BELIEVE WE ARE WEAK @2 | 8.48 (8.5, -0.2, 1.1) | 6.62 | — | EAFT×2 OBC×2 CMR×2 |
| LP2-27 | on | beaufort | sentence WE PRESERVE THINGS BECAUSE WE BELIEVE WE ARE WEAK @2 | 8.48 (8.5, -0.2, 1.1) | 6.62 | — | UFP×2 YEOA×2 AIAE×2 |
| LP2-05 | on | add | phrase-3 ONLY WHAT YOU @2 | 8.41 (8.4, -0.0, -0.4) | 6.22 | — | THBF×2 |
| LP2-38 | off | sub | phrase-2-rev ENOUGH LATER ʳ @9 | 8.07 (8.1, -0.0, -1.1) | 5.88 | — | — |
| LP2-38 | off | beaufort | phrase-2-rev ENOUGH LATER ʳ @9 | 8.07 (8.1, -0.0, -1.1) | 5.88 | — | — |
| LP2-22 | on | sub | phrase-4 PILGRIMAGE THAT WE SHAPE @12 | 7.72 (7.7, -0.0, 0.6) | 6.16 | — | WFAE×2 |
| LP2-22 | on | beaufort | phrase-4 PILGRIMAGE THAT WE SHAPE @12 | 7.72 (7.7, -0.0, 0.6) | 6.16 | — | OEFR×2 |
| LP2-55 | on | sub | phrase-2 THE KNOWLEDGE @7 | 7.61 (7.6, -0.0, 1.7) | 7.22 | — | HNGB×2 FCEO×2 |
| LP2-55 | on | beaufort | phrase-2 THE KNOWLEDGE @7 | 7.61 (7.6, -0.0, 1.7) | 7.22 | — | NGHEO×2 FAB×2 |
| LP2-43 | on | sub | phrase-2 OBTAIN WHAT @5 | 7.42 (7.4, -0.3, 1.9) | 6.39 | — | IAFOE×2 UMF×2 GSF×2 FFEA×2 FEOI×2 TOEA×2 GFF×2 |
| LP2-43 | on | beaufort | phrase-2 OBTAIN WHAT @5 | 7.42 (7.4, -0.3, 1.9) | 6.39 | — | THFW×2 EAIF×2 DXF×2 FFU×2 FBM×2 DFF×2 |
| LP2-16 | on | add | phrase-3-rev THE STUDENT AND ʳ @8 | 7.41 (7.4, -0.1, 0.9) | 6.12 | — | JJJ×2 FIU×2 SCEA×2 NEAE×2 |
| LP2-29 | on | sub | phrase-3 AND REPLIED I @6 | 7.35 (7.4, 1.7, -0.5) | 6.26 | EAH×2 UP×2 | THFF×2 |

## Registered predictions

- N1 (power): recovered at F off P0 0.00, P1 0.97, P2 1.00, P3 1.00, P4 0.97, P5 1.00 → holds.
- N2 (solved pages): 0 of 0 control pages are hits at rank 1 → fails.
- N3 (the pages): hits 0; listed cells 143 of 330 (all-null expectation 165 ± 9) → holds.
- N4 (tail): rows at z\* ≥ 5, library 2,564 against null 2,097 (ratio 1.22) → holds.

## The book's ᚠ convention (amendments 2 and 3): the key-lag dynamic programme, no language model

The WELCOME page under DIVINITY (sub library): chunk 2, where the key starts with the page, and chunk 3, where it continues from chunk 2 (so roll 0 is not expected there).

| chunk | runes | cipher ᚠ | z\* roll 0 | rank roll 0 | best roll | z\* | rank | rune accuracy | library top | z\* |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 251 | 14 | 12.9 | 13 | vigenere-word DIUINITY @0 | 12.9 | 13 | 1.00 | self running key plaintext@184 @0 | 110.7 |
| 3 | 264 | 11 | 4.2 | 768 | vigenere-word DIUINITY @4 | 17.8 | 6 | 1.00 | self running key plaintext@435 @0 | 143.7 |

| class | sign | recovered | median z\* | median rank | median rune accuracy |
|---|---|---|---|---|---|
| P1 | sub | 0.30 | 16.2 | 2 (0.50 at family rank 1; 0.70 recovered up to a constant shift) | 1.00 |
| P1 | add | 0.20 | 11.2 | 4 (0.30 at family rank 1; 0.30 recovered up to a constant shift) | 0.99 |
| P1 | beaufort | 0.10 | 9.8 | 3 (0.40 at family rank 1; 0.30 recovered up to a constant shift) | 0.99 |
| P4 | sub | 0.50 | 56.2 | 2 (0.50 at family rank 1; 0.60 recovered up to a constant shift) | 1.00 |
| P4 | add | 0.20 | 38.0 | 3 (0.20 at family rank 1; 0.30 recovered up to a constant shift) | 0.99 |
| P4 | beaufort | 0.40 | 52.1 | 2 (0.40 at family rank 1; 0.60 recovered up to a constant shift) | 1.00 |

The 55 pages, 165 cells (page × sign). **Hits: 0.** Listed: 69 of 165. Rows at z\* ≥ 5: library 1,519, null 1,209; at ≥ 6: 218 and 177; at ≥ 7: 27 and 42.

| page | sign | top row | z\* (U, W, G) | null max | repeated words | repeated 3-grams |
|---|---|---|---|---|---|---|
| LP2-40 | sub | phrase-3-rev TO DESTROY ALL ʳ @5 | 9.11 (9.1, -0.1, 2.0) | 7.40 | — | BFOE×2 FTHF×2 DRA×2 EOIATH×2 THSF×2 |
| LP2-40 | beaufort | phrase-3-rev TO DESTROY ALL ʳ @5 | 9.11 (9.1, -0.1, 2.0) | 7.40 | — | EOFW×2 FIAF×2 GAEC×2 BTHIA×2 IAXF×2 |
| LP2-38 | add | phrase-4 MAN THOUGHT FOR A @12 | 8.27 (8.3, -0.0, -0.1) | 8.21 | — | UAEEO×2 |
| LP2-41 | add | phrase-4 WHAT YOU ARE CALLED @14 | 7.94 (7.9, -0.0, 1.1) | 6.03 | — | THFEA×2 OIF×2 MSS×2 FUF×2 |
| LP2-27 | sub | sentence WE PRESERVE THINGS BECAUSE WE BELIEVE WE ARE WEAK @2 | 7.77 (7.8, -0.1, 0.9) | 5.66 | — | EAFT×2 OBC×2 CMR×2 |
| LP2-27 | beaufort | sentence WE PRESERVE THINGS BECAUSE WE BELIEVE WE ARE WEAK @2 | 7.77 (7.8, -0.1, 0.9) | 5.66 | — | UFP×2 YEOA×2 AIAE×2 |
| LP2-13 | sub | phrase-2-rev THOSE WHO ʳ @5 | 7.64 (7.6, -0.1, 0.6) | 6.62 | — | FFA×2 OELB×2 FAI×2 |
| LP2-13 | beaufort | phrase-2-rev THOSE WHO ʳ @5 | 7.64 (7.6, -0.1, 0.6) | 6.62 | — | FFC×2 WNEO×2 FCM×2 |
| LP2-18 | add | phrase-3-rev RIGHT ABOUT TO ʳ @2 | 7.58 (7.6, -0.1, 0.8) | 5.42 | — | EOFF×2 FYF×2 AMF×2 |
| LP2-19 | add | phrase-2 EVERY PILGRIM @2 | 7.41 (7.4, -0.2, -0.7) | 6.04 | — | FLF×2 |

- N1′ (power under the book's convention): P1 0.20, P4 0.37 → fails.
- N2′ (WELCOME chunk 2 at roll 0): z\* 12.9, rank 13 → fails.
- N3′ (the pages): hits 0; listed 69 of 165 → holds.

Reading: README §72. The two plain conventions and the book's own are all null on the 55 pages; the registered rank clauses N1′ and N2′ fail on the key's equivalence class (constant shifts and, under the book's convention, start-shift neighbours), while every control and plant decodes at rune accuracy ≥ 0.95 but one. [stated — the tables]

Reproduce: `STAGE=calib|plants|controls|pages|merge .venv/bin/python -I src/nonprose_lane.py`.
