"""Phase 4 sweep: phrase and sentence keys from the book itself, under the skip-on-repeat
rule, with all three key-sign conventions; plus phase 3's families under the two sign
conventions phase 3 did not run.

PRE-REGISTERED POSITIVE RULE (same as phase 3, written before running): a page counts as
decrypted only if its best configuration scores z >= 6 above that page's own
random-keystream null (2,000 random keystreams through the identical decoder, same F-rule
variant) AND the transliteration reads as English to a human.  The sweep makes roughly
2.6 million page x configuration x variant tests, whose chance maximum is about z = 5.4.
Planted controls (solved plaintext enciphered with the same families, the skip rule at
81 %, each sign convention and each F variant) must be recovered at z >= 6 and rank first
for their page, or the sweep is not trusted.

Sign conventions.  "sub": C = P + K, decrypt P = C - K (phase 3).  "add": C = P - K,
decrypt P = C + K (run as mode "sub" on -K).  "beaufort": C = K - P, decrypt P = K - C.
"""
import json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model, decode, null_scores, translit, S_MAX
from skip_decrypt import encrypt

rng = np.random.default_rng(4001)
lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
PR = np.array(primes(LMAX + 120))


def rep(v, L=LMAX):
    v = np.asarray(v) % N
    return np.resize(v, L)


# ---------- phrase and sentence keys from the translation's numbered lines ----------
lines = []
for ln in (RAW / "iddqd__liber-primus__translation.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\s*\d+\.\d+\.\d+\.\d+\s+(.*)$", ln)
    if not m: continue
    words = [w for w in re.findall(r"[A-Za-z']+", m.group(1))]
    if len(words) >= 1: lines.append(words)
print(f"{len(lines)} numbered lines, {sum(len(l) for l in lines)} words", flush=True)

keys = {}      # rune tuple -> (family, label)
def add(fam, label, runes):
    t = tuple(int(x) for x in runes)
    if 2 <= len(t) and t not in keys: keys[t] = (fam, label)
for words in lines:
    for n in (2, 3, 4):
        for i in range(len(words) - n + 1):
            ph = " ".join(words[i:i + n])
            r = english_to_runes(ph)
            add(f"phrase-{n}", ph, r)
            add(f"phrase-{n}-rev", ph + " ʳ", r[::-1])
    if len(words) >= 5:
        sent = " ".join(words); r = english_to_runes(sent)
        add("sentence", sent[:60], r)
        add("sentence-rev", sent[:60] + " ʳ", r[::-1])
phrase_fams = [(fam, lab, rep(t)) for t, (fam, lab) in keys.items()]
print(f"{len(phrase_fams)} distinct phrase/sentence keys", flush=True)

# ---------- phase 3's families, for the two sign conventions phase 3 did not run ----------
p3 = []
for s in range(N):
    p3.append(("shift", f"s={s}", rep([s])))
words = set()
for f in ("iddqd__liber-primus__translation.txt", "iddqd__liber-primus__known-plain-text--headlines.txt"):
    txt = (RAW / f).read_text(encoding="utf-8")
    for w in re.findall(r"[A-Za-z']+", txt):
        r = english_to_runes(w)
        if 2 <= len(r) <= 20: words.add(tuple(r))
words |= {tuple([23, 10, 1, 10, 9, 10, 16, 26]), tuple([0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18])}
for w in sorted(words):
    p3.append(("vigenere-word", to_latin(w), rep(w)))
    p3.append(("vigenere-word-rev", to_latin(w) + "ʳ", rep(w[::-1])))
for s in range(0, 101):
    p3.append(("primes", f"p[n+{s}]", rep(PR[s:s + LMAX])))
    p3.append(("primes-1 (totient)", f"p[n+{s}]-1", rep(PR[s:s + LMAX] - 1)))
    p3.append(("primes+1", f"p[n+{s}]+1", rep(PR[s:s + LMAX] + 1)))
fib = [0, 1]
while len(fib) < LMAX + 40: fib.append(fib[-1] + fib[-2])
luc = [2, 1]
while len(luc) < LMAX + 40: luc.append(luc[-1] + luc[-2])
for s in range(14):
    p3.append(("fibonacci", f"F[n+{s}]", rep(np.array(fib[s:s + LMAX]) % N)))
    p3.append(("lucas", f"L[n+{s}]", rep(np.array(luc[s:s + LMAX]) % N)))
for a in range(1, N):
    for b in range(N):
        p3.append(("affine position", f"{a}·n+{b}", rep((a * np.arange(LMAX) + b) % N)))
for b in range(N):
    p3.append(("square position", f"n²+{b}", rep((np.arange(LMAX) ** 2 + b) % N)))
for o in range(0, len(plain)):
    p3.append(("self running key", f"plaintext@{o}", rep(np.take(plain, np.arange(o, o + LMAX), mode="wrap"))))

