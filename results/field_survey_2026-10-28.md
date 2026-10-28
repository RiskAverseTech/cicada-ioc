# Field survey, 2026-10-28: every public Liber Primus repository against this one

A GitHub search on 2026-10-28 ("liber primus", "cicada 3301", "cicada3301", "gematria primus",
"liberprimus", "3301 runes", "cicada runes", "liber-primus"; sorted by update and by stars) returned
213 repositories. 45 carry analysis, tooling or claims about the unsolved pages; the rest are
converters, course projects, bots, stores and empty shells. Every file was fetched as raw text with
the GitHub API and read as data; nothing was executed. The earlier comparisons (jens-wedin, wazar /
Dukotah to Round 25, Leo-Y-Zhang to 2026-09-07, pnotisdev, murphy, aergasrg, Parcae, atelier-primus)
are in `ledger_diff.md`; this file covers what changed there and the labs not read before.

## 1. The labs, by what they are

| Repository | Last push | What it is | Controls | Worth citing |
|---|---|---|---|---|
| Dukotah/cicada3301 | 2026-10-07 | Pre-registered sweeps, LEDGER.json now 172 rows (was 156); "Round 30 merged, nothing running"; every sweep died in a host reboot 2026-09-15 and none resumed | planted, red-teamed | R27 S1: all 2^32 Python 2.7 MT seeds, null; R28-L3: 2.5 M string seeds, null (never written up); R30-A3: page ICC profile is Ghostscript 9.06 `srgb.icc`, toolchain GS 9.01–9.15; A-01 independent re-transcription 0 identity errors |
| pnotisdev/cicada3301 | 2026-10-24 | `docs/registry.toml`, 148 rows (56 excluded, 33 partial, 23 observed, 8 open, 3 untestable); GPU PRNG sweeps; word-boundary audit against the page images | planted (15/15 windows) | 1,447-stream library × every offset × both signs × both anti-repeat models: 409 M decodes, null; 19 M passphrase hash streams null; no key restart at any unit (LLR test), restart at the 9 section starts not testable (power z ≈ 2.7); 0 of 2,334 transcribed word dots missing from the images; the 2-rune-word deficit is mostly TH spelled T+H |
| anon5376/cicada | 2026-10-24 | ~115 experiment directories, "execution lab", plant recovery 0.88–1.0 per lane, marked seeds only | planted | Only lab with classical non-additive families (Hill 2×2–5×5, Playfair 5×6, Bifid, Trifid, ADFGX, Nihilist, Chaocipher, Enigma-29, Solitaire, Gromark, VIC …) and Marsaglia CDROM complete; output-nudge `c:=c+1` excluded at −16.7 σ; page 56 (AN END) shows 2 doublets in 84 pairs (P = 0.11 under the 0.19 filter) |
| farfromexact/Cicada_3301 | 2026-09-19 | Chinese-language lab, SHA-256-frozen pre-registrations, 999-draw nulls, 31 hypotheses | planted | H007: exact finite-state reachability of the solved-page rule at offset 0 excludes 53/55 pages; H030: Berlekamp–Massey over GF(29), no recurrence of order ≤ 16, minimum linear complexity 40 (stopped at 575/999 nulls); H031: 24,360 PGL(2,29) maps, rigid, null; cross-page identical 4-gram windows 121 vs null 112 (p 0.21) |
| ItIsCuthNotCup/Cicada-3301 | 2026-09-19 | 157,575-candidate stream search, rigid and beam, page-73 control z 13.3; hash hunt 1,962 candidates × 4 hashes | planted | IoC 0.034478 (random 0.034483 ± 0.000018); IoC of first differences 0.0353; doublet rate within-word 0.0062, across-word 0.0081, across-line 0.0074; literal-F skip ordinals of the solved pages listed |
| ZzNible (findings, research) | 2026-09-11 | Pre-registered private lab, public summaries only | partial | Within-word lag-5 equality 104/2,105, z 3.75, family-wise p 0.0086 under a null that fixes word lengths, rune multiplicities and K = 86 (§15 here did not replicate under a different null); lag-2 441 vs 456 (p 0.25) |
| invictustitan2/liber-primus-archive | 2026-10-12 | Replication of the deficit with jens-wedin's toolkit, page-57 spiral trace | — | 86/12,942; nudge-vs-resample favours resample; lag 11 at z −3.0 (same dip as §37); repeats independent of previous rune, previous step and prior repeat (p 0.47–0.78, 91 % power for a 4× effect) |
| Leo-Y-Zhang/LiberPrimusAnalysis | 2026-10-28 (CI only) | One substantive commit since 09-07 | planted | IoC null spread corrected to √(2(m−1))/(n−1) from 0.75/√n: 2× too wide at 400 runes, 3.5× at 1,200; dependent tables deliberately not regenerated; doublet-position parity mod 2–8 flat |
| Pitchfork-and-Torch/liber-research | 2026-09-22 | IoC-threshold hypothesis lab, artwork-driven transpositions | 3 plants | Sexagesimal block as running key: 517,896 rigid decrypts (3 orderings × 5 readings × 3 signs × F-rule, every phase and offset), null |
| cicada-solvers/Cicada-DWH-HashcatAttempts | runs 2020-12 | hashcat masks against the page-73 hash | — | Raw bytes ≤ 5, every IPv4, 35 US phone formats × {SHA-512, SHA3-512, BLAKE2b-512, Whirlpool, Streebog-512}: exhausted, 0 hits |
| Inghenius-Lab/cicada-l4-sweep | 2026-10-14 | Actions harness for 3 of Dukotah's L4 cells; no results committed | — | Dukotah's claim bars were fitted against a gitignored panel; a clean clone moves the pair bar 9.64 → ≈ 10.44; the S2 "hit" is a counter reset on restart |
| yo-yo-yo-jbo/cicada_tools | 2024-10 | 33 scripted experiments, no statistics | none | Families nobody else lists: grouping-size Vigenère (key advances every g runes), doublet-triggered switch between two keys, Hill with the squares, Alberti progressive shift, cuneiform page as base-59/60 key under all six digit orderings |
| localavaster/cadrypt | 2023-04 | GUI workbench | none | Crib-drag shift-difference test; word-periodic IoC; OEIS mod 29 by hand |
| mortlach/Liber-Primus-Crib-Assist | 2024-04 | Crib construction from Google 2-grams | none | Word-length skeletons of the red-ink passages (`s 3 12 4 e`, `s 3 6 5 5 3 4 3 3`, `s 8 3 6 2 5 3 2 3`, `2 6 5 5 2 2`, `1 8 8`) treated as English sentences |
| scream314/cicada3301 | 2023-06 | Canonical archive (174 stars) | — | `hints_never_used.md`: trailing-space prime counts, the 2013 "missing primes" 73–1223, the 2012 P.S. number as a 3-row matrix; 2014 notes that the 1033 square was a submission criterion, not a message |
| MonokumaBear/cicadaConvolutionKernels | 2023-07 | Page 32/55 tree kernels | — | Page-32 tree ≈ 17×17 Gaussian σ 5 on a 183×191 downsize; page-55 tree an edge kernel; both ~5×5 block upscales |
| TheronEagle, johnvteixido, nexon33, 2retooz270703, emmanuel6474, AegisTrustCore, HhWolfling, Echo446Ghq, vionorromanov, leorahross2015-afk, chipper1999 | 2025–2026 | Solve claims or "everything ruled out" | none | None checkable; see §4 |
| iBotPeaches, Taiiwo, cmbsolver, neuroretransmit, krcdavis, Taters79, RuneSwiss, Eternalth, Protheme-777, Locyyx64, f1nsternacht, sgroveman, Fafison4k, d4v1-sudo, isitcicada | 2014–2026 | Converters, GUIs, archives | none | isitcicada trusts exactly one key, fingerprint 6D85 4CD7 9333 22A6 01C3 286D 181F 01E5 7A35 090F (same as §30) |

