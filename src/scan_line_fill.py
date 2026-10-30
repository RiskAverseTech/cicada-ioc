"""Is the line-first rune effect the greedy line fill? (2026-10-30; registration results/line_fill_registration.md). G1: right-hand slack of a line against the next line's first glyph; G2: line-start counts against a width-weighted prediction. Needs results/scan_glyphs.json.
The scans are not vendored: SCANS=/path/to/liber-primus-complete (default ~/Desktop/cicada-images/liber-primus-complete), 75 JPEGs from
github.com/scream314/cicada3301 assets/2014/liber-primus-complete, SHA-256 in results/scans_sha256.txt; image NN is transcription chunk NN-1.
"""
import os, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
SCANS = os.environ.get("SCANS", os.path.expanduser("~/Desktop/cicada-images/liber-primus-complete"))
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
import json, numpy as np
from collections import defaultdict
from scipy.stats import chisquare
LET = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
G = json.load(open(RESULTS_DIR / "scan_glyphs.json"))
pages = {}
for k, d in G.items():
    if int(k) in (65, 67): continue
    L = [l for l in d["lines"] if len(l) >= 4]; tl = d["tlines"]
    if len(L) == len(tl) + 1 and len(L[0]) <= 3: L = L[1:]
    if len(L) != len(tl): continue
    pages[int(k)] = (L, d["runes"])
# inter-glyph space: median gap between consecutive glyph boxes within aligned lines (excluding separator gaps = larger)
gaps = []
for k, (L, R) in pages.items():
    for gl in L:
        xs = sorted(gl, key=lambda g: g["x0"])
        for a, b in zip(xs, xs[1:]): gaps.append(b["x0"] - (a["x0"] + a["w"]))
gaps = np.array(gaps); s_glyph = float(np.median(gaps)); print(f"inter-glyph gap: median {s_glyph:.0f} px, 25-75 % {np.percentile(gaps,25):.0f}-{np.percentile(gaps,75):.0f}; separator gaps (>{s_glyph*2:.0f}) share {np.mean(gaps>2*s_glyph):.2f}")
# G1: slack vs next first glyph
ok = tot = 0; slacks = []; ratios = []
for k, (L, R) in pages.items():
    ends = [max(g["x0"] + g["w"] for g in gl if g["x0"] + g["w"] <= 1830) for gl in L]; W = max(ends)   # 1830: a margin-ornament piece reaching inside x 2000 counted as a glyph on twelve pages and set the edge 200 px too far right; no text line ends beyond 1800
    for i in range(len(L) - 1):
        if len(L[i]) < 8: continue
        nxt = sorted(L[i + 1], key=lambda g: g["x0"])[0]; slack = W - ends[i]; need = nxt["w"] + s_glyph
        tot += 1; ok += slack < need + 8; slacks.append(slack); ratios.append(slack / need)
print(f"G1: slack < next first glyph + space (+8 px tolerance) on {ok} of {tot} line pairs = {ok/tot:.3f}; slack median {np.median(slacks):.0f} px, 90 % {np.percentile(slacks,90):.0f}; slack/need median {np.median(ratios):.2f}, 90 % {np.percentile(ratios,90):.2f}")
# G2: width-weighted prediction for line-start counts (all 55 unsolved pages' transcription, not only aligned ones)
from lp import RAW, IDX, N
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
col0, allr = [], []
for k in range(16, 72):
    new = True
    for ch in chunks[k]:
        if ch == '/': new = True; continue
        if ch in IDX:
            allr.append(IDX[ch]);
            if new: col0.append(IDX[ch])
            new = False
c0 = np.bincount(col0, minlength=N); ca = np.bincount(allr, minlength=N)
w = np.zeros(N); byr = defaultdict(list)
for k, (L, R) in pages.items():
    for gl, rs in zip(L, R):
        if len(gl) != len(rs): continue
        for g, r in zip(sorted(gl, key=lambda g: g["x0"]), rs): byr[r].append(g["w"])
for r in range(N): w[r] = np.median(byr[r])
e_page = ca / ca.sum() * len(col0); chi0, p0 = chisquare(c0, e_page)
best = None
for s in np.arange(0, 80, 1.0):
    e = ca * (w + s); e = e / e.sum() * len(col0); chi, p = chisquare(c0, e)
    if best is None or chi < best[0]: best = (chi, p, s, e)
chi_s, p_s, s_fit, e_fit = best
e_m = ca * (w + s_glyph); e_m = e_m / e_m.sum() * len(col0); chi_m, p_m = chisquare(c0, e_m)
print(f"G2: chi2 vs page distribution {chi0:.1f} (p {p0:.1e}); vs width model at measured space s={s_glyph:.0f}: {chi_m:.1f} (p {p_m:.3f}); best s={s_fit:.0f}: {chi_s:.1f} (p {p_s:.3f})")
order = np.argsort(-(c0 - e_page))
print("rune: observed / page-expected / width-model-expected (measured s):")
print(", ".join(f"{LET[r]} {c0[r]}/{e_page[r]:.0f}/{e_m[r]:.0f}" for r in list(order[:8]) + list(order[-8:])))
print("residual z under the width model, largest:", sorted([(round(float((c0[r]-e_m[r])/np.sqrt(e_m[r])),1), LET[r]) for r in range(N)], key=lambda x: -abs(x[0]))[:6])
