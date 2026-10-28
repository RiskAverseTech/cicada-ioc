"""Phase 6: word-edge events under the skip-on-repeat rule, an independent run of pnotisdev's
open registry item `open-unkeyed` (priority 2): "unkeyed insertions (an extra rune per word that
consumes no key value) and extra key advance at word separators / line / page breaks".

Kinds (candidate positions from data/processed/edges.json, each carrying an event with
probability nu = 0.42, pnotisdev's frozen rate):
  adv     extra key advance before a word-initial rune
  advline extra key advance before a line-initial rune (listed in their registry row, NOT built there)
  nulli   a word-initial rune is an unencrypted uniform null that consumes no key value
  nullf   a word-final rune is such a null
Decoder: the phase 3-5 Viterbi over skip count, with the event transitions added
(score.decode adv_mask / null_mask), per-event log prior ln(nu/(1-nu)) = -0.32.  Differences
from pnotisdev's chanscreen v2: max-path instead of summed-path likelihood; the anti-repeat
condition compares with the previous EMITTED rune (theirs: the previous real rune); unigram
English model; key library = this repository's book families and phrase keys (22,863
configurations), not their 1,447-stream library.

PRE-REGISTERED HIT RULE (written before any page is scored): a page counts as a hit only if
(1) its best configuration under an edge kind scores z >= 6 over that page's own null of 2,000
random keystreams decoded with the same kind, (2) its edge score exceeds the base decoder's
score for the same configuration by >= 20 nats (pnotisdev's edge-versus-base margin), and
(3) the transliteration reads as English.  Planted controls at nu = 0.42 must be recovered at
z >= 6 and rank 1 under the edge decoder.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, null_scores, translit, S_MAX
from skip_decrypt import combine
import families as F

NU = 0.42
PEN = float(np.log(NU / (1 - NU)))
rng = np.random.default_rng(6006)
lu = F.lu
pages = F.pages
SHORT = os.environ.get("SHORT") == "1"
if SHORT:
    import rescore5
    pages = [p for p in pages if p[0] in rescore5.SHORT_PAGES]; short_rows = []
EDGES = json.load(open(PROCESSED / "edges.json"))
SETS = F.ALLSETS
KINDS = ("adv", "advline", "nulli", "nullf")
SMOKE = os.environ.get("SMOKE") == "1"


def masks(pid, n, kind):
    e = EDGES[pid]
    adv = np.zeros(n, bool); nul = np.zeros(n, bool)
    if kind == "adv": adv[e["word_initial"]] = True
    elif kind == "advline": adv[e["line_initial"]] = True
    elif kind == "nulli": nul[e["word_initial"]] = True
    elif kind == "nullf": nul[e["word_final"]] = True
    return adv, nul


def encrypt_edges(P, K, kind, pid, f_rule, sign, nu=NU, soft=0.81):
    """Plant: walk the page's positions; at a candidate position an event fires with prob nu."""
    e = EDGES[pid]; n = e["n"]
    cand = set(e["line_initial"] if kind == "advline" else e["word_final"] if kind == "nullf" else e["word_initial"])
    C, j, pi, prev = [], 0, 0, None
    events = 0
    while len(C) < n and pi < len(P):
        i = len(C)
        fire = i in cand and rng.random() < nu
        if fire and kind in ("nulli", "nullf"):
            C.append(int(rng.integers(0, N))); prev = C[-1]; events += 1; continue
        if fire: j += 1; events += 1
        p = P[pi]; pi += 1
        if f_rule and p == 0:
            C.append(0); prev = 0; continue
        c = combine(p, K[j], sign)
        while prev is not None and c == prev and rng.random() < soft:
            j += 1; c = combine(p, K[j], sign)
        C.append(c); j += 1; prev = c
    return np.array(C), events


def best_configs(C, Ks, f_rule, mode, adv, nul, pen, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode, adv, nul, pen)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


