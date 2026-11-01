# Word-level and two-state autokeys: generators against the bands, decoders of the pages

Registration: `results/autokey_registration.md`. 1,464 procedures screened at 20 replicates; bands D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq, U, W2, WM; LP2 reference D 86, D_in 63, L3 179, L4 131, L5 102, L5S 11, BIG 9, L6T 77, SHARE 7.21, Sfreq 0.0335, U 26.4, W2 0.159, WM 4.42.

## Part A, the generator

S-admissible members (L5S, L5, D, U, Sfreq all within |z| < 3.0) at the screen: **0** of 1,464; at 200 replicates: **0**.
Candidates (every band within |z| < 3.0): **0**; survivors at 200: **0**.

Bands failed, over the family: D_in 1,452, D 1,424, L6T 1,408, U 1,139, L5S 1,049, BIG 838, Sfreq 763, W2 732, WM 732, L5 653, SHARE 582, L3 219, L4 174.

Positive control (L plain d=1 cont sub | fill 0.00 | none | litF off, 200 replicates): D 587 (z -17.6), D_in 463 (z -17.2), L3 164 (z +0.9), L4 131 (z -0.0), L5 64.4 (z +4.8), L5S 3.97 (z +3.2), BIG 3.08 (z +3.1), L6T 43.9 (z +4.6), SHARE 2.5 (z +2.1), Sfreq 0.0415 (z -3.9), U 1.6e+03 (z -13.6), W2 0.271 (z -11.2), WM 4.06 (z +5.4).

| confirmed row | survivor | S-admissible | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L plain d=1 cont sub | fill 0.00 | none | litF off | no | no | 587 (z -17.6) | 463 (z -17.2) | 164 (z +0.9) | 131 (z -0.0) | 64.4 (z +4.8) | 3.97 (z +3.2) | 3.08 (z +3.1) | 43.9 (z +4.6) | 2.5 (z +2.1) | 0.0415 (z -3.9) | 1.6e+03 (z -13.6) | 0.271 (z -11.2) | 4.06 (z +5.4) |

Nearest to the S cell (smallest |z| on L5S, with the four companion cells):

| procedure | bands failed | L5S z | L5 z | D z | U z | Sfreq z | L6T z |
|---|---|---|---|---|---|---|---|
| W plain pad sub | fill 0.40 | none | litF on | 6 | -0.0 | +2.2 | -17.2 | -17.1 | -13.5 | +5.0 |
| W plain pad beaufort | fill 0.00 | redraw | litF on | 8 | +0.0 | +2.6 | +3.3 | -18.1 | -12.6 | +8.1 |
| G plain len beaufort | fill 0.00 | redraw | litF on | 7 | -0.0 | -1.2 | +8.6 | -12.0 | -5.7 | +6.1 |
| G cipher len beaufort | fill 0.00 | redraw | litF on | 7 | -0.0 | -1.2 | +8.6 | -12.0 | -5.7 | +6.1 |
| L cipher d=6 reset sub | fill 0.40 | redraw | litF off | 7 | +0.1 | +2.0 | -16.6 | -48.6 | -16.5 | +3.9 |
| L cipher d=6 reset sub | fill 0.40 | none | litF off | 7 | +0.1 | +1.7 | -15.9 | -49.6 | -16.9 | +3.8 |
| W plain pad beaufort | fill 0.40 | redraw | litF on | 6 | -0.1 | +2.7 | +3.8 | -16.5 | -14.6 | +4.8 |
| L cipher d=6 reset sub | fill 0.40 | none | litF on | 6 | -0.1 | +1.8 | -14.6 | -40.6 | -14.7 | +6.4 |
| W plain pad sub | fill 0.00 | none | litF on | 8 | +0.1 | +2.7 | -21.4 | -18.1 | -12.1 | +8.2 |
| W plain pad beaufort | fill 0.00 | none | litF on | 8 | +0.1 | +2.7 | -21.4 | -18.1 | -12.1 | +7.9 |
| W plain pad beaufort | fill 0.40 | none | litF on | 6 | +0.1 | +2.4 | -15.4 | -18.2 | -13.5 | +4.5 |
| G cipher len beaufort | fill 0.40 | redraw | litF on | 6 | +0.1 | -1.2 | +9.5 | -9.1 | -8.9 | +4.0 |

Nearest misses on all bands (fewest failed, then smallest largest |z|):

