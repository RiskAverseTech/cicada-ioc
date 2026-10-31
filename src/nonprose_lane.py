"""A model-free structure scorer over the small libraries (2026-10-31; private-table row A1, docs/blind-spots.md §1).

Registration: results/nonprose_registration.md (commit 44beb58, before any run).  Every decode lane so far scored a candidate
plaintext with a language model; a right key over a non-prose plaintext scores as noise under all of them.  This lane scores
the plain decode (every rune keyed; F rule off and on; sub, add, beaufort) of every row of the book library (families.ALLSETS,
7,621 keys, every key of period <= 64 at all its rolls) and the 3,000 prime streams with three statistics that assume no
language: U = sum of squared rune counts (the index of coincidence), W = word tokens of >= 2 runes repeated on the page,
G = rune 3-gram positions repeated on the page; each a z against N0 uniform keystreams, score z* = max of the three.
Stages (STAGE=): calib (200,000-draw null on the longest and shortest page, fixes the bar), plants (six payload classes under
library keys, the scorer's power), controls (the solved WELCOME and KOAN pages under their own keys), pages (the 55 pages, a
library-sized null per page and F; SHARD/NSHARD split the pages), merge (results/nonprose_lane.md).
The plant encryption with the F rule follows the book: a plaintext F is written unkeyed and consumes no key; a keyed rune whose
cipher comes out F is then read as F by the decoder (the book's own ambiguity, accepted).
Reproduce: STAGE=calib .venv/bin/python -I src/nonprose_lane.py, then plants, controls, pages, merge.
"""
import os, sys, re, json, time, glob
from functools import lru_cache
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, english_to_runes, to_latin, vigenere
import families as F

t0 = time.time(); STAGE = os.environ.get("STAGE", "calib"); SMOKE = os.environ.get("SMOKE") == "1"
N0 = 50 if SMOKE else 2000; NCAL = 3000 if SMOKE else 200_000; REPS = 1 if SMOKE else 10; PMAX = 64; CHUNK = 8000
SHARD = int(os.environ.get("SHARD", 0)); NSHARD = int(os.environ.get("NSHARD", 1))
SEP = set('-.&$§'); SIGNS = ("sub", "add", "beaufort")
PRIMEVAL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
OUT = RESULTS / ("nonprose_smoke" if SMOKE else "nonprose")


def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


# ---------- pages
def parse_chunk(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, np.int64), np.array(wid, np.int64)


TXT = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); CHUNKS = TXT.split("%")
PAGES = [(f"LP2-{k-16:02d}",) + parse_chunk(CHUNKS[k]) for k in range(16, 72) if any(ch in IDX for ch in CHUNKS[k])]
assert len(PAGES) == 55
LMAX = max(len(C) for _, C, _ in PAGES)


# ---------- libraries
def period(row):
    for p in range(1, PMAX + 1):
        if np.array_equal(row[p:], row[:-p]): return p
    return 0


def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)


def build_library(sign, smoke=SMOKE):
    """rows (M, LMAX) int16, labels, decoder mode.  Book keys of families.ALLSETS at every roll of their period (<= 64),
    aperiodic keys at offset 0, the 3,000 prime streams; exact duplicates removed (first label kept)."""
    a, b, mode = {"sub": (0, 3, "sub"), "add": (1, 4, "sub"), "beaufort": (2, 5, "beaufort")}[sign]
    K = np.vstack([F.ALLSETS[a][2], F.ALLSETS[b][2]])[:, :LMAX]
    labels = [f"{x} {y}" for x, y in list(F.ALLSETS[a][3]) + list(F.ALLSETS[b][3])]
    if smoke:
        keep = [i for i, l in enumerate(labels) if l.startswith("vigenere-word ") and (len(l) < 22 or "DIUINITY" in l)][:160]
        K, labels = K[keep], [labels[i] for i in keep]
    rows, labs = [], []; ar = np.arange(LMAX)
    for i in range(len(K)):
        p = period(K[i])
        if p:
            for r in range(p): rows.append(K[i][(ar + r) % p]); labs.append(f"{labels[i]} @{r}")
        else: rows.append(K[i]); labs.append(f"{labels[i]} @0")
    P = sieve(20000)
    for s in range(100 if smoke else 1000):
        seg = P[s:s + LMAX]
        for name, arr in (("p", seg), ("p-1", seg - 1), ("p+1", seg + 1)):
            k = arr % N; rows.append((-k) % N if sign == "add" else k); labs.append(f"prime {name} s={s} @0")
    R = np.array(rows, dtype=np.int16); _, idx = np.unique(R, axis=0, return_index=True); idx.sort()
    return R[idx], [labs[i] for i in idx], mode


