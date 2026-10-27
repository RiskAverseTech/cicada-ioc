"""Verdict check: can the four page statistics plus lag-2 repeats separate the mechanisms a
Quorum panel (quorumsays.com/q/8gvLyrvHouBK, 2026-10-26) called equivalent?

Each construction enciphers solved-page English cut to the 55 real page lengths, R replicates,
and is scored on doublets, lag-2 repeats, non-zero lag-1 difference chi2 (27 dof), unigram chi2
(28 dof) and IC, against the unsolved pages.  Usage: python -I src/verdict_check.py [R]
Writes results/verdict_check.md.
"""
import json, sys, numpy as np
R = int(sys.argv[1]) if len(sys.argv) > 1 else 200
N = 29
d = json.load(open('data/processed/pages.json'))
allC = [np.array(p['cipher'], int) for p in d['unsolved']]
allC = [C for C in allC if len(C) > 2]            # LP2-50 is image-only
lens = [len(C) for C in allC]
pt = []
for p in d['solved']:
    for k in ('plain', 'plaintext', 'P'):
        if k in p: pt += list(p[k]); break
pt = np.array(pt, int)

def stats(pages):
    dbl = sum(int((C[1:] == C[:-1]).sum()) for C in pages)
    l2 = sum(int((C[2:] == C[:-2]).sum()) for C in pages)
    diff = np.concatenate([(C[1:] - C[:-1]) % N for C in pages]); h = np.bincount(diff, minlength=N)[1:]; e = h.sum() / 28
    chi1 = ((h - e) ** 2 / e).sum()
    u = np.bincount(np.concatenate(pages), minlength=N); eu = u.sum() / N; chiu = ((u - eu) ** 2 / eu).sum()
    n = u.sum(); ic = (u * (u - 1)).sum() / (n * (n - 1))
    return np.array([dbl, l2, chi1, chiu, ic])

obs = stats(allC)
rng = np.random.default_rng(1)

def plaintext_pages():
    P = np.roll(pt, -rng.integers(0, len(pt))); out = []; i = 0
    for L in lens:
        if i + L > len(P): P = np.roll(pt, -rng.integers(0, len(pt))); i = 0
        out.append(P[i:i + L]); i += L
    return out

def enc_iid(P): return (P + rng.integers(N, size=len(P))) % N

def enc_hard(P):                      # uniform key re-drawn until the ciphertext does not repeat
    C = np.empty(len(P), int); prev = -1
    for i, x in enumerate(P):
        c = (x + rng.integers(N)) % N
        while c == prev: c = (x + rng.integers(N)) % N
        C[i] = c; prev = c
    return C

def enc_soft(P, p=0.81):              # phase 2 survivor: the re-draw is applied 81% of the time
    C = np.empty(len(P), int); prev = -1
    for i, x in enumerate(P):
        c = (x + rng.integers(N)) % N
        if c == prev and rng.random() < p:
            while c == prev: c = (x + rng.integers(N)) % N
        C[i] = c; prev = c
    return C

def enc_sticky_hardskip(P, s):        # key copies its previous symbol w.p. s; one hard skip on collision
    L = len(P) * 3; K = np.empty(L, int); K[0] = rng.integers(N)
    for j in range(1, L): K[j] = K[j - 1] if rng.random() < s else rng.integers(N)
    C = np.empty(len(P), int); prev = -1; j = 0
    for i, x in enumerate(P):
        c = (x + K[j]) % N; j += 1
        if c == prev: c = (x + K[j]) % N; j += 1
        C[i] = c; prev = c
    return C

def enc_hard_nulls(P, q):             # hard rule, then a uniform null after each rune w.p. q; cut to page length
    out = []; prev = -1
    for x in P:
        c = (x + rng.integers(N)) % N
        while c == prev: c = (x + rng.integers(N)) % N
        out.append(c); prev = c
        if rng.random() < q: out.append(int(rng.integers(N))); prev = out[-1]
    return np.array(out[:len(P)], int)

