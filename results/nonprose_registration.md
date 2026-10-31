# Registration: a model-free structure scorer over the small libraries (blind spot 1), written before any run

Date 2026-10-31 (night). Private-table row A1; `docs/blind-spots.md` §1. Nothing below has been run; the row counts marked
"printed by the instrument" are filled in by the first run and copied here unchanged.

## Question

Every decode lane in this repository scored a candidate plaintext with an English model (unigram, then the rune 5-gram of §27)
or, in §13, with Latin and Old English unigrams. A right key whose plaintext is not prose, a list, numbers in words, digits or
numerals written in runes, a bounded alphabet, a formulaic register, scores as noise under all of them. pnotisdev's engine is an
index-of-coincidence and bigram scorer, language-agnostic by design, but it met only their own streams, on the first 300 runes
of eight sections (§54, §62). This repository's 7,621 book keys (`families.ALLSETS`) and the 3,000 prime streams of §70 have
never met a scorer that does not assume a language. This lane gives them one.

## Scorer

For a decode P of a page, with the ciphertext's word boundaries (word separators `-.&$§`; `/` is a line break, not a boundary):

- **U** = Σ_r n_r², the unigram concentration (the index of coincidence up to normalisation). Rewards any peaked or bounded
  alphabet, whatever the language or register.
- **W** = the number of word tokens of two or more runes whose rune string occurs at least twice on the page. Rewards lists,
  numbers in words, formulae, refrains.
- **G** = the number of rune 3-gram positions (boundaries ignored) whose 3-gram occurs at least twice on the page. Rewards any
  repeated substring: affixes, numerals, repeated tokens split across words.

Each statistic is turned into a z against N0 = 2,000 uniform iid keystreams decoded on the same page under the same F
convention (the null does not depend on the sign). The row's score is **z\* = max(z_U, z_W, z_G)**. The null of z\* is the null
of the maximum of three correlated statistics and is measured, never assumed Gaussian (lesson eight, §70).

