"""The direction lane (src/direction_lane.py, §75): word numbers become per-rune keys as the registration says (a shift is
constant over the word, a step is j·g, a solved offset reads the solved text from word g), and the word-shift map scheme at
alignment a keys the k-th word of a page with the (gw + a)-th solved word's number."""
import os, sys
from pathlib import Path
os.environ["SMOKE"] = "1"; os.environ["STAGE"] = "none"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import direction_lane as D


def test_keystream_from_numbers_follows_the_three_applications():
    runs = [(0, 4), (4, 9)]; nums = [7, 30]
    K = D.keystream_from_numbers(nums, runs, 9, "shift")
    assert list(K[:4]) == [7] * 4 and list(K[4:9]) == [30 % D.N] * 5
    K = D.keystream_from_numbers(nums, runs, 9, "step")
    assert list(K[:4]) == [0, 7, 14, 21] and list(K[4:9]) == [(j * 30) % D.N for j in range(5)]
    K = D.keystream_from_numbers(nums, runs, 9, "solved")
    s = D.SOLVED_START[7 % D.NW]
    assert list(K[:4]) == list(D.SOLVED_RUNES[s:s + 4])


def test_word_shift_scheme_keys_each_word_with_the_aligned_solved_number():
    pid, C, wid = D.PAGES[3]; gw, gr = D.GW[3], D.GR[3]; a = 11
    K = D.map_keystream("word-shift", a, 3, len(C), wid, gw, gr)
    for s, e in D.word_runs(wid)[:10]:
        assert (K[s:e] == int(D.WNUM[(gw[s] + a) % D.NW]) % D.N).all()
    assert 0 <= K[:len(C)].min() and K[:len(C)].max() < D.N
