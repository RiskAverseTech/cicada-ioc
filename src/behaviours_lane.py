"""The three behaviours as the switch of a self-keyed cipher, with a state beyond the word; decoder first.

Registration: results/behaviours_registration.md (commit 4a367ab, before any run).  At each plaintext rune the key takes one of
three behaviours: spend (a symbol of the text itself: the previous plaintext rune, or the next unconsumed plaintext rune of the
page from its start), hold (the previous key value) or adhere (the previous written cipher rune), chosen by a switch on a
three-valued state (previous plaintext class, previous cipher class, position in word, word index, running cipher sum, S count,
I count, previous word's Gematria sum; each mod 3) under one of the six assignments; c = p (+) k under add, sub or beaufort.
8 states x 6 assignments x 2 spend readings x 3 signs = 288 members x fillers x repair x literal F = 2,304 procedures, 1,152
decoders.  Part B (first): a beam decoder that places fillers per word slot with the §59 prior and the rune 5-gram score; six
plants; the 55 pages.  Part A (second): §73's harness against the thirteen bands.
Stages (STAGE=): plants, chance, decode, screen (SHARD/NSHARD on all four), confirm, merge.  SMOKE=1 shrinks everything and
decodes no page.  Reproduce: STAGE=plants .venv/bin/python -I src/behaviours_lane.py, then chance, decode, screen, confirm, merge.
"""
import os, sys, json, time, itertools
from math import log
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS, N, primes, to_latin

t0 = time.time(); STAGE = os.environ.get("STAGE", "plants"); SMOKE = os.environ.get("SMOKE") == "1"
SHARD = int(os.environ.get("SHARD", 0)); NSHARD = int(os.environ.get("NSHARD", 1))
NREP = 3 if SMOKE else 20; NCONF = 10 if SMOKE else 200; NCHANCE = 4 if SMOKE else 200; NOTHERS = 10 if SMOKE else 100
BEAM = 8; P_FILL = 0.40; ZBAND = 3.0; S_IDX = 15; I_IDX = 10; OUT = "behaviours" + ("_smoke" if SMOKE else "")
VALUE = primes(N)
def log_(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)

import autokey_lane as A                                             # §77's lane: sets the essay-body plaintext, gives comb / uncomb with literal F, the judge
H = A.H; LP2, LENS, JUDGE, VCLASS = H.LP2, H.LENS, H.JUDGE, H.VCLASS; comb, uncomb, judge, S_CELLS = A.comb, A.uncomb, A.judge, A.S_CELLS

# ---------- the family
STATES = ("pclass", "cclass", "wpos", "word", "csum", "scount", "icount", "prevword")
ASSIGN = list(itertools.permutations(("spend", "hold", "adhere")))
SPENDS = ("lag", "pointer"); SIGNS = ("add", "sub", "beaufort")
MEMBERS = [(st, ai, sp, sg) for st in STATES for ai in range(6) for sp in SPENDS for sg in SIGNS]; assert len(MEMBERS) == 288
FILLS = (0.0, P_FILL); REPAIRS = ("none", "redraw"); LITF = (False, True)
PROCS = [(mi, fi, ru, lf) for mi in range(len(MEMBERS)) for fi in FILLS for ru in REPAIRS for lf in LITF]; assert len(PROCS) == 2304
DECODERS = [pr for pr in PROCS if pr[1] == 0.0]; assert len(DECODERS) == 1152


def label(pr):
    mi, fi, ru, lf = pr; st, ai, sp, sg = MEMBERS[mi]
    return f"{st} {'/'.join(b[0] for b in ASSIGN[ai])} {sp} {sg} | fill {fi:.2f} | {ru} | litF {'on' if lf else 'off'}"


# key state: (kprev, ptr, m, wpos, csum3, scount3, icount3, prevword3, curword_sum, last_p, last_c)
STATE0 = (0, 0, -1, 0, 0, 0, 0, 0, 0, -1, -1)
def new_word(s): return (s[0], s[1], s[2] + 1, 0, s[4], s[5], s[6], s[8] % 3, 0, s[9], s[10])


def switch_value(s, st):
    if st == "pclass": return int(VCLASS[s[9]]) if s[9] >= 0 else 0
    if st == "cclass": return int(VCLASS[s[10]]) if s[10] >= 0 else 0
    if st == "wpos": return s[3] % 3
    if st == "word": return s[2] % 3
    if st == "csum": return s[4]
    if st == "scount": return s[5]
    if st == "icount": return s[6]
    return s[7]


