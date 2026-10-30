"""Writes STATUS.md, the one-screen status box: progress, coverage, value, breakthroughs.
Numbers come from results/*.json where a lane records them; the lane list, verdicts and open
items are maintained by hand in LANES / OPEN below.  Run after every lane: .venv/bin/python -I src/status.py
"""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import RESULTS

ROOT = RESULTS.parent
def nt(f, default=None):
    p = RESULTS / f
    if not p.exists(): return default
    try:
        d = json.loads(p.read_text()); return d.get("ntests", d.get("ntests_t1", default))
    except Exception: return default

# (README §, lane, tests, controls passed/total, verdict, coverage note)
LANES = [
    ("§1–3", "Key reuse between pages (IC, pooled offsets)", None, "planted 12/12", "null, large-scale", "clusters under ~12 pages not excluded"),
    ("§4–7", "Doublet deficit and twenty constructions", None, "—", "86 vs 445; soft re-draw 0.81 survives", "mechanism inference, not a key"),
    ("§9", "Phase 3: book streams + skip rule", nt("phase3.json"), "20/20", "null", ""),
    ("§12", "Phase 4: phrase and sentence keys", nt("phase4.json"), "26/26", "null", ""),
    ("§13", "Phase 5: Latin and Old English registers", nt("phase5.json"), "24 (12 per register)", "null", ""),
    ("§14", "Phase 6: word-edge events", nt("phase6.json"), "24/24", "null", ""),
    ("§16", "Phase 7: skip-by-two rule", nt("phase7.json"), "24 plants", "null", ""),
    ("§18", "Phase 8: LCG seeds, position multipliers", nt("phase8.json"), "16/16", "null", ""),
    ("§19", "Short-list lane (panel's finite families)", nt("shortlist.json"), "14 (12 rank 1)", "null", ""),
    ("§20", "Phase 9: Gematria feedback, global streams", nt("phase9.json"), "18 (3 exposed a bug, fixed)", "null", ""),
    ("§22", "Phase 10: unknown-position nulls, hard rule", nt("phase10.json"), "15/18", "null", "inconclusive on 9 short pages (§23)"),
    ("§24", "Short-page secondary rule, 9 pages", 22863 * 6 * 9 * 2, "A 39/45, B 31/45", "null", "phase 3–4 library only"),
    ("§25", "External running key, exact every offset", nt("runkey.json"), "15/17", "null", "12 texts; edition differences near mid-page cost ~1 sigma per rune"),
    ("§26", "Page images: container, chroma, geometry", 75, "19 controls", "null", "archive JPEGs only"),
    ("§27", "5-gram rescoring of short pages", 22863 * 6 * 9 * 2, "A 39/45; B 6/45 (fillers break n-grams)", "null", "5-gram power 99 % on planted soft-rule solutions at 66 runes; the short-page lane's own controls pass 39/45 (4/5 at 66 runes), a separate measurement"),
    ("§28", "Windowed dispersion (hand vs machine)", None, "—", "no power", "recorded so it is not re-proposed"),
    ("§29", "The two Know This magic squares as keys", 92 * 6 * 55, "8/8", "null", "direct use only; seeds and indices open"),
    ("§30", "Provenance: signed messages verify (2012, 2016, 2017)", None, "3 of 3 verify", "genuine", "the 2017 'hoax' claim is false"),
    ("§31", "Seeded generators no ledger lists (8 PRNGs, 2^18 seeds)", nt("generators.json") or 113261328, "8/8", "null", "seeds above 2^18 and unnamed generators open"),
    ("§32", "Keyword-mixed alphabets (quagmire I-IV) under the book's keys", nt("quagmire.json") or 25574670, "7/8 (8th rank 2, equivalent alphabet)", "null", "book words and streams only; other labs' key families under mixed alphabets open"),
    ("§33", "Where the 86 repeats sit", None, "—", "boundary-blind", "excludes reset-chain ciphers and transcription artefacts"),
    ("§34", "The 256-byte payload of LP2-49/50/51 as key (direct, pointer readings; +all 6 page orderings and base-59, 2026-10-28)", 383 * 6 * 55, "4/4", "null", "replication; PRF expansions are wazar's negatives"),
    ("§35", "Every archived artefact against the page-73 hash", 3977, "—", "no match", "public archives only"),
    ("§36", "Planted-cluster power of the key-reuse test", None, "30 reps per cell", "measured", "~20 aligned pages for 90 %; blind under key-skip"),
    ("§37", "Repeat spectrum to lag 120, null models, boundary convention", None, "—", "deficit at lag 1 only", ""),
    ("§38", "Blinded glyph re-reading of the unsolved pages", 12807, "99.7 % held-out", "0 disagreements; 149 unread", "pre-registered count criterion failed by the segmenter"),
    ("§39", "Phases 6-8 on the nine short pages, 5-gram rule", None, "22/24, 24/24, 15/16", "null", "phase 9 not yet carried there"),
    ("§40", "Pilgrim texts (Bunyan, Chaucer) as running keys", nt("runkey_pilgrim.json"), "3/3", "null", "The Way of a Pilgrim not run (no free text)"),
    ("§41", "Closure bundle: solved-page repeat rate, parity, repeat context, cross-page n-grams, word-length repeats, ICC", None, "—", "measured: rule specific to the unsolved section; all else at null", "statistics, not decodes"),
    ("§42", "Within-word echoes: lag-5 equality (S), lag-6 affine 24−2c; word-edge correction", None, "—", "measured: both present (z +3.66 K-fixed, p 0.011; z +5.1, best of 812)", "two further laws of the stream; mechanism open"),
    ("§43", "Exact reachability of the solved-page rule, every offset; linear complexity", 1_100_000, "plants recovered", "null: continuous section excluded for 5 streams; pages at n/2 complexity", "per-page reachability has no power (literal-F realignment)"),
    ("§45", "Word-aware mechanism simulation: 8 rules x 9 pre-registered statistics", None, "3 sanity controls", "measured: every rule fails; the S carrier breaks all eight; R4+extra rune (R4n) fits 8 of 10 in the corrected 2026-10-29 rerun", "English plaintext and iid key only; hold-aware decoding = §22"),
    ("§46", "Lag-5 echo runs in pairs (bigrams 9 vs 1.5); multiplier autokey and lag-1 affine closed; per-word period-5 key mixture", None, "—", "measured: f = 0.5 fits the equality count (101 vs 102), predicts 3.5 S pairs not 11, fails the difference flatness by 3 sd", "the S..S fit claimed on 2026-10-28 was an error, corrected the same day; row fixed 2026-10-29"),
    ("§47", "Echo rules in the mechanism simulator (14 rules x 10 statistics)", None, "3 sanity controls", "measured: gated lag-5/lag-6 echo (E56w) fits 9 of 10; E56w+R4n inside the band on all 10 after the R4n fix (S at z +2.9, lag 6 at −2.9, the band's edge); S carrier outside every additive mechanism with a key uniform given its own difference (corrected 2026-10-29: English running keys give about 6 % S at coincidences, the pages' eleven then at p 0.03-0.09)", "English plaintext, iid key; one gate parameter fitted to one count"),
    ("§48", "Echo-aware decoding (spent and held echoes) of the phase 3-4 library", nt("echo_lane.json"), "11/12", "null", "echoes cost an unaware decoder ~nothing when key-spending; held echoes cost only when several fall on one page"),
    ("§49", "E56w out-of-sample predictions (8 statistics, 14 cells, committed before the look); echoes on the image-derived stream", None, "—", "measured: 14/14 cells hold; image stream reproduces 101 / 11 / 75 exactly", "consistency, not confirmation; S weighting still outside the rule"),
    ("§50", "S carrier: the eleven sites in the images; line-break dependence of the lag-5 echo; RS5 second traces", None, "controls at lags 4, 6", "measured: nothing in ink; lag-5 echo 2x on line-wrapping pairs (z +2.2), lag 6 not; RS5 7/7 but near-unfalsifiable", "post-hoc cut found by eye; eleven events"),
    ("§51", "Layout follow-up to the line-wrap lead (split position, distance to line edge; registered before the check)", None, "lag-4, lag-6 controls", "null: no layout signature; wrap excess stands at z +2.2 and is not word length", "a layout step is not supported"),
    ("§52", "Hint reading: word edges and page rings written in clear (the parable as an operation)", nt("shed_lane.json"), "7/12 (WORD kind halves the encrypted material; 3 alias ranks)", "null", "WORD kind weak for keys under three words"),
    ("§53a", "Cicada's own words 2012-2017 as running keys (every offset, both directions, both spellings)", nt("runkey_cicada.json"), "2/2", "null", "one 7,792-rune stream"),
    ("§53b", "Cicada's own words 2012-2017 as word, phrase and line keys (8,916 keys, forwards and reversed)", nt("cicada_words.json"), "6/6 (rerun)", "null", "keys up to 400 runes; the group's prose and embedded strings"),
    ("§54", "Cross-library: pnotisdev's 1,439 streams under the plain, echo and hold decoders", nt("cross_library.json"), "14/18 rank 1 (18/18 found; misses are own-offset aliases)", "null", "tier 1 on the first 80 / 160 runes of LP2-00, LP2-01, LP2-02 only (all pages only for a candidate); every offset for plain / echo; hold at offsets 0–999 of the non-periodic streams; sacred / hyp libraries not rebuilt"),
    ("§55a", "Word-length fingerprint of the unsolved pages; positional IoC; repeated cipher words", None, "bootstrap null (2,000 English samples)", "measured: not English prose (chi-square 183, p 0.0005; 15.9 % two-rune words vs 24-25 %); best simple fit = fillers at about one per two words; positional IoC flat; no repeated 4-rune cipher words", "descriptive; register (verse, list) not excluded; per-word key restart excluded"),
    ("§55b", "Decoder power with fillers at 0.10 (3 families x 3 lengths x 12 plants, with and without fillers)", None, "108 + 108 plants", "measured: plain decoder power 0.00 in every filler cell; free-null at prior -2.2 keeps 0.75 (running key, 230 runes), 1.00 (Vigenère), 0.75 (primes)", "every plain-decoder lane had no power in a filler world at this rate; §22 and the §54 hold tier did"),
    ("§55c", "Filler sweep: 16 external texts (every offset both ways / sentence starts) and pnotisdev offsets 1,000-1,999 under the free-null decoder", nt("filler_lane.json"), "5/6 rank 1 (6th found at rank 2, offset alias)", "null", "160-rune windows on LP2-00/01/02 (power 0.58 for running keys); one prior; the 20-nat margin arm does not filter wrong keys at page length; pnotisdev offsets >= 2,000 and the sacred / hyp libraries open"),
    ("§57", "E56w+R4n out-of-sample predictions (16 cells + 2 declared, committed before the look)", None, "—", "measured: 15/16 hold; fails lag-6 hits in words >= 10 runes (30 vs 59 ± 9, z −3.15), the T-writing hold repair's signature; E56w predicted 37", "the filler component stands with the §55 fingerprint; the hold repair does not; E56w with fillers to be registered before it is run"),
    ("§58", "E56w+n (two echoes + filler in 45 % of words on the spend repair, no T-writing): §47's ten statistics and §57's sixteen cells, committed before the check", None, "—", "measured: survives §47's band on all ten (S at z +2.7 on spread, 4.8 predicted vs 11) and holds 16/16 of §57's cells; first rule inside every band", "generative description, not a decryption; S count still unreproduced; filler rate taken from R4, not fitted"),
    ("§59", "Three registered follow-ups to E56w+n: filler rate fitted to word lengths (p* 0.40, chi² 25, inside §55's English band); lag-5 / lag-6 profiles per exact length (13 cells); solved-page lag-3..6 equality", None, "—", "measured: 13/13 profile cells and 4/4 solved-page lags hold; at p* the S cell fails §47's band (11 vs 4.6 ± 2.0, z +3.2)", "the one free rate set by the words; the S weighting is outside E56w+n as it was outside every rule; read the filler rate as 0.40"),
    ("§60", "Filler power curve: per-rune r 0.01-0.10 and the §59 per-word form p 0.2-0.6, 3 families x 3 lengths x 12 paired plants, plain and free-null decoders; seven claims registered before the run", None, "864 plant-cells", "measured: C7 holds, C1-C6 fail toward a more robust plain decoder; plain power 0.02 at the fitted rate p 0.40, half at two fillers per hundred runes (a filler is absorbed when a natural key skip precedes it); free-null 0.75 at p 0.40, flat to r 0.05", "the §55 paragraph on the field's negatives weakened by its rule: zero power at the fitted rate, half in a sparse-filler world; no sweep"),
    ("§61", "Word-constrained filler decoder (at most one filler per word): power on §60's plants, false gain on wrong keys at page length, then the book's 22,863 key-sign configurations, 60,000 prime-stream variants and sixteen external texts at full page length; prior, claims and acceptance rule registered first", 31363746, "6/6 planted (z 10.8-14.0)", "null (largest z 6.04 in 19.8 M prime tests, unreadable; book 5.01; texts 5.52 at full page); A1 fails, B1-B2 fail, margin arm dropped", "the constraint buys nothing over free-null (power 0.73 vs 0.75, false gain -5 %); a gain margin cannot separate true from wrong keys at page length; part A's first run replayed 8/864 of §60 and was redone"),
    ("§62", "pnotisdev's full library (1,439 streams, periodic ones below their period) at offsets 0-999 under the free-null decoder: 160-rune windows on LP2-00/01/02 x 3 signs x 2 F, full-page tier 2; claims registered first", nt("pn_full.json"), "5/6 rank 1 (the same six plants as §55c; the rank-2 alias passes tier 2)", "null (377 tier-1 survivors, no candidate; largest tier-1 z 7.06 against 6.5 registered, page z 5.55, unreadable; largest page z 5.75)", "P1 and P3 fail as written: the control claim was copied without re-reading §55c and the chance maximum assumed Gaussian tails; non-periodic offsets >= 2,000 and tier 1 beyond the first three pages open"),
    ("§56", "Validation release after the second external review: n-gram lower orders, standalone R4n, K-fixed sampler clock fixed; affected statistics rerun; four summaries corrected", None, "3 new tests", "measured: no decode negative moved; see the section for the rerun figures", "the fixes bear on the mechanism table, two p-values and the wording"),
    ("§44", "Irrational digits (pi, e, sqrt 2, phi; three readings) under the soft rule, offsets to 30,000", nt("digits.json"), "4/4", "null", "base-10, digit pairs, base-29; fresh offset per page"),
]
OPEN = [
    "Filler (null) lane on LP2-49, LP2-55, LP2-51: below power at any rule tried",
    "Mixed alphabets under the other labs' key families (external texts, PRNG seeds): the quagmire lane covered the book's own keys only",
    "Phase 9 mechanisms on the nine short pages",
    "149 unread positions of the blind re-reading (merged ᚳ pairs, drop caps): a better splitter or the eye",
    "Red-text key schedule (the red initials and first words), ledger check first",
    "wazar's R12-C2 esoteric texts: Dukotah R26-B ran 33 of them at 4–8 offsets, sign −1 only (pages 20/22/25/27/29, sign +1, reversed texts unrun; Gutenberg ids wrong)",
    "LP2-50, the two-character-code page, as a cipher of its own",
    "Key source, not key search: the page behind the AN END SHA-512 (the one place a key is said to exist) is unfound; archived onion corpora (Dukotah 2026-07-27), 1,962 documents (ItIsCuthNotCup), raw bytes/IPv4/phones (hashcat), 124,017 onion-capture digests (pnotisdev) and 502 artefacts x 3,977 readings here (§35) do not contain it; Tor v2 is gone, so only an archive nobody has indexed can",
    "Cross-library decoding, second half: this repository's 7,621 keys (data/processed/book_library.tsv) have not been run under pnotisdev's flat-IoC engine; their sacred / sacred2 / sacred3 / hyp-streams libraries and the 12,944 hash-word streams have not met the decoders here (§54 covers the 1,439-stream main library)",

    "The S carrier (11 of 102 lag-5 pairs): a step acting on the written rune S (a plaintext-reading key is additive and NOT excluded by §47, as the second review noted), or a fluctuation; no additive mechanism with a key uniform given its own difference carries it, but an English running key gives about 6 % at coincidences and the eleven are then at p 0.03-0.09 (§47, corrected 2026-10-29); the lag-5 echo prefers line-wrapping words (§50) but shows no layout signature (§51): a fluctuation or an unnamed property of those words",
    "§39's phase-6 part (the nine short pages) under the corrected word edges: not rerun; §14's full rerun moved maxima by tenths of a sigma",
    "The designers'-side blind spots (docs/blind-spots.md, 2026-10-29): every scorer assumes natural-language plaintext (a non-prose token scorer is unrun in every lab); the combine operation is index arithmetic where the Gematria Primus is a table of primes (value arithmetic as the cipher is unrun); the sparse-message world (a rule-selected subsequence of the whole section, never read); one process for all four footprints rather than a fifth component",
    "A decoder that is echo-aware (§48) and filler-aware (§55, §61) at once, which E56w+n's own generative story requires; §61 shows the one-filler-per-word constraint adds nothing on its own, so the next instrument is the combined one, and pnotisdev's 1,439 streams at full length have not been run under any filler-aware decoder",
    "The filler world beyond §55: the six long texts at every offset (sentence starts only there), pnotisdev's non-periodic streams at offsets >= 2,000, pnotisdev's sacred / hyp libraries, and every phase 5-9 family (registers, word-edge events, skip-by-two, LCG seeds, feedback streams) under a filler-aware decoder; and the register question the fingerprint leaves open (verse or list instead of prose)",
]

