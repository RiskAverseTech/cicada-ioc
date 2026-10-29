"""Tests added 2026-10-29 for the three defects found by the second external review (README §56):
the n-gram model's lower orders, the standalone R4n rule, and the K-fixed sampler's clock."""
import itertools, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np


def test_ngram_lower_orders_see_their_context():
    from ngram import KN
    s = np.array([0, 1] * 400 + [2, 3] * 400)                 # the previous rune determines the next one
    m = KN(order=5).fit(s)
    u = m.prob_vec(())
    # before the fix every context shorter than four runes returned exactly the unigram vector; Kneser-Ney's
    # continuation counts are type counts, so on this stream the lower orders move the mass but do not saturate
    for ctx in ((0,), (1, 0), (0, 1, 0)):                      # measured 0.31, 0.48, 0.61 against a unigram 0.077
        p = m.prob_vec(ctx); assert p[1] > 2 * u[1] and p[3] < u[3], (ctx, p[1], u[1])
    p = m.prob_vec((2,)); assert p[3] > 2 * u[3] and p[1] < u[1]
    assert m.prob_vec((1, 0, 1, 0))[1] > 0.9                   # the top order uses raw counts and does saturate


def test_standalone_r4n_inserts_fillers():
    import mechanism_lane as ML
    ML.rng = np.random.default_rng(7); a = ML.simulate("R4")
    ML.rng = np.random.default_rng(7); b = ML.simulate("R4n")
    assert any(not np.array_equal(x[0], y[0]) for x, y in zip(a, b)), "R4n produced the same ciphertext as R4"


def _visit_counts(step, n_iter, thin, rng):
    from kfixed import doublets
    base = np.array([0, 0, 1, 2, 3]); k = doublets(base)        # 24 arrangements with one adjacent repeat, connected under single swaps
    states = sorted({tuple(p) for p in itertools.permutations(base.tolist()) if doublets(np.array(p)) == k})
    counts = {s: 0 for s in states}; c = base.copy()
    for _ in range(n_iter):
        step(c, thin, rng); counts[tuple(c.tolist())] += 1
    obs = np.array([counts[s] for s in states]); e = obs.sum() / len(states)
    return float(((obs - e) ** 2 / e).sum()), len(states)


def test_kfixed_sampler_is_uniform_on_a_small_case():
    from kfixed import kfixed_step, kfixed_step_accepted_clock
    chi_new, nstates = _visit_counts(kfixed_step, 30000, 6, np.random.default_rng(3))
    chi_old, _ = _visit_counts(kfixed_step_accepted_clock, 30000, 6, np.random.default_rng(3))
    # 30,000 correlated draws over 24 arrangements: the attempt clock sits near chi-square's mean of 23 (measured 20-27);
    # the accepted-only clock weights arrangements by their acceptance rate and lands near 100
    assert chi_new < 2.5 * nstates, (chi_new, nstates)
    assert chi_old > 2.5 * chi_new, (chi_old, chi_new)
