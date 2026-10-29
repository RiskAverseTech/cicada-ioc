"""§60 (2026-10-29): the filler power curve.  Pre-registered in results/filler_curve_registration.md (commit 92af8b9)
before any plant was scored; seven claims C1-C7 are evaluated by MERGE exactly as written there.

§55 part B's instrument (src/filler_power.py) with the filler cell widened: per-rune fillers at r = 0, 0.01, 0.02, 0.05,
0.10 and the §59 per-word form (one filler at a uniform position in a fraction p = 0.2, 0.4, 0.6 of the words of two or more
runes).  Plaintext English (Emerson) from a random word start; one plaintext and key per plant shared by its eight filler
cells.  Soft rule q = 0.81; the filler is uniform over the 28 runes other than the previous cipher rune.  Families: Vigenère
word >= 8 runes, prime stream, running key; signs and F cycled; 12 plants per (n, family); n = 100, 160, 230.
Decoders: plain and free-null at prior -2.2.  Recovered = z >= 6 over 400 random keystreams and rank 1 in the family.
Usage: SHARD=k NSHARD=8 .venv/bin/python -I src/filler_curve.py  -> results/filler_curve_shard{k}.json
       MERGE=1 -> results/filler_curve.md / .json;  SMOKE=1 for a quick check.
"""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import *
from score import decode, S_MAX
from skip_decrypt import combine
import families as F, corpus

SMOKE = os.environ.get("SMOKE") == "1"; MERGE = os.environ.get("MERGE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(6000 + SHARD)
lu = F.lu
LENGTHS = (100,) if SMOKE else (100, 160, 230)
FAMS = ("vigenere-word", "primes", "running key")
REPS = 1 if SMOKE else 12
Q_SOFT = 0.81; PRIOR = float(np.log(0.1 / 0.9))
CELLS = [("rune", 0.0), ("rune", 0.01), ("rune", 0.02), ("rune", 0.05), ("rune", 0.10), ("word", 0.2), ("word", 0.4), ("word", 0.6)]
if SMOKE: CELLS = [("rune", 0.0), ("rune", 0.02), ("word", 0.4)]
NULL_REPS = 100 if SMOKE else 400
NEIGH = 512 if SMOKE else 4096
Z_RULE = 6.0
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
DECS = ["plain", f"free-null {PRIOR:.1f}"]
RES = RESULTS
def tag(form, x): return f"r={x:.2f}" if form == "rune" else f"p={x:.1f}"

# ---------- key material (as §55 B)
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


class Writer:
    """The soft-rule encipherer with a filler step.  Real runes consume plaintext and (unless literal F) key; fillers consume
    neither, avoid the previous cipher rune, and become the previous rune for the next repair."""
    def __init__(self, K, f_rule, sign, n):
        self.K, self.f, self.sign, self.n = K, f_rule, sign, n; self.C, self.placed, self.j, self.prev = [], [], 0, None
    def full(self): return len(self.C) >= self.n
    def real(self, p):
        p = int(p)
        if self.f and p == 0: c = 0
        else:
            c = combine(p, self.K[self.j], self.sign)
            while self.prev is not None and c == self.prev and rng.random() < Q_SOFT: self.j += 1; c = combine(p, self.K[self.j], self.sign)
            self.j += 1
        self.C.append(int(c)); self.placed.append(p); self.prev = int(c)
    def filler(self):
        f = int(rng.integers(0, N - 1)); f = f if (self.prev is None or f < self.prev) else f + 1
        self.C.append(f); self.placed.append(-1); self.prev = f
    def out(self): return np.array(self.C[:self.n]), np.array(self.placed[:self.n])


def encrypt(words, K, f_rule, sign, form, x, n):
    """form 'rune': a filler after each emitted rune w.p. x.  form 'word': in each word of >= 2 runes, w.p. x one filler at a
    uniform position 0..L (the §59 / E56w+n form)."""
    w = Writer(K, f_rule, sign, n)
    for word in words:
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


def run(C, Ks, f_rule, mode, dec):
    if dec == "plain": return decode(C, Ks, lu, f_rule, mode)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, None, nm, PRIOR)