def key_for(s, src, member):
    """the key for the next plaintext rune from state s and the plaintext runes src written so far; returns (k, new pointer)"""
    st, ai, sp, sg = member; beh = ASSIGN[ai][switch_value(s, st)]
    if beh == "spend":
        if sp == "lag": return (s[9] if s[9] >= 0 else 0), s[1]
        return ((src[s[1]], s[1] + 1) if s[1] < len(src) else (0, s[1]))
    if beh == "hold": return s[0], s[1]
    return (s[10] if s[10] >= 0 else 0), s[1]


def after_plain(s, x, p, k, ptr):
    """state after writing cipher x for plaintext p with key k (not a literal F)"""
    return (k, ptr, s[2], s[3] + 1, (s[4] + x) % 3, (s[5] + (x == S_IDX)) % 3, (s[6] + (x == I_IDX)) % 3, s[7], s[8] + VALUE[p], p, x)


def after_filler(s, x, lf):
    if lf and x == 0: return s[:3] + (s[3] + 1,) + s[4:]                 # a written F updates nothing but the position
    return (s[0], s[1], s[2], s[3] + 1, (s[4] + x) % 3, (s[5] + (x == S_IDX)) % 3, (s[6] + (x == I_IDX)) % 3, s[7], s[8], s[9], x)


def write_page(P, W, pr, rng):
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[3]
    L = len(P); c = np.empty(L, np.int64); prev = -1; s = STATE0; src = []
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]: s = new_word(s)
        p = int(P[i])
        if p == -1:
            x = int(rng.integers(0, N))
            while x == prev: x = int(rng.integers(0, N))
            s = after_filler(s, x, lf)
        elif lf and p == 0:
            x = 0; s = s[:3] + (s[3] + 1,) + s[4:]
        else:
            k, ptr = key_for(s, src, member); x = comb(p, k, sg, lf)
            if x == prev and ru == "redraw": x = comb(x, k, sg, lf)
            s = after_plain(s, x, p, k, ptr); src.append(p)
        c[i] = x; prev = x
    return c


# ---------- Part B: the beam decoder that places fillers
LOG_NONE, LOG_KEEP, LOG_U28 = log(1 - P_FILL), log(P_FILL), log(1 / 28)   # a filler rune is uniform among the 28 runes unequal to its left neighbour: it pays its own term, so every cipher rune is explained by exactly one term (amendment after the smoke round-trip)
def lp5(pl, T):
    k = min(len(pl) - 1, 4); return float(T[k][tuple(pl[-k - 1:])])


def decode_beam(C, W, pr, beam=BEAM, fillers=True):
    """returns (plaintext without fillers, fillers placed).  Hypotheses per word slot: no filler, or a filler at each rune of
    a slot of two or more; each carries the key state, the plaintext, and the cumulative 5-gram log-probability plus the prior.
    fillers=False is the exact inversion (one hypothesis, no filler), used by the tests."""
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[3]; T = H.t5() if fillers else None   # the exact mode scores nothing and needs no 5-gram tables (CI has no corpus)
    bounds = np.flatnonzero(np.r_[True, W[1:] != W[:-1], True])
    hyps = [(0.0, [], [], STATE0, 0, [])]                                 # score, plain (for scoring and output), src (state plaintext), state, fillers, full decode (-1 at a filler)
    for a, b in zip(bounds[:-1], bounds[1:]):
        cs = [int(x) for x in C[a:b]]; Lw = len(cs); opts = [None] + (list(range(Lw)) if (Lw >= 2 and fillers) else []); new = []
        for sc0, pl0, src0, s0, nf0, full0 in hyps:
            for fpos in opts:
                sc = sc0 + ((LOG_NONE if fpos is None else LOG_KEEP - log(Lw)) if Lw >= 2 else 0.0)
                pl = list(pl0); src = list(src0); s = new_word(s0); nf = nf0; full = list(full0)
                for j, x in enumerate(cs):
                    if fpos == j: s = after_filler(s, x, lf); nf += 1; sc += LOG_U28; full.append(-1)
                    elif lf and x == 0: pl.append(0); sc += lp5(pl, T) if T is not None else 0.0; s = s[:3] + (s[3] + 1,) + s[4:]; full.append(0)
                    else:
                        k, ptr = key_for(s, src, member); p = uncomb(x, k, sg, lf); pl.append(p); sc += lp5(pl, T) if T is not None else 0.0
                        s = after_plain(s, x, p, k, ptr); src.append(p); full.append(p)
                new.append((sc, pl, src, s, nf, full))
        new.sort(key=lambda h: -h[0]); hyps = new[:beam]
    best = hyps[0]; return np.array(best[1], np.int64), best[4], np.array(best[5], np.int64)