# ---------- decoder and scorer
def kidx_of(x, f_rule):
    return np.cumsum(x != 0) - 1 if f_rule else np.arange(len(x))


def decode_rows(C, K, mode, f_rule):
    Kc = K[:, kidx_of(C, f_rule)].astype(np.int64)
    P = (C[None, :] - Kc) % N if mode == "sub" else (Kc - C[None, :]) % N
    if f_rule: P[:, C == 0] = 0
    return P


def encrypt(Pt, Krow, mode, f_rule):
    """plain encipherment; with the F rule a plaintext F is written unkeyed, and a keyed rune whose cipher comes out F is
    written as F without consuming the key symbol (the decoder reads it as a literal F; one rune lost, alignment kept)"""
    Krow = Krow.astype(np.int64)
    if not f_rule: return (Pt + Krow[:len(Pt)]) % N if mode == "sub" else (Krow[:len(Pt)] - Pt) % N
    C = np.zeros(len(Pt), np.int64); j = 0
    for i, q in enumerate(Pt):
        if q == 0: continue
        c = (q + Krow[j]) % N if mode == "sub" else (Krow[j] - q) % N
        C[i] = c
        if c != 0: j += 1
    return C


def word_slots(wid):
    starts = np.flatnonzero(np.r_[True, wid[1:] != wid[:-1]]); lens = np.diff(np.r_[starts, len(wid)])
    return starts[lens >= 2], lens[lens >= 2]


def repeated_positions(codes):
    """per row: the number of columns whose code occurs at least twice in that row"""
    s = np.sort(codes, axis=1); eq = s[:, 1:] == s[:, :-1]
    runs = eq & ~np.concatenate([np.zeros((len(s), 1), bool), eq[:, :-1]], axis=1)
    return eq.sum(1) + runs.sum(1)


def stats(P, starts, lens):
    m, L = P.shape; P = P.astype(np.int64)
    cnt = np.bincount((P + np.arange(m)[:, None] * N).ravel(), minlength=m * N).reshape(m, N)
    U = (cnt ** 2).sum(1)
    G = repeated_positions(P[:, :-2] * 841 + P[:, 1:-1] * 29 + P[:, 2:])
    h = np.zeros((m, len(starts)), np.uint64)
    for j in range(int(lens.max()) if len(lens) else 0):
        msk = lens > j
        h[:, msk] = h[:, msk] * np.uint64(31) + (P[:, starts[msk] + j].astype(np.uint64) + np.uint64(1))
    h ^= lens.astype(np.uint64) << np.uint64(56)
    W = repeated_positions(h) if len(starts) else np.zeros(m, np.int64)
    return np.stack([U, W, G], 1).astype(np.float64)


def moments(C, wid, f_rule, rng):
    """null moments from N0 uniform keystreams: (mean, sd) of U and the mean pair counts of W and G"""
    S = scored_rows(C, wid, rng.integers(0, N, size=(N0, LMAX)).astype(np.int16), "sub", f_rule, None)
    return float(S[:, 0].mean()), float(S[:, 0].std()) or 1.0, float(S[:, 1].mean() / 2), float(S[:, 2].mean() / 2)


def zify(S, mom):
    """U as a plain z; W and G as Anscombe-transformed pair counts, 2(sqrt(x/2 + 3/8) - sqrt(lambda + 3/8)), which is near
    N(0,1) for a Poisson count and conservative where the null mean is small (amendment in the registration)"""
    muU, sdU, lamW, lamG = mom
    return np.stack([(S[:, 0] - muU) / sdU, 2 * (np.sqrt(S[:, 1] / 2 + 0.375) - np.sqrt(lamW + 0.375)), 2 * (np.sqrt(S[:, 2] / 2 + 0.375) - np.sqrt(lamG + 0.375))], 1)


def scored_rows(C, wid, K, mode, f_rule, mom):
    """raw statistics (mom None) or z-scores (m, 3) of every row of K on page C, in chunks"""
    starts, lens = word_slots(wid); out = []
    for i in range(0, len(K), CHUNK):
        S = stats(decode_rows(C, K[i:i + CHUNK], mode, f_rule), starts, lens)
        out.append(S if mom is None else zify(S, mom))
    return np.concatenate(out)


def zstar(C, wid, K, mode, f_rule, mom): return scored_rows(C, wid, K, mode, f_rule, mom).max(1)


