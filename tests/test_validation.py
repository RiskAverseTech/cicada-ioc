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


def test_e56w_n_has_fillers_and_spend_repair():
    import mechanism_lane as ML
    ML.rng = np.random.default_rng(11); a = ML.simulate("E56w")
    ML.rng = np.random.default_rng(11); b = ML.simulate("E56w+n")
    assert any(not np.array_equal(x[0], y[0]) for x, y in zip(a, b)), "E56w+n produced the same ciphertext as E56w"
    ML.rng = np.random.default_rng(11); c = ML.simulate("E56w+R4n")
    assert any(not np.array_equal(x[0], y[0]) for x, y in zip(b, c)), "E56w+n produced the same ciphertext as E56w+R4n"


def _wc_fixture(seed=5):
    import numpy as np, families as F
    from lp import english_to_runes
    rng = np.random.default_rng(seed)
    text = ("the pilgrim set out at dawn with nothing but a staff and the memory of a voice that had told him the road would be long and the gate narrow and he walked until the hills were behind him and the river lay ahead like a question he could not yet answer and still he walked because stopping was the one thing he had promised never to do")
    words = [np.array(english_to_runes(w)) for w in text.split()]
    P, wid = np.concatenate(words), np.concatenate([np.full(len(w), k) for k, w in enumerate(words)])
    return rng, words, P, wid, F.lu


def test_wc_decoder_equals_plain_without_nulls():
    import numpy as np
    from score import decode, S_MAX
    from wc_decode import decode_wc, word_starts
    rng, words, P, wid, lu = _wc_fixture()
    Ks = rng.integers(0, 29, size=(40, len(P) + S_MAX + 2)); C = (P + Ks[0, :len(P)]) % 29
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            a = decode(C, Ks, lu, f_rule, mode)[0]; b = decode_wc(C, Ks, lu, word_starts(wid), f_rule, mode, allow_null=False)[0]
            assert np.allclose(a, b), (f_rule, mode)


def test_wc_decoder_equals_free_null_when_every_rune_is_a_word():
    import numpy as np
    from score import decode, S_MAX
    from wc_decode import decode_wc
    rng, words, P, wid, lu = _wc_fixture()
    Ks = rng.integers(0, 29, size=(40, len(P) + S_MAX + 2)); C = (P + Ks[0, :len(P)]) % 29
    nm = np.ones(len(C), bool); nm[0] = False
    a = decode(C, Ks, lu, False, "sub", None, nm, -2.2)[0]; b = decode_wc(C, Ks, lu, np.ones(len(C), bool), False, "sub", -2.2)[0]
    assert np.allclose(a, b)


def test_wc_decoder_recovers_word_fillers_and_never_places_two_in_a_word():
    import numpy as np
    from score import S_MAX
    from wc_decode import decode_wc, word_starts
    rng, words, P, wid, lu = _wc_fixture()
    K = rng.integers(0, 29, size=len(P) + S_MAX + 2); C, W, real = [], [], []
    j = 0
    for k, w in enumerate(words):                                 # one filler at a uniform slot in 40 % of words, key not consumed
        slot = int(rng.integers(0, len(w) + 1)) if (len(w) >= 2 and rng.random() < 0.4) else -1
        for i, p in enumerate(w):
            if i == slot: C.append(int(rng.integers(0, 29))); W.append(k); real.append(False)
            C.append(int((p + K[j]) % 29)); W.append(k); real.append(True); j += 1
        if slot == len(w): C.append(int(rng.integers(0, 29))); W.append(k); real.append(False)
    C, W, real = np.array(C), np.array(W), np.array(real)
    Ks = np.vstack([K[None, :], rng.integers(0, 29, size=(60, len(K)))])
    best, _, out, nulls = decode_wc(C, Ks, lu, word_starts(W), False, "sub", -2.2)
    assert best.argmax() == 0, "true key not ranked first"
    assert (out[0][real] == P).mean() > 0.9
    assert nulls[0].sum() == (~real).sum(), "filler count not recovered"
    planted = {k for k in range(W.max() + 1) if (~real[W == k]).any()}; found = {k for k in range(W.max() + 1) if nulls[0][W == k].any()}
    assert len(planted & found) >= 0.75 * len(planted), "filler words not recovered"     # a unigram scorer places a filler at a word edge in the neighbouring word now and then
    for k in range(W.max() + 1): assert nulls[:, W == k].sum(1).max() <= 1, "two fillers placed in one word"


def test_table_hook_equals_plain_decoder_on_additive_tables():
    """§67's general-rule hook: with the additive table it must reproduce the plain decoder exactly, skips and literal F included."""
    import numpy as np
    from score import decode, S_MAX, LOGU
    from skip_decrypt import encrypt
    rng, words, P, wid, lu = _wc_fixture(9); N = 29
    for mode, enc in (("sub", (np.arange(N)[:, None] + np.arange(N)[None, :]) % N), ("beaufort", (np.arange(N)[None, :] - np.arange(N)[:, None]) % N)):
        table = np.zeros((N, N), int); tgain = np.zeros((N, N))
        for k in range(N):
            for p in range(N): table[enc[p, k], k] = p; tgain[enc[p, k], k] = lu[p] - LOGU
        for f_rule in (False, True):
            K = rng.integers(0, N, size=len(P) + S_MAX + 2); C = encrypt(P, K, f_rule, rng, 0.81, mode)
            Ks = np.vstack([K[None, :], rng.integers(0, N, size=(30, len(K)))])
            a, ta, da = decode(C, Ks, lu, f_rule, mode); b, tb, db = decode(C, Ks, lu, f_rule, mode, table=table, tgain=tgain, enc=enc)
            assert np.allclose(a, b) and np.array_equal(ta, tb) and np.array_equal(da, db), (mode, f_rule)
            assert a.argmax() == 0 and (da[0] == P).mean() > 0.95


def test_lattice_decoder_reads_a_short_running_key_plant_and_beats_a_random_page():
    """§69's word-lattice joint decoder: on a 15-word English plant under an English running key (sub, soft 0.81) it reads at
    least half the words and scores well above a random page with the same word structure; the recomputed key matches."""
    import os; os.environ["STAGE"] = "none"
    import numpy as np, runkey_lattice as RL
    from lp import english_to_runes
    rng = np.random.default_rng(4)
    text = "the man set out at dawn with nothing but a staff and the memory of a voice that had told him the road would be long and the gate narrow"
    pw = [np.array(english_to_runes(w)) for w in text.split()]; pw = [w for w in pw if " ".join(map(str, w)) in RL.raw][:15]
    assert len(pw) == 15
    key = "he walked until the hills were behind him and the river lay ahead like a question he could not yet answer and still he walked because stopping"
    K = np.concatenate([english_to_runes(w) for w in key.split()])
    C = RL.encrypt_words(pw, K, "sub", rng, soft=0.81)
    s, P, Kd = RL.decode_lattice(C, "sub", False, False, beam=100)
    i = 0; hits = 0
    for c, w in zip(C, pw): hits += np.array_equal(P[i:i + len(c)], w); i += len(c)
    assert hits >= 8, hits
    assert np.array_equal(Kd, RL.key_of(np.concatenate(C), P, RL.SIGNS["sub"], False))
    rw = [rng.integers(0, 29, size=len(c)) for c in C]; s0, _, _ = RL.decode_lattice(rw, "sub", False, False, beam=100)
    assert s - s0 > 15, (s, s0)                                  # measured 28 nats at 60 runes
