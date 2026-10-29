"""Out-of-sample predictions of E56w+R4n (2026-10-29, §57), in the §49 pattern: two phases, committed between them.
  --predict   simulate E56w+R4n exactly as src/mechanism_lane.py defines it after the §56 fix (gated lag-5 / lag-6 echo,
              r = 0.5, on top of R4n: hold repair writing T(c_-6), q = 0.81, one extra neighbour-checked uniform rune at a
              uniform in-word position in 45 % of words of length >= 2; English plaintext, iid key, LP2 page lengths)
              300 times and write the predicted mean ± sd of the statistics below.
  --check     compute the same statistics on LP2 and compare.
Why this rule: after the R4n base was repaired (§56) E56w+R4n is the only rule inside |z| <= 3 on all ten judged
statistics, sitting at the band's edge on L5S (+2.9) and L6T (-2.9), and its 45 % filler rate reproduces the §55
word-length fingerprint without having been fitted to it.  Those facts are spent.  The test is what the rule says about
statistics nobody fitted or judged it on.
The cells (fixed before either phase ran; what was known beforehand is declared):
  P1-P8  the fourteen cells of §49, unchanged (lag-6 T hits by word length 7 / 8-9 / 10+; lag-5 equal pairs by word
         length 6 / 7-8 / 9+; words with >= 2 and >= 3 echo sites; within-word lag-10 equalities; share of lag-6 sites
         at word position 0; adjacent repeats inside and outside echo-bearing words of length >= 7; lag-5 equalities
         and lag-6 T hits across word gaps).  E56w passed all fourteen (§49); the question is whether adding R4n's
         filler and hold repair, which lengthen words and add lag-6 hits, moves any cell out of the band.
  P9     within-word lag-12 hits of T∘T, c_i = 4 c_(i-12) - 24 (two chained lag-6 echoes); not previously computed.
  P10    within-word lag-11 hits of T, c_i = 24 - 2 c_(i-11) (a lag-5 identity echo chained with a lag-6 T echo in
         either order); not previously computed.
  P11    the word-length fingerprint, two cells: share of two-rune words and mean word length over the pages' words.
         DECLARED KNOWN: §56 noted that E56w+R4n's filler rate matches the §55 fingerprint; §55 published LP2's values
         (15.9 %, 4.42).  Reported for completeness, not counted as out-of-sample.
Verdict rule: a cell holds if LP2 is within |z| <= 2.5 of the simulated distribution; the sixteen out-of-sample cells
(P1-P10) are judged as a set (about 0.2 chance failures expected).  Writes results/e56w_r4n_predictions.md / .json.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS, N
import mechanism_lane as ML
_argv, sys.argv = sys.argv, sys.argv[:1]      # §49's module acts on --predict / --check itself; import it inert
import e56w_predictions as E49
sys.argv = _argv

NREP = 300; RULE = "E56w+R4n"
T2 = lambda x: (4 * x - 24) % N
EXTRA = ["P9_lag12_TT", "P10_lag11_T", "P11_two_rune_share", "P11_mean_wordlen"]
STATS = E49.STATS + EXTRA

def measure(pages):
    out = E49.measure(pages); out.update({s: 0.0 for s in EXTRA}); lens = []
    for c, w in pages:
        n = len(c)
        for i in range(12, n):
            if w[i] == w[i - 12] and c[i] == T2(c[i - 12]): out["P9_lag12_TT"] += 1
        for i in range(11, n):
            if w[i] == w[i - 11] and c[i] == ML.T(c[i - 11]): out["P10_lag11_T"] += 1
        lens.append(np.bincount(w)[np.bincount(w) > 0])
    L = np.concatenate(lens); out["P11_two_rune_share"] = float(np.mean(L == 2)); out["P11_mean_wordlen"] = float(L.mean())
    return out

PRED = RESULTS / "e56w_r4n_predictions.json"; MD = RESULTS / "e56w_r4n_predictions.md"
if "--predict" in sys.argv:
    ML.rng = np.random.default_rng(57); t0 = time.time()
    reps = [measure(ML.simulate(RULE)) for _ in range(NREP)]
    pred = {s: dict(mean=float(np.mean([r[s] for r in reps])), sd=float(np.std([r[s] for r in reps]))) for s in STATS}
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), nrep=NREP, rule=RULE, r=ML.R_GATE, q=ML.Q, p_null=0.45, predictions=pred), open(PRED, "w"), indent=1)
    lines = [f"# {RULE}: predictions written before the check", "", f"Written {time.strftime('%Y-%m-%d %H:%M')} from {NREP} simulated books ({RULE}: r = {ML.R_GATE}, q = {ML.Q}, p_null = 0.45; {time.time() - t0:.0f} s); the LP2 column is empty until `--check` runs.", "", "| statistic | predicted mean ± sd | LP2 | z | holds (|z| ≤ 2.5) |", "|---|---|---|---|---|"]
    for s in STATS: lines.append(f"| {s} | {pred[s]['mean']:.3f} ± {pred[s]['sd']:.3f} | | | |")
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    d = json.load(open(PRED)); pred = d["predictions"]; obs = measure(E49.LP2)
    e49 = json.load(open(RESULTS / "e56w_predictions.json"))["predictions"]
    lines = [f"# {RULE}: out-of-sample predictions against LP2", "", f"Predictions written {d['written']} (commit recorded in README §57) from {d['nrep']} simulated books; checked afterwards. Rule: a cell holds within |z| ≤ 2.5; P1–P10 are the out-of-sample set, P11 is declared known (§55, §56). E56w's own §49 prediction is shown beside each shared cell.", "", "| statistic | E56w+R4n predicted | LP2 | z | holds | E56w (§49) predicted | z |", "|---|---|---|---|---|---|---|"]
    held = tot = 0
    for s in STATS:
        m, sd = pred[s]["mean"], max(pred[s]["sd"], 1e-9); z = (obs[s] - m) / sd; ok = abs(z) <= 2.5
        if not s.startswith("P11"): held += ok; tot += 1
        if s in e49: m2, sd2 = e49[s]["mean"], max(e49[s]["sd"], 1e-9); old = f"{m2:.2f} ± {sd2:.2f} | {(obs[s] - m2) / sd2:+.2f}"
        else: old = "— | —"
        lines.append(f"| {s} | {m:.3f} ± {sd:.3f} | {obs[s]:.3f} | {z:+.2f} | {'yes' if ok else 'NO'}{' (declared)' if s.startswith('P11') else ''} | {old} |")
    lines += ["", f"Held: {held} of {tot} out-of-sample cells."]
    json.dump(dict(d, lp2=obs, held=held, cells=tot), open(PRED, "w"), indent=1, default=float)
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
