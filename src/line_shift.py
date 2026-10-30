"""Is the line-first rune plaintext under one fixed key value?  (2026-10-30; registration results/line_shift_registration.md)
Column 0 of the 55 unsolved pages against English letter profiles shifted by k under three signs; log-likelihood gain over
the page's own distribution, maximised over 87 cells, with a multinomial look-elsewhere null and planted controls.
Output: results/line_shift.md.  Reproduce: .venv/bin/python -I src/line_shift.py
"""
import re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, english_to_runes
import corpus

t0 = time.time(); rng = np.random.default_rng(64); NDRAW = 5000
LET = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
col0, wordinit, allr = [], [], []
for k in range(16, 72):
    new, pending = True, True
    for ch in chunks[k]:
        if ch == '/': new = True; continue
        if ch in SEP: pending = True; continue
        if ch in IDX:
            r = IDX[ch]; allr.append(r)
            if new: col0.append(r); wordinit.append(pending)
            new = pending = False
col0, wordinit, allr = np.array(col0), np.array(wordinit), np.array(allr)
page_p = (np.bincount(allr, minlength=N) + 0.5) / (len(allr) + 0.5 * N)

text = corpus.TEXTS["emerson_essays1"][0](); words = [np.array(english_to_runes(w)) for w in re.findall(r"[A-Za-z]+", text)]; words = [w for w in words if len(w)]
prof = {"word-initial": np.concatenate([w[:1] for w in words]), "interior": np.concatenate([w[1:] for w in words if len(w) > 1]), "all": np.concatenate(words)}
prof = {k: (np.bincount(v, minlength=N) + 0.5) / (len(v) + 0.5 * N) for k, v in prof.items()}
SIGNS = {"sub": lambda p, k: (p + k) % N, "add": lambda p, k: (p - k) % N, "beaufort": lambda p, k: (k - p) % N}


def predicted(profile, sign, k):
    q = np.zeros(N)
    for p in range(N): q[SIGNS[sign](p, k)] += profile[p]
    return q


def best_cell(counts, profile):
    base = (counts * np.log(page_p)).sum(); best = (-np.inf, None, None)
    for sign in SIGNS:
        for k in range(N):
            g = (counts * np.log(predicted(profile, sign, k))).sum() - base
            if g > best[0]: best = (g, sign, k)
    return best


def pvalue(n, profile, g_obs):
    draws = rng.multinomial(n, page_p, size=NDRAW); mx = np.array([best_cell(d, profile)[0] for d in draws])
    return float((mx >= g_obs).mean()), float(np.median(mx))


rows, claims = [], {}
PAIRS = [("T1a", "all 594", col0, "all"), ("T1b", "all 594", col0, "word-initial"), ("T2", "word-initial lines", col0[wordinit], "word-initial"), ("T3", "mid-word lines", col0[~wordinit], "interior")]
for cid, label, obs, pname in PAIRS:
    c = np.bincount(obs, minlength=N); g, sign, k = best_cell(c, prof[pname]); p, med = pvalue(len(obs), prof[pname], g)
    q = predicted(prof[pname], sign, k) * len(obs); order = np.argsort(-q)[:6]
    rows.append(f"| {cid} | {label} ({len(obs)}) | {pname} | {sign} k={k} | {g:+.1f} (null median {med:+.1f}) | {p:.3f} | " + ", ".join(f"{LET[i]} {c[i]} vs {q[i]:.0f}" for i in order) + " |")
    claims[cid] = p >= 0.01
    # control: a synthetic column from the shifted profile, sub k = 7
    synth = rng.choice(N, size=len(obs), p=predicted(prof[pname], "sub", 7)); cs = np.bincount(synth, minlength=N)
    gs, ss, ks = best_cell(cs, prof[pname]); ps, _ = pvalue(len(obs), prof[pname], gs)
    rows.append(f"| control for {cid} | synthetic ({len(obs)}) from sub k=7 | {pname} | {ss} k={ks} | {gs:+.1f} | {ps:.4f} | {'found' if (ps < 0.01 and ss == 'sub' and ks == 7) else 'MISSED'} |")
    claims[f"C{cid}"] = bool(ps < 0.01 and ss == "sub" and ks == 7)
    print(f"{cid} done [{time.time()-t0:.0f}s]", flush=True)

T1 = claims["T1a"] and claims["T1b"]; T0 = all(claims[f"C{c}"] for c in ("T1a", "T1b", "T2", "T3"))
out = ["# Is the line-first rune plaintext under one fixed key value?", "",
       f"Column 0 of the 55 unsolved pages against English profiles (Emerson, rune spelling) shifted by k under three signs; statistic: log-likelihood gain over the page's own rune distribution, maximised over 87 (sign, k) cells; p from {NDRAW:,} multinomial draws from the page distribution with the same maximisation. Registration: `results/line_shift_registration.md`.", "",
       "| pairing | observed | profile | best cell | gain | p | best cell's top runes: observed vs predicted |", "|---|---|---|---|---|---|---|"] + rows + ["", "## Claims", "",
       f"- T0 controls 4/4: **{'holds' if T0 else 'fails'}**.", f"- T1 all 594 against both profiles, p ≥ 0.01: **{'holds' if T1 else 'fails'}**.",
       f"- T2 word-initial lines against the word-initial profile, p ≥ 0.01: **{'holds' if claims['T2'] else 'fails'}**.", f"- T3 mid-word lines against the interior profile, p ≥ 0.01: **{'holds' if claims['T3'] else 'fails'}**.", "",
       "Reading: written after the run. [stated — the table]", "", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/line_shift.py`.", ""]
(RESULTS / "line_shift.md").write_text("\n".join(out)); print("\n".join(out[4:]))
