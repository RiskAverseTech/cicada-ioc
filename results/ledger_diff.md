# Ledger diff: this repository against three public Liber Primus analyses

Checked 2026-10-23. Sources read as data (never executed), cloned or fetched into `external/`
(gitignored):

| Short name | Repository | Version read | Files read |
|---|---|---|---|
| **JW** | jens-wedin/liber-primus | HEAD 2026-10 (REPORT §1–§62, work dated 2026-08-17 → 08-26) | README.md, REPORT.md, BACKLOG.md, results/dukotah_ledger_diff_2026-08-23.md, src/attacks/attack_vigenere_skip.py |
| **WZ** | wazar/cicada3301 (earlier name Dukotah/cicada3301) | README "current as of 2026-08-31 (Round 25)"; LEDGER.json 156 entries | README.md, liber-primus/LEDGER.json, liber-primus/ELIMINATION-LEDGER.md, research/DEAD_ENDS.md (clone failed at 1.4 GB; files fetched raw) |
| **LZ** | Leo-Y-Zhang/LiberPrimusAnalysis | one session, 2026-09-06/07 | README.md, docs/REPORT.md, docs/FINDINGS.md |
| **here** | this repository | phases 1–3, README §1–§11 | — |

All three attack the same 12,956-rune unsolved stream (WZ and LZ byte-identical; JW differs by 9
runes of transcription lineage). All three report the same 86 doublets. WZ's LEDGER.json status
counts: measured 47, negative 38, audit 23, open 21, partially-run 14, never-run 6, eliminated 5,
superseded 2.

## Status codes

- **C** closed with a positive control (planted key recovered through the same pipeline)
- **c** closed by inference or by a statistic without a planted control
- **~** partly tested (coverage gap stated)
- **–** not tested
- Cells cite the section or ledger id. "skip" means the soft anti-repeat / key-skip rule is modelled
  in the decoder; "rigid" means position-locked decryption, which the rule defeats.

## Family-by-family table