def score_plant(C, placed, Kfam_dec, pos, f_rule, mode):
    out = {}; raw = {}
    for dec in DECS:
        Kr = rng.integers(0, N, size=(NULL_REPS, len(C) + S_MAX + 2)); nul = run(C, Kr, f_rule, mode, dec)[0]
        sc = np.empty(len(Kfam_dec)); dtrue = None
        for b in range(0, len(Kfam_dec), 1000):
            s, _, d = run(C, Kfam_dec[b:b + 1000], f_rule, mode, dec); sc[b:b + 1000] = s
            if b <= pos < b + 1000: dtrue = d[pos - b]
        z = (sc - nul.mean()) / nul.std(); real = placed >= 0
        out[dec] = dict(z=float(z[pos]), rank=int((z > z[pos]).sum()) + 1, acc=float((dtrue[real] == placed[real]).mean())); raw[dec] = float(sc[pos])
    out[DECS[1]]["nats"] = raw[DECS[1]] - raw["plain"]
    return out


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b)); return float(np.corrcoef(ra, rb)[0, 1])


if MERGE:
    rows = [r for p in sorted(RES.glob("filler_curve_shard*.json")) for r in json.loads(p.read_text())["rows"]]
    def sel(n=None, fam=None, form=None, x=None):
        return [r for r in rows if (n is None or r["n"] == n) and (fam is None or r["fam"] == fam) and (form is None or r["form"] == form) and (x is None or abs(r["x"] - x) < 1e-9)]
    def power(v, dec):
        z = np.array([r["res"][dec]["z"] for r in v]); rk = np.array([r["res"][dec]["rank"] for r in v])
        return float(np.mean((z >= Z_RULE) & (rk == 1))) if len(v) else float("nan"), float(np.median(z)) if len(v) else float("nan")
    out = ["# The filler power curve (§60)", "",
           f"Plants: English (Emerson) under the soft rule q = {Q_SOFT}; one plaintext and key per plant, shared by its eight filler cells. Per-rune fillers at r (a filler after each emitted rune w.p. r) and the §59 per-word form at p (one filler at a uniform position in a fraction p of the words of two or more runes). {REPS} plants per (n, family), signs and F cycled; z over {NULL_REPS} random keystreams through the same decoder; rank in the family ({len(VW)} Vigenère keys, {len(PRI)} prime streams, {NEIGH} neighbouring offsets). **Recovered = z ≥ {Z_RULE:.0f} and rank 1.** Cells: power / median z of the true key; fillers = mean count in the window.", ""]
    for dec in DECS:
        out += [f"## {dec} decoder", "", "| n | family | " + " | ".join(tag(f, x) for f, x in CELLS) + " |", "|---|---|" + "---|" * len(CELLS)]
        for n in LENGTHS:
            for fam in FAMS:
                out.append(f"| {n} | {fam} | " + " | ".join("{:.2f} / {:.1f}".format(*power(sel(n, fam, f, x), dec)) for f, x in CELLS) + " |")
        out.append("")
    out += ["Mean fillers per window (all families): " + ", ".join(f"{tag(f, x)}: {np.mean([r['fillers'] for r in sel(None, None, f, x)]):.1f}" for f, x in CELLS if x > 0), ""]
    # ---- claims
    P = {(n, fam, f, x): power(sel(n, fam, f, x), "plain")[0] for n in LENGTHS for fam in FAMS for f, x in CELLS}
    Q = {(n, fam, f, x): power(sel(n, fam, f, x), DECS[1])[0] for n in LENGTHS for fam in FAMS for f, x in CELLS}
    c1 = all(P[k] <= 0.50 for k in P if (k[2] == "rune" and k[3] >= 0.02) or k[2] == "word")
    c1 = all(P[(n, fam, "rune", r)] <= 0.50 for n in LENGTHS for fam in FAMS for r in (0.02, 0.05, 0.10))
    c2 = all(P[(n, fam, f, x)] <= 0.10 for n in LENGTHS for fam in FAMS for f, x in CELLS if (f == "rune" and x >= 0.05) or f == "word")
    c3n = sum(0.15 <= P[(n, fam, "rune", 0.01)] <= 0.65 for n in LENGTHS for fam in FAMS); c3 = c3n >= 6
    c4 = all(Q[(n, fam, "rune", r)] >= 0.75 for n in LENGTHS if n >= 160 for fam in FAMS for r in (0.01, 0.02))
    c5 = all(abs(Q[(n, fam, "word", 0.4)] - Q[(n, fam, "rune", 0.10)]) <= 0.25 for n in LENGTHS for fam in FAMS)
    c6 = all(P[(n, fam, "rune", 0.0)] > 0.5 and P[(n, fam, "rune", 0.02)] <= 0.5 for n in LENGTHS for fam in FAMS)
    fp = [r for r in rows if r["fillers"] > 0 and r["first"] >= 0]
    rho = spearman(np.array([r["res"]["plain"]["z"] for r in fp]), np.array([r["first"] for r in fp])) if len(fp) > 3 else float("nan"); c7 = rho >= 0.5
    def w(b): return "**holds**" if b else "**fails**"
    out += ["## The seven claims (results/filler_curve_registration.md, commit 92af8b9)", "",
            f"- C1 plain power ≤ 0.50 at every r ≥ 0.02: {w(c1)} (max {max(P[(n, fam, 'rune', r)] for n in LENGTHS for fam in FAMS for r in (0.02, 0.05, 0.10)):.2f}).",
            f"- C2 plain power ≤ 0.10 at r = 0.05, 0.10 and every p: {w(c2)} (max {max(P[(n, fam, f, x)] for n in LENGTHS for fam in FAMS for f, x in CELLS if (f == 'rune' and x >= 0.05) or f == 'word'):.2f}).",
            f"- C3 plain power in [0.15, 0.65] in ≥ 6 of 9 cells at r = 0.01: {w(c3)} ({c3n} of 9; cells " + ", ".join(f"{P[(n, fam, 'rune', 0.01)]:.2f}" for n in LENGTHS for fam in FAMS) + ").",
            f"- C4 free-null power ≥ 0.75 at r ≤ 0.02, n ≥ 160: {w(c4)} (min {min(Q[(n, fam, 'rune', r)] for n in LENGTHS if n >= 160 for fam in FAMS for r in (0.01, 0.02)):.2f}).",
            f"- C5 free-null power at p = 0.4 within ±0.25 of r = 0.10, same cell: {w(c5)} (max gap {max(abs(Q[(n, fam, 'word', 0.4)] - Q[(n, fam, 'rune', 0.10)]) for n in LENGTHS for fam in FAMS):.2f}).",
            f"- C6 plain power crosses 0.5 between r = 0 and r = 0.02 in every (n, family): {w(c6)}.",
            f"- C7 Spearman(z_plain, first-filler position) ≥ 0.5 over {len(fp)} filler plants: {w(c7)} (ρ = {rho:.2f}).", "",
            f"Runtime: {sum(json.loads(p.read_text())['seconds'] for p in RES.glob('filler_curve_shard*.json'))/60:.0f} CPU-minutes over {len(list(RES.glob('filler_curve_shard*.json')))} shards. Reproduce: `for k in 0..7: SHARD=$k NSHARD=8 .venv/bin/python -I src/filler_curve.py`, then `MERGE=1`.", ""]
    (RES / "filler_curve.md").write_text("\n".join(out))
    json.dump(dict(rows=rows, claims=dict(C1=c1, C2=c2, C3=c3, C4=c4, C5=c5, C6=c6, C7=c7, rho=rho, c3_cells=c3n)), open(RES / "filler_curve.json", "w"), indent=1)
    print("\n".join(out)); sys.exit(0)

