"""Rune-level n-gram English model for rescoring (2026-10-27).  Interpolated Kneser-Ney, order 5,
trained on the running-key corpus's book-digraph transliterations (data/corpus/corpus.json, every
text, about 1.4 million runes) with the solved Liber Primus plaintext held out for evaluation.
The decoder keeps its unigram Viterbi (the search needs a memoryless score); this model rescores
decoded candidates, where it is a far sharper judge of English on 60-160 runes than letter
frequencies.  Scores are log-probabilities in nats per rune; `score(P)` returns the total.
Usage: .venv/bin/python -I src/ngram.py   (trains, reports held-out perplexity, caches results/ngram5.npz)
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, RESULTS, PROCESSED

ORDER = 5
CACHE = RESULTS / "ngram5.npz"


class KN:
    def __init__(self, order=ORDER, d=0.75):
        self.order, self.d = order, d
        self.counts = [dict() for _ in range(order + 1)]      # counts[k][context tuple] -> array(N)
        self.cont = [dict() for _ in range(order + 1)]        # continuation counts for lower orders

    def fit(self, stream):
        s = np.asarray(stream); o = self.order
        for k in range(1, o + 1):
            ctx_len = k - 1; tbl = self.counts[k]
            for i in range(ctx_len, len(s)):
                ctx = tuple(s[i - ctx_len:i]) if ctx_len else ()
                a = tbl.get(ctx)
                if a is None: a = tbl[ctx] = np.zeros(N)
                a[s[i]] += 1
        # continuation counts: number of distinct left contexts in which (ctx, w) appears
        for k in range(1, o):
            cont = self.cont[k]
            for ctx, a in self.counts[k + 1].items():
                sub = ctx[1:]
                c = cont.get(sub)
                if c is None: c = cont[sub] = np.zeros(N)
                c[a > 0] += 1
        self.uni_cont = self.cont[1].get((), np.ones(N))
        return self

    def prob_vec(self, ctx):
        """P(w | ctx) for all w, interpolated KN; ctx a tuple of up to order-1 runes."""
        p = (self.uni_cont + 0.5) / (self.uni_cont.sum() + 0.5 * N)
        for k in range(2, self.order + 1):
            c = tuple(ctx[-(k - 1):]) if k - 1 <= len(ctx) else None
            if c is None or len(c) < k - 1: break
            tbl = self.counts[k] if k == self.order else self.cont[k - 1]
            a = tbl.get(c)
            if a is None: continue
            tot = a.sum()
            if tot == 0: continue
            lam = self.d * (a > 0).sum() / tot
            p = np.maximum(a - self.d, 0) / tot + lam * p
        return p

    def score(self, P):
        P = [int(x) for x in P]; tot = 0.0
        for i in range(len(P)):
            tot += np.log(self.prob_vec(tuple(P[max(0, i - self.order + 1):i]))[P[i]])
        return tot


def train(verbose=True):
    corpus = json.loads((Path(__file__).resolve().parent.parent / "data" / "corpus" / "corpus.json").read_text())
    stream = np.concatenate([np.array(v["runes"]) for v in corpus.values()])
    t0 = time.time(); m = KN().fit(stream)
    d = json.loads((PROCESSED / "pages.json").read_text()); held = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
    ll = m.score(held); uni = -np.log(N) * len(held)
    if verbose: print(f"trained on {len(stream):,} runes in {time.time()-t0:.0f}s; held-out solved plaintext {len(held)} runes: {ll/len(held):.3f} nats/rune (uniform {-np.log(N):.3f}); random-rune baseline check: {m.score(np.random.default_rng(0).integers(0, N, 500))/500:.3f}")
    return m


if __name__ == "__main__":
    train()


# ---------- dense tables for vectorised batch scoring ----------
def dense_tables(m):
    """log P(w | ctx) as dense arrays T[k] of shape (N,)*k + (N,), k = 0..order-1, built from the KN model."""
    import itertools
    T = []
    for k in range(m.order):
        arr = np.empty((N,) * k + (N,))
        for ctx in itertools.product(range(N), repeat=k):
            arr[ctx] = np.log(m.prob_vec(ctx))
        T.append(arr)
    return T


def load_dense():
    if CACHE.exists():
        z = np.load(CACHE); return [z[f"T{k}"] for k in range(ORDER)]
    m = train(verbose=False); T = dense_tables(m)
    np.savez(CACHE, **{f"T{k}": t for k, t in enumerate(T)}); return T


def score_batch(P, T):
    """P: (m, n) int array of decoded runes -> (m,) total log-probability under the dense 5-gram tables."""
    P = np.asarray(P); m, n = P.shape; out = np.zeros(m)
    for i in range(n):
        k = min(i, len(T) - 1)
        idx = tuple(P[:, i - k + j] for j in range(k)) + (P[:, i],)
        out += T[k][idx]
    return out
