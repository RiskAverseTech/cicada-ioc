# Registration: the last three rows of the clue table, written before any run

Date 2026-11-01 (afternoon, EDT). After §78, `docs/hints-coverage.md` leaves three readings unrun: the totient as a function
of the words' numbers, a key or switch driven by the lines or the layout, and a key spent from outside the text. The third is
not a reading that can be run: it is the running-key and library world, closed at the scale of §9, §25, §40, §54, §62 and §76,
and beyond that scale it is key material nobody outside holds; it is recorded here as such and not run. The two that can be run
are registered below as instruments T and N, built on §78's harness (the filler-placing beam decoder first, §73's bands second).
A third measurement, G, is registered ahead of them because it is cheaper and bears on the standing of E56w+n itself: whether
the gate that decides which words echo is a property of the word. Nothing below has been run.

## G. The echo gate as a property of the word (`src/gate_property.py`, `results/gate_property.md`)

**Why.** E56w+n (§58) has one part that is random by construction: each word echoes with probability r = 0.5
(`mechanism_lane.simulate`, a per-word draw). A designer who did it by hand did not toss a coin per word; if the rule is real, the
echo words are picked by something about the word. §42 found the lag-5 echo not tied to word position and under-using six-rune
words, and §47 named the gate's nature as the open question before a decoder was built. This is the direct measurement.

**Method.** The 55 pages' words with their within-word lag-5 equality sites and lag-6 affine sites (`24 − 2c`), as §42 counts
them. For each word long enough to host a site (six runes or more for lag 5, seven or more for lag 6), ten properties, each
two- or three-valued: first rune a vowel; first rune at or above S in Gematria order; last rune a vowel; Gematria sum even;
Gematria sum mod 3; index sum below 15 mod 29; word index on the page even; the word starts a line, ends a line, or neither;
the word crosses a line end; the word is in the first or second half of the section. The statistic per property is the
chi-square of site-carrying against the property, **stratified by exact word length** (longer words host more pairs, the
confound the second review named in §42), summed over strata; the null is 2,000 permutations of the site labels within each
exact-length stratum; the family-wise level is the permutation distribution of the largest statistic over the ten properties.
Lag-5 sites and lag-6 sites are tested separately and pooled.

**Power, measured before the check.** Synthetic site labels drawn on the real words with the same per-length counts, where one
property doubles or triples the odds of carrying a site (odds ratio 2 and 3), 200 draws each: the share of draws in which the
family-wise p falls below 0.05 is the instrument's power at those effect sizes and is reported beside the result.

**Predictions.** **G1** no property reaches family-wise p < 0.05 for either echo or pooled. **G2** the power at odds ratio 3 is
at least 0.8 for the pooled test (if it is not, G1's null is reported as weak and the effect sizes the test can see are stated).
Expected: G1 holds. If G1 fails, the property is reported first, the gate in E56w+n is made deterministic on it, and §58's bands
are rerun with that gate before anything else is written.

## T. The totient as a function of the words' numbers (`src/totient_lane.py`, `results/totient.md`)

**Why.** "The totient function is sacred." Prime and totient *sequences* are run at every start (§9, §70, and pnotisdev's
`sacred*` rows); the totient as a *function applied to the book's own numbers* is not. The warning page gives every word a
number, its Gematria sum. This instrument keys each word, or each rune, by a totient of a number the text itself supplies.

**The family.** Numbers n: *prevword*, the Gematria (prime-value) sum of the previous plaintext word (the first word takes the
primer 0); *selfword*, the Gematria sum of the current *cipher* word (keyless, the decoder sees it); *running*, the Gematria sum
of every plaintext rune written on the page so far, read per rune. Functions f: φ(n) mod 29; φ(n) mod 28 + 1; (n − φ(n)) mod
29, the count of non-coprime residues; φ(φ(n)) mod 29; with φ(0) = 0 and φ(1) = 1. Applied as the key of every rune of the word
(prevword, selfword) or of the rune (running), under add, sub and beaufort. 3 × 4 × 3 = **36 members** × fillers {0, 0.40} ×
repair {none, redraw} × literal ᚠ {off, on} = **288 procedures**, 144 decoders, on §78's skeleton.

**Part B first.** §78's beam decoder unchanged (per-word filler hypotheses, the §59 prior, a filler paying log 1/28, the 5-gram
score, beam 8); chance level 200 uniform page sets... the 144 decoders are few, so every decoder is run on 20 uniform page sets
and the chance level is the largest median and the largest single page over those 2,880 decoder–set pairs, recorded before any
page is read. Four plants: prevword φ sub and selfword (n − φ) beaufort without fillers; running φ add and prevword φ(φ) sub
with fillers at 0.40; each decoded by all 144 decoders.

