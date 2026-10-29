"""E56w with fillers on the spend-repair base (2026-10-29, §58): registration, prediction and check in one script.
  --predict   simulate E56w+n (src/mechanism_lane.py: gated lag-5 / lag-6 echo, r = 0.5, on the spend repair R0 at q = 0.81,
              with R4n's filler, one extra neighbour-checked uniform rune at a uniform in-word position in 45 % of words
              of length >= 2, and NO T-writing hold repair) and write predicted mean ± sd for two sets:
              A  §47's twelve statistics (ten judged) over 200 replicates, judged by §47's rule, |z| <= 3 on every one of
                 D, D_in, L3, L4, L5, L5S, BIG, L6T, SHARE, Sfreq.  LP2's values are public (86 / 63 / 179 / 131 / 102 /
                 11 / 9 / 77 / 7.21 / 0.0335), so this is a pre-registered comparison against known values, not a blind one.
              B  §57's sixteen out-of-sample cells plus the two declared word-length cells over 300 replicates, |z| <= 2.5
                 per cell, judged as a set.  LP2's values are in results/e56w_r4n_predictions.json (public since §57).
  --check     compare both sets with LP2.
Why this rule: §57 found that E56w+R4n fails the lag-6 count in words of ten or more runes, where its T-writing hold
repair, not its echo, puts the hits; its filler alone is what the §55 fingerprint supports.  E56w+n keeps the filler
and the echoes and drops the repair.  Written as the next registered rule at the end of §57, before any simulation of it.
What is expected and why, stated before running: the filler lowers D below E56w's 84 (a filler never repeats its
neighbour) and lengthens words, so L3 / L4 rise toward R4n's 171 / 116; without the hold repair L6T should return to
E56w's 80; L5S should stay near 4, so the rule is expected to FAIL the S cell as E56w does.  The question is whether it
clears everything else in both sets at once, which no rule has.  Writes results/e56w_n.md / .json.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RESULTS
import mechanism_lane as ML
_argv, sys.argv = sys.argv, sys.argv[:1]
import e56w_r4n_predictions as E57
sys.argv = _argv

RULE = "E56w+n"; NREP_A = 200; NREP_B = 300
OUT = RESULTS / "e56w_n.json"; MD = RESULTS / "e56w_n.md"

if "--predict" in sys.argv:
    t0 = time.time(); ML.rng = np.random.default_rng(58)
    repsA = [ML.measure(ML.simulate(RULE)) for _ in range(NREP_A)]
    repsB = [E57.measure(ML.simulate(RULE)) for _ in range(NREP_B)]
    predA = {s: dict(mean=float(np.mean([r[s] for r in repsA])), sd=float(np.std([r[s] for r in repsA]))) for s in ML.STATS}
    predB = {s: dict(mean=float(np.mean([r[s] for r in repsB])), sd=float(np.std([r[s] for r in repsB]))) for s in E57.STATS}
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), rule=RULE, nrepA=NREP_A, nrepB=NREP_B, r=ML.R_GATE, q=ML.Q, p_null=0.45, A=predA, B=predB), open(OUT, "w"), indent=1)
    lines = [f"# {RULE}: predictions written before the check", "", f"Written {time.strftime('%Y-%m-%d %H:%M')} ({time.time() - t0:.0f} s). Set A: {NREP_A} replicates, §47's statistics. Set B: {NREP_B} replicates, §57's cells. LP2 columns empty until `--check`.", "", "| set | statistic | predicted mean ± sd |", "|---|---|---|"]
    for s in ML.STATS: lines.append(f"| A | {s} | {predA[s]['mean']:.3f} ± {predA[s]['sd']:.3f} |")
    for s in E57.STATS: lines.append(f"| B | {s} | {predB[s]['mean']:.3f} ± {predB[s]['sd']:.3f} |")
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    d = json.load(open(OUT)); refA = ML.measure(ML.LP2); refB = E57.measure(E57.E49.LP2)
    mech = json.load(open(RESULTS / "mechanism.json"))["rules"]; e57 = json.load(open(RESULTS / "e56w_r4n_predictions.json"))["predictions"]
    def cell(rule, s):
        r = mech.get(rule)
        if r is None or s not in r["mean"]: return "—"
        m, sd = r["mean"][s], max(r["sd"][s], 1e-9); return f"{m:.4g} ± {sd:.2g} (z {(refA[s] - m) / sd:+.1f})"
    lines = [f"# {RULE}: §47's ten statistics and §57's sixteen cells against LP2", "", f"Predictions written {d['written']} (commit recorded in README §58); checked afterwards.", "",
             f"## Set A: §47's statistics ({d['nrepA']} replicates; rule |z| ≤ 3 on the ten judged)", "", "| statistic | LP2 | E56w+n predicted | z | holds | E56w (§47) | E56w+R4n (§47) |", "|---|---|---|---|---|---|---|"]
    failA = []
    for s in ML.STATS:
        m, sd = d["A"][s]["mean"], max(d["A"][s]["sd"], 1e-9); z = (refA[s] - m) / sd; judged = s in ML.JUDGE; ok = abs(z) <= 3
        if judged and not ok: failA.append(s)
        lines.append(f"| {s} | {refA[s]:.4g} | {m:.4g} ± {sd:.2g} | {z:+.2f} | {('yes' if ok else 'NO') if judged else 'not judged'} | {cell('E56w', s)} | {cell('E56w+R4n', s)} |")
    lines += ["", f"Set A verdict: {'survives' if not failA else 'fails: ' + ', '.join(failA)}.", "",
              f"## Set B: §57's cells ({d['nrepB']} replicates; rule |z| ≤ 2.5 per cell, P1–P10 judged as a set)", "", "| statistic | LP2 | E56w+n predicted | z | holds | E56w+R4n (§57) z |", "|---|---|---|---|---|---|"]
    held = tot = 0
    for s in E57.STATS:
        m, sd = d["B"][s]["mean"], max(d["B"][s]["sd"], 1e-9); z = (refB[s] - m) / sd; ok = abs(z) <= 2.5; decl = s.startswith("P11")
        if not decl: held += ok; tot += 1
        z57 = (refB[s] - e57[s]["mean"]) / max(e57[s]["sd"], 1e-9)
        lines.append(f"| {s} | {refB[s]:.3f} | {m:.3f} ± {sd:.3f} | {z:+.2f} | {'yes' if ok else 'NO'}{' (declared)' if decl else ''} | {z57:+.2f} |")
    lines += ["", f"Set B: {held} of {tot} out-of-sample cells hold.", "", "Reproduce: `.venv/bin/python -I src/e56w_n_lane.py --predict` then `--check`."]
    json.dump(dict(d, lp2A=refA, lp2B=refB, failA=failA, heldB=held, cellsB=tot), open(OUT, "w"), indent=1, default=float)
    MD.write_text("\n".join(lines) + "\n"); print("\n".join(lines))