def decode_pages(pr, pages, rng):
    import ngram
    z5s, nfs, best = [], [], (-1e9, None, None)
    for pid, (C, W) in enumerate(pages):
        P, nf, _ = decode_beam(C, W, pr); mu, sd = H.null5(len(P), rng); z5 = float((ngram.score_batch(P[None, :], H.t5())[0] - mu) / sd)
        z5s.append(z5); nfs.append(nf)
        if z5 > best[0]: best = (z5, pid, to_latin(P)[:100])
    return dict(med5=float(np.median(z5s)), max5=float(np.max(z5s)), n6=int(sum(z >= 6 for z in z5s)), fillers=int(sum(nfs)), best_page=best[1], text=best[2])


def dump(name, obj): (RESULTS / f"{OUT}_{name}.json").write_text(json.dumps(obj, indent=1)); log_("wrote", name)


PLANTS = [("pclass", 0, "lag", "sub", 0.0), ("word", 1, "pointer", "add", 0.0), ("scount", 2, "lag", "beaufort", 0.0),
          ("csum", 3, "pointer", "sub", P_FILL), ("prevword", 4, "lag", "add", P_FILL), ("cclass", 5, "pointer", "beaufort", P_FILL)]
def other_decoders(): return [DECODERS[j] for j in np.random.default_rng(99).choice(len(DECODERS), size=NOTHERS, replace=False)]


def stage_plants():
    rng = np.random.default_rng(400 + SHARD); others = other_decoders(); out = []
    lay = {fi: H.layouts(np.random.default_rng(23), 1, fi)[0] for fi in FILLS}
    for pi, (st, ai, sp, sg, fi) in enumerate(PLANTS):
        if pi % NSHARD != SHARD or (SMOKE and pi not in (0, 3)): continue
        pr = (MEMBERS.index((st, ai, sp, sg)), fi, "none", False); pages = [(write_page(P, W, pr, rng), W) for P, W in lay[fi]]
        planted = int(sum((P == -1).sum() for P, _ in lay[fi])) if fi else 0
        own = decode_pages(pr, pages, rng); oth = sorted(((decode_pages(d, pages, rng)["med5"], label(d)) for d in others if d[0] != pr[0]), reverse=True)
        rank = 1 + sum(1 for m, _ in oth if m > own["med5"])
        out.append(dict(plant=label(pr), own_med5=own["med5"], own_n6=own["n6"], rank=rank, n_decoders=len(oth) + 1, fillers_planted=planted, fillers_placed=own["fillers"], runner_up=oth[0], text=own["text"][:60]))
        log_("plant", label(pr), "own median z5", round(own["med5"], 2), "pages >= 6:", own["n6"], "rank", rank, "fillers planted / placed", planted, own["fillers"], "runner-up", oth[0])
    dump(f"plants_{SHARD}", {"rows": out})


def stage_chance():
    rng = np.random.default_rng(11 + SHARD); picks = np.random.default_rng(11).choice(len(DECODERS), size=NCHANCE, replace=False)[SHARD::NSHARD]; rows = []
    for n, j in enumerate(picks):
        fake = [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]; r = decode_pages(DECODERS[j], fake, rng); rows.append({"med5": r["med5"], "max5": r["max5"], "fillers": r["fillers"]})
        if n % 10 == 0: log_("chance", n, label(DECODERS[j]), round(r["med5"], 2), round(r["max5"], 2), "fillers", r["fillers"])
    dump(f"chance_{SHARD}", {"rows": rows})


