"""Do the echoes depend on line breaks? (2026-10-28, §50.)  Looking at the eleven S..S sites in the page images showed four
of them straddling a line break (the word wraps between the two S).  Post-hoc cut, so it is tested with controls:
for lags 4, 5, 6 (identity) and the lag-6 T relation, within-word pairs split by whether a line break lies between
the two runes; the same split for ACROSS-word pairs (a line break between the runes, different words); and the
two-proportion z for straddling against same-line.  Null for the straddle excess: 999 within-page shuffles with word
and line structure fixed (shuffle runes, keep every boundary where it is).  Writes results/linebreak_echo.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN
rng = np.random.default_rng(630); S = LATIN.index("S"); T = lambda x: (24 - 2 * x) % N
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid, brk = [], [], []; w = 0; pending = False; pb = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w); brk.append(pb); pb = False
        elif ch in SEP: pending = True
        elif ch == '/': pb = True
    return np.array(runes), np.array(wid), np.array(brk)
U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0])]
def counts(pages):
    out = {}
    for c, w, b in pages:
        n = len(c)
        for lag in (4, 5, 6):
            for i in range(lag, n):
                same = w[i] == w[i - lag]; strad = bool(b[i - lag + 1:i + 1].any())
                for name, h in ((f"id{lag}", c[i] == c[i - lag]),) + (((f"T6", c[i] == T(c[i - 6])),) if lag == 6 else ()):
                    key = (name, "word" if same else "gap", "wrap" if strad else "line")
                    t, hh, ss = out.get(key, (0, 0, 0)); out[key] = (t + 1, hh + int(h), ss + int(h and c[i] == S and name == "id5"))
    return out
obs = counts(U)
NREP = 999; null = {k: np.zeros(NREP) for k in obs}
for r in range(NREP):
    P = [(rng.permutation(c), w, b) for c, w, b in U]; cr = counts(P)
    for k in obs: null[k][r] = cr.get(k, (0, 0, 0))[1]
rows = ["| statistic | pair type | line break between | pairs | hits | uniform expected | z (uniform) | shuffle null mean ± sd | p | S..S |", "|---|---|---|---|---|---|---|---|---|---|"]
for name in ("id4", "id5", "id6", "T6"):
    for wt in ("word", "gap"):
        for lb in ("line", "wrap"):
            k = (name, wt, lb)
            if k not in obs: continue
            t, h, ss = obs[k]; e = t / N; nz = null[k]; p = (np.sum(nz >= h) + 1) / (NREP + 1)
            rows.append(f"| {name} | {'inside a word' if wt == 'word' else 'across a word gap'} | {'yes' if lb == 'wrap' else 'no'} | {t:,} | {h} | {e:.1f} | {(h - e) / np.sqrt(e * (1 - 1 / N)):+.2f} | {nz.mean():.1f} ± {nz.std():.1f} | {p:.3f} | {ss if name == 'id5' and wt == 'word' else ''} |")
def two_prop(k1, k2):
    t1, h1, _ = obs[k1]; t2, h2, _ = obs[k2]; p = (h1 + h2) / (t1 + t2)
    return (h1 / t1 - h2 / t2) / np.sqrt(p * (1 - p) * (1 / t1 + 1 / t2))
z5 = two_prop(("id5", "word", "wrap"), ("id5", "word", "line")); zT = two_prop(("T6", "word", "wrap"), ("T6", "word", "line")); z4 = two_prop(("id4", "word", "wrap"), ("id4", "word", "line")); z6 = two_prop(("id6", "word", "wrap"), ("id6", "word", "line"))
out = ["# Do the echoes depend on line breaks?", "", "Within-word and across-gap pairs at lags 4, 5, 6, split by whether a line break falls between the two runes. The shuffle null keeps every word and line boundary in place and permutes the runes within the page.", ""] + rows + ["",
       f"Two-proportion z, straddling against same-line, inside words: lag-5 equality {z5:+.2f}; lag-6 T {zT:+.2f}; controls lag-4 equality {z4:+.2f}, lag-6 equality {z6:+.2f}.", "",
       "Reading: the lag-5 echo is stronger on pairs that wrap a line than on pairs within a line, and the lag-6 relation is not; across word gaps neither shows anything at a line break. If the difference holds up it points at the layout step, which acts on written runes, which is where the S argument of §47 says to look. It is a post-hoc cut found by eye and is reported with that status; the pre-registered test would be the same split on any further Cicada text, which does not exist.", ""]
(RESULTS / "linebreak_echo.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
