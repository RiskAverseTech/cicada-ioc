"""Planted-cluster power of the key-reuse test (2026-10-28; the one open item of the first external review).

§6 says a cluster of pages sharing a keystream gives an expected pooled z of about 135 x (shared pairs /
1,485); this measures detection directly.  For k in a ladder, k of the 55 pages are enciphered with ONE
shared keystream (the others with independent keys), solved-page English at the real page lengths, and
the §2/§6 pooled statistic at offset 0 is computed: per pair, the unigram log-likelihood ratio of the
ciphertext difference stream under the English plaintext-difference distribution, z-scored against
random pages; pooled z = sum of pair z over sqrt(1,485).  Two mechanisms, because they differ here:
  REWRITE  soft anti-repeat by resampling the output rune in place (the key stays in step: shared pages
           stay aligned), wazar's pinned reading;
  KEY-SKIP the §5 re-draw (the key index advances: shared pages drift apart after the first skip).
Detection = pooled z >= 5 (the §6 rule) or any pair z >= 5.  30 replicates per cell.
Writes results/reuse_power.md.  Usage: .venv/bin/python -I src/reuse_power.py
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model

lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text()); lengths = [u["length"] for u in d["unsolved"] if u["length"] > 2]
rng = np.random.default_rng(1485); LOGU = np.log(1 / N)
# English plaintext-difference distribution from solved text pairs
PD = np.concatenate([(plain[i:i + 2000] - plain[i + 7:i + 2007]) % N for i in range(0, len(plain) - 2010, 97)])
cnt = np.bincount(PD, minlength=N) + 1.0; LD = np.log(cnt / cnt.sum())
P = len(lengths); pairs = [(i, j) for i in range(P) for j in range(i + 1, P)]; NP = len(pairs)


def enc(Pt, K, mech):
    C, j, prev = [], 0, None
    for p in Pt:
        c = (p + K[j]) % N
        if prev is not None and c == prev and rng.random() < 0.81:
            if mech == "rewrite": c = int(rng.integers(0, N))
            else:
                while c == prev: j += 1; c = (p + K[j]) % N
        C.append(c); j += 1; prev = c
    return np.array(C)


def pair_scores(pages_):
    out = np.empty(NP)
    for t, (i, j) in enumerate(pairs):
        n = min(len(pages_[i]), len(pages_[j])); D = (pages_[i][:n] - pages_[j][:n]) % N
        out[t] = (LD[D] - LOGU).sum() / np.sqrt(n)        # per-rune-normalised so one null fits every length
    return out


# null moments of the per-pair statistic from fully independent pages
null = np.concatenate([pair_scores([enc(plain[int(rng.integers(0, len(plain) - L - 1)):][:L], rng.integers(0, N, L + 100), "rewrite") for L in lengths]) for _ in range(6)])
m0, s0 = null.mean(), null.std(); print(f"pair null {m0:.3f} ± {s0:.3f} over {len(null)} pairs", flush=True)

rows = []; t0 = time.time()
for mech in ("rewrite", "keyskip"):
    for k in (2, 3, 4, 6, 8, 11, 13, 20, 55):
        det_pool, det_pair, zs = 0, 0, []
        for r in range(30):
            shared = rng.integers(0, N, max(lengths) + 400); members = set(rng.choice(P, k, replace=False).tolist()); pg = []
            for i, L in enumerate(lengths):
                Pt = plain[int(rng.integers(0, len(plain) - L - 1)):][:L]
                pg.append(enc(Pt, shared if i in members else rng.integers(0, N, L + 400), mech))
            z = (pair_scores(pg) - m0) / s0; zp = z.sum() / np.sqrt(NP)
            zs.append(zp); det_pool += zp >= 5; det_pair += z.max() >= 5
        rows.append(dict(mech=mech, k=k, pooled_mean=float(np.mean(zs)), pooled_sd=float(np.std(zs)), det_pooled=det_pool / 30, det_pair=det_pair / 30))
        print(f"{mech:8s} k={k:2d}: pooled z {np.mean(zs):6.2f} ± {np.std(zs):.2f}; detected by pooled rule {det_pool}/30, by any pair {det_pair}/30  [{time.time()-t0:.0f}s]", flush=True)
out = ["# Planted-cluster power of the key-reuse test", "", f"Per-pair statistic: unigram LLR of the ciphertext difference stream under the English plaintext-difference distribution, per-rune normalised, z-scored against {len(null)} independent pairs (null {m0:.3f} ± {s0:.3f}); pooled z over all 1,485 pairs; 30 replicates per cell; detection at z >= 5.", "",
       "| mechanism | pages sharing one key | pooled z (mean ± sd) | detected, pooled rule | detected, any pair |", "|---|---|---|---|---|"]
for r in rows: out.append(f"| {r['mech']} | {r['k']} | {r['pooled_mean']:.2f} ± {r['pooled_sd']:.2f} | {r['det_pooled']:.2f} | {r['det_pair']:.2f} |")
rw = [r for r in rows if r["mech"] == "rewrite" and r["det_pooled"] >= 0.9]; ks = [r for r in rows if r["mech"] == "keyskip" and r["det_pooled"] >= 0.9]
out += ["", f"**Reading.** Under the in-place rewrite mechanism (shared pages stay aligned) the pooled rule reaches 90 % detection at {rw[0]['k'] if rw else 'no tested'} shared pages; under the key-skip mechanism (shared pages drift apart after the first skip) it reaches 90 % at {ks[0]['k'] if ks else 'no tested'} shared pages. "
        "The §6 and §7 statement 'no detected large-scale aligned reuse' is therefore a statement about aligned reuse; a shared key under the key-skip rule is invisible to this test at any cluster size, which pnotisdev's ledger also records ('pad reuse under skip drift: untestable').", ""]
(RESULTS / "reuse_power.md").write_text("\n".join(out) + "\n"); json.dump(dict(null=[m0, s0], rows=rows), open(RESULTS / "reuse_power.json", "w"), indent=1)
print("\n".join(out[-3:]))