| Family | JW | WZ | LZ | here |
|---|---|---|---|---|
| Monoalphabetic, shifts, Atbash | **C** §3 (87 variants) | **C** ledger A ("periodic 1–40 +Atbash") | **c** IoC flat | **C** ph3 shifts under skip |
| Periodic Vigenère, rigid (no skip) | **C** §3 periodic IoC, crib-drag (18 cribs) | **C** periods 1–40, 7-symbol control | **C** periodic IoC/κ to 300 per section, z 8.5 control | ~ (subsumed by skip decoder, word list only) |
| Single-word Vigenère + skip | **C** §7–§8 Cicada vocab + top-1,200 English + mangled; rank-1 control | **C** LP1-H: 58 themed keys × signs × no-repeat combiner; campaign18 skip-aware | **C** κ-at-period test with skip control (z 5.5 at period 13) | **C** ph3: every solved-text word + headlines, fwd+rev, both F variants, z 10–15 controls |
| Very short keys, exhaustive (len 2–3) | **C** §10, §33 | ~ hand-Vigenère k 4–12 (B2) | – | – |
| **Multi-word phrase / sentence keys + skip (period ≈ 12–60)** | – (word lists; brute stops at len 3) | – (k ≤ 12; notes k ≥ 64 "out of scope") | ~ κ test covers period ≤ 300 only where the skip desync does not smear the lag; control run at period 13 only | – |
| Prime / totient / p+1 streams, offsets, skip | **C** §3, §35 (offsets to 200, 96 % beam) | **C** 1,800 configs: {prime, φ, φ(prime), Fib, golden} × add/sub/Beaufort × strides × offsets 0–39 | **C** 24 sequences × 200 offsets × 2 signs, raw and chain form | **C** ph3: 101 starts, both F variants |
| Fibonacci, Lucas, OEIS, arithmetic progressions | **C** §50: 16 keystreams, 4/4 control | **C** "all Fibonacci-mod-29 seeds" | **C** fib, lucas, tri, π digits, 3301n, … | **C** ph3 Fib/Lucas |
| Position formulas a·n+b, n²+b | ~ §50 (d = 1, 2, 3, 7 only) | ~ cumsums | **C** n, n², n³, triangular | **C** ph3 all a, b |
| Non-additive affine c = a·p + k | **C** §48 all multipliers | **C** LP1-H non-additive combiner | **c** word-level affine | – |
| Solved LP text as running key (all offsets) | **C** §35: 13 streams × 32 offsets × 2 signs, 12/12 control | **C** ledger A, all offsets, both directions, +Atbash; re-run skip-aware | **C** every offset, z 34 control | **C** ph3: 2,977 offsets under skip |
| External texts as running key | **C** §6, §9, §32, §36, §37, §57: KJV, Liber AL, Mabinogion, Blake, Emerson, Rune Poem, Cypherpunk Manifesto, Agrippa, fwd + rev | **C** ≈200 texts skip-aware (campaign18, armada18/19); R26-B 33 mysticism texts partially-run | **C** Emerson, Mabinogion (War and Peace as control) | – |
| Shared keystream between pages / page-on-page keys | **C** §35 (other segments as key), §43 depth test (no power) | **c** "page-on-page keying" in do-not-re-run list | **C** cross-section κ and IoC-of-differences, z 7.8 control | **C** ph1 depth-two scan with permutation null; ph2 unigram detector; ph3 neighbour pages under skip |
| Autokey (plaintext / ciphertext), k-history feedback | **C** §3 primers 1–3 | **C** R12-C1 k = 2..6; Round 11 unbounded feedback | **C** chain + ciphertext autokey lags 1–60, plaintext lags 1–3, all seeds | **C** ph2: identity feedback decrypts flat; fails lag-1 class χ² |
| **Gematria prime-value feedback** (shift by prime of previous rune) | – | **C** Round 22 X4: value / prime-index / totient streams ± sign ± Atbash; Round 11 N5 totient ladder; 48 PT/CT feedback configs | **C** six variants, all seeds, Δc detector | – |
| Ciphertext feedback through a general map π | **C** §11 deterministic bump/nudge ruled out | **C** R18-L2-A-LOCUS: 7 loci, ciphertext locus confirmed; **open** D-04 non-additive coefficient sweep beyond 3 pages | **C** chain with 14 bijections incl. 12 discrete logs | **C** ph2 identity and shifted feedback |
| **Per-page / per-line key resets, page-number-derived keys** | **C** §34: 32 schedules × {prime, φ, DIVINITY, FIRFUMFERENFE} × skip, floor −3.38, 32/32 identifiable | **C** "page-seeded" streams; B3 page-local semantic keys 0 hits / 168k | – (listed as untried) | ~ ph3 pages tested independently with free start (primes, self-key) |
| Keystream offset ≠ 0 | **C** §35 (to 200) | **C** B-02: 4.97 × 10⁸ offsets for derived generators (constant offset only) | **C** 200–300 offsets | **C** 101 prime starts; 2,977 self-key offsets |
| Derived pads: PRNG, hash-CTR, KDF, seeds | **C** §13, §41 (thematic passphrases) | **C** B-04, R16-KDF, R16-PRNG; R25 MT-2³² tail parked at 0.5 % coverage; Marsaglia CDROM never-run | – | – |
| Public pads (blockchain, NIST beacon, RANDOM.ORG, RAND) | – | **C** R17: 1.45 × 10¹⁰ offsets, 0 hits | – | – |
| Transposition, reading order, Hill / digraphic | **C** §61, §62 | **c** doublet-transparent | **c** doublet parity mod 2–8 | – |
| Homophonic-downward substitution | – | **open** D-03 (closed only by bigram-flatness inference) | – | – |
| **Non-English plaintext register** | – (English wordfreq LM) | **C** R24-C1, L7-A: Latin, Greek, Old English, Enochian re-adjudication, but **only of derived-key sweep candidates** | – (flagged as untried) | – (English unigram only) |
| **Lag 2–50 coincidence decay** | **C** §4: differencing restores 3.37 %; lags 2–8 null | **C** R17: lag-2..8 bleed bound < 1.70 % | **C** lags 2, 3 normal; κ lags 1–400 flat | – (lag-1 class χ² only) |
| Mechanism: soft vs hard, resolution, locus, hand vs machine | **C** §11 uniform resolution; §44 p_keep 0.193 | **C** p_keep ≈ 0.18; machine not hand (≥ 0.99 power); ciphertext locus | **c** chain model, EA conjecture | **C** ph2: 20 constructions, 81 % re-draw |
| skip_by_two relation (two key draws per rejection) | – | **C** R24-C2 decoder built; run on PRNG seed slice only | – | – (DP models one draw per skip) |
| Both key signs (c = p + k and c = p − k / Beaufort) | **C** both signs throughout | **C** add / sub / Beaufort | **C** c − K, K − c, c + K | **–** ph3 decrypts P = C − K only |
| Doublet sites real on the page (haplography audit) | **C** §23 second transcription | **C** A-03 crops | **C** crop_doublets.py | – |

