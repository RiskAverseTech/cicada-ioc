# §61 pre-registration: the word-constrained filler decoder, its power and false gain, and the small libraries under it (written 2026-10-29, before any plant was scored under it beyond the unit tests and before any page was decoded)

## Why

§59 fitted the filler form to the word lengths: one extra rune at a uniform position in 40 % of the words of two or more
runes, so at most one filler per word. §55's free-null decoder lets any rune be a filler and, on a wrong key over a full
page, gains about 110 nats on noise, which is why its margin arm filtered nothing. §60 found that decoder recovers more
per-word plants than per-rune plants at equal filler count (0.75 against 0.68). The constraint is information a decoder
can carry. This lane builds that decoder, measures what the constraint buys on §60's own plants, calibrates its false
gain on wrong keys at page length, and runs the small libraries under it: the ones an author with a taste for elegance
would have used, which every lane so far decoded plain.

## The decoder (`src/wc_decode.py`, `tests/test_validation.py`)

`score.decode` under rejection "one" (soft skip-on-repeat with up to four rejections, literal F, modes sub and beaufort)
with one extra bit of state: "a filler has been used in this word", reset at each word start; the null transition (rune
written as itself, no key consumed, gain 0, cost = log prior) is available only while the bit is clear. Two priors:
**fixed −2.2** (§55's) and the **§59 word prior** at p = 0.40, ln(p/(1 − p)) − ln(cipher word length) per position. Tests,
passing before this file was written: with nulls disabled it equals `score.decode` exactly (both modes, both F variants);
with every rune its own word it equals the free-null decoder exactly; on a plant with one filler in 40 % of words it
ranks the true key first among 60, decodes 90 % of the real runes, places exactly the planted number of fillers and never
two in one word. Cost at 230 runes, 1,000 keys: plain 0.6 s, free-null 5.1 s, word-constrained 2.3 s.

## Part A: power on §60's plants (`src/wc_power.py`, PART=A → `results/wc_power.md`)

§60's loop rerun verbatim with the same seeds and shard plan, so the 108 plants and their eight filler cells are the
same runes; the plain and free-null decoders are rescored (their z must reproduce §60's to the digit, reported) and the
two word-constrained decoders are added after them. Recovered = z ≥ 6 over 400 random keystreams through the same
decoder and rank 1 in the family, as §55/§60. **Prior decision**: the prior with more recoveries over the 108 plants at
p = 0.4 is the lane's prior for parts B and C (ties to −2.2).

| claim | pass if |
|---|---|
| A1 the constraint buys power where the data say it should | at p = 0.4, pooled power of the chosen word-constrained decoder ≥ the free-null decoder's on the same plants (0.75 in §60) |
| A2 and loses none by cell | at p = 0.4, no (n, family) cell of the chosen decoder below the free-null decoder's by more than 0.17 (two plants) |
| A3 it degrades gracefully when the constraint is violated | at r = 0.10 per rune (14.8 fillers, some words with two), pooled power ≥ 0.50 |
| A4 it costs nothing without fillers | at r = 0, pooled power within 0.05 of the plain decoder's (0.92) |
| A5 it has window power | at n = 160, p = 0.4, pooled power ≥ 0.70 (the tier-1 window of part C) |

Expected: A1–A5 hold, with the chosen decoder near 0.85 at p = 0.4 and 0.55–0.65 at r = 0.10.

## Part B: false gain on wrong keys at page length (`src/wc_power.py`, PART=B → `results/wc_margin.md`, `results/wc_nulls.json`)

For each of the 55 pages, both F variants and both modes (220 cells), 2,000 random keystreams through the plain, free-null
(−2.2) and both word-constrained decoders; recorded per cell: each decoder's null mean and sd (reused as the sweep's
null), and the 50th, 90th, 99th, 99.9th percentiles and maximum of the gain over the plain score for the free-null and
word-constrained decoders. **The margin** M(page, F, mode) is the 99.9th percentile of the chosen decoder's gain on that
cell's random keys.

| claim | pass if |
|---|---|
| B1 the constraint halves the false gain | median over the 220 cells of the 99.9th-percentile gain: chosen decoder ≤ 0.6 × free-null's |
| B2 the margin arm discriminates | the median true-key gain of the chosen decoder on the 36 plants at n = 230, p = 0.4 (part A) exceeds the median M over the cells with 200–277 runes |

Decision fixed now: if B2 fails, part C's candidate rule drops the margin arm and z plus readability decide; the drop is
recorded in the write-up. Expected: free-null 99.9th-percentile gain near +110 (§55), word-constrained near +50, true-key
gain at p = 0.4 near +80: B1 and B2 hold.

## Part C: the small libraries (`src/wc_lane.py` → `results/wc_lane.md`)

All under the chosen word-constrained decoder, the real pages' word edges (§42's corrected convention: `/` is a line
break, not a boundary), both F variants, the three sign conventions.

1. **The book's keys**: `families.ALLSETS`, 7,621 keys × 3 signs (the phase-3 families: the two solved words DIVINITY
   and FIRFUMFERENFE and every other Vigenère word of the book both directions, shifts, affine and square positions,
   Fibonacci and Lucas, the self running key, primes and primes ± 1 at the library's offsets; and the phase-4 phrase and
   sentence keys), × 2 F, every page at full length: 2.5 million page decodes.
2. **The prime streams with the literal-F rule** (the solved pages' own mechanism) and without it: p[n+s], p[n+s] − 1 and
   p[n+s] + 1 for s = 0 … 19,999, 3 signs, 2 F, every page at full length: 19.8 million page decodes.
3. **The sixteen external texts** in §55 C's units (ten texts at every offset in both directions, six longer texts at
   their sentence starts forward), tier 1 on the first 160 runes of LP2-00, LP2-01, LP2-02 × 3 signs × 2 F at z ≥ 4.5 over
   that window's null of 2,000 random keystreams through the same decoder; offsets within ±3 in one text and direction
   are one hypothesis: about 19.5 million window decodes.

**Candidate rule** (full page, for a page decode in 1–2 or a tier-1 survivor in 3): z ≥ 6 over the page's 2,000 random
keystreams through the chosen decoder (part B's null, same F and mode), AND gain over the plain decoder ≥ M(page, F, mode)
(unless dropped by B2), AND readable English in the decoded page, judged by eye and recorded. Chance maximum of z over
the tests: about 5.5 (1), 5.8 (2), 5.8 (3). **Controls** (six, 262-rune English under the §59 form at p = 0.4 with the
soft rule): two book Vigenère words, two prime streams at random offsets (one with literal F), two running keys at
random offsets; pass = rank 1 in its family (every word key; offsets within ±2,000; the 4,096 neighbouring offsets) and
the candidate rule met.

Expected result: null in all three. Coverage limits to be stated from part A (power at 230 and 160 runes under the §59
form) and part B (the margin). Budget: about four hours on eight cores.

## Not in this lane

The phase 5–9 families, pnotisdev's libraries and the longer texts away from sentence starts under this decoder; a
filler decoder for the per-rune form; the register question (verse or a list). Each is its own registration.
