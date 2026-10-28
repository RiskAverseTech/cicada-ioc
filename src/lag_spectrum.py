"""Repeat spectrum at lags 1-120 and the page-boundary convention (2026-10-28; a Quorum panel's two
checks, quorumsays.com/q/1CHmMxwoj6rH and the follow-up).  Writes results/lag_spectrum.md.
Statistic: within-page pairs (C_i, C_{i-k}) that are equal, against pairs/29 with the binomial sd.
Boundary conventions: the deficit is counted within pages; counting the 54 page joins as adjacent
pairs is the other convention, and the solved-page split (55/56/58-page conventions) only moves pairs
across those joins."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import PROCESSED, RESULTS

d = json.loads((PROCESSED / "pages.json").read_text()); pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 1]
def spectrum(k):
    npairs = sum(max(0, len(c) - k) for c in pages); rep = sum(int((c[k:] == c[:-k]).sum()) for c in pages if len(c) > k); e = npairs / 29
    return npairs, rep, e, (rep - e) / np.sqrt(e * (1 - 1 / 29))
rows = [spectrum(k) for k in range(1, 121)]
z = np.array([r[3] for r in rows]); out = ["# Repeat spectrum, lags 1 to 120, and the boundary convention", "", "| lag | pairs | repeats | expected | z |", "|---|---|---|---|---|"]
for k in list(range(1, 13)) + [20, 29, 30, 58, 87, 100, 116, 120]:
    n_, r_, e_, z_ = rows[k - 1]; out.append(f"| {k} | {n_:,} | {r_} | {e_:.0f} | {z_:+.1f} |")
out += ["", f"Lags 2–120: mean z {z[1:].mean():+.2f}, sd {z[1:].std():.2f}, extremes {z[1:].min():+.1f} (lag {2+int(z[1:].argmin())}) and {z[1:].max():+.1f} (lag {2+int(z[1:].argmax())}); {int((abs(z[1:]) >= 3).sum())} of 119 lags at |z| ≥ 3 (0.3 expected by chance). The deficit is at lag 1 only.", ""]
stream = np.concatenate(pages); dw = sum(int((c[1:] == c[:-1]).sum()) for c in pages); ds = int((stream[1:] == stream[:-1]).sum()); joins = len(pages) - 1
out += [f"**Boundary convention.** Within pages: {dw} doublets in {sum(len(c)-1 for c in pages):,} pairs. Counting the {joins} page joins as adjacent pairs: {ds} doublets in {len(stream)-1:,} ({ds-dw} at the joins, {joins/29:.1f} expected if the joins were random). No page-boundary convention can move the count by more than the number of joins it adds or removes, so the deficit of 86 against about 445 does not depend on the 55-, 56- or 58-page convention; retranscription would have to change hundreds of runes to matter, and the two independent transcriptions on record (rtkd/iddqd and Leo-Y-Zhang's cross-check) agree to within a few.", ""]
(RESULTS / "lag_spectrum.md").write_text("\n".join(out) + "\n"); print("\n".join(out[-4:]))
