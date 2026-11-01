# The three behaviours as the switch of a self-keyed cipher: decoder first, then the bands

Registration: `results/behaviours_registration.md`. 288 members, 2,304 procedures, 1,152 decoders; beam 8; bands D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq, U, W2, WM; LP2 reference D 86, D_in 63, L3 179, L4 131, L5 102, L5S 11, BIG 9, L6T 77, SHARE 7.21, Sfreq 0.0335, U 26.4, W2 0.159, WM 4.42.

## Part B, the decoder (first)

| plant | own decoder median z5 | pages at z5 >= 6 | rank among decoders | fillers planted / placed | runner-up (median z5, decoder) |
|---|---|---|---|---|---|
| pclass s/h/a lag sub | fill 0.00 | none | litF off | 47.48 | 55 of 55 | 1 of 101 | 0 / 13 | 11.51, prevword s/h/a lag sub | fill 0.00 | none | litF off |
| word s/a/h pointer add | fill 0.00 | none | litF off | 47.77 | 55 of 55 | 1 of 101 | 0 / 20 | 20.70, prevword s/h/a lag add | fill 0.00 | none | litF off |
| scount h/s/a lag beaufort | fill 0.00 | none | litF off | 48.07 | 55 of 55 | 1 of 101 | 0 / 25 | 13.76, prevword h/a/s lag beaufort | fill 0.00 | none | litF on |
| csum h/a/s pointer sub | fill 0.40 | none | litF off | 44.59 | 55 of 55 | 1 of 100 | 1075 / 1095 | 15.58, csum h/a/s lag sub | fill 0.00 | none | litF off |
| prevword a/s/h lag add | fill 0.40 | none | litF off | 45.15 | 55 of 55 | 1 of 101 | 1075 / 1069 | 18.32, prevword s/h/a lag add | fill 0.00 | none | litF off |
| cclass a/h/s pointer beaufort | fill 0.40 | none | litF off | 44.99 | 55 of 55 | 1 of 101 | 1075 / 1057 | 11.49, prevword s/h/a pointer beaufort | fill 0.00 | redraw | litF off |

Chance level (200 random decoders on uniform page sets): largest median page z5 10.17, largest single page 14.10.

1,152 decoders applied to the 55 pages. Largest median page z5 **10.79**; largest single page z5 14.73; pages at z5 >= 6 over all decoders 54442.

| decoder | median page z5 | best page z5 | best page | fillers placed | text |
|---|---|---|---|---|---|
| prevword a/s/h lag beaufort | fill 0.00 | none | litF off | 10.79 | 13.51 | 48 | 2108 | NGOACPASOMBEARSCAJEPOEMSEAJALNGRUMDNGEASYGIGTEUNBEEGEARSCUDT |
| prevword a/s/h lag beaufort | fill 0.00 | redraw | litF off | 10.69 | 13.59 | 48 | 2108 | NGOACPASOMBEARSCAJEPOEMSEAJALNGRUMDNGEASYGIGTEUNBEEGEARSCUDT |
| prevword a/h/s pointer add | fill 0.00 | redraw | litF on | 10.67 | 13.10 | 30 | 2085 | UBCEPATOUNGRAPTIALGEOURPCYUTHURYCONMOCPWTHLETHYOIATWCGTHAUCL |
| prevword a/s/h lag add | fill 0.00 | redraw | litF off | 10.67 | 13.31 | 31 | 2147 | THOEORAIAPAEMHACEDEALSCOGSEMDEEOPIWAUNGYNALJANUSCOEICELAWBAW |
| prevword s/h/a lag sub | fill 0.00 | none | litF off | 10.64 | 13.11 | 42 | 2090 | DHEANGFUDORLSNGWMUNGTHATIBASIAAWTHSASASTRHFAIGATHNGGYPATHSIA |
| prevword a/s/h lag add | fill 0.00 | none | litF off | 10.63 | 13.15 | 42 | 2147 | DXMTHHOELDWEPTAWBRXOOTHELPETPEWRITTOLIBSACIALSJBDUAUFYRIDLNA |
| prevword s/h/a lag beaufort | fill 0.00 | none | litF on | 10.61 | 12.37 | 16 | 2119 | EOMAETHUOSBCTHREBANGDTPAOLTNGMRAEXXICOMMUSYTOEPAMRATHWNGMAFO |
| prevword s/h/a pointer add | fill 0.00 | redraw | litF off | 10.60 | 12.79 | 29 | 2158 | THREAEXALCNGDIUAWDLUFODOENLAMAGEHTRAMNGBEAYIAIYUEIAMOLIAMYNG |
| prevword s/h/a lag beaufort | fill 0.00 | redraw | litF on | 10.60 | 12.30 | 43 | 2119 | MORMYNAEARHXLENTANGSFOHSFENTHOANDFEARFATHREANGOEINNGBXCBATAS |
| prevword s/h/a lag sub | fill 0.00 | redraw | litF off | 10.58 | 12.82 | 42 | 2090 | DHEANGFUDORLSNGWMUNGTHATIBASIAAWTHSASASTRHFAIGATHNGGYPATHSIA |
| prevword a/h/s pointer add | fill 0.00 | none | litF on | 10.57 | 13.05 | 30 | 2085 | UBCEPATOUNGRAPTIALGEOURPCYUTHURYCONMOCPWTHLETHYOIATWCGTHAUCL |
| prevword a/s/h lag sub | fill 0.00 | redraw | litF off | 10.57 | 13.41 | 18 | 2105 | EADGDJMDFOLUMUTHNIAUNHEACHMYLATHSPELUMEAOATHCOARIALTLEOHTHXE |

