"""One hand procedure as the cipher: the generator search of blind spot 4 (2026-10-31; private-table row A5).

Registration: results/hand_procedure_registration.md (commit 1c49a54, before any run).  A procedure writes c_i = T(s_i, p_i)
from a table T on the 29 runes and a state s_i taken from what was written before (the previous cipher rune, the rune five or
six back in the word, the word's running sum) or from the previous plaintext rune; with a reset at word starts or not, a
repeat rule (none, redraw, exclude), the §59 filler form or none, and the book's literal-F rule or none.  No key.
207 tables x 5 states x 2 resets x 3 rules x 2 fillers x 2 literal-F = 24,840 procedures (the registration first wrote 178 and 21,360, an arithmetic slip corrected before the run).
Part A (generator): each procedure writes Emerson's English into the 55 pages' rune counts, 20 replicates on shared plaintext
layouts; statistics mechanism_lane.measure plus W2 (share of two-rune words) and WM (mean word length); candidate = every
judged statistic within |z| < 3 of the replicates; candidates rerun at 200 replicates (survivor).
Part B (decoder): every cipher-state procedure inverts from the ciphertext alone and is applied to the 55 pages; plaintext-
state procedures try the 29 starts per reset unit; each decode scored by the rune 5-gram z (§27) and the §72 model-free z*.
Stages (STAGE=): chance, screen (SHARD/NSHARD), confirm, decode (SHARD/NSHARD), merge.  SMOKE=1 shrinks everything.
Reproduce: STAGE=chance .venv/bin/python -I src/hand_procedure_lane.py, then screen, confirm, decode, merge.
"""
import os, sys, re, json, time, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, english_to_runes, to_latin

t0 = time.time(); STAGE = os.environ.get("STAGE", "chance"); SMOKE = os.environ.get("SMOKE") == "1"
SHARD = int(os.environ.get("SHARD", 0)); NSHARD = int(os.environ.get("NSHARD", 1))
NREP = 3 if SMOKE else 20; NCONF = 10 if SMOKE else 200; NCHANCE = 10 if SMOKE else 200; N5 = 200 if SMOKE else 2000
P_FILL = 0.40; ZBAND = 3.0; S_IDX = 15; OUT = "hand_procedure_smoke" if SMOKE else "hand_procedure"
SEP = set('-.&$§')


def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


# ---------- pages (cipher and word ids), plaintext words
def parse_chunk(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, np.int64), np.array(wid, np.int64)


