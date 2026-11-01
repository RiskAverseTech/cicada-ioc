"""T: the totient as a function of the words' numbers (registration: results/clue_table_registration.md, T and its amendment).

The key of a word or a rune is f(n) for a number n the text supplies: prevword (Gematria sum of the previous plaintext word),
prevcipher (of the previous cipher word), running (of every plaintext rune written on the page so far, per rune), runcipher
(of every cipher rune so far, per rune); f in phi(n) mod 29, phi(n) mod 28 + 1, (n - phi(n)) mod 29, phi(phi(n)) mod 29;
add, sub or beaufort.  48 members x fillers x repair x literal F = 384 procedures, 192 decoders, on §78's skeleton; Part B first
with §78's filler-placing beam (per-word filler hypotheses, §59 prior, a filler paying log 1/28, 5-gram score, beam 8), chance
= every decoder on 20 uniform page sets; four plants; Part A second, §73's bands.
Stages (STAGE=): plants, chance, decode, screen (SHARD/NSHARD), confirm, merge.  SMOKE=1 shrinks everything and decodes no page.
Reproduce: STAGE=plants .venv/bin/python -I src/totient_lane.py, then chance, decode, screen, confirm, merge.
"""
import os, sys, json, time
from math import log
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS, N, primes, to_latin

t0 = time.time(); STAGE = os.environ.get("STAGE", "plants"); SMOKE = os.environ.get("SMOKE") == "1"
SHARD = int(os.environ.get("SHARD", 0)); NSHARD = int(os.environ.get("NSHARD", 1))
NREP = 3 if SMOKE else 20; NCONF = 10 if SMOKE else 200; NSETS = 2 if SMOKE else 20
BEAM = 8; P_FILL = 0.40; ZBAND = 3.0; OUT = "totient" + ("_smoke" if SMOKE else "")
VALUE = primes(N)
def log_(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)

import autokey_lane as A
H = A.H; LP2, LENS, JUDGE = H.LP2, H.LENS, H.JUDGE; comb, uncomb, judge, S_CELLS = A.comb, A.uncomb, A.judge, A.S_CELLS

PHI_MAX = 60000
_phi = np.arange(PHI_MAX + 1)
for i in range(2, PHI_MAX + 1):
    if _phi[i] == i: _phi[i::i] -= _phi[i::i] // i
_phi[1] = 1; _phi[0] = 0
def phi(n): return int(_phi[n]) if n <= PHI_MAX else int(_phi[n % PHI_MAX])

SOURCES = ("prevword", "prevcipher", "running", "runcipher"); FUNCS = ("phi29", "phi28", "nonco", "phiphi"); SIGNS = ("add", "sub", "beaufort")
def f_of(fn, n):
    if fn == "phi29": return phi(n) % N
    if fn == "phi28": return phi(n) % 28 + 1
    if fn == "nonco": return (n - phi(n)) % N
    return phi(phi(n)) % N
MEMBERS = [(src, fn, sg) for src in SOURCES for fn in FUNCS for sg in SIGNS]; assert len(MEMBERS) == 48
FILLS = (0.0, P_FILL); REPAIRS = ("none", "redraw"); LITF = (False, True)
PROCS = [(mi, fi, ru, lf) for mi in range(len(MEMBERS)) for fi in FILLS for ru in REPAIRS for lf in LITF]; assert len(PROCS) == 384
DECODERS = [pr for pr in PROCS if pr[1] == 0.0]; assert len(DECODERS) == 192
def label(pr):
    mi, fi, ru, lf = pr; src, fn, sg = MEMBERS[mi]; return f"{src} {fn} {sg} | fill {fi:.2f} | {ru} | litF {'on' if lf else 'off'}"

# state: (prev plaintext word sum, prev cipher word sum, current plaintext word sum, current cipher word sum, running plaintext, running cipher)
STATE0 = (0, 0, 0, 0, 0, 0)
def new_word(s): return (s[2], s[3], 0, 0, s[4], s[5])
def key_for(s, member):
    src, fn, sg = member
    n = s[0] if src == "prevword" else s[1] if src == "prevcipher" else s[4] if src == "running" else s[5]
    return f_of(fn, n)
