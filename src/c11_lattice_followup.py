"""C11, the lattice step (registration: results/quorum_checks_registration.md, "C11, the lattice step", commit ac68af1).

The twelve (stream, page) cells the cumulative-offset sweep left above the free-null line, each decoded with its own key at its
own offset under §70's lattice decoder (fillers, lag-5 / lag-6 echoes, skips, literal F; beam 8), scored against 2,000 random
keystreams for the page and F, and ranked against every offset of the cell's registered window under the same decoder.  Six
fresh plants (Bunyan words in E56w+n form under a library stream at the cumulative offset of six pages) calibrate.
Reproduce: .venv/bin/python -I src/c11_lattice_followup.py  (SMOKE=1 shrinks the null and the windows).
"""
import os, sys, json, glob, time
from pathlib import Path
os.environ["STAGE"] = "none"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, RESULTS
import e56_lattice as E
import families as F, pnotisdev_library as PL
from score import translit

t0 = time.time(); SMOKE = os.environ.get("SMOKE") == "1"; NNULL = 50 if SMOKE else 2000; S_MAX = E.S_MAX
def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)

PAGES = dict(E.PAGES)                                                              # pid -> cipher word slots
pages = [(p, C) for p, C in F.pages if len(C) > 0]; assert len(pages) == 55
PID = [p for p, _ in pages]; CUM = np.concatenate([[0], np.cumsum([len(C) for _, C in pages])[:-1]])
def window_of(k):
    lo = max(0, int(np.floor(0.90 * CUM[k])) - 50); hi = int(CUM[k]) + 50
    w = np.arange(lo, hi + 1); return w[-40:] if SMOKE else w

def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)
names, fams, periods, KP = PL.load(); PR = sieve(300000)[:20000]
STREAMS = {f"pn:{names[i]}": KP[i].astype(np.int64) for i in range(len(names)) if not periods[i]}
STREAMS.update({"prime p": PR % N, "prime p-1": (PR - 1) % N, "prime p+1": (PR + 1) % N})
MODE = {"sub": "sub", "add": "sub", "beaufort": "beaufort"}                        # the sweep's convention: add = sub with the key negated
def key_at(s, off, n, sign):
    K = s[off: off + n + S_MAX + 4].astype(np.int64); return (-K) % N if sign == "add" else K

NULLS = {}
def null(pid, f_rule, mode, rng):
    k = (pid, f_rule, mode)
    if k not in NULLS:
        ws = PAGES[pid]; n = sum(len(w) for w in ws)
        v = np.array([E.decode_e56(ws, kk, mode, f_rule)[0] for kk in rng.integers(0, N, size=(NNULL, n + S_MAX + 4))])
        NULLS[k] = (float(v.mean()), float(v.std()), float(v.max()))
    return NULLS[k]

def run_cell(pid, ws, s, off, sign, f_rule, rng):
    mode = MODE[sign]; n = sum(len(w) for w in ws); k = PID.index(pid)
    sc, P, nf, ne = E.decode_e56(ws, key_at(s, off, n, sign), mode, f_rule); m, sd, mx = null(pid, f_rule, mode, rng)
    offs = window_of(k); win = np.array([E.decode_e56(ws, key_at(s, int(o), n, sign), mode, f_rule)[0] for o in offs])
    near = np.abs(offs - off) <= 3; rank = int((win[~near] > sc).sum()) + 1
    return dict(z=float((sc - m) / sd), above_max=bool(sc > mx), rank=rank, window=len(offs), win_zmax=float((win.max() - m) / sd),
                fillers=int(nf), echoes=int(ne), tr=translit(P[P >= 0][:80]))

# ---------- the twelve cells: the best window per (stream, page) among the sweep's candidates
rows = [c for f in sorted(glob.glob(str(RESULTS / "cumulative_lane_shard*.json"))) for c in json.load(open(f))["candidates"]]
best = {}
for c in rows:
    kk = (c["name"], c["page"])
    if kk not in best or c["z2"] > best[kk]["z2"]: best[kk] = c
cells = sorted(best.values(), key=lambda c: -c["z2"]); log(len(rows), "candidate windows,", len(cells), "cells")
if SMOKE: cells = cells[:2]
out_cells = []
for c in cells:
    rng = np.random.default_rng(1234); r = run_cell(c["page"], PAGES[c["page"]], STREAMS[c["name"]], int(c["offset"]), c["sign"], bool(c["F"]), rng)
    r.update(stream=c["name"], page=c["page"], sign=c["sign"], F=bool(c["F"]), offset=int(c["offset"]), free_z=float(c["z2"]), free_minus_plain=float(c["fb"]))
    out_cells.append(r); log(c["name"], c["page"], c["sign"], "F", c["F"], "offset", c["offset"], "free z", round(c["z2"], 2), "-> lattice z", round(r["z"], 2), "rank", r["rank"], "of", r["window"], "window max z", round(r["win_zmax"], 2))

