# Replicate the two echo laws from scratch

*Written 2026-11-01 at the pause. This page is for someone who wants to check the record's central claims without reading or
running its code: everything needed to reimplement the two measurements and their nulls, and the numbers a correct
reimplementation should reproduce. Two other labs found the same two laws before this record did, under their own nulls
(ZzNible: 104 lag-5 equalities of 2,105 pairs, z 3.75; pnotisdev: the same eleven S pairs and registry row `obs-lag6` for the
affine relation), so an independent implementation here is a third.*

## 1. Source and conventions

- **File**: `data/raw/iddqd__liber-primus__transcription--master.txt`, the community master transcription, unchanged here;
  SHA-256 `e21743ccd9a07f3845d52a329c61b9fa69e9ca6a44ee3ba0db8f28a0d7065004`.
- **Pages**: split the file on `%`. The chunks at indices 16 to 71 (0-based) are the unsolved section; 55 of them contain
  runes. Keep them in file order; call them LP2-00 … LP2-54 after dropping the empty one.
- **Runes**: the 29 runes of the Gematria Primus in standard order, indexed 0 … 28:
  ᚠ ᚢ ᚦ ᚩ ᚱ ᚳ ᚷ ᚹ ᚻ ᚾ ᛁ ᛄ ᛇ ᛈ ᛉ ᛋ ᛏ ᛒ ᛖ ᛗ ᛚ ᛝ ᛟ ᛞ ᚪ ᚫ ᚣ ᛡ ᛠ (F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA).
  S is index 15. Ignore every other character except the separators below.
- **Words**: the characters `-` `.` `&` `$` `§` end a word. **`/` is a line break and is not a word boundary**: 452 of the 617
  line ends fall inside a word, and treating `/` as a boundary over-splits the words and hides the echoes (§42 of the README
  records that mistake). A word is a maximal run of runes between separators, continuing across `/` and `\n`.
- **Checks**: 12,956 runes in all; 86 adjacent equal pairs (doublets) across the 55 pages; 2,073 within-word pairs at
  distance 5 and 1,267 at distance 6.

## 2. The two measurements

Within-word pair at distance d: positions i and i + d on the same page with the same word id.

- **L5**: the number of within-word pairs at distance 5 whose two runes are equal. Expected: **102**.
- **L5S**: the number of those equal pairs whose rune is S (index 15). Expected: **11**.
- **L6T**: the number of within-word pairs at distance 6 with later = (24 − 2 × earlier) mod 29. Expected: **77**.
  (The map is the affine map a = 27, b = 24 in the family c_j = (a·c_i + b) mod 29; its only fixed point is H, index 8.)

## 3. The nulls

**K-fixed null (the record's main null).** For each page separately, sample arrangements of that page's runes that keep (i)
the multiset of runes, (ii) the word structure (which positions belong to which word), and (iii) the page's number of
adjacent equal pairs K. Sampler: start from the page as written; propose a transposition of two positions chosen uniformly;
accept it if and only if the page's doublet count is unchanged; **count every proposal as one step whether or not it is
accepted** (counting only accepted steps biases the chain; the record made and corrected that error, README §56). Burn in
20 × (page length) proposals, then take one draw every 4 × (page length) proposals, 999 draws per page. Compute the three
statistics on each draw, pooled over pages. Expected null means and sds (seed-dependent in the second decimal):

| statistic | observed | K-fixed null mean ± sd | z |
|---|---|---|---|
| L5 | 102 | 71.0 ± 8.3 | +3.7 |
| L5S | 11 | 2.2 ± 1.5 | +6.0 |
| L6T | 77 | 43.7 ± 6.5 | +5.1 |

**Word-preserving shuffle (the second null).** Permute each page's runes uniformly at random, keeping the word structure and
letting K float (it rises to about 445). Expected: L5 70.7 ± 8.2, L5S 2.2 ± 1.5, L6T 43.5 ± 6.7. The two nulls should agree
to a few tenths of a sigma; if yours do not, check the word convention first.

## 4. The search-adjusted significance (optional, README §82)

Inside every K-fixed draw, recompute (i) within-word equalities at every distance 2 … 12, (ii) within-word hits of every
affine map c_j = (a·c_i + b) mod 29, a = 1 … 28, b = 0 … 28, at distances 2 … 8, and (iii) at the sites of the distance that
won (i), the count of each of the 29 runes standardized as (count − n·f_r) / √(n·f_r(1 − f_r)) with f_r the rune's share of
all 12,956 runes. Standardize each cell by its own null mean and sd; take the maximum per scan per draw. Expected: the observed
maxima are distance 5 (z ≈ 3.7), the map a = 27, b = 24 at distance 6 (z ≈ 5.1), and S (z ≈ 4.2); family-wise p ≈ 0.015,
≈ 0.008 and ≈ 0.085; **no draw of 999 reaches the first two maxima at once**. Zero exceedances in 999 bounds that joint
probability at about 3 in 1,000 (95 %), so the pair of laws survives roughly a sixteenfold wider search by Bonferroni, and
either law alone only a three- to sixfold one.

## 5. Replications so far

2026-11-01: an external reviewer, with a separate counting implementation written from this page and without importing this repository's code, reproduced the source hash and all five counts of sections 1 and 2. The nulls of section 3 and the search-adjusted significance of section 4 have not yet been reproduced independently.

## 6. What counts as a replication

Within sampling error of the table in section 3 for all three statistics under both nulls, from an implementation that did
not import this repository's code. If you get the counts in section 1 but different null means, the sampler is the likely
cause; if you get different counts, the word convention is. Either way, please open an issue with your numbers: a
disagreement is worth more to this record than an agreement.
