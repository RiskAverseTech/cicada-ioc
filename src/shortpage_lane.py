"""Short-page lane (2026-10-27): a secondary, pre-registered rule for the pages on which the z >= 6
rule has little power (README §23, results/power.md).

PRE-REGISTERED RULE, written before any page was scored.  On the nine pages below the power
threshold a cell (page x sign x F variant x key) counts as a candidate only if ALL of
  (1) z_uni >= 4: unigram decoder score at least 4 sigma above the page's own null of 2,000 random
      keystreams through the identical decoder (same F variant, mode, lane);
  (2) rank first within its key family: a hypothesis is one key (family label + key); its z_uni is
      the largest over its six cells (three sign conventions x two F variants); the hypothesis must
      have the largest such z_uni among all keys in its family on that page.  AMENDED AFTER THE
      CONTROLS, BEFORE ANY PAGE RESULT WAS READ: the first wording ranked cells rather than keys, and
      the controls failed it 16 of 18 times because the same key decoded under the other F variant
      (a tighter null) scored a slightly higher z than the planted cell, i.e. a key was outranked by
      itself.  Three pages had been scored under the stricter wording with no candidate; ranking by
      key is looser, so the amendment can only add candidates, never remove one.
  (3) z_big >= 3: the bigram log-likelihood ratio of the decoded text is at least 3 sigma above the
      bigram LLR of the decodes the same 2,000 random keystreams produced (a statistic the unigram
      decoder did not maximise);
  (4) lane B only: free-null score at least 20 nats above the base decoder for the same key (§22);
  (5) it reads as English to a human.  Candidates meeting (1)-(4) are printed in full for that check.
Expected chance load: about 45,700 tests per page per lane, so a few cells per page at z_uni >= 4 by
chance; (2) and (3) are the filters, and (5) decides.  Controls: one plant per page length in each
lane, families and signs cycled; the lane is trusted only if most controls pass (1)-(4).
Lane A: soft anti-repeat rule 0.81, base decoder.  Lane B: hard rule + 22 % uniform nulls, free-null
decoder at prior -0.8.  Key library: families.ALLSETS (22,863 configurations).
Usage: .venv/bin/python -I src/shortpage_lane.py   (SMOKE=1: one page, one control, 200 nulls).
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt, combine
import families as F

SMOKE = os.environ.get("SMOKE") == "1"
rng = np.random.default_rng(4049)
lu, lb, plain, pages = F.lu, F.lb, F.plain, dict(F.pages)
PAGE_IDS = ["LP2-49", "LP2-55", "LP2-51", "LP2-32", "LP2-22", "LP2-14", "LP2-15", "LP2-53", "LP2-06"]
if SMOKE: PAGE_IDS = PAGE_IDS[:1]
SETS = F.ALLSETS
NREPS = 200 if SMOKE else 2000
PEN, Q, SOFT = -0.8, 0.22, 0.81
Z_UNI, Z_BIG, MARGIN = 4.0, 3.0, 20.0
LOGU = np.log(1 / N)


def bigram_many(P):
    P = np.asarray(P); return (lu[P[:, 0]] - LOGU) + (lb[P[:, :-1], P[:, 1:]] - LOGU).sum(1)


def run_decode(C, Ks, f_rule, mode, lane, batch=1000):
    nm = None
    if lane == "B":
        nm = np.ones(len(C), bool); nm[0] = False
    sc, dec = [], []
    for b in range(0, len(Ks), batch):
        s, _, d = decode(C, Ks[b:b + batch], lu, f_rule, mode, None, nm, PEN) if lane == "B" else decode(C, Ks[b:b + batch], lu, f_rule, mode)
        sc.append(s); dec.append(d)
    return np.concatenate(sc), np.concatenate(dec)


def null_cell(C, f_rule, mode, lane):
    Ks = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2))
    sc, dec = run_decode(C, Ks, f_rule, mode, lane, batch=500)
    bg = bigram_many(dec)
    return (sc.mean(), sc.std(), bg.mean(), bg.std(), sc.max())


def score_page(C, lane, only_family=None, record_all=False):
    """Scores every configuration (or one family label) in all six sign x F cells.  Returns rows and nulls."""
    rows, nulls = [], {}
    rec_thr = -np.inf if record_all else Z_UNI - 1.0
    for f_rule in (False, True):
        for si, (sign, mode, Ks, labs) in enumerate(SETS):
            idx = np.arange(len(labs)) if only_family is None else np.array([i for i, (f, _) in enumerate(labs) if f == only_family])
            if len(idx) == 0: continue
            key = (f_rule, mode)
            if key not in nulls: nulls[key] = null_cell(C, f_rule, mode, lane)
            m0, s0, b0, sb, mx = nulls[key]
            sc, dec = run_decode(C, Ks[idx], f_rule, mode, lane)
            zu = (sc - m0) / s0
            zb = (bigram_many(dec) - b0) / sb
            for k in np.where(zu >= rec_thr)[0]:               # keep a margin below the rule for the record
                rows.append(dict(sign=sign, F=f_rule, set=si, ki=int(idx[k]), fam=labs[idx[k]][0], key=labs[idx[k]][1], zu=float(zu[k]), zb=float(zb[k]), sc=float(sc[k]), translit=translit(dec[k])))
            # the family ranking needs every key's z over all six cells, not only the recorded rows
            for k in range(len(idx)):
                fam, kid = labs[idx[k]][0], (labs[idx[k]][0], int(idx[k]))
                fam_best[fam] = max(fam_best.get(fam, -99.0), float(zu[k]))
                key_best[kid] = max(key_best.get(kid, -99.0), float(zu[k]))
    return rows, nulls


def apply_rule(C, rows, lane):
    out = []
    for r in rows:
        kid = (r["fam"], r["ki"])
        # (1) z_uni, (3) z_big, (2) the key leads its family and this row is the key's best cell
        if r["zu"] < Z_UNI or r["zb"] < Z_BIG or key_best[kid] < fam_best[r["fam"]] - 1e-9 or r["zu"] < key_best[kid] - 1e-9: continue
        if lane == "B":
            sign, mode, Ks, labs = SETS[r["set"]]
            base = float(decode(C, Ks[r["ki"]:r["ki"] + 1], lu, r["F"], mode)[0][0]); r["free_minus_base"] = r["sc"] - base
            if r["free_minus_base"] < MARGIN: continue
        out.append(r)
    return out


def plant(n, lane, ci):
    """One control at length n: family and sign cycled, F by ci; returns ciphertext and the truth."""
    fams = ["vigenere-word", "phrase-3", "primes", "self running key", "phrase-2", "fibonacci", "affine position", "sentence", "primes+1"]
    fam = fams[ci % len(fams)]
    sets_with = [s for s in SETS if any(f == fam for f, _ in s[3])]
    sign, mode, Ks, labs = sets_with[ci % 3]; f_rule = bool((ci // 3) % 2)
    cand = [i for i, (f, _) in enumerate(labs) if f == fam]
    while True:
        ki = int(rng.choice(cand))
        if not np.all(Ks[ki] == Ks[ki][0]): break
    Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
    o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
    if lane == "A":
        C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=SOFT, mode=sign)
    else:
        C, j, pi, prev = [], 0, 0, None
        while len(C) < n and pi < len(P):
            p = P[pi]; pi += 1
            if f_rule and p == 0: C.append(0); prev = 0
            else:
                c = combine(p, Ktrue[j], sign)
                while prev is not None and c == prev: j += 1; c = combine(p, Ktrue[j], sign)
                C.append(c); j += 1; prev = c
            if len(C) < n and rng.random() < Q: C.append(int(rng.integers(0, N))); prev = C[-1]
        C = np.array(C)
    return C, dict(fam=fam, sign=sign, F=f_rule, key=labs[ki][1][:30], ki=ki)


t0 = time.time()
lengths = sorted({len(pages[p]) for p in PAGE_IDS})
report = {"rule": dict(z_uni=Z_UNI, z_big=Z_BIG, margin_nats=MARGIN, nulls=NREPS, prior=PEN, max_skip=MAX_SKIP), "controls": [], "pages": {}}

# ---------- controls ----------
for lane in ("A", "B"):
    for ci, n in enumerate(lengths if not SMOKE else lengths[:1]):
        fam_best, key_best = {}, {}
        C, truth = plant(n, lane, ci)
        rows, nulls = score_page(C, lane, only_family=truth["fam"], record_all=True)
        hits = apply_rule(C, rows, lane)
        mine = [r for r in rows if r["ki"] == truth["ki"] and r["sign"] == truth["sign"] and r["F"] == truth["F"]]
        zu = mine[0]["zu"] if mine else float("nan"); zb = mine[0]["zb"] if mine else float("nan")
        passed = any(h["ki"] == truth["ki"] for h in hits)
        zu, zb = key_best[(truth["fam"], truth["ki"])], max(r["zb"] for r in rows if r["ki"] == truth["ki"])
        report["controls"].append(dict(lane=lane, n=n, **truth, zu=zu, zb=zb, passed=bool(passed), other_hits=len(hits) - int(passed)))
        print(f"control lane {lane} n={n} {truth['fam']} {truth['sign']} F={truth['F']} '{truth['key']}': z_uni {zu:.1f} z_big {zb:.1f} rank-first {'yes' if key_best[(truth['fam'], truth['ki'])] >= fam_best[truth['fam']] - 1e-9 else 'no'} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

# ---------- the nine pages ----------
for pid in PAGE_IDS:
    C = pages[pid]
    for lane in ("A", "B"):
        fam_best, key_best = {}, {}
        rows, nulls = score_page(C, lane)
        hits = apply_rule(C, rows, lane)
        n4 = sum(1 for r in rows if r["zu"] >= Z_UNI)
        best = max(rows, key=lambda r: r["zu"]) if rows else None
        report["pages"][f"{pid}|{lane}"] = dict(n=len(C), cells_z4=n4, best=best, candidates=hits, null_max=max(v[4] for v in nulls.values()))
        print(f"{pid} ({len(C)} runes) lane {lane}: {n4} cells at z_uni >= 4, best z {best['zu'] if best else 0:.2f} ({best['fam'] if best else ''}); candidates after rank + bigram{' + margin' if lane=='B' else ''}: {len(hits)}  [{time.time()-t0:.0f}s]", flush=True)
        for h in hits:
            print(f"    CANDIDATE {h['sign']} F={h['F']} {h['fam']} '{h['key']}' z_uni {h['zu']:.2f} z_big {h['zb']:.2f}: {h['translit']}", flush=True)

report["seconds"] = time.time() - t0
json.dump(report, open(RESULTS / ("shortpage_smoke.json" if SMOKE else "shortpage.json"), "w"), indent=1)

# ---------- markdown ----------
out = [f"# Short-page lane: z >= {Z_UNI:.0f}, rank first within family, bigram z >= {Z_BIG:.0f}, readable", "",
       f"Pages below the §23 power threshold, scored with a secondary rule fixed before scoring (module docstring; rule (2) was re-worded after the controls and before any page result was read, see docstring). {NREPS} random-keystream nulls per cell; decoder max_skip {MAX_SKIP}; lane B prior {PEN}. A hypothesis is a key; its z_uni is the best of its six sign x F cells.", "",
       "## Controls (one plant per page length per lane)", "", "| lane | length | family | sign | F | key | z_uni | z_big | passes (1)-(4) | other cells passing |", "|---|---|---|---|---|---|---|---|---|---|"]
for c in report["controls"]:
    out.append(f"| {c['lane']} | {c['n']} | {c['fam']} | {c['sign']} | {c['F']} | {c['key']} | {c['zu']:.1f} | {c['zb']:.1f} | {'yes' if c['passed'] else 'no'} | {c['other_hits']} |")
for lane in ("A", "B"):
    cs = [c for c in report["controls"] if c["lane"] == lane]
    out.append(f"\nLane {lane}: {sum(c['passed'] for c in cs)} of {len(cs)} controls pass (1)-(4).")
out += ["", "## Pages", "", "| page | runes | lane | cells at z_uni >= 4 | null max | best z_uni (family) | candidates after (1)-(4) |", "|---|---|---|---|---|---|---|"]
for k, v in report["pages"].items():
    pid, lane = k.split("|"); b = v["best"]
    out.append(f"| {pid} | {v['n']} | {lane} | {v['cells_z4']} | {v['null_max']:.1f} | {b['zu']:.2f} ({b['fam']}) | {len(v['candidates'])} |" if b else f"| {pid} | {v['n']} | {lane} | 0 | {v['null_max']:.1f} | – | 0 |")
out += ["", "## Candidates meeting (1)-(4), for the readability check (5)", ""]
anyc = False
for k, v in report["pages"].items():
    for h in v["candidates"]:
        anyc = True; pid, lane = k.split("|")
        out.append(f"- **{pid} lane {lane}** {h['sign']} F={h['F']} {h['fam']} '{h['key']}', z_uni {h['zu']:.2f}, z_big {h['zb']:.2f}" + (f", free−base {h['free_minus_base']:+.0f}" if 'free_minus_base' in h else "") + f": `{h['translit']}`")
if not anyc: out.append("None.")
out += ["", f"Runtime {report['seconds']/60:.0f} minutes.", ""]
(RESULTS / ("shortpage_smoke.md" if SMOKE else "shortpage.md")).write_text("\n".join(out) + "\n")
print("\n".join(out[-12:]))
