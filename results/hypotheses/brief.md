# Evidence brief: the unsolved pages of Cicada 3301's Liber Primus (prepared 2026-10-26)

## The object
56 unsolved pages (55 with runes), 12,956 runes in the 29-rune Gematria Primus alphabet (index 0..28 = F U TH O R C G W H N I J
EO P X S T B E M L NG OE D A AE Y IA EA; each rune also carries a prime value F=2, U=3, TH=5, ... EA=109). Page lengths
66-277 runes, median 263. Word, line and paragraph separators are known from the transcription.

## The four statistics any construction must reproduce (pooled over the 55 pages)
| statistic | pages | iid uniform keystream would give |
|---|---|---|
| doubled runes (C_i == C_(i-1)) among 12,901 adjacent pairs | **86** | 445 ± 20 (z = −17) |
| chi-square of the other 28 lag-1 difference classes (27 dof) | **42** | ≈ 27 |
| unigram chi-square over the 29 runes (28 dof) | **26** | ≈ 28 |
| index of coincidence | **0.0345** | 0.0345 |
So: the ciphertext is flat in every respect except that a rune almost never repeats its predecessor, about one time in five
as often as chance. The deficit is the same inside words and across word boundaries, and the same on every page (no page
below −2σ). Lags 2 and beyond are null (no decay profile). The gate accepts a construction only if all four statistics fall
within 3 sd of the construction's own Monte Carlo distribution (200 replicates of real solved-page English cut to the real page lengths).
Other established facts: no two pages share a keystream at any alignment within ±200 runes (pooled test null at 135σ sensitivity
for full reuse); no within-page period 2-200; the solved pages' ciphertext sits at the normal doublet rate, so the deficit belongs
to the unsolved pages' cipher, not to the plaintext or the transcription.

## What the book itself did on the solved pages (the only ground truth about the author's methods)
Published keys per section (rtkd/iddqd keys file; '+ 0.k' = section k):
+ 0.0	Substitution. Invert Gematria.
+ 0.1	Polyalphabetic Substitution. Clear text F is not encrypted. Key: divinity (23,10,1,10,9,10,16,26)
+ 0.2	Substitution.
+ 0.3	Substitution. Invert Gematria. Key: 3
+ 0.4	Substitution.
+ 0.5	Polyalphabetic Substitution. Clear text F is not encrypted. Key: firfumferenfe (0,10,4,0,1,19,0,18,4,18,9,0,18)
+ 0.6	Substitution.
+ 0.16	Polyalphabetic Substitution. Clear text F is not encrypted. Key: f(n)=phi(n) where n = stream of prime numbers.
+ 0.17	Substitution.
Both word keys (DIVINITY, FIRFUMFERENFE) are words of the book's own plaintext. The F rule ("clear text F is not encrypted",
consumes no key symbol) is the author's own skip rule. The totient stream is phi(p_n) over the primes. One page (the 'Parable')
is a plain Gematria substitution; the last solved page uses shift 3 then Atbash. The author uses primes, totients, Gematria prime
values, 3301, and the book's own words; the community reads the hint "numbers are the direction, words are the map" as the book keying itself.

## Which constructions reproduce the statistics (phase 2, src/doublets.py, 20 constructions, same gate as this loop)
# Which constructions reproduce the signature?

Observed on the unsolved pages: doublets 86, non-zero lag-1 class chi² 42 (27 dof), unigram chi² 26 (28 dof), IC 0.0345.
Each construction: 200 replicates of solved-page plaintext cut into the 55 real page lengths. z = (observed − construction mean) / construction sd;
a construction is consistent with the pages when every |z| is small. Doublets is the discriminating column.

