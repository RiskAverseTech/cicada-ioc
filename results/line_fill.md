# Is the line-first rune effect the greedy line fill?

Registration: `results/line_fill_registration.md` (commit 02bb7a1, before the check). Scans: 75 JPEGs from github.com/scream314/cicada3301, assets/2014/liber-primus-complete, SHA-256 in `results/scans_sha256.txt`; image NN is transcription chunk NN−1 (confirmed by line counts on 74 pages and by glyph counts per line, which agree with the transcription within one glyph on nearly every line; `results/scan_glyphs.json`). 23 scans are grayscale.

## What the scans show about the glyphs

```
lines used 507; aligned exactly 439
height ratio first/rest : median 1.000, mean 0.995, 10-90 % 0.98-1.01
height ratio second/rest: median 1.000, mean 0.998, 10-90 % 0.99-1.01
height ratio last/rest  : median 1.000, mean 0.987, 10-90 % 0.99-1.01
width  ratio first/rest : median 1.060, mean 1.123, 10-90 % 0.76-1.51
width  ratio second/rest: median 1.000, mean 1.011, 10-90 % 0.70-1.40
width  ratio last/rest  : median 1.011, mean 1.041, 10-90 % 0.70-1.49

rune widths (px) from aligned glyphs at positions >= 1:
F 34±0 (n337), U 53±0 (n312), TH 34±0 (n323), O 34±3 (n343), R 35±1 (n317), C 53±3 (n257), G 43±0 (n316), W 35±0 (n275), H 43±0 (n295), N 34±0 (n322), I 9±2 (n335), J 45±2 (n342), EO 41±1 (n293), P 53±0 (n309), X 66±1 (n315), S 35±0 (n318), T 50±0 (n318), B 34±1 (n323), E 53±3 (n320), M 53±0 (n303), L 34±1 (n321), NG 50±0 (n332), OE 44±1 (n351), D 53±1 (n298), A 34±1 (n333), AE 34±0 (n321), Y 53±0 (n314), IA 53±1 (n329), EA 87±3 (n321)

first-glyph width vs its rune type: mean dev -0.32 sd, |dev|>2.5 in 0.000 of 439
second-glyph width vs its rune type: mean dev +0.02 sd, |dev|>2.5 in 0.002
largest first-glyph width disagreements (|dev|, chunk, line, rune, width, rune median): [(np.float64(1.0), 70, 9, 'S', 34, np.float64(35.0)), (np.float64(1.0), 70, 6, 'Y', 52, np.float64(53.0)), (np.float64(1.0), 69, 6, 'P', 52, np.float64(53.0)), (np.float64(1.0), 64, 9, 'P', 52, np.float64(53.0)), (np.float64(1.0), 64, 3, 'W', 34, np.float64(35.0)), (np.float64(1.0), 63, 9, 'U', 52, np.float64(53.0)), (np.float64(1.0), 63, 5, 'U', 52, np.float64(53.0)), (np.float64(1.0), 63, 1, 'P', 52, np.float64(53.0))]

first-glyph measured widths by transcribed rune (n, median) vs rune median elsewhere:
EA n28 87/87, OE n25 44/44, P n24 52/53, D n21 52/53, Y n20 52/53, U n19 52/53, M n19 52/53, C n19 53/53, IA n18 52/53, AE n17 34/34, NG n17 50/50, H n17 43/43, EO n16 41/41, X n16 66/66, F n16 34/34, E n15 52/53, J n15 45/45, L n14 34/34, S n12 34/35, TH n12 34/34, A n12 34/34, T n12 50/50, G n11 43/43, W n9 34/35, O n8 34/34, B n8 34/34, N n8 34/34, I n7 9/9, R n4 34/35
```

The runes are a digital font with fixed per-rune widths (standard deviation 0–3 px). Line-initial glyphs have the height of their line (ratio 1.000) and the width of their own rune type elsewhere (439 aligned lines, no first glyph more than 1 px off), so nothing is enlarged or decorated at line starts and the transcription's line-initial identities agree with the measured width classes. The line-initial glyphs are wider than the average glyph (width ratio to the rest of the line, median 1.06, mean 1.12) because wider runes are chosen there, not because the glyphs are drawn larger. [stated]

## G1 and G2

```
inter-glyph gap: median 5 px, 25-75 % 4-7; separator gaps (>10) share 0.22
G1: slack < next first glyph + space (+8 px tolerance) on 494 of 517 line pairs = 0.956; slack median 23 px, 90 % 53; slack/need median 0.46, 90 % 0.93
G2: chi2 vs page distribution 78.7 (p 1.1e-06); vs width model at measured space s=5: 34.5 (p 0.184); best s=9: 34.1 (p 0.196)
rune: observed / page-expected / width-model-expected (measured s):
EA 38/21/40, P 33/20/24, D 32/20/24, H 27/19/19, IA 29/22/25, NG 27/21/23, M 26/20/24, C 26/20/24, W 13/18/15, G 14/20/20, T 14/20/23, B 12/20/16, N 12/20/16, O 12/21/17, I 9/22/6, R 6/19/16
residual z under the width model, largest: [(-2.5, 'R'), (2.0, 'H'), (1.8, 'P'), (-1.8, 'T'), (1.7, 'D'), (-1.3, 'G')]
```

