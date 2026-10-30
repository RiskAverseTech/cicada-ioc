# Registration: the red runs as keys, as a stream, as ciphertext, and in the clear (2026-10-31, before any run)

**Data.** `results/red_runs.md`: 19 red runs, 213 runes, on 13 of the 32 colour scans (the 23 grayscale scans are blind to colour): nine page headings after the red drop cap, six inline headings, the 50-rune passage on LP2-53 lines 7–9, one single red rune. Read from the transcription at the red glyph positions of `results/scan_glyphs.json`.

**Ledger check.** pnotisdev restarted the key library at the ten red headings and the page starts (STATUS row 140, partial, nothing flagged). The earlier clone's report found that on the solved koan page the red runes forward-encrypt exactly like the black ones (rubrication inside the cipher stream). Nobody has used the red runs as keys or as a keystream, or tested the red runs on their own as ciphertext.

**Hypotheses and instrument** (`src/red_lane.py`, plain decoder with the soft skip, three signs × literal F on and off, z against 400 random keys of the same form). H1, own-page and cross-page keys: each run of three runes or more, and each page's runs concatenated, as a repeating key for its own page (full page and black runes only) and for every other page; null: random keys of the same period. H2, the red stream: all 213 red runes in book order, forward and reversed, as a running key for every page at every offset with wrap-around; null: random streams. H3, red runs as ciphertext: every run of eight runes or more under the book's 7,621 keys × 3 signs × 2 F; null: random keys. H4, in the clear and self-keyed: each heading scored as plaintext as written and under P = 15·C mod 29 (a heading enciphered with itself under the sub sign gives C = 2P); null: random strings of the same length.

**Controls.** C1: English (Emerson) at page length enciphered with LP2-00's heading run as a repeating key (sub, soft rule 0.81) must come top of H1's key set at z ≥ 6, rank 1. C2: English enciphered with the red stream from a random offset must be found by H2 at that offset, rank 1, z ≥ 6. C3: a 50-rune English string under a random book key must be found by H3 at rank 1, z ≥ 6; C4, the same at 12 runes, is reported as a power statement and is not a claim.

**Acceptance and the chance maximum.** A candidate is z ≥ 6, rank 1, readable by eye, and above the largest z among every null draw of its hypothesis (the empirical maximum is reported next to the observed maximum; the lesson of §62 and §64's addendum). Test counts are stated per hypothesis.

**Claims.** K1: C1–C3 pass. K2: H1 no candidate. K3: H2 no candidate. K4: H3 nothing at z ≥ 6, rank 1, readable. K5: H4 no heading at z ≥ 4 as written or self-keyed. **Expected: all hold.** The red is rubrication of headings inside the cipher stream (the solved koan page says so), and a heading's cipher runes have no reason to be a key.

**Budget.** About 2 million short decodes, under an hour on one core.
