"""Word-edge and line-edge masks for every unsolved page, aligned to data/processed/pages.json.
Source: the rtkd master transcription (word '-', clause '.', line '/' (inside words too), page '%').
Writes data/processed/edges.json: per page id, lists of rune positions that are word-initial
(i >= 1), word-final (i <= n-2) and line-initial (i >= 1), plus counts."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import RAW, PROCESSED, IDX, rune_indices

raw = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8")
chunks = raw.split("%")
pages = json.loads((PROCESSED / "pages.json").read_text())["unsolved"]

def masks(chunk):
    """Walk the chunk; a rune gets index i; any non-rune char between two runes marks an edge."""
    wi, wf, li = [], [], []
    runes = []
    pending_word = False; pending_line = False
    for ch in chunk:
        if ch in IDX:
            i = len(runes)
            if i > 0:
                if pending_word: wi.append(i); wf.append(i - 1)
                if pending_line: li.append(i)
            runes.append(IDX[ch]); pending_word = pending_line = False
        elif ch in "-.&$§":
            pending_word = True
        elif ch == "/":
            # A line break is NOT a word boundary: 452 of the 630 line breaks on the unsolved pages fall inside a
            # word (no '-' before the '/'); until 2026-10-28 this builder counted them as word edges (3,316 words
            # instead of 2,896), which the field survey's word counts exposed.
            pending_line = True
        # digits, spaces, newlines: ignored
    return runes, wi, wf, li

out = {}
for u in pages:
    runes, wi, wf, li = masks(chunks[u["book_page"]])
    assert runes == u["cipher"], f"{u['id']}: transcription chunk does not match stored cipher"
    out[u["id"]] = {"n": len(runes), "word_initial": wi, "word_final": wf, "line_initial": li}
json.dump(out, open(PROCESSED / "edges.json", "w"))
tot = sum(len(v["word_initial"]) for v in out.values()); lines = sum(len(v["line_initial"]) for v in out.values())
print(f"{len(out)} pages aligned; {tot} word edges, {lines} line edges; e.g. {pages[0]['id']}: {out[pages[0]['id']]['word_initial'][:8]} lines {out[pages[0]['id']]['line_initial'][:5]}")
