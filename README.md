# Liber Primus: is any keystream reused across the unsolved pages?

A depth-two (key-reuse) index-of-coincidence test on the 56 unsolved pages of Cicada
3301's Liber Primus, preceded by the computation that decides whether such a test can
work at all. Everything here is reproducible from `src/` with numpy; sources and pinned
revisions are in `SOURCES.md`; tables are in `results/`.

**Short answer.** The test the panel described is underpowered on single page pairs
(q − 1/29 = 0.0019, about 1.8 sigma per aligned pair of 250 runes), so I ran it anyway
and added a pooled version that sums all 1,485 pairs. Both are null for aligned reuse
at any offset within ±200 runes and for any within-page period from 2 to 200. The one
real non-randomness found is at lag 1: the unsolved pages contain 86 doubled runes
where 445 are expected (z = −17). That is a property of the cipher, not evidence of a
reused key.

## 1. Data

- Transcription: the rtkd/iddqd master file (pinned commit in `SOURCES.md`), confirmed
  rune-for-rune against Taiiwo/cicada and page-for-page against LiberPrimusSolver's
  `unsolved.txt`. The book has 74 pages; pages 1–15 and 72–73 are solved, chunks 16–71
  are the 56 unsolved LP2 pages (`LP2-00`..`LP2-55`), one of which (LP2-50) is image-only.
- Alphabet: Gematria Primus, 29 runes, index 0..28 = F U TH O R C G W H N I J EO P X S T
  B E M L NG OE D A AE Y IA EA.
- Plaintext: the solved pages were *decrypted with their published keys* (Atbash,
  Vigenère DIVINITY and FIRFUMFERENFE with the "plaintext F is left unencrypted" rule,
  shift-3-then-Atbash, the totient prime stream, and plain Gematria) and every section
  was verified rune-for-rune against the rtkd English translation. This gives 2,977
  plaintext runes in the book's own spelling (`data/processed/solved_plaintext_latin.txt`),
  avoiding the English-to-rune ambiguities (NG vs N+G, EA vs E+A, IA/IO, C/K) that a
  back-mapping would introduce. Script: `src/prepare.py`.

## 2. q and the power of the test (`src/q.py`, `results/q.md`)

With p the rune frequency vector of the plaintext, q = Σ_d (Σ_a p_a p_{(a−d) mod 29})² is
the coincidence rate of the difference of two independent plaintext streams, i.e. what
C − C' leaves behind when the keystream cancels.

| quantity | value |
|---|---|
| plaintext runes | 2,977 |
| IC of the plaintext itself | 0.0614 |
| **q** | **0.0364** (bootstrap 95% CI 0.0361–0.0368) |
| 1/29 | 0.0345 |
| **q − 1/29** | **0.0019** |
| empirical IC of page-minus-page differences, 200-rune windows | 0.0364 |

Under the null (independent iid uniform keystreams) the difference stream is iid
uniform, E[IC] = 1/29, and because pairs of positions sharing one index are uncorrelated
for a uniform alphabet, Var[IC] = 2π(1−π)/(N(N−1)) exactly (π = 1/29), i.e. sd ≈ 0.258/N.
Monte Carlo agrees to three digits.

| N | sd of IC under null (exact / MC) | sigma per aligned pair if the key is reused |
|---|---|---|
| 150 | 0.00173 / 0.00173 | 1.1 |
| 250 | 0.00103 / 0.00104 | 1.8 |
| 400 | 0.00065 / 0.00065 | 2.9 |

**Verdict on power: underpowered.** The excess is 0.0019, well under the 0.005 the panel
said it needed. A fully reused key would move a single 250-rune pair by under 2 sigma,
while the scan below makes half a million comparisons whose null maximum is 7–8 sigma.
Per-pair 5-sigma detection is therefore impossible for this plaintext distribution.

What *is* powered is pooling: if every page restarted the same generator from the same
state, all 1,485 pairs would be elevated at offset 0 and the pooled z would be about
65. If a quarter of the pages shared a stream, roughly 4 sigma pooled. So the pooled
test can still rule out the "identical reset on every page" hypothesis decisively.

## 3. The scan (`src/depth_two.py`, `results/depth_two.md`, `results/depth_two.png`)

Pre-registered before running (text in the script header):

- **R1 (panel rule, per pair):** a positive needs ≥ 3 disjoint page pairs each at or
  above 5 sigma with mutually consistent offsets.
