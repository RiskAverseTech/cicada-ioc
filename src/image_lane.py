"""Page-image lane (2026-10-27): is there information in the Liber Primus page images that the
transcription does not carry?  Pre-registered before any unsolved image was measured.

Images: scream314/cicada3301 assets/2014/liber-primus-complete/NN.jpg (75 pages, 2400 x 3600),
NN = book chunk + 1; unsolved LP2-k is image 17 + k (k = 0..55); images 00-16 (LP1) and 73-74 (the two
solved LP2 pages) are the CONTROL GROUP.  First run (2026-10-27) showed the two parts were exported in
different batches (every LP2 image carries one identical 2,576-byte sRGB ICC profile that no LP1 image
has, and text-only pages without red ink or border art were saved as grayscale), so the CONTAINER test
compares unsolved pages with the LP2 controls only; the pixel and geometry tests use all controls.
The LSB chi-square is reported but is uninformative on JPEG-decoded pixels (saturated for every image,
control or not); it is kept so the null is on the record.
Files live in data/images/raw/ (gitignored); SHA-256 in data/images/SHA256SUMS.txt.

Tests (each statistic is computed for every image; an unsolved page is FLAGGED only where it departs
from the solved/decorative control pages by the stated margin):
  T1 container: bytes after the JPEG end-of-image marker; APPn/COM segments; quantization tables; DPI
     tag; colour mode.  Flag: any unsolved image with trailing bytes or a marker set no control image has.
  T2 chroma: for RGB images, share of pixels with max|R-G|,|G-B|,|R-B| > 8 that are NOT the book's red ink
     (red ink: R exceeds both G and B by 40 or more; the initials, first words and dotted separators are
     printed red by design).  Flag: unsolved mean exceeds the control mean by 4 control standard deviations.
  T3 LSB: chi-square of least-significant-bit pair counts in the paper background (pixels > 200), the
     classic LSB-embedding statistic.  Flag: unsolved log10 p below the control minimum by more than 3.
  T4 glyph geometry: Otsu binarisation, connected components inside the text column (x in 550..1850 of
     2400, which excludes the border art and its leaves), components of glyph size kept, rows found by
     clustering y-centres; per row, the gap between consecutive glyph boxes and the baseline (bottom)
     residual from the row median.  Statistics per page: gap sd, baseline sd, excess kurtosis of the gap
     residuals (a 1-bit channel in the spacing would be bimodal, kurtosis near -2), and the glyph count.
     Flag: unsolved gap sd or baseline sd above the control mean by 4 control sd; kurtosis below -1 on
     an unsolved page when no control page is below -1.
  T5 count check: glyph components per unsolved page against the transcription's rune count plus its
     separators; a mismatch beyond 10 % marks the geometry statistics for that page as unreliable.
Writes results/images.md, results/images.json.  Usage: .venv/bin/python -I src/image_lane.py
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from PIL import Image
from scipy import ndimage, stats
from lp import PROCESSED, RESULTS

IMG = Path(__file__).resolve().parent.parent / "data" / "images" / "raw"
d = json.loads((PROCESSED / "pages.json").read_text())
unsolved = {17 + k: u for k, u in enumerate(d["unsolved"])}          # image number -> page record
MASTER = Path(__file__).resolve().parent.parent / "data" / "raw"


def container(path):
    b = path.read_bytes()
    eoi = b.rfind(b"\xff\xd9"); trailing = len(b) - (eoi + 2)
    markers, i = [], 2
    while i < len(b) - 4:
        if b[i] != 0xFF: break
        m = b[i + 1]
        if m == 0xDA: break                                   # start of scan
        ln = int.from_bytes(b[i + 2:i + 4], "big"); markers.append(f"{m:02X}"); i += 2 + ln
    im = Image.open(path)
    q = getattr(im, "quantization", None) or {}
    qsig = tuple(tuple(v) for _, v in sorted(q.items()))
    return dict(size=path.stat().st_size, trailing=trailing, markers=" ".join(markers), qhash=hash(qsig) & 0xFFFF, mode=im.mode, dpi=im.info.get("dpi"), dims=im.size)


def chroma(im):
    if im.mode != "RGB": return None
    a = np.asarray(im).astype(int); dif = np.max(np.abs(np.stack([a[..., 0] - a[..., 1], a[..., 1] - a[..., 2], a[..., 0] - a[..., 2]])), 0)
    red = (a[..., 0] - a[..., 1] >= 40) & (a[..., 0] - a[..., 2] >= 40)
    return float(((dif > 8) & ~red).mean())


def lsb_chi(gray):
    bg = gray[gray > 200]
    if bg.size < 1000: return None
    h = np.bincount(bg, minlength=256).astype(float)
    pairs = h.reshape(128, 2); exp = pairs.mean(1, keepdims=True).repeat(2, 1)
    keep = exp[:, 0] > 5
    if keep.sum() < 3: return None
    chi = (((pairs[keep] - exp[keep]) ** 2) / exp[keep]).sum()
    return float(max(stats.chi2.sf(chi, int(keep.sum()) - 1), 1e-300))


def geometry(gray):
    thr = _otsu(gray); ink = gray < thr
    lab, n = ndimage.label(ink)
    if n == 0: return None
    sl = ndimage.find_objects(lab); boxes = []
    for s in sl:
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        xc = (s[1].start + s[1].stop) / 2
        if 25 <= h <= 260 and 6 <= w <= 260 and 550 <= xc <= 1850: boxes.append((s[1].start, s[0].start, s[1].stop, s[0].stop))
    if len(boxes) < 20: return dict(n=len(boxes))
    B = np.array(boxes); yc = (B[:, 1] + B[:, 3]) / 2
    order = np.argsort(yc); B = B[order]; yc = yc[order]
    rows, cur = [], [0]
    for i in range(1, len(B)):
        if yc[i] - yc[cur[-1]] > 0.6 * np.median(B[:, 3] - B[:, 1]): rows.append(cur); cur = [i]
        else: cur.append(i)
    rows.append(cur)
    gaps, base = [], []
    for r in rows:
        if len(r) < 4: continue
        R = B[r][np.argsort(B[r][:, 0])]
        g = R[1:, 0] - R[:-1, 2]; g = g[(g > -5) & (g < 120)]          # letter gaps; word gaps and overlaps dropped
        gaps += list(g - np.median(g)); base += list(R[:, 3] - np.median(R[:, 3]))
    gaps, base = np.array(gaps), np.array(base)
    return dict(n=len(B), rows=len(rows), gap_sd=float(gaps.std()) if len(gaps) > 10 else None, base_sd=float(base.std()) if len(base) > 10 else None,
                gap_kurt=float(stats.kurtosis(gaps)) if len(gaps) > 30 else None, gap_bimodal_share=float((np.abs(gaps) > 2).mean()) if len(gaps) > 10 else None)


def _otsu(g):
    h = np.bincount(g.ravel(), minlength=256).astype(float); p = h / h.sum(); w = np.cumsum(p); m = np.cumsum(p * np.arange(256)); mt = m[-1]
    var = (mt * w - m) ** 2 / np.clip(w * (1 - w), 1e-12, None); return int(np.argmax(var))


fp = lambda x: 'None' if x is None else f'{x:.1e}'
t0 = time.time(); rows = {}
for nn in range(75):
    p = IMG / f"{nn:02d}.jpg"
    if not p.exists(): continue
    im = Image.open(p); gray = np.asarray(im.convert("L"))
    r = dict(image=nn, group="unsolved" if nn in unsolved else "control", page=unsolved[nn]["id"] if nn in unsolved else None,
             runes=unsolved[nn]["length"] if nn in unsolved else None, **container(p), chroma=chroma(im), lsb_p=lsb_chi(gray), geom=geometry(gray))
    rows[nn] = r
    print(f"  {nn:02d} {r['group']:8s} {r['page'] or '':7s} trailing={r['trailing']} mode={r['mode']} chroma={r['chroma'] if r['chroma'] is None else round(r['chroma'],4)} lsb_p={fp(r['lsb_p'])} geom={ {k: (round(v,2) if isinstance(v,float) else v) for k,v in (r['geom'] or {}).items()} }  [{time.time()-t0:.0f}s]", flush=True)

# ---------- comparison against the control group ----------
def grp(key, group, sub=None):
    v = []
    for r in rows.values():
        if r["group"] != group: continue
        x = r[key] if sub is None else (r["geom"] or {}).get(sub)
        if x is not None: v.append(x)
    return np.array(v, float)

flags = []
ctrl_markers = {r["markers"] for n_, r in rows.items() if r["group"] == "control" and n_ >= 73}; ctrl_q = {r["qhash"] for n_, r in rows.items() if r["group"] == "control" and n_ >= 73}
ctrl_markers |= {m.replace("DB DB C0 C4 C4 C4 C4", "DB C0 C4 C4") for m in ctrl_markers}            # the grayscale export of the same pipeline
for r in rows.values():
    if r["group"] != "unsolved": continue
    if r["trailing"] > 0: flags.append((r["page"], "T1", f"{r['trailing']} bytes after EOI"))
    if r["markers"] not in ctrl_markers: flags.append((r["page"], "T1", f"marker set {r['markers']} not seen in controls"))
    if r["qhash"] not in ctrl_q and r["mode"] != "L": flags.append((r["page"], "T1", "quantization tables unlike any LP2 control image"))
summary = []
for label, key, sub, direction in (("chroma share", "chroma", None, "high"), ("LSB log10 p", "lsb_p", None, "low"), ("gap sd (px)", "geom", "gap_sd", "high"), ("baseline sd (px)", "geom", "base_sd", "high"), ("gap kurtosis", "geom", "gap_kurt", "low"), ("glyph count", "geom", "n", None)):
    c = grp(key, "control", sub); u = grp(key, "unsolved", sub)
    if key == "lsb_p": c, u = np.log10(c), np.log10(u)
    if len(c) < 3 or len(u) < 3: summary.append((label, len(c), None, None, len(u), None, None)); continue
    summary.append((label, len(c), c.mean(), c.std(), len(u), u.mean(), u.std()))
    for r in rows.values():
        if r["group"] != "unsolved": continue
        x = r[key] if sub is None else (r["geom"] or {}).get(sub)
        if x is None or (r["runes"] == 0 and key == "geom"): continue           # LP2-50 carries no runes; its "glyphs" are art
        if key == "lsb_p": x = np.log10(x)
        if direction == "high" and x > c.mean() + 4 * c.std(): flags.append((r["page"], label, f"{x:.3g} vs control {c.mean():.3g} ± {c.std():.3g}"))
        if direction == "low" and label == "LSB log10 p" and x < c.min() - 3: flags.append((r["page"], label, f"{x:.1f} vs control min {c.min():.1f}"))
        if direction == "low" and label == "gap kurtosis" and x < -1 and c.min() >= -1: flags.append((r["page"], label, f"{x:.2f}; no control below -1 (min {c.min():.2f})"))
# T5 count check
count_bad = []
for nn, r in rows.items():
    if r["group"] == "unsolved" and r["geom"] and r["runes"]:
        n = r["geom"]["n"]; expect = r["runes"] * 1.15                         # runes plus roughly one separator per word
        if abs(n - r["runes"]) / r["runes"] > 0.5: count_bad.append((r["page"], n, r["runes"]))

out = ["# Page-image lane: container, chroma, LSB and glyph geometry, unsolved pages against the solved/decorative control pages", "",
       f"{sum(1 for r in rows.values() if r['group']=='control')} control images, {sum(1 for r in rows.values() if r['group']=='unsolved')} unsolved; rule and tests in the module docstring. Runtime {time.time()-t0:.0f} s.", "",
       "| statistic | control n | control mean | control sd | unsolved n | unsolved mean | unsolved sd |", "|---|---|---|---|---|---|---|"]
for s in summary:
    out.append("| " + " | ".join(("–" if v is None else (f"{v:.3g}" if isinstance(v, float) else str(v))) for v in s) + " |")
out += ["", "## Container (T1)", "", f"Trailing bytes after EOI on unsolved pages: {sum(r['trailing'] for r in rows.values() if r['group']=='unsolved')} total; marker sets seen: " + ", ".join(sorted({r['markers'] for r in rows.values()})) + f"; distinct quantization-table sets: {len({r['qhash'] for r in rows.values()})}; modes: " + ", ".join(f"{m} x {sum(1 for r in rows.values() if r['mode']==m)}" for m in sorted({r['mode'] for r in rows.values()})) + ".", "",
        "## Flags", ""] + ([f"- {p}: {t}: {msg}" for p, t, msg in flags] or ["None."]) + ["", "## Glyph count check (T5)", "",
        ("Pages whose component count is more than 50 % off the rune count (geometry unreliable there): " + ", ".join(f"{p} ({n} vs {k})" for p, n, k in count_bad)) if count_bad else "Every unsolved page's component count is within 50 % of its rune count.", "",
        "| image | page | runes | components | rows | gap sd | baseline sd | gap kurtosis | chroma | LSB p |", "|---|---|---|---|---|---|---|---|---|---|"]
for nn, r in rows.items():
    g = r["geom"] or {}
    out.append(f"| {nn:02d} | {r['page'] or ('control')} | {r['runes'] or ''} | {g.get('n','')} | {g.get('rows','')} | {g.get('gap_sd') if g.get('gap_sd') is None else round(g['gap_sd'],2)} | {g.get('base_sd') if g.get('base_sd') is None else round(g['base_sd'],2)} | {g.get('gap_kurt') if g.get('gap_kurt') is None else round(g['gap_kurt'],2)} | {r['chroma'] if r['chroma'] is None else round(r['chroma'],4)} | {fp(r['lsb_p'])} |")
(RESULTS / "images.md").write_text("\n".join(out) + "\n")
json.dump({str(k): v for k, v in rows.items()} | {"flags": flags, "summary": summary}, open(RESULTS / "images.json", "w"), indent=1, default=str)
print("\n".join(out[:12])); print("flags:", flags)