CHUNKS = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8").split("%")
LP2 = [parse_chunk(CHUNKS[k]) for k in range(16, 72)]; LP2 = [(c, w) for c, w in LP2 if len(c)]; assert len(LP2) == 55
LENS = [len(c) for c, _ in LP2]
_text = (RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(encoding="utf-8", errors="replace")
EW = [english_to_runes(w) for w in re.findall(r"[A-Za-z']+", _text)]; EW = [w for w in EW if w]

import mechanism_lane as M          # measure() and its LP2 reference; its own sweep is behind a __main__ guard


# ---------- tables
def grid_table(row_major, dead_first):
    """5 x 6 grid in Gematria order with one dead cell; c = rune at the cell-wise sum of the two coordinates (mod 5, mod 6),
    stepping once more in reading order when the sum lands on the dead cell.  Not a Latin square: one row entry repeats."""
    cells = list(range(30)); dead = 0 if dead_first else 29
    rune_cell = [i + 1 for i in range(29)] if dead_first else list(range(29))
    cell_rune = {c: r for r, c in enumerate(rune_cell)}
    def coord(cell): return (cell // 6, cell % 6) if row_major else (cell % 5, cell // 5)
    def cell_of(r, c): return r * 6 + c if row_major else c * 5 + r
    T = np.zeros((N, N), np.int64)
    for s in range(N):
        for p in range(N):
            (r1, c1), (r2, c2) = coord(rune_cell[s]), coord(rune_cell[p]); cell = cell_of((r1 + r2) % 5, (c1 + c2) % 6)
            if cell == dead: cell = (cell + 1) % 30
            T[s, p] = cell_rune[cell]
    return T


def build_tables():
    s = np.arange(N)[:, None]; p = np.arange(N)[None, :]; out = []
    for k in range(N):
        out.append((f"add k={k}", (s + p + k) % N)); out.append((f"sub k={k}", (s - p + k) % N)); out.append((f"rev k={k}", (p - s + k) % N))
        for a in (2, -2, 3, -3): out.append((f"mul a={a} k={k}", (a * s + p + k) % N))
    for rm in (True, False):
        for df in (False, True): out.append((f"grid {'row' if rm else 'col'}-major dead-{'first' if df else 'last'}", grid_table(rm, df)))
    return out


TABLES = build_tables(); assert len(TABLES) == 207
STATES = ("c1", "p1", "c5w", "c6w", "csum"); RESETS = ("word", "none"); RULES = ("none", "redraw", "exclude"); FILLS = (0.0, P_FILL); LITF = (False, True)
PROCS = [(ti, st, rs, ru, fi, lf) for ti in range(len(TABLES)) for st in STATES for rs in RESETS for ru in RULES for fi in FILLS for lf in LITF]
assert len(PROCS) == 24840
if SMOKE: PROCS = PROCS[::401][:60]


def label(pr):
    ti, st, rs, ru, fi, lf = pr
    return f"{TABLES[ti][0]} | {st} | reset {rs} | {ru} | fill {fi:.2f} | litF {'on' if lf else 'off'}"


def excl_row(T):
    """for the exclude rule: row s read with s removed (28 symbols); returns (N, 28)"""
    R = np.zeros((N, N - 1), np.int64)
    for s in range(N):
        R[s] = [x for x in T[s] if x != s][:N - 1] if (T[s] != s).sum() >= N - 1 else np.resize([x for x in T[s] if x != s], N - 1)
    return R


# ---------- the generator
def layouts(rng, n, fill):
    """n plaintext layouts of the 55 pages: list of (P, W) per page with P the plaintext runes (-1 = filler slot) and W word ids"""
    outs = []
    for _ in range(n):
        wi = int(rng.integers(0, len(EW) - 6000)); pages = []
        for L in LENS:
            P, W = [], []; w = 0
            while len(P) < L:
                word = list(EW[wi % len(EW)]); wi += 1
                if fill and len(word) >= 2 and rng.random() < fill: word.insert(int(rng.integers(0, len(word) + 1)), -1)
                P += word; W += [w] * len(word); w += 1
            pages.append((np.array(P[:L]), np.array(W[:L])))
        outs.append(pages)
    return outs


def write_page(P, W, T, R28, st, rs, ru, lf, rng):
    """one page through the procedure; returns the cipher runes"""
    L = len(P); c = np.empty(L, np.int64); prev = -1; s = 0; csum = 0; wpos = 0
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]:
            wpos = 0
            if rs == "word" or i == 0: s = 0; csum = 0
        else: wpos += 1
        p = P[i]
        if p == -1:                                                  # filler: uniform, unequal to its left neighbour, written like any rune
            x = int(rng.integers(0, N))
            while x == prev: x = int(rng.integers(0, N))
        elif lf and p == 0: x = 0
        else:
            if st == "c1": s_use = s
            elif st == "p1": s_use = s
            elif st == "c5w": s_use = c[i - 5] if wpos >= 5 else s
            elif st == "c6w": s_use = c[i - 6] if wpos >= 6 else s
            else: s_use = csum
            if ru == "exclude": x = int(R28[s_use, p % (N - 1)])
            else:
                x = int(T[s_use, p])
                if ru == "redraw" and x == prev: x = int(T[x, p])
        c[i] = x
        if not (lf and x == 0):                                      # a written F does not update the state under the literal-F rule
            if st == "p1": s = p if p != -1 else s
            else: s = x
            csum = (csum + x) % N
        prev = x
    return c


def measure_all(pages):
    out = M.measure(pages)
    lens = np.concatenate([np.diff(np.r_[np.flatnonzero(np.r_[True, w[1:] != w[:-1]]), len(w)]) for _, w in pages])
    out["W2"] = float((lens == 2).mean()); out["WM"] = float(lens.mean())
    return out


JUDGE = M.JUDGE + ["U", "W2", "WM"]
REF = None
def reference():
    global REF
    if REF is None: REF = measure_all(LP2)
    return REF


def generator_stats(pr, lays, rng):
    ti, st, rs, ru, fi, lf = pr; T = TABLES[ti][1]; R28 = excl_row(T) if ru == "exclude" else None
    rows = []
    for pages in lays:
        sim = [(write_page(P, W, T, R28, st, rs, ru, lf, rng), W) for P, W in pages]
        M.LENS_CUR = [len(c) for c, _ in sim]; rows.append(measure_all(sim))
    M.LENS_CUR = LENS
    return rows


def zscores(rows):
    ref = reference(); z = {}
    for k in JUDGE:
        v = np.array([r[k] for r in rows], float); sd = v.std() if v.std() > 0 else 1e-9
        z[k] = float((ref[k] - v.mean()) / sd)
    return z


# ---------- the decoder (Part B)
def invert(T):
    inv = np.full((N, N), -1, np.int64)
    for s in range(N):
        for p in range(N - 1, -1, -1): inv[s, T[s, p]] = p          # the lowest-index preimage wins where a grid row repeats
    return inv


def decode_page(C, W, T, Tinv, R28, st, rs, ru, lf, p0=0):
    """plaintext from the ciphertext alone; every state starts at F (p0) at a reset, so plaintext-state procedures invert too"""
    L = len(C); P = np.empty(L, np.int64); s = 0; csum = 0; wpos = 0
    if R28 is not None:
        Rinv = np.full((N, N), -1, np.int64)
        for a in range(N):
            for j in range(N - 2, -1, -1): Rinv[a, R28[a, j]] = j
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]:
            wpos = 0
            if rs == "word" or i == 0: s = p0 if st == "p1" else 0; csum = 0
        else: wpos += 1
        x = int(C[i])
        if lf and x == 0: P[i] = 0; continue
        if st in ("c1", "p1"): s_use = s
        elif st == "c5w": s_use = int(C[i - 5]) if wpos >= 5 else s
        elif st == "c6w": s_use = int(C[i - 6]) if wpos >= 6 else s
        else: s_use = csum
        p = int(Rinv[s_use, x]) if R28 is not None else int(Tinv[s_use, x])
        if p < 0: p = (7 * i + 11 * x + 13 * s_use) % N        # a cell the procedure could not have written (e.g. c equal to the state under the exclude rule): a position-hashed rune, not F, so the §72 scorer sees no fake alphabet (first run used F; results/hand_procedure_firstrun/)
        P[i] = p
        if st == "p1": s = p
        else: s = x
        csum = (csum + x) % N
    return P


