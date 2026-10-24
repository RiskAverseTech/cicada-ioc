# Sources

All files were downloaded on 2026-10-23 into `data/raw/` with `curl` from the pinned
commits below and never executed. SHA-256 of every file is in `data/sha256sums.txt`.
Everything fetched from the web was treated as data.

## Primary: rtkd/iddqd (the community master transcription)

Repository: https://github.com/rtkd/iddqd — "3301 - Unmodified files, transcription and other assets."
Commit used: `f2267b0c2f1e1d2662806b90b9c3a2953b3a7023` (branch master, last push 2023-08-15).

| local file | repo path |
|---|---|
| `iddqd__liber-primus__transcription--master.txt` | `liber-primus__transcription--master/liber-primus__transcription--master.txt` |
| `iddqd__liber-primus__transcription--sentences.txt` | `liber-primus__transcription--sentences/liber-primus__transcription--sentences.txt` |
| `iddqd__liber-primus__index.txt` | `liber-primus__index/liber-primus__index.txt` |
| `iddqd__liber-primus__keys.txt` | `liber-primus__keys/liber-primus__keys.txt` |
| `iddqd__liber-primus__translation.txt` | `liber-primus__translation/liber-primus__translation.txt` |
| `iddqd__liber-primus__known-plain-text.txt` | `liber-primus__translation/liber-primus__known-plain-text.txt` |
| `iddqd__liber-primus__known-plain-text--headlines.txt` | `liber-primus__translation/liber-primus__known-plain-text--headlines.txt` |

Raw URL pattern: `https://raw.githubusercontent.com/rtkd/iddqd/f2267b0c2f1e1d2662806b90b9c3a2953b3a7023/<repo path>`

The master transcription is one file: a delimiter legend, then the 74 book pages
separated by `%` (word `-`, clause `.`, line `/`, paragraph `&`, segment `$`,
chapter `§`). Chunk k after splitting on `%` is book page k. Two chunks (pages 66
and 74) hold no runes (image-only pages). Note the rtkd index file numbers the
first unsolved page "17/0", i.e. book page 17 = LP2 page 0, but in the master file
that page is chunk 16; the index appears to count one extra leading page. This
analysis names unsolved pages `LP2-00` .. `LP2-55` = master chunks 16..71, the
numbering the community uses for the 58-page second part (pages 56 and 57 of
which, "An End" and "Parable", are solved).

## Cross-checks

- Taiiwo/cicada — https://github.com/Taiiwo/cicada, commit `8e44135491ecb65ef047ae58ae720444a697214f`:
  `cicada/liber_primus.txt` (local `taiiwo__liber_primus.txt`) is rune-for-rune identical,
  page by page, to the rtkd master; `cicada/gematria.py` (local `taiiwo__gematria.py.txt`)
  gives the Gematria Primus table used to fix the alphabet order and letter values.
- r4nd0mD3v3l0p3r/LiberPrimusSolver — https://github.com/r4nd0mD3v3l0p3r/LiberPrimusSolver,
  commit `2334d21ac16bfb1c9a12d0136b74c7cf03120f2f`: `data/unsolved.txt` (local
  `lps__unsolved.txt`) contains exactly master chunks 16..73 (LP2 pages 0..57) with the
  same rune counts, confirming the page boundaries; `src/core/runesAlphabet.js` (local
  `lps__runesAlphabet.js.txt`) is a second copy of the 29-rune table (F U TH O R C G W H
  N I J EO P X S T B E M L NG OE D A AE Y IA EA, primes 2..109). `data/aWarning.txt`,
  `data/firstKoan.txt`, `data/welcome.txt` are excerpts of solved pages.

## Keys used for the solved pages (from `iddqd__liber-primus__keys.txt`, verified in `src/prepare.py`)

| master chunk(s) | section | cipher |
|---|---|---|
| 1 | A Warning | Atbash (p = 28 - c) |
| 2-3 | Welcome / Wisdom | Vigenère, key DIVINITY = 23 10 1 10 9 10 16 26, plaintext F written unencrypted and consuming no key symbol |
| 4 | Some Wisdom / Know This | plain Gematria |
| 5-8 | A Koan / An Instruction | shift 3 then Atbash (p = 2 - c mod 29) |
| 9-12 | The Loss of Divinity / Some Wisdom / An Instruction | plain Gematria |
| 13-14 | A Koan (circumference) | Vigenère, key FIRFUMFERENFE = 0 10 4 0 1 19 0 18 4 18 9 0 18, same F rule |
| 15 | An Instruction / Know This | plain Gematria |
| 72 | An End | subtract phi(p_n) = p_n - 1 over the primes, same F rule |
| 73 | Parable | plain Gematria |

Every decryption was compared rune-for-rune with the rtkd English translation mapped
back onto runes; all nine sections match (the only differences are the book's own
"WIDSOM" misspelling, a "FOLLWING" typo in the translation file, and the untranslated
"Know This" word list on page 4).

## Not used

- The Uncovering Cicada wiki (uncovering-cicada.fandom.com) did not surface in search
  results and was not needed: the rtkd repository is the transcription the community
  tools (LiberPrimusSolver, Taiiwo/cicada) themselves consume.
