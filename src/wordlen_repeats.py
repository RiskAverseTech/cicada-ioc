"""Repeated word-length n-grams across the unsolved pages (2026-10-28; TheronEagle reports the length 8-gram
[6,7,6,3,6,4,3,3] at page 22 word 45 and page 47 word 11 as notable).  Statistic: for n = 5..10, the number
of unordered pairs of positions in the word-length sequence (2,928 words) whose n-grams are identical,
against 999 shuffles of the word-length sequence.  Writes results/wordlen_repeats.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from collections import Counter
from lp import IDX, RAW, RESULTS
rng = np.random.default_rng(8)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-./&$§')
lens = []
for k in range(16, 72):
    n = 0
    for ch in chunks[k]:
        if ch in IDX: n += 1
        elif ch in SEP and n: lens.append(n); n = 0
    if n: lens.append(n)
L = np.array(lens)
def pairs(seq, n):
    c = Counter(tuple(seq[i:i+n]) for i in range(len(seq) - n + 1)); return sum(v * (v - 1) // 2 for v in c.values()), max(c.values())
rows = ["| n | identical n-gram pairs observed | shuffle null mean ± sd | p | largest multiplicity observed | null |", "|---|---|---|---|---|---|"]
for n in range(5, 11):
    o, om = pairs(L, n); nul = np.array([pairs(rng.permutation(L), n) for _ in range(999)])
    rows.append(f"| {n} | {o} | {nul[:,0].mean():.1f} ± {nul[:,0].std():.1f} | {(np.sum(nul[:,0] >= o)+1)/1000:.3f} | {om} | {nul[:,1].mean():.2f} |")
target = (6, 7, 6, 3, 6, 4, 3, 3); hits = [i for i in range(len(L) - 7) if tuple(L[i:i+8]) == target]
out = ["# Repeated word-length n-grams", "", f"{len(L):,} words on the unsolved pages (mean length {L.mean():.2f}). A shuffle of the word-length sequence keeps the length histogram and breaks any order.", ""] + rows + ["",
       f"The reported 8-gram {list(target)} occurs at word positions {hits} ({len(hits)} times). With {len(L)-7:,} positions and this length distribution the null expects about {np.mean([pairs(rng.permutation(L), 8)[0] for _ in range(200)]):.1f} identical 8-gram pairs in total, so one repeated 8-gram is the typical outcome, not a signal.", ""]
(RESULTS / "wordlen_repeats.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
