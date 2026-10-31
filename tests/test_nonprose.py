"""The model-free structure scorer (src/nonprose_lane.py, §72): the three statistics by hand, and a planted non-prose page
recovered at rank 1 against a small library where the English decoder would see nothing."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import nonprose_lane as L


def test_statistics_by_hand():
    P = np.array([[1, 2, 3, 1, 2, 3, 4]]); wid = np.array([0, 0, 0, 1, 1, 1, 2])
    starts, lens = L.word_slots(wid)
    U, W, G = L.stats(P, starts, lens)[0]
    assert U == 4 + 4 + 4 + 1          # counts 2, 2, 2, 1
    assert W == 2                      # the word 1-2-3 twice; the one-rune word does not count
    assert G == 2                      # the 3-gram 1-2-3 twice


def test_f_rule_encryption_round_trips_through_the_decoder():
    rng = np.random.default_rng(1); Pt = rng.integers(0, 29, size=250); K = rng.integers(0, 29, size=L.LMAX)
    C = L.encrypt(Pt, K, "sub", True); P = L.decode_rows(C, K[None, :].astype(np.int16), "sub", True)[0]
    assert (P == Pt).mean() > 0.9 and (P[C != 0] == Pt[C != 0]).all()     # only the runes written as F are lost


def test_digit_plant_is_rank_one_in_a_small_library():
    rng = np.random.default_rng(2); K, labels, mode = L.build_library("sub", smoke=True)
    pid, Cref, wref = L.PAGES[3]; Pt, wid = L.payload("P4", rng, len(Cref), wref)
    ki = [i for i, l in enumerate(labels) if l.startswith("vigenere-word ")][7]
    C = L.encrypt(Pt, K[ki], mode, False); mom = L.moments(C, wid, False, rng); z = L.zstar(C, wid, K, mode, False, mom)
    assert int(np.argmax(z)) == ki and z[ki] > 20
