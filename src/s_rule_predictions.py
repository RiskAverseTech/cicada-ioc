"""An S-triggered rule and its second trace, pre-registered (2026-10-28, §50).  The S carrier cannot come from the cipher
layer (§47).  The simplest rule acting on the written rune is RS5: inside a gated word, when the cipher rune five back is
S, write S.  Fitted to nothing but the eleven pairs it would be unfalsifiable, so it is judged ONLY on second traces it
implies and the eleven pairs are excluded from the score.  The rule is added on top of E56w (r = 0.5, q = 0.81); its own
rate rho is set so that the simulated count of lag-5 S..S pairs matches 11 (one parameter spent on the one fact).
Second traces, chosen before simulation:
  Q1  S..S..S triples at lag 5 inside words (copy chains)
  Q2  S..S at lag 10 inside words
  Q3  S..S at lag 5 ACROSS a word gap (predicted at the uniform rate: the rule is word-internal)
  Q4  S..S at lag 4 and at lag 6 inside words (uniform: the rule is lag-specific)
  Q5  share of S among all runes (rises by the copies, by about 0.06 points: predicted undetectable)
  Q6  within-word lag-5 equal pairs whose rune is P (the next-strongest rune in §45's table; the rule predicts no excess)
Rule: holds within |z| <= 2.5.  --predict writes and the result is committed before --check.  results/s_rule_predictions.md
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN, english_to_runes
import corpus
rng = np.random.default_rng(1515); Q, R_GATE, NREP = 0.81, 0.5, 300
S = LATIN.index("S"); P_ = LATIN.index("P"); T = lambda x: (24 - 2 * x) % N
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
LP2 = [parse(chunks[k]) for k in range(16, 72)]; LP2 = [(c, w) for c, w in LP2 if len(c)]; LENS = [len(c) for c, _ in LP2]
STATS = ["Q1_SSS_lag5", "Q2_SS_lag10", "Q3_SS_lag5_across", "Q4_SS_lag4", "Q4_SS_lag6", "Q5_S_share_pct", "Q6_PP_lag5", "fit_SS_lag5"]
def measure(pages):
    o = {s: 0 for s in STATS}; tot = 0; ns = 0
    for c, w in pages:
        n = len(c); tot += n; ns += int((c == S).sum())
        for i in range(n):
            if i >= 5 and c[i] == S and c[i - 5] == S:
                if w[i] == w[i - 5]:
                    o["fit_SS_lag5"] += 1
                    if i >= 10 and c[i - 10] == S and w[i - 10] == w[i]: o["Q1_SSS_lag5"] += 1
                else: o["Q3_SS_lag5_across"] += 1
            if i >= 10 and w[i] == w[i - 10] and c[i] == S and c[i - 10] == S: o["Q2_SS_lag10"] += 1
            if i >= 4 and w[i] == w[i - 4] and c[i] == S and c[i - 4] == S: o["Q4_SS_lag4"] += 1
            if i >= 6 and w[i] == w[i - 6] and c[i] == S and c[i - 6] == S: o["Q4_SS_lag6"] += 1
            if i >= 5 and w[i] == w[i - 5] and c[i] == P_ and c[i - 5] == P_: o["Q6_PP_lag5"] += 1
    o["Q5_S_share_pct"] = 100 * ns / tot
    return o
def simulate(rho):
    EW = simulate.EW; pages = []; wi = int(rng.integers(0, len(EW) - 5000))
    for L in LENS:
        Pp, W = [], []; w = 0
        while len(Pp) < L:
            word = list(EW[wi % len(EW)]); wi += 1; Pp += word; W += [w] * len(word); w += 1
        Pp, W = np.array(Pp[:L]), np.array(W[:L])
        k = rng.integers(0, N, 2 * L + 16); c = np.empty(L, int); j = 0; prev = -1; wpos = 0; active = False
        for i in range(L):
            if i == 0 or W[i] != W[i - 1]: wpos = 0; active = rng.random() < R_GATE
            else: wpos += 1
            p = Pp[i]
            if active:
                x = -1
                if wpos >= 5 and c[i - 5] == S and rng.random() < rho: x = S          # the S-triggered copy
                elif wpos >= 5 and Pp[i - 5] == p: x = c[i - 5]
                elif wpos >= 6 and Pp[i - 6] == p: x = T(c[i - 6])
                if x != -1 and x != prev: c[i] = x; prev = x; j += 1; continue
            x = (p + k[j]) % N
            if x == prev and rng.random() < Q:
                for _ in range(4):
                    j += 1; x = (p + k[j]) % N
                    if x != prev: break
            c[i] = x; prev = x; j += 1
        pages.append((c, W))
    return pages
PRED = RESULTS / "s_rule_predictions.json"
if "--predict" in sys.argv:
    simulate.EW = [w for w in (english_to_runes(x) for x in corpus.TEXTS["emerson_essays1"][0]().split()) if w]
    # set rho so that the simulated lag-5 S..S count is 11 (grid, 60 books per point)
    best = None
    for rho in np.arange(0.0, 0.61, 0.05):
        m = np.mean([measure(simulate(rho))["fit_SS_lag5"] for _ in range(60)])
        if best is None or abs(m - 11) < abs(best[1] - 11): best = (float(rho), float(m))
    rho = best[0]; reps = [measure(simulate(rho)) for _ in range(NREP)]
    pred = {s: dict(mean=float(np.mean([r[s] for r in reps])), sd=float(np.std([r[s] for r in reps]))) for s in STATS}
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), rho=rho, fitted_SS=best[1], nrep=NREP, predictions=pred), open(PRED, "w"), indent=1)
    lines = ["# RS5: predictions written before the check", "", f"Written {time.strftime('%Y-%m-%d %H:%M')}; rho = {rho:.2f} (set so the simulated lag-5 S..S count is {best[1]:.1f}); {NREP} books. The fit row is spent; the Q rows are the test.", "", "| statistic | predicted mean ± sd | LP2 | z | holds |", "|---|---|---|---|---|"] + [f"| {s} | {pred[s]['mean']:.2f} ± {pred[s]['sd']:.2f} | | | |" for s in STATS]
    (RESULTS / "s_rule_predictions.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    d = json.load(open(PRED)); pred = d["predictions"]; obs = measure(LP2); held = 0; lines = ["# RS5: second traces against LP2", "", f"Predictions written {d['written']}, rho = {d['rho']:.2f}; checked afterwards. Rule: holds within |z| <= 2.5; the fit row does not count.", "", "| statistic | predicted mean ± sd | LP2 | z | holds |", "|---|---|---|---|---|"]
    for s in STATS:
        m, sd = pred[s]["mean"], max(pred[s]["sd"], 1e-9); z = (obs[s] - m) / sd; ok = abs(z) <= 2.5; held += ok and not s.startswith("fit")
        lines.append(f"| {s} | {m:.2f} ± {sd:.2f} | {obs[s]:.2f} | {z:+.2f} | {'(fit)' if s.startswith('fit') else 'yes' if ok else 'NO'} |")
    lines += ["", f"Second traces held: {held} of {len(STATS) - 1}."]
    (RESULTS / "s_rule_predictions.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
