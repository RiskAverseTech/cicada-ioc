"""Phase 3 sweep: the book's keystream families, with the skip-on-repeat rule, on every
unsolved page.

PRE-REGISTERED POSITIVE RULE (written before running): a page counts as decrypted only if
its best configuration scores at least z = 6 above that page's own random-keystream null
(2,000 random keystreams through the identical decoder, same F-rule variant) AND the
transliteration reads as English to a human.  Anything below z = 6 is noise: the sweep makes
~640,000 page × configuration × variant tests, whose chance maximum is about z = 4.8.
Planted controls (solved plaintext enciphered with the same families + skip rule) must be
recovered at z >= 6 and rank first for their page, or the sweep is not trusted.
"""
import json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model, decode, null_scores, translit, S_MAX
from skip_decrypt import encrypt

rng = np.random.default_rng(3301)
lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
PR = np.array(primes(LMAX + 120))


def rep(v, L=LMAX):
    v = np.asarray(v) % N
    return np.resize(v, L)


# ---------- keystream families: list of (family, label, K[LMAX]) ----------
fams = []
for s in range(N):
    fams.append(("shift", f"s={s}", rep([s])))
words = set()
for f in ("iddqd__liber-primus__translation.txt", "iddqd__liber-primus__known-plain-text--headlines.txt"):
    txt = (RAW / f).read_text(encoding="utf-8")
    for w in re.findall(r"[A-Za-z']+", txt):
        r = english_to_runes(w)
        if 2 <= len(r) <= 20: words.add(tuple(r))
words |= {tuple([23, 10, 1, 10, 9, 10, 16, 26]), tuple([0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18])}
for w in sorted(words):
    fams.append(("vigenere-word", to_latin(w), rep(w)))
    fams.append(("vigenere-word-rev", to_latin(w) + "ʳ", rep(w[::-1])))
for s in range(0, 101):
    fams.append(("primes", f"p[n+{s}]", rep(PR[s:s + LMAX])))
    fams.append(("primes-1 (totient)", f"p[n+{s}]-1", rep(PR[s:s + LMAX] - 1)))
    fams.append(("primes+1", f"p[n+{s}]+1", rep(PR[s:s + LMAX] + 1)))
fib = [0, 1]
while len(fib) < LMAX + 40: fib.append(fib[-1] + fib[-2])
luc = [2, 1]
while len(luc) < LMAX + 40: luc.append(luc[-1] + luc[-2])
for s in range(14):
    fams.append(("fibonacci", f"F[n+{s}]", rep(np.array(fib[s:s + LMAX]) % N)))
    fams.append(("lucas", f"L[n+{s}]", rep(np.array(luc[s:s + LMAX]) % N)))
for a in range(N):
    for b in range(N):
        if a == 0: continue
        fams.append(("affine position", f"{a}·n+{b}", rep((a * np.arange(LMAX) + b) % N)))
for b in range(N):
    fams.append(("square position", f"n²+{b}", rep((np.arange(LMAX) ** 2 + b) % N)))
for o in range(0, len(plain)):
    fams.append(("self running key", f"plaintext@{o}", rep(np.take(plain, np.arange(o, o + LMAX), mode="wrap"))))
Kall = np.stack([k for _, _, k in fams]).astype(np.int64)
labels = [(f, l) for f, l, _ in fams]
print(f"{len(fams)} shared configurations per page (+4 neighbour-page keys per page), {len(pages)} pages, 2 F-rule variants", flush=True)


def page_keys(idx):
    """Neighbouring pages' runes as running keys, both directions."""
    out = []
    for name, nb in (("prev", idx - 1), ("next", idx + 1)):
        if 0 <= nb < len(pages):
            k = pages[nb][1]
            out.append(("neighbour page", f"{name} {pages[nb][0]}", rep(np.resize(k, LMAX))))
            out.append(("neighbour page", f"{name} {pages[nb][0]} reversed", rep(np.resize(k[::-1], LMAX))))
    return out


