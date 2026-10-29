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

## Cicada's own words, 2012–2017 (added 2026-10-29, §53)

`data/corpus/raw/cicada_own_words_2012_2017.txt`: the bodies of every PGP-signed Cicada message from 2012 to 2017 (25 distinct) and four quoted unsigned texts (the 2012 and 2013 opening images, the 2013 parable from the 761.mp3 ID3 tag, the 2016 outguess text), 1,592 words, extracted by script from the year narratives of github.com/scream314/cicada3301 (`2012.md`–`2017.md`, read as data). Each text is labelled with its year and status in square brackets; the labels are stripped before use. SHA-256 of the assembled text: c494a45c025ed15d…. Used as running keys (`CORPUS_SET=cicada`) and as a word and phrase key library (`src/cicada_words_lane.py`).

## pnotisdev's keystream library and registry (fetched 2026-10-28; `src/pnotisdev_library.py`, `src/cross_library_lane.py`, README §54)

Repository: https://github.com/pnotisdev/cicada3301, commit `15200c67abee106913ba01ff504c5b6e88d16cc7` (2026-10-24). Files fetched with `curl` from
`https://raw.githubusercontent.com/pnotisdev/cicada3301/15200c67abee106913ba01ff504c5b6e88d16cc7/<path>` into `data/external/pnotisdev/` (gitignored) and read as
data; nothing of theirs is executed. Their binary library export (`work/kscreen/data/library.ksb`, "KSB1") is not in their repository, so the 1,439 streams were
rebuilt here from the generator definitions below on this repository's copy of the rtkd/iddqd master transcription with their six errata applied; the rebuild is
checked against the first runes of the six model-0 decodes in `library_segments_verify.txt` (all six reproduce) and against `data/processed/irrational_digits.json`.
Per-stream SHA-256 values are in `data/processed/pnotisdev_library_manifest.tsv`.

| file | SHA-256 | what it is |
|---|---|---|
| docs/registry.toml | 6a9b4cbe2e5e926f8d53f34aa16fe496a1bd4876040aae6635f4e380aa99b434 | their 148-row experiment registry (rows lib-sections, multipliers, hyp-streams, sacred, sacred2, sacred3, keywords-r4, open-h1 read for the ledger check) |
| docs/CAMPAIGNS.md | dfbeb46824eac937b63e926ae40f3baee066fe4abb6411121272976fe5007066 | campaign table: windows, decision rule, matched nulls |
| docs/HYPOTHESES.md | 5631f2ab9d88e42d0f767bac2c81e26417a787c6307f166499e021a46694383b | H1-H6 (the H1 "library x keyword" slice is their open-h1 row) |
| docs/SOURCES.md, docs/INDEX.md, docs/TRIED.md, docs/FINDINGS.md, docs/RUNNING.md | b4cf7a16…, a92eb3c8…, 0637acfe…, 0c278494…, 4574be96… | context |
| work/kscreen/export.py | 9dabc9df9b002aeba49809a49bab37cc8a4f95542eeddd02c2e35ee04d604a46 | the library generator: new number families, more constants, hash streams, payload, KSB1 writer |
| work/keystreams.py | 8984ba70f7c95dc8f7a70869e4a7c2469a2a38177c45b0e695b7fa6b464cee74 | integer sequences, constant digits, Cicada numbers, keywords |
| work/prng_screen.py | fa5af88c48af4a789e4874ff7e30bb16072b463b90ff0aa4a950b0d8566eea1b | the hash seeds (`seeds()`, `SEEDS_EXTRA`; 65 distinct) |
| work/grid60.py | 393d06bf47f6a16131b73061ac587bbdd6c1a2ab82f1a616fe59f365a43364bb | the 256-byte payload and the An End hash |
| work/lp.py, work/stats.py, work/red_runs.py | 23920022…, f90dd35e…, 43471569… | their transcription parsing (segments, word spans, `word_to_key`, the solved-page rules) |
| work/ref/errata.tsv | 5ffddd76eb22711f3a6854d715496d2d605c648132fb05d7eab236ed316c073b | one rune swap (book page 9, BELEIUE → BELIEUE) and five payload bytes |
| work/kscreen/export_hyp.py, sacred.py, sacred_selftest.py, export28.py, export_hashwords.py, selftest.py, verify.py | 5bf93b53…, 600e9bc8…, e874c17a…, baf3f6e8…, 2c1a2e98…, 35914613…, 1f08bdb9… | the hyp / sacred libraries (not rebuilt here, see §54's coverage limit) and their self-tests |
| results/kscreen/library_segments.tsv, .log, _verify.txt | d2382324…, 8e7edc85…, 098b02e6… | their lib-sections screen: 1,447 items, 409,283,232 decodes, best IoC 1.366, 15 hits re-decoded and rejected |
| results/kscreen/library_hyp.tsv, _verify.txt, hyp_selftest.txt | 96085440…, 6fcbf7f2…, a1593ce0… | their hyp-streams screen |
| work/log/phase9_chain.md, phase9_hyp.md, phase10_sacred.md | 9d539ec9…, 07a64921…, 4a978d18… | their logs for the chain, hyp and sacred campaigns |

Full digests of every file: `cd data/external/pnotisdev && find . -type f ! -name library_cache.npz | sort | xargs shasum -a 256` (recorded in the commit message of §54).
