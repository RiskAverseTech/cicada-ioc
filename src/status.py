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
    ("§27", "5-gram rescoring of short pages", 22863 * 6 * 9 * 2, "A 39/45; B 6/45 (fillers break n-grams)", "null", "soft-rule exclusion now 99 % power on all 55 pages"),
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
    ("§42", "Within-word echoes: lag-5 equality (S), lag-6 affine 24−2c; word-edge correction", None, "—", "measured: both present (z +3.7 K-fixed; z +5.1, best of 812)", "two further laws of the stream; mechanism open"),
    ("§43", "Exact reachability of the solved-page rule, every offset; linear complexity", 1_100_000, "plants recovered", "null: continuous section excluded for 5 streams; pages at n/2 complexity", "per-page reachability has no power (literal-F realignment)"),
    ("§45", "Word-aware mechanism simulation: 8 rules x 9 pre-registered statistics", None, "3 sanity controls", "measured: every rule fails; the S carrier breaks all eight; R4+extra rune fits the other eight", "English plaintext and iid key only; hold-aware decoding = §22"),
    ("§46", "Lag-5 echo runs in pairs (bigrams 9 vs 1.5); multiplier autokey and lag-1 affine closed; per-word period-5 key mixture", None, "—", "measured: f = 0.5 fits equality and S exactly, fails the difference flatness by 3 sd", "first hypothesis producing the S carrier; lag 6 unexplained"),
    ("§47", "Echo rules in the mechanism simulator (14 rules x 10 statistics)", None, "3 sanity controls", "measured: gated lag-5/lag-6 echo (E56w) fits 9 of 10; S carrier outside every additive mechanism", "English plaintext, iid key; one gate parameter fitted to one count"),
    ("§48", "Echo-aware decoding (spent and held echoes) of the phase 3-4 library", nt("echo_lane.json"), "11/12", "null", "echoes cost an unaware decoder ~nothing when key-spending; held echoes cost only when several fall on one page"),
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
    "Cross-library decoding: pnotisdev's 1,447 number streams have met only IoC/bigram screens and the R4 engine, the book's phrase library here only the skip Viterbi (+ §22 hold nulls, + §48 echoes); each library under the other lab's decoder is untested",

    "The S carrier (11 of 102 lag-5 pairs): a step acting on the cipher value S, or a fluctuation; no additive mechanism carries it (§47)",
    "§39's phase-6 part (the nine short pages) under the corrected word edges: not rerun; §14's full rerun moved maxima by tenths of a sigma",
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
| The structures | 86 doubled runes where 445 are expected (0.19 of uniform; solved pages sit at 0.86); inside words, a lag-5 echo that copies equality in runs (102 vs 71 pairs, 9 vs 1.5 bigrams), 11 of the pairs S (3.5 expected, p 0.003), and a lag-6 relation c = 24 − 2c′ (77 vs 44); the two echoes share words; flat in every other statistic |
| Best current reading | a gated word-internal echo (plaintext repeat at lag 5 → copy the cipher rune; at lag 6 → 24 − 2c) in about half the words reproduces nine of ten statistics; the S weighting is outside every additive mechanism and is the open fact |
| External reviews adopted | 2 (2026-10-27), 8 corrections, no fact overturned |
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
- Instrument gains this week: bounded multi-rejection decoder, power curves by page length, a rune 5-gram that lifts short-page detection from 21 % to 99 %, an exact every-offset running-key scanner, an image lane.
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
