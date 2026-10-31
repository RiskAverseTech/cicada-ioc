# One hand procedure as the cipher: the generator search of blind spot 4 (row A5)

Registration: `results/hand_procedure_registration.md`. 24,840 procedures screened at 20 replicates; bands D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq, U, W2, WM; LP2 reference D 86, D_in 63, L3 179, L4 131, L5 102, L5S 11, BIG 9, L6T 77, SHARE 7.21, Sfreq 0.0335, U 26.4, W2 0.159, WM 4.42.

## Part A, the generator

Candidates (every band within |z| < 3.0): **0** of 24,840 (0.00 %); without fillers: 0. Survivors at 200 replicates: **0**.

Bands failed, over the family: L6T 22,612, D 22,191, L5S 21,360, D_in 21,319, U 21,172, BIG 15,353, W2 12,420, WM 12,420, L5 11,688, SHARE 10,324, Sfreq 9,489, L4 2,477, L3 1,595.

| reference row | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=0 | c1 | reset word | none | fill 0.00 | litF off | 349 (z -12.5) | 239 (z -10.8) | 146 (z +1.7) | 102 (z +2.0) | 55.6 (z +6.9) | 3.39 (z +3.7) | 3.23 (z +2.8) | 34.2 (z +5.5) | 1.9 (z +2.4) | 0.0412 (z -3.5) | 1.09e+03 (z -7.8) | 0.271 (z -11.0) | 4.06 (z +5.5) |
| add k=0 | c1 | reset word | exclude | fill 0.00 | litF off | 90.6 (z -0.4) | 0 (z +63000000000.0) | 144 (z +2.3) | 110 (z +1.9) | 70.4 (z +2.8) | 2.75 (z +3.1) | 2.4 (z +3.5) | 42 (z +3.3) | -0.875 (z +4.4) | 0.018 (z +10.7) | 1.16e+03 (z -11.2) | 0.271 (z -11.0) | 4.06 (z +5.5) |

Nearest misses (fewest bands failed, then smallest largest |z|):

| procedure | bands failed | largest \|z\| | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add k=15 | c6w | reset none | none | fill 0.40 | litF off | 1 | 3.5 | +2.2 | -0.4 | +1.3 | +2.3 | -0.3 | +3.0 | +1.2 | +3.5 | +1.9 | -0.8 | -0.1 | -0.6 | -0.7 |
| sub k=12 | c6w | reset none | none | fill 0.40 | litF on | 1 | 4.1 | -0.7 | -1.7 | +2.9 | +2.1 | -0.6 | +2.9 | +0.8 | +2.9 | +1.9 | -1.2 | -4.1 | -0.6 | -0.7 |
| rev k=26 | c6w | reset none | exclude | fill 0.40 | litF off | 1 | 4.5 | +4.5 | +2.0 | +0.3 | +1.1 | -0.7 | +2.6 | +0.9 | +2.9 | +2.5 | -0.4 | -2.5 | -0.6 | -0.7 |
| sub k=28 | c6w | reset none | redraw | fill 0.40 | litF off | 1 | 5.1 | +0.1 | -1.1 | +0.9 | +0.5 | -1.2 | +2.7 | +0.8 | +5.1 | +1.9 | -0.9 | -0.1 | -0.6 | -0.7 |
| mul a=2 k=1 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 6.3 | -0.4 | -1.0 | +0.6 | +2.1 | -0.7 | +2.6 | +1.0 | +2.7 | +2.2 | -0.1 | -6.3 | -0.6 | -0.7 |
| mul a=2 k=13 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 6.7 | +1.4 | -0.1 | +0.3 | +1.6 | -0.8 | +1.9 | +1.4 | +2.1 | +2.6 | -2.9 | -6.7 | -0.6 | -0.7 |
| sub k=28 | c6w | reset word | redraw | fill 0.40 | litF on | 1 | 8.6 | -0.5 | -1.8 | +0.7 | +0.5 | -1.0 | +2.6 | +1.2 | +2.5 | +1.2 | -1.3 | -8.6 | -0.6 | -0.7 |
| mul a=-3 k=19 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 8.6 | -0.8 | -2.1 | +0.3 | +1.2 | -0.6 | +2.4 | +1.1 | +3.0 | +2.5 | -2.6 | -8.6 | -0.6 | -0.7 |
| mul a=-2 k=6 | c6w | reset none | exclude | fill 0.40 | litF on | 1 | 8.8 | +0.2 | -0.8 | +0.5 | +1.4 | -0.9 | +2.8 | +1.4 | -1.3 | -0.2 | -1.4 | -8.8 | -0.6 | -0.7 |
| sub k=28 | c6w | reset word | redraw | fill 0.40 | litF off | 1 | 9.2 | +0.9 | -1.1 | +1.3 | +0.4 | -1.1 | +2.5 | +0.9 | +2.6 | +1.2 | -1.0 | -9.2 | -0.6 | -0.7 |
| mul a=3 k=1 | c6w | reset word | exclude | fill 0.40 | litF off | 1 | 10.5 | -2.2 | +2.7 | +0.7 | +2.8 | -0.3 | +0.3 | +0.9 | +1.3 | +1.0 | -0.7 | -10.5 | -0.6 | -0.7 |
| rev k=21 | csum | reset word | redraw | fill 0.40 | litF off | 1 | 10.8 | -0.3 | -2.2 | +0.2 | -0.1 | +2.4 | +2.2 | +3.0 | +2.2 | +2.2 | -1.6 | -10.8 | -0.6 | -0.7 |

