# Fillers planted on the solved pages under their own keys (row C6)

The solved pages' English (rtkd translation, pages 0.1 and 0.2) in rune spelling, cut into page-length pieces and enciphered with DIVINITY and FIRFUMFERENFE (C = P + K, every rune keyed) after planting the §59 filler form (one extra rune in 40% of words of ≥ 2 runes, uniform slot, key not consumed), 20 replicates each; decoders over the phase-3 Vigenère-word family (269 keys) plus the true key; z over 400 random keystreams. Rep 0 is the piece without fillers.

| page | decoder | no fillers: z / rank / acc | with fillers: recovered (z ≥ 6, rank 1) | median z | median acc on real runes | fillers planted → placed by the word-constrained decoder (median) | planted filler words found (wc) |
|---|---|---|---|---|---|---|---|
| translation 0.1 piece 1 (DIVINITY) | plain | 11.1 / 1 / 1.00 | 0.00 | 2.7 | 0.31 | 25 → — | — |
| translation 0.1 piece 1 (DIVINITY) | free-null | 15.6 / 1 / 1.00 | 1.00 | 11.8 | 0.87 | 25 → — | — |
| translation 0.1 piece 1 (DIVINITY) | wc | 14.8 / 1 / 1.00 | 1.00 | 10.6 | 0.88 | 25 → 24 | 0.80 |
| translation 0.1 piece 2 (DIVINITY) | plain | 11.8 / 1 / 1.00 | 0.05 | 4.2 | 0.32 | 23 → — | — |
| translation 0.1 piece 2 (DIVINITY) | free-null | 17.6 / 1 / 0.97 | 1.00 | 12.7 | 0.88 | 23 → — | — |
| translation 0.1 piece 2 (DIVINITY) | wc | 16.2 / 1 / 0.97 | 1.00 | 11.2 | 0.89 | 23 → 23 | 0.81 |
| translation 0.2 piece 1 (FIRFUMFERENFE) | plain | 12.9 / 1 / 1.00 | 0.00 | 1.4 | 0.26 | 28 → — | — |
| translation 0.2 piece 1 (FIRFUMFERENFE) | free-null | 22.3 / 1 / 1.00 | 1.00 | 15.1 | 0.95 | 28 → — | — |
| translation 0.2 piece 1 (FIRFUMFERENFE) | wc | 19.7 / 1 / 1.00 | 1.00 | 13.7 | 0.95 | 28 → 27 | 0.90 |
| translation 0.2 piece 2 (FIRFUMFERENFE) | plain | 11.7 / 1 / 1.00 | 0.00 | 1.9 | 0.26 | 26 → — | — |
| translation 0.2 piece 2 (FIRFUMFERENFE) | free-null | 19.6 / 1 / 1.00 | 1.00 | 13.6 | 0.94 | 26 → — | — |
| translation 0.2 piece 2 (FIRFUMFERENFE) | wc | 18.9 / 1 / 1.00 | 1.00 | 12.9 | 0.95 | 26 → 25 | 0.90 |

Reading: on the book's own plaintext under the book's own keys the §59 filler form removes the key from the plain decoder on 79 of 80 replicates (median z 1.4–4.2 against 11–13 without fillers; rune accuracy 0.26–0.32), and both filler decoders keep it on 80 of 80 (median z 10.6–15.1, accuracy 0.87–0.95). The word-constrained decoder places the planted filler count within one on every piece and finds 80–90 % of the filler words. This is §60's result reproduced on real text with real keys rather than on plants from a corpus; it adds no evidence about the unsolved pages, where the same two decoders found nothing (§55, §61). [stated — the table]

Runtime 3400 s. Reproduce: `.venv/bin/python -I src/solved_fillers.py`.
