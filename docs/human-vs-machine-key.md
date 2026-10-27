# Was the anti-repeat key made by a person or a program? (note, 2026-10-27)

The one measurable property of the unsolved pages is that a rune follows itself 86 times where
445 are expected (README §4–§5). A key that is redrawn when it would repeat the previous output
reproduces that and nothing else. This note asks what kind of generator has that habit, because
people and programs leave different fingerprints, and some of them are already measured.

## What a human hand would leave

The avoidance of immediate repeats is the best-replicated bias in human-generated "random"
sequences (Wagenaar 1972; Bar-Hillel and Wagenaar 1991; Nickerson 2002, reviews). The same
literature records two companions that come with it:

1. **Near-repeat avoidance.** People also thin out A-B-A patterns, more weakly than A-A.
2. **Local balancing.** People keep short windows more evenly populated than chance (too few
   long runs of any kind, lower short-window dispersion), the gambler's-fallacy signature.

A program with a one-line rejection step (`while c == prev: redraw`) leaves neither.

## What the pages show

| test | measured (README section) | human prediction | one-lag rule prediction |
|---|---|---|---|
| lag-1 repeats | 86 vs 445 expected (§4) | deficit | deficit |
| lag-2 repeats | 435 vs 443 expected (§21 premises) | deficit, weaker | none |
| lag-3, lag-4 repeats | 434 vs 441, 451 vs 439 (§21) | small deficit fading | none |
| suppression rate across pages | homogeneous, dispersion chi² 59 on 55 dof (§21) | drifts with fatigue and attention | constant |
| rune-blind | chi² 28 on 28 (§21) | repeats of "salient" runes avoided more | blind |

Three of four discriminating rows fall on the machine side; none falls on the human side. The
lag-2 row is the strong one: a hand that avoided A-A four times in five would not leave A-B-A
exactly at chance.

## What would settle it

- **Short-window dispersion of the key's differences.** Not directly observable (the key is
  masked by the plaintext), but the ciphertext difference stream C_i − C_{i−1} inherits the key's
  balancing if any; its lag-1 class chi² is already flat (§5, 42 against a flat expectation).
  A windowed version of that test, 50-rune windows, would show the gambler's-fallacy
  under-dispersion if a hand made the key. Not yet run.
- **The soft rate itself.** A program's rejection step is usually all-or-nothing; the pages show
  four in five. A program draws a *fresh* uniform rune and re-tests only once would give a
  "soft" rate of 1 − 1/29 ≈ 0.966, not 0.81. A rate of 0.81 is what you get from a rule that
  rejects a repeat with probability 0.81, or from a generator that re-draws only when some
  second condition holds. That constant is the most specific thing known about the generator
  and no construction in this repository explains why it is 0.81 rather than 1.

## Why it matters

If the key is a program's output, the program had a seed and a state, and the search is for
the generator (the LCG, PRNG and KDF families the labs have swept, §18–§19, wazar Round 16).
If it is a hand, there is nothing to find but the pad itself. The measurements above make the
program reading the better bet, which is why the generator families remain worth closing even
after the key-text families are done.

## References (as context, not sources for any number above)

Wagenaar, W. A. (1972). Generation of random sequences by human subjects: a critical survey.
*Psychological Bulletin* 77, 65–72. Bar-Hillel, M., & Wagenaar, W. A. (1991). The perception of
randomness. *Advances in Applied Mathematics* 12, 428–454. Nickerson, R. S. (2002). The
production and perception of randomness. *Psychological Review* 109, 330–357.
