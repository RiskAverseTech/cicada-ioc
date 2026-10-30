# Registration: pnotisdev's full keystream library at offsets 0–999 under the free-null decoder (2026-10-30, before any run)

**Gap.** §54 ran pnotisdev's 1,439 streams at offsets 0–999 under the plain decoder, whose power against the filler form the word lengths fit is 0.02 (§60). §55 part C ran only the 580 non-periodic streams, only at offsets 1,000–1,999, under the free-null decoder. So the library's first thousand offsets, and the 859 periodic streams at any offset, have never met a filler-aware decoder. This lane closes that gap and nothing else.

**Instrument.** `src/filler_lane.py` unchanged in its decoder, tiers, nulls and acceptance rule, run with `PN_ALL=1 TEXTS=0 PN_OFFS=0,1000 OUT=pn_full`: every one of the 1,439 streams, offsets 0–999 (a periodic stream only below its period), no text units; free-null at the §55 prior −2.2 (§61 part A: power 0.75 pooled at p = 0.40, 0.90 at r ≤ 0.02); tier 1 on the first 160 runes of LP2-00/01/02 × 3 signs × 2 F at z ≥ 4.5; tier 2 at full page, candidate at z ≥ 6 by the page's 2,000-key null through the same decoder, free − plain ≥ 20 nats, and readable. The six §55 controls run again on shard 0 (planted running keys with fillers at 0.10, 262 runes); all six must pass or the sweep is not read. 588,835 offsets × 18 cells = 10.6 M window decodes.

**Expected: null.** The streams are number-theoretic and constant-digit sequences and hash counters; nothing in the record points at any of them, and §54 and §55 found nothing at the offsets they covered. Chance maximum of z over 10.6 M tier-1 tests is about 5.7; a tier-1 z of 6 or more that fails tier 2 is noise.

**Claims.** P1: controls 6/6. P2: no candidate. P3: the largest tier-1 z is below 6.5. If P2 fails the transliteration is judged by eye and the page is rerun under both priors and all three decoders of §61 before anything is said.

**Budget.** About the §55 sweep's size; expected 6–10 h on eight cores, in the background.
