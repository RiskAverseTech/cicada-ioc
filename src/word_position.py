"""Lag laws or word-position laws? The two-dimensional word-position table (registration: results/word_position_registration.md,
commit 26b20e4).  Pairs inside words indexed by (position of the earlier rune, position of the later) from the word's start,
and by distances from its end; equality and affine-hit counts per cell; K-fixed null (999 arrangements per page); family-wise
over the 66 cells of each table; the diagonal's sharpening by multinomial chi-square; a fixed held-out split (even pages A,
odd pages B).  Reproduce: .venv/bin/python -I src/word_position.py
"""
import sys, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N
from kfixed import kfixed_step, doublets

t0 = time.time(); rng = np.random.default_rng(1034); NREP, BURN, THIN = 999, 20, 4; PMAX = 12; NMULTI = 10000
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)


U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0]) > 6]; assert len(U) == 55
CELLS = [(a, b) for a in range(PMAX) for b in range(a + 1, PMAX)]; CID = {c: k for k, c in enumerate(CELLS)}; NC = len(CELLS); assert NC == 66

# fixed pair structure per page: (i, j, start cell, end cell), -1 where a position exceeds PMAX - 1
PAIRS = []
for c, w in U:
    L = len(c); starts = {}; ends = {}
    for i in range(L): starts.setdefault(w[i], i); ends[w[i]] = i
    I, J, CS, CE = [], [], [], []
    for i in range(L):
        for j in range(i + 1, min(L, i + PMAX)):
            if w[j] != w[i]: break
            ps, pj = i - starts[w[i]], j - starts[w[i]]; ds, dj = ends[w[i]] - j, ends[w[i]] - i          # end distances: later rune ds, earlier rune dj
            I.append(i); J.append(j); CS.append(CID.get((ps, pj), -1)); CE.append(CID.get((ds, dj), -1))
    PAIRS.append((np.array(I), np.array(J), np.array(CS), np.array(CE)))


def tables(pages, sel=None):
    """four 66-cell count tables: equality by start, affine by start, equality by end, affine by end"""
    out = np.zeros((4, NC), int)
    for k, (c, w) in enumerate(pages):
        if sel is not None and k not in sel: continue
        I, J, CS, CE = PAIRS[k]; eq = c[I] == c[J]; af = c[J] == (24 - 2 * c[I]) % N
        for t, (mask, cells) in enumerate(((eq, CS), (af, CS), (eq, CE), (af, CE))):
            m = mask & (cells >= 0); out[t] += np.bincount(cells[m], minlength=NC)
    return out


A = set(range(0, 55, 2)); B = set(range(1, 55, 2))
obs = tables(U); obsA = tables(U, A); obsB = tables(U, B)
cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
for c, _ in cur: kfixed_step(c, BURN * len(c), rng)
S, SA, SB = np.zeros((NREP, 4, NC), int), np.zeros((NREP, 4, NC), int), np.zeros((NREP, 4, NC), int)
for r in range(NREP):
    for c, _ in cur: kfixed_step(c, THIN * len(c), rng)
    S[r] = tables(cur); SA[r] = tables(cur, A); SB[r] = S[r] - SA[r]
    if (r + 1) % 200 == 0: log("rep", r + 1)
assert all(doublets(c) == k for (c, _), k in zip(cur, ks))


def zs(o, s):
    mu, sd = s.mean(0), s.std(0); sd = np.where(sd > 0, sd, np.inf); z = (o - mu) / sd; zn = (s - mu) / sd
    fw = np.array([[(np.sum(zn[:, t].max(1) >= z[t, k]) + 1) / (NREP + 1) for k in range(NC)] for t in range(4)])
    return z, fw, mu, sd


z, fw, mu, sd = zs(obs, S); zA, fwA, _, _ = zs(obsA, SA); zB, fwB, muB, sdB = zs(obsB, SB)
pB = np.array([[(np.sum(SB[:, t, k] >= obsB[t, k]) + 1) / (NREP + 1) for k in range(NC)] for t in range(4)])
NAMES = ["equality, from start", "affine 24−2c, from start", "equality, from end", "affine 24−2c, from end"]
LAGD = [5, 6, 5, 6]
def diag(t): return [CID[(a, a + LAGD[t])] for a in range(PMAX - LAGD[t])]


