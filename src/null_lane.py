"""Phase 10: unknown-position uniform nulls under a hard anti-repeat skip rule.

§21 (results/verdict_check.md) left two mechanisms that fit every ciphertext statistic: the soft
re-draw of §5, and a HARD rule (the key is skipped until the ciphertext does not repeat) with
uniform null runes inserted at unknown positions at a rate of about 22 % (each null opens one
chance adjacency, so 0.22 x 12,901 / 29 ≈ 86 doublets).  Phase 6 ran nulls only at word edges.
This lane lets a null sit at ANY position: score.decode's null transition (t-1, gain 0, no key
consumed) is enabled at every rune with log prior ln(q/(1-q)), q = 0.22, and the Viterbi chooses.

Key library: the book's families and phrase keys (families.ALLSETS, 22,863 configurations over
three sign conventions), both F variants, 55 pages.  Null for z: 2,000 random keystreams per page,
F variant and decoder mode through the same free-null decoder.

PRE-REGISTERED HIT RULE (written before any page is scored): a page counts as a hit only if
(1) its best configuration scores z >= 6 over that page's own free-null random-keystream null,
(2) the free-null score exceeds the base decoder's score for the same configuration by >= 20 nats,
and (3) the transliteration reads as English.  Planted controls (hard rule, nulls at 0.15, 0.22
and 0.30, all signs, both F variants) must be recovered at z >= 6 and rank 1.  The null log prior
is fixed from the controls alone before any page is scored (NULLPEN; −0.8 won over −3, −2, −1.27, −0.4).

Usage: SMOKE=1 runs the controls only.  SHARD=k NSHARD=m runs pages k::m and writes
results/phase10_shard{k}.json; MERGE=1 reads the shard files and writes results/phase10.md.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, null_scores, translit, S_MAX, MAX_SKIP
from skip_decrypt import combine
import families as F

Q = 0.22
PEN = float(os.environ.get("NULLPEN", -0.8))   # the run value (chosen on controls, see docstring); the Bayesian ln(Q/(1-Q)) = -1.27 recovered fewer controls
rng = np.random.default_rng(1010)
lu = F.lu
pages = F.pages
plain = F.plain
SETS = F.ALLSETS
SMOKE = os.environ.get("SMOKE") == "1"
MERGE = os.environ.get("MERGE") == "1"
SHARD = int(os.environ.get("SHARD", "0")); NSHARD = int(os.environ.get("NSHARD", "1"))
nconf = sum(len(L) for *_, L in SETS)
ntests = nconf * len(pages) * 2
CHANCE = float(np.sqrt(2 * np.log(ntests)))


def free_null_mask(n):
    m = np.ones(n, bool); m[0] = False      # the decoder's null transition needs a previous rune
    return m


def encrypt_nulls(P, K, f_rule, sign, q, soft=1.0):
    """Plant: hard anti-repeat skip rule (soft=1.0: the key is advanced until the rune differs from
    the previous emitted rune), then a uniform null after each emitted rune with probability q.
    The null may equal its predecessor (that is where the doublets come from) and becomes the
    predecessor for the next rune.  Returns the ciphertext cut to len(P) and the null count."""
    n = len(P)
    C, placed, j, pi, prev, nulls = [], [], 0, 0, None, 0
    while len(C) < n and pi < len(P):
        p = P[pi]; pi += 1
        if f_rule and p == 0:
            C.append(0); prev = 0
        else:
            c = combine(p, K[j], sign)
            while prev is not None and c == prev and rng.random() < soft:
                j += 1; c = combine(p, K[j], sign)
            C.append(c); j += 1; prev = c
        placed.append(int(p))
        if len(C) < n and rng.random() < q:
            C.append(int(rng.integers(0, N))); prev = C[-1]; nulls += 1; placed.append(-1)
    return np.array(C), nulls, np.array(placed)


def best_configs(C, Ks, f_rule, mode, nul, batch=800):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode, None, nul, PEN)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


def null_free(C, f_rule, mode, nul, reps, batch=500):
    out = []
    for b in range(0, reps, batch):
        Ks = rng.integers(0, N, size=(min(batch, reps - b), len(C) + S_MAX + 2))
        out.append(decode(C, Ks, lu, f_rule, mode, None, nul, PEN)[0])
    return np.concatenate(out)


if MERGE:
    shards = sorted(RESULTS.glob("phase10_shard*.json"))
    ctrl_rows = None; results = []; nulls = {}; shard_time = 0.0
    for p in shards:
        d = json.load(open(p))
        if d.get("controls"): ctrl_rows = d["controls"]
        results += d["top"]; nulls.update(d["nulls"]); shard_time = max(shard_time, d["seconds"])
    results.sort(key=lambda r: -r[5])
    zmax = results[0][5]
    hits = [r for r in results if r[5] >= 6 and r[6] >= 20]
    pages_done = sorted({r[0] for r in results})
    out = ["# Phase 10: unknown-position uniform nulls under a hard anti-repeat skip rule", "",
           f"Free-null decoder (a uniform null allowed at every rune, log prior {PEN:.2f} per null, i.e. an implied rate of {1/(1+np.exp(-PEN)):.2f}, chosen on the planted controls before any page was scored: priors −3.0, −2.0, −1.27 (= ln(0.22/0.78)), −0.8 and −0.4 recovered 8, 11, 14, 15 and 14 of 18 controls at z ≥ 6 and rank 1); {nconf} configurations (phase 3 book families and phase 4 phrase keys, three sign conventions) x {len(pages_done)} pages x 2 F variants = **{nconf*len(pages_done)*2:,} tests**; chance maximum about {CHANCE:.1f}.",
           "Per page, F variant and decoder mode the null is 2,000 random keystreams through the same free-null decoder. Pre-registered hit rule: z >= 6 over that null AND free-null score minus base score for the same configuration >= 20 nats AND readable English.", "",
           f"## Planted controls (hard rule, nulls at 0.15 / 0.22 / 0.30; decoder prior fixed at {PEN:.2f})", "",
           "| control | sign | family | key | F | page | null rate | nulls | free-null z | rank | free − base (nats) | base-decoder z | runes recovered |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in ctrl_rows:
        out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]:.1f} | {r[9]} | {r[10]:+.1f} | {r[11]:.1f} | {r[12]:.3f} |")
    out += ["", f"Controls recovered at z >= 6 and rank 1: {sum(1 for r in ctrl_rows if r[8] >= 6 and r[9] == 1)} of {len(ctrl_rows)}; "
            f"the base decoder (no nulls) would have scored them at z {min(r[11] for r in ctrl_rows):.1f} to {max(r[11] for r in ctrl_rows):.1f}.", "",
            "## Unsolved pages: top 20 configurations overall", "",
            "| page | sign | F | family | key | z | free − base | key lag | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in results[:20]:
        out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:40]} | {r[5]:.2f} | {r[6]:+.1f} | {r[7]} | {r[8]} |")
    out += ["", f"Largest z over all tests: {zmax:.2f}. Cells meeting the pre-registered rule (z >= 6 and free − base >= 20): {len(hits)}.",
            "Largest z per sign: " + "; ".join(f"{sg} {max(r[5] for r in results if r[1]==sg):.2f}" for sg in ("sub", "add", "beaufort")) + ".",
            f"Wall time, longest shard: {shard_time/60:.0f} minutes on {len(shards)} shards.", "",
            "## Verdict", "",
            ("**No page decrypts with free nulls under the hard skip rule.** " if not hits else "**At least one cell meets the rule: inspect it before believing it.** ") +
            "A hard anti-repeat rule on this repository's key families, all three sign conventions and both F variants, with uniform null runes at unknown positions at the rate the doublet count implies, is excluded at the sensitivity the controls demonstrate. Not covered: non-uniform nulls, null rates far from 0.22 (the controls bracket 0.15 to 0.30), nulls that consume a key value, key streams outside these families.", ""]
    (RESULTS / "phase10.md").write_text("\n".join(out) + "\n")
    json.dump({"ntests": nconf * len(pages_done) * 2, "nconf": nconf, "q": Q, "null_prior": PEN, "decoder_max_skip": MAX_SKIP, "controls": ctrl_rows, "top": results[:80], "hits": hits, "nulls": nulls}, open(RESULTS / "phase10.json", "w"), indent=1)
    print("\n".join(out[:4] + out[-6:]))
    sys.exit(0)

print(f"{nconf} configurations x {len(pages)} pages x 2 F variants = {ntests:,} tests; chance max ~ {CHANCE:.1f} sigma; null prior {PEN:.3f}; shard {SHARD}/{NSHARD}", flush=True)

# ---------- controls: 18 plants = 3 null rates x 3 signs x 2 F, families cycled (shard 0 / smoke only) ----------
ctrl_rows = []
if SHARD == 0 or SMOKE:
    t0 = time.time()
    RATES = (0.15, 0.22, 0.30)
    for ci in range(18):
        q = RATES[ci % 3]
        si = ci % len(SETS)
        sign, mode, Ks, labs = SETS[si]
        f_rule = bool((ci // 9) % 2)
        pid, Cpage = pages[(ci * 3) % len(pages)]; n = len(Cpage)
        fams_here = sorted({f for f, _ in labs}); fam = fams_here[(ci * 5) % len(fams_here)]
        cand = [i for i, (f, _) in enumerate(labs) if f == fam]; ki = int(rng.choice(cand))
        Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
        o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
        C, nn_, placed = encrypt_nulls(P, Ktrue, f_rule, sign, q)
        nul = free_null_mask(len(C))
        nulE = null_free(C, f_rule, mode, nul, 400)
        sc, sk, tops = best_configs(C, Ks, f_rule, mode, nul)
        z = (sc - nulE.mean()) / nulE.std(); rank = int((z > z[ki]).sum()) + 1
        base = float(decode(C, Ks[ki:ki + 1], lu, f_rule, mode)[0][0])
        nulB = null_scores(C, lu, f_rule, rng, 400, mode); zb = float((base - nulB.mean()) / nulB.std())
        rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode, None, nul, PEN)[2][0]
        # recovery: share of the non-null positions where the decode equals the plaintext rune placed there
        real = placed >= 0
        acc = float(np.mean(rec[real] == placed[real]))
        ctrl_rows.append((f"control-{ci:02d}", sign, labs[ki][0], labs[ki][1][:30], f_rule, pid, q, nn_, float(z[ki]), rank, float(sc[ki] - base), zb, acc))
        print(f"  control-{ci:02d}: {sign} {labs[ki][0]} '{labs[ki][1][:24]}' F={f_rule} {pid} q={q} nulls={nn_}: free z={z[ki]:.1f} rank {rank}, free-base {sc[ki]-base:+.1f} nats, base z={zb:.1f}, rec {acc:.3f}", flush=True)
    print(f"controls done in {time.time()-t0:.0f}s", flush=True)
    if SMOKE: sys.exit(0)

# ---------- the sweep ----------
t0 = time.time()
results = []; nulls = {}
my_pages = pages[SHARD::NSHARD]
for pi_, (pid, C) in enumerate(my_pages):
    n = len(C); nul = free_null_mask(n)
    for f_rule in (False, True):
        nul_by_mode = {}
        for sign, mode, Ks, labs in SETS:
            if mode not in nul_by_mode:
                nul_by_mode[mode] = null_free(C, f_rule, mode, nul, 2000)
            nn = nul_by_mode[mode]
            nulls[f"{pid}|{f_rule}|{mode}"] = (float(nn.mean()), float(nn.std()), float(nn.max()))
            sc, sk, tops = best_configs(C, Ks, f_rule, mode, nul)
            z = (sc - nn.mean()) / nn.std()
            for k in np.argsort(-z)[:2]:
                base = float(decode(C, Ks[k:k + 1], lu, f_rule, mode)[0][0])
                results.append((pid, sign, f_rule, labs[k][0], labs[k][1], float(z[k]), float(sc[k] - base), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi_+1}/{len(my_pages)}), best z on this page: {max(r[5] for r in results if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

json.dump({"null_prior": PEN, "decoder_max_skip": MAX_SKIP, "controls": ctrl_rows, "top": results, "nulls": nulls, "seconds": time.time() - t0}, open(RESULTS / f"phase10_shard{SHARD}.json", "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} written", flush=True)