def describe(P, wid):
    """the repeated words and 3-grams of one decode, for the eye"""
    starts, lens = word_slots(wid); words = [to_latin(P[s:s + l]) for s, l in zip(starts, lens)]
    from collections import Counter
    rw = [f"{w}×{c}" for w, c in Counter(words).most_common() if c >= 2][:8]
    g = Counter(to_latin(P[i:i + 3]) for i in range(len(P) - 2)); rg = [f"{w}×{c}" for w, c in g.most_common() if c >= 2][:8]
    return {"words": rw, "trigrams": rg, "text": to_latin(P)[:120]}


# ---------- the book's F convention (amendment 2 in the registration)
def add_counts(cnt, S):
    m = len(S); cnt += np.bincount((S + np.arange(m)[:, None] * N).ravel(), minlength=m * N).reshape(m, N)


def loglik(cnt, S):
    """log-likelihood of each row's segment S under that row's own prefix counts (KT estimator, counts hold the prior)"""
    return np.log(np.take_along_axis(cnt, S, 1)).sum(1) - S.shape[1] * np.log(cnt.sum(1))


def decode_x(C, K, mode, prior=0.5):
    """Convention X, the book's: a plaintext F is written as F and consumes no key symbol, and a keyed rune may encipher
    to F.  At every cipher F the decoder branches (literal F, key not consumed | keyed rune) and keeps, per row, the branch
    whose segment up to the next F is likelier under the adaptive unigram of that row's own decoded prefix; greedy, no beam,
    no language model.  Returns the decodes (m, L)."""
    m, L = len(K), len(C); C = C.astype(np.int64); K = K.astype(np.int64)
    P = np.zeros((m, L), np.int64); cnt = np.full((m, N), prior); lit = np.zeros(m, np.int64)
    fpos = np.flatnonzero(C == 0); bounds = list(fpos) + [L]

    def seg(i0, i1, litv):
        idx = np.arange(i0, i1)[None, :] - litv[:, None]; Kc = np.take_along_axis(K, idx, 1)
        return (C[i0:i1][None, :] - Kc) % N if mode == "sub" else (Kc - C[i0:i1][None, :]) % N
    if bounds[0] > 0:
        S = seg(0, bounds[0], lit); P[:, :bounds[0]] = S; add_counts(cnt, S)
    for k, f in enumerate(fpos):
        i1 = bounds[k + 1]
        PA = np.concatenate([np.zeros((m, 1), np.int64), seg(f + 1, i1, lit + 1)], 1); PB = seg(f, i1, lit)
        a = loglik(cnt, PA) >= loglik(cnt, PB); S = np.where(a[:, None], PA, PB)
        P[:, f:i1] = S; add_counts(cnt, S); lit += a
    return P


def encrypt_x(Pt, Krow, mode):
    C = np.zeros(len(Pt), np.int64); j = 0; Krow = Krow.astype(np.int64)
    for i, q in enumerate(Pt):
        if q == 0: continue
        C[i] = (q + Krow[j]) % N if mode == "sub" else (Krow[j] - q) % N; j += 1
    return C


def scored_rows_x(C, wid, K, mode, mom):
    starts, lens = word_slots(wid); out = []
    for i in range(0, len(K), CHUNK):
        S = stats(decode_x(C, K[i:i + CHUNK], mode), starts, lens); out.append(S if mom is None else zify(S, mom))
    return np.concatenate(out)


def moments_x(C, wid, rng):
    S = scored_rows_x(C, wid, rng.integers(0, N, size=(N0, LMAX)).astype(np.int16), "sub", None)
    return float(S[:, 0].mean()), float(S[:, 0].std()) or 1.0, float(S[:, 1].mean() / 2), float(S[:, 2].mean() / 2)


def zstar_x(C, wid, K, mode, mom): return scored_rows_x(C, wid, K, mode, mom).max(1)


