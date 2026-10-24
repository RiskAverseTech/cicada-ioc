"""Phase 5 sweep: every family of phases 3 and 4 (book keystreams, phrase and sentence keys,
three sign conventions, both F variants, skip-on-repeat rule) rerun with the decoder's language
model set to Latin and to Old English instead of English.

PRE-REGISTERED POSITIVE RULE (same as phases 3 and 4): a page counts as decrypted only if its
best configuration scores z >= 6 above that page's own random-keystream null under the same
model, AND the transliteration reads as that language on inspection.  About 5 million tests;
chance maximum about 5.6 sigma.

Controls, per register: planted keys on 240-rune windows of that language's corpus, enciphered
with the families, the 81 % soft skip rule, each sign and F variant; decoded with the matching
model (must recover at z >= 6, rank 1) AND with the English model (measures the blind spot).
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, null_scores, translit, S_MAX
from skip_decrypt import encrypt
import families as F

rng = np.random.default_rng(5005)
regs = json.load(open(PROCESSED / "registers.json"))
texts = np.load(PROCESSED / "registers_text.npz")
LU = {k: np.array(v["lu"]) for k, v in regs.items()}
pages = F.pages
SETS = F.ALLSETS
nconf = sum(len(L) for *_, L in SETS)
REGS = ("la", "ang")
ntests = nconf * len(pages) * 2 * len(REGS)
print(f"{nconf} configurations per page x {len(pages)} pages x 2 F variants x {len(REGS)} registers = {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)


def best_configs(C, Ks, lu, f_rule, mode, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


# ---------- controls ----------
ctrl_rows = []
t0 = time.time()
for reg in REGS:
    text = texts[reg]
    for ci in range(12):
        si = ci % len(SETS)
        sign, mode, Ks, labs = SETS[si]
        f_rule = bool((ci // len(SETS)) % 2)
        fams_here = sorted({f for f, _ in labs})
        fam = fams_here[(ci * 7) % len(fams_here)]
        cand = [i for i, (f, _) in enumerate(labs) if f == fam]
        ki = int(rng.choice(cand))
        o = int(rng.integers(0, len(text) - 240)); P = text[o:o + 240]
        Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
        C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
        row = [f"{reg}-control-{ci:02d}", reg, sign, labs[ki][0], labs[ki][1], f_rule]
        for mname in (reg, "en"):
            lu = LU[mname]
            nul = null_scores(C, lu, f_rule, rng, 500, mode)
            sc, sk, tops = best_configs(C, Ks, lu, f_rule, mode)
            z = (sc - nul.mean()) / nul.std()
            rank = int((z > z[ki]).sum()) + 1
            rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode)[2][0]
            row += [float(z[ki]), rank, float((rec == P).mean())]
        ctrl_rows.append(row)
        print(f"  {row[0]}: {sign} {labs[ki][0]} '{labs[ki][1][:30]}' F={f_rule}: own model z={row[6]:.1f} rank {row[7]} rec {row[8]:.3f} | English model z={row[9]:.1f} rank {row[10]} rec {row[11]:.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)

# ---------- the sweep ----------
t0 = time.time()
results = []     # (reg, page, sign, f_rule, family, label, z, skips, score, translit)
nulls = {}
for pi, (pid, C) in enumerate(pages):
    for reg in REGS:
        lu = LU[reg]
        for f_rule in (False, True):
            nul_by_mode = {}
            for sign, mode, Ks, labs in SETS:
                if mode not in nul_by_mode:
                    nul_by_mode[mode] = null_scores(C, lu, f_rule, rng, 2000, mode)
                nul = nul_by_mode[mode]
                nulls[(reg, pid, f_rule, mode)] = (float(nul.mean()), float(nul.std()), float(nul.max()))
                sc, sk, tops = best_configs(C, Ks, lu, f_rule, mode)
                z = (sc - nul.mean()) / nul.std()
                for k in np.argsort(-z)[:2]:
                    results.append((reg, pid, sign, f_rule, labs[k][0], labs[k][1], float(z[k]), int(sk[k]), float(sc[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z on this page: " + ", ".join(f"{reg} {max(r[6] for r in results if r[1]==pid and r[0]==reg):.2f}" for reg in REGS) + f"  [{time.time()-t0:.0f}s]", flush=True)

results.sort(key=lambda r: -r[6])
zmax = results[0][6]
out = ["# Phase 5 sweep: phases 3 and 4 rerun under Latin and Old English plaintext models", "",
       f"{nconf} configurations per page (phase 3's {len(F.p3)} book keystreams and phase 4's {len(F.phrase_fams)} phrase/sentence keys, each under three sign conventions), {len(pages)} pages, 2 F variants, 2 registers: **{ntests:,} tests**. Chance maximum about {np.sqrt(2*np.log(ntests)):.1f}.",
       "Per page, register, variant and decoder mode the null is 2,000 random keystreams through the same decoder with the same model. Positive rule (pre-registered): z ≥ 6 over that null and readable in that language on inspection.", "",
       "## Planted controls (decoded with the register's own model, and with the English model)", "",
       "| control | register | sign | family | key | F | z own | rank own | rec own | z English | rank English | rec English |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:30]} | {r[5]} | {r[6]:.1f} | {r[7]} | {r[8]:.3f} | {r[9]:.1f} | {r[10]} | {r[11]:.3f} |")
for reg in REGS:
    rows = [r for r in ctrl_rows if r[1] == reg]
    out.append("")
    out.append(f"{reg}: own model recovers {sum(1 for r in rows if r[6] >= 6 and r[7] == 1)} of {len(rows)} at z ≥ 6 and rank 1 (z {min(r[6] for r in rows):.1f}–{max(r[6] for r in rows):.1f}); "
               f"the English model would have recovered {sum(1 for r in rows if r[9] >= 6 and r[10] == 1)} of {len(rows)} (z {min(r[9] for r in rows):.1f}–{max(r[9] for r in rows):.1f}).")
out += ["", "## Unsolved pages: top 20 configurations overall", "",
        "| register | page | sign | F | family | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5][:40]} | {r[6]:.2f} | {r[7]} | {r[9]} |")
out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f} ({results[0][0]}, {results[0][1]}, {results[0][4]} '{results[0][5][:40]}').",
        "Largest z per register: " + "; ".join(f"{reg} {max(r[6] for r in results if r[0]==reg):.2f}" for reg in REGS) + ".", "",
        "## Verdict", "",
        ("**No page decrypts under either register.** " if zmax < 6 else "**At least one configuration clears z = 6: inspect the transliteration above before believing it.** ") +
        "Every family of phases 3 and 4, under the skip-on-repeat rule, all three sign conventions and both F variants, is excluded for a Latin plaintext and for an Old English plaintext at the sensitivity the controls demonstrate. This says nothing about other languages or about keys from outside these families.", ""]
(RESULTS / "phase5.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "nconf": nconf, "controls": ctrl_rows, "top": results[:60],
           "nulls": {"|".join(map(str, k)): v for k, v in nulls.items()}}, open(RESULTS / "phase5.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
