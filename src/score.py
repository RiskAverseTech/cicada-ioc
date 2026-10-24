"""Phase 3: English-in-runes model, DP decoder for the skip-on-repeat rule, random-key null.

Decoding a candidate keystream K under the skip rule is ambiguous at about one position in
29 (a skip is forced to satisfy C_i - C_{i-1} == K_{j+1} - K_j, but that can also hold by
chance with no skip).  The decoder keeps the number of skips so far as a state and takes
the best-scoring path (Viterbi over states, unigram English log-likelihood), which is what
a human decoder does by reading ahead.  Scores are calibrated against random keystreams
run through the same decoder, so the maximisation's optimism is in the null.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, PROCESSED, LATIN

LOGU = np.log(1 / N)
S_MAX = 48               # skips allowed per page (the pages have ~230 runes; ~81% of ~8 would-be doublets)


def english_model():
    d = json.loads((PROCESSED / "pages.json").read_text())
    plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
    uni = np.bincount(plain, minlength=N) + 0.5
    lu = np.log(uni / uni.sum())
    big = np.zeros((N, N)) + 0.5
    np.add.at(big, (plain[:-1], plain[1:]), 1)
    lb = np.log(big / big.sum(1, keepdims=True))
    return lu, lb, plain


def decode(C, Ks, lu, f_rule=False):
    """C: (n,) ciphertext; Ks: (m, L) keystreams, L >= n + S_MAX.
    State t = (key index j) - i + T0, where T0 = number of ᚠ in C (a literal F consumes no key,
    so j - i can go as low as -T0).  Transitions at a non-ᚠ position: stay (no skip) or skip
    (t+1, only where C_i - C_{i-1} == K_{j} - K_{j-1}).  At a ᚠ position with the F rule: also
    'literal F' (t-1, plaintext F, no key consumed).  Viterbi on unigram English log-likelihood.
    Returns best LLR (m,), best final state (m,), decoded plaintext along the best path (m, n)."""
    C = np.asarray(C); m, L = Ks.shape; n = len(C)
    T0 = int((C == 0).sum()) if f_rule else 0
    S = T0 + S_MAX + 1
    NEG = -1e9
    dp = np.full((m, S), NEG); dp[:, T0] = 0.0
    back = np.zeros((n, m, S), dtype=np.int8)          # 0 stay, 1 came by skip (from t-1), -1 came by literal F (from t+1)
    rows = np.arange(m)
    jbase = np.arange(S) - T0                            # j = i + jbase[t]
    gF = lu[0] - LOGU
    for i in range(n):
        c = C[i]
        j = np.clip(i + jbase, 0, L - 1)
        Kj = Ks[:, j]
        P = (c - Kj) % N
        gain = lu[P] - LOGU
        stay = dp + gain
        cand = stay; src = np.zeros((m, S), dtype=np.int8)
        if i > 0:
            Kprev = Ks[:, np.clip(j - 1, 0, L - 1)]
            cond = ((c - C[i - 1]) - (Kj - Kprev)) % N == 0
            skip = np.full((m, S), NEG)
            skip[:, 1:] = np.where(cond[:, 1:], dp[:, :-1] + gain[:, 1:], NEG)
            take = skip > cand
            cand = np.where(take, skip, cand); src = np.where(take, 1, src)
        if f_rule and c == 0:
            lit = np.full((m, S), NEG)
            lit[:, :-1] = dp[:, 1:] + gF                 # j unchanged while i advances: t decreases by one
            take = lit > cand
            cand = np.where(take, lit, cand); src = np.where(take, -1, src)
        dp = cand; back[i] = src
    best = dp.max(1); t_best = dp.argmax(1)
    out = np.zeros((m, n), dtype=np.int16); t = t_best.copy()
    for i in range(n - 1, -1, -1):
        c = C[i]
        src = back[i][rows, t]
        j = np.clip(i + (t - T0), 0, L - 1)
        out[:, i] = np.where(src == -1, 0, (c - Ks[rows, j]) % N)
        t = t - (src == 1) + (src == -1)
    return best, t_best - T0, out


def bigram_llr(P, lu, lb):
    return float(lu[P[0]] - LOGU + (lb[P[:-1], P[1:]] - LOGU).sum())


def null_scores(C, lu, f_rule, rng, reps=2000):
    Ks = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2))
    best, _, _ = decode(C, Ks, lu, f_rule)
    return best


def translit(P):
    return "".join(LATIN[int(x)] for x in P)


if __name__ == "__main__":
    from skip_decrypt import encrypt
    rng = np.random.default_rng(3301)
    lu, lb, plain = english_model()
    P = plain[300:540]
    for f_rule in (False, True):
        for soft in (1.0, 0.81):
            K = rng.integers(0, N, 400)
            C = encrypt(P, K, f_rule=f_rule, rng=rng, soft=soft)
            best, sb, out = decode(C, K[None, :], lu, f_rule)
            acc = (out[0] == P).mean()
            nulls = null_scores(C, lu, f_rule, rng, 300)
            z = (best[0] - nulls.mean()) / nulls.std()
            print(f"f_rule={f_rule} soft={soft}: recovered {acc:.3f} of runes, skips {sb[0]}, score {best[0]:.1f} vs random-key null {nulls.mean():.1f} ± {nulls.std():.1f} (z = {z:.0f})")
    print("sample:", translit(out[0][:60]))
