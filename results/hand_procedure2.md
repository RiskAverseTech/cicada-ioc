# Hand procedures, second family (D1, instrument 1): value-built tables, marker rules, two-state procedures, the three behaviours

Registration: `results/hand_procedure_registration.md`. 56,952 procedures screened at 20 replicates; bands D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq, U, W2, WM; LP2 reference D 86, D_in 63, L3 179, L4 131, L5 102, L5S 11, BIG 9, L6T 77, SHARE 7.21, Sfreq 0.0335, U 26.4, W2 0.159, WM 4.42.

## Part A, the generator

Candidates (every band within |z| < 3.0): **1** of 56,952 (0.00 %); without fillers: 0. Survivors at 200 replicates: **0**.

Bands failed, over the family: D 52,165, L6T 51,333, D_in 50,365, L5S 46,163, U 45,401, W2 28,476, WM 28,476, Sfreq 28,026, BIG 25,483, SHARE 19,566, L5 17,813, L4 9,271, L3 4,841.

| reference row | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=0 | c1 | reset word | none | fill 0.00 | litF off | 349 (z -12.5) | 239 (z -10.8) | 146 (z +1.7) | 102 (z +2.0) | 55.6 (z +6.9) | 3.39 (z +3.7) | 3.23 (z +2.8) | 34.2 (z +5.5) | 1.9 (z +2.4) | 0.0412 (z -3.5) | 1.09e+03 (z -7.8) | 0.271 (z -11.0) | 4.06 (z +5.5) |
| add k=0 | c1 | reset word | exclude | fill 0.00 | litF off | 90.6 (z -0.4) | 0 (z +63000000000.0) | 144 (z +2.3) | 110 (z +1.9) | 70.4 (z +2.8) | 2.75 (z +3.1) | 2.4 (z +3.5) | 42 (z +3.3) | -0.875 (z +4.4) | 0.018 (z +10.7) | 1.16e+03 (z -11.2) | 0.271 (z -11.0) | 4.06 (z +5.5) |

| candidate | survivor | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=1 | c6w | reset none | none | fill 0.40 | litF off | behaviours copy/hold/spend | no | 81 (z +0.4) | 73.1 (z -0.8) | 164 (z +1.2) | 122 (z +0.6) | 127 (z -1.7) | 4.16 (z +3.3) | 6.32 (z +1.0) | 45.7 (z +4.4) | 1.84 (z +2.1) | 0.0341 (z -0.4) | 26.2 (z +0.0) | 0.165 (z -0.7) | 4.44 (z -0.3) |

Nearest misses (fewest bands failed, then smallest largest |z|):

| procedure | bands failed | largest \|z\| | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=1 | c6w | reset none | none | fill 0.40 | litF off | behaviours copy/hold/spend | 0 | 2.9 | +0.2 | -1.0 | +0.9 | +0.5 | -1.8 | +2.7 | +0.6 | +2.9 | +1.3 | -0.7 | +0.5 | -0.6 | -0.7 |
| sub k=28 | c1 | reset none | none | fill 0.40 | litF off | marker I:copy5 | 1 | 3.2 | +0.0 | -1.2 | +2.5 | +1.5 | -2.7 | +2.2 | +0.6 | +3.2 | +1.8 | -0.9 | -0.1 | -0.6 | -0.7 |
| sub k=25 | c6w | reset none | none | fill 0.40 | litF off | marker S:reset | 1 | 3.8 | +1.7 | +0.2 | +1.7 | +1.7 | -0.9 | +2.4 | +0.7 | +3.8 | +1.8 | -1.5 | -1.2 | -0.6 | -0.7 |
| sub k=28 | c6w | reset none | none | fill 0.40 | litF off | behaviours copy/spend/hold | 1 | 4.1 | +0.2 | -1.0 | +1.1 | +0.4 | -2.0 | +2.9 | +0.7 | +4.1 | +2.3 | -0.3 | -0.7 | -0.6 | -0.7 |
| sub k=28 | c6w | reset none | none | fill 0.40 | litF off | behaviours copy/hold/spend | 1 | 4.3 | +0.2 | -1.0 | +0.9 | +0.6 | -1.7 | +2.7 | +0.8 | +4.3 | +2.2 | -0.7 | +0.2 | -0.6 | -0.7 |
| sub k=25 | c6w | reset none | none | fill 0.40 | litF off | marker I:reset | 1 | 4.4 | +1.9 | +0.3 | +1.4 | +1.6 | -0.8 | +3.0 | +0.6 | +4.4 | +1.9 | -1.2 | -1.8 | -0.6 | -0.7 |
| add k=2 | c6w | reset none | none | fill 0.40 | litF off | marker S:reset | 1 | 4.6 | +0.6 | -1.5 | -2.4 | +2.3 | -0.7 | +2.2 | +0.8 | +4.6 | +1.7 | -0.8 | -1.3 | -0.6 | -0.7 |
| add k=2 | c1 | reset none | none | fill 0.40 | litF off | marker I:copy5 | 1 | 4.7 | +1.4 | -1.2 | -4.7 | +1.2 | -2.4 | +1.7 | +0.4 | +2.9 | +1.7 | -1.6 | -0.0 | -0.6 | -0.7 |
| sub k=28 | c6w | reset none | none | fill 0.40 | litF off | behaviours spend/hold/copy | 1 | 4.8 | +0.1 | -1.1 | +1.1 | +0.4 | -1.6 | +2.7 | +0.9 | +4.8 | +2.6 | -0.7 | -0.1 | -0.6 | -0.7 |
| tot-sub k=5 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 5.9 | -0.5 | -2.0 | +0.4 | +1.7 | -1.9 | +2.9 | +0.4 | +1.9 | +1.0 | -1.8 | -5.9 | -0.6 | -0.7 |
| val-add k=18 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 8.1 | +1.1 | -0.1 | +0.5 | +1.6 | -1.6 | +1.6 | +0.4 | +0.8 | +0.5 | +1.4 | -8.1 | -0.6 | -0.7 |
| tot-rev k=24 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 8.2 | +0.3 | -0.7 | +0.9 | +2.3 | -1.9 | +2.9 | +0.5 | +0.8 | +1.0 | -2.2 | -8.2 | -0.6 | -0.7 |

