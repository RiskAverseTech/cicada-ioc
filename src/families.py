"""Keystream families shared by phases 3-5: phase 3's book families and phase 4's phrase keys,
as (sign, decoder mode, key matrix, labels) sets.  Importable; builds on import."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model, S_MAX

lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
PR = np.array(primes(LMAX + 120))


def rep(v, L=LMAX):
    v = np.asarray(v) % N
    return np.resize(v, L)


# ---------- phrase and sentence keys from the translation's numbered lines ----------
lines = []
for ln in (RAW / "iddqd__liber-primus__translation.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*\d+\.\d+\.\d+\.\d+\s+(.*)$", ln)
    if not m: continue
    words = [w for w in re.findall(r"[A-Za-z']+", m.group(1))]
    if len(words) >= 1: lines.append(words)
if __name__ == "__main__": print(f"{len(lines)} numbered lines, {sum(len(l) for l in lines)} words", flush=True)

keys = {}      # rune tuple -> (family, label)
def add(fam, label, runes):
    t = tuple(int(x) for x in runes)
    if 2 <= len(t) and t not in keys: keys[t] = (fam, label)
for words in lines:
    for n in (2, 3, 4):
        for i in range(len(words) - n + 1):
            ph = " ".join(words[i:i + n])
            r = english_to_runes(ph)
            add(f"phrase-{n}", ph, r)
            add(f"phrase-{n}-rev", ph + " ʳ", r[::-1])
    if len(words) >= 5:
        sent = " ".join(words); r = english_to_runes(sent)
        add("sentence", sent[:60], r)
        add("sentence-rev", sent[:60] + " ʳ", r[::-1])
phrase_fams = [(fam, lab, rep(t)) for t, (fam, lab) in keys.items()]
if __name__ == "__main__": print(f"{len(phrase_fams)} distinct phrase/sentence keys", flush=True)

# ---------- phase 3's families, for the two sign conventions phase 3 did not run ----------
p3 = []
for s in range(N):
    p3.append(("shift", f"s={s}", rep([s])))
words = set()
for f in ("iddqd__liber-primus__translation.txt", "iddqd__liber-primus__known-plain-text--headlines.txt"):
    txt = (RAW / f).read_text(encoding="utf-8")
    for w in re.findall(r"[A-Za-z']+", txt):
        r = english_to_runes(w)
        if 2 <= len(r) <= 20: words.add(tuple(r))
words |= {tuple([23, 10, 1, 10, 9, 10, 16, 26]), tuple([0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18])}
for w in sorted(words):
    p3.append(("vigenere-word", to_latin(w), rep(w)))
    p3.append(("vigenere-word-rev", to_latin(w) + "ʳ", rep(w[::-1])))
for s in range(0, 101):
    p3.append(("primes", f"p[n+{s}]", rep(PR[s:s + LMAX])))
    p3.append(("primes-1 (totient)", f"p[n+{s}]-1", rep(PR[s:s + LMAX] - 1)))
    p3.append(("primes+1", f"p[n+{s}]+1", rep(PR[s:s + LMAX] + 1)))
fib = [0, 1]
while len(fib) < LMAX + 40: fib.append(fib[-1] + fib[-2])
luc = [2, 1]
while len(luc) < LMAX + 40: luc.append(luc[-1] + luc[-2])
for s in range(14):
    p3.append(("fibonacci", f"F[n+{s}]", rep(np.array(fib[s:s + LMAX]) % N)))
    p3.append(("lucas", f"L[n+{s}]", rep(np.array(luc[s:s + LMAX]) % N)))
for a in range(1, N):
    for b in range(N):
        p3.append(("affine position", f"{a}·n+{b}", rep((a * np.arange(LMAX) + b) % N)))
for b in range(N):
    p3.append(("square position", f"n²+{b}", rep((np.arange(LMAX) ** 2 + b) % N)))
for o in range(0, len(plain)):
    p3.append(("self running key", f"plaintext@{o}", rep(np.take(plain, np.arange(o, o + LMAX), mode="wrap"))))

# ---------- configuration sets: (sign, decoder mode, key matrix, labels) ----------
SETS = []
Kph = np.stack([k for _, _, k in phrase_fams]).astype(np.int64); Lph = [(f, l) for f, l, _ in phrase_fams]
Kp3 = np.stack([k for _, _, k in p3]).astype(np.int64); Lp3 = [(f, l) for f, l, _ in p3]
SETS.append(("sub",      "sub",      Kph,            Lph))
SETS.append(("add",      "sub",      (-Kph) % N,     Lph))
SETS.append(("beaufort", "beaufort", Kph,            Lph))
SETS.append(("add",      "sub",      (-Kp3) % N,     Lp3))
SETS.append(("beaufort", "beaufort", Kp3,            Lp3))
nconf = sum(len(L) for _, _, _, L in SETS)
ntests = nconf * len(pages) * 2
if __name__ == "__main__": print(f"{len(phrase_fams)} phrase keys x 3 signs + {len(p3)} phase-3 keys x 2 new signs = {nconf} configurations per page; "
      f"{len(pages)} pages x 2 F variants: {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)



ALLSETS = [("sub", "sub", Kph, Lph), ("add", "sub", (-Kph) % N, Lph), ("beaufort", "beaufort", Kph, Lph),
           ("sub", "sub", Kp3, Lp3), ("add", "sub", (-Kp3) % N, Lp3), ("beaufort", "beaufort", Kp3, Lp3)]
