# Registration: one hand procedure as the cipher (the generator search of blind spot 4), written before any run

Date 2026-11-01 (morning). Private-table row A5; `docs/blind-spots.md` §4; Quorum panel of §71, third recommendation.
Nothing below has been run.

## Question

E56w+n (§58) reproduces every pre-registered band but the S count with four parts fitted one at a time: a gated echo in half
the words, a filler in 40 % of words, a spend repair at q 0.81, an iid key. A designer who produced the pages by hand did one
thing, probably with a table. This lane asks whether a single procedure, with no key and at most two stated parameters, leaves
all of the stream's footprints at once: the adjacent-repeat deficit, the within-word lag-5 equality and its S share, the lag-6
affine relation, the long words, and a flat rune distribution. A procedure whose state is the previous cipher rune needs no key,
so it is also a deterministic decoder of every page; the lane therefore runs each procedure both as a generator against the
bands and as a decoder against the pages.

## The family (enumerated before the run; nothing is added after a row is read)

A procedure writes cipher rune c_i from the plaintext rune p_i and a state s_i:

- **Table** T(s, p), a Latin square on the 29 runes in Gematria order, from these forms (k = 0 … 28 throughout):
  additive c = s + p + k; subtractive c = s − p + k; reversed c = p − s + k; multiplied c = a·s + p + k for a ∈ {2, −2, 3, −3}
  (174 tables); and four **grid tables**: the runes laid in a 5 × 6 grid in Gematria order with one dead cell (row-major or
  column-major, dead cell first or last), c = the rune at the cell-wise sum of s's and p's grid coordinates, stepping once more
  in reading order when the sum lands on the dead cell (4 tables). 178 tables.
- **State**: the previous cipher rune (c1); the previous plaintext rune (p1); the cipher rune five back in the word (c5w) or six
  back (c6w), the previous cipher rune when the word is shorter; the running sum of the word's previous cipher runes (csum).
  Five states.
- **Reset**: the state starts at ᚠ at the top of every page; at a word start it either restarts at ᚠ (word) or carries over (none).
- **Repeat rule**: none; redraw (if c equals the previous written rune, apply the table once more with the new state);
  exclude (the row for state s is read with s removed, 28 symbols, the plaintext index taken modulo 28). Three rules.
- **Fillers**: none; the §59 form (one extra rune, uniform and unequal to its left neighbour, at a uniform slot in 40 % of
  words of two or more runes, written and state-updating like any rune). Two settings.
- **Literal ᚠ**: off; on (a plaintext ᚠ is written as ᚠ, and a written ᚠ, literal or produced by the table, does not update the state; the book's rule made exact for a decoder that sees only the ciphertext). Two settings.

178 × 5 × 2 × 3 × 2 × 2 = **21,360 procedures**, with k and the filler rate the only parameters, both enumerated, not fitted.

## Part A, the generator test

Plaintext as in §47: Emerson's Essays in rune spelling, cut into the 55 pages' exact rune counts with its own words, a fresh
start per replicate. Statistics, `mechanism_lane.measure` unchanged: D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq, U,
plus two word-length bands from §55: W2 (share of two-rune cipher words; LP2 0.159) and WM (mean cipher word length; LP2 4.42).
Screen: 20 replicates per procedure, z of LP2's value against the replicates; **candidate** = every judged statistic within
|z| < 3 (the §47 criterion; L6best not judged). Confirm: every candidate rerun at 200 replicates; **survivor** = still within
|z| < 3 on every statistic. Reference rows reported whatever they do: additive k = 0 with state c1, no rule, no fillers (the
plain cipher-feedback chain), and the same with the exclude rule.

## Part B, the decoder test

Every procedure with a cipher state (c1, c5w, c6w, csum: 17,088 procedures) inverts from the ciphertext alone,
p_i = T_s⁻¹(c_i), with fillers ignored (a filler-bearing survivor is decoded without its fillers and said so). Procedures with
state p1 invert given the first plaintext rune of each reset unit; all 29 starts are tried and the best kept, which is a
29-fold look-elsewhere per unit and is reported as such. Each decode of each of the 55 pages is scored by the rune 5-gram
z of §27 against 2,000 uniform pages of the same length and by the §72 model-free z\*. **Hit** = a procedure whose median
page 5-gram z over the 55 pages is ≥ 6 and whose best page is ≥ 10 and reads; the family-wide chance maximum of the median
is estimated by decoding 200 uniform random page sets under 200 random procedures and is recorded before any page row is read.

## Predictions

- **H1** (sanity): the plain additive chain (k = 0, c1, no rule, no fillers) fails D: it doubles exactly when p = ᚠ, about
  300 doublets against 86.
- **H2**: fewer than 1 % of the family are candidates at 20 replicates (fewer than 214).
- **H3**: no procedure without fillers meets W2 and WM (English word lengths are the pages' word lengths only with insertions,
  §55), so every candidate carries the filler setting or fails those two bands; this is recorded as a check of the band set, not
  of the cipher.
- **H4**: no survivor at 200 replicates. If one exists, its decode under Part B is the test that matters and is reported first.
- **H5**: no Part B hit. The largest median page z over 21,360 procedures is within 1.0 of the recorded chance maximum.

Expected: H1, H2, H3 hold, H4 and H5 hold (null). **Falsifier**: a Part B hit, or a survivor whose decode reads on any page.

## What a null means

That no procedure of this family, one table and one state rule with at most the enumerated parameters, leaves the pages'
footprints, and that none decodes the pages. It does not cover tables not built from the Gematria order (a keyword-mixed
table is a key, §32), states reaching further back than one word, or plaintext that is not English prose (blind spot 1; the
model-free z\* in Part B sees structure of any kind in the decode and is the partial cover). Cost: the screen is about an hour
on eight shards; the registration is the hour before it.

## Reproduce

`.venv/bin/python -I src/hand_procedure_lane.py` with `STAGE=chance|screen|confirm|decode|merge`, `SHARD`/`NSHARD` on the screen
and decode stages.
