# Registration: the 2016 sentence read as map, road and direction (two instruments), written before any run

Date 2026-10-31 (afternoon, EDT). Companion to `docs/hints-coverage.md`, which is the coverage map this registration acts on.
Nothing below has been run; C11 is running and these two lanes start when it ends.

## Why

*Liber Primus is the way. Its words are the map, their meaning is the road, and their numbers are the direction* (2016,
signed). The field and this repository have read that literally for a decade: words as key text, numbers as key sequences,
null at published scale. Three readings between its words are unrun: the words *locate* (a map is looked up), the
plaintext's instructions *name operations*, and the numbers are *directions* (shifts, steps, offsets) rather than values.
The warning page fixes what "their numbers" means: the message is in "the words or their numbers", so every word carries a
number, its Gematria sum. The three behaviours of the circumference (consumption, preservation, adherence) name the three
repair modes §47 and §58 fitted separately: spend, hold, copy. "Command your own self" names an autokey. "The I is the
voice of the circumference" marks a rune, as the lag-5 echo marks S. These are the specific predictions the two instruments
test. [inferred — `docs/hints-coverage.md`]

## Instrument 1: hand procedures, second family (`src/hand_procedure_lane.py`, `FAMILY=2`)

Everything of §73's harness (generator against the thirteen bands at 20 replicates on shared layouts, candidate at |z| < 3 on
all, 200-replicate confirmation; every procedure also a keyless decoder of the 55 pages scored by the 5-gram z and the §72 z\*)
with these additions, each enumerated, nothing fitted:

- **Value-built tables** (the name is not the thing). With v(r) the prime value of rune r and r(x) the rune at index x:
  c = r((v(s) + v(p)) mod 29), r((v(s) − v(p)) mod 29), r((v(p) − v(s)) mod 29), r((v(s)·v(p)) mod 29); the same four with
  the totient of the state, φ(v(s)) = v(s) − 1; and the same four with the sum reduced to the nearest prime value at or below
  it and that rune taken (the "nearest sacred number" map). Twelve tables, each at the 29 constant shifts k: 348 tables, run
  with §73's five states, two resets, three repeat rules, two filler settings and two ᚠ settings (41,760 procedures).
