"""Post hoc null for §70: do structured keys score higher than uniform keystreams under the E56 lattice decoder? (2026-10-31)

The registered null of src/e56_lattice.py is 2,000 uniform random keystreams per (page, F). The sweep put 29 library rows above
z 6 and above that null's maximum, all unreadable, against a plants' floor of z 52. §69 found that a uniform null lacks the
unigram structure of the thing it stands for; the library keys here are English text, phrases, affine streams and prime
residues, none of them uniform. This script, written after the sweep and labelled post hoc in the registration, re-nulls the
top cells with keys that carry the library's structure: (b) 2,000 library keys with their runes permuted (unigram-matched,
order destroyed), (c) 2,000 English windows from the corpus (fully structured running keys), and for the totient cell
(d) 2,000 permuted prime-stream keys. Reported per cell: the top library score's z under each null and how many null keys
beat it. CELL selects the cell (0-6). Output: results/e56_structured_null_{CELL}.json, merged by hand into
results/e56_structured_null.md.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("STAGE", "none")
import numpy as np
import e56_lattice as E
from lp import RESULTS, N

CELLS = [("LP2-22", "beaufort", False, "book"), ("LP2-02", "add", True, "book"), ("LP2-34", "beaufort", False, "book"),
         ("LP2-49", "beaufort", False, "book"), ("LP2-14", "add", True, "primes"), ("LP2-42", "sub", False, "book"), ("LP2-11", "sub", False, "book")]
ci = int(os.environ.get("CELL", 0)); pid, sign, f_rule, lib = CELLS[ci]; t0 = time.time()
ws = dict(E.PAGES)[pid]; rng = np.random.default_rng(7000 + ci); NN = 2000
Klib, Llib, mode = (E.library if lib == "book" else E.prime_library)(sign)
sc = np.array([E.decode_e56(ws, k, mode, f_rule)[0] for k in Klib]); top = int(sc.argmax()); s_top = float(sc[top])
corpus = json.load(open(Path(__file__).resolve().parents[1] / "data" / "corpus" / "corpus.json"))
text = np.concatenate([np.array(v["runes"], int) for v in corpus.values()])
def english_keys(n):
    offs = rng.integers(0, len(text) - E.LKEY, size=n); K = np.stack([text[o:o + E.LKEY] for o in offs])
    return (-K) % N if sign == "add" else K
nulls = {"uniform": rng.integers(0, N, size=(NN, E.LKEY)),
         "permuted library": np.stack([rng.permutation(Klib[i]) for i in rng.integers(0, len(Klib), size=NN)]),
         "english windows": english_keys(NN)}
res = dict(cell=ci, page=pid, sign=sign, F=f_rule, library=lib, top_key=Llib[top], top_score=s_top, n_lib=len(Klib), nulls={})
for name, Ks in nulls.items():
    v = np.array([E.decode_e56(ws, k, mode, f_rule)[0] for k in Ks])
    res["nulls"][name] = dict(mean=float(v.mean()), sd=float(v.std()), max=float(v.max()), z_top=float((s_top - v.mean()) / v.std()),
                              n_above_top=int((v >= s_top).sum()), n_above_uniform_max=None)
    print(f"{pid} {sign} F={int(f_rule)} {name}: mean {v.mean():.1f} sd {v.std():.2f} max {v.max():.1f} | top z {(s_top - v.mean()) / v.std():.2f}, {int((v >= s_top).sum())} null keys ≥ top [{time.time()-t0:.0f}s]", flush=True)
    if name == "uniform": umax = float(v.max())
    res["nulls"][name]["n_above_uniform_max"] = int((v > umax).sum())
res["lib_above_uniform_max"] = int((sc > umax).sum()); res["lib_z45_uniform"] = int(((sc - res["nulls"]["uniform"]["mean"]) / res["nulls"]["uniform"]["sd"] >= 4.5).sum())
json.dump(res, open(RESULTS / f"e56_structured_null_{ci}.json", "w"), indent=1); print("done", time.time() - t0)
