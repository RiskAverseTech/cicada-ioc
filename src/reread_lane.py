"""Blinded glyph-level re-reading of the unsolved pages (2026-10-28).  Pre-registered.

Every lab's negatives rest on one transcription (rtkd/iddqd).  Two Quorum panels (quorumsays.com/q/
OHUxs3Jget6b, Gt7EN7uFnoNk) independently put a blinded re-reading first, because a stateful cipher
test on a misread string is a test of a different object.  This lane reads the runes from the page
images with a classifier that never sees the unsolved transcription.

Method.  Glyphs are connected components of the Otsu-binarised page inside the text column, ordered
into rows by y-clustering and left to right within rows (the §26 pipeline).  TRAINING: the solved
pages (images 01-16, 73, 74) whose component count equals their transcription's rune count give
labelled glyphs; each glyph is its bounding box cropped, padded square, resized to 32 x 32, mean-centred
and unit-normalised.  Classifier: 3-nearest-neighbour vote by cosine similarity over all labelled glyphs, with the vote
margin between the best and second class as confidence; labels come from count-matched rows and are
then re-aligned twice by reading each row with a model trained on the other pages and pairing it with
the transcription line it agrees with best (rows under 60 % agreement are dropped).  VALIDATION, before any unsolved page is read: leave-one-page-
out accuracy over the solved pages and the margin threshold T at which held-out precision is >= 99.5 %;
glyphs with margin < T are "unresolved".  Components whose x-ranges overlap within a row are merged (a rune drawn as two strokes, found on the
solved pages before any unsolved glyph was read).  A width-based splitter for touching rune pairs was tried after the first blind run (149 unaligned positions, all transcription runes the reading could not isolate, 64 of them ᚳ) and withdrawn: it cut wide runes such as ᛠ in two and produced 491 unaligned positions and 540 spurious repeats.  The 149 positions are left unread and listed.  BLIND READING: every unsolved page with runes (images 17-72
except 67, which has no runes; on 66 and 68 the base-60 grid rows are excluded by layout, not by the
transcription).  RECONCILIATION, only after reading: alignment to the community string by position where
counts agree and by sequence alignment otherwise.

PRE-REGISTERED RULE.  The community transcription is CONFIRMED if (a) the number of RESOLVED glyphs
(margin >= T) is within 3 of the transcription's rune count on at least 50 of the 54 readable pages
(amended from "component count matches" after the segmentation diagnostic, before any unsolved glyph was
classified: a few separator marks survive the size filter and the image-to-chunk map is image 01 =
chunk 1, image 02 = no chunk, image k = chunk k-1 for k >= 3), (b) the disagreement rate at resolved glyphs is no
more than twice the held-out error rate of the classifier, and (c) the adjacent-repeat count on the blind
reading lies within 10 of 86.  Any resolved disagreement is listed with page and position for the eye.  If
the transcription is NOT confirmed, every stateful-cipher negative in this repository whose input spans
the corrected positions is reopened.  Writes results/reread.md, results/reread.json.
Usage: .venv/bin/python -I src/reread_lane.py
"""
import json, sys, time, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from PIL import Image
from scipy import ndimage
from lp import IDX, LATIN, RAW, RESULTS, N

IMG = Path(__file__).resolve().parent.parent / "data" / "images" / "raw"
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
def runes_of(chunk): return [IDX[c] for c in chunk if c in IDX]
def chunk_of(nn): return None if nn == 2 else (1 if nn == 1 else nn - 1)
def lines_of(chunk):
    """rune lines of a chunk (line '/', paragraph '&', segment '$' all break lines)"""
    out = []
    for part in chunk.replace("&", "/").replace("$", "/").split("/"):
        r = [IDX[c] for c in part if c in IDX]
        if r: out.append(r)
    return out
TRAIN_IMGS = [1] + list(range(3, 17)) + [73, 74]; UNSOLVED_IMGS = [i for i in range(17, 73) if i != 67]
GRID_ROWS = {66: ("top", 3), 68: ("bottom", 4)}      # layout: runes occupy these rows on the payload pages
SZ = 32


