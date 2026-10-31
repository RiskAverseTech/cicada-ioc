"""Post hoc to §74: the model-free z* of family-2 decoders on uniform random pages, per decoder (results/hand_procedure2_zstar_chance.json). Run from the repo root: .venv/bin/python -I src/hp2_zstar_chance.py"""
import os, sys, json, numpy as np
os.environ["FAMILY"] = "2"; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import hand_procedure_lane as H
rng = np.random.default_rng(777)
# population A: the decoders that scored z* >= 10.5 on the pages (from the decode files); population B: random decoders of the family
rows = []
for k in range(4): rows += json.load(open(f"results/hand_procedure2_decode_{k}.json"))["rows"]
hi = [tuple(r["proc"]) for r in rows if r["maxstar"] >= 10.5]
dec = [pr for pr in H.PROCS if pr[4] == 0.0]
pickA = [hi[i] for i in rng.choice(len(hi), 60, replace=False)]
pickB = [dec[i] for i in rng.choice(len(dec), 60, replace=False)]
top = [tuple(r["proc"]) for r in sorted(rows, key=lambda r: -r["maxstar"])[:2]]
def zstar_uniform(pr, reps=3):
    ti, st, rs, ru, fi, lf, mk, tw, bh = H.unpack(pr); T = H.TABLES[ti][1]; Tinv = H.invert(T); R28 = H.excl_row(T) if ru == "exclude" else None
    out = []
    for _ in range(reps):
        best = -1e9
        for pid, (C, Wd) in enumerate(H.LP2):
            Cf = rng.integers(0, H.N, size=len(C)); P = H.decode_page(Cf, Wd, T, Tinv, R28, st, rs, ru, lf, 0, mk, tw, bh)
            best = max(best, H.page_zstar(P, Wd, pid, rng))
        out.append(best)
    return out
res = {}
for name, picks in (("top2", top), ("hi_on_pages", pickA), ("random_family", pickB)):
    vals = [(H.label(pr), zstar_uniform(pr)) for pr in picks]
    allv = [v for _, vs in vals for v in vs]
    res[name] = dict(n=len(picks), max=float(max(allv)), median=float(np.median(allv)), share_ge_10_5=float(np.mean([v >= 10.5 for v in allv])), rows=vals)
    print(name, "n", len(picks), "median max-page z* on uniform pages", round(res[name]["median"], 2), "max", round(res[name]["max"], 2), "share >= 10.5", round(res[name]["share_ge_10_5"], 2), flush=True)
    if name == "top2":
        for l, vs in vals: print("  ", l, [round(v, 2) for v in vs])
json.dump(res, open("results/hand_procedure2_zstar_chance.json", "w"), indent=1)