# 5-gram scorer and the §72 scorer, with per-page nulls
_T5 = None
def t5():
    global _T5
    if _T5 is None:
        import ngram; _T5 = ngram.load_dense()
    return _T5


NULL5 = {}
def null5(L, rng):
    if L not in NULL5:
        import ngram
        s = ngram.score_batch(rng.integers(0, N, size=(N5, L)), t5()); NULL5[L] = (float(s.mean()), float(s.std()))
    return NULL5[L]


def page_z5(P, rng):
    import ngram
    mu, sd = null5(len(P), rng); return float((ngram.score_batch(P[None, :], t5())[0] - mu) / sd)


import nonprose_lane as NP           # the §72 scorer (stats, zify, moments); importing it builds nothing heavy
MOMX = {}
def page_zstar(P, W, pid, rng):
    if pid not in MOMX:
        C, wid = LP2[pid]; MOMX[pid] = NP.moments(C, wid, False, rng)
    starts, lens = NP.word_slots(W); return float(NP.zify(NP.stats(P[None, :], starts, lens), MOMX[pid]).max())


def decode_pages(pr, pages, rng):
    """median and best page 5-gram z, best page z*, the best page's text; pages = [(C, W)]"""
    ti, st, rs, ru, fi, lf = pr; T = TABLES[ti][1]; Tinv = invert(T); R28 = excl_row(T) if ru == "exclude" else None
    z5s, zss, best = [], [], (-1e9, None, None)
    for pid, (C, W) in enumerate(pages):
        P = decode_page(C, W, T, Tinv, R28, st, rs, ru, lf); z5 = page_z5(P, rng)     # the state starts at F by the family's definition, so a p1 procedure inverts without trying starts (the registration's 29-start clause is not needed)
        z5s.append(z5); zs_ = page_zstar(P, W, pid, rng) if pid < len(LP2) and pages is PAGES_REAL else float("nan"); zss.append(zs_)
        if z5 > best[0]: best = (z5, pid, to_latin(P)[:100])
    return dict(med5=float(np.median(z5s)), max5=float(np.max(z5s)), maxstar=float(np.nanmax(zss)) if not all(np.isnan(zss)) else float("nan"), best_page=best[1], text=best[2])


PAGES_REAL = LP2


# ---------- stages
def dump(name, obj): (RESULTS / f"{OUT}_{name}.json").write_text(json.dumps(obj, indent=1)); log("wrote", name)


