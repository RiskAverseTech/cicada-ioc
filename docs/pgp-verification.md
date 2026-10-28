# The signed messages verify, including April 2017

**Claim examined (Discord, 2026-10-27):** that the April 2017 "Beware false paths" message was a hoax
produced by "exploiting glaring weaknesses in PGP", and that the unsigned January 2016 "Pi Mobi"
puzzle was the genuine article.

**Check.** Cicada's public key was fetched from keys.openpgp.org by its full 160-bit fingerprint,
not its 32-bit short ID (short IDs can be collided; fingerprints cannot). Three messages were taken
from the pinned wazar/Dukotah archive and verified with an independent pure-Python OpenPGP
implementation (`src/verify_pgp.py`, pgpy); GnuPG gives the same result. Files and SHA-256 in
`data/raw/pgp/`.

| message | signed (UTC) | hash | verifies |
|---|---|---|---|
| Denial of the "Necrome" link | 2012-04-18 17:41 | SHA-1 | yes |
| "Liber Primus is the way …" | 2016-01-01 00:01 | SHA-1 | yes |
| "Beware false paths. Always verify PGP signature from 7A35090F." | 2017-04-04 23:23 | SHA-512 | yes |

Key: RSA 4096, created 2012-01-05 03:39 UTC, fingerprint 6D85 4CD7 9333 22A6 01C3 286D 181F 01E5
7A35 090F. All three signatures were made with that one key. Forging the 2017 signature would require
the private key, which would make the forger Cicada. wazar's ledger entry CORPUS-G-02 reports the
same check over 238 archived files, 54 distinct messages, 2012-01-05 to 2017-04-04, all verifying.

**Transcription note.** RFC 4880 strips trailing whitespace from cleartext lines before hashing.
Some archived copies carry a trailing space on one line; a verifier that does not canonicalise reports
those copies as bad signatures. That is a property of the copy, not the signature, and it is the kind
of artefact a "PGP weakness" story can be built on. The script reports both readings.

**Conclusion.** The 2017 message is genuine. The 2016 "Pi Mobi" puzzle is unsigned, which is exactly
what the 2017 message warned about. Nothing signed by Cicada after January 2014 is a puzzle.