## 2. What the field agrees on (independent labs, same answer)

- **The stream is flat.** IoC at the random value to four decimals; unigrams, bigrams, lags 2–3,000 flat; no key restart at line, sentence, paragraph or page; no key reuse between pages. (ItIsCuthNotCup, pnotisdev, Dukotah, LZ, here §1–§3, §36, §37.)
- **One structural fact, replicated six times.** 86 adjacent repeats where 445 are expected; the mechanism is a re-draw, not a nudge (nudge excluded at −16.7 σ by anon5376, by first-difference shape here §5); repeats are blind to word, line and clause boundaries (§33) and independent of the previous rune and step (invictustitan2); the lag-11 dip (z ≈ −3) is seen by two labs and is within the family-wise null.
- **The transcription is right.** Dukotah A-01 (0 identity errors in 13,121 slots), the blind re-reading here (§38, 0 disagreements at 12,807 glyphs), pnotisdev's word-dot audit (0 of 2,334 missing), Dukotah R28-L2 (payload bytes 11/11).
- **No linear generator of short order.** Berlekamp–Massey over GF(29) finds no recurrence of order ≤ 16 and a minimum linear complexity of 40 (farfromexact); the lag spectrum shows no period to 3,000.
- **The additive-stream space is swept at the published scale.** Libraries of 1,400+ number-theoretic streams at every offset, both signs, both anti-repeat models (pnotisdev 409 M decodes); ten common PRNGs over 2^32 seeds (pnotisdev GPU); Python 2.7 MT over 2^32 (Dukotah S1); 2.5 M string seeds (Dukotah L3); 19 M passphrase hashes (pnotisdev); ~215 running-key texts (wazar, JW, here §25, §40); the book's own words and phrases, all signs, both F variants, under the skip rule (here §9, §12).
- **The side channels are empty.** OutGuess, JPEG container, chroma, LSB, glyph geometry, font allographs, subpixel, onion stego (here §26, Dukotah R29–R30, ZzNible T13); the page-73 hash against raw bytes ≤ 5, IPv4, phone numbers, 1,962 document candidates, 19 M passphrases and 502 archived artefacts × 3,977 readings (hashcat, ItIsCuthNotCup, pnotisdev, here §35).
- **Power limits are now stated by three labs.** Pages under ~120 runes are not excluded by z ≥ 6 rules (here §23); restart at the nine section starts is untestable (pnotisdev); pooled reuse needs ~20 aligned pages (here §36); per-page maximum statistics hide the lag-1 deficit entirely (farfromexact H008), so a per-page screen is the wrong instrument for it.