CONS = [
    ("independent uniform key (control)", enc_iid),
    ("hard rule: never repeat", enc_hard),
    ("soft re-draw, 81% (phase 2 survivor, (a))", enc_soft),
    ("hard rule + 10% uniform nulls ((c) as the verdict stated it)", lambda P: enc_hard_nulls(P, 0.10)),
    ("hard rule + 20% uniform nulls", lambda P: enc_hard_nulls(P, 0.20)),
    ("hard rule + 22% uniform nulls", lambda P: enc_hard_nulls(P, 0.22)),
    ("sticky key s = 0.08, hard skip once", lambda P: enc_sticky_hardskip(P, 0.08)),
    ("sticky key s = 0.17, hard skip once (GPT's (b))", lambda P: enc_sticky_hardskip(P, 0.17)),
]
rows = []
for name, f in CONS:
    S = np.array([stats([f(P) for P in plaintext_pages()]) for _ in range(R)])
    m = S.mean(0); sd = S.std(0); z = (obs - m) / np.where(sd > 0, sd, np.nan)
    rows.append((name, m, sd, z))
    print(f"{name:62s} doublets {m[0]:4.0f}±{sd[0]:2.0f}  lag2 {m[1]:4.0f}±{sd[1]:2.0f}  diff-chi2 {m[2]:5.1f}±{sd[2]:4.1f}  uni-chi2 {m[3]:4.1f}±{sd[3]:3.1f}", flush=True)

diff = (pt[1:] - pt[:-1]) % N; h = np.bincount(diff, minlength=N)[1:]; e = h.sum() / 28
ptchi = ((h - e) ** 2 / e).sum()

def cell(m, sd, z): return f"{m:.0f} ± {sd:.0f} ({z:+.1f})" if np.isfinite(z) else f"{m:.0f} ± {sd:.0f}"
out = ["# Verdict check: are the panel's mechanisms really equivalent?", "",
       "A Quorum panel (quorumsays.com/q/8gvLyrvHouBK, 2026-10-26) was asked what mechanism produces a homogeneous 19% leak "
       "in an anti-repeat rule, and answered that a soft keep constant, a hard rule plus about 10% uniform nulls, and a hard rule "
       "over a memoryless sticky key are equivalent on every statistic listed, and that lag-2 repeats (hard-rule expectation about 463) "
       "are the one discriminator. This file checks both claims by simulation: solved-page English cut to the 55 real page lengths, "
       f"{R} replicates per construction, scored against the unsolved pages. z = (observed − mean) / sd.", "",
       f"Observed: doublets {obs[0]:.0f}, lag-2 repeats {obs[1]:.0f}, non-zero lag-1 difference chi² {obs[2]:.1f} (27 dof), unigram chi² {obs[3]:.1f} (28 dof), IC {obs[4]:.4f}.", "",
       "| construction | doublets (z) | lag-2 repeats (z) | lag-1 difference chi² (z) | unigram chi² (z) |", "|---|---|---|---|---|"]
for name, m, sd, z in rows:
    out.append(f"| {name} | {cell(m[0], sd[0], z[0])} | {cell(m[1], sd[1], z[1])} | {cell(m[2], sd[2], z[2])} | {cell(m[3], sd[3], z[3])} |")
out += ["", "## Reading", "",
        "- **Not equivalent.** Hard rule plus 10% nulls, the rate the verdict named, gives about half the observed doublets (each null opens one "
        "chance adjacency, so the rate must be about 22% to reach 86). A sticky key at the rate that gives 86 doublets (s ≈ 0.17) raises the "
        "lag-1 difference chi² to about 72, two sigma above the observed 42: the key's repeats put a 0.17-weighted copy of the plaintext "
        f"difference distribution (chi² {ptchi:.0f} on 27 dof over {h.sum()} solved pairs, about {ptchi * 12901 / h.sum():.0f} at page length) into the ciphertext differences. "
        "A sticky rate low enough to keep the differences flat (s ≈ 0.08) gives only about 49 doublets. No single sticky rate fits both.",
        "- **Lag-2 does not discriminate.** Every construction, including the independent key, lands within about one sigma of the observed 435; "
        "the hard-rule expectation is 459 ± 20, not 463, and 435 does not reject it. The verdict's other suggested test, runes per page against a "
        "solved-page norm, is not a test: page density is typesetting and nulls do not change how many runes fit a page.",
        "- **What survives.** The soft re-draw and hard-rule-plus-about-22%-nulls both fit every column. The observed lag-1 difference chi² of 42 sits "
        "about two sigma above every flat model and about two sigma below the sticky model, the same faint excess phase 2 noted, now bracketed from both sides.",
        "", f"Script: `src/verdict_check.py` ({R} replicates, seed 1)."]
open('results/verdict_check.md', 'w').write("\n".join(out) + "\n")
print("wrote results/verdict_check.md")
