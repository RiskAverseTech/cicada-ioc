"""§55 part B (2026-10-29): decoder power when a tenth of the runes are fillers.  Pre-registered in
results/filler_lane_registration.md before any plant was scored.

Plant: English (Emerson) of n = 100, 160, 230 runes under the repository's standard mechanism (soft reject-on-repeat,
q = 0.81) with a FILLER inserted after each emitted rune with probability r = 0.10; the filler is uniform over the 28 runes
other than the previous cipher rune (it adds no doublets) and becomes the previous rune for the next real rune's repair.
Families: a Vigenère word of >= 8 runes from the book library, a prime stream p[n+s], a running key (a corpus text of
<= 60,000 runes at a random offset, either direction).  Signs and F variants cycled.  12 plants per cell; each plant is also
encrypted once without fillers (r = 0) as the reference.
Decoders: plain (score.decode, soft skip rule) and free-null (null_mask at every rune) at priors -0.8 (§22's) and
ln(0.1/0.9) = -2.2.  Statistic: z of the true key over 400 random keystreams through the same decoder, and its rank among
its family (every vigenere-word key both directions; every prime stream of the three prime families; the 4,096 neighbouring
offsets of the text in the planted direction).  Recovered = z >= 6 and rank 1.
Decisions (fixed in the registration): the prior for part C is the one that recovers more running-key plants at r = 0.10
(ties to -0.8); part C runs only if that prior recovers >= 50 % of the running-key plants at n = 230, r = 0.10.
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/filler_power.py  -> results/filler_power_shard{k}.json
       MERGE=1 -> results/filler_power.md / .json;  SMOKE=1 for a quick check.
"""
import json, os, sys, time
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
rng = np.random.default_rng(5500 + SHARD)
lu = F.lu
LENGTHS = (100,) if SMOKE else (100, 160, 230)
FAMS = ("vigenere-word", "primes", "running key")
REPS = 1 if SMOKE else 12
R_FILL, Q_SOFT = 0.10, 0.81
PRIORS = (-0.8, float(np.log(0.1 / 0.9)))
NULL_REPS = 100 if SMOKE else 400
NEIGH = 512 if SMOKE else 4096
Z_RULE = 6.0
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
DECS = ["plain"] + [f"free-null {p:.1f}" for p in PRIORS]
RES = RESULTS

# ---------- key material
_, _, Kp3, Lp3 = F.ALLSETS[3]            # the book's phase-3 families, positive keys
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
text = corpus.TEXTS["emerson_essays1"][0](); EP = np.array(english_to_runes(text), dtype=np.int64)


def windows(stream, offs, L):
    s = np.concatenate([stream, stream[:L]]); return sliding_window_view(s, L)[np.asarray(offs) % len(stream)]


def encrypt_fill(P, K, f_rule, sign, r, n):
    """Soft rule q = 0.81 (as every plant since §9), then a filler after each emitted rune with probability r.
    The filler avoids the previous cipher rune.  Returns the first n cipher runes and, per position, the plaintext rune
    or -1 for a filler."""
    C, placed, j, pi, prev = [], [], 0, 0, None
    while len(C) < n:
        p = int(P[pi]); pi += 1
        if f_rule and p == 0: C.append(0); prev = 0
        else:
            c = combine(p, K[j], sign)
            while prev is not None and c == prev and rng.random() < Q_SOFT: j += 1; c = combine(p, K[j], sign)
            C.append(int(c)); j += 1; prev = int(c)
        placed.append(p)
        if len(C) < n and rng.random() < r:
            f = int(rng.integers(0, N - 1)); f = f if f < prev else f + 1
            C.append(f); placed.append(-1); prev = f
    return np.array(C[:n]), np.array(placed[:n])


def run(C, Ks, f_rule, mode, dec):
    if dec == "plain": return decode(C, Ks, lu, f_rule, mode)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, None, nm, float(dec.split()[1]))


def score_plant(C, placed, Kfam_dec, pos, f_rule, mode):
    """All three decoders on one plant: z of the true key, rank in the family, accuracy on real positions, raw scores."""
    out = {}; raw = {}
    for dec in DECS:
        Kr = rng.integers(0, N, size=(NULL_REPS, len(C) + S_MAX + 2)); nul = run(C, Kr, f_rule, mode, dec)[0]
        sc = np.empty(len(Kfam_dec)); dtrue = None
        for b in range(0, len(Kfam_dec), 1000):
            s, _, d = run(C, Kfam_dec[b:b + 1000], f_rule, mode, dec); sc[b:b + 1000] = s
            if b <= pos < b + 1000: dtrue = d[pos - b]
        z = (sc - nul.mean()) / nul.std(); real = placed >= 0
        out[dec] = dict(z=float(z[pos]), rank=int((z > z[pos]).sum()) + 1, acc=float((dtrue[real] == placed[real]).mean())); raw[dec] = float(sc[pos])
    for dec in DECS[1:]: out[dec]["nats"] = raw[dec] - raw["plain"]
    return out


