"""Adjudicate a claimed solution of an unsolved page with this repository's instrument (2026-10-27).

Give a page and EITHER a key stream (runes as Latin letters, e.g. DIVINITY, or integers 0-28 comma
separated) with a sign convention and F variant, OR a claimed plaintext (Latin letters).  The script
reports z_uni (decoder score over 2,000 random keystreams through the identical decoder), z_5 (rune
5-gram over the same keystreams' decodes), the transliteration, and whether the claim clears the bar
this repository pre-registers for a hit (z_uni >= 6 and z_5 >= 6; readability is the human's call).
A claimed plaintext is scored directly: its 5-gram log-probability against 2,000 random rune strings
of the same length, and its length against the page.
Usage: python -I src/check_solve.py --page LP2-03 --key DIVINITY --sign sub [--F]
       python -I src/check_solve.py --page LP2-03 --plaintext "WELCOME PILGRIM ..."
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX
import families as F, ngram

ap = argparse.ArgumentParser(); ap.add_argument("--page", required=True); ap.add_argument("--key"); ap.add_argument("--sign", default="sub", choices=["sub", "add", "beaufort"]); ap.add_argument("--F", action="store_true"); ap.add_argument("--plaintext")
a = ap.parse_args()
pages = dict(F.pages); C = pages[a.page]; lu = F.lu; T5 = ngram.load_dense(); rng = np.random.default_rng(3301)
if a.plaintext:
    P = np.array(english_to_runes(a.plaintext)); s = ngram.score_batch(P[None, :], T5)[0]
    nul = ngram.score_batch(rng.integers(0, N, size=(2000, len(P))), T5)
    print(f"claimed plaintext: {len(P)} runes (page has {len(C)}); 5-gram z over random rune strings of that length: {(s - nul.mean())/nul.std():.1f} (English of this length scores about {0.5*len(P)**0.5*4:.0f}+); the claim must also decrypt from a stated key to count.")
    sys.exit(0)
key = np.array([int(x) for x in a.key.split(",")]) if "," in a.key or a.key.strip().isdigit() else np.array(english_to_runes(a.key))
K = np.resize(key, len(C) + S_MAX + 2); mode = "beaufort" if a.sign == "beaufort" else "sub"
Kd = (-K) % N if a.sign == "add" else K
Kr = rng.integers(0, N, size=(2000, len(C) + S_MAX + 2)); sc0, _, dec0 = decode(C, Kr, lu, a.F, mode); s50 = ngram.score_batch(dec0, T5)
sc, _, dec = decode(C, Kd[None, :], lu, a.F, mode); s5 = ngram.score_batch(dec, T5)[0]
zu = (sc[0] - sc0.mean()) / sc0.std(); z5 = (s5 - s50.mean()) / s50.std()
print(f"{a.page} ({len(C)} runes), key {a.key[:40]} sign {a.sign} F={a.F}: z_uni {zu:.2f}, z_5 {z5:.2f} -> {'CLEARS the bar (now read it)' if zu >= 6 and z5 >= 6 else 'does not clear the bar (z_uni >= 6 and z_5 >= 6)'}")
print("decode:", translit(dec[0]))
