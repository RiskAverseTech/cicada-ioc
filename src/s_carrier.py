"""Look-elsewhere calibration of the S carrier (2026-10-28).  LP2's within-word lag-5 equal pairs are S 11 times
(3.5 expected).  Under the K-fixed Metropolis null of src/kfixed_echo.py (rune multiplicities, word structure and
repeat count per page held), the largest z over all 29 runes x lags 2..12 is recorded per replicate, so the
S-at-lag-5 cell can be judged against the maximum of 319 cells.  Writes results/s_carrier.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
rng = np.random.default_rng(1033)
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
def cell_counts(pages):
    out = np.zeros((N, len(D)), int)
    for c, w in pages:
        for j, d in enumerate(D):
            if len(c) <= d: continue
            m = (w[d:] == w[:-d]) & (c[d:] == c[:-d]); out[:, j] += np.bincount(c[d:][m], minlength=N)
    return out
from kfixed import kfixed_step, doublets   # attempt-counting clock (2026-10-29, §56)
obs = cell_counts(U); NREP = 999
cur = [(c.copy(), w) for c, w in U]
for c, _ in cur: kfixed_step(c, 20 * len(c), rng)
samp = np.zeros((NREP, N, len(D)), int)
for r in range(NREP):
    for c, _ in cur: kfixed_step(c, 4 * len(c), rng)
    samp[r] = cell_counts(cur)
mu, sd = samp.mean(0), samp.std(0) + 1e-9; z = (obs - mu) / sd
zmax = ((samp - mu) / sd).max(axis=(1, 2))
np.savez_compressed(RESULTS / "s_carrier_samples.npz", samp=samp, obs=obs)
# z over-rewards sparse cells (count 1 against 0.0 ± 0.2 is z +5); the calibrated statistic is the smallest
# Poisson tail probability over the 319 cells, for LP2 and for every replicate
from scipy import stats
def minp(counts): return stats.poisson.sf(counts - 1, mu + 1e-9).min()
p_lp2 = minp(obs); p_null = np.array([minp(samp[r]) for r in range(NREP)])
p_s5 = stats.poisson.sf(obs[LATIN.index("S"), D.index(5)] - 1, mu[LATIN.index("S"), D.index(5)])
cal = (np.sum(p_null <= p_lp2) + 1) / (NREP + 1)
s5 = z[LATIN.index("S"), D.index(5)]
top = sorted(((z[r, j], r, D[j]) for r in range(N) for j in range(len(D))), reverse=True)[:6]
out = ["# The S carrier of the lag-5 echo, calibrated over 29 runes x 11 lags", "",
       f"K-fixed null ({NREP} replicates; multiplicities, word structure and repeat count held per page). Cell = within-word equal pairs at lag d whose rune is r.", "",
       "| rune | lag | observed | null mean ± sd | z |", "|---|---|---|---|---|"] + [f"| {LATIN[r]} | {d} | {obs[r, D.index(d)]} | {mu[r, D.index(d)]:.1f} ± {sd[r, D.index(d)]:.1f} | {zz:+.2f} |" for zz, r, d in top] + ["",
       f"S at lag 5: z {s5:+.2f}. The null's largest z over the 319 cells is {zmax.mean():.2f} ± {zmax.std():.2f}; replicates whose maximum reaches LP2's S-at-lag-5 value: {(np.sum(zmax >= s5) + 1) / (NREP + 1):.3f}. "
       f"Note that the maximum over all cells in LP2 is {top[0][0]:+.2f} ({LATIN[top[0][1]]} at lag {top[0][2]}).", "",
       f"The z maximum is a poor instrument here: a count of 1 in a cell whose null is 0.0 ± 0.2 scores z +5, so sparse high-lag cells dominate the null's maximum. The calibrated statistic is the smallest Poisson tail probability over the 319 cells: LP2's is {p_lp2:.2e} (the S-at-lag-5 cell, Poisson tail {p_s5:.2e} at mean {mu[LATIN.index('S'), D.index(5)]:.2f}); the null's smallest-p reaches that value in {cal:.3f} of replicates (median null min-p {np.median(p_null):.2e}). That is the look-elsewhere-corrected p of the S carrier.", ""]
(RESULTS / "s_carrier.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
