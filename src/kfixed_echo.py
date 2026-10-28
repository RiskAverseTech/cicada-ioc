"""Within-word lag-d echo under a K-fixed null (2026-10-28).

ZzNible reports within-word lag-5 equalities at z 3.75 (family-wise p 0.0086 over d = 2..12) under a null that
keeps word lengths, rune multiplicities AND the number of adjacent repeats K = 86.  Section 15 here did not
replicate the echo under a plain within-page shuffle, which lets K float to ~445.  A K-fixed null is sampled
here by a Metropolis walk on within-page transpositions accepted only when the page's repeat count is unchanged
(symmetric proposals, so the stationary law is uniform over the arrangements with that repeat count).
Statistic: for d = 2..12, the number of within-word pairs (i-d, i) with equal runes; family-wise p by the
maximum z over d.  Writes results/kfixed_echo.md.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N

rng = np.random.default_rng(1033)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')   # '/' is a line break, which falls inside words 452 times of 630; not a word boundary
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
U = [parse(chunks[k]) for k in range(16, 72)]
D = range(2, 13)

def echo_counts(pages):
    out = np.zeros(len(D), int)
    for c, w in pages:
        for j, d in enumerate(D):
            if len(c) <= d: continue
            m = (w[d:] == w[:-d])
            out[j] += int(((c[d:] == c[:-d]) & m).sum())
    return out

def doublets(c): return int((c[1:] == c[:-1]).sum())

def kfixed_step(c, k, nswap):
    """nswap accepted transpositions that keep the repeat count k (Metropolis, uniform target)."""
    L = len(c); acc = 0
    while acc < nswap:
        i, j = rng.integers(0, L, 2)
        if i == j or c[i] == c[j]: acc += 1; continue
        # local repeat count before/after around i and j
        idx = set()
        for t in (i, j):
            if t > 0: idx.add(t - 1)
            if t < L - 1: idx.add(t)
        before = sum(c[t] == c[t + 1] for t in idx)
        c[i], c[j] = c[j], c[i]
        after = sum(c[t] == c[t + 1] for t in idx)
        if after != before: c[i], c[j] = c[j], c[i]
        else: acc += 1
    return c

obs = echo_counts(U)
NREP = 999; BURN = 20; THIN = 4   # in units of page length (accepted swaps per rune)
cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
for (c, _), k in zip(cur, ks): kfixed_step(c, k, BURN * len(c))
samp = np.zeros((NREP, len(D)), int)
for r in range(NREP):
    for (c, _), k in zip(cur, ks): kfixed_step(c, k, THIN * len(c))
    samp[r] = echo_counts(cur)
assert all(doublets(c) == k for (c, _), k in zip(cur, ks))
mu, sd = samp.mean(0), samp.std(0); z = (obs - mu) / sd
zmax_null = ((samp - mu) / sd).max(1)
rows = ["| lag d | within-word equal pairs observed | K-fixed null mean ± sd | z | one-sided p |", "|---|---|---|---|---|"]
for j, d in enumerate(D):
    p = (np.sum(samp[:, j] >= obs[j]) + 1) / (NREP + 1)
    rows.append(f"| {d} | {obs[j]} | {mu[j]:.1f} ± {sd[j]:.1f} | {z[j]:+.2f} | {p:.3f} |")
fw = (np.sum(zmax_null >= z.max()) + 1) / (NREP + 1)
out = ["# Within-word lag echo under a K-fixed null", "", f"{sum(len(c) for c, _ in U):,} runes on the 55 unsolved pages; null = {NREP} arrangements per page with the page's own rune multiplicities, word structure and adjacent-repeat count (K = {sum(ks)}) held fixed, sampled by a Metropolis walk on transpositions ({BURN} burn-in and {THIN} thinning swaps per rune).", ""] + rows + ["",
       f"Family-wise over d = 2..12: largest z is {z.max():+.2f} at lag {list(D)[int(z.argmax())]}; the null's largest z is {zmax_null.mean():.2f} ± {zmax_null.std():.2f}; p = {fw:.3f}.", ""]
(RESULTS / "kfixed_echo.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
