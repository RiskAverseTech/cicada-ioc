"""The autokey instrument (results/autokey_registration.md): the generator inverts, literal-F is reserved, and two key
sources mean what the registration says."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"; os.environ.setdefault("STAGE", "none")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import autokey_lane as A

PAGE = (np.array([18, 4, 15, 16, 0, 24, 9, 23, 8, 18, 4, 18, 0, 1, 16]), np.array([0] * 4 + [1] * 5 + [2] * 6))   # "ERST" "FANDH" "EREFUT"


def test_every_member_round_trips_with_and_without_literal_f():
    rng = np.random.default_rng(1); P, W = PAGE
    for mi in range(len(A.MEMBERS)):
        for lf in (False, True):
            pr = (mi, 0.0, "none", lf); C = A.write_page(P, W, pr, rng)
            assert np.array_equal(A.decode_page(C, W, pr), P), A.label(pr)
            if lf: assert ((C == 0) == (P == 0)).all(), A.label(pr)                 # a written F is a plaintext F and nothing else


def test_previous_word_keys_the_next_word_forward_and_cycled():
    P, W = PAGE; pr = (A.MEMBERS.index(("W", "plain", "fwd", "add")), 0.0, "none", False)
    C = A.write_page(P, W, pr, np.random.default_rng(0))
    assert (C[:4] == P[:4]).all()                                                  # the first word is keyed by the primer F
    key = P[:4]; assert all(C[4 + j] == (P[4 + j] + key[j % 4]) % 29 for j in range(5))   # the second by the first, cycled


def test_after_s_switches_the_source_for_the_rest_of_the_word():
    P, W = PAGE; pr = (A.MEMBERS.index(("T", "two", ("afterS", "word", "AB"), "add")), 0.0, "none", False)
    C = A.write_page(P, W, pr, np.random.default_rng(0))
    # first word E R S T: E keyed by the primer, R by plaintext E, S by plaintext R; S is written at index 2 only if (p + k) == 15
    assert C[0] == P[0] and C[1] == (P[1] + P[0]) % 29 and C[2] == (P[2] + P[1]) % 29
    written_s = [i for i in range(len(C)) if C[i] == 15]
    for i in written_s:                                                            # the rune after a written S, inside the word, takes the previous cipher rune
        if i + 1 < len(C) and W[i + 1] == W[i]: assert C[i + 1] == (P[i + 1] + C[i]) % 29


def test_family_counts_match_the_registration():
    assert len(A.MEMBERS) == 183 and len(A.PROCS) == 1464 and len(A.DECODERS) == 732
    assert sum(1 for m in A.MEMBERS if m[0] == "W") == 18 and sum(1 for m in A.MEMBERS if m[0] == "T") == 51
