# §60 pre-registration: the filler power curve (written 2026-10-29, before any plant was scored)

## Why

§55 part B measured decoder power at one filler rate, r = 0.10 per rune, chosen from the fingerprint before §59 fitted the
filler form to the word lengths (one extra rune at a uniform position in a fraction p = 0.40 of the words of two or more
runes). One point says the plain decoder has no power at that rate; it does not say where the loss begins, and it does not
test the form the data fit. This lane runs the curve. It settles, with a number, what the field's plain-decoder negatives
are worth at each filler rate.

## Design (fixed here)

Everything is §55 part B's instrument with the filler cell widened and one decoder dropped.

- Plaintext: English (Emerson, book spelling) from a random word start; each plant's plaintext and key are shared by all
  of its filler cells (paired design), so the curve is read within plants.
- Mechanism: soft reject-on-repeat at q = 0.81, then the filler. Two forms:
  - **per rune**: after each emitted rune a filler with probability r, r ∈ {0.01, 0.02, 0.05, 0.10}, plus r = 0 as the
    reference; the filler is uniform over the 28 runes other than the previous cipher rune (adds no doublets);
  - **per word** (the §59 form): in each word of two or more runes, with probability p ∈ {0.2, 0.4, 0.6}, one filler at a
    uniform position 0..L, same rune law. At the English mean word length (4.0 runes) p = 0.2, 0.4, 0.6 are about 0.045,
    0.09 and 0.13 fillers per rune.
- Lengths n = 100, 160, 230; families Vigenère word (≥ 8 runes, from the book library), prime stream, running key (corpus
  text ≤ 60,000 runes, random offset, either direction); signs and F variants cycled; 12 plants per (n, family).
- Decoders: plain (`score.decode`, soft skip rule) and free-null at the §55 prior −2.2 (`null_mask` at every rune). The −0.8
  prior is dropped (§55 chose −2.2 by its rule).
- Statistic: z of the true key over 400 random keystreams through the same decoder, rank among its family (538 Vigenère
  keys, 303 prime streams, the 4,096 neighbouring offsets). **Recovered = z ≥ 6 and rank 1.** Power = recovered fraction
  over the 12 plants of a cell. Recorded per plant in addition: the number of fillers and the position of the first one.
- Seed 6000 + shard; 8 shards by plan index; `MERGE=1` writes `results/filler_curve.md` / `.json`.

## Predictions, committed before the run

The mechanism of the loss: a plain decoder reads English under the true key up to the first filler and noise after it
(a filler moves the page one step against the key and the skip transition moves the key the other way, so it cannot undo
it; a periodic key can be realigned by P − 1 skips spread over later positions, which is why §55's Vigenère cells kept a
median z of 2.4–3.3 where the others had 1.0–1.5). With z ≈ 0.78 √n for a full English window (§55's r = 0 cells), a prefix
of m English runes gives z ≈ 0.78 m / √n, so z ≥ 6 needs m ≈ 77, 97 and 117 runes at n = 100, 160, 230, and the chance the
first filler comes later than m is (1 − r)^m.

| claim | statement | pass if |
|---|---|---|
| C1 | the plain decoder is already below half power at two fillers per hundred runes | plain power ≤ 0.50 in every cell with r ≥ 0.02 (all families, lengths) |
| C2 | the plain decoder is dead from five per hundred and at every per-word rate | plain power ≤ 0.10 in every cell at r = 0.05, r = 0.10 and p = 0.2, 0.4, 0.6 |
| C3 | the one sloped point: at one per hundred the plain decoder keeps part of its power | plain power between 0.15 and 0.65 in at least 6 of the 9 cells at r = 0.01 |
| C4 | the free-null decoder pays almost nothing for rare fillers | free-null power ≥ 0.75 in every cell with r ≤ 0.02 and n ≥ 160 |
| C5 | the two filler forms are equivalent at matched per-rune rate | free-null power at p = 0.4 within ±0.25 of the same (n, family) cell at r = 0.10 |
| C6 | the half-power rate is below two per hundred everywhere | the plain decoder's power crosses 0.5 between r = 0 and r = 0.02 in every (n, family) |
| C7 | the loss is the first-filler mechanism | over all plain-decoder filler plants, Spearman correlation of the true key's z with the first-filler position ≥ 0.5 |

Reading fixed in advance: the field's negatives were run plain; the rate the data fit is p = 0.40 (about 0.09 per rune).
If C2 holds, those negatives have power ≤ 0.10 against the fitted filler world at every family and length tested here, and
the scoped paragraph in §55 stands as written. If C1 or C2 fails, the §55 paragraph is to be weakened to the rate at which
the loss is measured. C3–C7 are mechanism checks; a failure there changes the explanation, not the scope.

Not in this lane: a word-constrained filler decoder (at most one filler per word), the margin calibration on wrong keys at
page length that §55 asked for, and any sweep. Each is its own registration.
