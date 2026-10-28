"""Phase 8: the hypothesis loop's short list of small, decryptable, unswept families.

Families (from results/hypotheses.md, "Short list"):
  A. Linear congruential generators, key = x_n mod 29, one seed per page, every seed:
     (a=1033, c=0, m=3301) add; (a=3, c=0, m=3301) add; (a=7, c=1, m=3301) add and Beaufort;
     (a=2, c=24, m=29) add; (a=3301, c=29, m=1033) add with skip-by-two.
     Soft reject-on-repeat (redraw = next symbol = skip k=1 on a deterministic stream).
  B. The two solved word keys (DIVINITY, FIRFUMFERENFE) under an affine combine with a
     position-walking multiplier C = m_i * P + K, m_i = ((a*i + b) mod 28) + 1, all 784 (a, b)
     schedules, skip k=1.
Both F-rule variants everywhere.  Decoder: src/score.py with rejection "one"/"two" and mult_inv.

PRE-REGISTERED POSITIVE RULE (written before running): a page counts as decrypted only if its
best configuration scores z >= 6 above that page's own random-keystream null (2,000 random
keystreams through the identical decoder, same mode / rejection / F variant) AND the
transliteration reads as English to a human.  About 1.8 million tests; chance maximum about 5.4.
Controls: 16 planted keys spanning every family, both F variants, soft 81 %, must be recovered at
z >= 6 and rank first in their set, or the sweep is not trusted.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import os
import numpy as np
from lp import *
from score import english_model, decode, null_scores, translit, S_MAX

SMOKE = "--smoke" in sys.argv
rng = np.random.default_rng(8008)
lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
if SMOKE: pages = pages[:2]
SHORT = os.environ.get("SHORT") == "1"
if SHORT:
    import rescore5
    pages = [p for p in pages if p[0] in rescore5.SHORT_PAGES]; CTRL_N = (92, 137, 159, 196); short_rows = []
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
INV = np.array([pow(int(m), -1, N) if m % N else 0 for m in range(N)])


def lcg_keys(a, c, m):
    seeds = np.arange(m, dtype=np.int64)
    x = seeds.copy(); out = np.empty((m, LMAX), dtype=np.int64)
    for n in range(LMAX):
        x = (a * x + c) % m; out[:, n] = x % N
    return out


def schedules():
    i = np.arange(LMAX)
    M = np.array([((a * i + b) % (N - 1)) + 1 for a in range(N - 1) for b in range(N - 1)])  # (784, LMAX)
    labs = [f"m=({a}i+{b})%28+1" for a in range(N - 1) for b in range(N - 1)]
    return M, labs


# ---------- configuration sets: (name, mode, rejection, Ks, labels, mult or None) ----------
SETS = []
for (a, c, m, mode, rej) in [(1033, 0, 3301, "sub", "one"), (3, 0, 3301, "sub", "one"), (7, 1, 3301, "sub", "one"),
                             (7, 1, 3301, "beaufort", "one"), (2, 24, 29, "sub", "one"), (3301, 29, 1033, "sub", "two")]:
    K = lcg_keys(a, c, m)
    SETS.append((f"lcg(a={a},c={c},m={m}) {'add' if mode=='sub' else mode}{' skip2' if rej=='two' else ''}", mode, rej, K,
                 [(f"lcg({a},{c},{m})", f"seed={s}") for s in range(m)], None))
M, mlabs = schedules()
WORDS = {"DIVINITY": [23, 10, 1, 10, 9, 10, 16, 26], "FIRFUMFERENFE": [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]}
Kw = np.vstack([np.resize(np.array(w), LMAX)[None, :] for w in WORDS.values() for _ in range(len(mlabs))])
Mw = np.vstack([M for _ in WORDS])
wlabs = [(f"word×schedule {name}", ml) for name in WORDS for ml in mlabs]
SETS.append(("word keys × position multiplier", "sub", "one", Kw, wlabs, Mw))
nconf = sum(len(L) for _, _, _, _, L, _ in SETS)
ntests = nconf * len(pages) * 2
print(f"{nconf} configurations per page x {len(pages)} pages x 2 F variants = {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)


def encrypt_affine(P, K, mult=None, f_rule=False, soft=0.81, mode="sub", skip_by=1):
    """C = m_i*P + K_j (mode sub) or K_j - P (beaufort); soft reject-on-repeat; optional F rule."""
    C, j, prev = [], 0, None
    for i, p in enumerate(P):
        if f_rule and p == 0:
            C.append(0); prev = 0; continue
        mi = 1 if mult is None else int(mult[i])
        comb = lambda k: ((mi * p + k) % N) if mode == "sub" else ((k - p) % N)
        c = comb(K[j])
        while prev is not None and c == prev and rng.random() < soft:
            j += skip_by; c = comb(K[j])
        C.append(c); j += 1; prev = c
    return np.array(C)


def best_configs(C, Ks, f_rule, mode, rej, mult, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        mi = None if mult is None else INV[mult[b:b + batch, :len(C)]]
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode, rejection=rej, mult_inv=mi)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


# ---------- controls ----------
ctrl_rows = []
t0 = time.time()
NC = 4 if SMOKE else 16
for ci in range(NC):
    name, mode, rej, Ks, labs, mult = SETS[ci % len(SETS)]
    f_rule = bool((ci // len(SETS)) % 2)
    ki = int(rng.integers(0, len(Ks)))
    nc = CTRL_N[ci % 4] if SHORT else 240
    o = int(rng.integers(0, len(plain) - nc)); P = plain[o:o + nc]
    C = encrypt_affine(P, Ks[ki], None if mult is None else mult[ki], f_rule, 0.81, mode, 2 if rej == "two" else 1)
    nul = null_scores(C, lu, f_rule, rng, 500, mode, rejection=rej)
    sc, sk, tops = best_configs(C, Ks, f_rule, mode, rej, mult)
    z = (sc - nul.mean()) / nul.std()
    rank = int((z > z[ki]).sum()) + 1
    mi = None if mult is None else INV[mult[ki:ki + 1, :len(C)]]
    rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode, rejection=rej, mult_inv=mi)[2][0]
    ctrl_rows.append((f"control-{ci:02d}", name, labs[ki][1], f_rule, float(z[ki]), rank, float((rec == P).mean())))
    if SHORT:
        z5c = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, rejection=rej, mult_inv=(None if mult is None else INV[mult[ki, :len(C)]]))[2], rec[None, :], rng)[0])
        short_rows.append(dict(kind="control", n=nc, sign=name, key=labs[ki][1], F=f_rule, zu=float(z[ki]), z5=z5c, rank=rank, passed=bool(z[ki] >= rescore5.Z_UNI_R and z5c >= rescore5.Z_5 and rank == 1)))
    print(f"  control-{ci:02d}: {name} {labs[ki][1]} F={f_rule}: z={z[ki]:.1f} rank {rank}, recovered {(rec == P).mean():.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)
if SMOKE: sys.exit(0)

# ---------- the sweep ----------
t0 = time.time()
results = []     # (page, set, f_rule, family, label, z, skips, score, translit)
for pi, (pid, C) in enumerate(pages):
    for f_rule in (False, True):
        nul = {}
        for name, mode, rej, Ks, labs, mult in SETS:
            key = (mode, rej)
            if key not in nul:
                nul[key] = null_scores(C, lu, f_rule, rng, 2000, mode, rejection=rej)
            n_ = nul[key]
            sc, sk, tops = best_configs(C, Ks, f_rule, mode, rej, mult)
            z = (sc - n_.mean()) / n_.std()
            for k in np.argsort(-z)[:2]:
                results.append((pid, name, f_rule, labs[k][0], labs[k][1], float(z[k]), int(sk[k]), float(sc[k]), translit(tops[k][:80]) if k in tops else ""))
                if SHORT and k in tops:
                    mi_k = None if mult is None else INV[mult[k, :len(C)]]
                    z5v = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, rejection=rej, mult_inv=mi_k)[2], tops[k][None, :], rng)[0])
                    short_rows.append(dict(kind="page", page=pid, sign=name, F=f_rule, fam=labs[k][0], key=labs[k][1], zu=float(z[k]), z5=z5v, translit=translit(tops[k][:80])))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z on this page: {max(r[5] for r in results if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

if SHORT:
    rescore5.write_short("phase8", "Phase 8 (LCG seeds, position multipliers) on the nine short pages", short_rows); sys.exit(0)
results.sort(key=lambda r: -r[5])
zmax = results[0][5]
out = ["# Phase 8 sweep: the hypothesis loop's short list (LCG seeds; word keys with a position-walking multiplier)", "",
       f"{nconf} configurations per page ({', '.join(f'{n}: {len(L):,}' for n, _, _, _, L, _ in SETS)}), {len(pages)} pages, 2 F variants: **{ntests:,} tests**. Chance maximum about {np.sqrt(2*np.log(ntests)):.1f}.",
       "Per page, variant, decoder mode and rejection width the null is 2,000 random keystreams through the same decoder (a random key through a multiplier schedule is still a random key, so one null serves every schedule). Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.", "",
       "## Planted controls", "", "| control | set | key | F | z | rank in set | runes recovered |", "|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.1f} | {r[5]} | {r[6]:.3f} |")
out += ["", f"Controls recovered at z ≥ 6 and rank 1: {sum(1 for r in ctrl_rows if r[4] >= 6 and r[5] == 1)} of {len(ctrl_rows)} (z {min(r[4] for r in ctrl_rows):.1f}–{max(r[4] for r in ctrl_rows):.1f}).", "",
        "## Unsolved pages: top 20 configurations overall", "",
        "| page | set | F | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[4]} | {r[5]:.2f} | {r[6]} | {r[8]} |")
out += ["", "Largest z per set: " + "; ".join(f"{n} {max(r[5] for r in results if r[1]==n):.2f}" for n, *_ in SETS) + ".", "",
        f"Largest z over all {ntests:,} tests: {zmax:.2f} ({results[0][0]}, {results[0][1]}, {results[0][4]}).", "",
        "## Verdict", "",
        ("**No page decrypts.** " if zmax < 6 else "**At least one configuration clears z = 6: inspect the transliteration above before believing it.** ") +
        "The LCG families at every seed (five moduli/multiplier pairs, add and Beaufort, single and double skip) and the two solved word keys under every position-walking affine multiplier schedule, each with and without the F rule under the soft reject-on-repeat rule, are excluded at the sensitivity the controls demonstrate. This says nothing about other LCG parameters, other words under the multiplier, or the loop's larger feedback families, which were not run.", ""]
(RESULTS / "phase8.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "nconf": nconf, "controls": ctrl_rows, "top": results[:60]}, open(RESULTS / "phase8.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
