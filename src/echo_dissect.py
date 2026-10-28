"""Dissection of the two within-word echoes (2026-10-28): lag-5 equality c_i = c_(i-5) and the lag-6 affine
relation c_i = 24 - 2 c_(i-6).  Which runes carry them, where in the word they sit, how long the words are,
and whether the two sets of sites overlap each other or the 86 adjacent repeats.  Null for each table: the
same within-page shuffles with word structure fixed (999).  Writes results/echo_dissect.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN
rng = np.random.default_rng(5)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid, pos = [], [], []; w = 0; pending = False; k = 0
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False; k = 0
            runes.append(IDX[ch]); wid.append(w); pos.append(k); k += 1
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int), np.array(pos, int)
U = [parse(chunks[k]) for k in range(16, 72) if len(parse(chunks[k])[0])]
allc = np.concatenate([c for c, _, _ in U]); allw = np.concatenate([w for _, w, _ in U]); allp = np.concatenate([p for _, _, p in U])
page = np.concatenate([np.full(len(c), i) for i, (c, _, _) in enumerate(U)])
wlen = np.zeros(len(allc), int)
for i in range(len(U)):
    m = page == i; cnt = np.bincount(allw[m]); wlen[m] = cnt[allw[m]]
def sites(c, lag, kind):
    ok = np.arange(lag, len(c)); ok = ok[(allw[ok] == allw[ok - lag]) & (page[ok] == page[ok - lag])]
    x, y = c[ok - lag], c[ok]
    hit = (y == x) if kind == "id" else (y == (27 * x + 24) % N)
    return ok, hit
out = ["# Dissection of the two within-word echoes", ""]
for lag, kind, name in ((5, "id", "lag-5 equality c_i = c_(i-5)"), (6, "aff", "lag-6 relation c_i = 24 − 2 c_(i-6)")):
    ok, hit = sites(allc, lag, kind); H = ok[hit]; n_h = len(H)
    out += [f"## {name}: {n_h} sites among {len(ok):,} within-word pairs", ""]
    # rune identity of the FIRST rune (x) at hit sites vs all pairs
    x_all = allc[ok - lag]; x_hit = allc[H - lag]
    share = np.bincount(x_all, minlength=N) / len(ok); obs = np.bincount(x_hit, minlength=N)
    # null distribution of the per-rune maximum excess z
    zs = (obs - n_h * share) / np.sqrt(n_h * share * (1 - share))
    top = np.argsort(-zs)[:5]
    out += ["First rune of the pair (the one echoed), top five by excess over its share of all pairs:", "", "| rune | sites | expected | z |", "|---|---|---|---|"]
    for r in top: out.append(f"| {LATIN[r]} | {obs[r]} | {n_h*share[r]:.1f} | {zs[r]:+.2f} |")
    out += ["", f"Chi-square of the 29 first-rune counts against the shares: p = {stats.chisquare(obs, n_h*share).pvalue:.3f}.", ""]
    # position in word of the first rune, and word length
    p_all = allp[ok - lag]; p_hit = allp[H - lag]
    L_all = wlen[ok]; L_hit = wlen[H]
    out += ["Position of the first rune in its word and the word length, hit sites against all within-word pairs at this lag:", "", "| | position 0 | 1 | 2 | 3+ | word length = lag+1 (pair spans the whole word) | longer |", "|---|---|---|---|---|---|---|"]
    def row(lbl, p, L):
        return f"| {lbl} | " + " | ".join(str(int(v)) for v in (np.sum(p == 0), np.sum(p == 1), np.sum(p == 2), np.sum(p >= 3))) + f" | {int(np.sum(L == lag + 1))} | {int(np.sum(L > lag + 1))} |"
    out += [row("hit sites", p_hit, L_hit), row(f"all pairs (×{n_h/len(ok):.3f})", p_all * 0 + p_all, L_all)]
    exp0 = n_h * np.mean(p_all == 0); out += ["", f"Expected hits at position 0 if hits fell like all pairs: {exp0:.1f}; observed {int(np.sum(p_hit == 0))} (binomial p = {stats.binomtest(int(np.sum(p_hit == 0)), n_h, np.mean(p_all == 0)).pvalue:.3f}). Expected whole-word spans: {n_h*np.mean(L_all == lag + 1):.1f}; observed {int(np.sum(L_hit == lag + 1))}.", ""]
# overlaps
ok5, h5 = sites(allc, 5, "id"); ok6, h6 = sites(allc, 6, "aff")
S5 = set(ok5[h5].tolist()) | set((ok5[h5] - 5).tolist()); S6 = set(ok6[h6].tolist()) | set((ok6[h6] - 6).tolist())
dbl = np.where((allc[1:] == allc[:-1]) & (page[1:] == page[:-1]))[0]; D = set(dbl.tolist()) | set((dbl + 1).tolist())
W5 = {(page[i], allw[i]) for i in ok5[h5]}; W6 = {(page[i], allw[i]) for i in ok6[h6]}; WD = {(page[i], allw[i]) for i in dbl}
out += ["## Overlap of the site sets", "", f"- Runes involved: lag-5 {len(S5)}, lag-6 {len(S6)}, adjacent repeats {len(D)}; shared lag-5/lag-6 {len(S5 & S6)}, lag-5/repeats {len(S5 & D)}, lag-6/repeats {len(S6 & D)}.",
        f"- Words involved: lag-5 {len(W5)}, lag-6 {len(W6)}, repeats {len(WD)}; shared lag-5/lag-6 words {len(W5 & W6)}, lag-5/repeat words {len(W5 & WD)}, lag-6/repeat words {len(W6 & WD)}.", ""]
# expectation conditional on word length: only words long enough to host both relations can share them
allwords = {(page[i], allw[i]): wlen[i] for i in range(len(allc))}
def cond(A, B, minlen):
    elig = {w for w, L in allwords.items() if L >= minlen}; a, b = A & elig, B & elig
    return len(a), len(b), len(a & b), len(a) * len(b) / max(1, len(elig)), len(elig)
for (A, B, ml, lbl) in ((W5, W6, 7, "lag-5 / lag-6"), (W5, WD, 6, "lag-5 / repeats"), (W6, WD, 7, "lag-6 / repeats")):
    a, b, sh, ex, ne = cond(A, B, ml)
    p = stats.hypergeom.sf(sh - 1, ne, a, b)
    out.append(f"- {lbl}, restricted to the {ne} words of length ≥ {ml} that can host both: {a} and {b} words, {sh} shared, {ex:.1f} expected if independent (hypergeometric p = {p:.3f}).")
out.append("")
(RESULTS / "echo_dissect.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