- **Marker rules** (the I is the voice; S carries the echo). On writing S, or on writing I: the state resets to ᚠ; or the
  table is read reversed (p → 28 − p) until the next marker; or the next rune is copied from five back in the word (the echo
  as a marker's effect). Six rules, over the 207 index tables and the 12 value tables at k = 0, states c1 and c6w, reset none,
  both filler settings, ᚠ off (5,256 procedures).
- **Two-state procedures** (the lag-5 and lag-6 geometry as a grid walk). State = (previous cipher rune, position in word);
  c = T(s, p) + step·pos mod 29 with step 5 or 6, over the 207 index tables, the three repeat rules, both filler settings,
  both ᚠ settings, reset none (4,968 procedures).
- **The three behaviours as one procedure** (consumption, preservation, adherence). On a would-be repeat the repair is chosen
  by the plaintext rune's class in Gematria order: vowel runes spend (redraw), the next class holds (write the state rune),
  the rest copy (write the rune five back, or the state if the word is shorter); the three class assignments permuted (six
  rules), over the 207 index tables at states c1 and c6w, reset none, both filler settings (4,968 procedures).

About 57,000 procedures; the screen at §73's rate is about three and a half hours on seven shards. Predictions: **H1′** candidates under
1 % of the family; **H2′** no survivor at 200 replicates; **H3′** no decoder hit (median page 5-gram z ≥ 6 with a page ≥ 10;
chance level re-recorded for the new family before any page is read); **H4′** if any procedure holds the S count (L5S within
|z| < 3) together with D, L5, L6T and BIG, it is reported first whatever else it fails, since the S count is the band no
procedure or rule has made. Expected: H1′–H3′ hold; H4′ is the thing to watch.

## Instrument 2: numbers as directions (`src/direction_lane.py`)

**Part A, keyless and self-referential.** The cipher word's own number directs its decryption, or the previous word's does.
For g ∈ {Gematria sum mod 29; sum mod 28 plus 1; sum of (v − 1) mod 29 (the totient reading); product of values mod 29; word
length; the index of the word's largest rune} taken from the word itself or from the previous cipher word (first word: ᚠ),
applied as: a constant shift over the word; a step (key_j = j·g for the j-th rune of the word); an offset into the prime
stream (the word keyed by p, p − 1, p + 1 from position g); an offset into the solved plaintext (the word keyed by the
solved text from word g). Three signs, ᚠ rule off and on. Every page decoded under every configuration (6 × 2 × 4 × 3 × 2 =
288 per stream choice; about 900 configurations), scored by the 5-gram z against 2,000 uniform pages and the §72 z\*. Hit as
in §73 Part B. Chance level: the same configurations on uniform pages, recorded first.

**Part B, the words as the map.** The solved pages' words in order, each with its number W_k. Streams from them: (i) W_k mod
29 as one key symbol per rune (the number sequence as a stream); (ii) W_k mod 29 as the shift of the k-th word of the unsolved
section (word-aligned; the section's words are counted through the page joins, §71); (iii) the k-th word keyed by the prime
stream from offset W_k; (iv) the k-th word keyed by the solved text from word W_k mod (number of words); (v) the cumulative
sum of W_k mod 29 as a running direction, one symbol per word. Each expressed as a per-rune keystream for every page from the
page's word structure, so §62's free-null decoder runs unchanged (prior −2.2, tier 1 on the first 160 runes at z ≥ 4.5,
tier 2 on the full page at z_uni ≥ 6 and free − plain ≥ 20 and readable). Alignment: the solved word index runs from 0 to
2,900 in steps of one (the map may start anywhere); for (i) the stream runs at offsets 0–2,900. Three signs, ᚠ off and on.
Six plants: Emerson enciphered under schemes (ii), (iii) and (v) with §62's filler form at a known alignment, two per scheme.
Predictions: **D1** plants 6 of 6 recovered at rank 1 within ±1 word of the planted alignment; **D2** no tier-2 candidate;
**D3** no Part A hit. Expected: all hold.

**Amendment (2026-10-31, after the instruments' smoke tests and before any run on the pages).** Instrument 2's plants located
their planted alignment at rank 1 in six of six smoke controls (tier-1 z 3.9–12.3, full-page z 5.2–17.3) and five of six
failed §62's free − plain ≥ 20 clause (margins 1–41 nats). The reason is the scheme, not the plants: a word-aligned key
realigns the plain decoder at every word, so a filler costs it one word's tail rather than the rest of the page, and the
free-null decoder's margin over it never grows. The clause was built for stream keys (§55 part B) and is not a discriminator
here. For Part B the tier-2 candidate rule is therefore z_uni ≥ 6, above the full-page null maximum, and readable, with the
free − plain margin reported; the plants pass on the same rule. Two smoke plants were weak (the prime-offset scheme at tier-1
z 3.9; a cumulative plant at full-page z 6.6 with a 200-draw null); the run's six plants with 2,000-draw nulls are the
measurement. Instrument 1's smoke ran clean. Both instruments are queued behind C11.

## What a null means

That the sentence's derived readings, at this resolution (one table and one or two states; word numbers as shifts, steps and
offsets into the book's own streams; the solved words as a map at every alignment), do not produce the pages' fingerprints or
read a page. It leaves: numbers of the *unsolved* words as directions into material not enumerated here; operations named by
sentences not yet read as instructions; and the literal reading, which is already closed at scale. Cost: a day of compute
after C11, a day of writing.

## Reproduce

`FAMILY=2 STAGE=chance|screen|confirm|decode|merge .venv/bin/python -I src/hand_procedure_lane.py`;
`STAGE=chance|keyless|map|merge .venv/bin/python -I src/direction_lane.py` (SHARD/NSHARD on the map stage).

## Outcome (2026-10-31 evening, written after both runs; README §74 and §75)

Instrument 1: H1′ holds (1 candidate of 56,952, the three-behaviours procedure on the lag-6 cipher state with fillers); H2′ holds (it fails the lag-6 count, 45.7 against 77, and the S count, 4.2 against 11, at 200 replicates); H3′ holds (largest median page z5 1.15 against chance 0.97); H4′: 104 procedures hold D, L5, L5S, L6T and BIG at 20 replicates, every one passing the S cell on the width of its spread (predicted 4–7 S pairs); the 1,454 procedures that predict eleven or more are totient-multiplied tables at k = 15 that make S common everywhere and fail Sfreq, L5, L6T and U. The model-free z\* column was not calibrated for this family's many-to-one tables; a per-decoder chance was recorded post hoc (`results/hand_procedure2_zstar_chance.json`) and shows the column measures the decoder. Instrument 2: D1 fails as written (4 of 6; the two misses are the schemes the amendment flagged, found at rank 1 at the planted alignment at tier-1 z 3.7 and full-page z 5.5); D2 and D3 hold. The solved text parsed into 726 words, not the 2,900 estimated above; alignments 0–725 are every start.