## The four questions asked

1. **Feedback through the Gematria prime value of the previous rune.** Closed. LZ ran six
   variants (c ± prime(c_prev), multiplicative, p = c ∓ prime(p_prev), all seeds) with the Δc
   detector that exposes ciphertext autokey at IoC 1.76; WZ ran prime-value, prime-index and totient
   streams over the letter stream with both signs and Atbash (Round 22 X4) and a 48-config PT/CT
   feedback set with f ∈ {mod 29, totient, digit sum}. Our proposed phase 4 item 1 would replicate.
2. **Multi-word phrase keys from the solved text under the skip rule.** Not tested by anyone. JW's
   key space is single words (Cicada vocabulary, top-1,200 English, mangled variants) plus an
   exhaustive brute to length 3; WZ's LP1-H is 58 themed single words and its hand-Vigenère lane
   stops at k = 12; LZ's κ-at-period test is the only coverage of long periods, and its skip
   control was run at period 13, where fewer than one skip falls inside a period. Under the skip
   rule the κ signature at lag T is spread over lags T..T+⌈T·0.028⌉, so for T ≥ 36 it is split
   across two or more lags and the test loses most of its power. Our phase 3 used single words too.
3. **Keys derived from page numbers or section structure.** Closed. JW §34 tested continuous,
   reset-to-0 and page-indexed schedules over four key streams with and without skip, 32/32
   schedules identifiable when planted, best real decode 3.1 below the floor on 10,198 runes;
   per-line resets likewise. WZ's B3 (page-local semantic keys, 168k crib readouts) and
   page-seeded number streams are null. Our phase 3 treats each page independently with a free
   start for primes and the self-key, which covers the "page k starts at an arbitrary offset" case
   for those families.