| procedure | bands failed | largest \|z\| | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L cipher d=1 cont add | fill 0.40 | none | litF on | 2 | 5.4 | -0.5 | -1.4 | +0.0 | +2.4 | +2.7 | +5.4 | +2.6 | +4.0 | +2.9 | -1.0 | -2.5 | -1.3 | -0.2 |
| T two afterI next BA add | fill 0.40 | none | litF on | 3 | 7.2 | -1.2 | -1.9 | -0.1 | +3.3 | +2.8 | +7.2 | +2.7 | +4.3 | +1.9 | -0.9 | -2.3 | -1.3 | -0.2 |
| G cipher first sub | fill 0.40 | none | litF off | 3 | 16.9 | -16.9 | -15.6 | -3.0 | -2.5 | -1.5 | +2.5 | +0.5 | +4.1 | +2.2 | -1.5 | -0.6 | -1.3 | -0.2 |
| G cipher gsum28 add | fill 0.40 | none | litF off | 3 | 22.8 | -22.8 | -17.9 | -3.0 | -2.5 | -1.4 | +2.6 | +0.6 | +4.2 | +2.2 | +0.1 | -1.0 | -1.3 | -0.2 |
| T two both AB beaufort | fill 0.40 | redraw | litF off | 3 | 23.9 | +21.9 | +23.9 | -2.9 | -2.3 | -0.9 | +1.7 | +0.6 | +5.5 | +2.4 | -0.9 | -2.1 | -1.3 | -0.2 |
| G cipher gsum28 sub | fill 0.40 | none | litF off | 3 | 28.9 | -28.9 | -19.2 | -2.9 | -2.4 | -1.4 | +2.6 | +0.5 | +4.8 | +2.1 | -1.4 | -1.1 | -1.3 | -0.2 |
| L plain d=1 reset sub | fill 0.40 | redraw | litF off | 3 | 40.6 | -0.3 | +40.6 | +0.5 | -0.1 | +2.3 | +1.8 | +1.9 | +2.5 | +1.6 | -6.3 | -13.5 | -1.3 | -0.2 |
| T two afterS next BA add | fill 0.40 | none | litF on | 4 | 4.7 | -1.4 | -2.0 | -0.0 | +2.5 | +2.9 | +4.7 | +3.1 | +4.3 | +4.0 | -2.0 | -2.3 | -1.3 | -0.2 |
| T two afterS word BA add | fill 0.40 | none | litF on | 4 | 7.6 | -2.6 | -3.5 | -0.0 | +2.3 | +2.6 | +3.6 | +3.8 | +7.6 | +2.3 | -2.2 | -2.6 | -1.3 | -0.2 |
| G cipher gsum28 sub | fill 0.40 | redraw | litF on | 4 | 13.1 | +13.1 | +9.9 | -3.4 | -2.3 | -1.2 | +2.7 | +0.5 | +4.1 | +2.0 | -1.4 | -2.3 | -1.3 | -0.2 |
| G cipher gsum add | fill 0.40 | redraw | litF off | 4 | 13.4 | +13.4 | +10.7 | -2.9 | -2.8 | -1.4 | +3.5 | +0.5 | +5.3 | +1.9 | -1.1 | -0.3 | -1.3 | -0.2 |
| R cipher beaufort | fill 0.40 | redraw | litF on | 4 | 14.6 | +14.6 | +10.6 | -3.2 | -2.8 | -1.3 | +2.6 | +0.6 | +5.0 | +2.5 | -1.9 | -2.6 | -1.3 | -0.2 |

## Part B, the decoder

Chance level (200 random decoders on uniform page sets): largest median page z5 0.38, largest single page 4.19.

| plant | own decoder median z5 | pages at z5 >= 6 | rank among decoders | runner-up (median z5, decoder) |
|---|---|---|---|---|
| W cipher fwd sub | fill 0.00 | none | litF off | 47.76 | 55 of 55 | 1 of 733 | 47.76, W cipher fwd sub | fill 0.00 | redraw | litF off |
| L cipher d=2 reset add | fill 0.00 | none | litF off | 47.76 | 55 of 55 | 1 of 733 | 47.76, L cipher d=2 reset add | fill 0.00 | redraw | litF off |
| T two afterS word AB beaufort | fill 0.00 | none | litF off | 47.76 | 55 of 55 | 1 of 733 | 47.76, T two afterS word AB beaufort | fill 0.00 | redraw | litF off |
| G cipher gsum sub | fill 0.40 | none | litF off | 33.61 | 55 of 55 | 1 of 733 | 33.61, G cipher gsum sub | fill 0.00 | redraw | litF off |
| W plain fwd add | fill 0.40 | none | litF off | 1.88 | 10 of 55 | 1 of 733 | 1.88, W plain fwd add | fill 0.00 | redraw | litF off |
| L plain d=1 cont sub | fill 0.40 | none | litF off | 1.41 | 4 of 55 | 5 of 733 | 1.84, L plain d=1 reset sub | fill 0.00 | redraw | litF off |

732 decoders applied to the 55 pages. Largest median page z5 **0.55**; largest single page z5 4.47; pages at z5 >= 6 over all decoders 0; largest z\* 5.30 (judged per decoder above 10, lesson eleven).

