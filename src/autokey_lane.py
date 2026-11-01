"""Word-level and two-state autokeys: generators against the thirteen bands (the S cell primary) and decoders of the 55 pages.

Registration: results/autokey_registration.md (commit d353f3b, before any run).  The text keys itself: c = p (+) k under add,
sub or beaufort, with k drawn from one of five sub-families (W the previous word as the key; G the previous word's number;
R one key rune consumed per word; L a word-aware rune autokey at lag d; T two sources, the previous plaintext or cipher rune,
chosen by a stated switch), on §73's skeleton (fillers 0 or 0.40, repeat rule none or redraw, literal-F off or on).
183 members x 2 x 2 x 2 = 1,464 procedures; 732 distinct decoders (the filler setting does not change a decoder).
Part A: §73's harness (hand_procedure_lane.layouts / measure_all / zscores), 20 replicates, candidate = all bands |z| < 3,
S-admissible = L5S, L5, D, U, Sfreq within |z| < 3; both rerun at 200.  Part B: filler-blind inversion of every page, rune
5-gram z and the §72 z*; six plants.  Stages (STAGE=): chance, screen (SHARD/NSHARD), confirm, decode (SHARD/NSHARD), plants,
merge.  SMOKE=1 shrinks everything and decodes no page.
Reproduce: STAGE=chance .venv/bin/python -I src/autokey_lane.py, then screen, confirm, decode, plants, merge.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS, N, primes, to_latin

t0 = time.time(); STAGE = os.environ.get("STAGE", "chance"); SMOKE = os.environ.get("SMOKE") == "1"
SHARD = int(os.environ.get("SHARD", 0)); NSHARD = int(os.environ.get("NSHARD", 1))
NREP = 3 if SMOKE else 20; NCONF = 10 if SMOKE else 200; NCHANCE = 10 if SMOKE else 200
P_FILL = 0.40; ZBAND = 3.0; S_IDX = 15; I_IDX = 10; OUT = "autokey" + ("_smoke" if SMOKE else "")
VALUE = np.array(primes(N), np.int64)                                 # Gematria prime values 2 .. 109


def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


import hand_procedure_lane as H                                      # §73's harness: layouts, bands, scorers; its sweep is behind a __main__ guard
LP2, LENS, JUDGE, VCLASS = H.LP2, H.LENS, H.JUDGE, H.VCLASS
# the plaintext is the essay body only: the Project Gutenberg licence at the file's end repeats GUTENBERG (U-T and E-R five
# apart, both fifteen apart in Gematria order) and alone made half the S coincidences of results/s_autokey_check.md (lesson twelve)
import re as _re
from lp import RAW as _RAW, english_to_runes as _e2r
_t = (_RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(encoding="utf-8", errors="replace")
_t = _t[_t.find("*** START OF"):_t.find("*** END OF")]
H.EW = [w for w in (_e2r(x) for x in _re.findall(r"[A-Za-z']+", _t)) if w]; assert 70000 < len(H.EW) < 76000, len(H.EW)   # 78,017 words in the file, about 3,100 of them header and licence
S_CELLS = ("L5S", "L5", "D", "U", "Sfreq")

# ---------- the family
SIGNS = ("add", "sub", "beaufort")
def comb(p, k, sign, lf=False):
    """c = p (+) k; under the literal-F rule (amendment, after the smoke round-trip) the 28 non-F runes are enciphered
    among themselves (indices 1..28, mod 28), so that a written F is always a plaintext F and the cipher inverts"""
    if lf: return 1 + ((p - 1 + k) % 28 if sign == "add" else (p - 1 - k) % 28 if sign == "sub" else (k - (p - 1)) % 28)
    return (p + k) % N if sign == "add" else (p - k) % N if sign == "sub" else (k - p) % N
def uncomb(c, k, sign, lf=False):
    if lf: return 1 + ((c - 1 - k) % 28 if sign == "add" else (c - 1 + k) % 28 if sign == "sub" else (k - (c - 1)) % 28)
    return (c - k) % N if sign == "add" else (c + k) % N if sign == "sub" else (k - c) % N


def build_members():
    m = []
    for src in ("plain", "cipher"):
        for v in ("fwd", "rev", "pad"):
            for sg in SIGNS: m.append(("W", src, v, sg))
    for src in ("plain", "cipher"):
        for v in ("isum", "gsum", "gsum28", "first", "last", "len"):
            for sg in SIGNS: m.append(("G", src, v, sg))
    for src in ("plain", "cipher"):
        for sg in SIGNS: m.append(("R", src, None, sg))
    for src in ("plain", "cipher"):
        for d in range(1, 7):
            for b in ("cont", "reset"):
                for sg in SIGNS: m.append(("L", src, (d, b), sg))
    rules = [("parity", None), ("afterS", "next"), ("afterS", "word"), ("afterS", "toggle"), ("afterI", "next"), ("afterI", "word"), ("afterI", "toggle"), ("vowel", None)]
    for rule, scope in rules:
        for order in ("AB", "BA"):
            for sg in SIGNS: m.append(("T", "two", (rule, scope, order), sg))
    for sg in SIGNS: m.append(("T", "two", ("both", None, "AB"), sg))
    return m


MEMBERS = build_members(); assert len(MEMBERS) == 183, len(MEMBERS)
FILLS = (0.0, P_FILL); REPAIRS = ("none", "redraw"); LITF = (False, True)
PROCS = [(mi, fi, ru, lf) for mi in range(len(MEMBERS)) for fi in FILLS for ru in REPAIRS for lf in LITF]; assert len(PROCS) == 1464
POSITIVE_CONTROL = (MEMBERS.index(("L", "plain", (1, "cont"), "sub")), 0.0, "none", False)


def label(pr):
    mi, fi, ru, lf = pr; fam, src, v, sg = MEMBERS[mi]
    vs = "" if v is None else (f"d={v[0]} {v[1]}" if fam == "L" else " ".join(str(x) for x in v if x is not None) if fam == "T" else str(v))
    return f"{fam} {src} {vs} {sg} | fill {fi:.2f} | {ru} | litF {'on' if lf else 'off'}".replace("  ", " ")


def word_number(runes, v):
    if not runes: return 0
    r = np.asarray(runes)
    if v == "isum": return int(r.sum() % N)
    if v == "gsum": return int(VALUE[r].sum() % N)
    if v == "gsum28": return int(VALUE[r].sum() % 28 + 1)
    if v == "first": return int(r[0])
    if v == "last": return int(r[-1])
    return len(r) % N


class Keyer:
    """the key for the next rune, from what was written so far; one instance per page, fed by the generator or the decoder"""
    def __init__(self, member, litf):
        self.fam, self.src, self.v, self.sg = member; self.litf = litf
        self.ch, self.ph = [], []                      # state-updating cipher and plaintext histories (a written F updates nothing under literal-F)
        self.cw, self.pw = [], []                      # the current word's cipher and plaintext runes
        self.prev_cw, self.prev_pw = [], []            # the previous word's
        self.page_c, self.page_p = [], []              # every written cipher rune; every plaintext rune (fillers excluded)
        self.m = -1; self.w = 0; self.flag = False; self.flag_word = False

    def new_word(self):
        self.m += 1; self.w = 0; self.prev_cw, self.prev_pw = self.cw, self.pw; self.cw, self.pw = [], []; self.flag_word = False

    def key(self):
        fam, src, v, w = self.fam, self.src, self.v, self.w
        if fam == "W":
            kw = (self.prev_pw if src == "plain" else self.prev_cw) if self.m > 0 else []
            if not kw: return 0
            if v == "fwd": return kw[w % len(kw)]
            if v == "rev": return kw[len(kw) - 1 - (w % len(kw))]
            return kw[w] if w < len(kw) else 0
        if fam == "G":
            return word_number(self.prev_pw if src == "plain" else self.prev_cw, v) if self.m > 0 else 0
        if fam == "R":
            seq = self.page_p if src == "plain" else self.page_c
            return seq[self.m] if self.m < len(seq) else 0
        if fam == "L":
            d, b = v
            if b == "reset" and w < d: return 0
            hist = self.ph if src == "plain" else self.ch
            return hist[-d] if len(hist) >= d else 0
        rule, scope, order = v
        A = self.ph[-1] if self.ph else 0; B = self.ch[-1] if self.ch else 0
        if rule == "both": return (A + B) % N
        if order == "BA": A, B = B, A
        if rule == "parity": useB = (w % 2 == 1)
        elif rule == "vowel": useB = bool(self.ph) and VCLASS[self.ph[-1]] == 0
        elif scope == "next": useB = self.flag
        elif scope == "word": useB = self.flag_word
        else: useB = self.flag
        return B if useB else A

    def written(self, x, p):
        """record a written cipher rune x with plaintext p (-1 for a filler)"""
        skip = self.litf and x == 0
        self.page_c.append(x); self.cw.append(x)
        if p != -1: self.page_p.append(p); self.pw.append(p)
        if not skip:
            self.ch.append(x)
            if p != -1: self.ph.append(p)
        if self.fam == "T":
            rule, scope, _ = self.v; mark = S_IDX if rule == "afterS" else I_IDX if rule == "afterI" else None
            if mark is not None:
                if scope == "next": self.flag = (x == mark)
                elif scope == "word":
                    if x == mark: self.flag_word = True
                elif x == mark: self.flag = not self.flag
        self.w += 1


def write_page(P, W, pr, rng):
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[3]; K = Keyer(member, lf)
    L = len(P); c = np.empty(L, np.int64); prev = -1
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]: K.new_word()
        p = int(P[i])
        if p == -1:
            x = int(rng.integers(0, N))
            while x == prev: x = int(rng.integers(0, N))
        elif lf and p == 0: x = 0
        else:
            k = K.key(); x = comb(p, k, sg, lf)
            if x == prev and ru == "redraw": x = comb(x, k, sg, lf)
        c[i] = x; K.written(x, p); prev = x
    return c


def decode_page(C, W, pr):
    """plaintext from the ciphertext alone, filler-blind; repairs are decoded as plain cells"""
    mi, fi, ru, lf = pr; member = MEMBERS[mi]; sg = member[3]; K = Keyer(member, lf)
    L = len(C); P = np.empty(L, np.int64)
    for i in range(L):
        if i == 0 or W[i] != W[i - 1]: K.new_word()
        x = int(C[i])
        if lf and x == 0: p = 0
        else: p = uncomb(x, K.key(), sg, lf)
        P[i] = p; K.written(x, p)
    return P


# ---------- Part A
def generator_stats(pr, lays, rng):
    rows = []
    for pages in lays:
        sim = [(write_page(P, W, pr, rng), W) for P, W in pages]
        H.M.LENS_CUR = [len(c) for c, _ in sim]; rows.append(H.measure_all(sim))
    H.M.LENS_CUR = LENS
    return rows


def judge(z):
    cand = all(abs(z[k]) < ZBAND for k in JUDGE); sadm = all(abs(z[k]) < ZBAND for k in S_CELLS)
    return cand, sadm, [k for k in JUDGE if abs(z[k]) >= ZBAND]


# ---------- Part B
def decode_pages(pr, pages, real, rng):
    z5s, zss, best = [], [], (-1e9, None, None)
    for pid, (C, W) in enumerate(pages):
        P = decode_page(C, W, pr); z5 = H.page_z5(P, rng); z5s.append(z5)
        zss.append(H.page_zstar(P, W, pid, rng) if real else float("nan"))
        if z5 > best[0]: best = (z5, pid, to_latin(P)[:100])
    return dict(med5=float(np.median(z5s)), max5=float(np.max(z5s)), n6=int(sum(z >= 6 for z in z5s)),
                maxstar=float(np.nanmax(zss)) if real else float("nan"), best_page=best[1], text=best[2])


DECODERS = [pr for pr in PROCS if pr[1] == 0.0]; assert len(DECODERS) == 732
def dump(name, obj): (RESULTS / f"{OUT}_{name}.json").write_text(json.dumps(obj, indent=1)); log("wrote", name)


def stage_chance():
    rng = np.random.default_rng(11); picks = rng.choice(len(DECODERS), size=min(NCHANCE, len(DECODERS)), replace=False); meds, maxs = [], []
    for n, j in enumerate(picks):
        fake = [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]
        r = decode_pages(DECODERS[j], fake, False, rng); meds.append(r["med5"]); maxs.append(r["max5"])
        if n % 20 == 0: log("chance", n, label(DECODERS[j]), round(r["med5"], 2), round(r["max5"], 2))
    res = {"n": len(picks), "median_max": float(max(meds)), "best_max": float(max(maxs)), "meds": meds, "maxs": maxs}
    log("chance: largest median page z5", round(res["median_max"], 2), "largest single page", round(res["best_max"], 2)); dump("chance", res)


def stage_screen():
    rng = np.random.default_rng(100 + SHARD); ref = H.reference(); log("LP2 reference", {k: round(ref[k], 3) for k in JUDGE})
    lays = {fi: H.layouts(np.random.default_rng(7), NREP, fi) for fi in FILLS}
    rows = []
    procs = PROCS[SHARD::NSHARD] if not SMOKE else [POSITIVE_CONTROL] + PROCS[SHARD::NSHARD][:6]
    for n, pr in enumerate(procs):
        z = H.zscores(generator_stats(pr, lays[pr[1]], rng)); cand, sadm, fails = judge(z)
        rows.append({"proc": list(pr), "label": label(pr), "z": z, "cand": cand, "sadm": sadm, "fails": fails})
        if n % 100 == 0 or cand or sadm: log(n, label(pr), "CANDIDATE" if cand else "S-ADMISSIBLE" if sadm else f"fails {len(fails)}", {k: round(v, 1) for k, v in z.items()} if (cand or sadm) else "")
    dump(f"screen_{SHARD}", {"NREP": NREP, "rows": rows})


def stage_confirm():
    rng = np.random.default_rng(200); rows = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), [])
    todo = [r for r in rows if r["cand"] or r["sadm"]]; log(len(rows), "screened,", len(todo), "to confirm")
    out = []
    for r in todo + [{"proc": list(POSITIVE_CONTROL), "label": label(POSITIVE_CONTROL), "control": True}]:
        pr = tuple(r["proc"]); st = generator_stats(pr, H.layouts(np.random.default_rng(17), NCONF, pr[1]), rng); z = H.zscores(st); cand, sadm, fails = judge(z)
        out.append({"proc": list(pr), "label": r["label"], "z": z, "survivor": cand, "sadm": sadm, "control": r.get("control", False),
                    "means": {k: float(np.mean([x[k] for x in st])) for k in JUDGE}})
        log(r["label"], "SURVIVOR" if cand else "S-ADMISSIBLE" if sadm else "fails", {k: round(v, 1) for k, v in z.items()})
    dump("confirm", {"NCONF": NCONF, "rows": out})


def stage_decode():
    rng = np.random.default_rng(300 + SHARD); rows = []
    pages = LP2 if not SMOKE else [(rng.integers(0, N, size=len(C)), W) for C, W in LP2]       # the smoke decodes no page
    for n, pr in enumerate(DECODERS[SHARD::NSHARD] if not SMOKE else DECODERS[SHARD::NSHARD][:5]):
        r = decode_pages(pr, pages, not SMOKE, rng); r.update(proc=list(pr), label=label(pr)); rows.append(r)
        if n % 100 == 0 or r["med5"] >= 4: log(n, label(pr), "med z5", round(r["med5"], 2), "max", round(r["max5"], 2), "z*", round(r["maxstar"], 2))
    dump(f"decode_{SHARD}", {"rows": rows})


PLANTS = [("W", "cipher", "fwd", "sub", 0.0), ("L", "cipher", (2, "reset"), "add", 0.0), ("T", "two", ("afterS", "word", "AB"), "beaufort", 0.0),
          ("G", "cipher", "gsum", "sub", P_FILL), ("W", "plain", "fwd", "add", P_FILL), ("L", "plain", (1, "cont"), "sub", P_FILL)]


def stage_plants():
    rng = np.random.default_rng(400); out = []
    lay = H.layouts(np.random.default_rng(23), 1, 0.0)[0]; layf = H.layouts(np.random.default_rng(23), 1, P_FILL)[0]
    decs = DECODERS if not SMOKE else DECODERS[::40]
    for fam, src, v, sg, fi in PLANTS:
        pr = (MEMBERS.index((fam, src, v, sg)), fi, "none", False); pages = [(write_page(P, W, pr, rng), W) for P, W in (layf if fi else lay)]
        own = decode_pages(pr, pages, False, rng)
        others = sorted(((decode_pages(d, pages, False, rng)["med5"], label(d)) for d in decs if d != (pr[0], 0.0, "none", False)), reverse=True)
        rank = 1 + sum(1 for m, _ in others if m > own["med5"])
        out.append({"plant": label(pr), "own_med5": own["med5"], "own_n6": own["n6"], "rank": rank, "n_decoders": len(decs) + 1, "runner_up": others[0] if others else None, "text": own["text"][:60]})
        log("plant", label(pr), "own median z5", round(own["med5"], 2), "pages >= 6:", own["n6"], "rank", rank, "runner-up", others[0] if others else None)
    dump("plants", {"rows": out})


def stage_merge():
    ch = json.loads((RESULTS / f"{OUT}_chance.json").read_text()); cf = json.loads((RESULTS / f"{OUT}_confirm.json").read_text()); pl = json.loads((RESULTS / f"{OUT}_plants.json").read_text())
    sc = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_screen_*.json"))), [])
    dc = sum((json.loads(p.read_text())["rows"] for p in sorted(RESULTS.glob(f"{OUT}_decode_*.json"))), [])
    ref = H.reference(); cands = [r for r in sc if r["cand"]]; sadm = [r for r in sc if r["sadm"]]
    surv = [r for r in cf["rows"] if r["survivor"] and not r["control"]]; sadm200 = [r for r in cf["rows"] if r["sadm"] and not r["control"]]
    ctrl = next(r for r in cf["rows"] if r["control"])
    o = ["# Word-level and two-state autokeys: generators against the bands, decoders of the pages", "",
         f"Registration: `results/autokey_registration.md`. {len(sc):,} procedures screened at {sc and json.loads(sorted(RESULTS.glob(f'{OUT}_screen_*.json'))[0].read_text())['NREP']} replicates; bands {', '.join(JUDGE)}; LP2 reference " + ", ".join(f"{k} {ref[k]:.3g}" for k in JUDGE) + ".", "",
         "## Part A, the generator", "",
         f"S-admissible members (L5S, L5, D, U, Sfreq all within |z| < {ZBAND}) at the screen: **{len(sadm)}** of {len(sc):,}; at {cf['NCONF']} replicates: **{len(sadm200)}**.",
         f"Candidates (every band within |z| < {ZBAND}): **{len(cands)}**; survivors at {cf['NCONF']}: **{len(surv)}**.", ""]
    fails = {}
    for r in sc:
        for k in r["fails"]: fails[k] = fails.get(k, 0) + 1
    o += ["Bands failed, over the family: " + ", ".join(f"{k} {v:,}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])) + ".", "",
          f"Positive control ({ctrl['label']}, {cf['NCONF']} replicates): " + ", ".join(f"{k} {ctrl['means'][k]:.3g} (z {ctrl['z'][k]:+.1f})" for k in JUDGE) + ".", ""]
    if cf["rows"]:
        o += ["| confirmed row | survivor | S-admissible | " + " | ".join(JUDGE) + " |", "|---|---|---|" + "---|" * len(JUDGE)]
        for r in cf["rows"]: o.append(f"| {r['label']} | {'yes' if r['survivor'] else 'no'} | {'yes' if r['sadm'] else 'no'} | " + " | ".join(f"{r['means'][k]:.3g} (z {r['z'][k]:+.1f})" for k in JUDGE) + " |")
    # S cell across the family, by sub-family: how many S pairs each predicts (z sign tells the side)
    o += ["", "Nearest to the S cell (smallest |z| on L5S, with the four companion cells):", "", "| procedure | bands failed | L5S z | L5 z | D z | U z | Sfreq z | L6T z |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(sc, key=lambda r: abs(r["z"]["L5S"]))[:12]: o.append(f"| {r['label']} | {len(r['fails'])} | " + " | ".join(f"{r['z'][k]:+.1f}" for k in ("L5S", "L5", "D", "U", "Sfreq", "L6T")) + " |")
    near = sorted(sc, key=lambda r: (len(r["fails"]), max(abs(v) for v in r["z"].values())))[:12]
    o += ["", "Nearest misses on all bands (fewest failed, then smallest largest |z|):", "", "| procedure | bands failed | largest \\|z\\| | " + " | ".join(JUDGE) + " |", "|---|---|---|" + "---|" * len(JUDGE)]
    for r in near: o.append(f"| {r['label']} | {len(r['fails'])} | {max(abs(v) for v in r['z'].values()):.1f} | " + " | ".join(f"{r['z'][k]:+.1f}" for k in JUDGE) + " |")
    o += ["", "## Part B, the decoder", "", f"Chance level ({ch['n']} random decoders on uniform page sets): largest median page z5 {ch['median_max']:.2f}, largest single page {ch['best_max']:.2f}.", "",
          "| plant | own decoder median z5 | pages at z5 >= 6 | rank among decoders | runner-up (median z5, decoder) |", "|---|---|---|---|---|"]
    for r in pl["rows"]: o.append(f"| {r['plant']} | {r['own_med5']:.2f} | {r['own_n6']} of 55 | {r['rank']} of {r['n_decoders']} | {r['runner_up'][0]:.2f}, {r['runner_up'][1]} |")
    top = max(r["med5"] for r in dc)
    o += ["", f"{len(dc):,} decoders applied to the 55 pages. Largest median page z5 **{top:.2f}**; largest single page z5 {max(r['max5'] for r in dc):.2f}; pages at z5 >= 6 over all decoders {sum(r['n6'] for r in dc)}; largest z\\* {max(r['maxstar'] for r in dc):.2f} (judged per decoder above 10, lesson eleven).", "",
          "| decoder | median page z5 | best page z5 | best page | z\\* | text |", "|---|---|---|---|---|---|"]
    for r in sorted(dc, key=lambda r: -r["med5"])[:12]: o.append(f"| {r['label']} | {r['med5']:.2f} | {r['max5']:.2f} | {r['best_page']} | {r['maxstar']:.2f} | {r['text'][:60]} |")
    o += ["", "## Registered predictions", ""]
    o.append(f"- A1 (no S-admissible member; the control, amended, predicts about four S pairs and fails U and Sfreq): {len(sadm200)} S-admissible at {cf['NCONF']}; control L5S {ctrl['means']['L5S']:.1f} against 11 (z {ctrl['z']['L5S']:+.1f}), U z {ctrl['z']['U']:+.1f}, Sfreq z {ctrl['z']['Sfreq']:+.1f} → {'holds' if not sadm200 and abs(ctrl['z']['U']) >= ZBAND and abs(ctrl['z']['Sfreq']) >= ZBAND else 'fails'}.")
    o.append(f"- A2 (no survivor; candidates < 1 %; every member fails L6T): {len(surv)} survivors, {len(cands)} candidates, L6T failed by {fails.get('L6T', 0):,} of {len(sc):,} → {'holds' if not surv and len(cands) < 0.01 * len(sc) and fails.get('L6T', 0) == len(sc) else 'fails'}.")
    nf = [r for r in pl["rows"] if "fill 0.00" in r["plant"]]; cf_ = [r for r in pl["rows"] if "fill 0.40" in r["plant"] and " cipher " in r["plant"]]; pf = [r for r in pl["rows"] if "fill 0.40" in r["plant"] and " plain " in r["plant"]]
    a3 = all(r["own_med5"] >= 6 and r["rank"] == 1 for r in nf) and all(r["own_med5"] >= 6 for r in cf_) and all(r["own_med5"] < 6 for r in pf)
    o.append(f"- A3 (plants: 3 no-filler read at rank 1; cipher-sourced filler plant read; plaintext-sourced filler plants not read): " + "; ".join(f"{r['plant'].split(' |')[0]} {r['own_med5']:.1f} rank {r['rank']}" for r in pl["rows"]) + f" → {'holds' if a3 else 'fails'}.")
    o.append(f"- A4 (no page read): largest median {top:.2f} against chance {ch['median_max']:.2f} → {'holds' if top < ch['median_max'] + 1.0 else 'fails'}; pages at z5 >= 6: {sum(r['n6'] for r in dc)}.")
    o += ["", "Reading: written after the run, below. [stated — the tables]", "", "Reproduce: `STAGE=chance|screen|confirm|decode|plants|merge .venv/bin/python -I src/autokey_lane.py`.", ""]
    (RESULTS / f"{OUT}.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"chance": stage_chance, "screen": stage_screen, "confirm": stage_confirm, "decode": stage_decode, "plants": stage_plants, "merge": stage_merge}[STAGE]()