# ---------- configuration sets: (sign, decoder mode, key matrix, labels) ----------
SETS = []
Kph = np.stack([k for _, _, k in phrase_fams]).astype(np.int64); Lph = [(f, l) for f, l, _ in phrase_fams]
Kp3 = np.stack([k for _, _, k in p3]).astype(np.int64); Lp3 = [(f, l) for f, l, _ in p3]
SETS.append(("sub",      "sub",      Kph,            Lph))
SETS.append(("add",      "sub",      (-Kph) % N,     Lph))
SETS.append(("beaufort", "beaufort", Kph,            Lph))
SETS.append(("add",      "sub",      (-Kp3) % N,     Lp3))
SETS.append(("beaufort", "beaufort", Kp3,            Lp3))
nconf = sum(len(L) for _, _, _, L in SETS)
ntests = nconf * len(pages) * 2
print(f"{len(phrase_fams)} phrase keys x 3 signs + {len(p3)} phase-3 keys x 2 new signs = {nconf} configurations per page; "
      f"{len(pages)} pages x 2 F variants: {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)


def best_configs(C, Ks, f_rule, mode, batch=1200):
    scores = np.empty(len(Ks)); skips = np.empty(len(Ks), dtype=int); tops = {}
    for b in range(0, len(Ks), batch):
        s, t, out = decode(C, Ks[b:b + batch], lu, f_rule, mode)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:3]:
            tops[b + k] = out[k]
    return scores, skips, tops


# ---------- planted controls: 24 = each set x both F variants, families cycled ----------
ctrl_rows = []
t0 = time.time()
ctrl_plan = []
for si, (sign, mode, Ks, labs) in enumerate(SETS):
    fams_here = sorted({f for f, _ in labs})
    for f_rule in (False, True):
        for rep_i in range(3 if si < 3 else 2):
            ctrl_plan.append((si, f_rule, fams_here[(rep_i + len(ctrl_plan)) % len(fams_here)]))
for ci, (si, f_rule, fam) in enumerate(ctrl_plan):
    sign, mode, Ks, labs = SETS[si]
    o = int(rng.integers(0, len(plain) - 240)); P = plain[o:o + 240]
    cand = [i for i, (f, _) in enumerate(labs) if f == fam]
    ki = int(rng.choice(cand))
    Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N          # the key as the encipherer holds it
    C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
    nul = null_scores(C, lu, f_rule, rng, 500, mode)
    sc, sk, tops = best_configs(C, Ks, f_rule, mode)
    z = (sc - nul.mean()) / nul.std()
    rank = int((z > z[ki]).sum()) + 1
    rec = decode(C, Ks[ki:ki + 1], lu, f_rule, mode)[2][0]
    ctrl_rows.append((f"control-{ci:02d}", sign, labs[ki][0], labs[ki][1], f_rule, float(z[ki]), rank, float((rec == P).mean())))
    print(f"  control-{ci:02d}: {sign} {labs[ki][0]} '{labs[ki][1]}' F={f_rule}: z={z[ki]:.1f} rank {rank}, recovered {(rec == P).mean():.3f}", flush=True)
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
                nul_by_mode[mode] = null_scores(C, lu, f_rule, rng, 2000, mode)
            nul = nul_by_mode[mode]
            nulls[(pid, f_rule, mode)] = (float(nul.mean()), float(nul.std()), float(nul.max()))
            sc, sk, tops = best_configs(C, Ks, f_rule, mode)
            z = (sc - nul.mean()) / nul.std()
            for k in np.argsort(-z)[:3]:
                results.append((pid, sign, f_rule, labs[k][0], labs[k][1], float(z[k]), int(sk[k]), float(sc[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z on this page: {max(r[5] for r in results if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

results.sort(key=lambda r: -r[5])
zmax = results[0][5]
out = ["# Phase 4 sweep: phrase and sentence keys from the book, all key signs, under the skip-on-repeat rule", "",
       f"{len(phrase_fams)} distinct phrase/sentence keys (2-, 3- and 4-word contiguous phrases and whole lines of the solved text, forwards and reversed) under three sign conventions, "
       f"plus phase 3's {len(p3)} keystreams under the two sign conventions phase 3 did not run: {nconf} configurations per page, {len(pages)} pages, 2 F-rule variants: **{ntests:,} tests**.",
       f"Per page, variant and decoder mode, the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection. Chance maximum for this many tests: about {np.sqrt(2*np.log(ntests)):.1f}.", "",
       "## Planted controls", "", "| control | sign | family | key | F rule | z of true key | rank in its set | runes recovered |", "|---|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.1f} | {r[6]} | {r[7]:.3f} |")
out += ["", f"Controls recovered at z ≥ 6 and rank 1: {sum(1 for r in ctrl_rows if r[5] >= 6 and r[6] == 1)} of {len(ctrl_rows)}; all at z ≥ 6: {sum(1 for r in ctrl_rows if r[5] >= 6)} of {len(ctrl_rows)}.", "",
        "## Unsolved pages: top 20 configurations overall", "",
        "| page | sign | F rule | family | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.2f} | {r[6]} | {r[8]} |")
best_phrase = max((r for r in results if r[3].startswith(("phrase", "sentence"))), key=lambda r: r[5])
out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f}. Largest z among phrase/sentence keys: {best_phrase[5]:.2f} ({best_phrase[0]}, {best_phrase[1]}, {best_phrase[3]} '{best_phrase[4]}').", "",
        "## Verdict", "",
        ("**No page decrypts.** " if zmax < 6 else "**At least one page clears z = 6: inspect the transliteration above before believing it.** ") +
        "Every 2-, 3- and 4-word phrase and every full line of the solved text, forwards and reversed, as a Vigenère key under the skip-on-repeat rule, with the key added, subtracted or used Beaufort-style, with and without the F rule, is excluded at the sensitivity the controls demonstrate; so are phase 3's families under the two sign conventions phase 3 had not run. This says nothing about keys from outside the book's own text.", ""]
(RESULTS / "phase4.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "nconf": nconf, "nphrase": len(phrase_fams), "controls": ctrl_rows, "top": results[:60],
           "nulls": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in nulls.items()}}, open(RESULTS / "phase4.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
