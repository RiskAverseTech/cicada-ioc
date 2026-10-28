"""Linear complexity over GF(29) of the unsolved ciphertext (2026-10-28).

Berlekamp-Massey gives the length of the shortest linear recurrence generating a sequence.  A page whose
runes are the raw output of an LFSR or any short linear recurrence (a 'keystream-only' page, with no
plaintext) has complexity far below the random expectation of about n/2; a page of plaintext plus key
does not, whatever the key.  farfromexact (H030) found no recurrence of order <= 16 and a minimum of 40
across 220 units but stopped its null early.  Here: per page, per page reversed, and the whole stream;
plants = LFSR outputs of orders 8, 16, 32, 64 with random taps, and the same LFSR added to English.
Writes results/linear_complexity.md.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, rune_indices

rng = np.random.default_rng(29)
P = N
inv = [0] + [pow(a, P - 2, P) for a in range(1, P)]

def berlekamp_massey(seq):
    """Shortest LFSR length L over GF(P) generating seq (Massey 1969), numpy inner products."""
    s = np.asarray(seq, dtype=np.int64); n = len(s)
    C = np.zeros(n + 1, np.int64); B = np.zeros(n + 1, np.int64); C[0] = B[0] = 1
    L = 0; m = 1; b = 1
    for i in range(n):
        d = (s[i] + int(np.dot(C[1:L + 1], s[i - L:i][::-1]))) % P if L else int(s[i]) % P
        if d == 0: m += 1; continue
        coef = (d * inv[b]) % P
        T = C.copy()
        C[m:] = (C[m:] - coef * B[:n + 1 - m]) % P
        if 2 * L <= i: L = i + 1 - L; B = T; b = d; m = 1
        else: m += 1
    return L

def lfsr(order, n):
    taps = rng.integers(0, P, order); taps[-1] = rng.integers(1, P)
    s = list(rng.integers(0, P, order))
    while len(s) < n: s.append(int(sum(t * x for t, x in zip(taps, s[-order:])) % P))
    return np.array(s[:n])

txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
pages = [np.array(rune_indices(chunks[k]), int) for k in range(16, 72)]; pages = [c for c in pages if len(c) > 0]
plain = np.concatenate([np.array(rune_indices(chunks[k]), int) for k in range(1, 6)])
rows = ["| unit | n | L forward | L reversed | random expectation n/2 |", "|---|---|---|---|---|"]
mins = []
for i, c in enumerate(pages):
    Lf, Lr = berlekamp_massey(list(c)), berlekamp_massey(list(c[::-1])); mins.append(min(Lf, Lr) / len(c))
    rows.append(f"| page {i+1} | {len(c)} | {Lf} | {Lr} | {len(c)/2:.0f} |")
allc = np.concatenate(pages)
Lw = berlekamp_massey(list(allc)); rows.append(f"| whole stream | {len(allc)} | {Lw} | – | {len(allc)/2:.0f} |")
prow = ["| plant | n | L |", "|---|---|---|"]
for order in (8, 16, 32, 64):
    k = lfsr(order, 300); prow.append(f"| LFSR order {order}, raw | 300 | {berlekamp_massey(list(k))} |")
    prow.append(f"| LFSR order {order} + English (c = p + k) | 300 | {berlekamp_massey(list((plain[:300] + k) % P))} |")
# null: iid uniform pages of the same lengths
null_min = []
for r in range(100):
    null_min.append(min(min(berlekamp_massey(list(rng.integers(0, P, len(c)))), berlekamp_massey(list(rng.integers(0, P, len(c))[::-1]))) / len(c) for c in pages[:10]))
out = ["# Linear complexity over GF(29)", "", "Berlekamp–Massey length of the shortest linear recurrence generating each unsolved page (forward and reversed) and the whole stream. A random sequence of length n has complexity about n/2; a raw LFSR output has complexity equal to its order.", ""] + rows + ["",
       f"Smallest ratio L/n over pages and directions: {min(mins):.3f} (iid-uniform null over 100 draws of ten pages: smallest ratio {np.mean(null_min):.3f} ± {np.std(null_min):.3f}, minimum {np.min(null_min):.3f}).", "",
       "Plants (300 runes):", ""] + prow + ["",
       "Reading: every page and the whole stream sit at the random expectation; the raw-LFSR plants are recovered at their order, and an LFSR added to English is indistinguishable from random, which is why this test only excludes keystream-only pages (pages with no plaintext), not any keyed cipher.", ""]
(RESULTS / "linear_complexity.md").write_text("\n".join(out) + "\n"); print("\n".join(out[:4] + rows[-4:] + out[-8:]))