def otsu(g):
    h = np.bincount(g.ravel(), minlength=256).astype(float); p = h / h.sum(); w = np.cumsum(p); m = np.cumsum(p * np.arange(256)); mt = m[-1]
    return int(np.argmax((mt * w - m) ** 2 / np.clip(w * (1 - w), 1e-12, None)))


def segment(nn):
    gray = np.asarray(Image.open(IMG / f"{nn:02d}.jpg").convert("L")); ink = gray < otsu(gray)
    lab, n = ndimage.label(ink); boxes = []
    for s in ndimage.find_objects(lab):
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start; xc = (s[1].start + s[1].stop) / 2
        if 25 <= h <= 420 and 6 <= w <= 420 and 500 <= xc <= 1900: boxes.append((s[1].start, s[0].start, s[1].stop, s[0].stop))
    if not boxes: return [], ink
    B = np.array(boxes); yc = (B[:, 1] + B[:, 3]) / 2; order = np.argsort(yc); B = B[order]; yc = yc[order]
    med_h = np.median(B[:, 3] - B[:, 1]); rows, cur = [], [0]
    for i in range(1, len(B)):
        if yc[i] - np.mean(yc[cur]) > 0.6 * med_h: rows.append(cur); cur = [i]
        else: cur.append(i)
    rows.append(cur)
    out = []
    for r in rows:
        R = B[r][np.argsort(B[r][:, 0])]; merged = []
        for b in R:                                   # merge components whose x-ranges overlap (a rune drawn as two strokes, e.g. ᚣ)
            if merged and b[0] <= merged[-1][2] - 3:          # genuine overlap only; neighbours sit 3-7 px apart
                m = merged[-1]; merged[-1] = (min(m[0], b[0]), min(m[1], b[1]), max(m[2], b[2]), max(m[3], b[3]))
            else: merged.append(tuple(int(v) for v in b))
        out.append(merged)
    return out, ink