def null_edge(C, f_rule, mode, adv, nul, reps):
    Ks = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2))
    return decode(C, Ks, lu, f_rule, mode, adv, nul, PEN)[0]


nconf = sum(len(L) for *_, L in SETS)
ntests = nconf * len(pages) * 2 * len(KINDS)
print(f"{nconf} configurations x {len(pages)} pages x 2 F variants x {len(KINDS)} kinds = {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma; event prior {PEN:.3f}", flush=True)

# ---------- controls: 24 plants, kinds x signs x F, families cycled ----------
ctrl_rows = []
t0 = time.time()
plain = F.plain
for ci in range(24):
    kind = KINDS[ci % 4]
    si = (ci // 4) % len(SETS)
    sign, mode, Ks, labs = SETS[si]
    f_rule = bool((ci // 12) % 2)
    pid = pages[ci % len(pages)][0]; n = EDGES[pid]["n"]
    fams_here = sorted({f for f, _ in labs}); fam = fams_here[(ci * 5) % len(fams_here)]
    cand = [i for i, (f, _) in enumerate(labs) if f == fam]; ki = int(rng.choice(cand))
    Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
    o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
    C, events = encrypt_edges(P, Ktrue, kind, pid, f_rule, sign)
    adv, nul = masks(pid, len(C), kind)
    nulE = null_edge(C, f_rule, mode, adv, nul, 400)
    sc, sk, tops = best_configs(C, Ks, f_rule, mode, adv, nul, PEN)
    z = (sc - nulE.mean()) / nulE.std(); rank = int((z > z[ki]).sum()) + 1
    base = decode(C, Ks[ki:ki + 1], lu, f_rule, mode)[0][0]
    nulB = null_scores(C, lu, f_rule, rng, 400, mode); zb = (base - nulB.mean()) / nulB.std()
    rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode, adv, nul, PEN)[2][0]
    acc = float(np.mean([rec[i] == P[i] for i in range(min(len(rec), len(P)))])) if kind.startswith("adv") else float("nan")
    ctrl_rows.append((f"control-{ci:02d}", kind, sign, labs[ki][0], labs[ki][1][:30], f_rule, pid, events, float(z[ki]), rank, float(sc[ki] - base), float(zb), acc))
    if SHORT:
        z5c = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, adv, nul, PEN)[2], rec[None, :], rng)[0])
        short_rows.append(dict(kind="control", n=len(C), sign=f"{kind} {sign}", key=labs[ki][1][:30], F=f_rule, zu=float(z[ki]), z5=z5c, rank=rank, passed=bool(z[ki] >= rescore5.Z_UNI_R and z5c >= rescore5.Z_5 and rank == 1)))
    print(f"  control-{ci:02d}: {kind} {sign} {labs[ki][0]} '{labs[ki][1][:24]}' F={f_rule} {pid} events={events}: edge z={z[ki]:.1f} rank {rank}, edge-base {sc[ki]-base:+.1f} nats, base-decoder z={zb:.1f}, rec {acc:.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)
if SMOKE: sys.exit(0)

# ---------- the sweep ----------
t0 = time.time()
results = []; nulls = {}
for pi_, (pid, C) in enumerate(pages):
    n = len(C)
    for kind in KINDS:
        adv, nul = masks(pid, n, kind)
        for f_rule in (False, True):
            nul_by_mode = {}
            for sign, mode, Ks, labs in SETS:
                if mode not in nul_by_mode:
                    nul_by_mode[mode] = null_edge(C, f_rule, mode, adv, nul, 2000)
                nn = nul_by_mode[mode]
                nulls[(pid, kind, f_rule, mode)] = (float(nn.mean()), float(nn.std()), float(nn.max()))
                sc, sk, tops = best_configs(C, Ks, f_rule, mode, adv, nul, PEN)
                z = (sc - nn.mean()) / nn.std()
                for k in np.argsort(-z)[:2]:
                    if SHORT and k in tops:
                        z5v = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, adv, nul, PEN)[2], tops[k][None, :], rng)[0])
                        short_rows.append(dict(kind="page", page=pid, sign=f"{kind} {sign}", F=f_rule, fam=labs[k][0], key=labs[k][1], zu=float(z[k]), z5=z5v, translit=translit(tops[k][:80])))
                    base = float(decode(C, Ks[k:k + 1], lu, f_rule, mode)[0][0])
                    results.append((pid, kind, sign, f_rule, labs[k][0], labs[k][1], float(z[k]), float(sc[k] - base), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi_+1}/{len(pages)}), best z: " + ", ".join(f"{kd} {max(r[6] for r in results if r[0]==pid and r[1]==kd):.2f}" for kd in KINDS) + f"  [{time.time()-t0:.0f}s]", flush=True)