Procedures holding the deficit, both echoes, the S count and the bigram runs together (D, L5, L5S, L6T, BIG all within |z| < 3.0; H4′): **104**.

| procedure | bands failed | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=1 | c6w | reset none | none | fill 0.40 | litF off | behaviours copy/hold/spend | none | +0.2 | -1.0 | +0.9 | +0.5 | -1.8 | +2.7 | +0.6 | +2.9 | +1.3 | -0.7 | +0.5 | -0.6 | -0.7 |
| val-rev k=22 | c6w | reset none | exclude | fill 0.40 | litF on | U | -1.0 | -2.3 | +0.7 | +1.2 | -1.8 | +2.6 | +0.6 | +2.6 | +1.3 | +0.6 | -13.6 | -0.6 | -0.7 |
| tot-sub k=5 | c6w | reset none | exclude | fill 0.40 | litF on | U | -0.5 | -2.0 | +0.4 | +1.7 | -1.9 | +2.9 | +0.4 | +1.9 | +1.0 | -1.8 | -5.9 | -0.6 | -0.7 |
| val-add k=18 | c6w | reset none | exclude | fill 0.40 | litF on | U | +1.1 | -0.1 | +0.5 | +1.6 | -1.6 | +1.6 | +0.4 | +0.8 | +0.5 | +1.4 | -8.1 | -0.6 | -0.7 |
| val-add k=19 | c6w | reset none | exclude | fill 0.40 | litF on | U | -0.2 | -1.4 | +0.6 | +1.3 | -1.6 | +2.7 | +0.8 | +2.3 | +1.9 | -0.8 | -11.5 | -0.6 | -0.7 |
| val-mul k=23 | c6w | reset none | exclude | fill 0.40 | litF on | U | -0.8 | -1.8 | -0.1 | +0.8 | -2.8 | +2.0 | -0.1 | +1.7 | +1.2 | +1.2 | -14.4 | -0.6 | -0.7 |
| tot-sub k=0 | c6w | reset none | exclude | fill 0.40 | litF on | U | -1.5 | -2.1 | -0.6 | +1.3 | -2.2 | +2.4 | +0.7 | +1.9 | +1.5 | -0.9 | -11.3 | -0.6 | -0.7 |
| tot-sub k=7 | c6w | reset word | exclude | fill 0.40 | litF off | U | -3.0 | +2.8 | -0.6 | +0.7 | -2.9 | +0.5 | +0.2 | +3.0 | +2.3 | +1.6 | -17.1 | -0.6 | -0.7 |
| add k=2 | c1 | reset none | none | fill 0.40 | litF off | marker I:copy5 | L3 | +1.4 | -1.2 | -4.7 | +1.2 | -2.4 | +1.7 | +0.4 | +2.9 | +1.7 | -1.6 | -0.0 | -0.6 | -0.7 |
| tot-add k=19 | c6w | reset none | exclude | fill 0.40 | litF on | U | +1.3 | +0.0 | +0.4 | +1.2 | -2.4 | +2.5 | +0.4 | +1.0 | +0.4 | +0.8 | -9.0 | -0.6 | -0.7 |
| tot-rev k=24 | c6w | reset none | exclude | fill 0.40 | litF on | U | +0.3 | -0.7 | +0.9 | +2.3 | -1.9 | +2.9 | +0.5 | +0.8 | +1.0 | -2.2 | -8.2 | -0.6 | -0.7 |
| val-add k=18 | p1 | reset word | redraw | fill 0.40 | litF on | Sfreq, U | +0.4 | -0.0 | +0.1 | +1.5 | +1.3 | +1.9 | +2.3 | +2.9 | +2.6 | -6.4 | -16.4 | -0.6 | -0.7 |