def stage_xrule():
    rng = np.random.default_rng(505); B = bar(); libs = {s: build_library(s) for s in SIGNS}; M = max(len(libs[s][0]) for s in SIGNS); res = {"bar": B}
    # controls: the WELCOME page, chunks 2 (key restarts) and 3 (the key continues from chunk 2)
    K, labels, mode = libs["sub"]; ki = [i for i, l in enumerate(labels) if l == "vigenere-word DIUINITY @0"][0]
    rolls = [i for i, l in enumerate(labels) if l.startswith("vigenere-word DIUINITY @")]; ctl = []
    pt = np.array([s["plaintext"] for s in json.loads((RAW.parent / "processed" / "pages.json").read_text())["solved"] if s["name"] == "welcome+wisdom"][0])
    off = 0
    for ch in (2, 3):
        C, wid = parse_chunk(CHUNKS[ch]); mom = moments_x(C, wid, rng); z = zstar_x(C, wid, K, mode, mom); best = rolls[int(np.argmax(z[rolls]))]
        P = decode_x(C, K[best:best + 1], mode)[0]; acc = float((P == pt[off:off + len(C)]).mean()); off += len(C)
        ctl.append({"chunk": ch, "L": int(len(C)), "nF": int((C == 0).sum()), "z_roll0": float(z[ki]), "rank_roll0": int((z > z[ki]).sum()) + 1, "best_roll": labels[best], "z_best": float(z[best]),
                    "rank_best": int((z > z[best]).sum()) + 1, "acc_best": acc, "top": labels[int(np.argmax(z))], "ztop": float(z.max())})
        log("control", ctl[-1])
    res["controls"] = ctl
    # plants under convention X
    rows = []
    for cls in ("P1", "P4"):
        for sign in SIGNS:
            K, labels, mode = libs[sign]; cand = plant_rows(labels)
            for rep in range(REPS):
                pid, Cref, wref = PAGES[rng.integers(55)]; Pt, wid = payload(cls, rng, len(Cref), wref); kj = cand[rng.integers(len(cand))]
                C = encrypt_x(Pt, K[kj], mode); mom = moments_x(C, wid, rng); z = zstar_x(C, wid, K, mode, mom); rank = int((z > z[kj]).sum()) + 1
                acc = float((decode_x(C, K[kj:kj + 1], mode)[0] == Pt).mean())
                rows.append({"cls": cls, "sign": sign, "rep": rep, "L": int(len(C)), "nF": int((C == 0).sum()), "key": labels[kj], "z": float(z[kj]), "rank": rank, "acc": acc,
                             "top": labels[int(np.argmax(z))], "ztop": float(z.max()), "rec": bool(z[kj] >= B and rank == 1)})
                log(cls, sign, rep, labels[kj], "z*", round(float(z[kj]), 2), "rank", rank, "acc", round(acc, 3))
    res["plants"] = rows
    # the pages
    cells = []
    for pid, C, wid in PAGES:
        mom = moments_x(C, wid, rng)
        zn = np.concatenate([zstar_x(C, wid, rng.integers(0, N, size=(min(20000, M - i), LMAX)).astype(np.int16), "sub", mom) for i in range(0, M, 20000)])
        for sign in SIGNS:
            K, labels, mode = libs[sign]; z = zstar_x(C, wid, K, mode, mom); top = int(np.argmax(z))
            P = decode_x(C, K[top:top + 1], mode)[0]; Z = scored_rows_x(C, wid, K[top:top + 1], mode, mom)[0]
            listed = bool(z[top] > zn.max()); hit = bool(z[top] >= B and z[top] >= zn.max() + 1.0)
            cells.append({"page": pid, "L": int(len(C)), "sign": sign, "M": int(len(K)), "top": labels[top], "ztop": float(z[top]), "zUWG": Z.tolist(), "null_max": float(zn.max()),
                          "null_tails": tails(zn), "lib_tails": tails(z), "listed": listed, "hit": hit, "desc": describe(P, wid) if listed else None})
            log(pid, "X", sign, "top", labels[top], round(float(z[top]), 2), "null max", round(float(zn.max()), 2), "listed" if listed else "", "HIT" if hit else "")
    res["cells"] = cells; dump("xrule", res)


