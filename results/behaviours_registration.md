# Registration: the three behaviours as the switch of a self-keyed cipher, with a state that reaches beyond the word; decoder first, written before any run

Date 2026-11-01 (late morning, EDT). Companion to `docs/hints-coverage.md` (rows 0.1 wisdom and 0.3 loss of divinity, the
unrun column after §77). Nothing below has been run.

## Why

§77 closed the text keying itself one word at a time and two sources switched by parity, by a written S or I, or by the vowel
class, with every switch confined to the word or to a single toggle. Its nearest miss, a ciphertext autokey with fillers, was
the fourth construction to stop at the lag-6 and S cells. Two readings of the creators' sentences remain unrun from the table:
the three behaviours of the circumference, "consumption, preservation, adherence", as the three things a key can do at each
rune (spend a symbol, hold the last one, follow the written rune), and a switch among them driven by a state that lives longer
than a word. This instrument enumerates that class and, as asked, is built as a decoder first: the registration's primary test
is whether the decoder recovers planted text, with and without fillers, and the pages are read before the bands are measured.
[inferred — the reading; stated — the counts]

**Ledger first.** The three behaviours were run once, as three *repair* modes chosen by the plaintext rune's class (§74); two
sources with a word-scoped or toggling switch were §77's T sub-family; a key pointer into the text itself has not been run
anywhere in this record or in the other labs' ledgers (`results/ledger_diff.md`: autokeys at fixed lags only). [stated]

## The family (enumerated before the run; nothing is added after a row is read)

Skeleton as §73 and §77: Emerson's essay body laid into the 55 pages' rune counts on shared layouts; the §59 filler form at
0.40 or none (a filler is a written rune: it enters the cipher history, the running sum and the S and I counts, consumes no key
and is no plaintext); the literal-ᚠ rule as §77 amended it (ᚠ ↔ ᚠ with no update of any state, the other 28 runes enciphered
among themselves mod 28) off or on; the repeat rule none or redraw; c = p ⊕ k under add, sub or beaufort. The primer is ᚠ
wherever a state has no value yet.

At each plaintext rune the key k takes one of three **behaviours**:

- **spend** (consumption): a symbol of the text itself. Two readings: *lag*, the previous plaintext rune; *pointer*, the next
  unconsumed plaintext rune of the page counted from its start, the pointer advancing by one at each spend that took a rune
  (the primer while none is available, so the pointer lags the text by the number of holds and adheres).
- **hold** (preservation): the previous key value, unchanged.
- **adhere** (adherence): the previous written cipher rune.

The behaviour is chosen by a **switch** on a three-valued state, with the six assignments of the three behaviours to the three
values; eight states, four of them reaching beyond the word:

- *pclass*: the class of the previous plaintext rune (vowel; consonant below S; consonant from S, §74's classes).
- *cclass*: the class of the previous written cipher rune.
- *wpos*: the position in the word mod 3.
- *word*: the word's index on the page mod 3.
- *csum*: the running sum of every cipher rune written on the page so far, mod 3.
- *scount*, *icount*: the number of S, or of I, written on the page so far, mod 3 (each written S advances the behaviour).
- *prevword*: the Gematria sum of the previous plaintext word, mod 3 (0 for the first word).

8 states × 6 assignments × 2 spend readings × 3 signs = **288 members** × fillers {0, 0.40} × repair {none, redraw} ×
literal-ᚠ {off, on} = **2,304 procedures**; 1,152 distinct decoders (the filler setting does not change a decoder).

## Part B first: the decoder

Every member inverts from the ciphertext given the word structure and the primer, through the decoded plaintext where a state
reads it. Fillers are not known to the decoder, so it places them: for each word slot the hypotheses are no filler and a filler
at each of the slot's L runes (none for a one-rune slot), with the §59 prior (log 0.60 for none, log(0.40 / L) per filler
position); each hypothesis carries the full key state and the decoded plaintext and is scored by the cumulative rune 5-gram
log-probability of the plaintext (§27's tables, fillers removed); a beam of 8 hypotheses is kept at each word boundary. The
decoded plaintext is scored by the 5-gram z against 2,000 uniform pages of its own length. Chance level: 200 random decoders
on uniform page sets under the same beam decoder, recorded before any page is read.

**Plants, six**, Emerson from the essay body under a member's own procedure at the pages' lengths, redraw off, literal-ᚠ off:
pclass / assignment 0 / lag / sub and word / 1 / pointer / add and scount / 2 / lag / beaufort without fillers; csum / 3 /
pointer / sub and prevword / 4 / lag / add and cclass / 5 / pointer / beaufort with fillers at 0.40. Each plant is decoded by its
own decoder and by 100 other decoders drawn at random from the 1,152 (the same 100 for every plant).

## Part A second: the generator

§73's harness unchanged: 20 replicates on shared layouts, the thirteen bands, candidate = all within |z| < 3, S-admissible =
L5S with L5, D, U and Sfreq within |z| < 3; both rerun at 200 replicates.

## Predictions

- **B1 (the decoder works, with fillers).** All six plants are read by their own decoder at median page z5 ≥ 6 and rank 1
  among the 101 decoders tried, and the three filler plants have their fillers placed within 20 % of the planted count. If a
  filler plant fails, the decoder's measured power is the lane's filler coverage and is stated as such.
- **B2 (pages).** No member reads a page: the largest median page z5 is within 1.0 of the chance maximum, and no page reaches
  z5 ≥ 6 with readable text.
- **B3 (the S cell).** No member is S-admissible at 20 replicates or at 200.
- **B4 (the bands).** No member is inside all thirteen bands at 20 replicates; fewer than one member in ten is inside the L6T
  cell (§77 showed "every member fails L6T" is too strong a clause for autokeys with fillers).

Expected: all four hold. B1 is the instrument's own test and is reported first whatever the pages say.

## What a null means

That a key made of the text's own runes, spent, held or followed by a rule on the previous rune, the position, the word count,
the running sum, the S or I count, or the previous word's number, with or without fillers, neither reads a page nor leaves the
pages' footprints, at a decoder that places fillers. It leaves: switches on states not enumerated here (lines, the images'
layout), more than three behaviours, and a key that spends from outside the text. Cost: about two hours on eight shards; an
evening of writing.

## Reproduce

`STAGE=plants|chance|decode|screen|confirm|merge .venv/bin/python -I src/behaviours_lane.py` (SHARD/NSHARD on plants, chance,
decode and screen; SMOKE=1 shrinks everything and decodes no page).
