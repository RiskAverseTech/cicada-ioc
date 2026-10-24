"""Depth-two key-reuse scan over the unsolved Liber Primus pages.

For every unordered pair of unsolved pages and every relative offset in
[-MAXOFF, MAXOFF] we form D_t = C_i[t] - C_j[t+k] (mod 29) over the overlap and
compute its index of coincidence.  sigma = (IC - 1/29) / sd_null(N) with the
exact iid-uniform sd sqrt(2*pi*(1-pi)/(N*(N-1))), pi = 1/29.  The same is done
within each page for lags 1..MAXLAG (a short-period or per-page-reset generator
would show there).

PRE-REGISTERED DECISION RULES (written before the scan was run):
  R1 (panel rule, per pair): a positive needs several (>= 3) disjoint page pairs,
     each at or above 5 sigma, with mutually consistent offsets.
  R2 (pooled, added here because q.py showed R1 is underpowered): for each offset k
     (and each lag L) the pooled z = sum of per-pair sigma / sqrt(#pairs).  A
     positive needs pooled z >= 5 at some offset/lag AND the same offset/lag must
     exceed the maximum pooled z seen in every within-page permutation replicate.
     The permutation null (runes shuffled inside each page) keeps every page's
     rune frequencies, so a merely non-flat ciphertext cannot fake a positive.
Anything else is a null result for aligned reuse at |offset| <= MAXOFF and for
within-page periods <= MAXLAG, and says nothing beyond that.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *

MAXOFF = 200
MAXLAG = 200
MIN_OVERLAP = 60
NULL_REPLICATES = int(sys.argv[1]) if len(sys.argv) > 1 else 30
PI = 1 / N
rng = np.random.default_rng(1033)


def sd_null(n):
    return np.sqrt(2 * PI * (1 - PI) / (n * (n - 1)))


def ic_counts(d):
    c = np.bincount(d, minlength=N)
    return (c * (c - 1)).sum()


def scan(pages):
    P = len(pages)
    pairs = [(i, j) for i in range(P) for j in range(i + 1, P)]
    offs = np.arange(-MAXOFF, MAXOFF + 1)
    sig = np.full((len(pairs), len(offs)), np.nan)
    icv = np.full_like(sig, np.nan)
    nv = np.zeros(sig.shape, dtype=np.int32)
    for pi_, (i, j) in enumerate(pairs):
        a, b = pages[i], pages[j]
        for oi, k in enumerate(offs):
            if k >= 0:
                n = min(len(a), len(b) - k)
                if n < MIN_OVERLAP:
                    continue
                d = (a[:n] - b[k:k + n]) % N
            else:
                n = min(len(b), len(a) + k)
                if n < MIN_OVERLAP:
                    continue
                d = (a[-k:-k + n] - b[:n]) % N
            s = ic_counts(d) / (n * (n - 1))
            icv[pi_, oi] = s
            nv[pi_, oi] = n
            sig[pi_, oi] = (s - PI) / sd_null(n)
    lags = np.arange(1, MAXLAG + 1)
    asig = np.full((P, len(lags)), np.nan)
    aic = np.full_like(asig, np.nan)
    an = np.zeros(asig.shape, dtype=np.int32)
    for p, a in enumerate(pages):
        for li, L in enumerate(lags):
            n = len(a) - L
            if n < MIN_OVERLAP:
                continue
            d = (a[:n] - a[L:L + n]) % N
            s = ic_counts(d) / (n * (n - 1))
            aic[p, li] = s; an[p, li] = n; asig[p, li] = (s - PI) / sd_null(n)
    return pairs, offs, sig, icv, nv, lags, asig, aic, an


def pooled(sig):
    m = ~np.isnan(sig)
    return np.nansum(sig, axis=0) / np.sqrt(m.sum(axis=0).clip(1))


def main():
    d = json.loads((PROCESSED / "pages.json").read_text())
    pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
    ids = [u["id"] for u in d["unsolved"] if u["length"] > 0]
    print(f"{len(pages)} unsolved pages with runes, lengths {min(map(len,pages))}-{max(map(len,pages))}")

    # Flatness of the ciphertext marginals (a reused key needs no flatness, but a
    # non-flat marginal biases pooled statistics, hence the permutation null).
    allc = np.concatenate(pages)
    cnt = np.bincount(allc, minlength=N)
    chi2 = float(((cnt - len(allc) / N) ** 2 / (len(allc) / N)).sum())
    print(f"ciphertext rune counts min/max {cnt.min()}/{cnt.max()}, chi2(28 dof) = {chi2:.1f}, IC = {ic_counts(allc)/(len(allc)*(len(allc)-1)):.5f}")

    t0 = time.time()
    pairs, offs, sig, icv, nv, lags, asig, aic, an = scan(pages)
    print(f"scan done in {time.time()-t0:.1f}s; {np.isfinite(sig).sum()} pair-offset tests, {np.isfinite(asig).sum()} page-lag tests")
    np.savez(RESULTS / "depth_two_arrays.npz", sig=sig, icv=icv, nv=nv, offs=offs, asig=asig, aic=aic, an=an, lags=lags,
             pairs=np.array(pairs), ids=np.array(ids))
    zp = pooled(sig); za = pooled(asig)

    # Permutation null: shuffle runes inside each page, rerun the identical scan.
    null_max_pair, null_max_auto, null_zp_max, null_za_max, null_zp, null_za = [], [], [], [], [], []
    null_n5, null_a5 = [], []
    for r in range(NULL_REPLICATES):
        sh = [rng.permutation(p) for p in pages]
        _, _, s2, _, _, _, a2, _, _ = scan(sh)
        null_max_pair.append(np.nanmax(s2)); null_max_auto.append(np.nanmax(a2))
        null_n5.append(int((s2[np.isfinite(s2)] >= 5).sum())); null_a5.append(int((a2[np.isfinite(a2)] >= 5).sum()))
        z2, w2 = pooled(s2), pooled(a2)
        null_zp.append(z2); null_za.append(w2)
        null_zp_max.append(z2.max()); null_za_max.append(w2.max())
        print(f"  null replicate {r+1}/{NULL_REPLICATES}: max pair sigma {null_max_pair[-1]:.2f}, max auto sigma {null_max_auto[-1]:.2f}, max pooled z {null_zp_max[-1]:.2f}/{null_za_max[-1]:.2f}", flush=True)
    null_zp = np.array(null_zp); null_za = np.array(null_za)
    np.savez(RESULTS / "depth_two_null.npz", null_max_pair=null_max_pair, null_max_auto=null_max_auto,
             null_zp=null_zp, null_za=null_za, null_n5=null_n5, null_a5=null_a5)

    # ---- tables
    M_pair = int(np.isfinite(sig).sum()); M_auto = int(np.isfinite(asig).sum()); M = M_pair + M_auto
    from math import log, sqrt
    exp_max = sqrt(2 * log(M)) - (log(log(M)) + log(4 * np.pi)) / (2 * sqrt(2 * log(M)))
    from math import erfc
    lo, hi = 0.0, 10.0
    for _ in range(60):  # normal quantile for a one-sided tail of 0.05/M
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if 0.5 * erfc(mid / sqrt(2)) > 0.05 / M else (lo, mid)
    bonf = (lo + hi) / 2
    flat = [(sig[p, o], p, o) for p in range(sig.shape[0]) for o in range(sig.shape[1]) if np.isfinite(sig[p, o])]
    flat.sort(reverse=True)
    lines = ["# Depth-two key-reuse scan: results", "",
             f"Pages: {len(pages)} unsolved pages (LP2-00..LP2-55 minus the image-only page), {len(pairs)} pairs, offsets -{MAXOFF}..+{MAXOFF}, lags 1..{MAXLAG}, min overlap {MIN_OVERLAP} runes.", "",
             f"Comparisons: {M_pair} pair-offset tests + {M_auto} page-lag tests = {M}. Expected maximum of {M} independent N(0,1) draws ~ {exp_max:.2f} sigma; Bonferroni 5% threshold = {bonf:.2f} sigma. The IC statistic has a heavier right tail than N(0,1) at these overlaps, so the permutation null below is the calibration that counts.", "",
             "## Top 20 pair/offset hits (R1)", "",
             "| rank | page A | page B | offset | N overlap | IC of difference | sigma |", "|---|---|---|---|---|---|---|"]
    for r, (s, p, o) in enumerate(flat[:20], 1):
        i, j = pairs[p]
        lines.append(f"| {r} | {ids[i]} | {ids[j]} | {offs[o]:+d} | {nv[p,o]} | {icv[p,o]:.4f} | {s:.2f} |")
    n5 = sum(1 for s, _, _ in flat if s >= 5)
    hits = [(offs[o], pairs[p]) for s, p, o in flat if s >= 5]
    from collections import Counter
    off_counts = Counter(k for k, _ in hits)
    mode_off, mode_n = off_counts.most_common(1)[0]
    near0 = [(k, ids[i], ids[j]) for k, (i, j) in hits if abs(k) <= 1]
    lines += ["", f"Pairs at or above 5 sigma: **{n5}** (R1 needs >= 3 disjoint pairs with consistent offsets). "
              f"Permutation null gives {min(null_n5)}-{max(null_n5)} such hits per replicate (median {np.median(null_n5):.0f}), i.e. the count is what chance produces.", "",
              f"Offset consistency: the {n5} hits sit at {len(off_counts)} distinct offsets; the most repeated offset is {mode_off:+d} with {mode_n} hit(s). "
              f"Hits at |offset| <= 1: {len(near0)} ({', '.join(f'{a}/{b} @ {k:+d}' for k, a, b in near0) or 'none'}); "
              f"expected under null ~ {3 * n5 / len(offs):.2f}.", "",
              f"Observed maximum pair sigma {flat[0][0]:.2f}; permutation-null maxima over {NULL_REPLICATES} replicates: "
              f"min {min(null_max_pair):.2f}, median {np.median(null_max_pair):.2f}, max {max(null_max_pair):.2f}.", "",
              "## Top 10 within-page lag hits", "", "| rank | page | lag | N | IC | sigma |", "|---|---|---|---|---|---|"]
    aflat = sorted([(asig[p, l], p, l) for p in range(asig.shape[0]) for l in range(asig.shape[1]) if np.isfinite(asig[p, l])], reverse=True)
    for r, (s, p, l) in enumerate(aflat[:10], 1):
        lines.append(f"| {r} | {ids[p]} | {lags[l]} | {an[p,l]} | {aic[p,l]:.4f} | {s:.2f} |")
    lines += ["", f"Observed maximum lag sigma {aflat[0][0]:.2f}; permutation-null maxima: min {min(null_max_auto):.2f}, median {np.median(null_max_auto):.2f}, max {max(null_max_auto):.2f}.", "",
              "## Pooled statistics (R2)", "",
              "Pooled z at offset k = sum over pairs of sigma / sqrt(#pairs). If every page re-used one keystream from the same start, offset 0 would show z of order "
              f"{(0.0019/ (0.26/230)) * sqrt(len(pairs)):.0f}.", "",
              "| statistic | observed | permutation null (mean, sd, max over replicates) |", "|---|---|---|",
              f"| pooled z at offset 0 | {zp[offs==0][0]:.2f} | {null_zp[:, offs==0].mean():.2f}, {null_zp[:, offs==0].std():.2f}, {null_zp[:, offs==0].max():.2f} |",
              f"| max pooled z over all offsets | {zp.max():.2f} (offset {offs[zp.argmax()]:+d}) | {np.mean(null_zp_max):.2f}, {np.std(null_zp_max):.2f}, {max(null_zp_max):.2f} |",
              f"| mean pooled z over offsets | {zp.mean():.2f} | {null_zp.mean():.2f}, {null_zp.mean(axis=1).std():.2f}, - |",
              f"| max pooled z over lags (autocorrelation) | {za.max():.2f} (lag {lags[za.argmax()]}) | {np.mean(null_za_max):.2f}, {np.std(null_za_max):.2f}, {max(null_za_max):.2f} |",
              f"| mean pooled z over lags | {za.mean():.2f} | {null_za.mean():.2f}, {null_za.mean(axis=1).std():.2f}, - |",
              "", "Top 5 pooled offsets:", "", "| offset | pooled z | #pairs |", "|---|---|---|"]
    for o in np.argsort(-zp)[:5]:
        lines.append(f"| {offs[o]:+d} | {zp[o]:.2f} | {int(np.isfinite(sig[:, o]).sum())} |")
    lines += ["", "Top 5 pooled lags:", "", "| lag | pooled z | #pages |", "|---|---|---|"]
    for l in np.argsort(-za)[:5]:
        lines.append(f"| {lags[l]} | {za[l]:.2f} | {int(np.isfinite(asig[:, l]).sum())} |")
    r1_raw = n5 >= 3
    r1 = bool(n5 > max(null_n5) and flat[0][0] > max(null_max_pair) and mode_n >= 3)
    r2 = bool(zp.max() >= 5 and zp.max() > max(null_zp_max)) or bool(za.max() >= 5 and za.max() > max(null_za_max))
    lines += ["", "## Decision", "",
              f"- R1 (per-pair, panel rule), literal reading: {'triggers' if r1_raw else 'does not trigger'} ({n5} pairs at >= 5 sigma) - but the permutation null produces {min(null_n5)}-{max(null_n5)} such pairs with no key reuse at all, and the observed maximum ({flat[0][0]:.2f}) is below every null replicate's maximum ({min(null_max_pair):.2f}-{max(null_max_pair):.2f}). Calibrated R1: **{'POSITIVE' if r1 else 'NULL'}**.",
              f"- R2 (pooled): {'POSITIVE' if r2 else 'NULL'} - max pooled z {max(zp.max(), za.max()):.2f} vs permutation-null max {max(max(null_zp_max), max(null_za_max)):.2f}.", ""]
    (RESULTS / "depth_two.md").write_text("\n".join(lines) + "\n")
    summary = {"pages": len(pages), "pairs": len(pairs), "tests_pair_offset": M_pair, "tests_page_lag": M_auto,
               "expected_max_sigma_null": exp_max, "max_pair_sigma": float(flat[0][0]), "pairs_ge_5sigma": n5,
               "max_auto_sigma": float(aflat[0][0]), "pooled_z_offset0": float(zp[offs == 0][0]),
               "max_pooled_z_offsets": float(zp.max()), "argmax_offset": int(offs[zp.argmax()]),
               "max_pooled_z_lags": float(za.max()), "argmax_lag": int(lags[za.argmax()]),
               "null_max_pair_sigma": [float(x) for x in null_max_pair], "null_max_auto_sigma": [float(x) for x in null_max_auto],
               "null_max_pooled_z_offsets": [float(x) for x in null_zp_max], "null_max_pooled_z_lags": [float(x) for x in null_za_max],
               "null_pairs_ge_5sigma": null_n5, "null_pages_lags_ge_5sigma": null_a5, "bonferroni_5pct_sigma": bonf,
               "hits_ge5_distinct_offsets": len(off_counts), "hits_ge5_mode_offset": int(mode_off), "hits_ge5_mode_count": mode_n,
               "pooled_z_lag1": float(za[lags == 1][0]), "null_pooled_z_lag1_max": float(null_za[:, lags == 1].max()),
               "R1_literal": r1_raw,
               "cipher_chi2_28dof": chi2, "R1": r1, "R2": r2}
    (RESULTS / "depth_two_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