def after_plain(s, x, p): return (s[0], s[1], s[2] + VALUE[p], s[3] + VALUE[x], s[4] + VALUE[p], s[5] + VALUE[x])
def after_filler(s, x, lf): return s if (lf and x == 0) else (s[0], s[1], s[2], s[3] + VALUE[x], s[4], s[5] + VALUE[x])


def write_page(P, W, pr, rng):
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[2]; L = len(P); c = np.empty(L, np.int64); prev = -1; s = STATE0
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]: s = new_word(s)
        p = int(P[i])
        if p == -1:
            x = int(rng.integers(0, N))
            while x == prev: x = int(rng.integers(0, N))
            s = after_filler(s, x, lf)
        elif lf and p == 0: x = 0
        else:
            k = key_for(s, member); x = comb(p, k, sg, lf)
            if x == prev and ru == "redraw": x = comb(x, k, sg, lf)
            s = after_plain(s, x, p)
        c[i] = x; prev = x
    return c


LOG_NONE, LOG_KEEP, LOG_U28 = log(1 - P_FILL), log(P_FILL), log(1 / 28)
def lp5(pl, T):
    k = min(len(pl) - 1, 4); return float(T[k][tuple(pl[-k - 1:])])


def decode_beam(C, W, pr, beam=BEAM, fillers=True):
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[2]; T = H.t5() if fillers else None
    bounds = np.flatnonzero(np.r_[True, W[1:] != W[:-1], True]); hyps = [(0.0, [], STATE0, 0, [])]
    for a, b in zip(bounds[:-1], bounds[1:]):
        cs = [int(x) for x in C[a:b]]; Lw = len(cs); opts = [None] + (list(range(Lw)) if (Lw >= 2 and fillers) else []); new = []
        for sc0, pl0, s0, nf0, full0 in hyps:
            for fpos in opts:
                sc = sc0 + ((LOG_NONE if fpos is None else LOG_KEEP - log(Lw)) if Lw >= 2 else 0.0); pl = list(pl0); s = new_word(s0); nf = nf0; full = list(full0)
                for j, x in enumerate(cs):
                    if fpos == j: s = after_filler(s, x, lf); nf += 1; sc += LOG_U28; full.append(-1)
                    elif lf and x == 0: pl.append(0); sc += lp5(pl, T) if T is not None else 0.0; full.append(0)
                    else:
                        p = uncomb(x, key_for(s, member), sg, lf); pl.append(p); sc += lp5(pl, T) if T is not None else 0.0; s = after_plain(s, x, p); full.append(p)
                new.append((sc, pl, s, nf, full))
        new.sort(key=lambda h: -h[0]); hyps = new[:beam]
    best = hyps[0]; return np.array(best[1], np.int64), best[3], np.array(best[4], np.int64)


def decode_pages(pr, pages, rng):
    import ngram
    z5s, nfs, best = [], [], (-1e9, None, None)
    for pid, (C, W) in enumerate(pages):
        P, nf, _ = decode_beam(C, W, pr); mu, sd = H.null5(len(P), rng); z5 = float((ngram.score_batch(P[None, :], H.t5())[0] - mu) / sd); z5s.append(z5); nfs.append(nf)
        if z5 > best[0]: best = (z5, pid, to_latin(P)[:100])
    return dict(med5=float(np.median(z5s)), max5=float(np.max(z5s)), n6=int(sum(z >= 6 for z in z5s)), fillers=int(sum(nfs)), best_page=best[1], text=best[2])


def dump(name, obj): (RESULTS / f"{OUT}_{name}.json").write_text(json.dumps(obj, indent=1)); log_("wrote", name)
PLANTS = [("prevword", "phi29", "sub", 0.0), ("prevcipher", "nonco", "beaufort", 0.0), ("running", "phi29", "add", P_FILL), ("prevword", "phiphi", "sub", P_FILL)]


