"""Post hoc for §70: a uniform-keystream null as large as the library (2026-10-31).

The sweep compared each page's 45,726 library configurations (7,621 keys x 3 signs x 2 F) with the maximum of 2,000 uniform
keystreams. The score distribution is right-skewed (the maximum of 2,000 draws sits at 4.5-5.1 sd), so the library's maximum
should exceed the 2,000-draw maximum under the null alone. Here: 46,000 uniform keystreams per (page, F) for the three pages with
the largest sweep z, in shards; results/e56_bignull.md reports the null's maximum, the count of null draws at or above the
library's top score, and the top score's rank among them. PAGE, F, SHARD, NSHARD from the environment.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("STAGE", "none")
import numpy as np
import e56_lattice as E
from lp import RESULTS, N
pid = os.environ["PAGE"]; f_rule = os.environ.get("F", "0") == "1"; k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
ws = dict(E.PAGES)[pid]; rng = np.random.default_rng(9000 + 10 * k + int(f_rule) + sum(map(ord, pid))); n = 46000 // m; t0 = time.time()
sc = [E.decode_e56(ws, kk, "sub", f_rule)[0] for kk in rng.integers(0, N, size=(n, E.LKEY))]
json.dump(dict(page=pid, F=f_rule, shard=k, scores=sc), open(RESULTS / f"e56_bignull_{pid}_{int(f_rule)}_{k}.json", "w")); print("done", len(sc), time.time() - t0)
