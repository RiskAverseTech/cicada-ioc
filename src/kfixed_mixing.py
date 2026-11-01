"""Does the K-fixed sampler mix? (registration: results/kfixed_mixing_registration.md, commit b3717e2)

Four chains of the Metropolis sampler in src/kfixed.py over the 55 pages, each 999 draws, recording per draw the three core
statistics (within-word lag-5 equalities, S..S pairs among them, lag-6 hits of 24 - 2c): base (seed 1034, burn-in 20, thinning 4),
seed (2027, 20, 4), slow (1034, 40, 8), long (1034, 100, 4).  Per chain: null mean and sd, lag-1 autocorrelation and effective
sample size per statistic, z of the observed counts.  CHAIN=merge compares the four.
Reproduce: CHAIN=base .venv/bin/python -I src/kfixed_mixing.py (and seed, slow, long), then CHAIN=merge.
"""
import os, sys, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
from kfixed import kfixed_step, doublets

CHAIN = os.environ.get("CHAIN", "base"); SPEC = {"base": (1034, 20, 4), "seed": (2027, 20, 4), "slow": (1034, 40, 8), "long": (1034, 100, 4)}
t0 = time.time(); NREP = 999; S = LATIN.index("S")
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')


def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)


U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0]) > 6]; assert len(U) == 55


def stats(pages):
    e5 = ss = h6 = 0
    for c, w in pages:
        L = len(c); i = np.arange(5, L); e = (w[i] == w[i - 5]) & (c[i] == c[i - 5]); e5 += int(e.sum()); ss += int((c[i[e]] == S).sum())
        j = np.arange(6, L); h6 += int(((w[j] == w[j - 6]) & (c[j] == (24 - 2 * c[j - 6]) % N)).sum())
    return e5, ss, h6


NAMES = ["lag-5 equalities", "S..S pairs", "lag-6 hits"]
def acf1(x):
    x = np.asarray(x, float); x = x - x.mean(); return float((x[:-1] * x[1:]).sum() / (x * x).sum()) if (x * x).sum() > 0 else 0.0


if CHAIN != "merge":
    seed, BURN, THIN = SPEC[CHAIN]; rng = np.random.default_rng(seed); obs = stats(U)
    cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
    for c, _ in cur: kfixed_step(c, BURN * len(c), rng)
    draws = np.zeros((NREP, 3), int)
    for r in range(NREP):
        for c, _ in cur: kfixed_step(c, THIN * len(c), rng)
        draws[r] = stats(cur)
        if (r + 1) % 250 == 0: print(f"{CHAIN} rep {r+1} [{time.time()-t0:.0f}s]", flush=True)
    assert all(doublets(c) == k for (c, _), k in zip(cur, ks))
    mu, sd = draws.mean(0), draws.std(0); rho = [acf1(draws[:, k]) for k in range(3)]; ess = [NREP * (1 - r_) / (1 + r_) for r_ in rho]
    out = dict(chain=CHAIN, seed=seed, burn=BURN, thin=THIN, obs=list(obs), mean=mu.tolist(), sd=sd.tolist(), rho1=rho, ess=ess, z=((np.array(obs) - mu) / sd).tolist(), seconds=time.time() - t0)
    json.dump(out, open(RESULTS / f"kfixed_mixing_{CHAIN}.json", "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k != "seconds"}, indent=1))
else:
    R = {c: json.load(open(RESULTS / f"kfixed_mixing_{c}.json")) for c in SPEC}; obs = R["base"]["obs"]
    o = ["# Does the K-fixed sampler mix? Four chains", "", "Registration: `results/kfixed_mixing_registration.md`. 999 draws per chain over the 55 pages; statistics pooled per draw.", "",
         "| chain | seed | burn-in | thinning | " + " | ".join(f"{n}: mean ± sd, ρ₁, ESS, z" for n in NAMES) + " |", "|---|---|---|---|" + "---|" * 3]
    for c, d in R.items(): o.append(f"| {c} | {d['seed']} | {d['burn']} | {d['thin']} | " + " | ".join(f"{d['mean'][k]:.2f} ± {d['sd'][k]:.2f}, {d['rho1'][k]:+.3f}, {d['ess'][k]:.0f}, {d['z'][k]:+.2f}" for k in range(3)) + " |")
    se = [R["base"]["sd"][k] / np.sqrt(NREP) for k in range(3)]
    spread = [max(d["mean"][k] for d in R.values()) - min(d["mean"][k] for d in R.values()) for k in range(3)]
    zspread = [max(d["z"][k] for d in R.values()) - min(d["z"][k] for d in R.values()) for k in range(3)]
    m1 = all(spread[k] <= 2 * se[k] * np.sqrt(2) for k in range(3)); m2 = all(abs(R["base"]["rho1"][k]) < 0.10 and R["base"]["ess"][k] > 800 for k in range(3)); m3 = all(zspread[k] < 0.3 for k in range(3))
    o += ["", f"Observed counts: {obs[0]}, {obs[1]}, {obs[2]}. Standard error of a null mean at 999 draws: " + ", ".join(f"{s:.2f}" for s in se) + "; largest spread of the four chains' means: " + ", ".join(f"{s:.2f}" for s in spread) + "; largest spread of z: " + ", ".join(f"{s:.2f}" for s in zspread) + ".", "",
          "Rare-event uncertainty: the joint replay's 0 of 999 (§82) bounds the joint probability at about 3 in 1,000 at 95 % (rule of three); the Bonferroni margin against a wider search is therefore about sixteenfold, as §81 and §82 state.", "",
          "## Registered predictions", "",
          f"- M1 (null means agree within two standard errors across chains): spreads {', '.join(f'{s:.2f}' for s in spread)} against 2·SE·√2 = {', '.join(f'{2*s*np.sqrt(2):.2f}' for s in se)} → {'holds' if m1 else 'fails'}.",
          f"- M2 (base chain ρ₁ < 0.10 and ESS > 800 for every statistic): ρ₁ {', '.join(f'{r_:+.3f}' for r_ in R['base']['rho1'])}, ESS {', '.join(f'{e:.0f}' for e in R['base']['ess'])} → {'holds' if m2 else 'fails'}.",
          f"- M3 (z varies by less than 0.3 across chains): {', '.join(f'{s:.2f}' for s in zspread)} → {'holds' if m3 else 'fails'}.", "",
          f"Reproduce: `CHAIN=base|seed|slow|long .venv/bin/python -I src/kfixed_mixing.py`, then `CHAIN=merge`.", ""]
    (RESULTS / "kfixed_mixing.md").write_text("\n".join(o)); print("\n".join(o))