# ---------- payloads
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_words(n):
    if n < 20: return [ONES[n]]
    if n < 100: return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000: return [ONES[n // 100], "hundred"] + (number_words(n % 100) if n % 100 else [])
    return number_words(n // 1000) + ["thousand"] + (number_words(n % 1000) if n % 1000 else [])


@lru_cache(None)
def gematria_numeral(n):
    """n as a tuple of rune indices whose prime values sum to n, largest value first; None if impossible (n = 1)"""
    if n == 0: return ()
    for r in range(N - 1, -1, -1):
        v = PRIMEVAL[r]
        if v <= n and n - v != 1:
            rest = gematria_numeral(n - v)
            if rest is not None: return (r,) + rest
    return None


_TEXT = {}
def text_words(path):
    if path not in _TEXT:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")
        _TEXT[path] = [w for w in re.findall(r"[A-Za-z']+", raw) if len(english_to_runes(w)) >= 1]
    return _TEXT[path]


ENGLISH = sorted(glob.glob(str(RAW.parent / "corpus" / "raw" / "*_pg*.txt")))
LATIN = str(RAW / "corpora" / "latin_corpus.txt")
PRIMES = sieve(200000)


def payload(cls, rng, Ltarget, wid_ref):
    """(plaintext runes, word ids) of about Ltarget runes"""
    if cls == "P0":
        return rng.integers(0, N, size=Ltarget), wid_ref.copy()
    if cls == "P1":
        ws = text_words(ENGLISH[rng.integers(len(ENGLISH))]); s = rng.integers(0, len(ws) - 400); gen = (english_to_runes(w) for w in ws[s:])
    elif cls == "P2":
        ws = text_words(LATIN); s = rng.integers(0, len(ws) - 400); gen = (english_to_runes(w) for w in ws[s:])
    elif cls == "P3":
        s = rng.integers(0, 2000); gen = (english_to_runes(w) for p in PRIMES[s:] for w in number_words(int(p)))
    elif cls == "P4":
        s = rng.integers(0, 2000); gen = ([int(d) for d in str(int(p))] for p in PRIMES[s:])
    elif cls == "P5":
        s = rng.integers(2, 3301); gen = (list(gematria_numeral(n)) for n in range(s, s + 10000))
    runes, wid = [], []; w = 0
    for word in gen:
        if not word: continue
        runes += list(word); wid += [w] * len(word); w += 1
        if len(runes) >= Ltarget: break
    return np.array(runes[:Ltarget], np.int64), np.array(wid[:Ltarget], np.int64)


# ---------- stages
def dump(name, obj): (RESULTS / f"{OUT.name}_{name}.json").write_text(json.dumps(obj, indent=1)); log("wrote", name)


def tails(z): return {str(t): int((z >= t).sum()) for t in (4, 5, 6, 7)}


def stage_calib():
    rng = np.random.default_rng(101); res = {"NCAL": NCAL, "N0": N0, "cells": []}
    lens = [len(C) for _, C, _ in PAGES]; picks = [int(np.argmax(lens)), int(np.argmin(lens))]
    for pi in picks:
        pid, C, wid = PAGES[pi]
        for f_rule in (False, True):
            mom = moments(C, wid, f_rule, rng); zs = []
            for i in range(0, NCAL, 20000):
                zs.append(zstar(C, wid, rng.integers(0, N, size=(min(20000, NCAL - i), LMAX)).astype(np.int16), "sub", f_rule, mom))
            z = np.concatenate(zs); Z = scored_rows(C, wid, rng.integers(0, N, size=(20000, LMAX)).astype(np.int16), "sub", f_rule, mom)
            res["cells"].append({"page": pid, "L": len(C), "F": f_rule, "max": float(z.max()), "tails": tails(z), "per_stat_max_20k": Z.max(0).tolist(),
                                 "corr_20k": np.corrcoef(Z.T).round(3).tolist()})
            log(pid, "F", f_rule, "max z*", round(float(z.max()), 2), tails(z))
    cal = max(c["max"] for c in res["cells"]); res["bar"] = float(np.ceil(max(7.0, cal + 1.0) * 2) / 2)
    log("bar", res["bar"]); dump("calib", res)


def bar():
    return json.loads((RESULTS / f"{OUT.name}_calib.json").read_text())["bar"]


def plant_rows(labels):
    return [i for i, l in enumerate(labels) if l.startswith("vigenere-word ") or l.startswith("prime ")]


def stage_plants():
    rng = np.random.default_rng(202); B = bar(); libs = {s: build_library(s) for s in SIGNS}; log("libraries", {s: len(libs[s][0]) for s in SIGNS})
    rows = []
    for cls in ("P0", "P1", "P2", "P3", "P4", "P5"):
        for sign in SIGNS:
            for f_rule in ((False, True) if cls == "P1" else (False,)):
                K, labels, mode = libs[sign]; cand = plant_rows(labels)
                for rep in range(REPS):
                    pid, Cref, wref = PAGES[rng.integers(55)]; Pt, wid = payload(cls, rng, len(Cref), wref)
                    ki = cand[rng.integers(len(cand))]; C = encrypt(Pt, K[ki], mode, f_rule)
                    mom = moments(C, wid, f_rule, rng); z = zstar(C, wid, K, mode, f_rule, mom)
                    rank = int((z > z[ki]).sum()) + 1
                    rows.append({"cls": cls, "sign": sign, "F": f_rule, "rep": rep, "L": int(len(C)), "key": labels[ki], "z": float(z[ki]), "rank": rank,
                                 "top": labels[int(np.argmax(z))], "ztop": float(z.max()), "rec": bool(z[ki] >= B and rank == 1)})
                    log(cls, sign, f_rule, rep, labels[ki], "z*", round(float(z[ki]), 2), "rank", rank)
    dump("plants", {"bar": B, "rows": rows})


def solved_controls():
    """(name, chunk, C, wid, key runes): the solved pages whose keys are in the library, found by decrypting and matching"""
    d = json.loads((RAW.parent / "processed" / "pages.json").read_text()); plain = {s["name"]: s["plaintext"] for s in d["solved"]}
    keys = {"DIVINITY": english_to_runes("divinity"), "FIRFUMFERENFE": [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]}; out = []
    for k in range(1, 16):
        C, wid = parse_chunk(CHUNKS[k])
        if len(C) == 0: continue
        for kname, key in keys.items():
            P = vigenere(C.tolist(), key, skip_f=True); s = "".join(map(str, P[:40]))
            for name, pt in plain.items():
                if s in "".join(map(str, pt)): out.append((name, k, C, wid, kname, key)); break
    return out


def stage_controls():
    rng = np.random.default_rng(303); B = bar(); K, labels, mode = build_library("sub"); rows = []
    for name, k, C, wid, kname, key in solved_controls():
        ki = int(np.flatnonzero((K == np.resize(key, LMAX).astype(np.int16)).all(1))[0])
        mom = moments(C, wid, True, rng); z = zstar(C, wid, K, mode, True, mom); rank = int((z > z[ki]).sum()) + 1
        Z = scored_rows(C, wid, K[ki:ki + 1], mode, True, mom)[0]
        rows.append({"page": name, "chunk": k, "L": int(len(C)), "key": kname, "row": labels[ki], "z": float(z[ki]), "zUWG": Z.tolist(), "rank": rank,
                     "hit": bool(z[ki] >= B and rank == 1), "top": labels[int(np.argmax(z))], "ztop": float(z.max())})
        log(name, k, kname, "z*", round(float(z[ki]), 2), "rank", rank)
    dump("controls", {"bar": B, "rows": rows})


def stage_pages():
    rng = np.random.default_rng(404 + SHARD); B = bar(); libs = {s: build_library(s) for s in SIGNS}; M = max(len(libs[s][0]) for s in SIGNS)
    log("libraries", {s: len(libs[s][0]) for s in SIGNS}); cells = []
    for pi in range(SHARD, 55, NSHARD):
        pid, C, wid = PAGES[pi]
        for f_rule in (False, True):
            mom = moments(C, wid, f_rule, rng)
            zn = np.concatenate([zstar(C, wid, rng.integers(0, N, size=(min(20000, M - i), LMAX)).astype(np.int16), "sub", f_rule, mom) for i in range(0, M, 20000)])
            for sign in SIGNS:
                K, labels, mode = libs[sign]; z = zstar(C, wid, K, mode, f_rule, mom); top = int(np.argmax(z))
                P = decode_rows(C, K[top:top + 1], mode, f_rule)[0]; Z = scored_rows(C, wid, K[top:top + 1], mode, f_rule, mom)[0]
                listed = bool(z[top] > zn.max()); hit = bool(z[top] >= B and z[top] >= zn.max() + 1.0)
                cells.append({"page": pid, "L": int(len(C)), "F": f_rule, "sign": sign, "M": int(len(K)), "top": labels[top], "ztop": float(z[top]), "zUWG": Z.tolist(),
                              "null_max": float(zn.max()), "null_tails": tails(zn), "lib_tails": tails(z), "listed": listed, "hit": hit,
                              "desc": describe(P, wid) if listed else None})
                log(pid, "F", f_rule, sign, "top", labels[top], round(float(z[top]), 2), "null max", round(float(zn.max()), 2), "listed" if listed else "", "HIT" if hit else "")
    dump(f"pages_{SHARD}", {"bar": B, "cells": cells})


def stage_merge():
    cal = json.loads((RESULTS / f"{OUT.name}_calib.json").read_text()); B = cal["bar"]
    pl = json.loads((RESULTS / f"{OUT.name}_plants.json").read_text())["rows"]; ct = json.loads((RESULTS / f"{OUT.name}_controls.json").read_text())["rows"]
    cells = sum((json.loads(p.read_text())["cells"] for p in sorted(RESULTS.glob(f"{OUT.name}_pages_*.json"))), [])
    o = ["# A model-free structure scorer over the small libraries (row A1, blind spot 1)", "",
         f"Registration: `results/nonprose_registration.md`. Scorer z\\* = max of the z of U (Σ counts²), W (repeated words of ≥ 2 runes) and G (repeated rune 3-grams) against N0 = {cal['N0']:,} uniform keystreams; plain decoder, three signs, F rule off and on; library rows per sign {sorted(set(c['M'] for c in cells))} (book keys at every roll of their period ≤ 64, plus 3,000 prime streams).", "",
         f"## Calibration null ({cal['NCAL']:,} draws per cell, before any library row was read)", "", "| page | runes | F | max z\\* | ≥ 4 | ≥ 5 | ≥ 6 | ≥ 7 | per-statistic max (U, W, G; 20,000 draws) |", "|---|---|---|---|---|---|---|---|---|"]
    for c in cal["cells"]: o.append(f"| {c['page']} | {c['L']} | {'on' if c['F'] else 'off'} | {c['max']:.2f} | " + " | ".join(str(c['tails'][t]) for t in '4567') + f" | {', '.join(f'{v:.1f}' for v in c['per_stat_max_20k'])} |")
    o += ["", f"**Bar** = max(7.0, calibration max + 1.0) rounded up to 0.5 = **{B}**.", "", "## Plants (power)", "", f"| class | sign | F | recovered (z\\* ≥ {B}, rank 1) | median z\\* | median rank |", "|---|---|---|---|---|---|"]
    for cls in ("P0", "P1", "P2", "P3", "P4", "P5"):
        for sign in SIGNS:
            for f in (False, True):
                rr = [r for r in pl if r["cls"] == cls and r["sign"] == sign and r["F"] == f]
                if rr: o.append(f"| {cls} | {sign} | {'on' if f else 'off'} | {np.mean([r['rec'] for r in rr]):.2f} | {np.median([r['z'] for r in rr]):.1f} | {np.median([r['rank'] for r in rr]):.0f} |")
    o += ["", "## Positive controls (solved pages under their own keys, F rule on, sub library)", "", "| page | chunk | runes | key | z\\* (U, W, G) | rank | hit |", "|---|---|---|---|---|---|---|"]
    for r in ct: o.append(f"| {r['page']} | {r['chunk']} | {r['L']} | {r['key']} | {r['z']:.1f} ({', '.join(f'{v:.1f}' for v in r['zUWG'])}) | {r['rank']} | {'yes' if r['hit'] else 'no'} |")
    hits = [c for c in cells if c["hit"]]; listed = [c for c in cells if c["listed"]]
    lt = {t: sum(c["lib_tails"][t] for c in cells) for t in "4567"}; nt = {t: sum(c["null_tails"][t] for c in cells if c["sign"] == "sub") * 3 for t in "4567"}
    o += ["", "## The 55 pages", "", f"{len(cells)} cells (page × F × sign). **Hits: {len(hits)}.** Listed (library top above the library-sized null's max): {len(listed)} of {len(cells)}.", "",
          "| threshold | library rows ≥ (all cells) | library-sized null draws ≥ (same count of draws) |", "|---|---|---|"]
    for t in "4567": o.append(f"| z\\* ≥ {t} | {lt[t]:,} | {nt[t]:,} |")
    o += ["", "Top cells by z\\*:", "", "| page | F | sign | top row | z\\* (U, W, G) | null max | repeated words | repeated 3-grams |", "|---|---|---|---|---|---|---|---|"]
    for c in sorted(cells, key=lambda c: -c["ztop"])[:15]:
        d = c["desc"] or {"words": [], "trigrams": []}
        o.append(f"| {c['page']} | {'on' if c['F'] else 'off'} | {c['sign']} | {c['top']} | {c['ztop']:.2f} ({', '.join(f'{v:.1f}' for v in c['zUWG'])}) | {c['null_max']:.2f} | {' '.join(d['words']) or '—'} | {' '.join(d['trigrams']) or '—'} |")
    o += ["", "## Registered predictions", ""]
    n1 = {cls: np.mean([r["rec"] for r in pl if r["cls"] == cls and not r["F"]]) for cls in ("P0", "P1", "P2", "P3", "P4", "P5")}
    o.append(f"- N1 (power): recovered at F off " + ", ".join(f"{k} {v:.2f}" for k, v in n1.items()) + f" → {'holds' if all(v >= 0.9 for k, v in n1.items() if k != 'P0') and n1['P0'] == 0 else 'fails'}.")
    o.append(f"- N2 (solved pages): {sum(r['hit'] for r in ct)} of {len(ct)} control pages are hits at rank 1 → {'holds' if ct and all(r['hit'] for r in ct) else 'fails'}.")
    o.append(f"- N3 (the pages): hits {len(hits)}; listed cells {len(listed)} of {len(cells)} (all-null expectation {len(cells)//2} ± {np.sqrt(len(cells)/4):.0f}) → {'holds' if not hits else 'fails'}.")
    ratio = lt["5"] / max(nt["5"], 1)
    o.append(f"- N4 (tail): rows at z\\* ≥ 5, library {lt['5']:,} against null {nt['5']:,} (ratio {ratio:.2f}) → {'holds' if 0.5 <= ratio <= 2 else 'fails'}.")
    xp = RESULTS / f"{OUT.name}_xrule.json"
    if xp.exists():
        X = json.loads(xp.read_text()); xc = X["cells"]; xh = [c for c in xc if c["hit"]]; xl = [c for c in xc if c["listed"]]
        o += ["", "## The book's ᚠ convention (amendment 2): greedy branch decoder, no language model", "",
              "The WELCOME page under DIVINITY (sub library): chunk 2, where the key starts with the page, and chunk 3, where it continues from chunk 2 (so roll 0 is not expected there).", "",
              "| chunk | runes | cipher ᚠ | z\* roll 0 | rank roll 0 | best roll | z\* | rank | rune accuracy | library top | z\* |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for c in X["controls"]: o.append(f"| {c['chunk']} | {c['L']} | {c['nF']} | {c['z_roll0']:.1f} | {c['rank_roll0']} | {c['best_roll']} | {c['z_best']:.1f} | {c['rank_best']} | {c['acc_best']:.2f} | {c['top']} | {c['ztop']:.1f} |")
        o += ["", "| class | sign | recovered | median z\* | median rank | median rune accuracy |", "|---|---|---|---|---|---|"]
        for cls in ("P1", "P4"):
            for sign in SIGNS:
                rr = [r for r in X["plants"] if r["cls"] == cls and r["sign"] == sign]
                o.append(f"| {cls} | {sign} | {np.mean([r['rec'] for r in rr]):.2f} | {np.median([r['z'] for r in rr]):.1f} | {np.median([r['rank'] for r in rr]):.0f} | {np.median([r['acc'] for r in rr]):.2f} |")
        xlt = {t: sum(c["lib_tails"][t] for c in xc) for t in "4567"}; xnt = {t: sum(c["null_tails"][t] for c in xc if c["sign"] == "sub") * 3 for t in "4567"}
        o += ["", f"The 55 pages, {len(xc)} cells (page × sign). **Hits: {len(xh)}.** Listed: {len(xl)} of {len(xc)}. Rows at z\* ≥ 5: library {xlt['5']:,}, null {xnt['5']:,}; at ≥ 6: {xlt['6']:,} and {xnt['6']:,}; at ≥ 7: {xlt['7']:,} and {xnt['7']:,}.", "",
              "| page | sign | top row | z\* (U, W, G) | null max | repeated words | repeated 3-grams |", "|---|---|---|---|---|---|---|"]
        for c in sorted(xc, key=lambda c: -c["ztop"])[:10]:
            d = c["desc"] or {"words": [], "trigrams": []}
            o.append(f"| {c['page']} | {c['sign']} | {c['top']} | {c['ztop']:.2f} ({', '.join(f'{v:.1f}' for v in c['zUWG'])}) | {c['null_max']:.2f} | {' '.join(d['words']) or '—'} | {' '.join(d['trigrams']) or '—'} |")
        n1x = {cls: np.mean([r["rec"] for r in X["plants"] if r["cls"] == cls]) for cls in ("P1", "P4")}; c2 = X["controls"][0]
        o += ["", f"- N1′ (power under the book's convention): P1 {n1x['P1']:.2f}, P4 {n1x['P4']:.2f} → {'holds' if all(v >= 0.9 for v in n1x.values()) else 'fails'}.",
              f"- N2′ (WELCOME chunk 2 at roll 0): z\* {c2['z_roll0']:.1f}, rank {c2['rank_roll0']} → {'holds' if c2['z_roll0'] >= B and c2['rank_roll0'] == 1 else 'fails'}.",
              f"- N3′ (the pages): hits {len(xh)}; listed {len(xl)} of {len(xc)} → {'holds' if not xh else 'fails'}."]
    o += ["", "Reading: written after the run, below. [stated — the tables]", "", f"Reproduce: `STAGE=calib|plants|controls|pages|merge .venv/bin/python -I src/nonprose_lane.py`.", ""]
    (RESULTS / f"{OUT.name}_lane.md").write_text("\n".join(o)); print("\n".join(o))


if __name__ == "__main__":
    {"calib": stage_calib, "plants": stage_plants, "controls": stage_controls, "pages": stage_pages, "xrule": stage_xrule, "merge": stage_merge}[STAGE]()
