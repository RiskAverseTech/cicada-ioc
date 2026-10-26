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


def decode(C, Ks, lu, f_rule=False, mode="sub", adv_mask=None, null_mask=None, penalty=0.0, rejection="one"):
    """C: (n,) ciphertext; Ks: (m, L) keystreams, L >= n + S_MAX.
    mode "sub": P = C - K (additive cipher C = P + K); mode "beaufort": P = K - C (C = K - P).
    For C = P - K pass -K with mode "sub".  The forced-skip condition C_i - C_{i-1} == K_j - K_{j-1}
    is the same under both modes (a skipped key symbol would have reproduced C_{i-1}).
    State t = (key index j) - i + T0, where T0 = number of ᚠ in C (a literal F consumes no key,
    so j - i can go as low as -T0).  Transitions at a non-ᚠ position: stay (no skip) or skip
    (t+1, only where C_i - C_{i-1} == K_{j} - K_{j-1}).  At a ᚠ position with the F rule: also
    'literal F' (t-1, plaintext F, no key consumed).  Viterbi on unigram English log-likelihood.
    Word-edge events (phase 6): adv_mask[i] True allows one extra key advance before rune i
    (t+1 without the collision condition); null_mask[i] True allows rune i to be an unencrypted
    uniform null that consumes no key (t-1, gain 0).  Each event costs `penalty` (log prior).
    rejection "one" (default): a rejected key draw advances the key by one (phase 3 rule), with the
    doubled-letter double skip.  rejection "two" (phase 7, wazar's skip_by_two): a rejection advances
    the key by two, the first draw having collided (C_i - C_{i-1} == K_j - K_{j-2}) and the second
    draw unconstrained; the single-advance skip is not available in that mode.
    Returns best LLR (m,), best final state (m,), decoded plaintext along the best path (m, n)."""
    C = np.asarray(C); m, L = Ks.shape; n = len(C)
    T0 = (int((C == 0).sum()) if f_rule else 0) + (int(np.asarray(null_mask).sum()) if null_mask is not None else 0)  # room for j < i
    S = T0 + S_MAX + 1
    NEG = -1e9
    dp = np.full((m, S), NEG); dp[:, T0] = 0.0
    back = np.zeros((n, m, S), dtype=np.int8)          # 0 stay, 1 skip or extra advance (from t-1), 2 double skip (from t-2), -1 literal F, -3 uniform null (from t+1)
    rows = np.arange(m)
    jbase = np.arange(S) - T0                            # j = i + jbase[t]
    gF = lu[0] - LOGU
    for i in range(n):
        c = C[i]
        j = np.clip(i + jbase, 0, L - 1)
        Kj = Ks[:, j]
        P = ((c - Kj) if mode == "sub" else (Kj - c)) % N
        gain = lu[P] - LOGU
        stay = dp + gain
        cand = stay; src = np.zeros((m, S), dtype=np.int8)
        if i > 0 and rejection == "one":
            Kprev = Ks[:, np.clip(j - 1, 0, L - 1)]
            cond = ((c - C[i - 1]) - (Kj - Kprev)) % N == 0
            skip = np.full((m, S), NEG)
            skip[:, 1:] = np.where(cond[:, 1:], dp[:, :-1] + gain[:, 1:], NEG)
            take = skip > cand
            cand = np.where(take, skip, cand); src = np.where(take, 1, src)
            # double skip: two consecutive key symbols both would have reproduced C_{i-1},
            # which requires K_{j-2} == K_{j-1} (doubled key letters, common in phrase keys)
            Kprev2 = Ks[:, np.clip(j - 2, 0, L - 1)]
            cond2 = cond & (Kprev == Kprev2)
            skip2 = np.full((m, S), NEG)
            skip2[:, 2:] = np.where(cond2[:, 2:], dp[:, :-2] + gain[:, 2:], NEG)
            take = skip2 > cand
            cand = np.where(take, skip2, cand); src = np.where(take, 2, src)
        elif i > 0 and rejection == "two":
            # skip_by_two: the rejected draw K_{j-2} would have reproduced C_{i-1}; K_{j-1} was
            # discarded unread; K_j is the symbol used.  Same condition under both modes.
            Kprev2 = Ks[:, np.clip(j - 2, 0, L - 1)]
            cond2 = ((c - C[i - 1]) - (Kj - Kprev2)) % N == 0
            skip2 = np.full((m, S), NEG)
            skip2[:, 2:] = np.where(cond2[:, 2:], dp[:, :-2] + gain[:, 2:], NEG)
            take = skip2 > cand
            cand = np.where(take, skip2, cand); src = np.where(take, 2, src)
        if f_rule and c == 0:
            lit = np.full((m, S), NEG)
            lit[:, :-1] = dp[:, 1:] + gF                 # j unchanged while i advances: t decreases by one
            take = lit > cand
            cand = np.where(take, lit, cand); src = np.where(take, -1, src)
        if adv_mask is not None and i > 0 and adv_mask[i]:
            adv = np.full((m, S), NEG)
            adv[:, 1:] = dp[:, :-1] + gain[:, 1:] + penalty   # extra key advance, no collision needed
            take = adv > cand
            cand = np.where(take, adv, cand); src = np.where(take, 1, src)
        if null_mask is not None and i > 0 and null_mask[i]:
            nul = np.full((m, S), NEG)
            nul[:, :-1] = dp[:, 1:] + penalty                # uniform null: gain 0, no key consumed
            take = nul > cand
            cand = np.where(take, nul, cand); src = np.where(take, -3, src)
        dp = cand; back[i] = src
    best = dp.max(1); t_best = dp.argmax(1)
    out = np.zeros((m, n), dtype=np.int16); t = t_best.copy()
    for i in range(n - 1, -1, -1):
        c = C[i]
        src = back[i][rows, t]
        j = np.clip(i + (t - T0), 0, L - 1)
        Kj = Ks[rows, j]
        dec = ((c - Kj) if mode == "sub" else (Kj - c)) % N
        out[:, i] = np.where(src == -1, 0, np.where(src == -3, c, dec))   # a null is written as itself
        t = t - (src == 1) - 2 * (src == 2) + (src == -1) + (src == -3)
    return best, t_best - T0, out


def bigram_llr(P, lu, lb):
    return float(lu[P[0]] - LOGU + (lb[P[:-1], P[1:]] - LOGU).sum())


def null_scores(C, lu, f_rule, rng, reps=2000, mode="sub", rejection="one"):
    Ks = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2))
    best, _, _ = decode(C, Ks, lu, f_rule, mode, rejection=rejection)
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
