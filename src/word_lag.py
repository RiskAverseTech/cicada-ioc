"""Within-word lag echo: do runes k apart *inside the same word* show any difference-class
structure, for k = 1..12?  The field survey quotes a lag-5/lag-6 within-word echo at about
2.5 sigma from another lab.  Pooled over all unsolved pages; null = runes shuffled within each
page with the word boundaries held fixed (300 replicates).  Statistics per lag: chi-square of
the 29 difference classes against uniform, and the count of the d = 0 class (repeat at distance k).
Writes results/word_lag.md."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *

E = json.loads((PROCESSED / "edges.json").read_text())
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
KMAX = 12
rng = np.random.default_rng(1113)


def word_ids(pid, n):
    w = np.zeros(n, dtype=int)
    for i in E[pid]["word_initial"]:
        w[i:] += 1
    return w


WID = {pid: word_ids(pid, len(x)) for pid, x in pages}


def stats(pg):
    counts = np.zeros((KMAX, N), dtype=int)
    for pid, x in pg:
        w = WID[pid]
        for k in range(1, KMAX + 1):
            same = w[:-k] == w[k:]
            dd = (x[:-k] - x[k:]) % N
            counts[k - 1] += np.bincount(dd[same], minlength=N)
    M = counts.sum(1)
    exp = M / N
    chi2 = ((counts - exp[:, None]) ** 2 / exp[:, None]).sum(1)
    return counts, M, chi2


counts, M, chi2 = stats(pages)
nchi, n0, nmax = [], [], []
for r in range(300):
    sh = [(pid, rng.permutation(x)) for pid, x in pages]
    c2, _, x2 = stats(sh)
    nchi.append(x2); n0.append(c2[:, 0]); nmax.append(np.abs((c2 - M[:, None] / N) / np.sqrt(M[:, None] / N)).max(1))
nchi = np.array(nchi); n0 = np.array(n0); nmax = np.array(nmax)

lines = ["# Within-word lag echo (lags 1-12)", "",
         f"{len(pages)} unsolved pages; pairs of runes k apart inside the same word (word boundaries from the master transcription). "
         "Null: 300 within-page shuffles with word boundaries fixed.", "",
         "| lag | pairs | chi2 (28 dof) | null chi2 mean ± sd | z | d=0 count | null d=0 mean ± sd | z | largest |z| class (obs) | null max |z| mean |",
         "|---|---|---|---|---|---|---|---|---|---|"]
for k in range(KMAX):
    zc = (chi2[k] - nchi[:, k].mean()) / nchi[:, k].std()
    z0 = (counts[k, 0] - n0[:, k].mean()) / n0[:, k].std()
    zcls = (counts[k] - M[k] / N) / np.sqrt(M[k] / N)
    top = int(np.argmax(np.abs(zcls)))
    lines.append(f"| {k+1} | {M[k]} | {chi2[k]:.1f} | {nchi[:, k].mean():.1f} ± {nchi[:, k].std():.1f} | {zc:+.2f} | {counts[k,0]} | {n0[:, k].mean():.1f} ± {n0[:, k].std():.1f} | {z0:+.2f} | d={top} ({zcls[top]:+.2f}) | {nmax[:, k].mean():.2f} |")
sig = [k + 1 for k in range(1, KMAX) if abs((chi2[k] - nchi[:, k].mean()) / nchi[:, k].std()) > 3]
lines += ["", f"Lag 1 is the known doublet deficit. Lags 2-12 with |z| > 3 on the chi-square: {sig or 'none'}. "
          "Twelve lags are tested, so one |z| near 2.5 is expected by chance about once in three such tables.", ""]
(RESULTS / "word_lag.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