readme = (ROOT / "README.md").read_text()
sections = max(int(m) for m in re.findall(r"^## (\d+)\.", readme, flags=re.M))
head = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short"], cwd=ROOT, capture_output=True, text=True).stdout.strip()   # date only: the hash of the commit that carries this file cannot be known when it is written
ncommits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
total = sum(t for _, _, t, _, _, _ in LANES if isinstance(t, (int, float)) and t > 1000)
closed = sum(1 for l in LANES if l[4].startswith("null"))
running = [l[1] for l in LANES if l[4] == "running"]

box = f"""# Status box

| | |
|---|---|
| **Breakthroughs** | **0** (a page decoding to readable English at a pre-registered bar, reproduced by someone else) |
| Decoder tests run | {total/1e6:.0f} million, all pre-registered, all with planted controls |
| Lanes closed null | {closed} of {len(LANES)} ({', '.join(running) if running else 'none running'}) |
| Pages | 55 unsolved with runes (12,956 runes); coverage limits listed per lane |
| The structures | 86 doubled runes where 445 are expected (0.19 of uniform; solved pages sit at 0.86); inside words, a lag-5 echo that copies equality in runs (102 vs 71 pairs, 9 vs 1.5 bigrams), 11 of the pairs S (3.5 expected under a uniform key, p 0.005; about 6.5 expected under an English running key, §47 corrected), and a lag-6 relation c = 24 − 2c′ (77 vs 44); the two echoes share words only at the level of description (p 0.11 once word length is held); flat in every other statistic |
| Best current reading | E56w+n (§58): a gated word-internal echo (plaintext repeat at lag 5 → copy the cipher rune; at lag 6 → 24 − 2c) in about half the words, one filler rune in about half the words, the spend repair at q 0.81, iid key, English plaintext; the first rule inside every pre-registered band (§47's ten statistics, §57's sixteen cells, consistency cells whose values were public); it predicts five S pairs against eleven, passing that cell on spread at the borrowed rate 0.45 and failing it (z +3.2) at the rate the word lengths fit, 0.40 (§59), so the S weighting stays the open fact, and a description is not a decryption |
| External reviews adopted | 3 (2026-10-27, two on 2026-10-29), 12 corrections, one claim withdrawn (§47's exclusion of every plaintext-independent key) |
| Repository | {sections} numbered sections, {ncommits} commits as of {head} |

## Lanes

| § | lane | tests | controls | verdict | coverage limit |
|---|---|---|---|---|---|
"""
for sec, name, t, ctrl, verdict, note in LANES:
    ts = "—" if t is None else (f"{t/1e6:.1f} M" if t > 1000 else str(t))
    box += f"| {sec} | {name} | {ts} | {ctrl} | {verdict} | {note} |\n"