4. **Lag-2-to-50 coincidence decay** (the Quorum verdict's suggested next question). Closed by all
   three: JW shows first-differencing restores the doublet rate to 3.37 % and equality at lags 2–8
   is null; LZ finds lags 2 and 3 at 3.4 % and κ flat to lag 400; WZ bounds any lag-2..8
   suppression below 1.70 %. The effect is pure lag-1. No decay profile to measure.

## Ranked list: untested under the anti-repeat rule

| # | Family | Why plausible for Cicada | Who has it | Configurations |
|---|---|---|---|---|
| 1 | ~~**Phrase and sentence keys from the book**~~ **DONE, null (phase 4, `results/phase4.md`)**: every 2-, 3- and 4-word contiguous phrase of the solved text and the known headlines, plus whole sentences, forwards and reversed, both signs, both F variants, under skip | Both solved word keys (DIVINITY, FIRFUMFERENFE) were taken from the book's own plaintext (WZ LP1-H recon); the "numbers are the direction / words are the map" hint reads as the book keying itself; longer keys are the smallest escalation from what the author demonstrably did; the one family every ledger stops short of | nobody | solved text ≈ 740 words → ≈ 2,200 phrases + ≈ 150 sentences; × 2 directions × 2 signs × 2 F ≈ 19,000 per page; × 55 pages ≈ **1.0 M tests**; chance max ≈ 5.2σ; our controls sit at 10–15σ |
| 2 | ~~**Both signs for phase 3's families**~~ **DONE, null (phase 4)** (C = K − P and C = P + K read as decryption variants) | Not a new family, but our only asymmetry against the other three, who all ran both signs; closes our own ledger | JW, WZ, LZ have it; we do not | ≈ 2 × 519,200 = **1.04 M tests**, same runtime as phase 3 |
| 3 | **Non-English register for the book families**: rerun phases 3 and item 1 with a Latin and an Old English unigram model inside the decoder | The title is Latin, the alphabet is Anglo-Saxon, the Rune Poem is Old English; LZ measures unsolved word lengths at 4.47 vs 4.03 for the solved English pages; WZ shows a correct non-English key scores as noise under an English model yet re-adjudicated only derived-key candidates, never word, prime or running-key families | nobody for these families | same configuration count as the family, × 2 languages; needs transliteration conventions for each |
| 4 | ~~**skip_by_two for the book families**~~ **DONE, null (phase 7, `results/phase7.md`)**: 2.5 M tests, controls show the single-advance decoder misses half of skip-by-two plants | WZ built and validated the decoder but ran it on 245,975 PRNG seeds only; if the rejection loop was coded as j += 2 every beam-based word/prime/self-key negative (ours included) is blind to it | WZ for PRNG only | our DP needs a second transition type; then phase 3's 4,716 configs again, ≈ **0.5 M tests** |
| 5 | Non-additive ciphertext-feedback coefficient sweep on all 55 pages (WZ D-04) | WZ ran 3 of 55 pages at orders k ≤ 3 and wrote it up as closed; LZ's 14 bijections cover the additive-chain part | WZ partially | small; low prior given LZ |
| 6 | Homophonic-downward substitution (WZ D-03) | closed only by inference from bigram flatness | WZ open | annealing search; low prior: unigram flatness already argues against |

Items 5 and 6 are listed for completeness; the first four are the honest phase 4, in that order.
Item 1 is the only one that is both untested by every ledger and specific to how the author
demonstrably built keys. Items 2 and 4 are instrument completions. Item 3 is the cross-cutting
blind spot all four projects share.

## What this changes in the public picture

Nothing yet. Every family that this repository closed was already closed by at least one of the
three, usually with comparable controls, and the mechanism parameter (81 % here, 81–82 % there)
agrees to within fitting error. The convergence is the result. The list above is what remains
after four independent sweeps, and it is short.

## Field survey (2026-10-23): the three ledgers are not the whole field

GitHub search finds 39 Liber Primus repositories, 21 of them pushed in 2026. The serious ones, by
recency and rigor (READMEs read as data; r/cicada and X could not be read, both block automated
access; the CicadaSolvers Discord is unread by every AI lab including this one):

| Repo | Last push | What it is | Relevance here |
|---|---|---|---|
| **pnotisdev/cicada3301** | 2026-10-24 | Registry-driven workspace: 56 families excluded, 33 partly, 8 open; IoC screens at 10⁹–10¹⁰ decodes with planted controls; a live queue | **Already ran phrase keys**: 1,841 keys ≤ 24 runes (words, phrases, titles, first/last lines, 2014 messages), 8 spellings, both signs, F rule on/off, at the 8 section starts (`solved-phrase-keys`, excluded); 1,940 keywords of length 3–30 under its R4 collision-repair model on all 48 windows (partial). Also all 28 key multipliers and periodic sign templates. Our phase 4 adds only keys > 24 runes, reversed keys, and all 55 pages. |
| **murphyaidanbusiness-ux/liberprimus** | 2026-10-18 | Orchestrated agent campaign, 14 + 14 lanes, all controlled; seven structural constraints; census of 232 community methods (`research/EXHAUSTED.md`: 130 dead by the fingerprint, 21 open-ended, 6 finite partials) | Lane E: plaintext language from word statistics favours English with THE/OF(/TO) absent; Latin 10–30× worse; Old English tested on verse only ("no prose source reachable"); Dutch/Danish not excluded. Names the best-fitting family left: evolving-alphabet walk / Quagmire dodge with skip-on-repeat (Oosterhof), excluded in its odometer form, clock form has no search tool yet. |
| **micheloosterhof/aldegonde** | 2026-10-21 (since 2021) | Classical-crypto library for non-standard alphabets; the walk model, the lag-5 echo, the layout findings | The community member whose findings the October campaign builds on |
| wazar (Dukotah)/cicada3301 | 2026-10-07 | see table above | |
| Leo-Y-Zhang/LiberPrimusAnalysis | 2026-10-02 | see table above | |
| jens-wedin/liber-primus | 2026-08-26 | see table above; HistoCrypt paper drafted, not reported as submitted | |
| TheronEagle/liber-primus-research | 2026-09-30 | AI-assisted log, no solve | cited by the October campaign |
| aergasrg/liber-primus | 2026-09 | Multi-session Claude lab with YAML ledger and backlog | backlog B07 "non-English plaintext scoring" still open there |
| ZzNible/…-findings, Wulfic, Pitchfork-and-Torch, anon5376 | Aug–Sep 2026 | sanitised negative results, trackers, "hypothesis lab, not a solve" | Wulfic retracted its pre-2026-09-29 claims as artifacts |
| relikd/LiberPrayground, Taiiwo/cicada-library, mortlach/RuneDecrypterPrime | long-running | community tooling, transcriptions, the finished 29-rune interrupter DB | infrastructure, not attacks |
| johnvteixido, 2retooz270703 (27×27 grid), vionorromanov ("full decipherment") | 2026 | unverified or crank | ignore |

**What this changes.** Phase 4 was, like phases 2 and 3, mostly a replication: pnotisdev had the
phrase family at the section starts five days earlier. Phase 5's Latin lane has low prior by lane E's
word statistics; its Old English prose lane is a real gap (lane E could not fetch OE prose), and
our own controls show the unigram scorer barely loses power across registers anyway, so the
"English-only blind spot" is a property of quadgram scorers, not of this decoder.

**The actual frontier, as the two most thorough repos state it:** the evolving-alphabet walk in
its clock-dependent form (no working search tool), the lag-5/lag-6 within-word echo (2.5σ, mechanism
unknown), pnotisdev's open items (keyword-mixed outer alphabet, unkeyed insertions and extra key
advance at separators, pointer-direction sign rules, tableau ciphers, drift-tracking keyword decoder),
and the external hunts. Anything else is on a ledger already.