**Amendment (2026-10-31, after the instrument's smoke test on a 924-row toy library and before any run on the libraries).**
W and G are counts of rare discrete events on a short page (on 66 runes a repeated word pair has a null mean near 0.05), so
their plain z explodes on a single chance pair: the smoke test's 3,000-draw calibration on the shortest page reached z\* 10.8
and would have set the bar at 12, which no plant on a medium page could reach. W and G therefore enter as **Anscombe-transformed
pair counts**, z = 2(√(x/2 + 3/8) − √(λ + 3/8)) with λ the null mean of x/2 from the N0 draws, which is near N(0, 1) for a
Poisson count and conservative where λ is small; U stays a plain z. The score is still z\* = max of the three, and everything
else below is unchanged. The smoke run's own figures are in `results/nonprose_smoke_*.json` and are not results.

## Decoder, libraries, rows

The plain decoder: every rune keyed, P = C − K (sub), P = C + K (add, as −K under sub), P = K − C (beaufort); F rule off
(every rune keyed) and on (a cipher ᚠ is a plaintext ᚠ that consumes no key). No skip, filler or echo model: §60 measured
what fillers cost a plain decoder, and U is alignment-sensitive from the first skip onward, so a skip rule is outside this lane
and is said so.

Rows per sign: the 7,621 keys of `families.ALLSETS` for that sign, every key of period p ≤ 64 at all p rolls (the book's
convention is roll 0, the key starting with the page; the rolls are the cheap generalisation), aperiodic keys at offset 0 as
before, duplicates removed; plus the 3,000 prime streams of §70 (`e56_lattice.prime_library`). M rows per (sign, F):
printed by the instrument. Pages: the 55 unsolved pages, and as positive controls the two solved pages whose keys are in
the library, read from the master transcription: the WELCOME page (chunks 2 and 3, DIVINITY, F rule on) and the KOAN 1 page
(FIRFUMFERENFE, F rule on; its chunk is found by decrypting and matching the published plaintext, and the chunk number is
recorded).

## Nulls and the bar

1. **Calibration null, before any library row is read**: 200,000 uniform keystreams on the longest and the shortest unsolved
   page, each F, z\* computed with the N0 moments. Its maximum and its tail counts at z\* ≥ 4, 5, 6, 7 are recorded.
2. **Bar**: max(7.0, calibration maximum + 1.0), rounded up to the next 0.5. Fixed before the first library row is read and
   written into the results file.
3. **Library-sized null** per (page, F): Nbig = M uniform keystreams, z\* as above; its maximum and tail counts recorded.
4. **Hit**: a library row with z\* ≥ bar, rank 1 in its (sign, F) library on that page, and z\* ≥ the library-sized null's
   maximum + 1.0. **Listed** (not a hit, reported for the tail comparison): the library's top row exceeds the library-sized
   null's maximum.

## Plants (power), before the pages

Payloads of about a page (the length of a randomly drawn unsolved page), with their own word structure, enciphered under a
key drawn from the library's periodic word keys and prime streams at a random roll, under each sign, F rule off; 10
replicates per (class, sign); class P1 also 10 replicates with the F rule on. Recovered = z\* ≥ bar and rank 1 in the
(sign, F) library.

- **P0** uniform random runes with the page's word lengths: the negative control, the limit no scorer passes.
- **P1** English prose (`data/corpus/corpus.json`, a random book and start).
- **P2** Latin prose (`data/raw/corpora/latin_corpus.txt`, random start, this repository's transliteration).
- **P3** the primes in English words from a random start (TWO THREE FIVE SEVEN ELEVEN THIRTEEN …), one word per number word.
- **P4** the primes in decimal from a random start, digit d written as rune d (ᚠ=0 … ᛁ=9), one word per prime.
- **P5** additive Gematria numerals: the natural numbers from a random start, each written greedily as the runes whose prime
  values sum to it (largest value first), one word per number.

## Predictions

- **N1** (power): P1–P5 recovered in ≥ 90 % of replicates per class at F off; P0 in 0 %.
- **N2** (positive controls on real text): the WELCOME page under the sub library with the F rule on puts DIVINITY roll 0 at
  rank 1 with z\* ≥ bar; the KOAN 1 page likewise for FIRFUMFERENFE.
- **N3** (the pages): no hit in any of the 55 × 3 × 2 cells. Listed cells: about half of 330 (binomial 165 ± 9) if all null.
- **N4** (tail): pooled over pages and F, the library's rate of rows at z\* ≥ 5 is within a factor of 2 of the library-sized
  null's rate.

Expected: all four hold. **Falsifier**: a hit whose decode shows a describable structure (the output lists the repeated
words and 3-grams of every listed row); it is then checked on the adjacent pages under the same key before anything is claimed.

**Amendment 2 (2026-10-31, after the first run of every stage above; recorded before the amended stage is run).** The positive
control could not be run as registered: the matcher found no solved page, because the book's ᚠ convention is not the one the
plain decoder forces. On the WELCOME page (chunk 2, DIVINITY) a plaintext ᚠ is written unkeyed and consumes no key symbol, *and*
a keyed rune may still encipher to ᚠ (14 cipher ᚠ, 7 of them literal); the key continues into chunk 3 without restarting.
Under that convention a cipher ᚠ is ambiguous, so the plain decoder's F-off cells are right only up to the first literal ᚠ and
its F-on cells only up to the first keyed ᚠ. Measured before this amendment, with the registered scorer: DIVINITY roll 0 on
chunk 2 ranks 827 (F off, z\* 4.5) and 17,054 (F on, z\* 1.0); the chunks' top rows are the solved plaintext used as a running
key (`self running key plaintext@184`, z\* 165; `@435`, z\* 178), which is the scorer finding the period-8 key itself as
structure. **N2 fails as registered**, by instrument, and the first run's page results (0 hits in 330 cells, 143 listed) stand.

The amended stage (`STAGE=xrule`): a third convention, the book's, with a **greedy branch decoder**: at every cipher ᚠ the
two branches (literal ᚠ, key not consumed | keyed rune) are decoded up to the next ᚠ and the branch whose segment is likelier
under the adaptive unigram of that row's own decoded prefix (KT estimator, prior 0.5) is kept; no language model, no beam.
Nulls, bar and the three statistics as above. Registered: **N1′** P1 and P4 plants enciphered under the book's convention
are recovered (z\* ≥ bar, rank 1) in ≥ 90 % of replicates per class (P4 because a digit 0 is a rune ᚠ, the worst case);
**N2′** WELCOME chunk 2 under the sub library puts DIVINITY roll 0 at rank 1 with z\* ≥ bar (chunk 3 is reported at its best
roll, since the key does not restart there); **N3′** no hit in the 55 × 3 cells. Expected: all three hold.

## What a null means and does not mean

A null closes "a library key is right and the plaintext is not prose" for the plain decoder at the plants' power: book keys
and prime streams, three signs, two F conventions, every roll. It says nothing about a key outside these libraries, about a
skip, filler or echo rule on top of a library key (§60, §61, §70), or about the iid-key world of E56w+n (§58). pnotisdev's
language-agnostic screen of their own streams stands as the other half of this blind spot's closure and is not repeated here.

## Reproduce

`.venv/bin/python -I src/nonprose_lane.py` (stages: `calib`, `plants`, `controls`, `pages`, `merge` via `STAGE=`).