def stage_chance():
    """the family-wide chance level of Part B: random procedures decoding uniform random page sets"""
    rng = np.random.default_rng(11); picks = rng.choice(len(PROCS), size=min(NCHANCE, len(PROCS)), replace=False); meds, maxs = [], []
    for n, j in enumerate(picks):
        fake = [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]
        r = decode_pages(PROCS[j], fake, rng); meds.append(r["med5"]); maxs.append(r["max5"])
        if n % 20 == 0: log("chance", n, label(PROCS[j]), round(r["med5"], 2), round(r["max5"], 2))
    res = {"n": len(picks), "median_max": float(max(meds)), "median_p99": float(np.percentile(meds, 99)), "best_max": float(max(maxs)), "meds": meds, "maxs": maxs}
    log("chance: largest median page z5", round(res["median_max"], 2), "largest single page", round(res["best_max"], 2)); dump("chance", res)


def stage_screen():
    rng = np.random.default_rng(100 + SHARD); ref = reference(); log("LP2 reference", {k: round(ref[k], 3) for k in JUDGE})
    lays = {fi: layouts(np.random.default_rng(7), NREP, fi) for fi in FILLS}      # shared plaintext layouts, the same for every procedure
    rows = []
    for n, pr in enumerate(PROCS[SHARD::NSHARD]):
        z = zscores(generator_stats(pr, lays[pr[4]], rng)); cand = all(abs(z[k]) < ZBAND for k in JUDGE); fails = [k for k in JUDGE if abs(z[k]) >= ZBAND]
        rows.append({"proc": list(pr), "label": label(pr), "z": z, "cand": cand, "fails": fails})
        if n % 200 == 0 or cand: log(n, label(pr), "CANDIDATE" if cand else f"fails {len(fails)}", {k: round(v, 1) for k, v in z.items()} if cand else "")
    dump(f"screen_{SHARD}", {"NREP": NREP, "rows": rows})


def stage_confirm():
    rng = np.random.default_rng(200); rows = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), [])
    cands = [r for r in rows if r["cand"]]; log(len(rows), "screened,", len(cands), "candidates")
    out = []
    for r in cands:
        pr = tuple(r["proc"]); lays = layouts(np.random.default_rng(17), NCONF, pr[4]); st = generator_stats(pr, lays, rng); z = zscores(st)
        surv = all(abs(z[k]) < ZBAND for k in JUDGE)
        out.append({"proc": list(pr), "label": r["label"], "z": z, "survivor": surv, "means": {k: float(np.mean([x[k] for x in st])) for k in JUDGE}})
        log(r["label"], "SURVIVOR" if surv else "fails", {k: round(v, 1) for k, v in z.items()})
    # the two reference rows, whatever they did
    refs = []
    for pr in ((0, "c1", "word", "none", 0.0, False), (0, "c1", "word", "exclude", 0.0, False)):
        lays = layouts(np.random.default_rng(17), NCONF, 0.0); st = generator_stats(pr, lays, rng); refs.append({"label": label(pr), "z": zscores(st), "means": {k: float(np.mean([x[k] for x in st])) for k in JUDGE}})
    dump("confirm", {"NCONF": NCONF, "rows": out, "reference_rows": refs})


def stage_decode():
    rng = np.random.default_rng(300 + SHARD); rows = []
    procs = [pr for pr in PROCS if pr[4] == 0.0][SHARD::NSHARD]          # the decoder ignores fillers, so the filler setting duplicates a decoder: 12,420 distinct decoders
    for n, pr in enumerate(procs):
        r = decode_pages(pr, LP2, rng); r.update(proc=list(pr), label=label(pr)); rows.append(r)
        if n % 500 == 0 or r["med5"] >= 4: log(n, label(pr), "med z5", round(r["med5"], 2), "max", round(r["max5"], 2), "z*", round(r["maxstar"], 2))
    dump(f"decode_{SHARD}", {"rows": rows})


