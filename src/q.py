"""Compute q, the coincidence rate of the difference of two independent plaintext
streams, from the verified Liber Primus plaintext, and the power of the depth-two
(key-reuse) index-of-coincidence test.

q = sum_d ( sum_a p_a * p_{(a-d) mod 29} )^2

Under the null (independent uniform keystreams) the difference stream is iid
uniform on 29 symbols, E[IC] = 1/29 and, because pairs sharing one index are
uncorrelated for a uniform alphabet, Var[IC] = 2*pi*(1-pi)/(N*(N-1)) exactly,
pi = 1/29  ->  sd ~= 0.258/N.  Monte Carlo below checks that.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *

rng = np.random.default_rng(3301)


def ic(x: np.ndarray) -> float:
    n = len(x)
    c = np.bincount(x, minlength=N)
    return float((c * (c - 1)).sum() / (n * (n - 1)))


def q_from_p(p: np.ndarray) -> float:
    r = np.array([sum(p[a] * p[(a - d) % N] for a in range(N)) for d in range(N)])
    return float((r ** 2).sum())


def sd_null_exact(n: int) -> float:
    pi = 1 / N
    return float(np.sqrt(2 * pi * (1 - pi) / (n * (n - 1))))


def main():
    d = json.loads((PROCESSED / "pages.json").read_text())
    plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
    T = len(plain)
    counts = np.bincount(plain, minlength=N)
    p = counts / T
    q = q_from_p(p)
    ic_plain = ic(plain)
    excess = q - 1 / N

    # Bootstrap uncertainty on q from the finite plaintext sample.
    boots = []
    for _ in range(2000):
        s = rng.choice(plain, size=T, replace=True)
        boots.append(q_from_p(np.bincount(s, minlength=N) / T))
    q_lo, q_hi = np.percentile(boots, [2.5, 97.5])

    # Direct empirical check: IC of the difference of two *different* solved pages
    # at random relative offsets (what a reused key would leave behind).
    pages = [np.array(s["plaintext"]) for s in d["solved"]]
    emp = []
    for _ in range(4000):
        i, j = rng.choice(len(pages), 2, replace=False)
        a, b = pages[i], pages[j]
        n = min(len(a), len(b), 200)
        oa = rng.integers(0, len(a) - n + 1); ob = rng.integers(0, len(b) - n + 1)
        emp.append(ic((a[oa:oa + n] - b[ob:ob + n]) % N))
    q_emp = float(np.mean(emp))

    # Null sd of IC: exact formula and Monte Carlo of iid uniform streams.
    rows = []
    for n in (150, 250, 400):
        sims = np.array([ic(rng.integers(0, N, n)) for _ in range(20000)])
        rows.append({"N": n, "sd_formula_0.26/N": 0.26 / n, "sd_exact": sd_null_exact(n),
                     "sd_mc": float(sims.std()), "mean_mc": float(sims.mean()),
                     "p_gt_5sigma_mc": float((sims > 1 / N + 5 * sd_null_exact(n)).mean()),
                     "sigma_per_pair_0.26": n * excess / 0.26,
                     "sigma_per_pair_mc": excess / float(sims.std())})

    verdict = "well powered" if excess > 0.005 else ("marginal" if excess > 0.002 else "underpowered")
    out = {"plaintext_runes": int(T), "rune_counts": {LATIN[i]: int(counts[i]) for i in range(N)},
           "p": {LATIN[i]: float(p[i]) for i in range(N)},
           "ic_plaintext": ic_plain, "q": q, "one_over_29": 1 / N, "q_minus_1_over_29": excess,
           "q_bootstrap_95ci": [float(q_lo), float(q_hi)],
           "q_empirical_page_pairs": q_emp, "power_rows": rows, "verdict": verdict}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "q.json").write_text(json.dumps(out, indent=2))

    lines = ["# q for Liber Primus plaintext", "",
             f"Plaintext sample: {T} runes from the 9 solved sections (pages 1-15, 72-73 of the rtkd master).", "",
             f"| quantity | value |", "|---|---|",
             f"| IC of the plaintext itself | {ic_plain:.4f} |",
             f"| q (difference-of-two-plaintexts coincidence rate) | {q:.4f} |",
             f"| 1/29 | {1/N:.4f} |",
             f"| q - 1/29 | {excess:.4f} |",
             f"| q bootstrap 95% CI | {q_lo:.4f} - {q_hi:.4f} |",
             f"| empirical IC of page-minus-page differences (200-rune windows) | {q_emp:.4f} |", "",
             "## Power per aligned pair", "",
             "| N | sd null (0.26/N) | sd null (exact) | sd null (MC) | sigma if key reused (0.26/N) | sigma (MC sd) | P(>5 sigma) under null (MC) |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['N']} | {r['sd_formula_0.26/N']:.5f} | {r['sd_exact']:.5f} | {r['sd_mc']:.5f} | "
                     f"{r['sigma_per_pair_0.26']:.1f} | {r['sigma_per_pair_mc']:.1f} | {r['p_gt_5sigma_mc']:.2e} |")
    lines += ["", f"**Verdict: the depth-two test is {verdict}** (excess {excess:.4f} vs the 0.005 threshold).", "",
              "## Rune frequencies (plaintext)", "", "| rune | count | p |", "|---|---|---|"]
    for i in np.argsort(-counts):
        lines.append(f"| {LATIN[i]} ({RUNES[i]}) | {counts[i]} | {p[i]:.4f} |")
    (RESULTS / "q.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:22]))


if __name__ == "__main__":
    main()
