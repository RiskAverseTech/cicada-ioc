"""Repeated bigrams and trigrams at lag d inside words and in the whole stream (2026-10-28).
The lag-5 S..S sites include SDNGGLSDNG (SDNG twice, five apart) and ESEOTHTHES (ES twice, five apart);
pnotisdev's branch research/word-internal-lag5 reports 9 repeated bigrams at lag 5 inside words against 1.5.
Count, for d = 2..12 and n = 2, 3: positions i with c[i..i+n) == c[i+d..i+d+n) (within one word; and anywhere on
the page).  Null: 999 within-page shuffles with word structure fixed.  Writes results/ngram_lag.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N
rng = np.random.default_rng(55)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
U = [parse(chunks[k]) for k in range(16, 72)]; U = [(c, w) for c, w in U if len(c)]
D = list(range(2, 13))
def count(pages, n, inword):
    out = np.zeros(len(D), int)
    for c, w in pages:
        for j, d in enumerate(D):
            L = len(c) - d - n + 1
            if L <= 0: continue
            eq = np.ones(L, bool)
            for t in range(n): eq &= c[t:t + L] == c[d + t:d + t + L]
            if inword: eq &= w[:L] == w[d + n - 1:d + n - 1 + L]
            out[j] += int(eq.sum())
    return out
obs = {(n, iw): count(U, n, iw) for n in (2, 3) for iw in (True, False)}
NREP = 999; samp = {k: np.zeros((NREP, len(D)), int) for k in obs}
for r in range(NREP):
    P = [(rng.permutation(c), w) for c, w in U]
    for k in samp: samp[k][r] = count(P, *k)
out = ["# Repeated bigrams and trigrams at lag d", "", "Positions whose n-gram recurs exactly d runes later; 'inside words' requires the whole span to lie in one word. Null: 999 within-page shuffles, word structure fixed.", ""]
for (n, iw) in obs:
    out += [f"## {'Bigrams' if n == 2 else 'Trigrams'}, {'inside words' if iw else 'anywhere on the page'}", "", "| lag d | observed | null mean ± sd | z | one-sided p |", "|---|---|---|---|---|"]
    mu, sd = samp[(n, iw)].mean(0), samp[(n, iw)].std(0) + 1e-9
    for j, d in enumerate(D):
        o = obs[(n, iw)][j]; p = (np.sum(samp[(n, iw)][:, j] >= o) + 1) / (NREP + 1)
        out.append(f"| {d} | {o} | {mu[j]:.1f} ± {sd[j]:.1f} | {(o - mu[j]) / sd[j]:+.2f} | {p:.3f} |")
    out.append("")
(RESULTS / "ngram_lag.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