| construction | doublets (mean ± sd) | z | lag-1 class chi² | z | unigram chi² | z | IC | z | verdict |
|---|---|---|---|---|---|---|---|---|---|
| independent uniform keystream (control) | 446 ± 20 | -18.1 | 27 | +1.9 | 28 | -0.2 | 0.0345 | -0.2 | ruled out |
| running key from English (solved text, random offset) | 465 ± 22 | -17.4 | 38 | +0.4 | 739 | -13.1 | 0.0364 | -13.1 | ruled out |
| hand pad: uniform key that never repeats a symbol | 448 ± 20 | -17.9 | 30 | +1.5 | 28 | -0.2 | 0.0345 | -0.2 | ruled out |
| plaintext autokey, lag 1 | 698 ± 31 | -19.6 | 1136 | -12.3 | 1977 | -15.7 | 0.0397 | -15.7 | ruled out |
| plaintext autokey, lag 2 | 481 ± 21 | -18.5 | 230 | -6.8 | 1355 | -17.5 | 0.0380 | -17.5 | ruled out |
| plaintext autokey, lag 5 | 522 ± 29 | -14.9 | 309 | -6.1 | 930 | -18.8 | 0.0369 | -18.8 | ruled out |
| ciphertext autokey, lag 1 | 207 ± 14 | -8.9 | 9903 | -56.8 | 29 | -0.3 | 0.0345 | -0.3 | ruled out |
| ciphertext autokey, lag 2 | 445 ± 23 | -15.6 | 25 | +2.4 | 25 | +0.3 | 0.0345 | +0.3 | ruled out |
| ciphertext autokey, lag 5 | 443 ± 20 | -17.9 | 27 | +1.9 | 27 | -0.1 | 0.0345 | -0.1 | ruled out |
| ciphertext autokey, lag 1, offset so doublet⇔EA | 86 ± 9 | -0.1 | 9629 | -66.1 | 24 | +0.3 | 0.0345 | +0.3 | matches doublets, fails lag-1 structure |
| ciphertext autokey, lag 1, offset so doublet⇔EO (never) | 0 ± 0 | +86000000000.0 | 9400 | -54.5 | 24 | +0.3 | 0.0345 | +0.3 | ruled out |
| Vigenère key 8, step key when a doublet would form | 15 ± 6 | +12.2 | 32 | +1.2 | 49 | -1.5 | 0.0345 | -1.5 | ruled out |
| book Vigenère DIVINITY with F-skip | 506 ± 21 | -20.4 | 193 | -5.3 | 2583 | -27.7 | 0.0413 | -27.7 | ruled out |
| book totient prime stream with F-skip | 430 ± 22 | -15.6 | 197 | -5.1 | 144 | -4.9 | 0.0348 | -4.9 | ruled out |
| uniform key + anti-doublet rule (always +1) | 0 ± 0 | +86000000000.0 | 438 | -7.0 | 26 | +0.0 | 0.0345 | +0.0 | ruled out |
| uniform key + anti-doublet rule (81% of the time) | 84 ± 9 | +0.2 | 299 | -5.8 | 27 | -0.0 | 0.0345 | -0.0 | matches doublets, fails lag-1 structure |
| keystream re-rolled until no doublet (hard rule) | 0 ± 0 | +86000000000.0 | 27 | +2.0 | 26 | +0.1 | 0.0345 | +0.1 | ruled out |
| keystream re-rolled when it would repeat, 81% of the time (soft rule) | 87 ± 10 | -0.1 | 27 | +1.7 | 28 | -0.2 | 0.0345 | -0.2 | **consistent on all four** |
| keystream re-rolled when it would repeat, 70% of the time | 137 ± 12 | -4.2 | 26 | +2.1 | 27 | -0.0 | 0.0345 | -0.0 | ruled out |
| keystream re-rolled when it would repeat, 90% of the time | 46 ± 6 | +6.6 | 27 | +2.2 | 27 | -0.1 | 0.0345 | -0.1 | ruled out |

## Reading

