# Registration: word-level and two-state autokeys, as generators against the bands and as decoders of the pages, written before any run

Date 2026-10-31 (night, EDT). Companion to `docs/hints-coverage.md` (row 0.1 wisdom, "Command your own self", the unrun
column) and to `results/s_autokey_check.md`. Nothing below has been run; the instrument is queued behind C11.

## Why

Every construction that reproduces the stream's background habits predicts four or five S..S pairs at lag 5 inside words where
the pages have eleven: E56w 4.6, E56w+n 4.8, the three behaviours 4.2 (§47, §58, §74). §47's argument says why: a cipher that
writes an echoed value as plaintext plus a key whose value is uniform given its own difference across the pair puts a uniform
rune at the echo, so no copy rule, periodic key or independent key can prefer S. The ingredient that is missing must make the
written value depend on the plaintext. The simplest such cipher, a lag-1 plaintext autokey, puts S at 3.1 × uniform at the
coincidences for a stated reason (the Gematria order places E-R, N-A, A-I, U-T and R-M fifteen apart, and S is rune fifteen) and
is excluded by everything else it predicts (TH, X, L, Y enriched; IoC 1.12; repeat rate 1.32 ×). What has not been run is the
plaintext-dependent key at the resolution the creators' own sentence suggests: the text keying itself one word at a time, and a
key whose source switches by a rule the text states. This instrument enumerates that class, measures every member against the
thirteen bands with the S cell as the primary question, and applies every member as a decoder of the 55 pages. [inferred — the
reading; stated — the counts]

**Ledger first.** Autokeys elsewhere (`results/ledger_diff.md`): this repository's §3 (plaintext and ciphertext autokeys, lags
1–5, three primers), pnotisdev's R12-C1 (k-history feedback, k = 2..6) and Round 11 (unbounded feedback), Dukotah's chain and
ciphertext autokeys at lags 1–60 and plaintext lags 1–3 over all seeds, ZzNible's phase-2 identity feedback. All are rune-rate
autokeys run as decoders and judged on readability or the IoC. None is word-level, none switches its source by a rule, none is
run with fillers, and none is scored on the S cell. [stated — the ledger]

## The family (enumerated before the run; nothing is added after a row is read)

Skeleton as in §73: Emerson's English laid into the 55 pages' rune counts on shared layouts; the §59 filler form (one uniform
extra rune at a uniform position in 40 % of words of two or more runes, written like any rune and never updating a plaintext
state) or none; the book's literal-ᚠ rule (plaintext ᚠ written as ᚠ, no state update) off or on; a repeat rule none or
**redraw** (if the written rune equals the previous one, the key is applied once more to the written rune; if it is still equal
the repeat stands). Each rune is written c = p ⊕ k under one of three signs: add c = p + k, sub c = p − k, beaufort c = k − p
(mod 29, Gematria indices). The primer is ᚠ (index 0) wherever a key has no source yet. The key k for the rune at position w
(from 0) of word m (counted through the page) comes from one of five sub-families:

- **W, the previous word as the key.** The runes of word m − 1 (its plaintext runes for source *plain*; its cipher runes as
  written for source *cipher*), read forward and cycled (k_w = key[w mod len]), read backward and cycled, or read forward and
  padded with the primer past its end. The first word of a page is keyed by the primer. 2 sources × 3 readings × 3 signs = 18.
- **G, the previous word's number as the key.** One constant k over word m, g(word m − 1) for g ∈ {sum of indices mod 29;
  Gematria (prime-value) sum mod 29; Gematria sum mod 28 plus 1; first rune; last rune; length mod 29}; source plain or
  cipher; the first word of a page takes g = 0. 6 × 2 × 3 = 36.
- **R, one key rune consumed per word.** k for word m is the m-th rune of the page (0-based; the m-th plaintext rune for source
  plain, the m-th cipher rune for source cipher, the primer if that rune is not yet written). 2 × 3 = 6.
