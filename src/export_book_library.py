"""Export this repository's key library (families.ALLSETS: the phase 3 book streams and the phase 4 phrase keys) as a TSV,
so that another lab can run it under its own engine (2026-10-28, §54).  Nothing of theirs is run here.

Output data/processed/book_library.tsv, one row per distinct key: family, label, period, values.
  values  the keystream as space-separated rune indices 0..28 (Gematria Primus order F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA)
  period  0 for a non-periodic stream (the values are the first 327 = longest page + the decoder's key margin, exactly as decoded here);
          otherwise the key is periodic and `values` holds one period: repeat it to the length you need.
Sign conventions are not part of the key: every key here was decoded as C = P + K, C = P - K and C = K - P (README §12).
Usage: .venv/bin/python -I src/export_book_library.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import PROCESSED, N
import families as F

OUT = PROCESSED / "book_library.tsv"


def period(v):
    for p in range(1, len(v) // 2 + 1):
        if np.array_equal(v[p:], v[:-p]): return p
    return 0


seen = set(); rows = []
for sign, mode, Ks, labs in F.ALLSETS:
    if sign != "sub": continue                       # the add / beaufort sets hold the same keys (negated or not)
    for k, (fam, lab) in zip(Ks, labs):
        key = (fam, lab)
        if key in seen: continue
        seen.add(key); v = np.asarray(k) % N; p = period(v)
        rows.append((fam, lab, p, v[:p] if p else v))
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# this repository's key library (src/families.py ALLSETS), exported by src/export_book_library.py; see the module docstring for the format\n")
    f.write("family\tlabel\tperiod\tvalues\n")
    for fam, lab, p, v in rows:
        f.write(f"{fam}\t{lab.replace(chr(9), ' ')}\t{p}\t{' '.join(map(str, v.tolist()))}\n")
from collections import Counter
print(f"{len(rows)} keys written to {OUT} ({OUT.stat().st_size/1e6:.1f} MB); by family: {dict(Counter(r[0] for r in rows))}; periodic {sum(1 for r in rows if r[2])}")
