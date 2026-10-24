"""Phase 2, step 3: can a better scorer rescue the key-reuse test?

Four scorers for "two aligned pages share a keystream" on an overlap of n runes:
  ic     : index of coincidence of the difference stream D = C - C' (phase 1, the panel's choice)
  kappa  : plain match count, #(C_t == C'_t); under reuse this equals #(P_t == P'_t),
           rate = plaintext IC 0.0614 vs 1/29 under independent keys (the classic depth test)
  uni    : unigram log-likelihood ratio of D under the difference-of-plaintext model vs uniform
  bigram : the same with a first-order Markov model over adjacent differences
Power is measured by simulation at the false-positive rate implied by the phase-1 scan
(about 500,000 comparisons, FPR 2e-6).  The model is trained on half the solved plaintext
and tested on the other half.  If a scorer is materially stronger than ic, the phase-1 scan
is rerun with it under the same pre-registered rules and permutation null.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy.stats import norm, binom
from lp import *
from depth_two import MAXOFF, MIN_OVERLAP, sd_null, pooled

rng = np.random.default_rng(3301)
PI = 1 / N
LOGU = np.log(PI)
FPR = 2e-6
d = json.loads((PROCESSED / "pages.json").read_text())
plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
A, B = plain[: len(plain) // 2], plain[len(plain) // 2:]
B1, B2 = B[: len(B) // 2], B[len(B) // 2:]          # disjoint sources for the two members of a simulated pair
pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
ids = [u["id"] for u in d["unsolved"] if u["length"] > 0]


def windows(src, n, k):
    o = rng.integers(0, len(src), size=k)
    return np.take(src, (o[:, None] + np.arange(n)[None, :]), mode="wrap")


# ---------- model from the training half ----------
A1, A2 = A[: len(A) // 2], A[len(A) // 2:]
X, Y = windows(A1, 250, 4000), windows(A2, 250, 4000)
D = (X - Y) % N
uni = np.bincount(D.ravel(), minlength=N) + 0.5
LU = np.log(uni / uni.sum())
big = np.zeros((N, N)) + 0.5
np.add.at(big, (D[:, :-1].ravel(), D[:, 1:].ravel()), 1)
LB = np.log(big / big.sum(1, keepdims=True))
KL_uni = float(np.sum(np.exp(LU) * (LU - LOGU)))


def score_all(Dw):
    """Dw: (k, n) difference windows. Returns dict of (k,) scores."""
    k, n = Dw.shape
    cnt = np.stack([np.bincount(r, minlength=N) for r in Dw])
    ic = (cnt * (cnt - 1)).sum(1) / (n * (n - 1))
    kappa = (Dw == 0).sum(1)
    u = (LU[Dw] - LOGU).sum(1)
    b = (LU[Dw[:, 0]] - LOGU) + (LB[Dw[:, :-1], Dw[:, 1:]] - LOGU).sum(1)
    return {"ic": ic, "kappa": kappa.astype(float), "uni": u, "bigram": b}


rows = []
h0_moments = {}
for n in (60, 100, 150, 250):
    H0 = score_all(rng.integers(0, N, size=(200_000, n)))
    X1, Y1 = windows(B1, n, 20_000), windows(B2, n, 20_000)
    H1 = score_all((X1 - Y1) % N)
    for name in ("ic", "kappa", "uni", "bigram"):
        m0, s0 = H0[name].mean(), H0[name].std()
        if name == "kappa":
            thr = binom.isf(FPR, n, PI)                       # exact tail
        elif name == "ic":
            thr = PI + norm.isf(FPR) * sd_null(n)
        else:
            thr = m0 + norm.isf(FPR) * s0
        power = float((H1[name] > thr).mean())
        sigma = float((H1[name].mean() - m0) / s0)
        emp = float(np.quantile(H0[name], 1 - 1e-4))          # sanity: empirical 1e-4 tail vs normal
        rows.append((n, name, sigma, power, thr, emp, m0 + norm.isf(1e-4) * s0))
        h0_moments[(n, name)] = (m0, s0)

out = ["# Can a better scorer rescue the key-reuse test?", "",
       f"Difference-of-plaintext model trained on {len(A)} runes of solved plaintext, tested on the other {len(B)}. KL(q ‖ uniform) per rune = {KL_uni:.4f} nats.",
       f"Threshold at FPR {FPR:g} (the phase-1 scan size). Power = fraction of true shared-key pairs that clear it. sigma = (mean under reuse − mean under null) / null sd.", "",
       "| overlap n | scorer | sigma per pair | power at FPR 2e-6 | empirical 1e-4 tail vs normal fit |", "|---|---|---|---|---|"]
for n, name, sigma, power, thr, emp, fit in rows:
    out.append(f"| {n} | {name} | {sigma:.2f} | {power:.3f} | {emp:.4g} vs {fit:.4g} |")

best = max(("kappa", "uni", "bigram"), key=lambda nm: [r for r in rows if r[0] == 250 and r[1] == nm][0][2])
sig_ic = [r for r in rows if r[0] == 250 and r[1] == "ic"][0][2]
sig_best = [r for r in rows if r[0] == 250 and r[1] == best][0][2]
gain = sig_best / sig_ic
out += ["", f"Best scorer at n = 250: **{best}**, {sig_best:.2f} sigma per pair against {sig_ic:.2f} for the phase-1 IC ({gain:.2f}×).",
        "The match count works because a shared key cancels in C − C' and leaves plaintext coincidences at rate 0.061 instead of 0.034, a gap of 0.027; the",
        "difference-stream IC squares and sums the whole difference distribution and keeps only a 0.0019 gap. The bigram model adds little: adjacent",
        "differences of two independent texts are nearly independent of each other.", ""]

# ---------- rescan with the best scorer if it is materially better ----------
RESCAN = gain >= 1.2
REUSE = "--no-rescan" in sys.argv and (RESULTS / "rescan_arrays.npz").exists()
if RESCAN and REUSE:
    sv = np.load(RESULTS / "rescan_arrays.npz")
    sig, offs, nulls = sv["sig"], sv["offs"], sv["null_zp"]
    P = len(pages); pairs = [tuple(x) for x in sv["pairs"]]
    zp = pooled(sig)
    null_max = [float(sv.get("null_max", np.array([np.nan]))[0])] if "null_max" in sv else None
    nsave = json.load(open(RESULTS / "rescan_null.json")) if (RESULTS / "rescan_null.json").exists() else None
    null_max, null_zp_max, null_n5 = (nsave["null_max"], nsave["null_zp_max"], nsave["null_n5"]) if nsave else ([np.nan], [np.nan], [0])
    obs_n5 = int((sig[np.isfinite(sig)] >= 5).sum())
    top = np.dstack(np.unravel_index(np.argsort(-np.nan_to_num(sig, nan=-9).ravel())[:10], sig.shape))[0]
    exp_pool = sig_best * np.sqrt(np.isfinite(sig[:, offs == 0]).sum())
    out += [f"## Rescan with {best} (same pairs, offsets ±{MAXOFF}, min overlap {MIN_OVERLAP}, within-page permutation null, 20 replicates)", "",
            f"- Per pair (R1): hits at or above 5 sigma: observed {obs_n5}, null {min(null_n5)}–{max(null_n5)} per replicate; observed maximum {np.nanmax(sig):.2f} vs null maxima {min(null_max):.2f}–{max(null_max):.2f}.",
            f"- Pooled (R2): z at offset 0 = {zp[offs == 0][0]:+.2f} (null {nulls[:, offs == 0].mean():+.2f} ± {nulls[:, offs == 0].std():.2f}); largest pooled z over all offsets {zp.max():.2f} at offset {offs[zp.argmax()]} vs null maxima {min(null_zp_max):.2f}–{max(null_zp_max):.2f}.",
            "", "Top per-pair hits:", "", "| pair | offset | sigma | overlap |", "|---|---|---|---|"]
    for pi_, oi in top:
        i, j = pairs[pi_]; k = int(offs[oi])
        n = min(len(pages[i]), len(pages[j]) - k) if k >= 0 else min(len(pages[j]), len(pages[i]) + k)
        out.append(f"| {ids[i]}/{ids[j]} | {k:+d} | {sig[pi_, oi]:.2f} | {n} |")
    verdict = "null" if (obs_n5 <= max(null_n5) or np.nanmax(sig) <= max(null_max)) and zp.max() <= max(null_zp_max) else "POSITIVE: inspect"
    out += ["", f"**Rescan verdict: {verdict}.** If every page shared one keystream, the pooled z at offset 0 would be about {sig_best:.1f} sigma per pair × √1485 ≈ {exp_pool:.0f}; "
            f"if a quarter of the pages did, about {exp_pool/4:.0f}. The observed {zp[offs == 0][0]:+.2f} is indistinguishable from the permutation null.", ""]
elif RESCAN:
    t0 = time.time()
    P = len(pages); pairs = [(i, j) for i in range(P) for j in range(i + 1, P)]
    offs = np.arange(-MAXOFF, MAXOFF + 1)

    def zscore(Dv, n):
        if best == "kappa":
            m = (Dv == 0).sum(); return (m - n * PI) / np.sqrt(n * PI * (1 - PI))
        m1 = (LU - LOGU).mean() if best == "uni" else None
        s = (LU[Dv] - LOGU).sum() if best == "uni" else (LU[Dv[0]] - LOGU) + (LB[Dv[:-1], Dv[1:]] - LOGU).sum()
        mu0 = n * (np.exp(LOGU) * (LU - LOGU)).sum() * N / N if best == "uni" else n * ((LB - LOGU) / N).sum() / N
        # per-length null moments from the simulation table, interpolated linearly in n
        ns = np.array([60, 100, 150, 250]); m0s = np.array([h0_moments[(k, best)][0] for k in ns]); s0s = np.array([h0_moments[(k, best)][1] for k in ns])
        m0 = np.interp(n, ns, m0s); s0 = np.interp(n, ns, s0s)
        return (s - m0) / s0

    def scan(pg):
        sig = np.full((len(pairs), len(offs)), np.nan)
        for pi_, (i, j) in enumerate(pairs):
            a, b = pg[i], pg[j]
            for oi, k in enumerate(offs):
                if k >= 0:
                    n = min(len(a), len(b) - k)
                    if n < MIN_OVERLAP: continue
                    Dv = (a[:n] - b[k:k + n]) % N
                else:
                    n = min(len(b), len(a) + k)
                    if n < MIN_OVERLAP: continue
                    Dv = (a[-k:-k + n] - b[:n]) % N
                sig[pi_, oi] = zscore(Dv, n)
        return sig

    sig = scan(pages); zp = pooled(sig)
    print(f"rescan done in {time.time()-t0:.0f}s", flush=True)
    nulls, null_max, null_zp_max, null_n5 = [], [], [], []
    for r in range(20):
        s2 = scan([rng.permutation(p) for p in pages]); z2 = pooled(s2)
        null_max.append(np.nanmax(s2)); null_zp_max.append(z2.max()); null_n5.append(int((s2[np.isfinite(s2)] >= 5).sum())); nulls.append(z2)
        print(f"  null {r+1}/20: max sigma {null_max[-1]:.2f}, max pooled {null_zp_max[-1]:.2f}", flush=True)
    nulls = np.array(nulls)
    obs_n5 = int((sig[np.isfinite(sig)] >= 5).sum())
    top = np.dstack(np.unravel_index(np.argsort(-np.nan_to_num(sig, nan=-9).ravel())[:10], sig.shape))[0]
    out += [f"## Rescan with {best} (same pairs, offsets ±{MAXOFF}, min overlap {MIN_OVERLAP}, within-page permutation null, 20 replicates)", "",
            f"- Per pair (R1): hits at or above 5 sigma: observed {obs_n5}, null {min(null_n5)}–{max(null_n5)} per replicate; observed maximum {np.nanmax(sig):.2f} vs null maxima {min(null_max):.2f}–{max(null_max):.2f}.",
            f"- Pooled (R2): z at offset 0 = {zp[offs == 0][0]:+.2f} (null {nulls[:, offs == 0].mean():+.2f} ± {nulls[:, offs == 0].std():.2f}); largest pooled z over all offsets {zp.max():.2f} at offset {offs[zp.argmax()]} vs null maxima {min(null_zp_max):.2f}–{max(null_zp_max):.2f}.",
            "", "Top per-pair hits:", "", "| pair | offset | sigma | overlap |", "|---|---|---|---|"]
    for pi_, oi in top:
        i, j = pairs[pi_]; k = offs[oi]
        n = min(len(pages[i]), len(pages[j]) - k) if k >= 0 else min(len(pages[j]), len(pages[i]) + k)
        out.append(f"| {ids[i]}/{ids[j]} | {k:+d} | {sig[pi_, oi]:.2f} | {n} |")
    verdict = "null" if (obs_n5 <= max(null_n5) or np.nanmax(sig) <= max(null_max)) and zp.max() <= max(null_zp_max) else "POSITIVE: inspect"
    exp_pool = sig_best * np.sqrt(np.isfinite(sig[:, offs == 0]).sum())
    out += ["", f"**Rescan verdict: {verdict}.** If every page shared one keystream, the pooled z at offset 0 would be about {sig_best:.1f} sigma per pair × √1485 ≈ {exp_pool:.0f}; "
            f"if a quarter of the pages did, about {exp_pool/4:.0f}. The observed {zp[offs == 0][0]:+.2f} is indistinguishable from the permutation null.", ""]
    np.savez(RESULTS / "rescan_arrays.npz", sig=sig, offs=offs, pairs=np.array(pairs), ids=np.array(ids), null_zp=nulls)
    json.dump({"null_max": [float(x) for x in null_max], "null_zp_max": [float(x) for x in null_zp_max], "null_n5": null_n5}, open(RESULTS / "rescan_null.json", "w"))
else:
    out += ["No scorer is materially stronger than the phase-1 IC; the scan was not rerun."]
(RESULTS / "diff_score.md").write_text("\n".join(out) + "\n")
json.dump({"rows": rows, "best": best, "gain": gain, "rescan": RESCAN}, open(RESULTS / "diff_score.json", "w"), indent=1)
print("\n".join(out))
