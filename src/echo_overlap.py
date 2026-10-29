"""Word sharing between the lag-5 echo and the lag-6 relation, pooled and stratified by exact word length (2026-10-29).

§42 reported that 18 of the 554 words of length >= 7 carry both a within-word lag-5 equality and a within-word lag-6
relation c_i = 24 - 2 c_(i-6), against 10.8 expected if the two sat in words independently (p 0.012).  The second external
review (2026-10-29) noted that pooling all lengths >= 7 leaves a word-length confound: longer words have more pairs of both
kinds.  Here the expectation and the permutation null are computed within each exact word length (12 and longer pooled),
so a word's chance of carrying the lag-6 relation is permuted only among words of its own length.
Output: results/echo_overlap.md.
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N

t0 = time.time(); rng = np.random.default_rng(42); NPERM = 20000
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§'); words = []
for k in range(16, 72):
    cur = []
    for ch in chunks[k]:
        if ch in IDX: cur.append(IDX[ch])
        elif ch in SEP and cur: words.append(np.array(cur)); cur = []
    if cur: words.append(np.array(cur))
L = np.array([len(w) for w in words])
e5 = np.array([bool(len(w) > 5 and np.any(w[5:] == w[:-5])) for w in words])
e6 = np.array([bool(len(w) > 6 and np.any(w[6:] == (24 - 2 * w[:-6]) % N)) for w in words])
m = L >= 7; obs = int((e5 & e6 & m).sum()); n5, n6, nn = int((e5 & m).sum()), int((e6 & m).sum()), int(m.sum())
pooled = np.array([int((e5[m] & rng.permutation(e6[m])).sum()) for _ in range(NPERM)])
Ls = np.minimum(L, 12); strat = np.zeros(NPERM, int); exp_s = 0.0; rows = []
for l in np.unique(Ls[m]):
    s = m & (Ls == l); a, b = e5[s], e6[s]; n_ = int(s.sum()); exp_s += a.sum() * b.sum() / n_
    both = int((a & b).sum()); rows.append(f"| {l}{'+' if l == 12 else ''} | {n_} | {int(a.sum())} | {int(b.sum())} | {both} | {a.sum() * b.sum() / n_:.1f} |")
    for r in range(NPERM): strat[r] += int((a & rng.permutation(b)).sum())
p_pool = float(np.mean(pooled >= obs)); p_strat = float(np.mean(strat >= obs))
out = ["# Word sharing between the two echoes: pooled and length-stratified", "",
       f"Words of length ≥ 7 on the 55 unsolved pages: {nn}; with a within-word lag-5 equality {n5}; with a within-word lag-6 relation {n6}; with both **{obs}**.", "",
       f"- Pooled (§42's calculation): expected {n5 * n6 / nn:.1f}; permutation of the lag-6 labels over all {nn} words, {NPERM:,} draws: mean {pooled.mean():.1f}, one-sided p = **{p_pool:.3f}**.",
       f"- Stratified by exact word length (labels permuted within each length): expected {exp_s:.1f}, permutation mean {strat.mean():.1f}, one-sided p = **{p_strat:.3f}**.", "",
       "| word length | words | lag-5 echo | lag-6 relation | both | expected both |", "|---|---|---|---|---|---|"] + rows + ["",
       "Reading: once each pattern's rate is allowed to depend on word length, the shared-word excess is 18 against 14, p about 0.1. The sharing stands as a description, not as evidence that one word-level process produces both echoes; §42, §45 and the summary are worded accordingly from 2026-10-29. [stated]", "",
       f"Runtime {time.time() - t0:.0f} s. Reproduce: `.venv/bin/python -I src/echo_overlap.py`.", ""]
(RESULTS / "echo_overlap.md").write_text("\n".join(out)); print("\n".join(out[:6]))
