# Registration: value arithmetic as the cipher (2026-10-31, before any run)

**Gap.** Every decoder in this repository and in the ledgers combines plaintext and key by rune *index*: addition in the three signs, and the affine form c = a·p + k (§48 here, LZ's non-additive combiner, Dukotah's word-level affine, all closed). The Gematria Primus assigns each rune a *prime* (2 … 109), and the designers' own documented arithmetic is on those values (word sums, "the primes are sacred", the totient). Feedback through the prime value of the previous rune is closed (LZ six variants, WZ value / prime-index / totient streams); the cumulative value as a *key source* is §20 here. Combining the plaintext's and the key's prime values as the operation itself has not been run anywhere the ledgers show.

**Family** (`src/value_lane.py`). Value maps V: the prime, and the totient prime − 1. Operations: V(p) + V(k), V(p) − V(k), V(k) − V(p), V(p) · V(k). Reduction: the value modulo M for M ∈ {29, 110, 113} (29 the alphabet, 110 one past the largest prime, 113 the next prime), then modulo 29 as the cipher rune's index. 2 × 4 × 3 = 24 rules; none is a bijection in p for fixed k, so the decoder takes, at each (c, k), the best candidate plaintext under the English unigram model and a finite penalty (−8 nats) where c is unreachable under k. The decoder is `score.decode` with the new `table / tgain / enc` hook: the soft reject-on-repeat skip (the condition becomes enc[P, K_(j−1)] = C_(i−1)), literal F on and off, the same Viterbi. A test fixes that the hook with the additive table reproduces the plain decoder exactly.

**Keys.** The book's 7,621 keystreams (§9/§12 phrase and word sets, as raw rune indices) and the prime streams p[n+s], p[n+s] − 1, p[n+s] + 1 for s = 0 … 999 (3,000), under each rule the key rune's value is V(k) where k is the stream's rune index, so a prime stream enters by its index as everywhere else. 10,621 keys × 24 rules × 2 F × 55 pages ≈ 28 M full-page decodes, plus 400 random keys per (page, rule, F) for the null.

**Acceptance.** z ≥ 6 against the cell's 400-key null, rank 1, readable by eye, and above the largest z among all null draws of the rule (the empirical maximum, reported). Rows within 1.5 of the bar are printed in transliteration.

**Controls.** Six plants: English at page length enciphered under six of the rules (every operation at least once, both value maps, two moduli) with a random book key and the soft rule at 0.81, decoded under the plant's own rule over the 7,621 book keys: each must come first at z ≥ 6. The equality test of the hook is the seventh control.

**Claims.** V1: controls 6/6. V2: no candidate. **Expected: null**; the solved pages used index arithmetic and nothing in the book points at a value cipher, but the family is small and it is the designers' own material, so it is run once, fully, and closed.

**Budget.** Eight shards over pages, about an hour.
