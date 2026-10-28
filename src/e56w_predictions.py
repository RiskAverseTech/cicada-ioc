"""Out-of-sample predictions of the gated echo rule E56w (2026-10-28, §49).  Two phases, run in this order and committed
between them so the record shows the predictions preceded the look:
  --predict   simulate E56w (as fitted in §47: r = 0.5, q = 0.81, English plaintext, iid key, LP2 page lengths) 300 times
              and write the predicted mean ± sd of EIGHT statistics that were NOT used to fit or judge the rule.
  --check     compute the same eight on LP2 and compare.
The eight (chosen before either phase ran; what was known beforehand is declared next to each):
  P1  lag-6 T hits by word length: 7 runes / 8-9 / 10+   (pnotisdev reported "none in 7-rune words, 2x in 8-9"; declared)
  P2  lag-5 equal pairs by word length: 6 / 7-8 / 9+
  P3  words carrying two or more echo sites (lag-5 equality or lag-6 T), and words carrying three or more
  P4  within-word lag-10 equal pairs (a lag-5 echo in a word with three equal plaintext runes five apart)
  P5  lag-6 T sites whose first rune is at word position 0, as a share of all lag-6 T sites
  P6  adjacent repeats inside echo-bearing words per 100 adjacent pairs, against the same rate in other words of length >= 7
  P7  lag-5 equal pairs ACROSS a word gap (positions 5 apart in different words of the same page): E56w predicts the
      uniform rate, since its echo is word-internal   (the page-wide bigram count of §46 touched this; declared)
  P8  lag-6 T hits across a word gap: likewise the uniform rate
Verdict rule: a prediction holds if LP2 is within |z| <= 2.5 of the simulated distribution; the set is judged as a whole
(eight at 2.5 sd: about one chance failure expected in 90 runs).  Writes results/e56w_predictions.md (both phases).
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN, english_to_runes
import corpus

rng = np.random.default_rng(49); Q, R_GATE, NREP = 0.81, 0.5, 300
T = lambda x: (24 - 2 * x) % N
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
LP2 = [parse(chunks[k]) for k in range(16, 72)]; LP2 = [(c, w) for c, w in LP2 if len(c)]
LENS = [len(c) for c, _ in LP2]
STATS = ["P1_len7", "P1_len89", "P1_len10p", "P2_len6", "P2_len78", "P2_len9p", "P3_multi2", "P3_multi3", "P4_lag10", "P5_pos0_share", "P6_rep_echo_words", "P6_rep_other_words", "P7_lag5_across", "P8_lag6_across"]

def measure(pages):
    out = {s: 0.0 for s in STATS}; sites = {}; wlen = {}; echo_words = set()
    pairs_echo = reps_echo = pairs_other = reps_other = 0
    for pi, (c, w) in enumerate(pages):
        n = len(c); wl = np.bincount(w); L = wl[w]
        pos = np.zeros(n, int)
        for i in range(1, n): pos[i] = pos[i - 1] + 1 if w[i] == w[i - 1] else 0
        hits = {}
        for i in range(5, n):
            if w[i] == w[i - 5] and c[i] == c[i - 5]:
                hits[(pi, w[i])] = hits.get((pi, w[i]), 0) + 1
                out["P2_len6" if L[i] == 6 else "P2_len78" if L[i] <= 8 else "P2_len9p"] += 1
            elif w[i] != w[i - 5] and c[i] == c[i - 5]: out["P7_lag5_across"] += 1
        for i in range(6, n):
            if w[i] == w[i - 6] and c[i] == T(c[i - 6]):
                hits[(pi, w[i])] = hits.get((pi, w[i]), 0) + 1
                out["P1_len7" if L[i] == 7 else "P1_len89" if L[i] <= 9 else "P1_len10p"] += 1
                out["P5_pos0_share"] += (pos[i - 6] == 0)
            elif w[i] != w[i - 6] and c[i] == T(c[i - 6]): out["P8_lag6_across"] += 1
        for i in range(10, n):
            if w[i] == w[i - 10] and c[i] == c[i - 10]: out["P4_lag10"] += 1
        ew = {k for k, v in hits.items()}
        for i in range(1, n):
            if w[i] == w[i - 1] and L[i] >= 7:
                if (pi, w[i]) in ew: pairs_echo += 1; reps_echo += (c[i] == c[i - 1])
                else: pairs_other += 1; reps_other += (c[i] == c[i - 1])
        out["P3_multi2"] += sum(1 for v in hits.values() if v >= 2); out["P3_multi3"] += sum(1 for v in hits.values() if v >= 3)
    n6 = out["P1_len7"] + out["P1_len89"] + out["P1_len10p"]
    out["P5_pos0_share"] = out["P5_pos0_share"] / max(1, n6)
    out["P6_rep_echo_words"] = 100 * reps_echo / max(1, pairs_echo); out["P6_rep_other_words"] = 100 * reps_other / max(1, pairs_other)
    return out

def simulate():
    text = simulate.text; EW = simulate.EW
    pages = []; wi = int(rng.integers(0, len(EW) - 5000))
    for L in LENS:
        P, W = [], []; w = 0
        while len(P) < L:
            word = list(EW[wi % len(EW)]); wi += 1; P += word; W += [w] * len(word); w += 1
        P, W = np.array(P[:L]), np.array(W[:L])
        k = rng.integers(0, N, 2 * L + 16); c = np.empty(L, int); j = 0; prev = -1; wpos = 0; active = False
        for i in range(L):
            if i == 0 or W[i] != W[i - 1]: wpos = 0; active = rng.random() < R_GATE
            else: wpos += 1
            p = P[i]
            if active:
                x = -1
                if wpos >= 5 and P[i - 5] == p: x = c[i - 5]
                elif wpos >= 6 and P[i - 6] == p: x = T(c[i - 6])
                if x != -1 and x != prev: c[i] = x; prev = x; j += 1; continue
            x = (p + k[j]) % N
            if x == prev and rng.random() < Q:
                for _ in range(4):
                    j += 1; x = (p + k[j]) % N
                    if x != prev: break
            c[i] = x; prev = x; j += 1
        pages.append((c, W))
    return pages

PRED = RESULTS / "e56w_predictions.json"
if "--predict" in sys.argv:
    simulate.text = corpus.TEXTS["emerson_essays1"][0](); simulate.EW = [w for w in (english_to_runes(x) for x in simulate.text.split()) if w]
    reps = [measure(simulate()) for _ in range(NREP)]
    pred = {s: dict(mean=float(np.mean([r[s] for r in reps])), sd=float(np.std([r[s] for r in reps]))) for s in STATS}
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), nrep=NREP, r=R_GATE, q=Q, predictions=pred), open(PRED, "w"), indent=1)
    lines = ["# E56w: predictions written before the check", "", f"Written {time.strftime('%Y-%m-%d %H:%M')} from {NREP} simulated books (r = {R_GATE}, q = {Q}); the LP2 column is empty until `--check` runs.", "", "| statistic | predicted mean ± sd | LP2 | z | holds (|z| ≤ 2.5) |", "|---|---|---|---|---|"]
    for s in STATS: lines.append(f"| {s} | {pred[s]['mean']:.2f} ± {pred[s]['sd']:.2f} | | | |")
    (RESULTS / "e56w_predictions.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    d = json.load(open(PRED)); pred = d["predictions"]; obs = measure(LP2)
    lines = ["# E56w: eight out-of-sample predictions against LP2", "", f"Predictions written {d['written']} (commit recorded in README §49) from {d['nrep']} simulated books; checked afterwards. Rule: a prediction holds within |z| ≤ 2.5.", "", "| statistic | predicted mean ± sd | LP2 | z | holds |", "|---|---|---|---|---|"]
    held = 0
    for s in STATS:
        m, sd = pred[s]["mean"], max(pred[s]["sd"], 1e-9); z = (obs[s] - m) / sd; ok = abs(z) <= 2.5; held += ok
        lines.append(f"| {s} | {m:.2f} ± {sd:.2f} | {obs[s]:.2f} | {z:+.2f} | {'yes' if ok else 'NO'} |")
    lines += ["", f"Held: {held} of {len(STATS)} cells (eight predictions, some with two or three cells)."]
    (RESULTS / "e56w_predictions.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