# ---------- six plants
bw = E.bunyan_words(); plants = []; snames = sorted(STREAMS)
for ci, (sign, f_rule, k) in enumerate(zip(("sub", "add", "beaufort") * 2, (False,) * 3 + (True,) * 3, (5, 14, 23, 32, 41, 50))):
    rng = np.random.default_rng(900 + ci); pid = PID[k]; n = len(pages[k][1]); mode = MODE[sign]
    a = int(rng.integers(0, len(bw) - 200)); pw = []; m = 0
    while m < n: pw.append(bw[a + len(pw)]); m += len(pw[-1])
    sname = snames[int(rng.integers(len(snames)))]; s = STREAMS[sname]; off = int(CUM[k]); K = key_at(s, off, m, sign)
    cw, P0, FM, EM = E.encrypt_e56(pw, K, mode, f_rule, rng); ws = cw; nn = sum(len(w) for w in ws)
    sc, P, nf, ne = E.decode_e56(ws, key_at(s, off, nn, sign), mode, f_rule)
    v = np.array([E.decode_e56(ws, kk, mode, f_rule)[0] for kk in rng.integers(0, N, size=(NNULL, nn + S_MAX + 4))]); mm, sd = v.mean(), v.std()
    offs = window_of(k); win = np.array([E.decode_e56(ws, key_at(s, int(o), nn, sign), mode, f_rule)[0] for o in offs])
    near = np.abs(offs - off) <= 3; rank = int((win[~near] > sc).sum()) + 1; real = ~FM
    plants.append(dict(plant=ci, page=pid, stream=sname, sign=sign, F=f_rule, offset=off, z=float((sc - mm) / sd), rank=rank, window=len(offs),
                       acc=float((P[real] == P0[real]).mean()), fillers=int(FM.sum()), echoes=int(EM.sum()), fillers_placed=int(nf), echoes_placed=int(ne)))
    log("plant", ci, pid, sname, sign, "F", f_rule, "lattice z", round(plants[-1]["z"], 2), "rank", rank, "acc", round(plants[-1]["acc"], 2))

# ---------- report
L1 = all(p["rank"] == 1 and p["z"] >= 8 for p in plants); L2 = all(c["z"] < 8 for c in out_cells)
o = ["# C11, the lattice step: the twelve cells above the free-null line under the §70 lattice decoder", "",
     f"Registration: `results/quorum_checks_registration.md`, \"C11, the lattice step\". Null: {NNULL} random keystreams per (page, F); rank: every offset of the cell's registered window under the same decoder (offsets within 3 of the cell's count as the same hypothesis).", "",
     "| stream | page | sign | F | offset | free-null z | lattice z | above null max | rank in window | window max z | fillers / echoes placed | decode (first 60) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c in out_cells: o.append(f"| {c['stream']} | {c['page']} | {c['sign']} | {int(c['F'])} | {c['offset']} | {c['free_z']:.2f} | {c['z']:.2f} | {'yes' if c['above_max'] else 'no'} | {c['rank']} of {c['window']} | {c['win_zmax']:.2f} | {c['fillers']} / {c['echoes']} | `{c['tr'][:60]}` |")
o += ["", "Plants (Bunyan words in E56w+n form under a library stream at the page's cumulative offset):", "", "| plant | page | stream | sign | F | lattice z | rank in window | accuracy | fillers (placed) | echoes (placed) |", "|---|---|---|---|---|---|---|---|---|---|"]
for p in plants: o.append(f"| {p['plant']} | {p['page']} | {p['stream']} | {p['sign']} | {int(p['F'])} | {p['z']:.1f} | {p['rank']} of {p['window']} | {p['acc']:.2f} | {p['fillers']} ({p['fillers_placed']}) | {p['echoes']} ({p['echoes_placed']}) |")
o += ["", "## Registered predictions", "", f"- L1 (every plant rank 1 at lattice z ≥ 8): {'holds' if L1 else 'fails'}.", f"- L2 (no cell at lattice z ≥ 8): largest {max(c['z'] for c in out_cells):.2f} → {'holds' if L2 else 'fails'}.",
      "- L3 (no readable decode): by inspection of the decode column.", "", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/c11_lattice_followup.py`.", ""]
(RESULTS / ("c11_lattice_smoke.md" if SMOKE else "c11_lattice.md")).write_text("\n".join(o)); json.dump(dict(cells=out_cells, plants=plants), open(RESULTS / ("c11_lattice_smoke.json" if SMOKE else "c11_lattice.json"), "w"), indent=1)
print("\n".join(o))
