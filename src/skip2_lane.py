"""Phase 7: the book's keystream families and phrase keys under wazar's skip_by_two rejection
rule (a rejected key draw discards TWO key symbols, the second unread), all three sign
conventions, both F variants, English model.

Why: wazar/cicada3301 built and validated a skip_by_two decoder but ran it only on PRNG seeds;
every word / prime / phrase / running-key negative in the public ledgers (phases 3-6 here included)
used single-advance rejection, and src/score.py's regression shows a skip-by-two plant decoded
with the single-advance rule recovers 13-48 % of runes at z 2-4, i.e. those negatives are blind
to this variant.

PRE-REGISTERED POSITIVE RULE (written before running): a page counts as decrypted only if its best
configuration scores z >= 6 above that page's own random-keystream null (2,000 random keystreams
through the identical decoder in rejection="two" mode, same sign and F variant) AND the
transliteration reads as English to a human.  About 2.5 million tests; chance maximum about 5.4.
Controls: 24 planted skip-by-two keys (soft 81 %) spanning every set, sign and F variant must be
recovered at z >= 6 and rank first in their set, or the sweep is not trusted; each is also decoded
with the single-advance rule to measure the blind spot.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import os
import numpy as np
from lp import *
from score import english_model, decode, null_scores, translit
from skip_decrypt import encrypt
import families as F

REJ = "two"
rng = np.random.default_rng(7007)
lu, lb, plain = english_model()
pages = F.pages
SHORT = os.environ.get("SHORT") == "1"
if SHORT:
    import rescore5
    pages = [p for p in pages if p[0] in rescore5.SHORT_PAGES]; CTRL_N = (92, 137, 159, 196); short_rows = []
SETS = F.ALLSETS
nconf = sum(len(L) for *_, L in SETS)
ntests = nconf * len(pages) * 2
print(f"{nconf} configurations per page x {len(pages)} pages x 2 F variants = {ntests:,} tests under skip_by_two; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)


def best_configs(C, Ks, f_rule, mode, rejection=REJ, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode, rejection=rejection)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


# ---------- controls ----------
ctrl_rows = []
t0 = time.time()
for ci in range(24):
    si = ci % len(SETS)
    sign, mode, Ks, labs = SETS[si]
    f_rule = bool((ci // len(SETS)) % 2)
    fams_here = sorted({f for f, _ in labs})
    fam = fams_here[(ci * 5) % len(fams_here)]
    cand = [i for i, (f, _) in enumerate(labs) if f == fam]
    ki = int(rng.choice(cand))
    nc = CTRL_N[ci % 4] if SHORT else 240
    o = int(rng.integers(0, len(plain) - nc)); P = plain[o:o + nc]
    Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
    C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=0.81, mode=sign, skip_by=2)
    row = [f"control-{ci:02d}", sign, labs[ki][0], labs[ki][1], f_rule]
    for rej in (REJ, "one"):
        nul = null_scores(C, lu, f_rule, rng, 500, mode, rejection=rej)
        sc, sk, tops = best_configs(C, Ks, f_rule, mode, rejection=rej)
        z = (sc - nul.mean()) / nul.std()
        rank = int((z > z[ki]).sum()) + 1
        rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode, rejection=rej)[2][0]
        row += [float(z[ki]), rank, float((rec == P).mean())]
        if SHORT and rej == REJ:
            z5c = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, rejection=rej)[2], rec[None, :], rng)[0])
            short_rows.append(dict(kind="control", n=nc, sign=sign, key=labs[ki][1], F=f_rule, zu=float(z[ki]), z5=z5c, rank=rank, passed=bool(z[ki] >= rescore5.Z_UNI_R and z5c >= rescore5.Z_5 and rank == 1)))
    ctrl_rows.append(row)
    print(f"  {row[0]}: {sign} {labs[ki][0]} '{labs[ki][1][:30]}' F={f_rule}: skip-by-two decoder z={row[5]:.1f} rank {row[6]} rec {row[7]:.3f} | single-advance decoder z={row[8]:.1f} rank {row[9]} rec {row[10]:.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)

# ---------- the sweep ----------
t0 = time.time()
results = []     # (page, sign, f_rule, family, label, z, skips, score, translit)
nulls = {}
for pi, (pid, C) in enumerate(pages):
    for f_rule in (False, True):
        nul_by_mode = {}
        for sign, mode, Ks, labs in SETS:
            if mode not in nul_by_mode:
                nul_by_mode[mode] = null_scores(C, lu, f_rule, rng, 2000, mode, rejection=REJ)
            nul = nul_by_mode[mode]
            nulls[(pid, f_rule, mode)] = (float(nul.mean()), float(nul.std()), float(nul.max()))
            sc, sk, tops = best_configs(C, Ks, f_rule, mode)
            z = (sc - nul.mean()) / nul.std()
            for k in np.argsort(-z)[:2]:
                results.append((pid, sign, f_rule, labs[k][0], labs[k][1], float(z[k]), int(sk[k]), float(sc[k]), translit(tops[k][:80]) if k in tops else ""))
                if SHORT and k in tops:
                    z5v = float(rescore5.z5(C, lambda Kr: decode(C, Kr, lu, f_rule, mode, rejection=REJ)[2], tops[k][None, :], rng)[0])
                    short_rows.append(dict(kind="page", page=pid, sign=sign, F=f_rule, fam=labs[k][0], key=labs[k][1], zu=float(z[k]), z5=z5v, translit=translit(tops[k][:80])))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z on this page: {max(r[5] for r in results if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

if SHORT:
    rescore5.write_short("phase7", "Phase 7 (skip-by-two) on the nine short pages", short_rows); sys.exit(0)
results.sort(key=lambda r: -r[5])
zmax = results[0][5]
out = ["# Phase 7 sweep: book families and phrase keys under the skip-by-two rejection rule", "",
       f"{nconf} configurations per page (phase 3's {len(F.p3)} book keystreams and phase 4's {len(F.phrase_fams)} phrase/sentence keys, each under three sign conventions), {len(pages)} pages, 2 F variants: **{ntests:,} tests**, decoder in rejection=\"two\" mode. Chance maximum about {np.sqrt(2*np.log(ntests)):.1f}.",
       "Per page, variant and decoder mode the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.", "",
       "## Planted controls (skip-by-two plants, decoded with the skip-by-two decoder and with the single-advance decoder)", "",
       "| control | sign | family | key | F | z (skip-by-two) | rank | rec | z (single-advance) | rank | rec |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3][:30]} | {r[4]} | {r[5]:.1f} | {r[6]} | {r[7]:.3f} | {r[8]:.1f} | {r[9]} | {r[10]:.3f} |")
out += ["", f"Skip-by-two decoder recovers {sum(1 for r in ctrl_rows if r[5] >= 6 and r[6] == 1)} of {len(ctrl_rows)} at z ≥ 6 and rank 1 (z {min(r[5] for r in ctrl_rows):.1f}–{max(r[5] for r in ctrl_rows):.1f}, rune recovery {min(r[7] for r in ctrl_rows):.2f}–{max(r[7] for r in ctrl_rows):.2f}); "
        f"the single-advance decoder used by every earlier phase and ledger scores the same plants at z {min(r[8] for r in ctrl_rows):.1f}–{max(r[8] for r in ctrl_rows):.1f} (rune recovery {min(r[10] for r in ctrl_rows):.2f}–{max(r[10] for r in ctrl_rows):.2f}).", "",
        "## Unsolved pages: top 20 configurations overall", "",
        "| page | sign | F | family | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:40]} | {r[5]:.2f} | {r[6]} | {r[8]} |")
out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f} ({results[0][0]}, sign {results[0][1]}, {results[0][3]} '{results[0][4][:40]}').", "",
        "## Verdict", "",
        ("**No page decrypts under the skip-by-two rule.** " if zmax < 6 else "**At least one configuration clears z = 6: inspect the transliteration above before believing it.** ") +
        "Every family of phases 3 and 4, with a rejection that discards two key symbols, under all three sign conventions and both F variants, is excluded at the sensitivity the controls demonstrate. This says nothing about keys outside these families or about other rejection widths.", ""]
(RESULTS / "phase7.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "nconf": nconf, "controls": ctrl_rows, "top": results[:60],
           "nulls": {"|".join(map(str, k)): v for k, v in nulls.items()}}, open(RESULTS / "phase7.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