def stage_decode():
    rng = np.random.default_rng(300 + SHARD); rows = []
    pages = LP2 if not SMOKE else [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]
    for n, pr in enumerate(DECODERS[SHARD::NSHARD] if not SMOKE else DECODERS[SHARD::NSHARD][:3]):
        r = decode_pages(pr, pages, rng); r.update(proc=list(pr), label=label(pr)); rows.append(r)
        if n % 50 == 0 or r["med5"] >= 4: log_(n, label(pr), "med z5", round(r["med5"], 2), "max", round(r["max5"], 2), "fillers", r["fillers"])
    dump(f"decode_{SHARD}", {"rows": rows})


# ---------- Part A
def generator_stats(pr, lays, rng):
    rows = []
    for pages in lays:
        sim = [(write_page(P, W, pr, rng), W) for P, W in pages]; H.M.LENS_CUR = [len(c) for c, _ in sim]; rows.append(H.measure_all(sim))
    H.M.LENS_CUR = LENS; return rows


def stage_screen():
    rng = np.random.default_rng(100 + SHARD); ref = H.reference(); lays = {fi: H.layouts(np.random.default_rng(7), NREP, fi) for fi in FILLS}; rows = []
    for n, pr in enumerate(PROCS[SHARD::NSHARD] if not SMOKE else PROCS[SHARD::NSHARD][:6]):
        z = H.zscores(generator_stats(pr, lays[pr[1]], rng)); cand, sadm, fails = judge(z)
        rows.append({"proc": list(pr), "label": label(pr), "z": z, "cand": cand, "sadm": sadm, "fails": fails})
        if n % 100 == 0 or cand or sadm: log_(n, label(pr), "CANDIDATE" if cand else "S-ADMISSIBLE" if sadm else f"fails {len(fails)}", {k: round(v, 1) for k, v in z.items()} if (cand or sadm) else "")
    dump(f"screen_{SHARD}", {"NREP": NREP, "rows": rows})


def stage_confirm():
    rng = np.random.default_rng(200); rows = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), [])
    todo = [r for r in rows if r["cand"] or r["sadm"]]; log_(len(rows), "screened,", len(todo), "to confirm"); out = []
    for r in todo:
        pr = tuple(r["proc"]); st = generator_stats(pr, H.layouts(np.random.default_rng(17), NCONF, pr[1]), rng); z = H.zscores(st); cand, sadm, fails = judge(z)
        out.append({"proc": list(pr), "label": r["label"], "z": z, "survivor": cand, "sadm": sadm, "means": {k: float(np.mean([x[k] for x in st])) for k in JUDGE}})
        log_(r["label"], "SURVIVOR" if cand else "S-ADMISSIBLE" if sadm else "fails", {k: round(v, 1) for k, v in z.items()})
    dump("confirm", {"NCONF": NCONF, "rows": out})