## Part A, the generator (second)

S-admissible at the screen: **0** of 2,304; at 200 replicates: **0**. Candidates: **0**; survivors: **0**.
Bands failed, over the family: D 2,304, D_in 2,304, L6T 2,278, U 2,272, L5S 2,060, BIG 1,279, Sfreq 1,263, W2 1,152, WM 1,152, L5 824, SHARE 802, L4 145, L3 64.


Nearest misses (fewest bands failed, then smallest largest |z|):

| procedure | bands failed | largest \|z\| | D | D_in | L3 | L4 | L5 | L5S | BIG | L6T | SHARE | Sfreq | U | W2 | WM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wpos a/h/s pointer sub | fill 0.40 | none | litF off | 4 | 11.3 | -11.3 | -8.8 | +0.6 | +1.5 | +2.9 | +2.6 | +5.3 | +4.8 | +2.6 | -2.1 | -2.8 | -1.3 | -0.2 |
| word s/a/h pointer beaufort | fill 0.40 | redraw | litF on | 4 | 11.3 | +11.3 | +7.3 | -0.3 | +0.4 | +1.1 | +2.9 | +3.0 | +3.8 | +2.9 | -2.7 | -5.6 | -1.3 | -0.2 |
| icount s/a/h pointer add | fill 0.40 | none | litF on | 4 | 11.5 | -11.5 | -11.2 | -0.8 | +0.6 | +1.9 | +6.2 | +2.7 | +4.0 | +2.4 | +1.1 | -2.9 | -1.3 | -0.2 |
| icount a/h/s pointer beaufort | fill 0.40 | none | litF off | 4 | 12.3 | -12.3 | -10.6 | -0.7 | +0.7 | +1.9 | +5.4 | +2.5 | +3.4 | +2.7 | -2.4 | -2.9 | -1.3 | -0.2 |
| icount a/h/s pointer add | fill 0.40 | none | litF off | 4 | 12.9 | -12.3 | -12.9 | -0.4 | +0.3 | +1.6 | +4.5 | +2.8 | +3.7 | +2.3 | +0.5 | -2.5 | -1.3 | -0.2 |
| word s/a/h pointer add | fill 0.40 | none | litF off | 4 | 13.4 | -13.4 | -13.1 | -1.0 | -0.1 | +1.5 | +5.8 | +2.2 | +3.8 | +2.1 | +1.4 | -2.9 | -1.3 | -0.2 |
| word a/h/s pointer beaufort | fill 0.40 | none | litF off | 4 | 14.9 | -14.6 | -14.9 | -1.5 | -0.4 | +1.3 | +5.4 | +2.9 | +4.0 | +2.3 | -3.0 | -2.7 | -1.3 | -0.2 |
| icount s/h/a pointer beaufort | fill 0.40 | redraw | litF off | 4 | 15.2 | +15.2 | +11.1 | -0.9 | -0.3 | +1.2 | +2.5 | +2.1 | +2.8 | +2.0 | -5.2 | -5.5 | -1.3 | -0.2 |
| scount s/a/h lag sub | fill 0.40 | none | litF off | 4 | 15.6 | -15.6 | -14.2 | -1.3 | -1.4 | +1.8 | +2.9 | +2.0 | +4.1 | +2.9 | -2.2 | -4.3 | -1.3 | -0.2 |
| icount a/h/s pointer beaufort | fill 0.40 | redraw | litF on | 4 | 15.7 | +15.7 | +11.4 | -0.1 | +0.5 | +1.7 | +4.0 | +2.9 | +5.1 | +2.1 | -2.1 | -3.0 | -1.3 | -0.2 |
| icount s/a/h pointer add | fill 0.40 | none | litF off | 4 | 18.4 | -18.4 | -16.2 | -0.4 | +0.6 | +2.6 | +5.2 | +2.7 | +3.9 | +2.6 | +0.6 | -2.1 | -1.3 | -0.2 |
| scount a/h/s lag sub | fill 0.40 | none | litF off | 4 | 19.5 | -19.5 | -16.3 | -1.3 | -1.0 | +0.7 | +2.7 | +1.7 | +3.9 | +2.4 | -2.2 | -4.7 | -1.3 | -0.2 |

## Registered predictions

- B1 (six plants read at rank 1; filler plants' fillers placed within 20 %): pclass s/h/a lag sub 47.5 rank 1 fillers 0/13; word s/a/h pointer add 47.8 rank 1 fillers 0/20; scount h/s/a lag beaufort 48.1 rank 1 fillers 0/25; csum h/a/s pointer sub 44.6 rank 1 fillers 1075/1095; prevword a/s/h lag add 45.1 rank 1 fillers 1075/1069; cclass a/h/s pointer beaufort 45.0 rank 1 fillers 1075/1057 → holds.
- B2 (no page read, amended: median within 1.0 of the chance maximum median, single page within 1.0 of the chance maximum single page): largest median 10.79 against chance 10.17; largest single page 14.73 against chance 14.10 → holds.
- B3 (no S-admissible member): 0 at the screen, 0 at 200 → holds.
- B4 (no candidate; under one in ten inside L6T): 0 candidates, 26 of 2,304 inside L6T → holds.

Reading: README §78. The decoder reads every plant with its fillers placed; the pages sit at the decoder's own chance level, which the beam's optimizing lift puts near z 10; no procedure reaches the S cell or the bands, and every one fails the repeat count. [stated — the tables]

Reproduce: `STAGE=plants|chance|decode|screen|confirm|merge .venv/bin/python -I src/behaviours_lane.py`.