## 3. Where this repository differs from the field

Distinct here: detection power measured by page length and a second pre-registered rule for the short pages (§23–§24, §27, §39); the soft re-draw rule fitted as a generative model (0.81) and used inside an exact every-offset Viterbi rather than a beam or an IoC screen; boundary-blindness of the repeats; the blinded glyph-level re-reading; keyword-mixed alphabets under the book's keys (§32); five unlisted generators (§31); PGP verification by full fingerprint (§30); the squares as keys (§29); the artefact hash sweep (§35).

Not here, and done elsewhere with at least one plant: the classical non-additive families (anon5376), Berlekamp–Massey linear complexity (farfromexact), exact finite-state reachability of the solved-page rule (farfromexact H007, offset 0 only), the sexagesimal block at every phase (Pitchfork, rigid), the page-56 doublet count (anon5376), the IoC null spread correction (LZ), rigid extra-key-advance at word edges and after ciphertext F (anon5376; pnotisdev lists "unkeyed insertions" as its open row of priority 1).

## 4. Claims that can be dismissed, and why

- **2retooz270703 (27×27 grid, 2026-10-28).** The specified part (row-major grid of pages 0–2, node key (a, φ(b), c), phase rotation, subtraction) is testable; the chaining of blocks (anchor, distance, block length 2–7, direct-or-totient key) is chosen per block from ≈ 10^7 readings, and the 17 decrypted blocks cover 54 of 729 cells. Any 3–5-rune English word is reachable by choice. Refutation: a shuffled-grid null on the same enumeration (one hour; see §5, item 10).
- **nexon33 ("95 % solved").** Post-hoc formulas for the known literal-F skip ordinals; the document itself needs a different seed per page.
- **TheronEagle ("everything ruled out").** Dictionary hit-rate scorer, no skip model, page map off by 14 then by 3, page 67 missing.
- **johnvteixido ("25,241-rune geometric payload").** Line-angle quantisation artefact, no controls.
- **emmanuel6474 ("DESTROY / TRUTH differentials").** Private formalism, synthetic-only control, no look-elsewhere accounting.
- **vionorromanov ("full decryption").** The one file is one byte.
- **Echo446Ghq, leorahross2015-afk, HhWolfling, chipper1999.** Not Liber Primus analysis (a 131-digit number, devotional prose, word salad, pixel arithmetic).

## 5. Checks this repository has not run, ranked by what they could change

