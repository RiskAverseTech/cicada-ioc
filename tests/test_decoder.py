"""Fast checks of the decoder and the data (seconds; run with: python -m pytest tests/)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import numpy as np
from lp import N, english_to_runes, LATIN
from score import decode, english_model, S_MAX
from skip_decrypt import encrypt


def test_reviewer_three_rejection_case():
    lu, _, _ = english_model(); lu2 = lu.copy(); lu2[6] = np.log(0.9); lu2[7] = np.log(0.001)
    P = np.array([5, 6]); K = np.array([2, 1, 1, 1, 2] + list(np.arange(60) % N)); C = encrypt(P, K)
    assert decode(C, K[None, :], lu2, max_skip=2)[2][0].tolist() != P.tolist()   # the old bound cannot reach the path
    assert decode(C, K[None, :], lu2, max_skip=4)[2][0].tolist() == P.tolist()


def test_soft_rule_roundtrip_all_signs():
    lu, _, plain = english_model(); rng = np.random.default_rng(0); n = 200; P = plain[500:500 + n]
    for sign, mode in (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort")):
        for f_rule in (False, True):
            K = rng.integers(0, N, size=n + S_MAX + 2)
            C = encrypt(P, K, f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
            Kd = (-K) % N if sign == "add" else K
            dec = decode(C, Kd[None, :], lu, f_rule, mode)[2][0]
            assert (dec == P).mean() > 0.97, (sign, f_rule, (dec == P).mean())


def test_random_key_scores_as_noise():
    lu, _, plain = english_model(); rng = np.random.default_rng(1); P = plain[1000:1262]
    K = rng.integers(0, N, size=len(P) + S_MAX + 2); C = encrypt(P, K, rng=rng, soft=0.81)
    Kr = rng.integers(0, N, size=(300, len(P) + S_MAX + 2))
    true = decode(C, K[None, :], lu)[0][0]; null = decode(C, Kr, lu)[0]
    assert (true - null.mean()) / null.std() > 8


def test_know_this_squares_and_gematria():
    GV = {"F": 2, "U": 3, "TH": 5, "O": 7, "R": 11, "C": 13, "G": 17, "W": 19, "H": 23, "N": 29, "I": 31, "J": 37, "EO": 41, "P": 43, "X": 47, "S": 53, "T": 59, "B": 61, "E": 67, "M": 71, "L": 73, "NG": 79, "OE": 83, "D": 89, "A": 97, "AE": 101, "Y": 103, "IA": 107, "EA": 109}
    val = lambda w: sum(GV[LATIN[i]] for i in english_to_runes(w))
    assert val("SHADOWS") == 341 and val("AETHEREAL") == 366 and val("CABAL") == 341
    A = np.array([[434, 1311, 312, 278, 966], [204, 812, 934, 280, 1071], [626, 620, 809, 620, 626], [1071, 280, 934, 812, 204], [966, 278, 312, 1311, 434]])
    assert (A.sum(0) == 3301).all() and (A.sum(1) == 3301).all() and np.trace(A) == 3301


def test_pages_and_doublets():
    import json
    d = json.loads((Path(__file__).resolve().parent.parent / "data" / "processed" / "pages.json").read_text())
    uns = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
    assert len(uns) == 55 and sum(len(c) for c in uns) == 12956
    assert sum(int((c[1:] == c[:-1]).sum()) for c in uns) == 86
