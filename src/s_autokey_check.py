"""The S carrier against a plaintext autokey (2026-10-30, §47 addendum).

§47's corrected argument leaves one additive class open: a key that reads the plaintext.  The simplest member, the lag-1
plaintext autokey c_i = p_i - p_(i-1) (sub sign), turns out to put S at 3.1 x uniform among within-word lag-5 cipher
coincidences on English, the pages' own figure, with no S-specific step: the Gematria order puts several of English's
commonest bigrams (E-R, N-A, A-I, U-T, R-M) exactly 15 apart, so S is the most frequent difference value and the most
frequent value dominates coincidences.  The same rule predicts the whole profile of values at coincidences, not only S,
and it predicts an IoC of 1.12, an S share 1.21 x uniform and a repeat rate 1.32 x uniform, where the pages have 1.00,
0.97 and 0.19.  This script measures the profile test: the pages' 102 coincidence values against the autokey prediction
(Emerson, 47,000 within-word lag-5 pairs) and against uniform.  Output: results/s_autokey_check.md.
"""
import re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy.stats import chisquare
from lp import IDX, RAW, RESULTS, N, english_to_runes

t0 = time.time(); LAG, S = 5, 15; rng = np.random.default_rng(7)
NAMES = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
obs = np.zeros(N, int)
for k in range(16, 72):
    runes, wid = [], []; w = 0; pend = False
    for ch in chunks[k]:
        if ch in IDX:
            if pend: w += 1; pend = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pend = True
    C, W = np.array(runes), np.array(wid)
    if len(C) <= LAG: continue
    i = np.where(W[LAG:] == W[:-LAG])[0]; eq = i[C[i] == C[i + LAG]]; obs += np.bincount(C[eq], minlength=N)
text = (RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(errors="ignore")[20000:]
words = []
for w in re.findall(r"[A-Za-z']+", text):
    try: r = english_to_runes(w)
    except Exception: continue
    if len(r): words.append(np.array(r))
P = np.concatenate(words); wid = np.concatenate([np.full(len(w), k) for k, w in enumerate(words)]); i = np.where(wid[LAG:] == wid[:-LAG])[0]


def stats(C):
    cnt = np.bincount(C, minlength=N); ioc = (cnt * (cnt - 1)).sum() / (len(C) * (len(C) - 1)) * N
    eq = i[C[i] == C[i + LAG]]; prof = np.bincount(C[eq], minlength=N).astype(float)
    return ioc, np.mean(C[1:] == C[:-1]) * N, np.mean(C == S) * N, prof / prof.sum()


rows = []
for d in (1, 2, 3):
    for sign, f in (("sub", lambda p, k: (p - k) % N), ("beaufort", lambda p, k: (k - p) % N), ("add", lambda p, k: (p + k) % N)):
        K = np.concatenate([rng.integers(0, N, d), P[:-d]]); ioc, dbl, ssh, prof = stats(f(P, K))
        exp = prof * obs.sum(); m = exp >= 1.0
        o_, e_ = (np.append(obs[m], obs[~m].sum()), np.append(exp[m], exp[~m].sum())) if (~m).any() else (obs, exp)
        chi, p = chisquare(o_, e_ * o_.sum() / e_.sum())
        rows.append((d, sign, ioc, dbl, ssh, prof[S] * N, chi, len(o_) - 1, p, prof))
chi_u, p_u = chisquare(obs, np.full(N, obs.sum() / N))
best = rows[0]; order = np.argsort(-best[9])
out = ["# The S carrier against a plaintext autokey", "",
       f"Pages: {obs.sum()} within-word lag-5 cipher coincidences, {obs[S]} of them S. Prediction: English (Emerson in runes, {len(i):,} within-word lag-5 pairs) under a plaintext autokey of lag d, key = the plaintext d runes back, primer uniform. Columns: the rule's IoC, repeat rate and S share (× uniform; pages 1.00, 0.19, 0.97), its S share at coincidences (× uniform; pages 3.1), and the chi-square of the pages' 29-value coincidence profile against the rule's predicted profile (cells with expectation < 1 pooled).", "",
       "| lag | sign | IoC | repeats × | S share × | S at coincidences × | χ² of the pages' profile | df | p |", "|---|---|---|---|---|---|---|---|---|"]
for d, sign, ioc, dbl, ssh, s5, chi, df, p, _ in rows: out.append(f"| {d} | {sign} | {ioc:.2f} | {dbl:.2f} | {ssh:.2f} | {s5:.2f} | {chi:.0f} | {df} | {p:.2g} |")
out += ["", f"The pages' profile against uniform: χ² {chi_u:.1f} on 28 df, p = {p_u:.3f} (the S cell carries it).", "",
        "Lag-1 sub, the rule that matches the S weight, predicts these values at coincidences (expected of 102 against observed):", "", "| value | predicted share | expected | observed |", "|---|---|---|---|"]
for v in order[:8]: out.append(f"| {NAMES[v]} | {100*best[9][v]:.1f} % | {best[9][v]*obs.sum():.1f} | {obs[v]} |")
out += ["", "Reading: a lag-1 plaintext autokey under the sub sign reproduces the S weight at coincidences exactly (3.1 × uniform) and for a stated reason, the Gematria order's placement of E-R, N-A, A-I, U-T and R-M fifteen apart. It is excluded all the same: it predicts TH, X, L and Y enriched beside S, and the pages show them at or below uniform (χ² 167 on 25 df); and it predicts an IoC of 1.12, a repeat rate 1.32 × and an S share 1.21 × where the pages read 1.00, 0.19 and 0.97. The S carrier is not a plaintext-difference effect. What remains of §47's residual class is a key that reads the written rune S itself. [stated — the tables; inferred — the last two sentences]", "",
        f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/s_autokey_check.py`.", ""]
(RESULTS / "s_autokey_check.md").write_text("\n".join(out)); print("\n".join(out[:12]))
