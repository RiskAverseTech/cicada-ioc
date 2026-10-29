# §55 pre-registration: the word-length fingerprint, decoder power under fillers, and the filler sweep (written 2026-10-29, before any plant was scored or any page swept)

## What prompted it (exploratory, computed this morning before this file)

With the corrected word edges (§42: `/` is a line break, not a word boundary), the 55 unsolved pages hold 2,928 words of mean
length 4.42 runes. The solved pages' 698 cipher words (their ciphers preserve word boundaries) have mean length 4.01, English
prose spelled in runes 4.02. The two-rune cell is 15.9 % on the unsolved pages against 23.9 % (solved) and 25.4 % (English prose);
the chi-square of the unsolved histogram against English prose is 183 on about 13 degrees of freedom, where a second English
sample (the solved pages' translation, 727 words) scores 10. Latin (chi-square 1,476), Old English (2,930), Chaucer (345), and
English with a fraction of word separators dropped (152 at best) fit worse; English with a filler rune inserted after each rune
with probability 0.10 fits best (80), still not perfectly. Two other facts were checked the same morning: the index of
coincidence by word position (from either end, positions 0–7) is flat (|z| ≤ 1.4 in 15 of 16 cells, +3.5 in one cell of 340
runes), and no cipher word of four or more runes occurs twice anywhere on the 55 pages (per-page shuffle null 0.2). So the
plaintext is not English prose with its separators intact and is not under a key that restarts at each word.

These numbers are descriptive and were not pre-registered. What follows was.

## Already covered, not rerun

- §22 ran the free-null decoder (a rune may be an unkeyed filler that consumes no key value, log prior −0.8 per rune, chosen on
  controls) over the book's own key library (families.ALLSETS, 22,863 configurations = 7,621 keys × 3 signs) on all 55 pages,
  with plants at filler rates 0.15, 0.22 and 0.30 under the hard rule: 15 of 18 controls, null. The book library is therefore
  covered in the filler world at rates above the one the fingerprint suggests.
- §54 ran the same decoder over pnotisdev's 1,439 streams at every offset of the periodic streams and offsets 0–999 of the
  non-periodic ones (window 160): null, 6/6 hold controls.
- Not covered in the filler world: the external running-key texts of §25, §40 and §53 (15 texts, 2.7 M runes, decoded there
  with the plain decoder only), and offsets ≥ 1,000 of pnotisdev's non-periodic streams.

## Part A: the fingerprint, written up (`src/wordlen_fingerprint.py`, `results/wordlen_fingerprint.md`)

Reported as computed above, with one addition fixed now: the chi-square's sampling distribution from 2,000 bootstrap samples
of 2,928 words drawn from English prose (the "English against English" null), so the unsolved pages' 183 has a p-value rather
than a comparison with one second sample. Models reported: Latin, Old English, Chaucer; separators dropped at d = 0.1–0.4;
per-word Poisson fillers λ = 0.25–1.0; per-rune fillers r = 0.05–0.15; function words removed. No claim beyond "does not match
English prose; the best simple distortion is per-rune insertion near 0.10" is made from this part.

## Part B: decoder power under fillers (`src/filler_power.py`, `results/filler_power.md`)

Plant: English (Emerson, as §54) of n = 100, 160 and 230 runes, encrypted under the repository's standard mechanism (soft
reject-on-repeat, q = 0.81) with a filler inserted after each emitted rune with probability r = 0.10; the filler is uniform
over the 28 runes other than the previous cipher rune (so it adds no doublets; the data have 86) and becomes the previous rune
for the next real rune's repair. Three key families: a Vigenère word of ≥ 8 runes from the book library; a prime stream
p[n+s]; a running key (a corpus text at a random offset, either direction). Three signs and two F variants cycled. 12 plants
per cell (3 lengths × 3 families = 9 cells, 108 plants), each also encrypted once WITHOUT fillers (r = 0) as the reference.

Decoders: plain (score.decode, soft skip rule) and free-null (null_mask at every position) at two priors, −0.8 (§22's) and
ln(0.10/0.90) = −2.2. The echo-aware decoder is not tested: it needs the filler positions, which are unknown.

Statistic per plant: z of the true key over 400 random keystreams through the same decoder, and the true key's rank among its
family (every word key of the family; every prime offset; the 4,096 neighbouring offsets of the text, as §54). A plant is
recovered at z ≥ 6 and rank 1. Power = recovered fraction per cell.

Decisions fixed now: (1) the prior used in Part C is whichever of −0.8 and −2.2 recovers more running-key plants at r = 0.10
over the three lengths, ties to −0.8; (2) Part C is run only if the free-null decoder at that prior recovers at least 50 % of the
running-key plants at n = 230 and r = 0.10. Below that, the power table is reported and Part C is not run, with the reason that
the lane cannot be run at useful power.

## Part C: the filler sweep (`src/filler_lane.py`, `results/filler_lane.md`)

Key material: the 15 external running-key texts (data/corpus/corpus.json, corpus_pilgrim.json, corpus_cicada.json), at every
offset in both directions for texts up to 60,000 runes (§25's EXACT scope) and at sentence-start offsets, forward, for the
longer ones (§25's SENTENCE scope); and pnotisdev's non-periodic streams at offsets 1,000–1,999 (continuing §54; its periodic
streams were complete). Decoder: free-null at the prior chosen in Part B. Two tiers, as §54's hold decoder:
- Tier 1: the first 160 runes of LP2-00, LP2-01 and LP2-02 (the three longest first pages), 3 signs × 2 F variants, every offset
  in scope; a cell survives at z ≥ 4.5 over that window's null of 2,000 random keystreams through the free-null decoder.
- Tier 2: the survivor's full page. Candidate rule (§22's): z_uni ≥ 6 over the full-page free-null null AND the free-null score at
  least 20 nats above the plain decoder's score for the same key AND readable English to a human. Offsets within ±3 in the same
  text and direction are one hypothesis. A candidate is then decoded on every page at every offset of its scope.
Controls (6, fixed before the run): 262 runes of English under the Part B mechanism (soft rule, fillers at 0.10) with a corpus
text at a random offset, signs, F variants and directions cycled; a control passes when tier 1 finds the true offset at rank 1
among the text's 4,096 neighbouring offsets with z ≥ 4.5 and tier 2 meets the candidate rule.
Expected result: null. Coverage limits to be stated: the window power at 160 runes from Part B; pnotisdev offsets ≥ 2,000;
the long texts at sentence starts only.