| decoder | median page z5 | best page z5 | best page | z\* | text |
|---|---|---|---|---|---|
| L cipher d=3 reset beaufort | fill 0.00 | none | litF off | 0.55 | 2.40 | 51 | 2.97 | TFIHCBEOTHCYHORSOOIGTHAEWOEPDOCBUTNGNGIAAEIAONBUTREAERCEOTXI |
| L cipher d=3 reset beaufort | fill 0.00 | redraw | litF off | 0.53 | 2.38 | 51 | 3.08 | TFIHCBEOTHCYHORSOOIGTHAEWOEPDOCBUTNGNGIAAEIAONBUTREAERCEOTXI |
| L cipher d=1 reset beaufort | fill 0.00 | none | litF on | 0.51 | 2.14 | 42 | 3.44 | WTWLMLUNBUSGAESFHJFHCCDTHJHIUCNGWIBGRIPDYNGXSPIAJCXMNGNGYUIG |
| L cipher d=1 reset beaufort | fill 0.00 | redraw | litF on | 0.48 | 2.15 | 42 | 3.69 | WTWLMLUNBUSGAESFHJFHCCDTHJHIUCNGWIBGRIPDYNGXSPIAJCXMNGNGYUIG |
| T two afterS next BA beaufort | fill 0.00 | none | litF off | 0.48 | 2.39 | 0 | 4.47 | XGMSYTNGIAXBHYTOLCIAEEEMDWOELJMOENTITHELNGPMAEHDLHJXAEHYUNWO |
| T two afterS next BA beaufort | fill 0.00 | redraw | litF off | 0.46 | 2.36 | 2 | 4.54 | WOEOENGEACNGYSLIALATHULEAEODEOPAXXIAMMNGYGDTHWEADJBAYJAIAEON |
| R plain sub | fill 0.00 | none | litF off | 0.42 | 2.59 | 35 | 2.68 | NGHYTWCXTHEASGIAWOEWIAADWNGSLEATIRTHNGYPTHDOENEMHSREOHAEEEAH |
| L cipher d=1 cont beaufort | fill 0.00 | none | litF off | 0.41 | 2.51 | 2 | 4.01 | WOEOENGEACNGYSLIALATHULEAEODEOPAXXIAMMNGYGDTHWEADJBAYJAIAEON |
| T two afterS toggle BA beaufort | fill 0.00 | none | litF on | 0.41 | 2.86 | 14 | 2.99 | XWFIPIATCOSTBNGEAONTUBYUBGEORPGAOHIWDXXNAPRWEEONAOEOARHBLLAL |
| R plain sub | fill 0.00 | redraw | litF off | 0.40 | 2.55 | 35 | 2.71 | NGHYTWCXTHEASGIAWOEWIAADWNGSLEATIRTHNGYPTHDOENEMHSREOHAEEEAH |
| L cipher d=4 reset beaufort | fill 0.00 | none | litF off | 0.39 | 2.68 | 38 | 2.36 | EARABAEEATHRPJOEAEXNGXAEEAIAMXHITMLLOEULHAJTOESEASRLTANGCTIA |
| L cipher d=4 reset beaufort | fill 0.00 | redraw | litF off | 0.38 | 2.58 | 38 | 2.34 | EARABAEEATHRPJOEAEXNGXAEEAIAMXHITMLLOEULHAJTOESEASRLTANGCTIA |

## Registered predictions

- A1 (no S-admissible member; the control, amended, predicts about four S pairs and fails U and Sfreq): 0 S-admissible at 200; control L5S 4.0 against 11 (z +3.2), U z -13.6, Sfreq z -3.9 → holds.
- A2 (no survivor; candidates < 1 %; every member fails L6T): 0 survivors, 0 candidates, L6T failed by 1,408 of 1,464 → fails.
- A3 (plants: 3 no-filler read at rank 1; cipher-sourced filler plant read; plaintext-sourced filler plants not read): W cipher fwd sub 47.8 rank 1; L cipher d=2 reset add 47.8 rank 1; T two afterS word AB beaufort 47.8 rank 1; G cipher gsum sub 33.6 rank 1; W plain fwd add 1.9 rank 1; L plain d=1 cont sub 1.4 rank 5 → holds.
- A4 (no page read): largest median 0.55 against chance 0.38 → holds; pages at z5 >= 6: 0.

Reading: README §77. No member is S-admissible and none reads; the nearest miss, a ciphertext lag-1 autokey with fillers and literal ᚠ, is inside eleven bands and fails the S count and the lag-6 count, the fourth construction to stop at those two cells. A2's clause that every member fails L6T did not hold (56 inside on their spread). [stated — the tables]

Reproduce: `STAGE=chance|screen|confirm|decode|plants|merge .venv/bin/python -I src/autokey_lane.py`.