box += "\n## Open\n\n" + "\n".join(f"- {o}" for o in OPEN) + """

## Value so far

- Every exclusion above is reproducible from `src/` with a planted control that shows the test can see a solution; that is what the other 2026 ledgers mostly lack.
- Instrument gains this week: bounded multi-rejection decoder, power curves by page length, a rune 5-gram that lifts short-page detection at 66 runes from 21 % to 100 %, an exact every-offset running-key scanner, an image lane.
- `results/ledger_diff.md` lets a new idea be checked against five labs' prior work in minutes.

*Generated by `src/status.py`; the lane table is maintained by hand in that file, the counts are read from `results/`.*
"""
(ROOT / "STATUS.md").write_text(box)
# machine-readable ledger beside the box
ledger = [dict(section=sec, lane=name, tests=t, controls=ctrl, verdict=verdict, coverage_limit=note, date="2026-10-27") for sec, name, t, ctrl, verdict, note in LANES]
json.dump(dict(generated_by="src/status.py", repository="https://github.com/RiskAverseTech/cicada-ioc", head=head, breakthroughs=0,
               breakthrough_definition="a page decoding to readable English at a pre-registered bar, reproduced by someone else",
               lanes=ledger, open=OPEN), open(ROOT / "ledger.json", "w"), indent=1)
print(box[:1400])
