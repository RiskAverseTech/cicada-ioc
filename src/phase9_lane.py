"""Phase 9: two families no ledger has run, both shaped by Cicada's own hint that
"their numbers are the direction".

  A. Cumulative-Gematria ciphertext feedback.  S_i = sum of the values of the ciphertext runes
     before position i (value = rune index 0..28, the rune's Gematria prime 2..109, or that
     prime minus one), reset per page.  The key at i is f(S_i) + T_j with f one of
     S mod 29, p_S mod 29 (the S-th prime) or (p_S - 1) mod 29, and T a base stream
     (the totient or prime stream at offsets 0..100, or none).  With a base stream the soft
     reject-on-repeat applies to T (skip k=1); with none the key has nothing to skip and the
     page is decoded plainly.  S_i is known from the ciphertext, so decryption is exact.
  B. Global streams with no per-page reset.  The prime, totient, prime+1, prime-gap, Fibonacci
     and Lucas streams at EVERY offset 0..13,500 (every phase so far restarted each page at
     offsets 0..100; a stream that runs through the whole book puts page 30 near offset 7,000),
     soft reject-on-repeat.
Both: signs add (C = P + K), sub (C = P - K) and Beaufort (C = K - P); both F variants.

PRE-REGISTERED POSITIVE RULE (written before running): a page counts as decrypted only if its
best configuration scores z >= 6 above that page's own random-keystream null (2,000 random
keystreams through the identical decoder, same mode and F variant) AND the transliteration
reads as English to a human.  About 13 million tests; chance maximum about 5.7.  Controls:
planted keys spanning both families, all signs and F variants, soft 81 %, must be recovered at
z >= 6 and rank first in their set, or the sweep is not trusted.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import english_model, decode, null_scores, translit, S_MAX

SMOKE = "--smoke" in sys.argv
SHARD = next((a for a in sys.argv if a.startswith("--shard")), None)
SHARD_K, SHARD_N = (int(x) for x in sys.argv[sys.argv.index(SHARD) + 1].split("/")) if SHARD else (0, 1)
MERGE = "--merge" in sys.argv
REDO = "--redo-a-sub" in sys.argv   # rerun family A x sign "sub" only (first run had the offset sign wrong for that mode)
rng = np.random.default_rng(9009)
lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
if SMOKE: pages = pages[:2]
ALL_PAGES = len(pages)
if SHARD: pages = pages[SHARD_K::SHARD_N]
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
GLOBAL_MAX = 300 if SMOKE else 13_500


def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)


PR = sieve(26_000_000)                      # 1.6 M primes: enough for p_S with S up to ~1.5 M, and for the global streams
PV = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109])
VALUES = {"index": np.arange(N), "prime": PV, "totient": PV - 1}
FMAPS = {"sum mod 29": lambda S: S % N, "p_S mod 29": lambda S: PR[S] % N, "phi(p_S) mod 29": lambda S: (PR[S] - 1) % N}
STREAMS = {"prime": PR % N, "totient": (PR - 1) % N, "prime+1": (PR + 1) % N, "prime gap": (PR[1:] - PR[:-1]) % N}
fib = [0, 1]
while len(fib) < GLOBAL_MAX + LMAX + 10: fib.append((fib[-1] + fib[-2]) % N)
luc = [2, 1]
while len(luc) < GLOBAL_MAX + LMAX + 10: luc.append((luc[-1] + luc[-2]) % N)
STREAMS["fibonacci"] = np.array(fib); STREAMS["lucas"] = np.array(luc)
MODES = {"add": ("sub", 1), "sub": ("sub", -1), "beaufort": ("beaufort", 1)}   # sign -> (decoder mode, key multiplier)


def cumulative_offsets(C, vname, fname):
    S = np.concatenate([[0], np.cumsum(VALUES[vname][C])[:-1]])
    return FMAPS[fname](S).astype(np.int64)


def stream_slices(name, offsets):
    base = STREAMS[name]
    return np.stack([base[o:o + LMAX] for o in offsets]).astype(np.int64)


# ---------- family A configurations: (label, vname, fname, base stream name or None, base offset) ----------
A_CONF = [(f"{v}-sum → {f}" + (f" + {b}@{o}" if b else ""), v, f, b, o)
          for v in VALUES for f in FMAPS for (b, offs) in (("totient", range(0, 101)), ("prime", range(0, 101)), (None, [0])) for o in offs]
B_OFFS = np.arange(0, GLOBAL_MAX + 1)
print(f"family A: {len(A_CONF)} configurations x 3 signs; family B: {len(STREAMS)} streams x {len(B_OFFS)} offsets x 3 signs; "
      f"{len(pages)} pages x 2 F variants: about {(3*len(A_CONF) + 3*len(STREAMS)*len(B_OFFS)) * len(pages) * 2:,} tests", flush=True)


def encrypt_A(P, vname, fname, Kbase, sign, f_rule, soft=0.81):
    C, j, prev, S = [], 0, None, 0
    for p in P:
        if f_rule and p == 0:
            C.append(0); prev = 0; S += int(VALUES[vname][0]); continue
        O = int(FMAPS[fname](np.array([S]))[0])
        def comb(k):
            key = (O + k) % N
            return (p + key) % N if sign == "add" else ((p - key) % N if sign == "sub" else (key - p) % N)
        c = comb(int(Kbase[j]) if Kbase is not None else 0)
        while Kbase is not None and prev is not None and c == prev and rng.random() < soft:
            j += 1; c = comb(int(Kbase[j]))
        C.append(c); j += 1; prev = c; S += int(VALUES[vname][c])
    return np.array(C)


def encrypt_B(P, K, sign, f_rule, soft=0.81):
    C, j, prev = [], 0, None
    for p in P:
        if f_rule and p == 0:
            C.append(0); prev = 0; continue
        comb = lambda k: (p + k) % N if sign == "add" else ((p - k) % N if sign == "sub" else (k - p) % N)
        c = comb(int(K[j]))
        while prev is not None and c == prev and rng.random() < soft:
            j += 1; c = comb(int(K[j]))
        C.append(c); j += 1; prev = c
    return np.array(C)


def decode_A(C, conf, sign, f_rule):
    """One configuration, one page: returns (score, skips, plaintext)."""
    _, v, f, b, o = conf
    mode, km = MODES[sign]
    off = (km * cumulative_offsets(C, v, f)) % N   # sign "sub": C = P - (O + K), so the offset is negated with K
    if b is None:
        K = np.zeros((1, LMAX), dtype=np.int64)
        # no base stream: plain decode without the skip rule (nothing to skip); emulate by a decoder
        # whose skip transition can never fire (a constant zero key never satisfies K_j != K_{j-1}... it
        # does satisfy C_i - C_{i-1} == 0 only on a doublet; those are rare and the null shares the optimism)
        return decode(C, K, lu, f_rule, mode, offset=off)
    K = (km * stream_slices(b, [o])) % N
    return decode(C, K, lu, f_rule, mode, offset=off)


def best_A(C, sign, f_rule):
    scores = np.empty(len(A_CONF)); skips = np.zeros(len(A_CONF), dtype=int); tops = {}
    # group by (v, f, b): offsets batch together with the same offset vector
    groups = {}
    for idx, conf in enumerate(A_CONF):
        groups.setdefault((conf[1], conf[2], conf[3]), []).append(idx)
    mode, km = MODES[sign]
    for (v, f, b), idxs in groups.items():
        off = (km * cumulative_offsets(C, v, f)) % N
        if b is None:
            K = np.zeros((1, LMAX), dtype=np.int64)
        else:
            K = (km * stream_slices(b, [A_CONF[i][4] for i in idxs])) % N
        s, t, out = decode(C, K, lu, f_rule, mode, offset=off)
        for r, i in enumerate(idxs):
            scores[i] = s[r]; skips[i] = t[r]
        for r in np.argsort(-s)[:2]:
            tops[idxs[r]] = out[r]
    return scores, skips, tops


def best_B(C, sign, f_rule, batch=1500):
    mode, km = MODES[sign]
    labels, scores, skips, tops = [], [], [], {}
    for name in STREAMS:
        for b0 in range(0, len(B_OFFS), batch):
            offs = B_OFFS[b0:b0 + batch]
            K = (km * stream_slices(name, offs)) % N
            s, t, out = decode(C, K, lu, f_rule, mode)
            base = len(labels)
            labels += [(name, int(o)) for o in offs]; scores += list(s); skips += list(t)
            for r in np.argsort(-s)[:2]:
                tops[base + r] = out[r]
    return labels, np.array(scores), np.array(skips), tops


# ---------- controls ----------
ctrl_rows = []
t0 = time.time()
NC = 4 if SMOKE else (18 if SHARD_K == 0 else 0)
if MERGE: NC = 0
if REDO: NC = 4 if SHARD_K == 0 else 0
for ci in range(NC):
    sign = ["add", "sub", "beaufort"][ci % 3]
    f_rule = bool((ci // 3) % 2)
    if REDO: sign, f_rule, ci = "sub", bool(ci % 2), 100 + (2 * ci if SMOKE else ci)   # redo controls: sign sub, F alternating; A when ci even (all A under --smoke)
    o = int(rng.integers(0, len(plain) - 240)); P = plain[o:o + 240]
    mode, km = MODES[sign]
    if ci % 2 == 0:   # family A
        ki = int(rng.integers(0, len(A_CONF))); conf = A_CONF[ki]
        Kb = None if conf[3] is None else stream_slices(conf[3], [conf[4]])[0]
        C = encrypt_A(P, conf[1], conf[2], Kb, sign, f_rule)
        nul = null_scores(C, lu, f_rule, rng, 500, mode)
        sc, sk, tops = best_A(C, sign, f_rule)
        z = (sc - nul.mean()) / nul.std()
        rank = int((z > z[ki]).sum()) + 1
        rec = decode_A(C, conf, sign, f_rule)[2][0]
        label = f"A {conf[0]}"
    else:             # family B
        name = list(STREAMS)[ci % len(STREAMS)]; off = int(rng.integers(0, GLOBAL_MAX))
        K = stream_slices(name, [off])[0]
        C = encrypt_B(P, (km * K) % N if sign != "sub" else K, sign, f_rule) if False else encrypt_B(P, K, sign, f_rule)
        nul = null_scores(C, lu, f_rule, rng, 500, mode)
        labels, sc, sk, tops = best_B(C, sign, f_rule)
        ki = labels.index((name, off))
        z = (sc - nul.mean()) / nul.std()
        rank = int((z > z[ki]).sum()) + 1
        rec = decode(C, (km * stream_slices(name, [off])) % N, lu, f_rule, mode)[2][0]
        label = f"B {name}@{off}"
    cname = f"redo-{ci-100:02d}" if REDO else f"control-{ci:02d}"
    ctrl_rows.append((cname, label, sign, f_rule, float(z[ki]), rank, float((rec == P).mean())))
    print(f"  {cname}: {label} {sign} F={f_rule}: z={z[ki]:.1f} rank {rank}, recovered {(rec == P).mean():.3f}", flush=True)
print(f"controls done in {time.time()-t0:.0f}s", flush=True)
if SMOKE: sys.exit(0)

# ---------- redo of family A x sub (offset sign fix) ----------
if REDO:
    jf = RESULTS / f"phase9_shard{SHARD_K}.json"
    j = json.load(open(jf))
    keep = [tuple(r) for r in j["results"] if not (r[1] == "A" and r[2] == "sub")]
    new, t0 = [], time.time()
    for pi, (pid, C) in enumerate(pages):
        for f_rule in (False, True):
            n_ = null_scores(C, lu, f_rule, rng, 2000, "sub")
            sc, sk, tops = best_A(C, "sub", f_rule)
            z = (sc - n_.mean()) / n_.std()
            for k in np.argsort(-z)[:2]:
                new.append((pid, "A", "sub", f_rule, A_CONF[k][0], float(z[k]), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
        print(f"  {pid} redone ({pi+1}/{len(pages)}), best A/sub z: {max(r[5] for r in new if r[0]==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)
    ctrls = []
    for r in j["controls"]:
        r = tuple(r)
        if r[0] in ("control-04", "control-10", "control-16") and "sign bug" not in r[1]:
            r = (r[0], r[1] + " [first run: offset sign bug, superseded by redo rows]") + r[2:]
        ctrls.append(r)
    json.dump({"results": keep + new, "controls": ctrls + ctrl_rows, "redo_a_sub": True}, open(jf, "w"))
    print(f"shard {SHARD_K}/{SHARD_N} A/sub rows replaced", flush=True); sys.exit(0)

# ---------- the sweep ----------
t0 = time.time()
results = []   # (page, family, sign, f_rule, label, z, skips, translit)
if MERGE: pages = []
for pi, (pid, C) in enumerate(pages):
    for f_rule in (False, True):
        nul = {}
        for sign in MODES:
            mode, _ = MODES[sign]
            if mode not in nul: nul[mode] = null_scores(C, lu, f_rule, rng, 2000, mode)
            n_ = nul[mode]
            sc, sk, tops = best_A(C, sign, f_rule)
            z = (sc - n_.mean()) / n_.std()
            for k in np.argsort(-z)[:2]:
                results.append((pid, "A", sign, f_rule, A_CONF[k][0], float(z[k]), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
            labels, sc, sk, tops = best_B(C, sign, f_rule)
            z = (sc - n_.mean()) / n_.std()
            for k in np.argsort(-z)[:2]:
                results.append((pid, "B", sign, f_rule, f"{labels[k][0]}@{labels[k][1]}", float(z[k]), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
    print(f"  {pid} done ({pi+1}/{len(pages)}), best z on this page: A {max(r[5] for r in results if r[0]==pid and r[1]=='A'):.2f}, B {max(r[5] for r in results if r[0]==pid and r[1]=='B'):.2f}  [{time.time()-t0:.0f}s]", flush=True)

if SHARD and not MERGE:
    json.dump({"results": results, "controls": ctrl_rows}, open(RESULTS / f"phase9_shard{SHARD_K}.json", "w"))
    print(f"shard {SHARD_K}/{SHARD_N} written", flush=True); sys.exit(0)
if MERGE:
    for f in sorted(RESULTS.glob("phase9_shard*.json")):
        j = json.load(open(f)); results += [tuple(r) for r in j["results"]]; ctrl_rows += [tuple(r) for r in j["controls"]]
    pages = [None] * ALL_PAGES
results.sort(key=lambda r: -r[5])
ntests = (3 * len(A_CONF) + 3 * len(STREAMS) * len(B_OFFS)) * len(pages) * 2
zmax = results[0][5]
out = ["# Phase 9 sweep: cumulative-Gematria ciphertext feedback, and global streams with no per-page reset", "",
       f"Family A: {len(A_CONF)} configurations (3 value maps × 3 index maps × base stream totient/prime at offsets 0..100 or none); family B: {len(STREAMS)} streams × {len(B_OFFS):,} global offsets; 3 signs; {len(pages)} pages; 2 F variants: **{ntests:,} tests**. Chance maximum about {np.sqrt(2*np.log(ntests)):.1f}.",
       "Per page, variant and decoder mode the null is 2,000 random keystreams through the same decoder. Positive rule (pre-registered): z ≥ 6 over that null and English on inspection.", "",
       "## Planted controls", "", "| control | key | sign | F | z | rank in family | runes recovered |", "|---|---|---|---|---|---|---|"]
for r in ctrl_rows:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.1f} | {r[5]} | {r[6]:.3f} |")
good = [r for r in ctrl_rows if "sign bug" not in r[1]]
out += ["", f"Controls recovered at z ≥ 6 and rank 1: {sum(1 for r in good if r[4] >= 6 and r[5] == 1)} of {len(good)} (z {min(r[4] for r in good):.1f}–{max(r[4] for r in good):.1f})."
        + (" The three rows marked *offset sign bug* are the first run's family-A `sub` controls: the decoder was given the cumulative offset un-negated for that sign, so family A × sub was effectively testing C = P + O − K. The sign was fixed, family A × sub was rerun for every page and both F variants with fresh nulls, and the four `redo-*` rows are its new controls." if len(good) != len(ctrl_rows) else ""), "",
        "## Unsolved pages: top 20 configurations overall", "",
        "| page | family | sign | F | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|"]
for r in results[:20]:
    out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.2f} | {r[6]} | {r[7]} |")
out += ["", "Largest z per family: " + "; ".join(f"{fam} {max(r[5] for r in results if r[1]==fam):.2f}" for fam in ("A", "B")) + ".", "",
        f"Largest z over all {ntests:,} tests: {zmax:.2f} ({results[0][0]}, family {results[0][1]}, {results[0][2]}, {results[0][4]}).", "",
        "## Verdict", "",
        ("**No page decrypts.** " if zmax < 6 else "**At least one configuration clears z = 6: inspect the transliteration above before believing it.** ") +
        "Keys driven by the cumulative Gematria value of the preceding ciphertext (three value maps, three index maps, with the totient or prime stream at 101 offsets or alone), and the book's six streams run continuously through the book at every offset up to 13,500, under the soft reject-on-repeat rule, three signs and both F variants, are excluded at the sensitivity the controls demonstrate. Not covered: cumulative sums of the plaintext (an autokey the Viterbi state cannot carry), sums that include the current rune, or streams outside these six.", ""]
(RESULTS / "phase9.md").write_text("\n".join(out) + "\n")
json.dump({"ntests": ntests, "controls": ctrl_rows, "top": results[:60]}, open(RESULTS / "phase9.json", "w"), indent=1)
print("\n".join(out[:4] + out[-6:]))