def stage_plants():
    rng = np.random.default_rng(400); out = []; lay = {fi: H.layouts(np.random.default_rng(23), 1, fi)[0] for fi in FILLS}
    decs = DECODERS if not SMOKE else DECODERS[::24]
    for src, fn, sg, fi in (PLANTS if not SMOKE else PLANTS[::3]):
        pr = (MEMBERS.index((src, fn, sg)), fi, "none", False); pages = [(write_page(P, W, pr, rng), W) for P, W in lay[fi]]
        planted = int(sum((P == -1).sum() for P, _ in lay[fi])) if fi else 0; own = decode_pages(pr, pages, rng)
        oth = sorted(((decode_pages(d, pages, rng)["med5"], label(d)) for d in decs if d[0] != pr[0]), reverse=True); rank = 1 + sum(1 for m, _ in oth if m > own["med5"])
        out.append(dict(plant=label(pr), own_med5=own["med5"], own_n6=own["n6"], rank=rank, n_decoders=len(oth) + 1, fillers_planted=planted, fillers_placed=own["fillers"], runner_up=oth[0], text=own["text"][:60]))
        log_("plant", label(pr), "own median z5", round(own["med5"], 2), "rank", rank, "fillers planted / placed", planted, own["fillers"], "runner-up", oth[0])
    dump("plants", {"rows": out})


def stage_chance():
    rng = np.random.default_rng(11 + SHARD); rows = []
    for n, pr in enumerate(DECODERS[SHARD::NSHARD] if not SMOKE else DECODERS[SHARD::NSHARD][:3]):
        for _ in range(NSETS):
            fake = [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]; r = decode_pages(pr, fake, rng); rows.append({"med5": r["med5"], "max5": r["max5"]})
        if n % 20 == 0: log_("chance", n, label(pr), round(rows[-1]["med5"], 2), round(rows[-1]["max5"], 2))
    dump(f"chance_{SHARD}", {"rows": rows})


def stage_decode():
    rng = np.random.default_rng(300 + SHARD); rows = []; pages = LP2 if not SMOKE else [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]
    for n, pr in enumerate(DECODERS[SHARD::NSHARD] if not SMOKE else DECODERS[SHARD::NSHARD][:3]):
        r = decode_pages(pr, pages, rng); r.update(proc=list(pr), label=label(pr)); rows.append(r)
        if n % 20 == 0 or r["med5"] >= 4: log_(n, label(pr), "med z5", round(r["med5"], 2), "max", round(r["max5"], 2), "fillers", r["fillers"])
    dump(f"decode_{SHARD}", {"rows": rows})


def generator_stats(pr, lays, rng):
    rows = []
    for pages in lays:
        sim = [(write_page(P, W, pr, rng), W) for P, W in pages]; H.M.LENS_CUR = [len(c) for c, _ in sim]; rows.append(H.measure_all(sim))
    H.M.LENS_CUR = LENS; return rows


def stage_screen():
    rng = np.random.default_rng(100 + SHARD); lays = {fi: H.layouts(np.random.default_rng(7), NREP, fi) for fi in FILLS}; rows = []
    for n, pr in enumerate(PROCS[SHARD::NSHARD] if not SMOKE else PROCS[SHARD::NSHARD][:6]):
        z = H.zscores(generator_stats(pr, lays[pr[1]], rng)); cand, sadm, fails = judge(z); rows.append({"proc": list(pr), "label": label(pr), "z": z, "cand": cand, "sadm": sadm, "fails": fails})
        if n % 50 == 0 or cand or sadm: log_(n, label(pr), "CANDIDATE" if cand else "S-ADMISSIBLE" if sadm else f"fails {len(fails)}")
    dump(f"screen_{SHARD}", {"NREP": NREP, "rows": rows})


def stage_confirm():
    rng = np.random.default_rng(200); rows = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), []); todo = [r for r in rows if r["cand"] or r["sadm"]]; out = []
    for r in todo:
        pr = tuple(r["proc"]); st = generator_stats(pr, H.layouts(np.random.default_rng(17), NCONF, pr[1]), rng); z = H.zscores(st); cand, sadm, fails = judge(z)
        out.append({"proc": list(pr), "label": r["label"], "z": z, "survivor": cand, "sadm": sadm, "means": {k: float(np.mean([x[k] for x in st])) for k in JUDGE}})
    log_(len(rows), "screened,", len(todo), "confirmed"); dump("confirm", {"NCONF": NCONF, "rows": out})


