"""Three registered follow-up tests of E56w+n (2026-10-29, §59), named at the end of §58 before any of them was run.
Two phases, committed between them: --predict writes every prediction; --check compares with the pages.

T1  FILLER RATE FITTED TO THE WORD LENGTHS, THEN THE LAG COUNTS PREDICTED.  §58 took the filler rate 0.45 from
    pnotisdev's R4.  Here the rate is chosen on the word-length histogram alone: for p in 0.20 .. 0.70 step 0.05, 100
    simulated books of E56w+n at p, the pooled histogram of simulated word lengths (1 .. 15+) is the reference and the
    chi-square of LP2's 2,928 words against it is the fit statistic; p* = the minimum.  Then 200 books at p* give the
    predicted mean ± sd of §47's twelve statistics, judged by §47's rule (|z| <= 3 on the ten).  Expectation written
    before running: p* a little below 0.45 (at 0.45 the simulated mean length is 4.53 against LP2's 4.42), so D rises
    toward 80 and L3 / L4 fall a little; L5S stays near 5.
T2  LAG-5 PROFILE PER EXACT WORD LENGTH.  Within-word lag-5 equal pairs in words of exactly 6, 7, 8, 9, 10, 11 and 12+
    runes (7 cells) and within-word lag-6 T hits in words of exactly 7, 8, 9, 10, 11 and 12+ runes (6 cells), 300 books
    of E56w+n at the registered rate 0.45 (p* reported beside it as a secondary column, not judged).  Rule: |z| <= 2.5
    per cell, the thirteen judged as a set (about 0.16 chance failures).  §57's pooled bins (6 / 7-8 / 9+ and 7 / 8-9 /
    10+) are spent; the question is whether the pooling hid a shape.
T3  THE L4 EXCESS ON THE SOLVED PAGES.  LP2 has 131 within-word lag-4 equal pairs against E56w+n's 113 ± 11 (z +1.6), the
    one judged cell besides S above +1.5.  The solved polyalphabetic pages (chunks 2, 3: Vigenère DIVINITY; 13, 14:
    Vigenère FIRFUMFERENFE; 72: totient stream; 919 runes, §41's selection) carry English under a key with no filler
    and no echo, so E56w+n with its filler and echoes switched off predicts their within-word equal-pair counts at lags
    3, 4, 5 and 6.  Null: 300 books of Emerson's words laid into each chunk's rune count, encrypted with the chunk's
    key (the two Vigenère keys at a uniform random phase; an iid key for the totient chunk), equal pairs counted inside
    the simulated words; rule |z| <= 2.5 per lag.  Expectation written before running: all four lags inside the band,
    so that the lag-4 excess, like the repeat deficit (§41) and the echoes, is a property of the unsolved section
    alone; the sample is small (about 500 lag-4 pairs, 17 expected equal), so this test can see only a large excess.
Writes results/e56w_n_followups.md / .json.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS, N, english_to_runes
import mechanism_lane as ML

OUT = RESULTS / "e56w_n_followups.json"; MD = RESULTS / "e56w_n_followups.md"
RULE = "E56w+n"; GRID = [round(0.20 + 0.05 * i, 2) for i in range(11)]; MAXL = 15
T = ML.T
POLY = {2: "DIVINITY", 3: "DIVINITY", 13: "FIRFUMFERENFE", 14: "FIRFUMFERENFE", 72: None}

def word_lengths(pages):
    L = np.concatenate([np.bincount(w) for _, w in pages]); return L[L > 0]
def hist(L):
    h = np.bincount(np.minimum(L, MAXL), minlength=MAXL + 1)[1:].astype(float); return h / h.sum()
def chi2(obs_L, ref_h):
    n = len(obs_L); e = np.maximum(ref_h * n, 0.5); return float((((hist(obs_L) * n) - e) ** 2 / e).sum())

L5_BINS = [6, 7, 8, 9, 10, 11, 12]; L6_BINS = [7, 8, 9, 10, 11, 12]
def profile(pages):
    out = {f"L5_len{b}{'p' if b == 12 else ''}": 0 for b in L5_BINS}; out.update({f"L6T_len{b}{'p' if b == 12 else ''}": 0 for b in L6_BINS})
    for c, w in pages:
        wl = np.bincount(w); L = np.minimum(wl[w], 12); n = len(c)
        for i in range(5, n):
            if w[i] == w[i - 5] and c[i] == c[i - 5]: out[f"L5_len{L[i]}{'p' if L[i] == 12 else ''}"] += 1
        for i in range(6, n):
            if w[i] == w[i - 6] and c[i] == T(c[i - 6]): out[f"L6T_len{L[i]}{'p' if L[i] == 12 else ''}"] += 1
    return out
PROF = list(profile([(np.zeros(1, int), np.zeros(1, int))]).keys())

def eq_lags(pages, lags=(3, 4, 5, 6)):
    out = {}
    for lag in lags:
        n_eq = n_pairs = 0
        for c, w in pages:
            ok = ML.pairs_at(c, w, lag); n_pairs += len(ok); n_eq += int((c[ok] == c[ok - lag]).sum())
        out[f"eq_lag{lag}"] = n_eq; out[f"pairs_lag{lag}"] = n_pairs
    return out

SOLVED = {k: ML.parse(ML.chunks[k]) for k in POLY}
def sim_solved(rng):
    pages = []
    for k, key in POLY.items():
        c0, w0 = SOLVED[k]; Lp = len(c0); P, W = [], []; wi = int(rng.integers(0, len(ML.EW) - 500)); w = 0
        while len(P) < Lp:
            word = list(ML.EW[wi % len(ML.EW)]); wi += 1; P += word; W += [w] * len(word); w += 1
        P, W = np.array(P[:Lp]), np.array(W[:Lp])
        if key is None: K = rng.integers(0, N, Lp)
        else: kk = np.array(english_to_runes(key)); ph = int(rng.integers(0, len(kk))); K = kk[(np.arange(Lp) + ph) % len(kk)]
        pages.append(((P + K) % N, W))
    return pages

if "--predict" in sys.argv:
    t0 = time.time(); rng = np.random.default_rng(59); ML.rng = rng
    lp2_L = word_lengths(ML.LP2); fit = []
    for p in GRID:
        H = np.mean([hist(word_lengths(ML.simulate(RULE, p_null=p))) for _ in range(100)], axis=0); fit.append((p, chi2(lp2_L, H)))
    p_star = min(fit, key=lambda x: x[1])[0]
    repsA = [ML.measure(ML.simulate(RULE, p_null=p_star)) for _ in range(200)]
    predA = {s: dict(mean=float(np.mean([r[s] for r in repsA])), sd=float(np.std([r[s] for r in repsA]))) for s in ML.STATS}
    reps2 = [profile(ML.simulate(RULE)) for _ in range(300)]; reps2s = [profile(ML.simulate(RULE, p_null=p_star)) for _ in range(300)]
    pred2 = {s: dict(mean=float(np.mean([r[s] for r in reps2])), sd=float(np.std([r[s] for r in reps2]))) for s in PROF}
    pred2s = {s: dict(mean=float(np.mean([r[s] for r in reps2s])), sd=float(np.std([r[s] for r in reps2s]))) for s in PROF}
    reps3 = [eq_lags(sim_solved(rng)) for _ in range(300)]
    pred3 = {s: dict(mean=float(np.mean([r[s] for r in reps3])), sd=float(np.std([r[s] for r in reps3]))) for s in reps3[0]}
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), fit=fit, p_star=p_star, A=predA, T2=pred2, T2_pstar=pred2s, T3=pred3), open(OUT, "w"), indent=1)
    lines = ["# E56w+n follow-ups: predictions written before the check", "", f"Written {time.strftime('%Y-%m-%d %H:%M')} ({time.time() - t0:.0f} s).", "",
             "## T1 fit of the filler rate to the word-length histogram", "", "| p | chi-square of LP2's words against the simulated histogram |", "|---|---|"] + [f"| {p:.2f} | {c:.1f} |" for p, c in fit] + ["", f"p* = {p_star:.2f}", "", "| statistic | predicted at p* |", "|---|---|"] + [f"| {s} | {predA[s]['mean']:.3f} ± {predA[s]['sd']:.3f} |" for s in ML.STATS]
    lines += ["", "## T2 profile cells (at 0.45; at p* in the second column)", "", "| cell | predicted (0.45) | predicted (p*) |", "|---|---|---|"] + [f"| {s} | {pred2[s]['mean']:.2f} ± {pred2[s]['sd']:.2f} | {pred2s[s]['mean']:.2f} ± {pred2s[s]['sd']:.2f} |" for s in PROF]
    lines += ["", "## T3 solved polyalphabetic pages, English under the published keys", "", "| statistic | predicted |", "|---|---|"] + [f"| {s} | {pred3[s]['mean']:.2f} ± {pred3[s]['sd']:.2f} |" for s in pred3]
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    d = json.load(open(OUT)); refA = ML.measure(ML.LP2); obs2 = profile(ML.LP2); obs3 = eq_lags(list(SOLVED.values())); obsU = eq_lags(ML.LP2)
    lines = ["# E56w+n follow-ups: three registered tests against the pages", "", f"Predictions written {d['written']} (commit recorded in README §59); checked afterwards.", ""]
    lines += [f"## T1: filler rate fitted to the word lengths, p* = {d['p_star']:.2f}; §47's statistics at p*", "", "| p | chi-square |", "|---|---|"] + [f"| {p:.2f} | {c:.1f} |" for p, c in d["fit"]] + ["", "| statistic | LP2 | predicted at p* | z | holds (|z| ≤ 3) |", "|---|---|---|---|---|"]
    failA = []
    for s in ML.STATS:
        m, sd = d["A"][s]["mean"], max(d["A"][s]["sd"], 1e-9); z = (refA[s] - m) / sd; j = s in ML.JUDGE
        if j and abs(z) > 3: failA.append(s)
        lines.append(f"| {s} | {refA[s]:.4g} | {m:.4g} ± {sd:.2g} | {z:+.2f} | {('yes' if abs(z) <= 3 else 'NO') if j else 'not judged'} |")
    lines += ["", f"T1 verdict at p*: {'survives' if not failA else 'fails: ' + ', '.join(failA)}.", "", "## T2: lag-5 and lag-6 profiles per exact word length (300 books at 0.45; p* column not judged)", "", "| cell | LP2 | predicted (0.45) | z | holds (|z| ≤ 2.5) | predicted (p*) | z |", "|---|---|---|---|---|---|---|"]
    held = 0
    for s in PROF:
        m, sd = d["T2"][s]["mean"], max(d["T2"][s]["sd"], 1e-9); z = (obs2[s] - m) / sd; ok = abs(z) <= 2.5; held += ok
        m2, sd2 = d["T2_pstar"][s]["mean"], max(d["T2_pstar"][s]["sd"], 1e-9)
        lines.append(f"| {s} | {obs2[s]} | {m:.2f} ± {sd:.2f} | {z:+.2f} | {'yes' if ok else 'NO'} | {m2:.2f} ± {sd2:.2f} | {(obs2[s] - m2) / sd2:+.2f} |")
    lines += ["", f"T2: {held} of {len(PROF)} cells hold.", "", "## T3: within-word equal pairs on the solved polyalphabetic pages (chunks 2, 3, 13, 14, 72)", "", "| lag | pairs | equal, observed | uniform pairs/29 | predicted (English under the keys) | z | holds (|z| ≤ 2.5) | LP2 for comparison: equal / pairs / per-29 ratio |", "|---|---|---|---|---|---|---|---|"]
    held3 = 0
    for lag in (3, 4, 5, 6):
        s = f"eq_lag{lag}"; m, sd = d["T3"][s]["mean"], max(d["T3"][s]["sd"], 1e-9); z = (obs3[s] - m) / sd; ok = abs(z) <= 2.5; held3 += ok
        lines.append(f"| {lag} | {obs3[f'pairs_lag{lag}']} | {obs3[s]} | {obs3[f'pairs_lag{lag}'] / N:.1f} | {m:.1f} ± {sd:.1f} | {z:+.2f} | {'yes' if ok else 'NO'} | {obsU[s]} / {obsU[f'pairs_lag{lag}']} / {obsU[s] / (obsU[f'pairs_lag{lag}'] / N):.2f} |")
    lines += ["", f"T3: {held3} of 4 lags hold.", "", "Reproduce: `.venv/bin/python -I src/e56w_n_followups.py --predict` then `--check`."]
    json.dump(dict(d, lp2A=refA, lp2T2=obs2, solvedT3=obs3, lp2T3=obsU, failA=failA, heldT2=held, heldT3=held3), open(OUT, "w"), indent=1, default=float)
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