**Part A second.** §73's bands, 20 replicates, candidates and S-admissible members, 200-replicate confirmation.

**Predictions.** **T1** the four plants read at rank 1 of 144 at median page z5 ≥ 30, the filler plants' fillers placed within
20 %. **T2** no page read: largest median within 1.0 of the chance maximum median, largest page within 1.0 of the chance maximum
page. **T3** no S-admissible member. **T4** no candidate. Expected: all hold.

## N. Lines and layout as the key's unit or switch (`src/behaviours_lane.py` with `FAMILY=line`, `results/behaviours_line.md`)

**Why.** The transcription marks 617 line ends on the 55 pages and 452 of them fall inside a word (§42; `src/edges.py`), so the
line is a typographic unit, not a unit of the text (§65). A key that resets at the line, or a switch that reads the line, would
be a design laid against the text's grain, which is why this row's prior is low; it is run because it is the one layout reading
left and because the images, not the words, are what the solver is handed.

**The family.** §78's three behaviours (spend from the text, hold, adhere) with two new switch states, *line* (the line's index
on the page mod 3) and *lpos* (the position in the line mod 3), under the six assignments, two spend readings and three signs
(72 members); and §77's rune autokey at lag 1, plaintext- or cipher-sourced, with the primer restored at every line start
(*line-reset*) under three signs (6 members). 78 members × fillers × repair × literal ᚠ = **624 procedures**, 312 decoders. The
line structure is the pages' own; the generator lays its plaintext into the pages' rune counts and takes each page's line
boundaries as given.

**Part B first, Part A second**, as T, with §78's chance stage (200 random decoders on uniform page sets) and four plants: line
s/h/a lag sub and lpos a/h/s pointer beaufort without fillers; line-reset plaintext autokey add and lpos s/a/h lag sub with
fillers at 0.40; each decoded by its own decoder and 100 others.

**Predictions.** **N1** the four plants read at rank 1 of 101 at median page z5 ≥ 30, fillers within 20 %. **N2** no page read
(§78's chance rule). **N3** no S-admissible member. **N4** no candidate. Expected: all hold.

## What a null across the three means

That the echo gate is not visibly a property of the word at the odds ratios the test can see; that the totient of the book's own
numbers, as the key of the word or the rune, neither reads a page nor leaves the pages' footprints; and that neither the line
as the key's unit nor the line as its switch does either. With §77 and §78 that closes the clue table's unrun column as written
on 2026-10-31, and the remaining mass of the private odds sits in designs not yet named rather than in readings of the
creators' sentences. Cost: G an hour; T and N half a day each to build and under an hour each to run.

## Reproduce

`.venv/bin/python -I src/gate_property.py`; `STAGE=plants|chance|decode|screen|confirm|merge .venv/bin/python -I src/totient_lane.py`;
`FAMILY=line STAGE=… .venv/bin/python -I src/behaviours_lane.py`.

## Amendment to T (2026-11-01, afternoon, at build time and before any run)

The *selfword* source as written, the Gematria sum of the current cipher word, is circular for the encipherer: the cipher runes
depend on the key that depends on them. It is replaced by *prevcipher*, the Gematria sum of the previous cipher word (the
decoder sees it; the first word takes 0), and a fourth source is added for symmetry, *runcipher*, the Gematria sum of every
cipher rune written on the page so far, read per rune. Sources are therefore prevword (plaintext), prevcipher, running
(plaintext) and runcipher: 4 × 4 functions × 3 signs = **48 members**, **384 procedures**, 192 decoders; the chance level is
every decoder on 20 uniform page sets (3,840 decoder–set pairs). The second plant becomes prevcipher (n − φ) beaufort without
fillers. T1–T4 are otherwise unchanged.

## Note on N (2026-11-01, at build time, before its run)

N is built as its own file, `src/line_lane.py`, rather than as a `FAMILY` switch inside `src/behaviours_lane.py`, so that §78's
lane stays as published; the family, plants and rules are as registered. Exact inversion holds for all 156 member × literal-ᚠ
settings; the beam places 77 of 80 and 70 of 80 planted fillers on the two filler plants in the smoke test, at rune accuracy
0.98–0.99.