def best_configs(C, Ks, f_rule, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


# ---------- planted controls ----------
controls = []
ctrl_rows = []
for ci in range(20):
    o = rng.integers(0, len(plain) - 240)
    P = plain[o:o + 240]
    fam = ["vigenere-word", "primes-1 (totient)", "affine position", "self running key", "shift"][ci % 5]
    cand = [i for i, (f, _) in enumerate(labels) if f == fam]
    ki = int(rng.choice(cand))
    f_rule = bool(ci % 2)
    C = encrypt(P, Kall[ki], f_rule=f_rule, rng=rng, soft=0.81)
    controls.append((f"control-{ci:02d}", C, ki, f_rule, P))
t0 = time.time()
for name, C, ki, f_rule, P in controls:
    nul = null_scores(C, lu, f_rule, rng, 500)
    sc, sk, tops = best_configs(C, Kall, f_rule)
    z = (sc - nul.mean()) / nul.std()
    rank = int((z > z[ki]).sum()) + 1
    rec = decode(C, Kall[ki:ki + 1], lu, f_rule)[2][0]
    ctrl_rows.append((name, labels[ki][0], labels[ki][1], f_rule, float(z[ki]), rank, float((rec == P).mean())))
    print(f"  {name}: {labels[ki][0]} {labels[ki][1]} F={f_rule}: z={z[ki]:.1f} rank {rank}, recovered {(rec == P).mean():.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)

# ---------- the sweep ----------
t0 = time.time()
results = []     # (page, variant, family, label, z, skips, score, translit)
nulls = {}
for pi, (pid, C) in enumerate(pages):
    Ks = np.vstack([Kall] + [k[None, :] for _, _, k in page_keys(pi)]) if page_keys(pi) else Kall
    labs = labels + [(f, l) for f, l, _ in page_keys(pi)]
    for f_rule in (False, True):
        nul = null_scores(C, lu, f_rule, rng, 2000)
        nulls[(pid, f_rule)] = (float(nul.mean()), float(nul.std()), float(nul.max()))
        sc, sk, tops = best_configs(C, Ks, f_rule)
        z = (sc - nul.mean()) / nul.std()
        for k in np.argsort(-z)[:5]:
            results.append((pid, f_rule, labs[k][0], labs[k][1], float(z[k]), int(sk[k]), float(sc[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z so far on this page: {max(r[4] for r in results if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

results.sort(key=lambda r: -r[4])
ntests = len(pages) * 2 * (len(fams) + 4)
out = ["# Phase 3 sweep: the book's keystream families with the skip-on-repeat rule", "",
       f"{len(fams)} shared keystream configurations (+ up to 4 neighbour-page keys per page), {len(pages)} pages, 2 F-rule variants: about {ntests:,} tests.",
       "Per page and variant, the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.", "",
       "## Planted controls", "", "| control | family | key | F rule | z of true key | rank among all configs | runes recovered |", "|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.1f} | {r[5]} | {r[6]:.3f} |")
out += ["", f"Controls recovered at z ≥ 6 and rank 1: {sum(1 for r in ctrl_rows if r[4] >= 6 and r[5] == 1)} of {len(ctrl_rows)}.", "",
        "## Unsolved pages: top 15 configurations overall", "",
        "| page | F rule | family | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|"]
for r in results[:15]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.2f} | {r[5]} | {r[7]} |")
zmax = results[0][4]
out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f}. Expected chance maximum for this many tests: about 4.8.", "",
        "## Verdict", "",
        ("**No page decrypts.** " if zmax < 6 else "**At least one page clears z = 6: inspect the transliteration above before believing it.** ") +
        f"The families tested (constant shifts, Vigenère with every word of the solved text and headlines, prime streams p, p−1, p+1 at 101 starting points, Fibonacci and Lucas, affine and square position formulas, the solved plaintext as a running key at every offset, and neighbouring pages as running keys), each with and without the F rule and with the skip-on-repeat rule, are excluded at the sensitivity the controls demonstrate. This says nothing about keystreams outside these families.", ""]
(RESULTS / "phase3.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "controls": ctrl_rows, "top": results[:50], "nulls": {f"{k[0]}|{k[1]}": v for k, v in nulls.items()}}, open(RESULTS / "phase3.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
