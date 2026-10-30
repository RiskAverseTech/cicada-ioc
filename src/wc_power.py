"""§61 parts A and B (2026-10-29): the word-constrained filler decoder's power on §60's plants, and its false gain on wrong
keys at page length.  Pre-registered in results/wc_lane_registration.md (commit 8ff95b0).

PART=A  §60's loop (src/filler_curve.py) rerun verbatim with the same seeds and shard plan, so the plants and their eight
        filler cells are the same runes; the plain and free-null decoders are rescored (their z must reproduce §60's) and
        two word-constrained decoders are added after them: fixed prior -2.2 and the §59 word prior at p = 0.40.
        Output per shard results/wc_power_shard{k}.json; MERGE=1 PART=A -> results/wc_power.md / .json with claims A1-A5
        and the prior decision.
PART=B  For each page x F x mode, 2,000 random keystreams through the four decoders: null mean/sd per decoder (the sweep's
        null) and the quantiles of each filler decoder's gain over the plain score.  results/wc_margin_shard{k}.json;
        MERGE=1 PART=B -> results/wc_margin.md, results/wc_nulls.json, claims B1-B2.
Usage: PART=A SHARD=k NSHARD=8 .venv/bin/python -I src/wc_power.py ; SMOKE=1 for a quick check.
"""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import *
from score import decode, S_MAX
from skip_decrypt import combine
from wc_decode import decode_wc, word_starts, word_prior
import families as F, corpus