**Rule for further work in this repository:** check `pnotisdev/docs/registry.toml` and
`murphy…/research/EXHAUSTED.md` before any sweep, and prefer contributing a lane to pnotisdev's queue
format over a sixth parallel ledger.

## Added 2026-10-27: two repositories active since the survey, read as data (`external/survey2/`)

| Short name | Repository | Read | What it is | Overlap with this repository |
|---|---|---|---|---|
| **PA** | ToldByNun/Parcae | README at HEAD 2026-10-14 (10 stars) | C++20 toolkit: solved pages frozen as regression oracles, a theory DSL, candidate generation and ranking, optional CUDA; covers Atbash, Vigenère + skips, totient streams as worked examples | Tooling, not a sweep: publishes no ledger of negatives and no planted-control power figures. Nothing here duplicates a lane; its oracle fixtures are a cross-check for our `lp.py` transcription if ever needed. |
| **AP** | MarcelDuSHAmp/atelier-primus | README at HEAD 2026-10-22 (French, "collaboration IA") | Studies the 75 page images, their runes and geometry; 171 notes in 12 families; the current lead derives two Tor v2 onion identifiers from one page image (G032), which the authors state are reproducible but not authenticated and not a decryption | Overlaps §26 (page images). Their angle is extraction of an address from image structure; ours is steganography and glyph-geometry tests against the solved pages. Their 171 negative notes were not read in detail; worth a pass before any further image work. |

Also seen, not entered: murphyaidanbusiness-ux/liberprimus and aergasrg/liber-primus (already in the survey), mak777uh/cicada3301-import (a mirror of WZ), popsumpercs/Liber-Primus-Attack-Pipeline and VinnyMo/cicadaCrypt (small transliteration toolkits, no claims), HhWolfling/Gematria-Primus-Lattice-Resonance (no testable content), invictustitan2/liber-primus-archive (empty README). No repository found claims a solve as of 2026-10-27.

**Note on WZ's never-run R12-C2 corpus (checked 2026-10-27).** Its `fetch.sh` names 23 Project Gutenberg ids and 10 archive.org / globalgrey URLs. Fetched from Gutenberg mirrors, at least five of the ids return other books (71455 "Girart de Nevers", 16929 "Treat 'em Rough", 33443 a Corwin cruise report, 33244 "Maximina", 24459 "The Lost Princess of Oz"), six return nothing, and the archive.org and globalgrey URLs return HTML, not text. The lane was never run and its corpus as scripted could not have been run as described; anyone picking it up must re-source the texts by title.
