"""Lag-1 affine scan inside words, and the echo sites laid out for the eye (2026-10-28).
(1) The 812 affine maps c_i = a c_(i-1) + b inside words, identity excluded (that cell is the repeat deficit): is
    24 - 2c or any other map elevated at lag 1?  Null: 999 within-page shuffles with word structure fixed.
(2) Every lag-5 S..S site and every lag-6 T site, with its word in Latin transliteration, the page, the word
    position and the rune six/five back.  Writes results/echo_sites.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
rng = np.random.default_rng(11)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§'); S = LATIN.index("S")
def parse(s):
    runes, wid, pos = [], [], []; w = 0; pending = False; k = 0
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False; k = 0
            runes.append(IDX[ch]); wid.append(w); pos.append(k); k += 1
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int), np.array(pos, int)
U = [(k - 16, *parse(chunks[k])) for k in range(16, 72)]; U = [u for u in U if len(u[1])]
A = np.arange(1, N)[:, None]; B = np.arange(N)[None, :]; xs = np.arange(N)
tgt = (A[:, :, None] * xs[None, None, :] + B[:, :, None]) % N
def hits(x, y):
    H = np.zeros((N, N)); np.add.at(H, (x, y), 1); return H[xs[None, None, :], tgt].sum(-1)
ok = []; off = 0
allc = np.concatenate([c for _, c, _, _ in U]); allw = np.concatenate([w for _, _, w, _ in U])
for _, c, w, _ in U:
    i = np.arange(1, len(c)); i = i[w[i] == w[i - 1]]; ok.append(i + off); off += len(c)
ok = np.concatenate(ok); x, y = allc[ok - 1], allc[ok]
h = hits(x, y); h_noid = h.copy(); h_noid[0, 0] = -1
n = len(ok); e = n / N; sd = np.sqrt(n / N * (1 - 1 / N))
best = np.unravel_index(h_noid.argmax(), h.shape)
perm = np.empty(999)
for r in range(999):
    pc = np.concatenate([rng.permutation(c) for _, c, _, _ in U]); hp = hits(pc[ok - 1], pc[ok]); hp[0, 0] = -1; perm[r] = hp.max()
out = ["# Lag-1 affine maps inside words, and the echo sites", "",
       f"## (1) Lag 1: {n:,} within-word adjacent pairs, {e:.1f} ± {sd:.1f} hits expected per map", "",
       f"- Identity (the repeat deficit): {int(h[0,0])}.", f"- 24 − 2c (the lag-6 map, a = 27, b = 24): {int(h[26,24])} (z {(h[26,24]-e)/sd:+.2f}).",
       f"- Best of the other 811 maps: a = {best[0]+1}, b = {best[1]}, {int(h_noid.max())} hits (z {(h_noid.max()-e)/sd:+.2f}); null maximum over 811 maps {perm.mean():.1f} ± {perm.std():.1f}, p = {(np.sum(perm >= h_noid.max()) + 1) / 1000:.3f}.", ""]
# the top 5 maps at lag 1
order = np.argsort(-h_noid.ravel())[:5]
out += ["| a | b | hits | z |", "|---|---|---|---|"] + [f"| {i // N + 1} | {i % N} | {int(h_noid.ravel()[i])} | {(h_noid.ravel()[i]-e)/sd:+.2f} |" for i in order] + [""]
def word_of(c, w, j):
    m = w == w[j]; return "".join(LATIN[v] for v in c[m]), int(m.sum())
out += ["## (2) The lag-5 S..S sites", "", "| page | word (Latin) | length | position of first S | runes between |", "|---|---|---|---|---|"]
for pid, c, w, p in U:
    for j in range(5, len(c)):
        if w[j] == w[j - 5] and c[j] == c[j - 5] == S:
            wd, L = word_of(c, w, j); out.append(f"| LP2-{pid:02d} | {wd} | {L} | {p[j-5]} | {''.join(LATIN[v] for v in c[j-4:j])} |")
out += ["", "## (3) The lag-6 sites c_i = 24 − 2 c_(i−6)", "", "| page | word (Latin) | length | position of first rune | first rune | sixth rune after it | runes between |", "|---|---|---|---|---|---|---|"]
for pid, c, w, p in U:
    for j in range(6, len(c)):
        if w[j] == w[j - 6] and c[j] == (24 - 2 * c[j - 6]) % N:
            wd, L = word_of(c, w, j); out.append(f"| LP2-{pid:02d} | {wd} | {L} | {p[j-6]} | {LATIN[c[j-6]]} | {LATIN[c[j]]} | {''.join(LATIN[v] for v in c[j-5:j])} |")
(RESULTS / "echo_sites.md").write_text("\n".join(out) + "\n"); print("\n".join(out[:14])); print(f"... {len(out)} lines written")