def sharpen(t):
    cells = diag(t); o = obs[t, cells]; share = mu[t, cells] / mu[t, cells].sum(); n = int(o.sum()); e = n * share
    chi = float(((o - e) ** 2 / e).sum()); draws = np.random.default_rng(5).multinomial(n, share, size=NMULTI); chid = ((draws - e) ** 2 / e).sum(1)
    return chi, float((np.sum(chid >= chi) + 1) / (NMULTI + 1)), n, o.tolist(), np.round(e, 1).tolist()


SH = [sharpen(t) for t in range(4)]
sig = {t: [k for k in range(NC) if fw[t, k] < 0.05] for t in range(4)}
offdiag = {t: [k for k in sig[t] if (CELLS[k][1] - CELLS[k][0]) != LAGD[t]] for t in range(4)}
sigA = {t: [k for k in range(NC) if fwA[t, k] < 0.05] for t in range(4)}
rep = {t: [(k, float(pB[t, k])) for k in sigA[t]] for t in range(4)}
w1 = all(not offdiag[t] for t in range(4)); w2 = all(SH[t][1] >= 0.05 for t in range(4))
w3 = all(((CELLS[k][1] - CELLS[k][0]) == LAGD[t]) or (p >= 0.05) for t in range(4) for k, p in rep[t])

o = ["# Lag laws or word-position laws: the two-dimensional word-position table", "",
     f"Registration: `results/word_position_registration.md`. Pairs inside words with both positions below {PMAX}; 66 cells per table; K-fixed null {NREP} arrangements per page; family-wise p from the largest cell z of each table; held-out halves A (even pages) and B (odd pages).", "",
     "## Cells at family-wise p < 0.05 on the full set", "", "| table | cell (earlier, later) | lag | observed | null mean ± sd | z | family-wise p |", "|---|---|---|---|---|---|---|"]
for t in range(4):
    for k in sorted(sig[t], key=lambda k: -z[t, k]): o.append(f"| {NAMES[t]} | {CELLS[k]} | {CELLS[k][1] - CELLS[k][0]} | {obs[t, k]} | {mu[t, k]:.1f} ± {sd[t, k]:.1f} | {z[t, k]:+.2f} | {fw[t, k]:.3f} |")
    if not sig[t]: o.append(f"| {NAMES[t]} | none | | | | | |")
o += ["", "Largest cell z per table and its family-wise p: " + "; ".join(f"{NAMES[t]} {z[t].max():+.2f} ({fw[t, int(np.argmax(z[t]))]:.3f})" for t in range(4)) + ".", "",
      "## Sharpening along the lag diagonal", "", "| table | diagonal cells (earlier position …) | observed counts | null-share expectation | χ² | multinomial p |", "|---|---|---|---|---|---|"]
for t in range(4):
    chi, p, n, oo, ee = SH[t]; o.append(f"| {NAMES[t]} | lag {LAGD[t]}, {len(oo)} cells, n = {n} | {oo} | {ee} | {chi:.1f} | {p:.3f} |")
o += ["", "## Held-out halves", "", "| table | cells family-wise < 0.05 on A | lag | replication on B (one-sided p) |", "|---|---|---|---|"]
for t in range(4):
    if rep[t]:
        for k, p in rep[t]: o.append(f"| {NAMES[t]} | {CELLS[k]} | {CELLS[k][1] - CELLS[k][0]} | {p:.3f} |")
    else: o.append(f"| {NAMES[t]} | none | | |")
o += ["", "## Registered predictions", "",
      f"- W1 (no off-diagonal cell at family-wise p < 0.05): " + ("none" if w1 else "; ".join(f"{NAMES[t]} {[CELLS[k] for k in offdiag[t]]}" for t in range(4) if offdiag[t])) + f" → {'holds' if w1 else 'fails'}.",
      f"- W2 (no sharpening along the diagonals): multinomial p " + ", ".join(f"{SH[t][1]:.3f}" for t in range(4)) + f" → {'holds' if w2 else 'fails'}.",
      f"- W3 (off-diagonal cells on A do not replicate on B): {sum(len(v) for v in rep.values())} cells significant on A → {'holds' if w3 else 'fails'}.", "",
      f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/word_position.py`.", ""]
(RESULTS / "word_position.md").write_text("\n".join(o)); print("\n".join(o))
json.dump(dict(z=z.tolist(), fw=fw.tolist(), obs=obs.tolist(), mu=mu.tolist(), sharpen=SH, sigA={str(t): v for t, v in sigA.items()}, rep={str(t): v for t, v in rep.items()}, cells=CELLS), open(RESULTS / "word_position.json", "w"), indent=1)