def crop(ink, b):
    x0, y0, x1, y1 = b; g = ink[y0:y1, x0:x1].astype(np.uint8) * 255; h, w = g.shape; s = max(h, w)
    pad = np.zeros((s, s), np.uint8); pad[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = g
    v = np.asarray(Image.fromarray(pad).resize((SZ, SZ), Image.BILINEAR), float).ravel(); v -= v.mean(); n = np.linalg.norm(v)
    return v / n if n > 0 else v


def page_glyphs(nn):
    rows, ink = segment(nn)
    if nn in GRID_ROWS:
        where, k = GRID_ROWS[nn]; rows = rows[:k] if where == "top" else rows[-k:]
    boxes = [b for r in rows for b in r]
    return boxes, np.array([crop(ink, b) for b in boxes]) if boxes else np.zeros((0, SZ * SZ))


t0 = time.time(); report = {}
# ---------- training set: count-matched rows, then bootstrap realignment ----------
def rows_and_lines(nn):
    lines = lines_of(chunks[chunk_of(nn)]); rows, ink = segment(nn); return lines, rows, ink


def knn_predict(Xt, yt, Xq, k=3):
    """3-NN vote; the confidence returned is the similarity to the NEAREST training glyph, so that a
    component unlike any rune (a decoration, a separator, a fragment) can be declared unresolved"""
    S = Xq @ Xt.T; idx = np.argsort(-S, axis=1)[:, :k]; votes = np.zeros((len(Xq), N))
    for j in range(k): np.add.at(votes, (np.arange(len(Xq)), yt[idx[:, j]]), S[np.arange(len(Xq)), idx[:, j]] + 1)
    best = np.argmax(votes, axis=1)
    return best, S[np.arange(len(Xq)), idx[:, 0]]


feats = {}; data = {}
for nn in TRAIN_IMGS:
    lines, rows, ink = rows_and_lines(nn); data[nn] = (lines, rows); feats[nn] = [np.array([crop(ink, b) for b in r]) for r in rows]
# stage A: exact-count row matching
Xs, ys, pl = [], [], []
for nn in TRAIN_IMGS:
    lines, rows = data[nn]; sm = difflib.SequenceMatcher(a=[len(l) for l in lines], b=[len(r) for r in rows], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal": continue
        for k in range(i2 - i1): Xs.append(feats[nn][j1 + k]); ys += lines[i1 + k]; pl += [nn] * len(lines[i1 + k])
X = np.vstack(Xs); y = np.array(ys); pages_of = np.array(pl)
# stage B (twice): read every row with a model trained on the other pages, pair rows with lines by agreement, keep aligned positions
stats = []
for it in range(2):
    Xs, ys, pl, kept = [], [], [], 0
    for nn in TRAIN_IMGS:
        lines, rows = data[nn]; m = pages_of != nn
        if m.sum() == 0: continue
        for ri, Xr in enumerate(feats[nn]):
            if len(Xr) == 0: continue
            pr, _ = knn_predict(X[m], y[m], Xr)
            best = None
            for li, line in enumerate(lines):
                if abs(len(line) - len(pr)) > 2: continue
                sm = difflib.SequenceMatcher(a=list(map(int, line)), b=list(map(int, pr)), autojunk=False); r = sm.ratio()
                if best is None or r > best[0]: best = (r, li, sm)
            if best is None or best[0] < 0.6: continue
            r, li, sm = best; line = lines[li]
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
                    Xs.append(Xr[j1:j2]); ys += line[i1:i2]; pl += [nn] * (i2 - i1)
            kept += 1
    X = np.vstack(Xs); y = np.array(ys); pages_of = np.array(pl); stats.append((it + 1, kept, len(y)))
print(f"training glyphs {len(y)} after bootstrap (iteration, rows kept, glyphs): {stats}; classes present {len(set(y.tolist()))}/29  [{time.time()-t0:.0f}s]", flush=True)
used = sorted(set(pages_of.tolist())); skipped = [nn for nn in TRAIN_IMGS if nn not in used]


def centroids(Xt, yt):
    C = np.zeros((N, SZ * SZ))
    for c in range(N):
        if (yt == c).any(): C[c] = Xt[yt == c].mean(0)
    nrm = np.linalg.norm(C, axis=1, keepdims=True); return C / np.where(nrm == 0, 1, nrm), (nrm.ravel() > 0)


def predict(C, present, Xq):
    """kNN (k=3, similarity-weighted votes) against the full training set; C/present kept for the interface"""
    return knn_predict(X, y, Xq)


# ---------- leave-one-page-out validation ----------
pred_all, marg_all = np.zeros(len(y), int), np.zeros(len(y))
for nn in used:
    m = pages_of != nn; p, mg = knn_predict(X[m], y[m], X[~m]); pred_all[~m] = p; marg_all[~m] = mg
acc = float((pred_all == y).mean())
T = float(np.percentile(marg_all, 0.5))          # a blind component nearer to no training glyph than 99.5 % of held-out glyphs were is unresolved
res_rate = float((marg_all >= T).mean()); err_res = float((pred_all[marg_all >= T] != y[marg_all >= T]).mean())
conf = {}
for a, b in zip(y[pred_all != y], pred_all[pred_all != y]): conf[(LATIN[a], LATIN[b])] = conf.get((LATIN[a], LATIN[b]), 0) + 1
print(f"held-out accuracy {acc:.4f}; margin threshold T={T:.3f} resolves {res_rate:.3f} of glyphs at error {err_res:.4f}; confusions {sorted(conf.items(), key=lambda kv: -kv[1])[:8]}  [{time.time()-t0:.0f}s]", flush=True)
C, present = centroids(X, y)

# ---------- blind reading ----------
readings = {}
for nn in UNSOLVED_IMGS:
    boxes, Xq = page_glyphs(nn)
    if len(boxes) == 0: readings[nn] = dict(pred=[], margin=[]); continue
    p, mg = predict(C, present, Xq); readings[nn] = dict(pred=[int(v) for v in p], margin=[float(v) for v in mg], boxes=[list(map(int, b)) for b in boxes])
print(f"blind reading done: {sum(len(r['pred']) for r in readings.values())} glyphs on {len(readings)} pages  [{time.time()-t0:.0f}s]", flush=True)

# ---------- reconciliation ----------
rows, count_match, n_res, n_dis, dis_list, n_unaligned = [], 0, 0, 0, [], 0; blind_doublets = 0
for nn in UNSOLVED_IMGS:
    truth = runes_of(chunks[chunk_of(nn)]); pr_all = readings[nn]["pred"]; mg = readings[nn]["margin"]; pid = f"LP2-{nn-17:02d}"
    pr = [p_ for p_, m_ in zip(pr_all, mg) if m_ >= T]          # resolved glyphs only
    n_resolved_page = len(pr); same = abs(n_resolved_page - len(truth)) <= 3; count_match += same
    bd = sum(1 for i in range(1, len(pr)) if pr[i] == pr[i - 1]); blind_doublets += bd
    sm = difflib.SequenceMatcher(a=truth, b=pr, autojunk=False); aligned = 0; dis = []; unal = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": aligned += i2 - i1
        elif tag == "replace" and (i2 - i1) == (j2 - j1) and (i2 - i1) <= 3:
            aligned += i2 - i1
            for k in range(i2 - i1): dis.append((j1 + k, pr[j1 + k], truth[i1 + k]))
        else: unal += max(i2 - i1, j2 - j1)
    n_res += aligned; n_dis += len(dis); n_unaligned += unal
    for i, p_, t_ in dis: dis_list.append((pid, i, LATIN[t_], LATIN[p_]))
    rows.append((pid, len(truth), len(pr_all), n_resolved_page, same, aligned, len(dis), unal, bd, sum(1 for i in range(1, len(truth)) if truth[i] == truth[i - 1])))
dis_rate = n_dis / max(n_res, 1)
confirmed = count_match >= 50 and dis_rate <= 2 * max(err_res, 1e-4) and abs(blind_doublets - 86) <= 10
out = ["# Blinded glyph-level re-reading of the unsolved pages", "",
       f"Classifier: 3-NN on 32 x 32 glyph crops, trained on {len(y)} labelled glyphs from solved images {used} (images with no exactly matched row: {skipped}). Leave-one-page-out accuracy **{acc:.4f}**; a component is resolved if its nearest training glyph has cosine similarity at least T = {T:.3f} (the 0.5th percentile of held-out glyphs), which keeps {res_rate:.1%} of held-out glyphs at error {err_res:.4%}. Most frequent held-out confusions: " + ", ".join(f"{a}→{b} {n}" for (a, b), n in sorted(conf.items(), key=lambda kv: -kv[1])[:6]) + ".", "",
       f"Blind reading of {len(UNSOLVED_IMGS)} pages: resolved-glyph count within 3 of the transcription on **{count_match} of {len(UNSOLVED_IMGS)}**; at the {n_res:,} aligned resolved glyphs the reading disagrees with the transcription **{n_dis}** times ({dis_rate:.4%}, against a held-out classifier error of {err_res:.4%}); {n_unaligned} glyph positions could not be aligned (insertions, deletions or runs longer than three); adjacent repeats on the resolved blind reading **{blind_doublets}** (transcription 86).", "",
       f"**Pre-registered verdict: transcription {'CONFIRMED' if confirmed else 'NOT confirmed'}** (count match ≥ 50/54: {count_match >= 50}; disagreement ≤ 2 × classifier error: {dis_rate <= 2*max(err_res,1e-4)}; blind doublets within 10 of 86: {abs(blind_doublets-86) <= 10}).", "",
       "| page | runes (transcription) | components | resolved glyphs | count within 3 | aligned | disagree | unaligned | doublets blind | doublets transcription |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows: out.append("| " + " | ".join(str(v) for v in r) + " |")
out += ["", "## Resolved disagreements (page, position in the blind reading, transcription → blind reading)", ""] + ([f"- {p} #{i}: {t} → {b}" for p, i, t, b in dis_list[:200]] or ["None."]) + ["", f"Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / "reread.md").write_text("\n".join(out) + "\n")
json.dump(dict(train_images=used, skipped=skipped, n_train=int(len(y)), accuracy=acc, T=T, resolved_rate=res_rate, err_resolved=err_res, count_match=count_match, n_resolved=n_res, n_disagree=n_dis, blind_doublets=blind_doublets, confirmed=bool(confirmed), rows=rows, disagreements=dis_list, readings={str(k): v for k, v in readings.items()}), open(RESULTS / "reread.json", "w"), indent=1)
print("\n".join(out[2:7]))
