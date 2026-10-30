# Registration: rule-selected subsequences, the sparse-message world (2026-10-30, before any run)

**Why.** Every lane in this record and in the ledgers read reads every rune of a page as message (with the filler world of §55–§61 as the one exception, where the extra runes sit at random positions). A designer who meant only some runes to be read, by a deterministic rule, leaves the rest as cover: the page's statistics are then a mixture, the plain decoders see noise, and the message is shorter and cleaner than the page. The ledger diff lists position formulas as *key* material (a·n+b, n², cumsums) and transposition / reading order, but no row anywhere selects a subsequence as the message. `docs/blind-spots.md` §3; private table A4.

**Rules (fixed here, all deterministic, position-only).** On each page's rune sequence (positions 0…n−1, '/' line breaks and word separators from the master transcription):
- index sets: primes; composites; squares; triangular numbers; Fibonacci numbers; every k-th rune for k = 2…7 at every residue r < k (27 sets); positions i with i mod 3301 ... (none, pages are shorter) — 32 sets, each also from the page's end;
- layout sets: first rune of each line; last rune of each line; first rune of each word; last rune of each word; every rune not first or last in its word (the word interiors); the one-rune and two-rune words concatenated;
- complements of the index sets (the cover read as message).
The rules are enumerated in the script header; the count is printed in the result.

**Statistics, per rule, pooled over the 55 pages' selected runes.**
S1 index of coincidence (× 29) and adjacent-repeat rate of the selected stream; null: the same rule on 1,000 per-page shuffles of the runes.
S2 in-clear test: rune 5-gram log-probability of each page's selected stream against 2,000 random rune strings of the same length (`ngram`), reported as the pooled z over pages.
S3 decode test: each page's selected stream as a Vigenère ciphertext under the book's 7,621 keys × 3 signs × 2 F with the plain decoder (soft rule), z by 2,000 random keystreams; a hit is z ≥ 6, rank 1 in its family, readable.

**Controls.** Six plants: an English passage written into a 263-rune page at the positions of a rule (two index rules, two layout rules, one complement, one every-k-th), the remaining positions uniform cover, three in clear and three under a book Vigenère word with the soft rule; S2 must find the clear plants (z ≥ 6 on their rule, rank 1 among the 96 rules) and S3 the keyed ones.

**Expected: null.** S1 at the shuffle null for every rule (the positional IoC of §55 part A was flat); S2 below 6 everywhere; S3 nothing at the bar. Claims: Q1 controls 6/6; Q2 no rule's pooled S2 z ≥ 6; Q3 no rule's S1 IoC z ≥ 4 against the shuffle null (96 rules, look-elsewhere about 2.9); Q4 no S3 candidate. If Q2 or Q3 fails on a rule, that rule's selected text is printed in transliteration and judged by eye before anything is said; if Q4 fails, the candidate is run through `check_solve.py`.

**Coverage limits stated now.** Position-only rules on the transcription's rune order; no rule that depends on the rune values (a self-selecting rule is the hypothesis-loop's territory); no rule crossing pages; selected streams under 40 runes are reported but not decoded. Budget: S1–S2 minutes; S3 about 96 × 55 × 45,726 keys ≈ 240 M short decodes, tens of minutes on eight cores at the selected lengths.
