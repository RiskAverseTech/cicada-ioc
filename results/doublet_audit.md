# Doublet audit

Doublet = the same rune twice in a row. Two nulls: iid uniform (rate 1/29 = 0.0345), and a within-page
shuffle that keeps each page's rune frequencies (rate ≈ that text's own index of coincidence).

| text | runes | adjacent pairs | doublets | rate | z vs uniform | shuffle mean ± sd | z vs shuffle | IC |
|---|---|---|---|---|---|---|---|---|
| solved plaintext (decrypted) | 2977 | 2968 | 77 | 0.0259 | -2.5 | 186 ± 13 | -8.6 | 0.0614 |
| solved ciphertext (as transcribed) | 2977 | 2960 | 75 | 0.0253 | -2.7 | 163 ± 12 | -7.2 | 0.0397 |
| unsolved ciphertext | 12956 | 12901 | 86 | 0.0067 | -17.3 | 439 ± 21 | -17.1 | 0.0345 |

Solved ciphertext by page (cipher from the published keys):

| page | cipher | pairs | doublets | expected uniform | z |
|---|---|---|---|---|---|
| 1 | Atbash | 183 | 5 | 6.3 | -0.5 |
| 2 | Vigenère DIVINITY | 250 | 8 | 8.6 | -0.2 |
| 3 | Vigenère DIVINITY | 263 | 8 | 9.1 | -0.4 |
| 4 | plain | 156 | 7 | 5.4 | +0.7 |
| 5 | shift 3 + Atbash | 208 | 4 | 7.2 | -1.2 |
| 6 | shift 3 + Atbash | 209 | 3 | 7.2 | -1.6 |
| 7 | shift 3 + Atbash | 217 | 5 | 7.5 | -0.9 |
| 8 | shift 3 + Atbash | 140 | 2 | 4.8 | -1.3 |
| 9 | plain | 186 | 7 | 6.4 | +0.2 |
| 10 | plain | 206 | 5 | 7.1 | -0.8 |
| 11 | plain | 191 | 3 | 6.6 | -1.4 |
| 12 | plain | 168 | 3 | 5.8 | -1.2 |
| 13 | Vigenère FIRFUMFERENFE | 225 | 6 | 7.8 | -0.6 |
| 14 | Vigenère FIRFUMFERENFE | 92 | 3 | 3.2 | -0.1 |
| 15 | plain | 88 | 3 | 3.0 | -0.0 |
| 72 | totient prime stream | 84 | 2 | 2.9 | -0.5 |
| 73 | plain | 94 | 1 | 3.2 | -1.3 |

## Transcription conventions

The master file separates words with '-', clauses with '.', lines with '/', paragraphs with '&', segments with '$'. Phase 1 drops all of
them, so adjacency across a word or line boundary counts exactly as adjacency inside a word, for the observed pages and for the shuffle
null alike. Digits (572) and Latin letters (252) in the file mark page numbers and drawings and carry no runes. Doubled letters in the solved
plaintext are written as two runes (the decrypted plaintext has 77 doublets, rate 0.0259), so nothing in the
transcription or the Gematria Primus convention removes repeats from the text itself.

Unsolved pages, doublets split by whether a separator sits between the two runes:

| position | adjacent pairs | doublets | expected uniform | rate |
|---|---|---|---|---|
| inside a word | 9640 | 60 | 332.4 | 0.0062 |
| across a boundary | 3261 | 26 | 112.4 | 0.0080 |

## Ciphertext-autokey decrypt of the unsolved pages

Under K_i = C_{i-k}, the plaintext is P_i = C_i - C_{i-k} (mod 29). If that were the cipher, this stream would look like
plaintext: IC near 0.0614, E at 0.128, F at 0.016. Under lag 1 a ciphertext doublet is exactly a recovered F.

| lag k | runes | IC of recovered stream | top rune (share) | share of F | KL(recovered ‖ plaintext) | KL(recovered ‖ uniform) |
|---|---|---|---|---|---|---|
| 1 | 12901 | 0.0353 | N (0.040) | 0.0067 | 1.152 | 0.0189 |
| 2 | 12846 | 0.0345 | G (0.037) | 0.0339 | 1.154 | 0.0008 |
| 3 | 12791 | 0.0345 | M (0.038) | 0.0339 | 1.180 | 0.0011 |
| 4 | 12736 | 0.0345 | N (0.039) | 0.0354 | 1.181 | 0.0009 |
| 5 | 12681 | 0.0345 | OE (0.037) | 0.0365 | 1.197 | 0.0010 |

At lag 1 the recovered stream's unigram chi-square against uniform is 343 on 28 dof
(almost all of it from the missing F); against the solved plaintext's distribution the fit is far worse. The recovered stream is a
flat distribution with one hole, not a language.

## Decision

- The solved plaintext has a mild doublet deficit against uniform (rate 0.0259, z -2.5) and a strong one against its own
  shuffle (z -8.6), which is ordinary English behaviour: letters repeat less often than independence predicts.
- The solved ciphertext, enciphered with the book's own short-key and stream methods, sits at the uniform rate (rate 0.0253, z -2.7).
- The unsolved ciphertext is at rate 0.0067, z -17.3 against uniform and z -17.1 against its own shuffle: a fivefold deficit that
  neither the plaintext nor the transcription nor the book's known ciphers produce.
- Within words and across word boundaries the deficit is the same, so it is not a word-level writing rule.
- Simple ciphertext autokey (any lag 1 to 5) does not decrypt to anything plaintext-like.

**The deficit is cipher structure.** Whatever generates the unsolved pages makes the next rune avoid the previous one far more
often than an additive cipher with an independent key can. The mechanism simulation (doublets.py) asks which constructions do that.
