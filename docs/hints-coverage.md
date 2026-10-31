# The creators' words as a coverage map

*Written 2026-10-31. Every statement the creators signed or printed, read as a possible instruction to the solver, with the
literal operations a reader could take from it and where each has been tested, here or in another lab's ledger. The
readings are opinion and tagged inferred; the coverage column is fact. Append dated notes under a row rather than rewriting
it. Sources: `data/corpus/raw/cicada_own_words_2012_2017.txt` (signed statements verified by full fingerprint, §30) and the
solved pages' English (`data/raw/iddqd__liber-primus__translation.txt`).*

The 2016 signed text is the one direct instruction about the book: *Liber Primus is the way. Its words are the map, their
meaning is the road, and their numbers are the direction.* The field, this repository included, has read it literally for a
decade: the words as key text, the numbers as key sequences. That reading is null at published scale (§9, §12, §25, §40,
§53, §54, §62; pnotisdev's library; Dukotah's seeds). Three other readings sit between its words and are mostly unrun:
the words *locate* (a map is looked up, not added), the plaintext's instructions *name operations*, and the numbers are
*directions* (offsets, steps, shifts) rather than values. [inferred]

| source | statement | literal operations a reader could name | tested here | tested elsewhere | status |
|---|---|---|---|---|---|
| 0.0 warning | "Do not edit or change this book or the message contained within, either the words or their numbers, for all is sacred" | the message is carried by the words *and* their numbers: every word has a number (its Gematria sum); page and line numbers matter | word numbers as a per-word key or step: not run; cumulative Gematria of cipher runes as feedback (§20); value arithmetic as the combine (§67); the squares (§29) | pnotisdev number-theoretic streams; Cicada numbers as streams | partly: numbers as values and sequences yes; numbers *of the words* as steps, no |
| 0.1 welcome | "Journey deep within and you will arrive outside" | an inside-out order: read or key from the middle outward; reverse | reversed keys in every family (`-rev`); the ciphertext read in another order: not run (transposition demoted by the doublet argument, §71's panel) | anon5376 route and classical transpositions | partly |
| 0.1 welcome | "Like the instar, it is only through going within that we may emerge" | a stage-wise process: layers, molting, one shell removed at a time | the hint-reading family on "shed" (§52); no multi-stage decode | — | mostly unrun |
| 0.1 wisdom | "You are a law unto yourself", "Command your own self" | the text keys itself: autokey on plaintext or ciphertext; the solved text as the running key | rigid autokeys (§3); the solved plaintext as running key at every offset (§9 self rows); one-state feedback procedures (§73); lag-1 plaintext autokey as the S origin (`results/s_autokey_check.md`) | pnotisdev keyword keys from the solved pages | run for additive forms; two-state and word-level autokeys unrun |
| 0.1 some wisdom | "The primes are sacred. The totient function is sacred. All things should be encrypted" | the primes as the alphabet's values (given); prime and totient *sequences* as keys; the totient as a *function* applied to numbers in the book; "all things" encrypted, including numbers, separators, red runes | prime, totient and prime±1 streams at every start (§9, §70); φ as a function of word or rune values: not run; red runes (§66), separators as cipher: not run | pnotisdev `sacred*` and number-theoretic rows; page 0.16's totient stream is the solved precedent | sequences run; the function reading unrun |
| 0.1 know this | the two magic squares | the squares as keys, tables or routes | as keys in every sign and offset (§29) | Pitchfork, yo-yo-yo-jbo (Hill with the squares) | run as keys; as a lookup table for a feedback procedure, no |
| 0.2 koan | "That is not who you are, that is only what you are called" | the name is not the thing: a rune's letter is a label, its value or position is what it is | value arithmetic as the combine (§67); Gematria-order tables with feedback (§73) | — | partly; value-built tables with feedback unrun |
| 0.2 koan | "A consciousness inhabiting an arbitrary body" | the carrier is arbitrary, the content is not: nulls or fillers around a message; a sparse message | fillers (§55, §58–§61), rule-selected subsequences (§63) | pnotisdev "unkeyed insertions" (open row) | run at the stated powers |
| 0.3 loss of divinity | "The circumference practices three behaviors: consumption, preservation, adherence" | three modes for a key symbol: spend it, hold it, follow (copy) the previous rune | spend repair (§5, §9), hold repair and copy echoes (§47, §58): fitted one at a time, never as one three-mode procedure chosen by a rule in the text | pnotisdev R4 hold repair | the three modes run separately; a single procedure switching among them by a stated rule unrun |
| 0.3 loss of divinity | "Most things are not worth consuming / preserving" | consume little key (fillers consume none), preserve little | the filler form (§59, 0.40 of words) | — | run |
| 0.4 koan | "The I is the voice of the circumference" | the rune I (index 10) is a marker, as S is weighted in the lag-5 echo | S as a marker (§47 residual class, §50); I as a marker: not run | — | S partly, I unrun |
| 0.4 instruction | "Question all things. Discover truth inside yourself. Follow your truth. Impose nothing on others" | verify; the key is inside the text; do not add material from outside | the book's own material under every decoder (§9, §12, §53); outside texts as running keys (§25, §40) | ~215 running-key texts across labs | run for additive forms |
| 0.13 an end | "Within the deep web there exists a page that hashes to …" | the page-73 hash as a check or as key material | every archived artefact against the hash (§35); hash streams of Cicada strings (§54) | hashcat masks, ItIsCuthNotCup, pnotisdev 19 M passphrases | run; the page itself is not public |
| 0.14 parable | "Shed our own circumferences; find the divinity within and emerge" | remove the outer runes of each word; read the inside | the hint-reading family (§52), null | — | run for the literal reading |
| 2012–2013 images | "There is a message hidden in this image … it will lead you on the road" | the page images carry a channel | side channels (§26), the scans' line fill (§65), glyph re-reading (§38) | Dukotah R29–R30, ZzNible T13 | run |
| 2016 signed | "Its words are the map, their meaning is the road, and their numbers are the direction" | see the three readings above | literal reading run throughout; the derived readings not | the field's literal reading at scale | the derived readings are the open room |
| 2017 signed | "Beware false paths. Always verify PGP signature" | discard unsigned material; many community "solutions" are false | PGP verification by full fingerprint (§30); false claims dismissed with reasons (field survey §4) | isitcicada | run |

**What the table says.** Every statement has been read at least once as an additive key or a sequence, and those readings are
null at the published scale. The unrun readings cluster: operations named by the text (the three behaviours as one switching
procedure; "command your own self" as a word-level or two-state autokey; the totient as a function; a rune as a marker), and
numbers as directions (word sums as steps, offsets or shifts). Those are the instruments after §73. [inferred]
