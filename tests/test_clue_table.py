"""The clue table's last instruments (results/clue_table_registration.md): T and N invert exactly, and the families are as registered."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"; os.environ.setdefault("STAGE", "none")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import totient_lane as T
import line_lane as Lx

PAGE = (np.array([18, 4, 15, 16, 0, 24, 9, 23, 8, 18, 4, 18, 0, 1, 16]), np.array([0] * 4 + [1] * 5 + [2] * 6), np.array([0] * 7 + [1] * 8))


def test_totient_members_invert_exactly_and_count_as_registered():
    assert len(T.MEMBERS) == 48 and len(T.PROCS) == 384 and len(T.DECODERS) == 192
    rng = np.random.default_rng(1); P, W, _ = PAGE
    for mi in range(len(T.MEMBERS)):
        for lf in (False, True):
            pr = (mi, 0.0, "none", lf); C = T.write_page(P, W, pr, rng); Pd, nf, full = T.decode_beam(C, W, pr, fillers=False)
            assert nf == 0 and np.array_equal(Pd, P), T.label(pr)


def test_totient_of_the_previous_word_keys_the_next_word():
    P, W, _ = PAGE; pr = (T.MEMBERS.index(("prevword", "phi29", "add")), 0.0, "none", False)
    C = T.write_page(P, W, pr, np.random.default_rng(0))
    assert (C[:4] == P[:4]).all()                                                          # the first word: n = 0, phi(0) = 0
    n = int(sum(T.VALUE[p] for p in P[:4])); k = T.phi(n) % 29
    assert all(C[i] == (P[i] + k) % 29 for i in range(4, 9))


def test_line_members_invert_exactly_and_the_reset_restores_the_primer():
    assert len(Lx.MEMBERS) == 78 and len(Lx.PROCS) == 624 and len(Lx.DECODERS) == 312
    rng = np.random.default_rng(1); P, W, Ln = PAGE
    for mi in range(len(Lx.MEMBERS)):
        for lf in (False, True):
            pr = (mi, 0.0, "none", lf); C = Lx.write_page(P, W, Ln, pr, rng); Pd, nf, full = Lx.decode_beam(C, W, Ln, pr, fillers=False)
            assert nf == 0 and np.array_equal(Pd, P), Lx.label(pr)
    pr = (Lx.MEMBERS.index(("reset", "plain", None, "add")), 0.0, "none", False); C = Lx.write_page(P, W, Ln, pr, np.random.default_rng(0))
    assert C[0] == P[0] and C[7] == P[7]                                                   # the first rune of each line is keyed by the primer F
    assert all(C[i] == (P[i] + P[i - 1]) % 29 for i in range(1, 7)) and all(C[i] == (P[i] + P[i - 1]) % 29 for i in range(8, 15))
