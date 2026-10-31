"""Is the page a unit? Words that cross page joins, and the cross-join pairs (2026-10-31; row C10).

Registered in results/quorum_checks_registration.md (commit before this run). In the master transcription a page that ends
on a rune with no separator continues its word on the next page (solved page 0.3 ends ADHEREN, 0.4 begins CE). Here: the
unsolved joins that fall inside a word, the joined words' lengths against within-page words (KS), the join split rate
against the line split rate, doublets at the mid-word joins, and the cross-join within-word pairs at lags 2-6 with their
equalities and lag-6 affine hits against chance and against the within-page within-word rates of §42.
Output: results/page_joins.md. Reproduce: .venv/bin/python -I src/page_joins.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN

txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
ks = [k for k in range(16, 72) if any(c in IDX for c in chunks[k])]
def body(s): return [c for c in s if c in IDX or c in SEP]
def words_in(s):
    out, cur = [], []
    for c in body(s):
        if c in IDX: cur.append(IDX[c])
        elif cur: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
# words wholly inside a page: drop a page-initial word when the previous page ended mid-word, and a page-final word when the page ends mid-word
inside, cross, joins_midword = [], [], 0; lat = lambda w: "".join(LATIN[v] for v in w)
B = {k: body(chunks[k]) for k in ks}
for n, k in enumerate(ks):
    ws = words_in(chunks[k]); b = B[k]
    first_open = n > 0 and B[ks[n-1]][-1] in IDX and b[0] in IDX
    last_open = n < len(ks) - 1 and b[-1] in IDX and B[ks[n+1]][0] in IDX
    lo = 1 if first_open else 0; hi = len(ws) - 1 if last_open else len(ws)
    inside += ws[lo:hi]
    if last_open:
        nxt = words_in(chunks[ks[n+1]])[0]; cross.append((k - 16, ws[-1], nxt)); joins_midword += 1
L_in = np.array([len(w) for w in inside]); L_x = np.array([len(a) + len(b) for _, a, b in cross])
ksp = stats.ks_2samp(L_x, L_in).pvalue
# within-page within-word rates (§42 definitions) for comparison
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
rate = {}
for d in range(1, 7):
    eq = pairs = hit = 0
    for k in ks:
        c, w = parse(chunks[k]); i = np.arange(d, len(c)); m = w[i] == w[i-d]
        pairs += int(m.sum()); eq += int(((c[i] == c[i-d]) & m).sum()); hit += int(((c[i] == (24 - 2*c[i-d]) % N) & m).sum())
    rate[d] = (pairs, eq, hit)
# cross-join pairs: positions in the joined word a+b, pairs (p, p+d) with p in a-part and p+d in b-part
rows = []; summary = {}
for d in range(1, 7):
    pairs = eq = hit = 0
    for _, a, b in cross:
        w = a + b; A = len(a)
        for p in range(max(0, A - d), A):
            q = p + d
            if q < len(w) and q >= A:
                pairs += 1; eq += w[p] == w[q]; hit += w[q] == (24 - 2*w[p]) % N
    summary[d] = (pairs, eq, hit)
P, E, H = rate[5][0], rate[5][1], rate[6][2]
out = ["# Is the page a unit? Words across page joins (row C10)", "",
       f"Unsolved pages: {len(ks)}, joins {len(ks)-1}. Joins that fall inside a word (page ends on a rune, next page begins on a rune, no separator between): **{joins_midword}**. Line breaks inside words, for comparison: 452 of 630 (§33). Words wholly inside a page: {len(inside):,}.", "",
       f"- C10-P1: joined-word lengths (n = {len(L_x)}, mean {L_x.mean():.1f}) against within-page word lengths (mean {L_in.mean():.1f}): KS p = **{ksp:.2f}**. Join split rate {joins_midword}/{len(ks)-1} = {joins_midword/(len(ks)-1):.2f}; line split rate 452/630 = 0.72.",
       f"- Doublets at the {joins_midword} mid-word joins: **{summary[1][1]}** (expected {joins_midword/N:.2f} under a per-page reset with a uniform first rune; {joins_midword*rate[1][1]/rate[1][0]:.2f} at the within-word adjacent-repeat rate {rate[1][1]}/{rate[1][0]:,}). Likelihood ratio for continuity from this count alone: {np.exp(-joins_midword*rate[1][1]/rate[1][0]) / np.exp(-joins_midword/N):.1f}.", "",
       "| lag d | cross-join within-word pairs | equal | expected at 1/29 | expected at the within-page within-word rate | lag-6 affine hits | expected at 1/29 | expected at the within-page rate |", "|---|---|---|---|---|---|---|---|"]
for d in range(2, 7):
    pr, eq, hit = summary[d]; pp, pe, ph = rate[d]
    out.append(f"| {d} | {pr} | {eq} | {pr/N:.2f} | {pr*pe/pp:.2f} | {hit} | {pr/N:.2f} | {pr*ph/pp:.2f} |")
out += ["", "The joined words, Latin transliteration (page | next page):", "", "| join | page-final part | page-initial part | joined length |", "|---|---|---|---|"]
out += [f"| LP2-{k:02d} → {k+1:02d} | {lat(a)} | {lat(b)} | {len(a)+len(b)} |" for k, a, b in cross]
out += ["", "Reading: written after the run, below. [stated — the table]", ""]
(RESULTS / "page_joins.md").write_text("\n".join(out)); print("\n".join(out[:12]))