def stage_merge():
    g = lambda pat: sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_{pat}_*.json"))), [])
    pl = json.loads((RESULTS / f"{OUT}_plants.json").read_text())["rows"]; ch, dc, sc = g("chance"), g("decode"), g("screen"); cf = json.loads((RESULTS / f"{OUT}_confirm.json").read_text())
    ref = H.reference(); cands = [r for r in sc if r["cand"]]; sadm = [r for r in sc if r["sadm"]]; surv = [r for r in cf["rows"] if r["survivor"]]; sadm200 = [r for r in cf["rows"] if r["sadm"]]
    ch_med = max(r["med5"] for r in ch); ch_max = max(r["max5"] for r in ch); top = max(r["med5"] for r in dc); topmax = max(r["max5"] for r in dc)
    o = ["# T. The totient as a function of the words' numbers: decoder first, then the bands", "",
         f"Registration: `results/clue_table_registration.md` (T, amended). {len(MEMBERS)} members, {len(PROCS)} procedures, {len(DECODERS)} decoders; §78's beam decoder; chance = every decoder on {NSETS} uniform page sets ({len(ch):,} pairs); bands {', '.join(JUDGE)}.", "",
         "## Part B, the decoder (first)", "", "| plant | own decoder median z5 | pages at z5 >= 6 | rank among decoders | fillers planted / placed | runner-up |", "|---|---|---|---|---|---|"]
    for r in pl: o.append(f"| {r['plant']} | {r['own_med5']:.2f} | {r['own_n6']} of 55 | {r['rank']} of {r['n_decoders']} | {r['fillers_planted']} / {r['fillers_placed']} | {r['runner_up'][0]:.2f}, {r['runner_up'][1]} |")
    o += ["", f"Chance level: largest median page z5 {ch_med:.2f}, largest single page {ch_max:.2f}.", "", f"{len(dc)} decoders on the 55 pages: largest median page z5 **{top:.2f}**, largest single page {topmax:.2f}.", "",
          "| decoder | median page z5 | best page z5 | best page | fillers placed | text |", "|---|---|---|---|---|---|"]
    for r in sorted(dc, key=lambda r: -r["med5"])[:10]: o.append(f"| {r['label']} | {r['med5']:.2f} | {r['max5']:.2f} | {r['best_page']} | {r['fillers']} | {r['text'][:60]} |")
    fails = {}
    for r in sc:
        for k in r["fails"]: fails[k] = fails.get(k, 0) + 1
    o += ["", "## Part A, the generator (second)", "", f"S-admissible: **{len(sadm)}** at the screen, **{len(sadm200)}** at {cf['NCONF']}; candidates **{len(cands)}**, survivors **{len(surv)}**.",
          "Bands failed, over the family: " + ", ".join(f"{k} {v:,}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])) + ".", ""]
    near = sorted(sc, key=lambda r: (len(r["fails"]), max(abs(v) for v in r["z"].values())))[:8]
    o += ["| nearest miss | bands failed | " + " | ".join(JUDGE) + " |", "|---|---|" + "---|" * len(JUDGE)]
    for r in near: o.append(f"| {r['label']} | {len(r['fails'])} | " + " | ".join(f"{r['z'][k]:+.1f}" for k in JUDGE) + " |")
    t1 = all(r["own_med5"] >= 30 and r["rank"] == 1 for r in pl) and all(abs(r["fillers_placed"] - r["fillers_planted"]) <= 0.2 * r["fillers_planted"] for r in pl if r["fillers_planted"])
    o += ["", "## Registered predictions", "", f"- T1 (plants rank 1 at median z5 ≥ 30, fillers within 20 %): " + "; ".join(f"{r['plant'].split(' |')[0]} {r['own_med5']:.1f} rank {r['rank']}" for r in pl) + f" → {'holds' if t1 else 'fails'}.",
          f"- T2 (no page read): largest median {top:.2f} vs chance {ch_med:.2f}; largest page {topmax:.2f} vs {ch_max:.2f} → {'holds' if top < ch_med + 1.0 and topmax < ch_max + 1.0 else 'fails: read for sense'}.",
          f"- T3 (no S-admissible member): {len(sadm)} / {len(sadm200)} → {'holds' if not sadm200 else 'fails'}.", f"- T4 (no candidate): {len(cands)} → {'holds' if not cands else 'fails'}.",
          "", "Reading: written after the run, below. [stated — the tables]", "", "Reproduce: `STAGE=plants|chance|decode|screen|confirm|merge .venv/bin/python -I src/totient_lane.py`.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"plants": stage_plants, "chance": stage_chance, "decode": stage_decode, "screen": stage_screen, "confirm": stage_confirm, "merge": stage_merge}[STAGE]()
