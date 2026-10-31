"""Lag-5 equality conditional on the lag-6 relation, and the converse, under the K-fixed null (2026-10-31; row C9).

Registered in results/quorum_checks_registration.md (committed before this run), answering the Quorum panel's ask-next
(quorumsays.com/q/36o14sRgY65E): a fixed lag-6 echo could manufacture lag-5 coincidences, so the lag-5 excess should be
measured among lag-5 pairs that touch no lag-6 site. Definitions as in §42/§45 and src/kfixed_echo.py: within-word pairs;
lag-6 site c_i = 24 - 2 c_(i-6); lag-5 site c_j = c_(j-5); a pair touches the other relation when either of its positions
is an endpoint of one of its sites. Null: K-fixed Metropolis arrangements per page (rune multiplicities, word structure and
adjacent-repeat count fixed; 20 burn-in, 4 thinning attempted transpositions per rune; 999 replicates; seed 1034); the
strata are recomputed in every null arrangement. Output: results/lag5_given_lag6.md.
Reproduce: .venv/bin/python -I src/lag5_given_lag6.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
from kfixed import kfixed_step, doublets

t0 = time.time(); rng = np.random.default_rng(1034); NREP, BURN, THIN = 999, 20, 4
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§'); S = LATIN.index("S")
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0]) > 6]
NAMES = ["lag-5 equal, free", "lag-5 equal, touching", "lag-5 pairs, free", "lag-5 pairs, touching",
         "lag-6 hits, free", "lag-6 hits, touching", "lag-6 pairs, free", "lag-6 pairs, touching",
         "lag-5 S..S, free", "lag-5 S..S, touching"]

def stats(pages):
    out = np.zeros(10, int)
    for c, w in pages:
        L = len(c)
        i6 = np.arange(6, L); m6 = w[i6] == w[i6 - 6]; h6 = (c[i6] == (24 - 2 * c[i6 - 6]) % N) & m6
        E6 = np.zeros(L, bool); E6[i6[h6]] = True; E6[i6[h6] - 6] = True
        i5 = np.arange(5, L); m5 = w[i5] == w[i5 - 5]; e5 = (c[i5] == c[i5 - 5]) & m5
        E5 = np.zeros(L, bool); E5[i5[e5]] = True; E5[i5[e5] - 5] = True
        t5 = E6[i5] | E6[i5 - 5]; t6 = E5[i6] | E5[i6 - 6]; ss = e5 & (c[i5] == S)
        out += np.array([(e5 & ~t5).sum(), (e5 & t5).sum(), (m5 & ~t5).sum(), (m5 & t5).sum(),
                         (h6 & ~t6).sum(), (h6 & t6).sum(), (m6 & ~t6).sum(), (m6 & t6).sum(),
                         (ss & ~t5).sum(), (ss & t5).sum()], int)
    return out

obs = stats(U)
cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
for c, _ in cur: kfixed_step(c, BURN * len(c), rng)
samp = np.zeros((NREP, 10), int)
for r in range(NREP):
    for c, _ in cur: kfixed_step(c, THIN * len(c), rng)
    samp[r] = stats(cur)
    if (r + 1) % 50 == 0: print(f"rep {r+1}/{NREP} [{time.time()-t0:.0f}s]", flush=True)
assert all(doublets(c) == k for (c, _), k in zip(cur, ks))
mu, sd = samp.mean(0), samp.std(0)
rows = ["| statistic | observed | K-fixed null mean ± sd | z | one-sided p (≥) |", "|---|---|---|---|---|"]
for j, nm in enumerate(NAMES):
    z = (obs[j] - mu[j]) / sd[j] if sd[j] > 0 else float("nan"); p = (np.sum(samp[:, j] >= obs[j]) + 1) / (NREP + 1)
    rows.append(f"| {nm} | {obs[j]} | {mu[j]:.1f} ± {sd[j]:.1f} | {z:+.2f} | {p:.3f} |")
z5f = (obs[0] - mu[0]) / sd[0]; z6f = (obs[4] - mu[4]) / sd[4]
out = ["# Lag-5 equality conditional on the lag-6 relation, and the converse (row C9)", "",
       f"{sum(len(c) for c, _ in U):,} runes on {len(U)} unsolved pages; within-word pairs; null = {NREP} K-fixed arrangements per page (src/kfixed.py; {BURN} burn-in, {THIN} thinning attempted transpositions per rune; seed 1034), strata recomputed inside each arrangement. A lag-5 pair is *touching* when either position is an endpoint of a lag-6 site c_i = 24 − 2·c_(i−6) inside a word, else *free*; the converse likewise.", ""] + rows + ["",
       f"- C9-P1 (free lag-5 stratum carries the excess: ratio ≥ 1.25 and z ≥ +2.5): observed / null mean = {obs[0]/mu[0]:.2f}, z = {z5f:+.2f} → **{'holds' if (obs[0]/mu[0] >= 1.25 and z5f >= 2.5) else 'fails'}**.",
       f"- C9-P2 (touching lag-5 stratum holds fewer than 10 equalities): {obs[1]} → **{'holds' if obs[1] < 10 else 'fails'}**.",
       f"- C9-P3 (free lag-6 stratum shows the relation at z ≥ +3): z = {z6f:+.2f} → **{'holds' if z6f >= 3 else 'fails'}**.",
       f"- Falsifier (free lag-5 z < +1.5 and touching ≥ 15): {'triggered' if (z5f < 1.5 and obs[1] >= 15) else 'not triggered'}.", "",
       "Reading: written after the run, below. [stated — the table]", "",
       f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/lag5_given_lag6.py`.", ""]
(RESULTS / "lag5_given_lag6.md").write_text("\n".join(out)); print("\n".join(out))
