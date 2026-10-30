"""Line-initial glyphs on the scans against the rest of their lines and their own rune type; red glyphs read against the transcription (2026-10-30). Prints the tables quoted in README §65; needs results/scan_glyphs.json from scan_segment.py.
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
LET = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
G = json.load(open(RESULTS_DIR / "scan_glyphs.json"))
# 1. first glyph vs the rest of its line (lines with >= 8 glyphs, count within 1 of the transcription), skipping line 1 of each page
hr, wr, hr2, wr2, hrl, wrl = [], [], [], [], [], []
aligned = []   # (chunk, line idx, glyph list, rune list) with exact count match
for k, d in G.items():
    if int(k) in (65, 67): continue
    tl = d["tlines"]; L = d["lines"]
    # drop spurious tiny 'lines'
    L = [l for l in L if len(l) >= 4]
    # align by order after dropping; require same number of lines
    if len(L) != len(tl):
        # try dropping an initial ornament line
        if len(L) == len(tl) + 1 and len(L[0]) <= 3: L = L[1:]
        if len(L) == len(tl) + 1 and len(L[-1]) <= 3: L = L[:-1]
    if len(L) != len(tl): continue
    for li, (gl, n) in enumerate(zip(L, tl)):
        if li == 0 or len(gl) < 8 or abs(len(gl) - n) > 1: continue
        hs = np.array([g["h"] for g in gl]); ws = np.array([g["w"] for g in gl])
        mh, mw = np.median(hs[1:-1]), np.median(ws[1:-1])
        hr.append(hs[0] / mh); wr.append(ws[0] / mw); hr2.append(hs[1] / mh); wr2.append(ws[1] / mw); hrl.append(hs[-1] / mh); wrl.append(ws[-1] / mw)
        if len(gl) == n: aligned.append((int(k), li, gl, d["runes"][li]))
def q(a): a = np.array(a); return f"median {np.median(a):.3f}, mean {a.mean():.3f}, 10-90 % {np.percentile(a,10):.2f}-{np.percentile(a,90):.2f}"
print(f"lines used {len(hr)}; aligned exactly {len(aligned)}")
print("height ratio first/rest :", q(hr)); print("height ratio second/rest:", q(hr2)); print("height ratio last/rest  :", q(hrl))
print("width  ratio first/rest :", q(wr)); print("width  ratio second/rest:", q(wr2)); print("width  ratio last/rest  :", q(wrl))
# 2. per-rune width medians from aligned lines, positions >= 1; then first-glyph width vs its rune's median
byrune = defaultdict(list)
for k, li, gl, rs in aligned:
    for g, r in list(zip(gl, rs))[1:]: byrune[r].append(g["w"])
med = {r: np.median(v) for r, v in byrune.items()}; sd = {r: np.std(v) for r, v in byrune.items()}
print("\nrune widths (px) from aligned glyphs at positions >= 1:")
print(", ".join(f"{LET[r]} {med[r]:.0f}±{sd[r]:.0f} (n{len(byrune[r])})" for r in sorted(med)))
dev0, dev1 = [], []
for k, li, gl, rs in aligned:
    r0 = rs[0]; dev0.append((gl[0]["w"] - med[r0]) / max(sd[r0], 1))
    r1 = rs[1]; dev1.append((gl[1]["w"] - med[r1]) / max(sd[r1], 1))
dev0, dev1 = np.array(dev0), np.array(dev1)
print(f"\nfirst-glyph width vs its rune type: mean dev {dev0.mean():+.2f} sd, |dev|>2.5 in {np.mean(np.abs(dev0)>2.5):.3f} of {len(dev0)}")
print(f"second-glyph width vs its rune type: mean dev {dev1.mean():+.2f} sd, |dev|>2.5 in {np.mean(np.abs(dev1)>2.5):.3f}")
# which first glyphs disagree with their rune's width most
bad = sorted([(abs(d), k, li, LET[rs[0]], gl[0]["w"], med[rs[0]]) for d, (k, li, gl, rs) in zip(dev0, aligned)], reverse=True)[:8]
print("largest first-glyph width disagreements (|dev|, chunk, line, rune, width, rune median):", [(round(b[0],1),)+b[1:] for b in bad])
# 3. transcription's line-first rune identities vs measured width class: compare widths of first glyphs grouped by transcribed rune
print("\nfirst-glyph measured widths by transcribed rune (n, median) vs rune median elsewhere:")
grp = defaultdict(list)
for k, li, gl, rs in aligned: grp[rs[0]].append(gl[0]["w"])
print(", ".join(f"{LET[r]} n{len(v)} {np.median(v):.0f}/{med.get(r,float('nan')):.0f}" for r, v in sorted(grp.items(), key=lambda x: -len(x[1]))))
# 4. red glyphs (RGB pages), read against the transcription where the line aligns
print("\nred text (RGB scans), per page, line: runes")
for k, d in sorted(G.items(), key=lambda x: int(x[0])):
    if d["mode"] != "RGB" or int(k) in (65, 67): continue
    L = [l for l in d["lines"] if len(l) >= 4]
    if len(L) == len(d["tlines"]) + 1 and len(L[0]) <= 3: L = L[1:]
    for li, gl in enumerate(L):
        reds = [i for i, g in enumerate(gl) if g["red"] >= 0.5]
        if not reds: continue
        rs = d["runes"][li] if li < len(d["runes"]) else []
        n_ok = (li < len(d["tlines"]) and len(gl) == d["tlines"][li])
        if n_ok: txt = "".join(LET[rs[i]] + ("" if i + 1 in reds or i == reds[-1] else "") for i in reds)
        else:
            # misaligned (drop cap/heading): read the red run by count from the line start if the red glyphs are a prefix
            if reds == list(range(len(reds))): txt = "".join(LET[r] for r in rs[:len(reds) + (d["tlines"][li] - len(gl) if li < len(d["tlines"]) else 0)]) + " (by count, line short by %d)" % ((d["tlines"][li] - len(gl)) if li < len(d["tlines"]) else 0)
            else: txt = "(unaligned)"
        print(f"  chunk {k} img {d['img']:02d} line {li+1}: {len(reds)} red glyphs at {reds[:12]}{'...' if len(reds)>12 else ''} -> {txt}")