- **L, rune autokey, word-aware.** k_i = p_(i−d) (plain) or c_(i−d) (cipher), d = 1 … 6; *continuous* (the key runs across
  word boundaries within the page) or *reset* (positions w < d take the primer). 2 × 6 × 2 × 3 = 72. The member plain, d = 1,
  continuous, sub, no filler, no repair, literal-ᚠ off is the rule of `results/s_autokey_check.md` and serves as the positive
  control for the S cell.
- **T, two sources and a switch.** The key is the previous plaintext rune (A) or the previous cipher rune (B), chosen per rune
  by a rule: *parity* (A at even w, B at odd); *after S* and *after I* (B for the rune after a written S or I, else A), each with
  scope next rune only, the rest of the word, or a toggle that persists for the page; *vowel* (B when the previous plaintext
  rune is a vowel in the §74 classes, else A); the roles of A and B exchanged for every rule; and *both*, k = p_(i−1) + c_(i−1).
  (1 + 3 + 3 + 1) × 2 × 3 + 3 = 51.

183 members × fillers {0, 0.40} × repair {none, redraw} × literal-ᚠ {off, on} = **1,464 procedures**. No parameter is fitted.

## Part A, the generator

§73's harness unchanged: 20 replicates on shared layouts; the thirteen bands D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq,
U, W2, WM against the pages' values; candidate = every band within |z| < 3; candidates rerun at 200 replicates. Added for this
family: a member is **S-admissible** when L5S, L5, D, U and Sfreq are all within |z| < 3 at 20 replicates (the S count together
with the four cells the lag-1 autokey failed); every S-admissible member is rerun at 200 replicates whatever else it fails and
reported first.

## Part B, the decoder

Every member inverts from the ciphertext given the word structure and the primer: exactly for cipher-sourced keys, and for
plaintext-sourced keys through the decoded plaintext. The decoder is filler-blind (every cipher rune is decoded as a plain
cell), so under fillers a plaintext-sourced key propagates the filler's error: through the rest of the page for L-continuous and
W-plain, through one word for L-reset and G-plain. That is a stated limit of this instrument, measured by the plants, not
hidden. The 732 distinct decoders (the filler setting does not change a decoder) are applied to the 55 pages and scored by the
rune 5-gram z per page (§27; null 2,000 uniform pages per length) and the §72 z\*; by registration lesson eleven, any z\* at or
above 10 is judged against that decoder's own uniform-page null before it is called anything. Chance level: 200 random members
on uniform page sets, recorded first.

**Plants.** Emerson enciphered under six members at the pages' lengths, each decoded by all 732: W cipher forward sub, L cipher
d = 2 reset add, T after-S word-scope (A plain, B cipher) beaufort, all without fillers; G cipher Gematria-sum sub, W plain
forward add and L plain d = 1 continuous sub with fillers at 0.40. Redraw off, literal-ᚠ off.

## Predictions

- **A1 (the S cell, primary).** No member is S-admissible. The positive control lands L5S inside the band (about eleven S pairs)
  and fails U and Sfreq, as the check found. If any member is S-admissible, it is the first mechanism in this record to carry the
  S count without an S-specific rule, and it is reported first whatever else it fails.
- **A2 (the bands).** No member is inside all thirteen bands at 20 replicates and candidates are under 1 % of the family; every
  member fails L6T, since nothing in the family writes the lag-6 relation.
- **A3 (plants).** The three plants without fillers are read by their own decoder at median page z5 ≥ 6 and at rank 1 among
  the 732 on median z5. The cipher-sourced filler plant is read at median z5 ≥ 6 (a filler costs one rune). The two
  plaintext-sourced filler plants are not read (median z5 below 6): the stated power limit.
- **A4 (pages).** No member reads a page: the largest median page z5 is within 1.0 of the chance maximum, and no page reaches
  z5 ≥ 6 with readable text.

Expected: A1–A4 hold. A1 is the thing to watch; A3's two expected failures are the reason a filler-aware lattice decoder for
plaintext-sourced members is the named follow-up if Part A produces an S-admissible member among them.

