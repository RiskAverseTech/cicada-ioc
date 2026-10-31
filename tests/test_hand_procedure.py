"""The hand-procedure family (src/hand_procedure_lane.py, §73): every table form round-trips through its own decoder, the
exclude rule never writes the state rune, and the plain cipher-feedback chain doubles exactly where the plaintext is F."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import hand_procedure_lane as H


def _page(rng, n=240):
    P, W = [], []; w = 0
    while len(P) < n:
        word = list(H.EW[int(rng.integers(len(H.EW)))]); P += word; W += [w] * len(word); w += 1
    return np.array(P[:n]), np.array(W[:n])


def test_every_latin_table_round_trips_under_every_cipher_state():
    rng = np.random.default_rng(3); P, W = _page(rng)
    for ti in (0, 1, 2, 3, 6, 29 * 3, 202):                       # add, sub, rev, mul, and the last Latin table
        T = H.TABLES[ti][1]; assert all(len(set(T[s])) == 29 for s in range(29)); Tinv = H.invert(T)
        for st in ("c1", "p1", "c5w", "c6w", "csum"):
            for rs in ("word", "none"):
                C = H.write_page(P, W, T, None, st, rs, "none", False, rng)
                assert (H.decode_page(C, W, T, Tinv, None, st, rs, "none", False) == P).all(), (ti, st, rs)


def test_exclude_rule_never_writes_the_state_rune_and_inverts():
    rng = np.random.default_rng(4); P, W = _page(rng); T = H.TABLES[40][1]; R28 = H.excl_row(T); Tinv = H.invert(T)
    C = H.write_page(P, W, T, R28, "c1", "none", "exclude", False, rng)
    assert not (C[1:] == C[:-1]).any()                               # a cipher-feedback chain with the exclude rule has no doublets
    Pd = H.decode_page(C, W, T, Tinv, R28, "c1", "none", "exclude", False)
    assert (Pd[P != 28] == P[P != 28]).all()                         # only the plaintext index 28 is folded onto 0 by the modulo-28 read


def test_plain_chain_doubles_exactly_at_plaintext_f():
    rng = np.random.default_rng(5); P, W = _page(rng); T = H.TABLES[0][1]
    C = H.write_page(P, W, T, None, "c1", "none", "none", False, rng)
    dbl = np.flatnonzero(C[1:] == C[:-1]) + 1
    assert set(dbl) == set(np.flatnonzero(P == 0)) - {0}
