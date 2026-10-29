# Blind spots: the record read from the designers' side

*Written 2026-10-29, after §61's registration. Everything here is opinion and is tagged inferred; it is kept so that the
next lanes are chosen against the strongest critique of the work rather than the most convenient one. Revisit after each
lane that touches an item and append a dated note under it rather than rewriting.*

## The critique in one sentence

The record treats the Liber Primus as a ciphertext and never as a book. Sixty-one sections and 883 million decoder tests
ask one question in different costumes: is this English under an additive rune key with small tweaks? The authors published
the mechanism of the solved pages so that a solver would learn it, and then said, three years later, that the words are the
map, their meaning is the road and their numbers are the direction. §53 ran that sentence as a keystream. It is not a
description of a keystream. [inferred]

## The five blind spots, in the order a designer would enjoy pointing at them

### 1. Every scorer assumes natural-language plaintext

What the record does: every decode lane, in every lab cross-referenced here, scores a candidate decryption with an English
rune model (unigram, then the 5-gram of §27), or with Latin and Old English in phase 5. What it cannot see: a page whose
content is numbers, coordinates, a list, runic numerals, or runes standing for digits of something. The word-length
fingerprint of §55 fits "English with a filler in 40 % of words" (§59) and the record reads it that way because fillers
were in view; it fits "not prose" at least as well, and §55 says so in one clause. **The lane:** a scorer built from
expected non-prose tokens (number words in the book's spelling, runic and Gematria numerals, the book's own vocabulary, the
digits and hex of the page-73 hash and the PGP fingerprint, prime and totient sequences spelled out), run through the
existing plain, free-null and word-constrained decoders over the small libraries. Cost: a day. Ledger check: none of the
registries read here scores against a non-prose model; verify before claiming it. [inferred]

### 2. The decoders add rune indices; the Gematria Primus is a table of primes

What the record does: the combine operation in every lane is index addition or subtraction modulo 29 (with Beaufort and the
quagmire alphabets of §32). Phase 9 used cumulative Gematria value as a feedback term into an index cipher. What it cannot
see: a cipher whose arithmetic is on the prime values themselves (sum of primes reduced modulo 3301, 1033, 29 or the next
prime, mapped back to the rune whose value is nearest or equal), which is not a bijection of index addition, so no additive
sweep sees it and the repeat deficit survives it untouched. The authors' published aesthetic is exactly this arithmetic.
**The lane:** value-arithmetic combine operations as a small family (a handful of reductions and back-maps), under the
soft rule, over the book's keys and the prime streams. Cost: a decoder hook and a day. Ledger check: pnotisdev's
`prime-value` rows are feedback terms, not combine operations, on the 2026-10-28 reading. [inferred]

### 3. The sparse-message world

What the record does: the filler lanes (§22, §55, §60, §61) imagine mostly plaintext with some unkeyed runes. What it cannot
see: the opposite, mostly cover with a message selected by a rule, which is what "the numbers are the direction" means if
taken literally. A repeat deficit blind to word, line and clause boundaries (§33) is what a cover generator with a
no-doublet rule leaves behind, and a selected subsequence would carry none of the structures measured here. **The lane:**
rule-selected subsequences of the whole unsolved section (positions that are prime, totient, cumulative-Gematria
multiples, the solved pages' numbers, every nth rune for small n, the red runes) read under the solved mechanism and plain.
Deterministic, hours. Ledger check: pnotisdev's `layout27` and layout rows and Dukotah's position lanes first. [inferred]

### 4. The mechanism story is epicycles

What the record does: E56w+n (§58, §59) reproduces every pre-registered band but the S count with four fitted or borrowed
components: a gated echo in half the words, a filler in 40 %, a spend repair at 0.81, an iid key. What a designer sees: a
Ptolemaic fit to one operation they performed, probably by hand, probably with a table. A relation of the form 24 − 2c at
lag 6 is the shadow of a lookup geometry, not a property of English. **The lane:** not another component; a search for one
process that leaves all four footprints (deficit, lag-5 equality carried by S, lag-6 affine, long words), beginning with
tabula geometries in which S and EO (the fixed point of c ↦ 24 − 2c) sit at distinguished positions, and hand-copying
rules. Cost: thought first, simulation second. [inferred]

### 5. False paths

The authors warned of them in 2016. Eleven S pairs have absorbed six sections. If any structure here was salted, it is the
one that is small, striking and resistant to every mechanism. The record keeps the S carrier as the open fact (§47, §50,
§59); it should also keep the possibility that it is bait, and spend on it accordingly. [inferred]

## What they would not fault

The controls, the registrations, the published failed predictions (§49, §57, §59, §60), and the filler result, since nulls
are a trick the solved pages already use. The critique is not that the work is sloppy. It is that it is thorough in one
direction. [inferred]

## Order of the next lanes, by this reading

1. The non-prose scorer (blind spot 1), because it is the one assumption shared by every negative in every lab.
2. Value arithmetic as the cipher (blind spot 2), because it is small and it is theirs.
3. The selection rule (blind spot 3), because it is deterministic and cheap.
4. The one-process search (blind spot 4), as thinking rather than sweeping.

Each is pen-and-paper sized. None needs more than the eight cores this record has used throughout.
