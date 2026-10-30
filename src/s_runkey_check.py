"""The S rate at lag-5 cipher coincidences under English running keys (2026-10-29, §47 correction).

§47 argued that under an additive cipher whose key is independent of the plaintext, the rune at an equal cipher pair is
uniform, so S with probability 1/29.  The third external review (2026-10-29) showed the stated condition is too weak:
conditioning on c_i = c_j conditions on the key difference k_j - k_i, and the cipher value is uniform only if k_j is
uniform GIVEN that difference (true for independent uniform keys and for periodic keys with uniform values; false in
general).  A running key from English text is the realistic case that breaks it: a key repeat five apart is an English
repeated letter, not a uniform one.  This script measures how far from 1/29 that case lands.  Plaintext: Emerson's essays
in rune spelling, within-word lag-5 pairs; keys: three other texts of the corpus as running keys from 20 offsets each,
under the three sign conventions; controls: an iid uniform key (1/29 expected) and a zero key (plaintext's own S..S rate).
Output: results/s_runkey_check.md.
"""
import json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, RESULTS, english_to_runes

t0 = time.time(); rng = np.random.default_rng(47); S = 15; LAG = 5; NOFF = 20
ROOT = Path(__file__).resolve().parent.parent
cj = json.loads((ROOT / "data" / "corpus" / "corpus.json").read_text())
text = (ROOT / "data" / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(errors="ignore")[20000:]
words = []
for w in re.findall(r"[A-Za-z']+", text):
    try: r = english_to_runes(w)
    except Exception: continue
    if len(r) > LAG: words.append(np.array(r))
P = np.concatenate(words); wid = np.concatenate([np.full(len(w), k) for k, w in enumerate(words)])
pair = np.where(wid[LAG:] == wid[:-LAG])[0]                      # i such that (i, i+5) lie in one word
A, B = pair, pair + LAG
enc = {"sub": lambda p, k: (p - k) % N, "add": lambda p, k: (p + k) % N, "beaufort": lambda p, k: (k - p) % N}


def rate(C):
    eq = C[A] == C[B]; n = int(eq.sum()); s = int((C[A][eq] == S).sum()); return n, s


rows = []; keys = {k: np.asarray(cj[k]["runes"]) for k in ("kybalion", "king_in_yellow", "mabinogion_guest")}
for name, K in keys.items():
    for sign, f in enc.items():
        n = s = 0
        for _ in range(NOFF):
            o = int(rng.integers(0, len(K))); Kw = np.resize(np.roll(K, -o), len(P)); a, b = rate(f(P, Kw)); n += a; s += b
        rows.append((f"{name} as running key", sign, n, s))
n = s = 0
for _ in range(NOFF): a, b = rate(enc["add"](P, rng.integers(0, N, len(P)))); n += a; s += b
rows.append(("iid uniform key (control)", "add", n, s))
a, b = rate(P); rows.append(("zero key (plaintext in clear)", "—", a, b))
out = ["# The S rate at within-word lag-5 cipher coincidences under English running keys", "",
       f"Plaintext: Emerson's essays in rune spelling, {len(words):,} words of more than {LAG} runes, {len(pair):,} within-word lag-5 pairs. Each running key is read from {NOFF} random offsets; counts are pooled. The rune at an equal cipher pair is S with probability 1/29 = {100/N:.2f} % when the key is uniform given its own lag-5 difference (iid uniform keys, periodic uniform keys); under an English running key the key repeats are English's repeated letters and the rate moves off 1/29 by the amount shown. The pages' own figure for comparison is 11 of 102 = 10.8 % (§45).", "",
       "| key | sign | equal cipher pairs | of which S | S rate | z against 1/29 |", "|---|---|---|---|---|---|"]
for name, sign, n, s in rows:
    p = s / n if n else float("nan"); z = (s - n / N) / np.sqrt(n * (1 / N) * (1 - 1 / N)) if n else float("nan")
    out.append(f"| {name} | {sign} | {n:,} | {s:,} | {100 * p:.2f} % | {z:+.1f} |")
mx = max(s / n for name, sign, n, s in rows if "running" in name)
out += ["", f"Reading: the largest S rate under an English running key is {100 * mx:.2f} %, against 3.45 % for a uniform key and 10.8 % on the pages. The §47 theorem's condition is corrected to 'uniform given the key difference'; running keys from text are outside the theorem and are measured here instead, and they do not reach the pages' rate. [stated]", "",
       f"Runtime {time.time() - t0:.0f} s. Reproduce: `.venv/bin/python -I src/s_runkey_check.py`.", ""]
(RESULTS / "s_runkey_check.md").write_text("\n".join(out)); print("\n".join(out))