G1 as registered used the page's widest line end as the right edge; on twelve pages (chunks 56–64, 68–70) a piece of the margin tree ornament reaching inside x = 2000 was counted as a glyph and set that edge about 200 px too far right, which made 26 % of line pairs look slack. With the edge capped at 1830 px (no text line ends beyond 1800) the rule holds on 494 of 517 pairs, 95.6 %, and the slack is below one next-glyph on 90 % of pairs. The correction is a measurement fix, recorded here and in the script; the claim was not changed. [stated]

**Reading.** G1 holds: the lines are filled greedily, a line breaking when the next glyph does not fit, mid-word two times in three. G2 holds: weighting each rune's page frequency by its glyph width plus the measured 5-px space takes the line-start χ² from 78.7 (p 1 × 10⁻⁶) to 34.5 (p 0.18) on 28 df, with EA predicted at 40 against 38 observed and I at 6 against 9; the largest residual left is R at −2.5. The line-first effect of §63 and §64 is the line fill selecting wide glyphs. It is a layout mechanism of the typesetting, not a cipher statistic and not a transcription error, and it is closed. [stated — the tables; the reading inferred]

## Red glyphs on the colour scans (inventory for the red-text row)

Read against the transcription where the line aligns; where the line is short by the drop cap or heading glyphs the run is read by count. The 23 grayscale scans carry no colour.

- chunk 16 img 17 line 1: 10 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] -> SHEOGMIAFSYENGC (by count, line short by 3)
- chunk 19 img 20 line 1: 15 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> LJEOHNGCTHTAEJTXHTUOE (by count, line short by 1)
- chunk 19 img 20 line 7: 2 red glyphs at [0, 1] -> PDTH (by count, line short by 1)
- chunk 22 img 23 line 4: 10 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] ->  (by count, line short by -14)
- chunk 23 img 24 line 10: 14 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> DOOETTHAECWJXEAGEAM
- chunk 24 img 25 line 1: 11 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> XIXMUXMCTHPOB (by count, line short by 1)
- chunk 31 img 32 line 1: 9 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8] -> FULMAEAYOEA
- chunk 31 img 32 line 3: 4 red glyphs at [4, 5, 6, 7] -> (unaligned)
- chunk 31 img 32 line 6: 10 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] -> IARNGUFTHNGPOEBHGH (by count, line short by 3)
- chunk 39 img 40 line 1: 15 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> UAWNGGXDGIBIEOTBIY (by count, line short by 1)
- chunk 43 img 44 line 1: 18 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> MPYLSOAAEHLEEOIMLLSCP (by count, line short by 1)
- chunk 49 img 50 line 1: 9 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8] -> DEOXCFIAWHG (by count, line short by 1)
- chunk 49 img 50 line 6: 6 red glyphs at [0, 1, 2, 3, 4, 5] -> NGTHEOIFCOEEO (by count, line short by 2)
- chunk 52 img 53 line 6: 1 red glyphs at [0] ->  (by count, line short by -1)
- chunk 53 img 54 line 1: 1 red glyphs at [0] ->  (by count, line short by -1)
- chunk 53 img 54 line 5: 1 red glyphs at [0] ->  (by count, line short by -1)
- chunk 53 img 54 line 10: 1 red glyphs at [0] ->  (by count, line short by -1)
- chunk 54 img 55 line 4: 1 red glyphs at [0] ->  (by count, line short by -1)
- chunk 55 img 56 line 7: 2 red glyphs at [0, 1] -> IACS (by count, line short by 1)
- chunk 56 img 57 line 1: 7 red glyphs at [0, 1, 2, 3, 4, 5, 6] -> FNMYGDAEH (by count, line short by 1)
- chunk 69 img 70 line 6: 1 red glyphs at [18] -> T
- chunk 69 img 70 line 7: 24 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> PWEOSWBEOTHNHGJRIADIATHAIEOAEXLEO
- chunk 69 img 70 line 8: 22 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]... -> EAIAAJHRTHPDJNGOGFEOMCHDOTC
- chunk 69 img 70 line 9: 4 red glyphs at [0, 1, 2, 3] -> URPN
- chunk 70 img 71 line 1: 8 red glyphs at [0, 1, 2, 3, 4, 5, 6, 7] -> AMNGDIATHXIM (by count, line short by 1)

Reproduce: `SCANS=... .venv/bin/python -I src/scan_segment.py`, then `src/scan_first_glyphs.py` and `src/scan_line_fill.py`.