def stage_merge():
    g = lambda pat: sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_{pat}_*.json"))), [])
    pl, ch, dc, sc = g("plants"), g("chance"), g("decode"), g("screen"); cf = json.loads((RESULTS / f"{OUT}_confirm.json").read_text())
    ref = H.reference(); cands = [r for r in sc if r["cand"]]; sadm = [r for r in sc if r["sadm"]]; surv = [r for r in cf["rows"] if r["survivor"]]; sadm200 = [r for r in cf["rows"] if r["sadm"]]
    ch_med = max(r["med5"] for r in ch); ch_max = max(r["max5"] for r in ch); top = max(r["med5"] for r in dc)
    o = ["# The three behaviours as the switch of a self-keyed cipher: decoder first, then the bands", "",
         f"Registration: `results/behaviours_registration.md`. {len(MEMBERS)} members, {len(PROCS):,} procedures, {len(DECODERS):,} decoders; beam {BEAM}; bands {', '.join(JUDGE)}; LP2 reference " + ", ".join(f"{k} {ref[k]:.3g}" for k in JUDGE) + ".", "",
         "## Part B, the decoder (first)", "", "| plant | own decoder median z5 | pages at z5 >= 6 | rank among decoders | fillers planted / placed | runner-up (median z5, decoder) |", "|---|---|---|---|---|---|"]
    for r in pl: o.append(f"| {r['plant']} | {r['own_med5']:.2f} | {r['own_n6']} of 55 | {r['rank']} of {r['n_decoders']} | {r['fillers_planted']} / {r['fillers_placed']} | {r['runner_up'][0]:.2f}, {r['runner_up'][1]} |")
    o += ["", f"Chance level ({len(ch)} random decoders on uniform page sets): largest median page z5 {ch_med:.2f}, largest single page {ch_max:.2f}.", "",
          f"{len(dc):,} decoders applied to the 55 pages. Largest median page z5 **{top:.2f}**; largest single page z5 {max(r['max5'] for r in dc):.2f}; pages at z5 >= 6 over all decoders {sum(r['n6'] for r in dc)}.", "",
          "| decoder | median page z5 | best page z5 | best page | fillers placed | text |", "|---|---|---|---|---|---|"]
    for r in sorted(dc, key=lambda r: -r["med5"])[:12]: o.append(f"| {r['label']} | {r['med5']:.2f} | {r['max5']:.2f} | {r['best_page']} | {r['fillers']} | {r['text'][:60]} |")
    fails = {}
    for r in sc:
        for k in r["fails"]: fails[k] = fails.get(k, 0) + 1
    o += ["", "## Part A, the generator (second)", "", f"S-admissible at the screen: **{len(sadm)}** of {len(sc):,}; at {cf['NCONF']} replicates: **{len(sadm200)}**. Candidates: **{len(cands)}**; survivors: **{len(surv)}**.",
          "Bands failed, over the family: " + ", ".join(f"{k} {v:,}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])) + ".", ""]
    if cf["rows"]:
        o += ["| confirmed row | survivor | S-admissible | " + " | ".join(JUDGE) + " |", "|---|---|---|" + "---|" * len(JUDGE)]
        for r in cf["rows"]: o.append(f"| {r['label']} | {'yes' if r['survivor'] else 'no'} | {'yes' if r['sadm'] else 'no'} | " + " | ".join(f"{r['means'][k]:.3g} (z {r['z'][k]:+.1f})" for k in JUDGE) + " |")
    near = sorted(sc, key=lambda r: (len(r["fails"]), max(abs(v) for v in r["z"].values())))[:12]
    o += ["", "Nearest misses (fewest bands failed, then smallest largest |z|):", "", "| procedure | bands failed | largest \\|z\\| | " + " | ".join(JUDGE) + " |", "|---|---|---|" + "---|" * len(JUDGE)]
    for r in near: o.append(f"| {r['label']} | {len(r['fails'])} | {max(abs(v) for v in r['z'].values()):.1f} | " + " | ".join(f"{r['z'][k]:+.1f}" for k in JUDGE) + " |")
    l6in = sum(1 for r in sc if "L6T" not in r["fails"])
    b1 = all(r["own_med5"] >= 6 and r["rank"] == 1 for r in pl) and all(abs(r["fillers_placed"] - r["fillers_planted"]) <= 0.2 * r["fillers_planted"] for r in pl if r["fillers_planted"])
    o += ["", "## Registered predictions", "",
          f"- B1 (six plants read at rank 1; filler plants' fillers placed within 20 %): " + "; ".join(f"{r['plant'].split(' |')[0]} {r['own_med5']:.1f} rank {r['rank']} fillers {r['fillers_planted']}/{r['fillers_placed']}" for r in pl) + f" → {'holds' if b1 else 'fails'}.",
          f"- B2 (no page read, amended: median within 1.0 of the chance maximum median, single page within 1.0 of the chance maximum single page): largest median {top:.2f} against chance {ch_med:.2f}; largest single page {max(r['max5'] for r in dc):.2f} against chance {ch_max:.2f} → {'holds' if top < ch_med + 1.0 and max(r['max5'] for r in dc) < ch_max + 1.0 else 'fails: read for sense'}.",
          f"- B3 (no S-admissible member): {len(sadm)} at the screen, {len(sadm200)} at {cf['NCONF']} → {'holds' if not sadm200 else 'fails'}.",
          f"- B4 (no candidate; under one in ten inside L6T): {len(cands)} candidates, {l6in} of {len(sc):,} inside L6T → {'holds' if not cands and l6in < 0.1 * len(sc) else 'fails'}.",
          "", "Reading: written after the run, below. [stated — the tables]", "", "Reproduce: `STAGE=plants|chance|decode|screen|confirm|merge .venv/bin/python -I src/behaviours_lane.py`.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"plants": stage_plants, "chance": stage_chance, "decode": stage_decode, "screen": stage_screen, "confirm": stage_confirm, "merge": stage_merge}[STAGE]()
