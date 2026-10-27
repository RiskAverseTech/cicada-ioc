"""External running-key lane (2026-10-27): the texts Cicada demonstrably pointed at, used as running
keys under the anti-repeat skip rule, scored EXACTLY at every offset with the §9 Viterbi decoder.

Why this lane exists after wazar's ~200-text skip-aware sweep and jens-wedin's eight texts: both
labs scanned offsets through a coarse prefilter (recall 7/8 per page) and the sign pair c±k; neither
documents the Beaufort convention, both F-rule variants and a reversed key text for every text, and
neither reports detection power by page length.  This lane closes those gaps on the short, high-prior
texts, and runs the long texts at sentence-start offsets only.  Expected result: null.

PRE-REGISTERED RULE (written before any page was scored).  About 1e8 tests, so the chance maximum of
z over the per-page random-keystream null is about 6.1; a cell (page x text x direction x variant x
sign x F x offset) is a candidate only if ALL of
  (1) z_uni >= 7 over the page's own null (2,000 random keystreams, same F variant and decoder mode);
  (2) z_big >= 3 (bigram LLR of the decode against the random keystreams' decodes, as §24);
  (3) it reads as English to a human.  Candidates meeting (1)-(2) are printed in full.
Offsets within +-3 of each other in the same text and direction are one hypothesis (the stream, not
the exact start); the best is reported.  Controls: solved-page English enciphered under the soft rule
(re-draw 0.81) with a corpus text at a random offset, signs, F variants and directions cycled; a
control passes if the planted stream is the top hypothesis for its text and cell with z_uni >= 7 and
z_big >= 3, and the recovered offset is within +-3 of the planted one.  Detection power by page
length follows §23 (the correct key's z grows with length; pages under about 92 runes are
inconclusive at any rule this strict).

Scope.  EXACT (every offset, both directions, V1; V2 forward only for texts up to V2LIMIT runes, 3 signs
x 2 F): texts up to LIMIT runes.  SENTENCE (sentence-start offsets only, V1, both directions, 3 signs x 2 F): the longer
texts.  Key library: data/corpus/corpus.json (src/corpus.py).
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/runkey_lane.py   -> results/runkey_shard{k}.json
       MERGE=1 ... -> results/runkey.md, results/runkey.json ; SMOKE=1 for a quick check.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F

SMOKE = os.environ.get("SMOKE") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
MERGE = os.environ.get("MERGE") == "1"
rng = np.random.default_rng(3301 + SHARD)
lu, lb, plain = F.lu, F.lb, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
LIMIT = 60_000
V2LIMIT = 25_000
Z_UNI, Z_BIG, NREPS, SOFT = 7.0, 3.0, (200 if SMOKE else 2000), 0.81
LOGU = np.log(1 / N)
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))   # (sign, decoder mode)
corpus = json.loads((Path(__file__).resolve().parent.parent / "data" / "corpus" / "corpus.json").read_text())
EXACT = {k: v for k, v in corpus.items() if len(v["runes"]) <= LIMIT}
SENT = {k: v for k, v in corpus.items() if len(v["runes"]) > LIMIT}
if SMOKE:
    pages = pages[:1]; EXACT = dict(list(EXACT.items())[:1]); SENT = dict(list(SENT.items())[:1])


def bigram_many(P):
    P = np.asarray(P); return (lu[P[:, 0]] - LOGU) + (lb[P[:, :-1], P[:, 1:]] - LOGU).sum(1)


def null_for(C, f_rule, mode):
    Ks = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2))
    sc, _, dec = decode(C, Ks, lu, f_rule, mode)
    bg = bigram_many(dec); return (float(sc.mean()), float(sc.std()), float(bg.mean()), float(bg.std()))


def key_matrix(stream, n, offsets=None):
    """Windows of the key stream long enough for the page; the stream is padded with itself so every
    offset up to len-1 is usable (a key shorter than the page wraps)."""
    L = n + S_MAX + 2
    s = np.asarray(stream, dtype=np.int64)
    s = np.concatenate([s, s[:L]]) if len(s) >= L else np.resize(s, len(s) + L)
    W = sliding_window_view(s, L)[:len(stream)]
    return W if offsets is None else W[np.asarray(offsets)]


def scan(C, stream, f_rule, sign, mode, nul, offsets=None, batch=1000):
    """z_uni for every offset (or the given offsets); returns z array, and decodes for the top rows."""
    W = key_matrix(stream, len(C), offsets)
    m0, s0, b0, sb = nul
    zs = np.empty(len(W)); best = []
    for b in range(0, len(W), batch):
        Kb = W[b:b + batch]
        Kb = (-Kb) % N if sign == "add" else Kb
        sc, _, dec = decode(C, Kb, lu, f_rule, mode)
        z = (sc - m0) / s0; zs[b:b + batch] = z
        for k in np.argsort(-z)[:3]:
            best.append((float(z[k]), b + int(k), float((bigram_many(dec[k:k + 1])[0] - b0) / sb), translit(dec[k])))
    best.sort(key=lambda r: -r[0])
    return zs, best


def collapse(rows, tol=3):
    out = []
    for r in rows:
        if all(abs(r[1] - o[1]) > tol for o in out): out.append(r)
    return out


def plant(text, variant, n):
    stream = np.asarray(corpus[text][variant]); o = int(rng.integers(0, len(stream) - 1))
    si = int(rng.integers(0, 3)); sign, mode = SIGNS[si]; f_rule = bool(rng.integers(0, 2)); rev = bool(rng.integers(0, 2))
    s = stream[::-1] if rev else stream
    L = n + S_MAX + 2
    s2 = np.concatenate([s, s[:L]]) if len(s) >= L else np.resize(s, len(s) + L)
    K = s2[o:o + L]
    p0 = int(rng.integers(0, len(plain) - n - 1)); P = plain[p0:p0 + n]
    C = encrypt(P, K, f_rule=f_rule, rng=rng, soft=SOFT, mode=sign)
    return C, dict(text=text, variant=variant, offset=o, sign=sign, mode=mode, F=f_rule, reversed=rev, n=n)


t0 = time.time()
RES = RESULTS

if MERGE:
    shards = sorted(RES.glob("runkey_shard*.json"))
    data = [json.loads(p.read_text()) for p in shards]
    controls = [c for d in data for c in d["controls"]]; cells = [c for d in data for c in d["cells"]]; ntests = sum(d["ntests"] for d in data)
    cands = [c for c in cells if c["z"] >= Z_UNI and c["zb"] >= Z_BIG]
    out = [f"# External running-key lane: exact decoding at every offset", "",
           f"{len(EXACT)} texts exact (every offset, both directions, V1 and V2) and {len(SENT)} long texts at sentence starts (V1); 3 signs x 2 F; "
           f"{ntests:,} tests over {len(pages)} pages; {NREPS} random-keystream nulls per page, F and mode; decoder max_skip {MAX_SKIP}. "
           f"Rule: z_uni >= {Z_UNI:.0f} and z_big >= {Z_BIG:.0f} and readable (module docstring). Chance maximum of z over this many tests about {np.sqrt(2*np.log(max(ntests,2))):.1f}.", "",
           "## Controls (soft rule 0.81, corpus text at a random offset, signs/F/direction random)", "",
           "| text | variant | n | sign | F | reversed | planted offset | top offset | z_uni | z_big | pass |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in controls:
        out.append(f"| {c['text']} | {c['variant']} | {c['n']} | {c['sign']} | {c['F']} | {c['reversed']} | {c['offset']} | {c['top_offset']} | {c['z']:.1f} | {c['zb']:.1f} | {'yes' if c['passed'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Best cell per page (over every text, direction, variant, sign and F)", "",
            "| page | runes | z_uni | z_big | text | variant | reversed | sign | F | offset | transliteration (first 60) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    bypage = {}
    for c in cells: bypage.setdefault(c["page"], []).append(c)
    for pid, C in pages:
        rs = sorted(bypage.get(pid, []), key=lambda r: -r["z"])
        if rs:
            r = rs[0]; out.append(f"| {pid} | {len(C)} | {r['z']:.2f} | {r['zb']:.1f} | {r['text']} | {r['variant']} | {r['reversed']} | {r['sign']} | {r['F']} | {r['offset']} | {r['translit'][:60]} |")
    out += ["", "## Candidates meeting (1)-(2), for the readability check", ""]
    for c in sorted(cands, key=lambda r: -r["z"]): out.append(f"- **{c['page']}** {c['text']} ({c['variant']}, {'reversed' if c['reversed'] else 'forward'}) {c['sign']} F={c['F']} offset {c['offset']}: z_uni {c['z']:.2f}, z_big {c['zb']:.1f}: `{c['translit']}`")
    if not cands: out.append("None.")
    zmax = max((c["z"] for c in cells), default=0)
    out += ["", f"Largest z_uni over all tests: {zmax:.2f}. Cells at z_uni >= 5: {sum(1 for c in cells if c['z'] >= 5)}. Runtime, longest shard: {max(d['seconds'] for d in data)/60:.0f} minutes on {len(shards)} shards.", ""]
    (RES / "runkey.md").write_text("\n".join(out) + "\n")
    json.dump({"ntests": ntests, "rule": dict(z_uni=Z_UNI, z_big=Z_BIG, nulls=NREPS, max_skip=MAX_SKIP, limit=LIMIT), "controls": controls, "cells": cells}, open(RES / "runkey.json", "w"), indent=1)
    print("\n".join(out[:6] + out[-4:])); sys.exit(0)

# ---------- controls (shard 0 / smoke) ----------
controls = []
if SHARD == 0 or SMOKE:
    lens = [262, 137, 92, 200, 277, 159]
    plan = [(t, v) for t in EXACT for v in (("runes", "runes_nodigraph") if (not SMOKE and len(EXACT[t]["runes"]) <= V2LIMIT) else ("runes",))] + [(t, "runes") for t in SENT]
    for ci, (text, variant) in enumerate(plan):
        n = lens[ci % len(lens)]
        C, truth = plant(text, variant, n)
        nul = null_for(C, truth["F"], truth["mode"])
        stream = np.asarray(corpus[text][variant]); s = stream[::-1] if truth["reversed"] else stream
        offs = None if text in EXACT else corpus[text]["sentence_starts"]
        if offs is not None and truth["offset"] not in offs: offs = sorted(set(offs) | {truth["offset"]})   # a planted sentence-lane key sits at a sentence start by construction of the test
        if truth["reversed"] and offs is not None: offs = sorted({(len(stream) - o) % len(stream) for o in corpus[text]["sentence_starts"]} | {truth["offset"]})
        zs, best = scan(C, s, truth["F"], truth["sign"], truth["mode"], nul, offs)
        top = collapse(best)[0]
        top_off = top[1] if offs is None else int(np.asarray(offs)[top[1]])
        passed = top[0] >= Z_UNI and top[2] >= Z_BIG and abs(top_off - truth["offset"]) <= 3
        controls.append(dict(**truth, top_offset=top_off, z=top[0], zb=top[2], passed=bool(passed)))
        print(f"  control {text}/{variant} n={n} {truth['sign']} F={truth['F']} rev={truth['reversed']} planted {truth['offset']}: top {top_off} z_uni {top[0]:.1f} z_big {top[2]:.1f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)
    print(f"controls: {sum(c['passed'] for c in controls)}/{len(controls)} pass", flush=True)
    if SMOKE and not pages: sys.exit(0)

# ---------- the pages ----------
cells, ntests = [], 0
my_pages = pages[SHARD::NSHARD]
for pi_, (pid, C) in enumerate(my_pages):
    n = len(C)
    for f_rule in (False, True):
        nul_by_mode = {}
        for sign, mode in SIGNS:
            if mode not in nul_by_mode: nul_by_mode[mode] = null_for(C, f_rule, mode)
            nul = nul_by_mode[mode]
            for text, v in list(EXACT.items()) + list(SENT.items()):
                variants = ("runes", "runes_nodigraph") if (text in EXACT and len(v["runes"]) <= V2LIMIT) else ("runes",)
                for variant in variants:
                    stream = np.asarray(v[variant])
                    for rev in ((False, True) if variant == "runes" else (False,)):
                        s = stream[::-1] if rev else stream
                        # reversed long text: start at sentence ends read backwards (position len - o holds the rune before start o)
                        offs = None if text in EXACT else sorted({(len(stream) - o) % len(stream) for o in v["sentence_starts"]}) if rev else v["sentence_starts"]
                        zs, best = scan(C, s, f_rule, sign, mode, nul, offs); ntests += len(zs)
                        for z, k, zb, tr in collapse(best)[:2]:
                            off = k if offs is None else int(np.asarray(offs)[k])
                            cells.append(dict(page=pid, text=text, variant="V1" if variant == "runes" else "V2", reversed=rev, sign=sign, F=f_rule, offset=off, z=z, zb=zb, translit=tr))
    bz = max(c["z"] for c in cells if c["page"] == pid)
    print(f"  {pid} ({n} runes) done ({pi_+1}/{len(my_pages)}): best z_uni {bz:.2f}; {ntests:,} tests so far  [{time.time()-t0:.0f}s]", flush=True)

json.dump({"controls": controls, "cells": cells, "ntests": ntests, "seconds": time.time() - t0}, open(RES / (f"runkey_smoke.json" if SMOKE else f"runkey_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} written: {ntests:,} tests, {time.time()-t0:.0f}s", flush=True)