if MERGE:
    rows = [r for p in sorted(RES.glob("filler_power_shard*.json")) for r in json.loads(p.read_text())["rows"]]
    def cell(n, fam, r, dec):
        v = [x for x in rows if x["n"] == n and x["fam"] == fam and x["r"] == r]
        z = np.array([x["res"][dec]["z"] for x in v]); rk = np.array([x["res"][dec]["rank"] for x in v])
        return float(np.mean((z >= Z_RULE) & (rk == 1))) if len(v) else float("nan"), float(np.median(z)) if len(v) else float("nan"), len(v)
    out = ["# Decoder power when a tenth of the runes are fillers (§55 part B)", "",
           f"Plants: English (Emerson) under the soft rule q = {Q_SOFT} with a filler after each emitted rune w.p. {R_FILL} (uniform over the 28 runes other than the previous cipher rune), and the same plaintext and key without fillers (r = 0). {REPS} plants per cell, signs and F variants cycled. Statistic: z of the true key over {NULL_REPS} random keystreams through the same decoder, rank among the family (vigenere words both directions: {len(VW)} keys; prime streams of three families: {len(PRI)}; running key: the {NEIGH} neighbouring offsets of the text). **Recovered = z >= {Z_RULE:.0f} and rank 1.**", "",
           "| n | family | r | " + " | ".join(f"{d}: power / median z" for d in DECS) + " |", "|---|---|---|" + "---|" * len(DECS)]
    for n in LENGTHS:
        for fam in FAMS:
            for r in (0.0, R_FILL):
                cells = [cell(n, fam, r, d) for d in DECS]
                out.append(f"| {n} | {fam} | {r:.2f} | " + " | ".join(f"{p:.2f} / {mz:.1f}" for p, mz, _ in cells) + " |")
    # decision
    rk = [x for x in rows if x["fam"] == "running key" and x["r"] == R_FILL]
    rec = {d: sum(1 for x in rk if x["res"][d]["z"] >= Z_RULE and x["res"][d]["rank"] == 1) for d in DECS[1:]}
    prior = DECS[1] if rec[DECS[1]] >= rec[DECS[2]] else DECS[2]
    p230, _, n230 = cell(230, "running key", R_FILL, prior) if 230 in LENGTHS else (float("nan"), 0, 0)
    go = bool(p230 >= 0.5)
    nats = {r: float(np.median([x["res"][prior]["nats"] for x in rows if x["r"] == r])) for r in (0.0, R_FILL)}
    out += ["", f"## Decisions (rules fixed in the registration)", "",
            f"- Running-key plants with fillers recovered: {rec[DECS[1]]} under prior −0.8, {rec[DECS[2]]} under prior −2.2 (of {len(rk)}). **Prior for part C: {prior.split()[1]}.**",
            f"- Power at n = 230, running key, r = {R_FILL}, under that prior: **{p230:.2f}** ({n230} plants). Threshold 0.50 → **part C {'runs' if go else 'does not run'}.**",
            f"- Free-null minus plain score for the true key (median nats): {nats[R_FILL]:+.0f} with fillers, {nats[0.0]:+.0f} without; §22's candidate rule asks for +20.", "",
            "Columns read: power is the recovered fraction, median z the true key's typical z. The plain decoder's power under fillers is the power the plain-decoder lanes (§25, §40, §53 and the plain tiers of §54) had in a filler world; the free-null columns are what the sweep of part C has. [stated]", ""]
    (RES / "filler_power.md").write_text("\n".join(out)); json.dump(dict(rows=rows, prior=float(prior.split()[1]), go=go, power_230=p230), open(RES / "filler_power.json", "w"), indent=1)
    print("\n".join(out)); sys.exit(0)

# ---------- plants
t0 = time.time(); rows = []
plan = [(n, fam, rep) for n in LENGTHS for fam in FAMS for rep in range(REPS)]
for k, (n, fam, rep) in enumerate(plan):
    if k % NSHARD != SHARD: continue
    sign, mode = SIGNS[rep % 3]; f_rule = bool((rep // 3) % 2)
    p0 = int(rng.integers(0, len(EP) - 2 * n - 1)); P = EP[p0:p0 + 2 * n]
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
    for r in (0.0, R_FILL):
        C, placed = encrypt_fill(P, K, f_rule, sign, r, n)
        res = score_plant(C, placed, Kfam_dec, pos, f_rule, mode)
        rows.append(dict(n=n, fam=fam, rep=rep, r=r, sign=sign, F=f_rule, key=label, fillers=int((placed < 0).sum()), res=res))
        print(f"  n={n} {fam:13s} rep {rep:2d} {sign:8s} F={int(f_rule)} r={r:.2f} fillers={rows[-1]['fillers']:2d} | " + " | ".join(f"{d}: z {res[d]['z']:5.1f} rank {res[d]['rank']:4d}" for d in DECS) + f"  [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(rows=rows, seconds=time.time() - t0), open(RES / (f"filler_power_smoke.json" if SMOKE else f"filler_power_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD}: {len(rows)} rows in {time.time()-t0:.0f}s", flush=True)
