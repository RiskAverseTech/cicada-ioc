"""The line-first rune and the line-column coincidence profile (2026-10-30; registration results/line_column_registration.md).

§63's Q3 failed on one rule: the first rune of each line has pooled IoC 1.090, z +7.1 against per-page shuffles.  Here every
in-line column j (from the start, 0-15; from the end, 0-5) gets the pooled IoC (x29) over the 55 unsolved pages and the
within-page same-column coincidence count, each with a z against 2,000 within-page shuffles that keep the line lengths;
the same with the first line of each page removed.  Claims R1-R4 in the registration.  Output: results/line_column.md.
Reproduce: .venv/bin/python -I src/line_column.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N
from score import translit
from scipy.stats import chisquare

t0 = time.time(); rng = np.random.default_rng(63); NSH = 2000; JS, JE = 16, 6
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
pages = []                                          # list of pages; a page is a list of lines; a line is an int array
for k in range(16, 72):
    lines = [np.array([IDX[ch] for ch in ln if ch in IDX], int) for ln in chunks[k].split("/")]
    lines = [l for l in lines if len(l)]
    if lines: pages.append(lines)
LET = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()


def columns(pg, drop_first):
    """per page: dict (side, j) -> runes of that column across the page's lines"""
    out = {}
    for li, l in enumerate(pg):
        if drop_first and li == 0: continue
        for j in range(min(JS, len(l))): out.setdefault(("start", j), []).append(l[j])
        for j in range(min(JE, len(l))): out.setdefault(("end", j), []).append(l[len(l) - 1 - j])
    return out


KEYS = [("start", j) for j in range(JS)] + [("end", j) for j in range(JE)]


def stats(pgs, drop_first):
    """pooled IoC x29 and within-page coincidence count per column"""
    pool = {k: np.zeros(N, int) for k in KEYS}; within = {k: 0 for k in KEYS}
    for pg in pgs:
        for k, v in columns(pg, drop_first).items():
            c = np.bincount(v, minlength=N); pool[k] += c; within[k] += int((c * (c - 1)).sum() // 2)
    ioc = {k: (N * (pool[k] * (pool[k] - 1)).sum() / (pool[k].sum() * (pool[k].sum() - 1)) if pool[k].sum() > 1 else np.nan) for k in KEYS}
    return ioc, within, pool


def shuffled(pgs):
    out = []
    for pg in pgs:
        flat = np.concatenate(pg); flat = flat[rng.permutation(len(flat))]; cut = np.cumsum([len(l) for l in pg])[:-1]
        out.append(np.split(flat, cut))
    return out


res = {}
for drop_first in (False, True):
    ioc, within, pool = stats(pages, drop_first)
    si = {k: [] for k in KEYS}; sw = {k: [] for k in KEYS}
    for _ in range(NSH):
        i2, w2, _ = stats(shuffled(pages), drop_first)
        for k in KEYS: si[k].append(i2[k]); sw[k].append(w2[k])
    res[drop_first] = {k: dict(n=int(pool[k].sum()), ioc=ioc[k], zi=(ioc[k] - np.mean(si[k])) / np.std(si[k]), within=within[k],
                               zw=(within[k] - np.mean(sw[k])) / np.std(sw[k])) for k in KEYS}
    print(f"{'without' if drop_first else 'with'} first lines done [{time.time()-t0:.0f}s]", flush=True)

A, B = res[False], res[True]
def cell_ok(side, js, src):
    zs = [abs(src[(side, j)][w]) for j in js for w in ("zi", "zw")]
    return (max(zs) < 4) and (sum(z >= 3 for z in zs) < 2), max(zs)
R1 = A[("start", 0)]["zi"] >= 4
R2, R2max = cell_ok("start", range(1, 6), A)
R3 = B[("start", 0)]["zi"] >= 4
R4, R4max = cell_ok("end", range(0, 6), A)
allr = np.concatenate([np.concatenate(pg) for pg in pages]); e = np.bincount(allr, minlength=N) / len(allr)
col0 = np.concatenate([[l[0] for l in pg] for pg in pages]); c0 = np.bincount(col0, minlength=N); chi, p = chisquare(c0, e * len(col0))
order = np.argsort(-(c0 - e * len(col0)))

out = ["# The line-first rune and the line-column coincidence profile", "",
       f"55 unsolved pages, {sum(len(pg) for pg in pages)} lines. Per in-line column: pooled IoC (× 29) over all pages and the within-page same-column coincidence count; z against {NSH:,} within-page shuffles that keep the line lengths. Registration: `results/line_column_registration.md`.", "",
       "| column | runes | pooled IoC | z | within-page coincidences | z | without first lines: pooled z | within z |", "|---|---|---|---|---|---|---|---|"]
for k in KEYS:
    a, b = A[k], B[k]
    out.append(f"| {k[0]} {k[1]} | {a['n']} | {a['ioc']:.3f} | {a['zi']:+.1f} | {a['within']} | {a['zw']:+.1f} | {b['zi']:+.1f} | {b['zw']:+.1f} |")
out += ["", "## Claims", "",
        f"- R1 column 0 pooled z ≥ 4: **{'holds' if R1 else 'fails'}** (z {A[('start',0)]['zi']:+.1f}).",
        f"- R2 columns 1–5, pooled and within page, no cell at 4 and at most one at 3: **{'holds' if R2 else 'fails'}** (largest |z| {R2max:.1f}).",
        f"- R3 column 0 keeps z ≥ 4 without the first line of each page: **{'holds' if R3 else 'fails'}** (z {B[('start',0)]['zi']:+.1f}).",
        f"- R4 the from-end columns 0–5 by the R2 rule: **{'holds' if R4 else 'fails'}** (largest |z| {R4max:.1f}).", "",
        "## Column 0 against the pages' rune distribution", "",
        f"χ² {chi:.1f} on 28 df, p {p:.1e}. Over: " + ", ".join(f"{LET[i]} {c0[i]} vs {e[i]*len(col0):.1f}" for i in order[:6]) + ". Under: " + ", ".join(f"{LET[i]} {c0[i]} vs {e[i]*len(col0):.1f}" for i in order[-6:]) + ".", "",
        "Column streams in transliteration (first 120 runes each):", ""]
for j in range(3):
    s = np.concatenate([[l[j] for l in pg if len(l) > j] for pg in pages]); out.append(f"- column {j}: `{translit(s)[:120]}`")
out += ["", "Reading: written after the run. [stated — the table]", "", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/line_column.py`.", ""]
(RESULTS / "line_column.md").write_text("\n".join(out)); print("\n".join(out[4:8] + out[-14:-4]))
