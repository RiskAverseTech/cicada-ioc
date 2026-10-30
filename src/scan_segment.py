"""Glyph segmentation of the Liber Primus scans (2026-10-30): connected components -> lines -> glyphs on the 55 unsolved pages, aligned to the transcription's rune counts per line. Writes results/scan_glyphs.json. Reproduce: SCANS=... .venv/bin/python -I src/scan_segment.py
The scans are not vendored: SCANS=/path/to/liber-primus-complete (default ~/Desktop/cicada-images/liber-primus-complete), 75 JPEGs from
github.com/scream314/cicada3301 assets/2014/liber-primus-complete, SHA-256 in results/scans_sha256.txt; image NN is transcription chunk NN-1.
"""
import os, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
SCANS = os.environ.get("SCANS", os.path.expanduser("~/Desktop/cicada-images/liber-primus-complete"))
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
import numpy as np
from PIL import Image
from scipy import ndimage
from lp import RAW, IDX
IMG = SCANS + "/%02d.jpg"
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
def tlines(k): return [[IDX[ch] for ch in l if ch in IDX] for l in chunks[k].split("/") if any(ch in IDX for ch in l)]

def segment(img):
    im = Image.open(IMG % img); rgb = np.asarray(im.convert("RGB")).astype(int); g = rgb.mean(-1)
    ink = g < 130; red = ((rgb[..., 0] - np.maximum(rgb[..., 1], rgb[..., 2])) > 60) & (rgb[..., 0] > 110)
    ink = ink | red
    lab, n = ndimage.label(ink); sl = ndimage.find_objects(lab)
    comps = []
    for i, s in enumerate(sl):
        y0, y1, x0, x1 = s[0].start, s[0].stop, s[1].start, s[1].stop; h, w = y1 - y0, x1 - x0
        if h < 12 or w < 4: continue                          # dots, specks
        if h > 420 or w > 420: continue                       # illustrations
        if x0 < 420 or x1 > 2000: continue                    # margins (crosses, trees)
        m = lab[s] == i + 1; area = int(m.sum()); r = float(red[s][m].mean())
        comps.append(dict(y0=y0, y1=y1, x0=x0, x1=x1, h=h, w=w, area=area, red=r, yc=(y0 + y1) / 2))
    if not comps: return []
    # body glyph height: mode of heights among medium components
    hs = np.array([c["h"] for c in comps]); body = float(np.median(hs[(hs > 40) & (hs < 200)])) if ((hs > 40) & (hs < 200)).any() else 100
    # line clustering by y-center, using components of body-ish height first
    core = sorted([c for c in comps if 0.5 * body < c["h"] < 1.6 * body], key=lambda c: c["yc"])
    lines = []
    for c in core:
        if lines and abs(c["yc"] - np.mean([d["yc"] for d in lines[-1]])) < 0.5 * body: lines[-1].append(c)
        else: lines.append([c])
    lines = [l for l in lines if len(l) >= 4]
    # attach small components (separators, glyph pieces) and tall drop caps to the nearest line by y-center
    for c in comps:
        if any(c is d for l in lines for d in l): continue
        if not lines: break
        k = int(np.argmin([abs(c["yc"] - np.mean([d["yc"] for d in l])) for l in lines]))
        if abs(c["yc"] - np.mean([d["yc"] for d in lines[k]])) < 1.6 * body: lines[k].append(c)
    out = []
    for l in lines:
        l = sorted(l, key=lambda c: c["x0"]); merged = []
        for c in l:
            if merged and c["x0"] < merged[-1]["x1"] - 3:       # horizontal overlap: same glyph
                m = merged[-1]; m.update(x1=max(m["x1"], c["x1"]), y0=min(m["y0"], c["y0"]), y1=max(m["y1"], c["y1"]), area=m["area"] + c["area"], red=max(m["red"], c["red"]))
                m["h"], m["w"] = m["y1"] - m["y0"], m["x1"] - m["x0"]
            else: merged.append(dict(c))
        glyphs = [c for c in merged if c["h"] >= 0.45 * body]   # drop separators and specks
        out.append(dict(yc=float(np.mean([c["yc"] for c in glyphs])) if glyphs else 0, body=body, glyphs=glyphs))
    return out

res = {}
for img in range(17, 73):
    k = img - 1; tl = tlines(k)
    if not tl: continue
    L = segment(img); mode = Image.open(IMG % img).mode
    res[k] = dict(img=img, mode=mode, tlines=[len(l) for l in tl], runes=tl, lines=[[dict(h=c["h"], w=c["w"], x0=c["x0"], y0=c["y0"], red=round(c["red"], 2)) for c in l["glyphs"]] for l in L], body=L[0]["body"] if L else None)
    counts = [len(l["glyphs"]) for l in L]
    ok = len(counts) == len(tl) and all(a == b for a, b in zip(counts, [len(l) for l in tl]))
    print(f"chunk {k} (img {img:02d}, {mode}): transcription {[len(l) for l in tl]} | image {counts} {'OK' if ok else ''}", flush=True)
json.dump(res, open(RESULTS_DIR / "scan_glyphs.json", "w"))
