"""Exact reachability of the solved-page rule at every offset (2026-10-28).

The solved polyalphabetic pages follow one rule: c = p + k (or p - k) with k from a stream, a ciphertext F is
EITHER a literal plaintext F that consumes no key value OR an encrypted rune, and no encrypted rune decrypts
to F (farfromexact H007 states it this way).  Under that rule a page and a stream offset either admit a
consistent skip/no-skip path or they do not: a deterministic exclusion with no score.  farfromexact ran it at
offset 0 only.  Here: every offset 0..MAXOFF of five streams, both signs, per page (fresh offset per page) and
continuous (one offset for the whole section).  Power: an English page encrypted under the rule at a random
offset; the count of surviving wrong offsets says how selective the test is.  Writes results/reachability.md.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, primes, rune_indices

rng = np.random.default_rng(7)
MAXOFF = 20000
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
pages = [np.array(rune_indices(chunks[k]), int) for k in range(16, 72)]; pages = [c for c in pages if len(c) > 0]
ps = np.array(primes(MAXOFF + 14000))
fib = [0, 1]
while len(fib) < MAXOFF + 14000: fib.append(fib[-1] + fib[-2])
luc = [2, 1]
while len(luc) < MAXOFF + 14000: luc.append(luc[-1] + luc[-2])
STREAMS = {"prime - 1 (phi)": (ps - 1) % N, "prime": ps % N, "prime + 1": (ps + 1) % N,
           "Fibonacci": np.array(fib, dtype=object).astype(int) % N if False else np.array([f % N for f in fib]),
           "Lucas": np.array([l % N for l in luc])}

def survivors(c, S, sign, offs):
    """Offsets admitting a skip/no-skip assignment with no encrypted rune decrypting to F.
    Vectorised over offsets; state = number of F's skipped so far (key index = off + i - s).
    Offsets with no live state are dropped as the DP walks the page."""
    c = np.asarray(c); L = len(c); nF = int((c == 0).sum())
    offs = np.asarray(offs); alive = np.zeros((len(offs), nF + 1), bool); alive[:, 0] = True
    for i in range(L):
        smax = min(nF, i)                                  # cannot have skipped more F's than seen
        s = np.arange(smax + 1)
        kk = S[offs[:, None] + i - s[None, :]]           # (offsets, states)
        bad = (c[i] - sign * kk) % N == 0
        if c[i] == 0:
            nxt = np.zeros_like(alive)
            w = min(smax + 1, nF)
            nxt[:, 1:1 + w] |= alive[:, :w]                  # skip: literal F, key not consumed
            nxt[:, :smax + 1] |= alive[:, :smax + 1] & ~bad # or encrypt, if it does not decrypt to F
        else:
            nxt = np.zeros_like(alive); nxt[:, :smax + 1] = alive[:, :smax + 1] & ~bad
        keep = nxt.any(1)
        alive, offs = nxt[keep], offs[keep]
        if len(offs) == 0: return []
    return offs.tolist()

def encrypt(p, S, off, sign):
    out, j = [], 0
    for x in p:
        if x == 0: out.append(0); continue       # literal F, consumes no key
        out.append((x + sign * S[off + j]) % N); j += 1
    return np.array(out)

# plaintext for plants: the solved text
plain = np.array(rune_indices((RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8").split("%")[2]), int)
offs = np.arange(MAXOFF)
rows = ["| stream | sign | pages with ≥1 surviving offset (of 55) | total surviving (page, offset) pairs | continuous section: surviving offsets | plant: true offset found | plant: wrong offsets surviving |", "|---|---|---|---|---|---|---|"]
for name, S in STREAMS.items():
    for sign in (+1, -1):
        per = [survivors(c, S, sign, offs) for c in pages]
        npages = sum(1 for s in per if s); tot = sum(len(s) for s in per)
        cont = survivors(np.concatenate(pages), S, sign, offs)
        # plant: a 300-rune English page at a random offset
        o_true = int(rng.integers(0, MAXOFF - 400)); pl = encrypt(plain[:300], S, o_true, sign)
        sv = survivors(pl, S, sign, offs)
        rows.append(f"| {name} | {'+' if sign > 0 else '−'} | {npages} | {tot} | {len(cont)} | {'yes' if o_true in sv else 'NO'} | {len(sv) - (o_true in sv)} |"); print(rows[-1], flush=True)
out = ["# Exact reachability of the solved-page rule", "", f"Rule: c = p ± k, a ciphertext F is a literal F (no key consumed) or an encrypted rune, no encrypted rune decrypts to F. Streams reduced mod 29; offsets 0..{MAXOFF-1}; per page (fresh offset each page) and continuous (one offset for all 12,956 runes). A page survives an offset if any skip assignment keeps every encrypted rune off F.", ""] + rows + ["",
       "Reading: a surviving offset is necessary, not sufficient, for the rule; a page with zero surviving offsets is excluded exactly for that stream and sign. The plant column shows how many wrong offsets survive by chance for a 300-rune page, i.e. the test's selectivity.", ""]
(RESULTS / "reachability.md").write_text("\n".join(out) + "\n"); print("\n".join(out[-3:]))