def stage_merge():
    ch = json.loads((RESULTS / f"{OUT}_chance.json").read_text()); cf = json.loads((RESULTS / f"{OUT}_confirm.json").read_text())
    sc = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), [])
    dc = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_decode_*.json"))), [])
    ref = reference(); cands = [r for r in sc if r["cand"]]; surv = [r for r in cf["rows"] if r["survivor"]]
    nofill_cands = [r for r in cands if r["proc"][4] == 0.0]
    o = ["# One hand procedure as the cipher: the generator search of blind spot 4 (row A5)", "",
         f"Registration: `results/hand_procedure_registration.md`. {len(sc):,} procedures screened at {NREP} replicates; bands {', '.join(JUDGE)}; LP2 reference " + ", ".join(f"{k} {ref[k]:.3g}" for k in JUDGE) + ".", "",
         "## Part A, the generator", "", f"Candidates (every band within |z| < {ZBAND}): **{len(cands)}** of {len(sc):,} ({100*len(cands)/max(1,len(sc)):.2f} %); without fillers: {len(nofill_cands)}. Survivors at {cf['NCONF']} replicates: **{len(surv)}**.", ""]
    fails = {}
    for r in sc:
        for k in r["fails"]: fails[k] = fails.get(k, 0) + 1
    o += ["Bands failed, over the family: " + ", ".join(f"{k} {v:,}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])) + ".", "",
          "| reference row | " + " | ".join(JUDGE) + " |", "|---|" + "---|" * len(JUDGE)]
    for r in cf["reference_rows"]: o.append(f"| {r['label']} | " + " | ".join(f"{r['means'][k]:.3g} (z {r['z'][k]:+.1f})" for k in JUDGE) + " |")
    if cf["rows"]:
        o += ["", "| candidate | survivor | " + " | ".join(JUDGE) + " |", "|---|---|" + "---|" * len(JUDGE)]
        for r in cf["rows"]: o.append(f"| {r['label']} | {'yes' if r['survivor'] else 'no'} | " + " | ".join(f"{r['means'][k]:.3g} (z {r['z'][k]:+.1f})" for k in JUDGE) + " |")
    # the nearest misses: fewest failing bands, then smallest max |z|
    near = sorted(sc, key=lambda r: (len(r["fails"]), max(abs(v) for v in r["z"].values())))[:12]
    o += ["", "Nearest misses (fewest bands failed, then smallest largest |z|):", "", "| procedure | bands failed | largest \\|z\\| | " + " | ".join(JUDGE) + " |", "|---|---|---|" + "---|" * len(JUDGE)]
    for r in near: o.append(f"| {r['label']} | {len(r['fails'])} | {max(abs(v) for v in r['z'].values()):.1f} | " + " | ".join(f"{r['z'][k]:+.1f}" for k in JUDGE) + " |")
    o += ["", "## Part B, the decoder", "", f"Chance level ({ch['n']} random procedures on uniform page sets): largest median page 5-gram z {ch['median_max']:.2f}, largest single page {ch['best_max']:.2f}.", "",
          f"{len(dc):,} procedures applied to the 55 pages. Largest median page z5 **{max(r['med5'] for r in dc):.2f}**; largest single page z5 {max(r['max5'] for r in dc):.2f}; largest model-free z\\* {max(r['maxstar'] for r in dc):.2f}. Hits (median ≥ 6 and a page ≥ 10): **{sum(r['med5'] >= 6 and r['max5'] >= 10 for r in dc)}**.", "",
          "| procedure | median page z5 | best page z5 | best page | z\\* | text |", "|---|---|---|---|---|---|"]
    for r in sorted(dc, key=lambda r: -r["med5"])[:12]: o.append(f"| {r['label']} | {r['med5']:.2f} | {r['max5']:.2f} | {r['best_page']} | {r['maxstar']:.2f} | {r['text'][:60]} |")
    o += ["", "## Registered predictions", ""]
    h1 = next((r for r in cf["reference_rows"] if "none" in r["label"] and "exclude" not in r["label"]), None)
    o.append(f"- H1 (plain chain fails D): D {h1['means']['D']:.0f} against 86 → {'holds' if h1 and abs(h1['z']['D']) >= ZBAND else 'fails'}.")
    o.append(f"- H2 (< 1 % candidates): {len(cands)} of {len(sc):,} → {'holds' if len(cands) < 0.01 * len(sc) else 'fails'}.")
    o.append(f"- H3 (no candidate without fillers): {len(nofill_cands)} → {'holds' if not nofill_cands else 'fails'}.")
    o.append(f"- H4 (no survivor): {len(surv)} → {'holds' if not surv else 'fails'}.")
    top = max(r["med5"] for r in dc)
    o.append(f"- H5 (no decode hit; largest median within 1.0 of chance): {top:.2f} against chance {ch['median_max']:.2f} → {'holds' if top < ch['median_max'] + 1.0 and not any(r['med5'] >= 6 and r['max5'] >= 10 for r in dc) else 'fails'}.")
    o += ["", "Reading: written after the run, below. [stated — the tables]", "", "Reproduce: `STAGE=chance|screen|confirm|decode|merge .venv/bin/python -I src/hand_procedure_lane.py`.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"chance": stage_chance, "screen": stage_screen, "confirm": stage_confirm, "decode": stage_decode, "merge": stage_merge}[STAGE]()