## What a null means

That the text keying itself at word rate, by its numbers, or through a switch the text names, with or without fillers, neither
leaves the pages' footprints nor reads a page. It leaves the plaintext-dependent key at structures not enumerated here (a state
reaching beyond one word; the behaviours' three modes as the switch) and the lattice decoder for the filler case. Cost: under
an hour of compute on four shards; an evening of writing.

## Reproduce

`STAGE=chance|screen|confirm|decode|plants|merge .venv/bin/python -I src/autokey_lane.py` (SHARD/NSHARD on screen and decode;
SMOKE=1 shrinks everything and touches no page in the decode stage).

## Amendment (2026-10-31, night: after the smoke round-trip, before any run on the pages)

1. **Literal-ᚠ is now a bijection.** As first written, a non-ᚠ plaintext whose written rune came out ᚠ decoded as ᚠ, and
   for a plaintext-sourced key that error cascades; 182 of the 183 members failed the smoke round-trip with the rule on. The
   rule is now: ᚠ ↔ ᚠ with no state update, and the other 28 runes enciphered among themselves (indices 1–28, the key taken
   mod 28), which is what a reserved rune means in a reversible hand cipher. Round-trip exact for all 366 member settings
   on three pages. The family's count and every other definition are unchanged.
2. **The positive control's premise was wrong, and so was a published sentence.** The 3.1 × of `results/s_autokey_check.md`
   (README §47 addendum, 2026-10-30) was the corpus file: that check read Emerson from character 20,000 to the end of the
   Project Gutenberg file, and the licence text at the end repeats GUTENBERG, whose U-T and E-R stand five apart and each
   fifteen apart in Gematria order; the one word made 98 of the 196 S coincidences. On the essay body the lag-1 sub autokey
   puts S at 1.75 × uniform at within-word lag-5 coincidences (beaufort 2.3 ×), against the pages' 3.1 ×. The check, its
   companion `src/s_runkey_check.py` (figures move under half a point, conclusion unchanged) and the README are corrected in
   the same commit as this amendment. For this registration: A1's clause that the control "lands L5S inside the band (about
   eleven S pairs)" is withdrawn; the control is expected to predict about four S pairs of about sixty-six coincidences and to
   fail U and Sfreq, and its L5S z may sit inside |z| < 3 on the width of its spread as every rule's does. A1's primary
   clause, no S-admissible member, is unchanged. **Registration lesson twelve**: a plaintext corpus is its body, not its
   file; a licence or header that repeats one word fakes any within-word coincidence statistic, and the strip belongs in the
   loader, not in a character offset.
3. **This instrument's plaintext is the essay body** (the file between its START and END markers; 74,900 words). §73's and
   §74's layouts start at most 6,000 words before the file's end and the latest layout ends about eighty words before the
   licence begins, so no replicate of those sections read it; the header's four occurrences lie in the file's first 130 words,
   which a layout start reaches with probability 0.002. Their results stand; they were not rerun.

## Outcome (2026-11-01, 10:17–10:24, behind C11; README §77)

A1 holds: 0 of 1,464 S-admissible at 20 replicates; the control predicts 4.0 S pairs (z +3.2), U z −13.6, Sfreq z −3.9. A2 fails as written on one clause: 0 candidates and 0 survivors, but 56 members sit inside the L6T cell on their spread (1,408 fail it); the nearest miss on all bands is the ciphertext lag-1 autokey with fillers 0.40 and literal ᚠ on, inside eleven bands and outside L5S (+5.4) and L6T (+4.0). A3 holds: the filler-free plants and the cipher-sourced filler plant at median z5 47.8 / 33.6, rank 1 (tied with their repair-setting siblings, the same decoder); the plaintext-sourced filler plants at 1.9 and 1.4, not read, as registered. A4 holds: largest median page z5 0.55 against chance 0.38; largest single page 4.47; no page at 6; largest z\* 5.30.