Ranked by the chance of producing plaintext or a second structural fact, then by cost. "Closure" means the result is expected null and the value is a stated boundary.

1. **Doublet-triggered second key** (yo-yo-yo-jbo's family, never run with controls anywhere). The re-draw rule says what is rejected, not what replaces it. A deterministic replacement from a second key word is a concrete mechanism that produces exactly a lag-1 deficit and would make the plaintext recoverable by key search. Book-word pairs ≈ 10^5 × 55 pages under the existing decoder with a two-key state; one evening.
2. **Unkeyed insertions and extra key advance at word edges under the skip decoder** (pnotisdev's open row of priority 1; anon5376 ran it rigid with a small key set). Our §14 covered key-advance events; the "one extra rune per word that consumes no key" variant is untested skip-aware. Hours.
3. **The within-word lag-5 echo under the K-fixed null** (ZzNible z 3.75, pnotisdev: carried by the rune S, 11 of 102 coincidences). §15 did not replicate under a null that did not fix K = 86 or the multiplicities. If it survives the right null it is the only second structural fact in the stream and any mechanism must produce it. Hours.
4. **PHP `mt_rand` (canonical and the pre-7.1 twist) and glibc `random() % 29` under the soft rule.** Dukotah's L4 queue, never fired; Inghenius committed no results; §31 did not include them. 2^18 seeds in hours; 2^32 in C over days.
5. **Closure bundle, one afternoon:** (a) doublet rate on every solved polyalphabetic page (AN END, WELCOME) against the 0.19 ratio, which decides whether the re-draw is a house style or specific to the unsolved section; (b) pooled cross-page repeated 3/4/5-gram counts against a per-page shuffle null, which nobody has beyond one 4-gram figure; (c) Berlekamp–Massey linear-complexity profile per page and whole stream with LFSR plants, completing farfromexact's stopped run; (d) doublet-position parity mod 2–8 (LZ), which excludes fixed-frame digraphic ciphers; (e) repeat context-independence replicated inside `doublet_boundaries`.
6. **IoC null spread audit.** If any pooled-offset statistic in §1–§3 or §36 used a √n approximation, LZ's correction changes the power figures and the reuse boundary. Under an hour.
7. **Streams run rigidly elsewhere, under the skip rule here:** digits of π, e, √2, φ in base 10 and base 29 (ItIsCuthNotCup, 200 offsets rigid); the sexagesimal block under all six digit orderings, reversed, every phase (yo-yo-yo-jbo, Pitchfork rigid); a common PGL(2,29) map (farfromexact rigid). Closure; hours each with the existing lanes.
8. **Exact finite-state reachability of the solved-page rule at every offset, both signs, per page and continuous** (farfromexact did offset 0 only). A no-path result is a deterministic exclusion, stronger than any score. Minutes per offset.
9. **Digraphic and fractionating families with word-based frames on the nine short pages** (Playfair 5×6, Bifid, Trifid, Hill from the squares). anon5376 planted them on a few splits only; LZ's parity test excludes only fixed frames. Low prior, about a day.
10. **Community service, one hour each:** the shuffled-grid null for the 27×27 claim; TheronEagle's repeated word-length 8-gram at pages 22/47 against the expected count among 2,928 words; the ICC byte-compare to Ghostscript 9.06 `srgb.icc` (confirms the production toolchain); the red-ink word-length skeletons against English 2-gram skeletons (feeds the open red-text item); the 2013 "missing primes" and trailing-space counts as finite seeds.

## 6. Corrections to earlier statements here

- `ledger_diff.md` said wazar's R12-C2 corpus of 29 esoteric texts was never run. Dukotah R26-B has since run 33 texts at 4–8 offsets each over 9 pages, sign −1 only, keyskip 1 and 2 (1,562 decodes, 0 clears); pages 20, 22, 25, 27, 29, sign +1 and reversed texts remain unrun, and the Gutenberg-id problem recorded there is unaddressed.
- Dukotah's R27 S2 "HIT-CANDIDATE" is a status counter that resets on restart (Inghenius); the S1 2^32 null stands, the S2 lane (44 % complete) does not carry a hit.
- Dukotah's claim bars for the pair cells were fitted against a panel file not in the repository (Inghenius); anyone reusing those bars must refit.

Files read are listed per repository under the survey directory of the session scratchpad; none are committed.
