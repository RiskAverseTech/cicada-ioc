"""The three-behaviours instrument (results/behaviours_registration.md): exact inversion, the switch and the behaviours."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"; os.environ.setdefault("STAGE", "none")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import behaviours_lane as B

PAGE = (np.array([18, 4, 15, 16, 0, 24, 9, 23, 8, 18, 4, 18, 0, 1, 16]), np.array([0] * 4 + [1] * 5 + [2] * 6))


def test_every_member_inverts_exactly_without_fillers():
    rng = np.random.default_rng(1); P, W = PAGE
    for mi in range(len(B.MEMBERS)):
        for lf in (False, True):
            pr = (mi, 0.0, "none", lf); C = B.write_page(P, W, pr, rng); Pd, nf, full = B.decode_beam(C, W, pr, fillers=False)
            assert nf == 0 and np.array_equal(Pd, P) and np.array_equal(full, P), B.label(pr)
            if lf: assert ((C == 0) == (P == 0)).all(), B.label(pr)


def test_word_switch_assigns_behaviours_by_word_index():
    # state 'word', assignment (spend, hold, adhere): word 0 spends (lag: previous plaintext), word 1 holds, word 2 adheres
    P, W = PAGE; ai = B.ASSIGN.index(("spend", "hold", "adhere")); pr = (B.MEMBERS.index(("word", ai, "lag", "add")), 0.0, "none", False)
    C = B.write_page(P, W, pr, np.random.default_rng(0))
    assert C[0] == P[0] and all(C[i] == (P[i] + P[i - 1]) % 29 for i in range(1, 4))      # word 0: key = previous plaintext (primer F first)
    k_held = P[2]                                                                          # the last key spent (at i = 3) was the previous plaintext rune p_2; word 1 holds it
    assert all(C[i] == (P[i] + k_held) % 29 for i in range(4, 9))
    assert all(C[i] == (P[i] + C[i - 1]) % 29 for i in range(9, 15))                      # word 2 adheres: key = previous cipher rune


def test_pointer_spend_consumes_the_text_from_its_start():
    # every rune spends from the pointer: key_i = p_(i-1) for i >= 1 (the pointer lags by one), primer at i = 0
    P, W = PAGE; ai = B.ASSIGN.index(("spend", "spend", "spend")) if ("spend", "spend", "spend") in B.ASSIGN else None
    assert ai is None                                                                      # assignments are permutations: no all-spend member exists
    ai = B.ASSIGN.index(("spend", "hold", "adhere")); pr = (B.MEMBERS.index(("wpos", ai, "pointer", "sub")), 0.0, "none", False)
    C = B.write_page(P, W, pr, np.random.default_rng(0))
    assert C[0] == P[0]                                                                    # position 0 spends: nothing consumed yet, primer F
    assert C[3] == (P[3] - P[0]) % 29                                                      # position 3 (wpos 3 mod 3 = 0) spends the first unconsumed rune, p_0


def test_family_counts_match_the_registration():
    assert len(B.MEMBERS) == 288 and len(B.PROCS) == 2304 and len(B.DECODERS) == 1152 and len(B.ASSIGN) == 6
