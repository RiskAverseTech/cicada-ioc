"""Encoder/decoder consistency under the hard anti-repeat rule when the key has runs of identical
symbols (2026-10-27, after external review).  A hard rule rejects key symbols until the rune differs
from the previous one, so a run of k equal key symbols that all collide forces k rejections at one
position; the decoder before this date could take at most two.  Writes results/skip_consistency.md.
Usage: .venv/bin/python -I src/test_skip.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, english_model, S_MAX, MAX_SKIP
from skip_decrypt import encrypt, combine
import families as F

lu, lb, plain = english_model()
rng = np.random.default_rng(11)
out = ["# Decoder consistency under runs of identical key symbols", ""]


def encrypt_track(P, K, f_rule, sign):
    """Hard rule; returns ciphertext and the largest number of consecutive rejections at one position."""
    C, j, prev, worst = [], 0, None, 0
    for p in P:
        if f_rule and p == 0:
            C.append(0); prev = 0; continue
        c = combine(p, K[j], sign); k = 0
        while prev is not None and c == prev:
            j += 1; k += 1; c = combine(p, K[j], sign)
        worst = max(worst, k); C.append(c); j += 1; prev = c
    return np.array(C), worst


# 1. the reviewer's minimal case
P = np.array([5, 6]); K = np.array([2, 1, 1, 1, 2] + list(np.arange(60) % 29)); C = encrypt(P, K)
lu_bias = lu.copy(); lu_bias[6] = np.log(0.9); lu_bias[7] = np.log(0.001)
out += ["## 1. Minimal case (plaintext [5, 6], key 2 1 1 1 2 ..., three rejections at the second rune)", "",
        "| decoder max_skip | decode, English unigrams | decode, unigrams biased to rune 6 | path with 3 rejections reachable |", "|---|---|---|---|"]
for ms in (2, 3, 4):
    d1 = decode(C, K[None, :], lu, max_skip=ms)[2][0]; d2 = decode(C, K[None, :], lu_bias, max_skip=ms)[2][0]
    out.append(f"| {ms} | {d1.tolist()} | {d2.tolist()} | {'yes' if (d2 == P).all() else 'no'} |")
out += ["", "With max_skip 2 the correct path does not exist in the decoder.  With max_skip >= 3 it exists; on a two-rune text the unigram "
        "model still prefers rune 7 to rune 6 (both decodes are valid encryptions), which is a tie-break, not a coverage gap.", ""]

# 2. English plaintext, keys with injected runs, all signs, both F variants
TRIALS, n = 240, 160
out += ["## 2. English plaintext (160 runes), hard rule, keys with injected runs of equal symbols", "",
        "Runs injected by copying the previous key symbol with probability r. 240 trials per r, signs and F variants cycled; "
        "'needs >= 3' is the share of plants where the true path has a position with three or more rejections.", "",
        "| r | plants needing >= 3 rejections | exact recovery, max_skip 2 | max_skip 4 | max_skip 6 | mean recovery 2 / 4 / 6 |", "|---|---|---|---|---|---|"]
for r in (0.0, 0.05, 0.15):
    need, exact, acc = 0, {2: 0, 4: 0, 6: 0}, {2: [], 4: [], 6: []}
    for t in range(TRIALS):
        sign = ("sub", "add", "beaufort")[t % 3]; mode = "beaufort" if sign == "beaufort" else "sub"; f_rule = bool((t // 3) % 2)
        K = rng.integers(0, N, size=n + S_MAX + 8)
        for i in range(1, len(K)):
            if rng.random() < r: K[i] = K[i - 1]
        o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
        C, worst = encrypt_track(P, K, f_rule, sign); need += worst >= 3
        Kd = K if sign != "add" else (-K) % N
        for ms in (2, 4, 6):
            dec = decode(C, Kd[None, :], lu, f_rule, mode, max_skip=ms)[2][0]
            exact[ms] += bool((dec == P).all()); acc[ms].append(float((dec == P).mean()))
    out.append(f"| {r} | {need/TRIALS:.3f} | {exact[2]/TRIALS:.3f} | {exact[4]/TRIALS:.3f} | {exact[6]/TRIALS:.3f} | {np.mean(acc[2]):.3f} / {np.mean(acc[4]):.3f} / {np.mean(acc[6]):.3f} |")
out.append("")

# 3. how often the book's key families contain runs of three or more equal symbols
out += ["## 3. Runs of three or more equal symbols in the repository's key library", "",
        "Counted over the first 327 symbols of every key (the decoder's reach on the longest page).", "",
        "| family | keys | keys with a run >= 3 | runs >= 3 per 1,000 symbols | longest run |", "|---|---|---|---|---|"]
seen = set()
for sign, mode, Ks, labs in F.ALLSETS:
    for fam in sorted({f for f, _ in labs}):
        if fam in seen: continue
        seen.add(fam)
        idx = [i for i, (f, _) in enumerate(labs) if f == fam]; M = Ks[idx]
        eq = (M[:, 1:] == M[:, :-1])
        runs3, longest, any3 = 0, 1, 0
        for row in eq:
            L_, best, cnt = 1, 1, 0
            for e in row:
                L_ = L_ + 1 if e else 1
                if L_ == 3: cnt += 1
                best = max(best, L_)
            runs3 += cnt; longest = max(longest, best); any3 += cnt > 0
        out.append(f"| {fam} | {len(idx)} | {any3} | {1000*runs3/(len(idx)*M.shape[1]):.2f} | {longest} |")
out += ["", f"Decoder default is now max_skip = {MAX_SKIP}. Every sweep before 2026-10-27 ran with max_skip = 2; a key needing three or more "
        "rejections at one position lost that position and, under the soft rule, the following ones until the paths re-synchronised.", ""]
(RESULTS / "skip_consistency.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
