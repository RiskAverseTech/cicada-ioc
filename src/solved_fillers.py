"""Fillers planted on the solved pages under their own keys (2026-10-30; private table row C6).

Question, stated before running: the §59 filler form (one extra rune at a uniform slot in 40 % of words of two or more
runes) fitted the unsolved pages' word lengths.  What does it do to the book's own plaintext under the book's own keys?
The solved pages' English (the rtkd translation, pages 0.1 WELCOME... and 0.2 A KOAN..., in rune spelling) is cut into
page-length pieces at word boundaries and enciphered with DIVINITY and FIRFUMFERENFE under this repository's convention
(C = P + K, every rune keyed; the book's own literal-F quirk, a plaintext F written unkeyed, is not reproduced because a
cipher F is then ambiguous and the decoders here model it only as all-or-none), with and without fillers planted into the
words (the key is not consumed by a filler), and then decoded with the plain, free-null (−2.2) and word-constrained (−2.2)
decoders over the phase-3 Vigenère-word family with the true key added; 20 replicates each, plus the no-filler page.
Reported: rank of the true key, z over 400 random keystreams, rune accuracy on real positions, fillers placed by the
decoder against fillers planted, and the share of planted filler words found.  Expected, from §60/§61: the plain decoder
loses the key on most replicates and the two filler decoders keep it with a filler count near the planted one.
Rep 0 is the piece enciphered without fillers.  Output: results/solved_fillers.md.  Reproduce: .venv/bin/python -I src/solved_fillers.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, english_to_runes
from score import decode, translit, S_MAX
from wc_decode import decode_wc, word_starts
import families as F

t0 = time.time(); rng = np.random.default_rng(66); REPS, NULLK, P_WORD = 20, 400, 0.40
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')


def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)


import re
TR = (RAW / "iddqd__liber-primus__translation.txt").read_text(errors="ignore")
def words_of(pg):
    lines = re.findall(rf"^{re.escape(pg)}\.\d+\.\d+\s+(.*)$", TR, flags=re.M)
    return [np.array(english_to_runes(w)) for l in lines for w in re.findall(r"[A-Za-z]+", l)]
def pieces(words, n=262):
    out, cur, tot = [], [], 0
    for w in words:
        if tot + len(w) > n and cur: out.append(cur); cur, tot = [], 0
        cur.append(w); tot += len(w)
    if cur: out.append(cur)
    return out
PAGES = []
for pg, kname, K in (("0.1", "DIVINITY", np.array(english_to_runes("divinity"))), ("0.2", "FIRFUMFERENFE", np.array([0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]))):
    for k, ws in enumerate(pieces(words_of(pg))[:2]):
        PAGES.append((f"translation {pg} piece {k+1} ({kname})", np.concatenate(ws), np.concatenate([np.full(len(w), i) for i, w in enumerate(ws)]), K, False))
_, _, Kp3, Lp3 = F.ALLSETS[3]; VW = [i for i, (f, _) in enumerate(Lp3) if f == "vigenere-word"]; Kfam0 = Kp3[VW]


def decrypt(C, K, f_rule):
    P = []; j = 0
    for c in C:
        if f_rule and c == 0: P.append(0); continue
        P.append((c - K[j % len(K)]) % N); j += 1
    return np.array(P)


def encrypt_with_fillers(P, wid, K, f_rule, p):
    """§59 form on the plaintext words; key consumed by real runes only (literal F consumes none when f_rule)."""
    C, W, real = [], [], []; j = 0; prev = None
    def emit(c, w, r):
        nonlocal prev
        C.append(int(c)); W.append(w); real.append(r); prev = int(c)
    for w in range(wid.max() + 1):
        word = P[wid == w]; slot = int(rng.integers(0, len(word) + 1)) if (len(word) >= 2 and rng.random() < p) else -1
        for i, q in enumerate(word):
            if i == slot: f = int(rng.integers(0, N - 1)); emit(f if (prev is None or f < prev) else f + 1, w, False)
            if f_rule and q == 0: emit(0, w, True)
            else: emit((q + K[j % len(K)]) % N, w, True); j += 1
        if slot == len(word): f = int(rng.integers(0, N - 1)); emit(f if (prev is None or f < prev) else f + 1, w, False)
    return np.array(C), np.array(W), np.array(real)


rows = []
for name, P0, wid0, K, f_rule in PAGES:
    Kfull = np.resize(K, Kfam0.shape[1]); Kfam = np.vstack([Kfull[None, :], Kfam0]); pos = 0
    for rep in range(REPS + 1):
        C, W, real = encrypt_with_fillers(P0, wid0, K, f_rule, P_WORD if rep else 0.0)
        ws = word_starts(W); nm = np.ones(len(C), bool); nm[0] = False
        for dec in ("plain", "free-null", "wc"):
            Kr = rng.integers(0, N, size=(NULLK, len(C) + S_MAX + 2))
            if dec == "plain": run = lambda Ks: decode(C, Ks, F.lu, f_rule, "sub")[:3]
            elif dec == "free-null": run = lambda Ks: decode(C, Ks, F.lu, f_rule, "sub", None, nm, -2.2)[:3]
            else: run = lambda Ks: decode_wc(C, Ks, F.lu, ws, f_rule, "sub", -2.2)[:3]
            nul = run(Kr)[0]; s, _, d = run(Kfam); z = (s - nul.mean()) / nul.std()
            acc = float((d[pos][real] == P0).mean()) if len(d[pos][real]) == len(P0) else float("nan")
            if dec != "wc": nulls = -1; found = float("nan")                 # score.decode does not return null positions; only the word-constrained decoder's are counted
            else:
                nl = decode_wc(C, Kfam[:1], F.lu, ws, f_rule, "sub", -2.2)[3][0]
                nulls = int(nl.sum()); planted = {w for w in set(W) if (~real[W == w]).any()}; got = {w for w in set(W) if nl[W == w].any()}
                found = len(planted & got) / len(planted) if planted else float("nan")
            rows.append(dict(page=name, rep=rep, dec=dec, n=len(C), fillers=int((~real).sum()), z=float(z[pos]), rank=int((z > z[pos]).sum()) + 1, acc=acc, nulls=nulls, found=found))
    print(f"{name}: {len(P0)} runes, {wid0.max()+1} words; done [{time.time()-t0:.0f}s]", flush=True)

out = ["# Fillers planted on the solved pages under their own keys (row C6)", "",
       f"The solved pages' English (rtkd translation, pages 0.1 and 0.2) in rune spelling, cut into page-length pieces and enciphered with DIVINITY and FIRFUMFERENFE (C = P + K, every rune keyed) after planting the §59 filler form (one extra rune in {P_WORD:.0%} of words of ≥ 2 runes, uniform slot, key not consumed), {REPS} replicates each; decoders over the phase-3 Vigenère-word family ({len(VW)} keys) plus the true key; z over {NULLK} random keystreams. Rep 0 is the piece without fillers.", "",
       "| page | decoder | no fillers: z / rank / acc | with fillers: recovered (z ≥ 6, rank 1) | median z | median acc on real runes | fillers planted → placed by the word-constrained decoder (median) | planted filler words found (wc) |", "|---|---|---|---|---|---|---|---|"]
for name, *_ in PAGES:
    for dec in ("plain", "free-null", "wc"):
        r0 = [r for r in rows if r["page"] == name and r["dec"] == dec and r["rep"] == 0][0]; rr = [r for r in rows if r["page"] == name and r["dec"] == dec and r["rep"] > 0]
        rec = np.mean([r["z"] >= 6 and r["rank"] == 1 for r in rr]); fnd = np.nanmedian([r["found"] for r in rr]) if dec != "plain" else float("nan")
        placed = "—" if dec != "wc" else f"{np.median([r['nulls'] for r in rr]):.0f}"; fw = "—" if dec != "wc" else f"{fnd:.2f}"
        out.append(f"| {name} | {dec} | {r0['z']:.1f} / {r0['rank']} / {r0['acc']:.2f} | {rec:.2f} | {np.median([r['z'] for r in rr]):.1f} | {np.median([r['acc'] for r in rr]):.2f} | {np.median([r['fillers'] for r in rr]):.0f} → {placed} | {fw} |")
out += ["", "Reading: written after the run, below. [stated — the table]", "", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/solved_fillers.py`.", ""]
(RESULTS / "solved_fillers.md").write_text("\n".join(out)); print("\n".join(out))