## Part B, the decoder

Chance level (200 random procedures on uniform page sets): largest median page 5-gram z 0.97, largest single page 4.04.

28,476 procedures applied to the 55 pages. Largest median page z5 **1.15**; largest single page z5 5.49; largest model-free z\* 16.27. Hits (median ≥ 6 and a page ≥ 10): **0**.

| procedure | median page z5 | best page z5 | best page | z\* | text |
|---|---|---|---|---|---|
| near-mul k=21 | c6w | reset none | exclude | fill 0.00 | litF on | 1.15 | 3.54 | 24 | 7.74 | UGFIGETHXCIOAPUSWLTAFSANHTHPCOEFIDEPGOEFIXGUAEYUSYJUPNPNNGSH |
| near-mul k=21 | c5w | reset none | exclude | fill 0.00 | litF on | 1.05 | 3.70 | 24 | 9.85 | UGFIGETHXCIOAPUSWLTAFSANHTHPCOEFIDHWGOEFIXGUAEYUSYJUPNPNNGSH |
| near-mul k=22 | c5w | reset word | exclude | fill 0.00 | litF on | 1.04 | 2.52 | 28 | 7.81 | IXOEEONEIFUHUAUHLMEWPPDSPGHTHGJSHEOLNGPIGETWHSFAANLJAESMNIJX |
| near-mul k=8 | c5w | reset none | redraw | fill 0.00 | litF on | 1.01 | 2.46 | 20 | 9.34 | OCNOEAELRUTHEBWCRNGTHAWTWJMIANSEOEENGNAMIFXUHFOEFTHFDAPUDGNB |
| near-mul k=18 | c1 | reset none | exclude | fill 0.00 | litF off | 1.01 | 3.22 | 36 | 5.92 | CTHYHEOWGLEOJNGHXRCSNGOESOEARSOANRIGOERNGCBOUIAWEBNTHMBRIAEO |
| near-mul k=18 | c1 | reset none | exclude | fill 0.00 | litF on | 1.01 | 3.91 | 36 | 7.99 | CTHYHEOWGLEOJNGHXRCSFROESOEARSOANRIGOERNGCBOUIAWEBNTHMBRIAEO |
| val-mul k=1 | csum | reset word | none | fill 0.00 | litF on | 1.01 | 3.21 | 13 | 12.26 | GEOFJYNGJUWYUOEOETYOESTTNGBIFEOHNGFONTFYENUEAFEOYYNGCNGAEHNG |
| val-mul k=1 | csum | reset word | redraw | fill 0.00 | litF off | 0.98 | 3.00 | 6 | 7.67 | NGEOWPEAUNGGGEOCUSTHJHUFCPUFCUCEAEXICCNLAENGLXRCGOETHTGOEFNG |
| near-mul k=19 | csum | reset none | exclude | fill 0.00 | litF off | 0.97 | 2.47 | 52 | 5.70 | EOOEMSUGIBWRMTHPWYCTPXAEFFBCPPTTERFHEOMEATMRIAJEASUBPWOOENDY |
| near-mul k=24 | csum | reset none | redraw | fill 0.00 | litF off | 0.97 | 3.60 | 27 | 4.11 | GALNENGWEAHIGANEEACFRCUTHJYDFLTHOENGNGIANGJEAOEFTEOWONOTHBIH |
| val-add k=16 | c6w | reset none | redraw | fill 0.00 | litF on | 0.97 | 2.94 | 21 | 10.88 | YOENPYNGHYHADHEAFFXWGNGAHIAHOIAXHNJOEAEAHOESFUSWYPFNNCPTOEIA |
| tot-add k=17 | c6w | reset none | redraw | fill 0.00 | litF on | 0.97 | 2.94 | 21 | 10.88 | YOENPYNGHYHADHEAFFXWGNGAHIAHOIAXHNJOEAEAHOESFUSWYPFNNCPTOEIA |

## Registered predictions

- H1 (plain chain fails D): D 349 against 86 → holds.
- H2 (< 1 % candidates): 1 of 56,952 → holds.
- H3 (no candidate without fillers): 0 → holds.
- H4 (no survivor): 0 → holds.
- H5 (no decode hit; largest median within 1.0 of chance): 1.15 against chance 0.97 → holds.

Reading: README §74. Null in both parts. The one 20-replicate candidate (the three behaviours on the lag-6 cipher state with fillers) fails the lag-6 count and the S count at 200 replicates; the model-free z\* column is a decoder artefact for the many-to-one value tables (per-decoder chance on uniform pages in `results/hand_procedure2_zstar_chance.json`, `src/hp2_zstar_chance.py`: the decoders at z\* ≥ 10.5 on the pages score a median 10.6 and up to 16.5 on uniform pages). [stated — the tables]

Reproduce: `STAGE=chance|screen|confirm|decode|merge .venv/bin/python -I src/hand_procedure_lane.py`.