# ---------- plants
t0 = time.time(); rows = []
plan = [(n, fam, rep) for n in LENGTHS for fam in FAMS for rep in range(REPS)]
for k, (n, fam, rep) in enumerate(plan):
    if k % NSHARD != SHARD: continue
    sign, mode = SIGNS[rep % 3]; f_rule = bool((rep // 3) % 2)
    w0 = int(rng.integers(0, len(WORDS) - 3 * n)); words = []; tot = 0
    for wd in WORDS[w0:]:
        words.append(wd); tot += len(wd)
        if tot >= 3 * n: break                                  # enough plaintext for n cipher runes at any filler rate
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
        C, placed = encrypt(words, K, f_rule, sign, form, x, n)
        assert len(C) == n, (len(C), n)
        res = score_plant(C, placed, Kfam_dec, pos, f_rule, mode)
        nf = int((placed < 0).sum()); first = int(np.argmax(placed < 0)) if nf else -1
        rows.append(dict(n=n, fam=fam, rep=rep, form=form, x=x, sign=sign, F=f_rule, key=label, fillers=nf, first=first, res=res))
        print(f"  n={n} {fam:13s} rep {rep:2d} {sign:8s} F={int(f_rule)} {tag(form, x):7s} fillers={nf:2d} first={first:3d} | " + " | ".join(f"{d}: z {res[d]['z']:5.1f} rank {res[d]['rank']:4d}" for d in DECS) + f"  [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(rows=rows, seconds=time.time() - t0), open(RES / ("filler_curve_smoke.json" if SMOKE else f"filler_curve_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD}: {len(rows)} rows in {time.time()-t0:.0f}s", flush=True)