if SHORT:
    rescore5.write_short("phase6", "Phase 6 (word-edge events) on the nine short pages", short_rows); sys.exit(0)
results.sort(key=lambda r: -r[6])
zmax = results[0][6]
hits = [r for r in results if r[6] >= 6 and r[7] >= 20]
out = ["# Phase 6: word-edge events under the skip rule (pnotisdev registry item `open-unkeyed`, run independently)", "",
       f"Kinds adv / advline / nulli / nullf at event rate nu = {NU}; {nconf} configurations (phase 3 book families and phase 4 phrase keys, three sign conventions) x {len(pages)} pages x 2 F variants x 4 kinds = **{ntests:,} tests**; chance maximum about {np.sqrt(2*np.log(ntests)):.1f}.",
       "Per page, kind, variant and decoder mode the null is 2,000 random keystreams through the same edge decoder. Pre-registered hit rule: z >= 6 over that null AND edge score minus base score for the same configuration >= 20 nats AND readable English.", "",
       "## Planted controls (nu = 0.42, skip 0.81)", "",
       "| control | kind | sign | family | key | F | page | events | edge z | rank | edge − base (nats) | base-decoder z | runes recovered |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]:.1f} | {r[9]} | {r[10]:+.1f} | {r[11]:.1f} | {'' if r[12] != r[12] else f'{r[12]:.3f}'} |")
out += ["", f"Controls recovered at z >= 6 and rank 1 under the edge decoder: {sum(1 for r in ctrl_rows if r[8] >= 6 and r[9] == 1)} of {len(ctrl_rows)}; "
        f"the base decoder (no events) would have scored them at z {min(r[11] for r in ctrl_rows):.1f} to {max(r[11] for r in ctrl_rows):.1f}.", "",
        "## Unsolved pages: top 20 configurations overall", "",
        "| page | kind | sign | F | family | key | z | edge − base | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5][:40]} | {r[6]:.2f} | {r[7]:+.1f} | {r[8]} | {r[9]} |")
out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f}. Cells meeting the pre-registered rule (z >= 6 and edge − base >= 20): {len(hits)}.",
        "Largest z per kind: " + "; ".join(f"{kd} {max(r[6] for r in results if r[1]==kd):.2f}" for kd in KINDS) + ".", "",
        "## Verdict", "",
        ("**No page decrypts under any word-edge or line-edge event kind.** " if not hits else "**At least one cell meets the rule: inspect it before believing it.** ") +
        "Extra key advances at word or line starts and unencrypted null runes at word starts or ends, at the 42 % rate pnotisdev's word-length fit implies, combined with this repository's key families under the skip rule, all three sign conventions and both F variants, are excluded at the sensitivity the controls demonstrate. Not covered: nulls inside words, non-uniform null runes, more than one event per position, event rates far from 0.42, key streams outside these families, and pnotisdev's own 1,447-stream library.", ""]
(RESULTS / "phase6.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "nconf": nconf, "nu": NU, "controls": ctrl_rows, "top": results[:80], "hits": hits,
           "nulls": {"|".join(map(str, k)): v for k, v in nulls.items()}}, open(RESULTS / "phase6.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
