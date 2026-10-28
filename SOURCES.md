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

## External running-key corpus (fetched by hand 2026-10-27; `src/corpus.py` builds `data/corpus/corpus.json`)

Raw files in `data/corpus/raw/` are committed where public domain; Gibson's *Agrippa* is under copyright and only its hash is recorded (file gitignored).

| file | SHA-256 | source |
|---|---|---|
| agrippa_gibson_diskimage.txt | d404a19157557a27a0438b657dfe6d71d8181da0c1a2c6a92b3197fa0df2b056 | https://agrippa.english.ucsb.edu/wp-content/uploads/images/emulation/diskimage-analysis/freek/agrippa-poem-extracted-from-diskimage.txt (copyrighted; not committed) |
| blake_mhh_wikisource.json | 90aeff70c035fa5281d9242baa61716a5f4035001622e632dfc453614de65e2a | https://en.wikisource.org/wiki/The_Marriage_of_Heaven_and_Hell (API action=parse) |
| bulfinch_age_of_chivalry_pg4926.txt | 6372dea2a04426db725fc645ee1c6c360bd75be65a28f4d047f564ad5d192d4d | https://mirrors.xmission.com/gutenberg/4/9/2/4926/4926.txt (Project Gutenberg #4926) |
| cypherpunk_manifesto.html | e63fe33f5de9f49b842d02d3d8e42c5f132edb480d6c2173b54084bcf090afe1 | https://www.activism.net/cypherpunk/manifesto.html |
| emerson_essays1_pg2944.txt | c38b1203b6acc456dc038279868649f656acd80eea90a8c8c92e2c3808cd91da | https://gutenberg.pglaf.org/2/9/4/2944/2944-0.txt (Project Gutenberg #2944) |
| king_in_yellow_pg8492.txt | e1f3f545b2d0f681181e169479aa6e3d3097004108d51eb198cf19cf686944c8 | https://gutenberg.pglaf.org/8/4/9/8492/8492-0.txt (Project Gutenberg #8492) |
| kybalion_pg14209.txt | a9aa0a3ec5b60c630cab7ad0817f0d3253503fe8fff5b56d3d73813333bd62ca | https://gutenberg.pglaf.org/1/4/2/0/14209/14209-0.txt (Project Gutenberg #14209) |
| liber_al_wikisource.json | 0a2a0180e1e459a6db8b9bf620278414b7e9cfbd4cd12d8e0fdd8d3b74aae9c3 | https://en.wikisource.org/wiki/Liber_AL_vel_Legis (API action=parse, rendered page) |
| mabinogion_guest_pg5160.txt | 80dc6f0d8efc8398a2d1cc8cdf17237020c881cf4fbd2412dfa37ec8be19a5ed | https://gutenberg.pglaf.org/5/1/6/5160/5160-0.txt (Project Gutenberg #5160) |
| rune_poem_wikisource.json | 8d8998cda226badf8c5378039ab54e16dd5afa0f6f2a6cae82f885a6d3707f4e | https://en.wikisource.org/wiki/Runic_and_Heroic_Poems_of_the_Old_Teutonic_Peoples/The_Runic_Poems/The_Anglo-Saxon_Runic_Poem (API action=parse) |

Rune counts per text and both transliteration conventions: `data/corpus/CORPUS.md`.

## Page images (fetched 2026-10-27; `src/image_lane.py`, README §26)

scream314/cicada3301, `assets/2014/liber-primus-complete/00.jpg` … `74.jpg` (75 pages, 2400 × 3600)
and their thumbnails, fetched from `https://raw.githubusercontent.com/scream314/cicada3301/master/<path>`
(repository HEAD pushed 2023-06-06). Image NN is master-transcription chunk NN − 1; unsolved LP2-k is
image 17 + k. The 54 MB of files are gitignored; `data/images/SHA256SUMS.txt` holds every file's
SHA-256 and `data/images/filelist.tsv` the archive paths and sizes.

## PGP key and signed messages (fetched 2026-10-27; `src/verify_pgp.py`, `docs/pgp-verification.md`)

Public key `data/raw/pgp/cicada_7A35090F_pubkey.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/6D854CD7933322A601C3286D181F01E57A35090F.
Messages from wazar/cicada3301 `corpus/A-primary-artifacts/` (pgp/messages/2012-01-necrome-denial.asc, ibotpeaches/messages/2016/hello-the-path-lies-empty.asc, ibotpeaches/messages/2017/beware-false-paths.asc). SHA-256 in `data/raw/pgp/SHA256SUMS.txt`.

## Pilgrim corpus (fetched 2026-10-28; `CORPUS_SET=pilgrim src/corpus.py`, README §40)

`data/corpus/raw/bunyan_pilgrims_progress_pg131.txt` from https://gutenberg.pglaf.org/1/3/131/131-0.txt (Project Gutenberg #131); `data/corpus/raw/chaucer_canterbury_pg2383.txt` from https://gutenberg.pglaf.org/2/3/8/2383/2383-0.txt (#2383). Rune counts in `data/corpus/CORPUS_pilgrim.md`.