- **R2 (pooled, added because of section 2):** pooled z(k) = Σ_pairs sigma / √(#pairs) at
  each offset k and each within-page lag L; a positive needs z ≥ 5 *and* above the
  maximum seen in every within-page permutation replicate (runes shuffled inside each
  page, which keeps every page's rune frequencies so a non-flat ciphertext cannot fake
  a positive).

Setup: 55 pages with runes, 1,485 pairs, offsets −200..+200, lags 1..200, minimum
overlap 60 runes; 507,789 pair-offset tests and 9,376 page-lag tests; 30 permutation
replicates of the whole scan.

![depth-two scan vs null](results/depth_two.png)

**Per pair (R1).** Top 20 hits are in `results/depth_two.md`. The strongest is
LP2-38/LP2-49 at offset −41, 6.63 sigma, on an overlap of only 66 runes. There are 74
hits at or above 5 sigma, at 68 distinct offsets, the most repeated offset having 3.
The shuffled-page null gives 58–87 such hits per replicate (median 70), and the observed
maximum 6.63 is *below* every one of the 30 null maxima (6.65–8.11). The histogram of
observed sigmas lies on top of the null's. R1 does not trigger once calibrated; read
literally ("some pair ≥ 5 sigma") it would trigger on shuffled data just as often.

A post-hoc note for honesty: three hits sit at |offset| ≤ 1 (LP2-28/42 at 0, LP2-04/45
at +1, LP2-35/38 at −1) where about 0.55 are expected, a ~2% coincidence after the fact.
Their difference-stream ICs (0.040) are also about 4 sigma *above* what a reused key
predicts (q = 0.0364), and the pooled z at offset 0 over all pairs is 0.08. I do not
count them as evidence.

**Pooled (R2), cross-page offsets.** Pooled z at offset 0 is 0.08 (null: 0.16 ± 0.89).
The largest pooled z over all 401 offsets is 2.96 (offset −181) against a null maximum of
2.99 ± 0.37 (max 4.07). Null. Nothing resembling the ~65 an identical reset would give,
nor the ~4 a quarter-sized shared subset would give.

**Pooled (R2), within-page lags.** The largest pooled z is 6.39 at **lag 1**, above the
null maximum 3.87, so R2 triggers there. Lags 2–200 are null (next largest 3.47 at lag 13,
3.21 at lag 10, both inside the null range). `src/lag1.py` shows what lag 1 is: of 12,901
adjacent rune pairs, only **86 are doublets (same rune twice) against 445 expected,
z = −17.3**; a few other difference classes are mildly over-represented (d = 20, 27, 16,
19 at +2.5 to +3.1). This is a deficit of repeats spread across pages (5 pages above +2
sigma, none below −2, mean +0.86), not a short-period generator: a period-1 generator
means a constant key, which would make every page's lag-1 structure that of plaintext
(lag-1 IC 0.0388) and give a pooled z near 29, not 6.4. The doublet deficit in the
unsolved pages is, to my knowledge, already known in the Cicada community; here it is
simply the only thing in the ciphertext that is not consistent with iid uniform
keystreams. It also explains the one other oddity in the tables: the mean sigma over all
pair-offset tests is +0.0065 (null ≈ 0), the same at every offset. Adjacent index pairs
are 2/N of all pairs, and two pages sharing the same non-uniform lag-1 difference
distribution match on those with an excess of about 9 × 10⁻⁴, which predicts a mean
sigma of about +0.007. Offset-independent, so unrelated to aligned reuse.

## 4. Decision

- Aligned keystream reuse between any two unsolved pages at any offset in ±200 runes:
  **not detected**; the pooled test excludes a shared reset generator across all or a
  large fraction of pages, and the per-pair test could not have seen a single reused
  pair anyway (section 2).
- Within-page periodic keystream with period 2–200: **not detected**.
- Lag 1: a real, strong deficit of doubled runes; a cipher property, not key reuse.
- A null here rules out aligned reuse at the tested offsets and short-period resets
  only. It says nothing about a long-period generator, about reuse at offsets beyond
  200, about autokey or transposition schemes, or about whether the pages are stream
  ciphers at all.

## 5. For the debate

My take: the depth-two test cannot settle this. I computed q from the 2,977 runes of
verified Liber Primus plaintext and got 0.0364, only 0.0019 above 1/29, so even a page
pair that shared its entire keystream would show up at under 2 sigma, while the scan
needs to survive half a million comparisons whose chance maximum is 7 to 8 sigma. I ran
it anyway over all 1,485 pairs of unsolved pages at every offset within ±200 and every
within-page lag up to 200: the per-pair hits are exactly what shuffled pages produce, the
pooled signal at offset 0 is zero against a prediction of about 65 if every page reset the
same generator, and no offset or lag from 2 to 200 stands out. The only real structure is
that the unsolved pages almost never repeat a rune twice in a row (86 doublets where
445 are expected, 17 sigma), which is a property of the cipher and not a reused key. So
aligned key reuse and short-period page resets are off the table; everything else,
including a long-period stream or a non-stream cipher, is untouched by this test.

## Reproduce

```
python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
.venv/bin/python -I src/prepare.py      # decrypt + verify solved pages -> data/processed/
.venv/bin/python -I src/q.py            # results/q.md, q.json
.venv/bin/python -I src/depth_two.py 30 # results/depth_two.md, *.npz, summary.json (~3 min)
.venv/bin/python -I src/lag1.py         # results/lag1.md
.venv/bin/python -I src/plot.py         # results/depth_two.png
```

Layout: `data/raw/` downloaded sources (never executed), `data/processed/` verified
pages, `src/` scripts (`lp.py` holds the alphabet and parsers), `results/` outputs.
