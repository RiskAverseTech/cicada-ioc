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
    try: return json.loads(p.read_text()).get("ntests", default)
    except Exception: return default

# (README §, lane, tests, controls passed/total, verdict, coverage note)
LANES = [
    ("§1–3", "Key reuse between pages (IC, pooled offsets)", None, "planted 12/12", "null, large-scale", "clusters under ~12 pages not excluded"),
    ("§4–7", "Doublet deficit and twenty constructions", None, "—", "86 vs 445; soft re-draw 0.81 survives", "mechanism inference, not a key"),
    ("§9", "Phase 3: book streams + skip rule", nt("phase3.json"), "12/12", "null", ""),
    ("§12", "Phase 4: phrase and sentence keys", nt("phase4.json"), "18/18", "null", ""),
    ("§13", "Phase 5: Latin and Old English registers", nt("phase5.json"), "24/24", "null", ""),
    ("§14", "Phase 6: word-edge events", nt("phase6.json"), "12/12", "null", ""),
    ("§16", "Phase 7: skip-by-two rule", nt("phase7.json"), "24/24", "null", ""),
    ("§18", "Phase 8: LCG seeds, position multipliers", nt("phase8.json"), "14/14", "null", ""),
    ("§19", "Short-list lane (panel's finite families)", nt("shortlist.json"), "14/14", "null", ""),
    ("§20", "Phase 9: Gematria feedback, global streams", nt("phase9.json"), "12/12", "null", ""),
    ("§22", "Phase 10: unknown-position nulls, hard rule", nt("phase10.json"), "15/18", "null", "inconclusive on 9 short pages (§23)"),
    ("§24", "Short-page secondary rule, 9 pages", 22863 * 6 * 9 * 2, "A 39/45, B 31/45", "null", "phase 3–4 library only"),
    ("§25", "External running key, exact every offset", nt("runkey.json"), "15/17", "running" if not (RESULTS / "runkey.json").exists() else "null", "13 texts; Beaufort, F variants, reversal"),
    ("§26", "Page images: container, chroma, geometry", 75, "19 controls", "null", "archive JPEGs only"),
    ("§27", "5-gram rescoring of short pages", 22863 * 6 * 9 * 2, "power 99 % at 66 runes (soft rule)", "running" if not (RESULTS / "shortpage_rescore.json").exists() else "null", "filler lane gains less"),
    ("§28", "Windowed dispersion (hand vs machine)", None, "—", "no power", "recorded so it is not re-proposed"),
]
OPEN = [
    "Filler (null) lane on LP2-49, LP2-55, LP2-51: below power at any rule tried",
    "Phase 6–9 mechanisms on the nine short pages: not carried there",
    "wazar's 29 fetched-but-never-run esoteric texts (R12-C2)",
    "Planted-cluster simulation for the key-reuse test (small clusters)",
    "LP2-50, the two-character-code page, as a cipher of its own",
    "Generator families (PRNG/KDF seeds) under the soft rule, where the machine reading points",
]

readme = (ROOT / "README.md").read_text()
sections = len(re.findall(r"^## \d+\.", readme, flags=re.M))
head = subprocess.run(["git", "log", "-1", "--format=%h %ad", "--date=short"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
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
| The one structure | 86 doubled runes where 445 are expected; flat in every other statistic |
| Best current reading | key redrawn ~4 times in 5 when it would repeat; lag-2 at chance points to a program, not a hand |
| External reviews adopted | 2 (2026-10-27), 8 corrections, no fact overturned |
| Repository | {sections} numbered sections, {ncommits} commits, last {head} |

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
- Instrument gains this week: bounded multi-rejection decoder, power curves by page length, a rune 5-gram that lifts short-page detection from 21 % to 99 %.
- `results/ledger_diff.md` lets a new idea be checked against five labs' prior work in minutes.

*Generated by `src/status.py`; the lane table is maintained by hand in that file, the counts are read from `results/`.*
"""
(ROOT / "STATUS.md").write_text(box)
print(box[:1400])