## Part B, the decoder

Chance level (200 random procedures on uniform page sets): largest median page 5-gram z 0.58, largest single page 4.19.

12,420 procedures applied to the 55 pages. Largest median page z5 **0.83**; largest single page z5 5.46; largest model-free z\* 13.12. Hits (median ≥ 6 and a page ≥ 10): **0**.

| procedure | median page z5 | best page z5 | best page | z\* | text |
|---|---|---|---|---|---|
| add k=4 | c6w | reset word | none | fill 0.00 | litF on | 0.83 | 2.71 | 53 | 5.05 | LSIAIAFFHTDDNGSRCTHOENGEOROEBGNGCREGLNGPHGOESTIXIEOTNGFOEFJL |
| add k=4 | c1 | reset word | none | fill 0.00 | litF on | 0.81 | 2.98 | 9 | 4.90 | OEGXGUBDUHTHLTHRNIBAUAGINBFNSIAHCEATJDYNREJFMHOEWEEOLUEOBOWR |
| add k=4 | c5w | reset none | redraw | fill 0.00 | litF on | 0.80 | 2.72 | 8 | 4.97 | INGFUWNUJOEHXDGWOHJATETHIAMTIAEACBWTXTHEORFGMUXICEOENRSNCLDL |
| add k=4 | c6w | reset word | redraw | fill 0.00 | litF on | 0.79 | 2.75 | 53 | 5.05 | LSIAIAFFHTDDNGSRCTHOENGEOROEBGNGCREGLNGPHGOESTIXIEOTNGFOEFJL |
| add k=4 | c5w | reset word | none | fill 0.00 | litF off | 0.78 | 2.64 | 41 | 3.70 | AWIJWEFEAAEPTHPHEATHOFUSOEFIAIADWNGELTHWMEEABABFIABRJEIAEEAE |
| add k=4 | c5w | reset word | redraw | fill 0.00 | litF off | 0.76 | 2.52 | 41 | 3.79 | AWIJWEFEAAEPTHPHEATHOFUSOEFIAIADWNGELTHWMEEABABFIABRJEIAEEAE |
| add k=4 | c1 | reset word | redraw | fill 0.00 | litF on | 0.76 | 2.98 | 9 | 4.97 | OEGXGUBDUHTHLTHRNIBAUAGINBFNSIAHCEATJDYNREJFMHOEWEEOLUEOBOWR |
| add k=4 | c5w | reset none | none | fill 0.00 | litF on | 0.76 | 2.81 | 8 | 5.11 | INGFUWNUJOEHXDGWOHJATETHIAMTIAEACBWTXTHEORFGMUXICEOENRSNCLDL |
| add k=4 | c6w | reset none | redraw | fill 0.00 | litF off | 0.75 | 2.49 | 41 | 4.03 | AWITWEFEAXIATHPHCTHOFISOEHIAIADUNGELTHWWEEABAWFXABRJMIAEEAEU |
| sub k=11 | c6w | reset none | redraw | fill 0.00 | litF off | 0.73 | 3.08 | 6 | 4.03 | YLFMAEOENHFXIANDSEIUOLEAHDDPRTYDSASHRNGEOTHNUOYNGXENGYRUEOEA |
| add k=4 | c6w | reset none | none | fill 0.00 | litF off | 0.73 | 2.37 | 41 | 4.08 | AWITWEFEAXIATHPHCTHOFISOEHIAIADUNGELTHWWEEABAWFXABRJMIAEEAEU |
| sub k=11 | c6w | reset none | none | fill 0.00 | litF off | 0.72 | 3.12 | 6 | 4.08 | YLFMAEOENHFXIANDSEIUOLEAHDDPRTYDSASHRNGEOTHNUOYNGXENGYRUEOEA |

## Registered predictions

- H1 (plain chain fails D): D 349 against 86 → holds.
- H2 (< 1 % candidates): 0 of 24,840 → holds.
- H3 (no candidate without fillers): 0 → holds.
- H4 (no survivor): 0 → holds.
- H5 (no decode hit; largest median within 1.0 of chance): 0.83 against chance 0.58 → holds.

Reading: README §73. Null in both parts; the near family and the two routes to the deficit inside the family are described there. The results file's best page per decoder is the best 5-gram page; the best z\* page of the top model-free row was located post hoc (LP2-43, 37 ᚠ in 274 runes, no word). [stated — the tables]

Reproduce: `STAGE=chance|screen|confirm|decode|merge .venv/bin/python -I src/hand_procedure_lane.py`.
