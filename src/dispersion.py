"""Windowed dispersion of the ciphertext difference stream (2026-10-27, docs/human-vs-machine-key.md):
does the key show the local balancing a human "random" sequence shows?

A hand-made random sequence keeps short windows more evenly populated than chance (too few runs,
the gambler's-fallacy signature).  The key is masked by the plaintext, but under an additive
cipher the difference stream D_i = C_i - C_{i-1} = (P_i - P_{i-1}) + (K_j - K_{j-1}) inherits any
balancing of the key's differences, diluted by the plaintext.  Statistic: mean over all 50-rune
windows (stride 25) of the chi-square of the 29 difference classes against uniform.  Observed value
on the 55 pages against three simulated generators of 200 replicates each, every one producing the
observed doublet rate on solved-page English at the real page lengths:
  A  iid uniform key, soft re-draw 0.81 on an output repeat (the §5 survivor);
  B  "bag" key: concatenated random permutations of the 29 runes (strong local balancing), same re-draw;
  C  "recent-avoid" key: a draw is rejected with probability 0.5 if it occurred in the last 6 key
     symbols (mild balancing), same re-draw.
Two statistics: S1 on the difference stream D (windows of 50) and S2 on the ciphertext C itself
(windows of 29 and 58), because balancing in the key does not carry into the key's differences:
the first run (S1 only) found generators A, B and C indistinguishable (29.12 / 29.18 / 29.10), i.e.
S1 has no power, and S2 was added before the observed S2 was read.  POWER is reported as the
separation between A and B/C in units of A's sd; a statistic with separation under 3 cannot speak.
Pre-registered reading: the pages are called balanced only if, on a statistic with separation >= 3,
the observed value lies below A's 1st percentile and within B's or C's central 95 %.
Usage: .venv/bin/python -I src/dispersion.py
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model

lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 2]
rng = np.random.default_rng(29)
W, STRIDE, REPS, SOFT = 50, 25, 200, 0.81


def wchi(X, w, stride):
    vals = []
    for s in range(0, len(X) - w + 1, stride):
        h = np.bincount(X[s:s + w], minlength=N); e = w / N
        vals.append(((h - e) ** 2 / e).sum())
    return vals


def stats_of(C):
    D = (C[1:] - C[:-1]) % N
    return dict(S1_D50=wchi(D, 50, 25), S2_C29=wchi(C, 29, 15), S2_C58=wchi(C, 58, 29))


def key_A(n): return rng.integers(0, N, size=n)
def key_B(n):
    out = []
    while len(out) < n: out += list(rng.permutation(N))
    return np.array(out[:n])
def key_C(n, m=6, q=0.5):
    out = []
    while len(out) < n:
        k = int(rng.integers(0, N))
        if k in out[-m:] and rng.random() < q: continue
        out.append(k)
    return np.array(out)


def encrypt_soft(P, keyfun):
    K = keyfun(len(P) * 3 + 60); C, j, prev = [], 0, None
    for p in P:
        c = (p + K[j]) % N
        while prev is not None and c == prev and rng.random() < SOFT:
            j += 1; c = (p + K[j]) % N
        C.append(c); j += 1; prev = c
    return np.array(C)


STATS = ("S1_D50", "S2_C29", "S2_C58")
obs_all = {k: [] for k in STATS}
for C in pages:
    for k, v in stats_of(C).items(): obs_all[k] += v
obs = {k: float(np.mean(v)) for k, v in obs_all.items()}
obs_dbl = sum(int((C[1:] == C[:-1]).sum()) for C in pages)
rows = {}
for name, kf in (("A iid + soft re-draw", key_A), ("B permutation bag + soft re-draw", key_B), ("C recent-avoid + soft re-draw", key_C)):
    means = {k: [] for k in STATS}; dbls = []
    for r in range(REPS):
        acc = {k: [] for k in STATS}; dbl = 0
        for C0 in pages:
            o = int(rng.integers(0, len(plain) - len(C0) - 1)); P = plain[o:o + len(C0)]
            C = encrypt_soft(P, kf); dbl += int((C[1:] == C[:-1]).sum())
            for k, v in stats_of(C).items(): acc[k] += v
        for k in STATS: means[k].append(np.mean(acc[k]))
        dbls.append(dbl)
    rows[name] = {"doublets": float(np.mean(dbls))}
    for k in STATS:
        m = np.array(means[k]); rows[name][k] = dict(mean=float(m.mean()), sd=float(m.std()), p1=float(np.percentile(m, 1)), p2_5=float(np.percentile(m, 2.5)), p97_5=float(np.percentile(m, 97.5)), z_obs=float((obs[k] - m.mean()) / m.std()))
    print(name, "doublets", round(rows[name]["doublets"]), {k: f"{rows[name][k]['mean']:.2f}±{rows[name][k]['sd']:.2f} z_obs {rows[name][k]['z_obs']:+.1f}" for k in STATS}, flush=True)

A = rows["A iid + soft re-draw"]
sep = {k: max(abs(rows[g][k]["mean"] - A[k]["mean"]) / A[k]["sd"] for g in rows if not g.startswith("A")) for k in STATS}
balanced = any(sep[k] >= 3 and obs[k] < A[k]["p1"] and any(rows[g][k]["p2_5"] <= obs[k] <= rows[g][k]["p97_5"] for g in rows if not g.startswith("A")) for k in STATS)
powered = [k for k in STATS if sep[k] >= 3]
out = ["# Windowed dispersion: do the pages show a hand's local balancing?", "",
       f"S1: mean chi-square (28 dof) of the 29 difference classes over 50-rune windows of D = C_i − C_{{i−1}}; S2: the same on the ciphertext itself over 29- and 58-rune windows. All 55 pages; {REPS} replicates per generator, solved-page English at the real page lengths, soft re-draw {SOFT}. Observed doublets {obs_dbl}.", "",
       "| statistic | observed | A iid (mean ± sd) | B bag | C recent-avoid | separation A vs B/C (sd) | observed z vs A |", "|---|---|---|---|---|---|---|"]
for k in STATS:
    out.append(f"| {k} | {obs[k]:.2f} | {A[k]['mean']:.2f} ± {A[k]['sd']:.2f} | {rows['B permutation bag + soft re-draw'][k]['mean']:.2f} | {rows['C recent-avoid + soft re-draw'][k]['mean']:.2f} | {sep[k]:.1f} | {A[k]['z_obs']:+.1f} |")
out += ["", f"Statistics with power (separation ≥ 3 sd): {', '.join(powered) if powered else 'none'}.", "",
        f"**Reading (pre-registered rule): {'the pages ARE locally balanced' if balanced else ('no local balancing on the powered statistic(s)' if powered else 'NO VERDICT: neither statistic separates a balanced key from an iid key through the plaintext')}.**",
        "", "S1 was the note's proposal; it has no power because a key's local balance does not carry into its successive differences. S2 was added after that was seen and before its observed value was read. "
        "Where a statistic has power, the observed value is compared with generator A's 1st percentile and the balancing generators' central 95 %. A balancing weaker than generator C would not be visible on any of these.", ""]
(RESULTS / "dispersion.md").write_text("\n".join(out) + "\n")
json.dump(dict(observed=obs, doublets=obs_dbl, generators=rows, separation=sep, powered=powered, balanced=bool(balanced)), open(RESULTS / "dispersion.json", "w"), indent=1)
print("\n".join(out[-5:]))
