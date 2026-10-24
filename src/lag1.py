"""Diagnose the lag-1 signal: which adjacent-rune differences are over/under-represented
in the unsolved ciphertext, how it is spread across pages, and what a constant-key
(period-1) cipher would have produced instead."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from depth_two import sd_null, PI

d = json.loads((PROCESSED / "pages.json").read_text())
pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
ids = [u["id"] for u in d["unsolved"] if u["length"] > 0]
plain = [np.array(s["plaintext"]) for s in d["solved"]]


def lag_ic(x, L):
    dd = (x[:-L] - x[L:]) % N
    c = np.bincount(dd, minlength=N)
    return (c * (c - 1)).sum() / (len(dd) * (len(dd) - 1)), c


# Pooled lag-1 difference distribution over all unsolved pages.
tot = np.zeros(N, dtype=int)
per_page = []
for x, i in zip(pages, ids):
    s, c = lag_ic(x, 1)
    tot += c
    per_page.append((i, len(x) - 1, s, (s - PI) / sd_null(len(x) - 1), c[0]))
M = tot.sum()
exp = M / N
z = (tot - exp) / np.sqrt(exp * (1 - 1 / N))
lines = ["# Lag-1 diagnostic (adjacent runes in the unsolved pages)", "",
         f"Adjacent pairs pooled over {len(pages)} pages: {M}. Expected count per difference class d = C[t] - C[t+1] mod 29: {exp:.1f}.", "",
         "| d | count | z vs uniform |", "|---|---|---|"]
for dd in np.argsort(-np.abs(z))[:8]:
    lines.append(f"| {dd} | {tot[dd]} | {z[dd]:+.2f} |")
lines += ["", f"Doublets (d = 0, same rune twice in a row): {tot[0]} observed vs {exp:.1f} expected, z = {z[0]:+.2f}.",
          f"Chi-square of the 29 difference classes: {float(((tot-exp)**2/exp).sum()):.1f} on 28 dof.", "",
          "## Per page", "", "Lag-1 sigma per page (positive = non-uniform adjacent differences). Count of pages above +2: "
          f"{sum(1 for r in per_page if r[3] > 2)}, below -2: {sum(1 for r in per_page if r[3] < -2)}, mean {np.mean([r[3] for r in per_page]):+.2f}.", "",
          "| page | N | lag-1 IC | sigma | doublets |", "|---|---|---|---|---|"]
for r in sorted(per_page, key=lambda r: -r[3])[:10]:
    lines.append(f"| {r[0]} | {r[1]} | {r[2]:.4f} | {r[3]:+.2f} | {r[4]} |")

# What a constant key (period-1 generator, i.e. a plain shift) would give: the plaintext's own lag-1 IC.
pl = np.concatenate(plain)
q1 = sum(lag_ic(x, 1)[1] for x in plain)
q1 = (q1 * (q1 - 1)).sum() / (sum(len(x) - 1 for x in plain) * (sum(len(x) - 1 for x in plain) - 1))
pred = sum((q1 - PI) / sd_null(len(x) - 1) for x in pages) / np.sqrt(len(pages))
pl_doublets = sum((x[:-1] == x[1:]).sum() for x in plain); pl_pairs = sum(len(x) - 1 for x in plain)
lines += ["", "## Against a constant-key reading", "",
          f"The solved plaintext has lag-1 difference IC {q1:.4f} (doublet rate {pl_doublets/pl_pairs:.4f} vs 1/29 = {PI:.4f}). "
          f"If every unsolved page were a constant-key (shift / simple substitution) cipher, the pooled lag-1 z would be about {pred:.0f}; "
          f"the observed pooled z is {sum(r[3] for r in per_page)/np.sqrt(len(pages)):.2f}.", ""]
(RESULTS / "lag1.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
