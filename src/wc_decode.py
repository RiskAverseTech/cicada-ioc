"""§61 (2026-10-29): the word-constrained filler decoder.

score.decode's free-null option lets ANY rune be an unkeyed filler at a fixed log prior; §55 found that on a wrong key over a
full page such a decoder gains about 110 nats on noise, so its margin arm did no filtering.  §59 fitted the filler form to
the word lengths: one extra rune at a uniform position in a fraction p = 0.40 of the words of two or more runes, i.e. AT MOST
ONE FILLER PER WORD.  §60 found the free-null decoder recovers more per-word plants than per-rune plants at equal filler
count (0.75 vs 0.68).  This decoder carries the constraint as state: a flag "filler already used in this word", reset at
each word start, and the null transition (rune written as itself, no key consumed, gain 0, cost `penalty`) is available only
while the flag is clear.  Everything else is score.decode under rejection "one": soft skip-on-repeat with up to max_skip
rejections, the literal-F rule, modes "sub" and "beaufort".
penalty may be a scalar or an (n,) array (a per-position log prior, e.g. ln(p/(1-p)) - ln(cipher word length) for the
§59 form at rate p).  allow_null=False reproduces score.decode exactly; word_start all True reproduces the free-null decoder.
Returns best LLR (m,), final key offset (m,), decoded plaintext along the best path (m, n), null positions (m, n) bool.
"""
import numpy as np
import score
from lp import N
from score import S_MAX, MAX_SKIP
LOGU = getattr(score, "LOGU", -np.log(N))


def word_starts(word_id):
    """word_id: (n,) ints, constant inside a word -> bool (n,) True at the first rune of each word."""
    w = np.asarray(word_id); ws = np.ones(len(w), bool); ws[1:] = w[1:] != w[:-1]; return ws


def decode_wc(C, Ks, lu, word_start, f_rule=False, mode="sub", penalty=-2.2, max_skip=MAX_SKIP, allow_null=True):
    C = np.asarray(C); Ks = np.asarray(Ks); m, L = Ks.shape; n = len(C)
    ws = np.asarray(word_start, bool); assert len(ws) == n
    pen = np.broadcast_to(np.asarray(penalty, float), (n,))
    T0 = (int((C == 0).sum()) if f_rule else 0) + (int(ws.sum()) if allow_null else 0)
    S = T0 + S_MAX + 1; NEG = -1e9
    dp = np.full((m, 2, S), NEG); dp[:, 0, T0] = 0.0
    back = np.zeros((n, m, 2, S), dtype=np.int8)        # 0 stay, k>0 rejections (from t-k), -1 literal F (from t+1), -3 filler (from t+1, flag 0 -> 1)
    coll = np.zeros((n, m, S), dtype=np.int8)           # at a word start: the flag the collapsed state was taken from
    rows = np.arange(m); jbase = np.arange(S) - T0; gF = lu[0] - LOGU
    for i in range(n):
        if ws[i] and i > 0:
            take1 = dp[:, 1, :] > dp[:, 0, :]; coll[i] = take1
            d0 = np.where(take1, dp[:, 1, :], dp[:, 0, :]); d1 = np.full((m, S), NEG)
        else:
            d0, d1 = dp[:, 0, :], dp[:, 1, :]
        c = int(C[i]); j = np.clip(i + jbase, 0, L - 1); Kj = Ks[:, j]
        P = ((c - Kj) if mode == "sub" else (Kj - c)) % N
        gain = lu[P] - LOGU
        new = np.empty_like(dp); src_all = np.zeros((m, 2, S), dtype=np.int8)
        if i > 0:
            Kprev = Ks[:, np.clip(j - 1, 0, L - 1)]; cond1 = ((c - C[i - 1]) - (Kj - Kprev)) % N == 0
        for f, d in ((0, d0), (1, d1)):
            cand = d + gain; src = np.zeros((m, S), dtype=np.int8)
            if i > 0:
                condk = cond1
                for k in range(1, max_skip + 1):
                    if k > 1: condk = condk & (Ks[:, np.clip(j - k, 0, L - 1)] == Kprev)
                    skipk = np.full((m, S), NEG)
                    skipk[:, k:] = np.where(condk[:, k:], d[:, :-k] + gain[:, k:], NEG)
                    take = skipk > cand; cand = np.where(take, skipk, cand); src = np.where(take, k, src)
            if f_rule and c == 0:
                lit = np.full((m, S), NEG); lit[:, :-1] = d[:, 1:] + gF
                take = lit > cand; cand = np.where(take, lit, cand); src = np.where(take, -1, src)
            if f == 1 and allow_null and i > 0:
                nul = np.full((m, S), NEG); nul[:, :-1] = d0[:, 1:] + pen[i]
                take = nul > cand; cand = np.where(take, nul, cand); src = np.where(take, -3, src)
            new[:, f, :] = cand; src_all[:, f, :] = src
        dp = new; back[i] = src_all
    flat = dp.reshape(m, -1); bi = flat.argmax(1); best = flat[rows, bi]
    f = bi // S; t = bi % S; t_final = t.copy()
    out = np.zeros((m, n), dtype=np.int16); nulls = np.zeros((m, n), bool)
    for i in range(n - 1, -1, -1):
        c = int(C[i]); src = back[i][rows, f, t]
        j = np.clip(i + (t - T0), 0, L - 1); Kj = Ks[rows, j]
        dec = ((c - Kj) if mode == "sub" else (Kj - c)) % N
        out[:, i] = np.where(src == -1, 0, np.where(src == -3, c, dec)); nulls[:, i] = src == -3
        t = t - np.where(src > 0, src, 0) + (src == -1) + (src == -3)
        f = np.where(src == -3, 0, f)
        if ws[i] and i > 0: f = coll[i][rows, t]
    return best, t_final - T0, out, nulls


def word_prior(word_start, p):
    """The §59 form's log prior per position: a filler in this word at this slot against no filler, ln(p/(1-p)) - ln(slots),
    slots = the cipher word's length (a word of L plaintext runes has L + 1 slots and is written with L + 1 runes)."""
    ws = np.asarray(word_start, bool); n = len(ws); wid = np.cumsum(ws) - 1; lens = np.bincount(wid)
    return np.log(p / (1 - p)) - np.log(lens[wid].astype(float))
