# An audit of the two foreground facts

Registration: `results/foreground_audit_registration.md`. 55 pages, within-word pairs; K-fixed null 999 arrangements per page (burn-in 20, thinning 4 attempted transpositions per rune, seed 1034); word-preserving shuffle 999 per page.

## 1. Reproduction and 7. the second null

| fact | observed | K-fixed mean ± sd | z | p | shuffle mean ± sd | z | p |
|---|---|---|---|---|---|---|---|
| lag-5 equalities | 102 | 71.0 ± 8.3 | +3.73 | 0.001 | 70.7 ± 8.2 | +3.84 | 0.001 |
| S..S pairs | 11 | 2.2 ± 1.5 | +6.00 | 0.001 | 2.2 ± 1.5 | +5.66 | 0.001 |
| lag-6 hits of 24 − 2c | 77 | 43.7 ± 6.5 | +5.13 | 0.001 | 43.5 ± 6.7 | +5.02 | 0.001 |

## 2. Leave one page out

| fact (null) | full z | smallest z over the 55 leaves | largest | largest single-page share of the excess | top contributing pages (observed, null mean, share) |
|---|---|---|---|---|---|
| lag-5 equal (K-fixed) | +3.73 | +3.19 | +3.96 | 0.15 | LP2-16 (6, 1.5, 0.15); LP2-09 (6, 1.8, 0.14); LP2-13 (4, 1.2, 0.09); LP2-50 (3, 0.5, 0.08); LP2-36 (4, 1.6, 0.08) |
| S..S (K-fixed) | +6.00 | +5.35 | +6.25 | 0.11 | LP2-50 (1, 0.0, 0.11); LP2-51 (1, 0.0, 0.11); LP2-06 (1, 0.0, 0.11); LP2-38 (1, 0.0, 0.11); LP2-39 (1, 0.0, 0.11) |
| lag-6 hits (K-fixed) | +5.13 | +4.62 | +5.40 | 0.10 | LP2-29 (4, 0.6, 0.1); LP2-45 (4, 0.8, 0.1); LP2-00 (4, 0.9, 0.09); LP2-13 (3, 0.7, 0.07); LP2-12 (3, 0.7, 0.07) |
| lag-5 equal (shuffle) | +3.84 | +3.34 | +4.06 | 0.14 | LP2-16 (6, 1.6, 0.14); LP2-09 (6, 1.7, 0.14); LP2-13 (4, 1.2, 0.09); LP2-50 (3, 0.5, 0.08); LP2-36 (4, 1.5, 0.08) |
| S..S (shuffle) | +5.66 | +5.05 | +5.89 | 0.11 | LP2-50 (1, 0.0, 0.11); LP2-06 (1, 0.0, 0.11); LP2-38 (1, 0.0, 0.11); LP2-51 (1, 0.0, 0.11); LP2-41 (1, 0.0, 0.11) |
| lag-6 hits (shuffle) | +5.02 | +4.54 | +5.27 | 0.10 | LP2-29 (4, 0.6, 0.1); LP2-45 (4, 0.8, 0.1); LP2-00 (4, 0.9, 0.09); LP2-22 (3, 0.7, 0.07); LP2-13 (3, 0.7, 0.07) |

## 3. Concentration at lag 6

77 hits in **27** distinct (earlier, later) pairs. Largest pair: W→I (6), T→NG (5), O→E (5), TH→L (5), P→IA (4).
Largest pair's share 0.078 (K-fixed null among its own hits: central 95 % 0.070–0.150; p(≥) 0.915); distinct pairs / hits 0.351 (null 0.413–0.647, a ratio that falls as hits rise because the map has only 29 pairs: 77 hits falling uniformly on 29 pairs would occupy 27.1 distinct pairs, and they occupy 27); share through the fixed point H→H 0.026 (null 0.000–0.100, p 0.490).

## 4. Concentration at lag 5

102 equalities over **28** rune values; largest: S (11), A (7), P (7), N (6), NG (6), EA (5). Largest value's share 0.108 (null 0.063–0.118; p 0.068); distinct values / equalities 0.275 (null 0.312–0.464).
By page: 43 of 55 pages carry a lag-5 equality (largest page 6); 40 carry a lag-6 hit (largest 4).

## 5. The words that carry sites

179 sites in 145 words. Largest number of sites in one word: **4** (SDNGGLSDNG, LP2-50: 3 lag-5 equalities, 1 lag-6 hit; it is the lag-5 trigram run of §46). Without that one word the three facts stand at z +3.37, +5.32, +4.97. Share of site words whose exact rune string occurs as another word anywhere on the pages: **0.000** (words of the same lengths drawn at random from the pages: 0.000 ± 0.000).

Word forms carrying two or more sites: SDNGGLSDNG (4), CBUOECBLNOENGXO (3), WBMRNMHMINAD (3), EAYPOETHSYP (3), POEJANGPTHPANG (3), SPTFPUNGYNGXIA (2), BEOLDHBM (2), RIGTHEAETG (2), THYEOTHJTHRU (2), ASIATHSTHSFMGDEA (2), NGPOAYNGPS (2), WIAEARAEWIADATH (2), AEEOFTHCLOXLOL (2), BGDXMBXCNGTHYDAEEA (2), NAEAOANATHGO (2), EORNSOOCAEYEE (2), PHNGEDOEOHJ (2), NUXAEMTDTAE (2), OEAEGJNGIANMYOEIA (2), IBNGPNIRG (2), NPCHRYWLXRB (2), HTNGHAGONGAE (2), UPSTHICPSIW (2), UIOJOEOOEJDO (2), YEASOEEOUAIA (2), MLITHTEASNGL (2), PCEOUTCIAEONGNUHTH (2), ESEOTHTHES (2).

## 6. The eleven S pairs

| page | word | position of the later S | word (Latin) | form recurs among site words |
|---|---|---|---|---|
| LP2-01 | 1 | 5 | SOERUWSLIA | no |
| LP2-06 | 6 | 8 | WIIASPLTHASJ | no |
| LP2-09 | 49 | 6 | ASIATHSTHSFMGDEA | no |
| LP2-20 | 38 | 6 | OSTMRYSX | no |
| LP2-38 | 30 | 8 | NGNCSNDEONSICIA | no |
| LP2-39 | 42 | 7 | UPSTHICPSIW | no |
| LP2-41 | 1 | 5 | SYMDYS | no |
| LP2-47 | 2 | 8 | FUXSXITHAESM | no |
| LP2-50 | 11 | 5 | SDNGGLSDNG | no |
| LP2-51 | 17 | 5 | SOEACES | no |
| LP2-54 | 12 | 6 | ESEOTHTHES | no |

11 S pairs in 11 distinct word forms on 11 pages.

## Registered predictions

- F1 (every leave-one-out z within 1.0 of the full z; no page over a fifth of the excess; the two facts under K-fixed): → holds.
- F2 (largest lag-6 pair under 15 %; distinct pairs ≥ 45 % of hits; H→H inside the null's 95 %): 0.078, 0.351, 0.026 → fails.
- F3 (no word form with more than three sites; under 15 % of site words repeat a form): 4, 0.000 → fails.
- F4 (the S pairs in ≥ 8 forms on ≥ 6 pages): 11 forms, 11 pages → holds.
- F5 (both facts at z ≥ 3 under the word-preserving shuffle): +3.84, +5.02 → holds.

Runtime 239 s. Reproduce: `.venv/bin/python -I src/foreground_audit.py`.