- Anything additive with a key independent of the text (uniform, running key, hand pad, the book's own Vigenère and totient streams) gives
  doublets at the uniform rate: a doublet needs P_i − P_{i+1} ≡ K_{i+1} − K_i, and an independent key hits that one time in 29 whatever it does.
- Autokeys tie the key to the text and change the doublet rate, but not downward enough (plaintext autokey raises it; ciphertext autokey makes a
  doublet a plaintext F, about 1.6%) and they leave a non-flat lag-1 structure that the pages do not show.
- A ciphertext-feedback rule with a chosen offset can hit any doublet rate, including the observed one, but then the lag-1 difference stream is
  the plaintext shifted, with IC 0.06, and the pages' lag-1 stream is flat (IC 0.0353). Ruled out on that column.
- What matches is a key that is otherwise random and is rejected, most of the time, exactly when it would repeat the previous rune: a soft
  anti-repeat rule applied to about four doublets in five. A hard rule (never repeat) overshoots to zero doublets; the pages have 86.


## What has already been swept, with planted controls (this repository's phases 3-7 and five public 2026 labs)
Phase 3: shifts, every solved-text word (fwd/rev), primes p/p−1/p+1 at 101 starts, Fibonacci, Lucas, a·n+b and n²+b, the solved
plaintext as running key at all 2,977 offsets, neighbour pages as keys; each with/without the F rule under the skip-on-repeat rule
(a key symbol that would make C repeat is skipped, p ≈ 0.81 modelled). 519,200 tests, null; planted keys recovered at z 10-15.
Phase 4: every 2-, 3-, 4-word phrase and every line of the solved text, fwd/rev, under skip, all three signs (C = P+K, P−K, K−P),
plus phase 3's families under the two other signs. 1,996,170 tests, null; controls z 10.6-16.3.
Phase 5: phases 3-4 rescored with Latin and Old English unigram models. 5,029,860 tests, null; the English scorer loses little power on either.
Phase 6: extra key advance at word/line starts and unencrypted null runes at word edges (pnotisdev's open lane), over the same
families. 10,059,720 tests, null; controls z 7-15.
Phase 7 (RUNNING NOW): the same families with wazar's skip-by-two rejection (a rejection discards two key symbols).
Also measured here: a lag-5/6 within-word echo reported elsewhere does not replicate (chance at one of twelve lags).
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



MENU (the only constructions the gate can execute; every proposal must be assembled from it)

key_source.type, one of ['uniform', 'lcg', 'prime', 'totient', 'prime_plus1', 'prime_gap', 'fibonacci', 'lucas', 'position', 'word', 'running_text', 'cipher_feedback', 'plain_feedback']:
  uniform        iid uniform key symbols (a secret pad; any unpublished pad or PRNG looks like this to the gate)
  lcg            x_(n+1) = (a*x_n + c) mod modulus, random seed per page, key = x mod 29        [a, c, modulus]
  prime          p_(n+offset) mod 29;  totient: p-1;  prime_plus1: p+1;  prime_gap: p_(n+1)-p_n   [offset]
  fibonacci      F_(n+offset) mod 29;  lucas likewise                                            [offset]
  position       (a*n^2 + b*n + c) mod 29                                                        [a, b, c]
  word           periodic key: the runes of `text` (English spelled with the book's rules, e.g. "DIVINITY",
                 a phrase, a sentence) or, if text is "", a random key of length `period`          [text | period]
  running_text   the solved pages' own plaintext from a random offset (any English running key looks like this)
  cipher_feedback  K_i = map(C_(i-lag)) (+ base stream symbol if base != none), random seed for i < lag   [lag, map, a, b, base]
  plain_feedback   K_i = map(P_(i-lag)) (+ base stream symbol if base != none)                           [lag, map, a, b, base]
key_source.map (feedback only), one of ['identity', 'atbash', 'shift', 'affine', 'prime_value', 'totient_value', 'square', 'random_bijection']: identity x; atbash 28-x; shift x+b; affine a*x+b;
  prime_value = Gematria Primus prime of the rune (F=2, U=3, TH=5, ...) mod 29; totient_value = that prime - 1;
  square x^2; random_bijection = a fixed random permutation of the 29 runes.
key_source.base (feedback only), one of ['none', 'uniform', 'lcg', 'prime', 'totient', 'prime_plus1', 'fibonacci', 'lucas', 'position', 'word', 'running_text']: a deterministic or random stream added to the feedback term.

combine.rule, one of ['add', 'sub', 'beaufort', 'affine']:  add C = P + K;  sub C = P - K;  beaufort C = K - P;
  affine C = m*P + K with m from combine.multiplier_source in ['const', 'position', 'key2']:
  const (m = combine.multiplier, 1..28), position (m_i = ((a*i + b) mod 28) + 1), key2 (a second secret uniform stream in 1..28).

repeat_rule.rule, one of ['none', 'redraw', 'skip', 'bump'], applied when the rune at `target` would repeat its predecessor
  (target in ['cipher', 'key', 'plain']: cipher = C_i == C_(i-1), the observed property; key = K_j == K_(j-1), a pad that never repeats;
  plain = P_i == P_(i-1)), each time with probability p (1.0 = always):
  none; redraw = draw the next key symbol instead (on a deterministic stream this is the same as skip k=1; on a
  feedback-only key it is a fresh uniform symbol); skip = advance the key index by k; bump = add delta to C_i.

f_rule, one of ['none', 'literal_f', 'literal_f_consumes']: none; literal_f = a plaintext F is written unencrypted and consumes no key symbol
  (the book's published rule); literal_f_consumes = written unencrypted but the key symbol is still consumed.

Things the gate cannot see and you should not propose: a fixed substitution applied before or after (it does not
change any of the four statistics), transposition, nulls at word edges (phase 6), which text an external running key
comes from (all English running keys look alike), the seed of a pad (all pads look like `uniform`).