PART = os.environ.get("PART", "A"); SMOKE = os.environ.get("SMOKE") == "1"; MERGE = os.environ.get("MERGE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng((6000 if PART == "A" else 6100) + SHARD)          # part A: §60's seed, so the plants are §60's
lu = F.lu; RES = RESULTS
LENGTHS = (100,) if SMOKE else (100, 160, 230)
FAMS = ("vigenere-word", "primes", "running key")
REPS = 1 if SMOKE else 12
Q_SOFT = 0.81; PRIOR = float(np.log(0.1 / 0.9)); P_WORD = 0.4
CELLS = [("rune", 0.0), ("rune", 0.01), ("rune", 0.02), ("rune", 0.05), ("rune", 0.10), ("word", 0.2), ("word", 0.4), ("word", 0.6)]
if SMOKE: CELLS = [("rune", 0.0), ("rune", 0.02), ("word", 0.4)]
NULL_REPS = 100 if SMOKE else 400
NEIGH = 512 if SMOKE else 4096
Z_RULE = 6.0
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
DECS = ["plain", f"free-null {PRIOR:.1f}", "wc -2.2", f"wc word{P_WORD}"]
def tag(form, x): return f"r={x:.2f}" if form == "rune" else f"p={x:.1f}"


def run(C, Ks, f_rule, mode, dec, ws=None):
    """(scores, decoded) for one decoder."""
    if dec == "plain": s, _, d = decode(C, Ks, lu, f_rule, mode); return s, d
    if dec.startswith("free-null"):
        nm = np.ones(len(C), bool); nm[0] = False; s, _, d = decode(C, Ks, lu, f_rule, mode, None, nm, PRIOR); return s, d
    pen = -2.2 if dec == "wc -2.2" else word_prior(ws, P_WORD)
    s, _, d, _ = decode_wc(C, Ks, lu, ws, f_rule, mode, pen); return s, d


# ======================================================================= PART A
if PART == "A":
    _, _, Kp3, Lp3 = F.ALLSETS[3]
    def period_of(row, pmax=24):
        for p in range(1, pmax + 1):
            if np.all(row[p:] == row[:-p]): return p
        return 0
    VW = np.array([i for i, (f, _) in enumerate(Lp3) if f in ("vigenere-word", "vigenere-word-rev")])
    VW_PLANT = np.array([i for i in VW if Lp3[i][0] == "vigenere-word" and period_of(Kp3[i]) >= 8])
    PRI = np.array([i for i, (f, _) in enumerate(Lp3) if f in ("primes", "primes-1 (totient)", "primes+1")])
    PRI_PLANT = np.array([i for i in PRI if Lp3[i][0] == "primes"])
    cj = json.loads((Path(__file__).resolve().parent.parent / "data" / "corpus" / "corpus.json").read_text())
    TEXTS = {k: np.asarray(v["runes"], dtype=np.int64) for k, v in cj.items() if len(v["runes"]) <= 60_000}
    text = corpus.TEXTS["emerson_essays1"][0]()
    WORDS = [np.array(english_to_runes(w), dtype=np.int64) for w in re.findall(r"[A-Za-z']+", text)]
    WORDS = [w for w in WORDS if len(w)]

    def windows(stream, offs, L):
        s = np.concatenate([stream, stream[:L]]); return sliding_window_view(s, L)[np.asarray(offs) % len(stream)]

    class Writer:                                    # §60's Writer with the word id of each cipher position recorded (no extra rng draws)
        def __init__(self, K, f_rule, sign, n):
            self.K, self.f, self.sign, self.n = K, f_rule, sign, n; self.C, self.placed, self.W, self.j, self.prev, self.wid = [], [], [], 0, None, 0
        def full(self): return len(self.C) >= self.n
        def real(self, p):
            p = int(p)
            if self.f and p == 0: c = 0
            else:
                c = combine(p, self.K[self.j], self.sign)
                while self.prev is not None and c == self.prev and rng.random() < Q_SOFT: self.j += 1; c = combine(p, self.K[self.j], self.sign)
                self.j += 1
            self.C.append(int(c)); self.placed.append(p); self.W.append(self.wid); self.prev = int(c)
        def filler(self):
            f = int(rng.integers(0, N - 1)); f = f if (self.prev is None or f < self.prev) else f + 1
            self.C.append(f); self.placed.append(-1); self.W.append(self.wid); self.prev = f
        def out(self): return np.array(self.C[:self.n]), np.array(self.placed[:self.n]), np.array(self.W[:self.n])

    def encrypt(words, K, f_rule, sign, form, x, n):
        w = Writer(K, f_rule, sign, n)
        for k, word in enumerate(words):
            w.wid = k
            if form == "word" and len(word) >= 2 and rng.random() < x:
                pos = int(rng.integers(0, len(word) + 1))
                for i, p in enumerate(word):
                    if i == pos: w.filler()
                    w.real(p)
                if pos == len(word): w.filler()
            else:
                for p in word:
                    w.real(p)
                    if form == "rune" and rng.random() < x: w.filler()
            if w.full(): break
        return w.out()

    def score_plant(C, placed, W, Kfam_dec, pos, f_rule, mode):
        out = {}; raw = {}; ws = word_starts(W)
        for dec in DECS:
            # §60 drew one block of null keystreams per decoder from the plant generator, so to replay its plants this loop
            # must consume that generator exactly as §60 did: one draw for plain, one for free-null.  The two added decoders
            # reuse free-null's keystreams (the same 400 random keys through a different decoder) and draw nothing, so the
            # generator's state after each plant-cell is §60's.  The first run drew a fresh block for every decoder and so
            # replayed only the first plant-cell of each shard (8 of 864); found by the third external review, 2026-10-29.
            if dec in DECS[:2]: Kr = rng.integers(0, N, size=(NULL_REPS, len(C) + S_MAX + 2))
            nul = run(C, Kr, f_rule, mode, dec, ws)[0]
            sc = np.empty(len(Kfam_dec)); dtrue = None
            for b in range(0, len(Kfam_dec), 1000):
                s, d = run(C, Kfam_dec[b:b + 1000], f_rule, mode, dec, ws); sc[b:b + 1000] = s
                if b <= pos < b + 1000: dtrue = d[pos - b]
            z = (sc - nul.mean()) / nul.std(); real = placed >= 0
            out[dec] = dict(z=float(z[pos]), rank=int((z > z[pos]).sum()) + 1, acc=float((dtrue[real] == placed[real]).mean())); raw[dec] = float(sc[pos])
        for dec in DECS[1:]: out[dec]["nats"] = raw[dec] - raw["plain"]
        return out

    if MERGE:
        rows = [r for p in sorted(RES.glob("wc_power_shard*.json")) for r in json.loads(p.read_text())["rows"]]
        ref = {(r["n"], r["fam"], r["rep"], r["form"], round(r["x"], 3)): r for r in json.loads((RES / "filler_curve.json").read_text())["rows"]} if (RES / "filler_curve.json").exists() else {}
        rep_ok = rep_n = 0
        for r in rows:
            k = (r["n"], r["fam"], r["rep"], r["form"], round(r["x"], 3))
            if k in ref:
                rep_n += 1; rep_ok += all(abs(r["res"][d]["z"] - ref[k]["res"][d]["z"]) < 1e-6 for d in DECS[:2])
        def sel(n=None, fam=None, form=None, x=None):
            return [r for r in rows if (n is None or r["n"] == n) and (fam is None or r["fam"] == fam) and (form is None or r["form"] == form) and (x is None or abs(r["x"] - x) < 1e-9)]
        def power(v, dec):
            z = np.array([r["res"][dec]["z"] for r in v]); rk = np.array([r["res"][dec]["rank"] for r in v])
            return float(np.mean((z >= Z_RULE) & (rk == 1))) if len(v) else float("nan"), float(np.median(z)) if len(v) else float("nan")
        rec = {d: sum(1 for r in sel(None, None, "word", 0.4) if r["res"][d]["z"] >= Z_RULE and r["res"][d]["rank"] == 1) for d in DECS[2:]}
        chosen = DECS[2] if rec[DECS[2]] >= rec[DECS[3]] else DECS[3]
        out = ["# The word-constrained filler decoder on §60's plants (§61 part A)", "",
               f"§60's {len(rows)//len(CELLS)} plants and {len(CELLS)} filler cells, rescored: plain and free-null reproduce §60's z in {rep_ok} of {rep_n} plant-cells; two word-constrained decoders added (fixed prior −2.2; the §59 word prior at p = {P_WORD}). Recovered = z ≥ {Z_RULE:.0f} over {NULL_REPS} random keystreams through the same decoder and rank 1 in the family. Cells: power / median z.", ""]
        for dec in DECS:
            out += [f"## {dec}", "", "| n | family | " + " | ".join(tag(f, x) for f, x in CELLS) + " |", "|---|---|" + "---|" * len(CELLS)]
            for n in LENGTHS:
                for fam in FAMS: out.append(f"| {n} | {fam} | " + " | ".join("{:.2f} / {:.1f}".format(*power(sel(n, fam, f, x), dec)) for f, x in CELLS) + " |")
            out.append("")
        out += ["## Pooled power by cell (all plants of a cell)", "", "| decoder | " + " | ".join(tag(f, x) for f, x in CELLS) + " |", "|---|" + "---|" * len(CELLS)]
        for dec in DECS: out.append(f"| {dec} | " + " | ".join(f"{power(sel(None, None, f, x), dec)[0]:.2f}" for f, x in CELLS) + " |")
        pw = lambda d, f, x: power(sel(None, None, f, x), d)[0]
        a1 = pw(chosen, "word", 0.4) >= pw(DECS[1], "word", 0.4)
        gaps = [power(sel(n, fam, "word", 0.4), DECS[1])[0] - power(sel(n, fam, "word", 0.4), chosen)[0] for n in LENGTHS for fam in FAMS]; a2 = max(gaps) <= 0.17 + 1e-9
        a3 = pw(chosen, "rune", 0.10) >= 0.50
        a4 = abs(pw(chosen, "rune", 0.0) - pw("plain", "rune", 0.0)) <= 0.05 + 1e-9
        a5 = power(sel(160, None, "word", 0.4), chosen)[0] >= 0.70 if 160 in LENGTHS else False
        tk = [r["res"][chosen]["nats"] for r in sel(230, None, "word", 0.4)]
        def w(b): return "**holds**" if b else "**fails**"
        out += ["", f"## Prior decision and claims (registration, commit 8ff95b0)", "",
                f"- Recoveries at p = 0.4 over {len(sel(None, None, 'word', 0.4))} plants: {DECS[2]} {rec[DECS[2]]}, {DECS[3]} {rec[DECS[3]]}. **Chosen prior: {chosen}.**",
                f"- A1 pooled power at p = 0.4, chosen ≥ free-null: {w(a1)} ({pw(chosen, 'word', 0.4):.2f} against {pw(DECS[1], 'word', 0.4):.2f}).",
                f"- A2 no (n, family) cell at p = 0.4 below free-null by more than 0.17: {w(a2)} (largest gap {max(gaps):+.2f}).",
                f"- A3 pooled power at r = 0.10 ≥ 0.50: {w(a3)} ({pw(chosen, 'rune', 0.10):.2f}; free-null {pw(DECS[1], 'rune', 0.10):.2f}).",
                f"- A4 pooled power at r = 0 within 0.05 of plain: {w(a4)} ({pw(chosen, 'rune', 0.0):.2f} against {pw('plain', 'rune', 0.0):.2f}).",
                f"- A5 pooled power at n = 160, p = 0.4 ≥ 0.70: {w(a5)} ({power(sel(160, None, 'word', 0.4), chosen)[0] if 160 in LENGTHS else float('nan'):.2f}).",
                f"- True-key gain over the plain score, chosen decoder, n = 230, p = 0.4: median {np.median(tk) if tk else float('nan'):+.0f} nats (for B2).", "",
                f"Runtime: {sum(json.loads(p.read_text())['seconds'] for p in RES.glob('wc_power_shard*.json'))/60:.0f} CPU-minutes over {len(list(RES.glob('wc_power_shard*.json')))} shards.", ""]
        (RES / "wc_power.md").write_text("\n".join(out))
        json.dump(dict(rows=rows, chosen=chosen, rec=rec, claims=dict(A1=a1, A2=a2, A3=a3, A4=a4, A5=a5), true_gain_230_p04=float(np.median(tk)) if tk else None, replication=[rep_ok, rep_n]), open(RES / "wc_power.json", "w"), indent=1)
        print("\n".join(out[-12:])); sys.exit(0)

    t0 = time.time(); rows = []
    plan = [(n, fam, rep) for n in LENGTHS for fam in FAMS for rep in range(REPS)]
    for k, (n, fam, rep) in enumerate(plan):
        if k % NSHARD != SHARD: continue
        sign, mode = SIGNS[rep % 3]; f_rule = bool((rep // 3) % 2)
        w0 = int(rng.integers(0, len(WORDS) - 3 * n)); words = []; tot = 0
        for wd in WORDS[w0:]:
            words.append(wd); tot += len(wd)
            if tot >= 3 * n: break
        L = n + S_MAX + 2
        if fam == "vigenere-word":
            ki = int(rng.choice(VW_PLANT)); K = Kp3[ki, :L]; Kfam = Kp3[VW][:, :L]; pos = int(np.where(VW == ki)[0][0]); label = Lp3[ki][1]
        elif fam == "primes":
            ki = int(rng.choice(PRI_PLANT)); K = Kp3[ki, :L]; Kfam = Kp3[PRI][:, :L]; pos = int(np.where(PRI == ki)[0][0]); label = Lp3[ki][1]
        else:
            tname = list(TEXTS)[int(rng.integers(0, len(TEXTS)))]; s = TEXTS[tname]; rev = bool(rng.integers(0, 2)); s = s[::-1] if rev else s
            o = int(rng.integers(0, len(s))); offs = np.arange(o - NEIGH // 2, o + NEIGH // 2); Kfam = windows(s, offs, L); pos = NEIGH // 2; K = Kfam[pos]
            label = f"{tname}{' rev' if rev else ''} @{o}"
        Kfam_dec = (-Kfam) % N if sign == "add" else Kfam
        for form, x in CELLS:
            C, placed, W = encrypt(words, K, f_rule, sign, form, x, n)
            assert len(C) == n
            res = score_plant(C, placed, W, Kfam_dec, pos, f_rule, mode)
            nf = int((placed < 0).sum()); first = int(np.argmax(placed < 0)) if nf else -1
            rows.append(dict(n=n, fam=fam, rep=rep, form=form, x=x, sign=sign, F=f_rule, key=label, fillers=nf, first=first, res=res))
            print(f"  n={n} {fam:13s} rep {rep:2d} {sign:8s} F={int(f_rule)} {tag(form, x):7s} fillers={nf:2d} | " + " | ".join(f"{d}: z {res[d]['z']:5.1f} rk {res[d]['rank']:4d}" for d in DECS) + f"  [{time.time()-t0:.0f}s]", flush=True)
    json.dump(dict(rows=rows, seconds=time.time() - t0), open(RES / ("wc_power_smoke.json" if SMOKE else f"wc_power_shard{SHARD}.json"), "w"), indent=1)
    print(f"shard {SHARD}/{NSHARD}: {len(rows)} rows in {time.time()-t0:.0f}s", flush=True)

# ======================================================================= PART B
else:
    pages = [(p, C) for p, C in F.pages if len(C) > 0]
    txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
    def parse(s):
        runes, wid = [], []; w = 0; pending = False
        for ch in s:
            if ch in IDX:
                if pending: w += 1; pending = False
                runes.append(IDX[ch]); wid.append(w)
            elif ch in SEP: pending = True
        return np.array(runes, int), np.array(wid, int)
    LPW = [parse(chunks[k]) for k in range(16, 72)]; LPW = [(c, w) for c, w in LPW if len(c)]
    assert len(LPW) == len(pages) and all(np.array_equal(c, C) for (c, _), (_, C) in zip(LPW, pages)), "page order or content differs between families.pages and the transcription parse"
    WS = {pid: word_starts(w) for (pid, _), (_, w) in zip(pages, LPW)}
    NREPS = 200 if SMOKE else 2000; QS = (50, 90, 99, 99.9)
    cells = [(pi, f_rule, mode) for pi in range(len(pages)) for f_rule in (False, True) for mode in ("sub", "beaufort")]
    if SMOKE: cells = cells[:2]
    mine = [c for j, c in enumerate(cells) if j % NSHARD == SHARD]

    if MERGE:
        rows = [r for p in sorted(RES.glob("wc_margin_shard*.json")) for r in json.loads(p.read_text())["rows"]]
        A = json.loads((RES / "wc_power.json").read_text()) if (RES / "wc_power.json").exists() else {}
        chosen = A.get("chosen", "wc -2.2"); tg = A.get("true_gain_230_p04")
        nulls = {f"{r['page']}|{int(r['F'])}|{r['mode']}": {d: r["null"][d] for d in DECS} for r in rows}
        json.dump(dict(nulls=nulls, chosen=chosen, margin={k: r["gain"][chosen]["99.9"] for k, r in zip(nulls, rows)}), open(RES / "wc_nulls.json", "w"), indent=1)
        g99 = {d: np.array([r["gain"][d]["99.9"] for r in rows]) for d in DECS[1:]}
        b1 = float(np.median(g99[chosen])) <= 0.6 * float(np.median(g99[DECS[1]]))
        long_ = [r["gain"][chosen]["99.9"] for r in rows if 200 <= r["n"] <= 277]; Mlong = float(np.median(long_)) if long_ else float("nan")
        b2 = (tg is not None) and tg > Mlong
        def w(b): return "**holds**" if b else "**fails**"
        out = ["# False gain on wrong keys at page length (§61 part B)", "",
               f"{len(rows)} cells (page × F × mode), {NREPS:,} random keystreams each through the plain, free-null (−2.2) and both word-constrained decoders. Gain = decoder score − plain score on the same random key. Columns: median over cells of each gain quantile; the margin M(page, F, mode) used by part C is the 99.9th percentile of the chosen decoder's gain on that cell.", "",
               "| decoder | " + " | ".join(f"q{q}" for q in QS) + " | max |", "|---|" + "---|" * (len(QS) + 1)]
        for d in DECS[1:]: out.append(f"| {d} | " + " | ".join(f"{np.median([r['gain'][d][str(q)] for r in rows]):+.0f}" for q in QS) + f" | {np.median([r['gain'][d]['max'] for r in rows]):+.0f} |")
        out += ["", "By page length (chosen decoder, 99.9th percentile gain, median over cells):", ""]
        for lo, hi in ((60, 120), (120, 200), (200, 278)):
            v = [r["gain"][chosen]["99.9"] for r in rows if lo <= r["n"] < hi]
            if v: out.append(f"- {lo}–{hi - 1} runes: {np.median(v):+.0f} nats ({len(v)} cells)")
        out += ["", f"## Claims (registration, commit 8ff95b0); chosen decoder from part A: {chosen}", "",
                f"- B1 median 99.9th-percentile gain, chosen ≤ 0.6 × free-null: {w(b1)} ({np.median(g99[chosen]):+.0f} against {np.median(g99[DECS[1]]):+.0f}).",
                f"- B2 true-key gain at n = 230, p = 0.4 (part A median {tg if tg is None else round(tg)}) exceeds the median margin on pages of 200–277 runes ({Mlong:+.0f}): {w(b2)}. **Margin arm in part C: {'kept' if b2 else 'dropped'}.**", "",
                f"Runtime: {sum(json.loads(p.read_text())['seconds'] for p in RES.glob('wc_margin_shard*.json'))/60:.0f} CPU-minutes.", ""]
        (RES / "wc_margin.md").write_text("\n".join(out)); json.dump(dict(rows=rows, claims=dict(B1=b1, B2=b2), margin_long=Mlong, chosen=chosen), open(RES / "wc_margin.json", "w"), indent=1)
        print("\n".join(out)); sys.exit(0)

    t0 = time.time(); rows = []
    for pi, f_rule, mode in mine:
        pid, C = pages[pi]; ws = WS[pid]; sc = {d: [] for d in DECS}
        for b in range(0, NREPS, 1000):
            Kr = rng.integers(0, N, size=(min(1000, NREPS - b), len(C) + S_MAX + 2))
            for d in DECS: sc[d].append(run(C, Kr, f_rule, mode, d, ws)[0])
        sc = {d: np.concatenate(v) for d, v in sc.items()}
        gain = {d: {**{str(q): float(np.percentile(sc[d] - sc["plain"], q)) for q in QS}, "max": float((sc[d] - sc["plain"]).max())} for d in DECS[1:]}
        rows.append(dict(page=pid, n=len(C), F=f_rule, mode=mode, null={d: [float(sc[d].mean()), float(sc[d].std())] for d in DECS}, gain=gain))
        print(f"  {pid} n={len(C)} F={int(f_rule)} {mode:8s} | " + " | ".join(f"{d}: q99.9 {gain[d]['99.9']:+5.0f}" for d in DECS[1:]) + f"  [{time.time()-t0:.0f}s]", flush=True)
    json.dump(dict(rows=rows, seconds=time.time() - t0), open(RES / ("wc_margin_smoke.json" if SMOKE else f"wc_margin_shard{SHARD}.json"), "w"), indent=1)
    print(f"shard {SHARD}/{NSHARD}: {len(rows)} cells in {time.time()-t0:.0f}s", flush=True)
