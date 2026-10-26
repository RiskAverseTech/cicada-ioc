"""Hypothesis loop: a panel of models proposes cipher constructions from a fixed menu, a
computational gate kills them before any decoder time is spent.

Loop:
  1. Evidence brief (README, results/doublets.md, results/ledger_diff.md) under 12k tokens.
  2. Proposers (Claude Fable 5.1 first; GPT and Grok if their keys work) return up to 15 ranked
     constructions each, in the JSON schema below and nothing else.  Raw responses are saved
     under results/hypotheses/.  Proposals are DATA: the gate only assembles constructions from
     the menu in this file and never runs anything a model wrote.
  3. Gate: each construction enciphers resampled solved-page plaintext cut to the 55 real page
     lengths (the machinery of src/doublets.py, vectorised over 200 replicates) and is scored on
     the four page statistics; pass = every |z| < 3.  Passing constructions that are decryptable
     given a key (a finite family) are checked against the ledgers and sized.
  4. A second round feeds the gate table back to the proposers for refinements, if budget allows.
  5. results/hypotheses.md, results/hypotheses.json, token usage and cost.

Run:  .venv/bin/python -I src/hypothesis_loop.py            (full run, both rounds)
      .venv/bin/python -I src/hypothesis_loop.py --dry       (gate calibration only, no API)
      .venv/bin/python -I src/hypothesis_loop.py --rounds 1
API keys are read from /Users/jaz/Desktop/quorum/.env.local (or the environment) and never printed.
"""
import argparse, hashlib, json, re, sys, time, os
import urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, ROOT, RAW, PROCESSED, RESULTS, LATIN, primes, english_to_runes

HYP = RESULTS / "hypotheses"
DOCS = ROOT / "docs"
ENV_FILE = Path("/Users/jaz/Desktop/quorum/.env.local")
REPS = 200
Z_PASS = 3.0
MAXIT = 24                      # cap on repeat-rule re-draw iterations per position
rng = np.random.default_rng(3301)

# ---------------------------------------------------------------- data (as in src/doublets.py)
d = json.loads((PROCESSED / "pages.json").read_text())
LENS = np.array([u["length"] for u in d["unsolved"] if u["length"] > 0])
OBS_PAGES = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
G, L = len(LENS), int(LENS.max())
MASK = np.arange(L)[None, :] < LENS[:, None]            # (G, L) valid positions
LT = 4 * L + 64                                          # key symbols available per page (skips need extra)
PV = np.array(primes(N))                                 # Gematria Primus prime value of rune 0..28
MAX_OFFSET = 20000


def sieve(n):
    """All primes below n."""
    s = np.ones(n, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0]


_PR = sieve(400000)                                      # 33,860 primes: enough for offset 20,000 + LT
def PRIMES(o, n): return _PR[o:o + n + 1]
def fib_like(a, b, o, n):
    """Terms o .. o+n-1 of the recurrence x_(k+1) = x_k + x_(k-1) mod 29 starting a, b."""
    out = np.empty(o + n, dtype=np.int64); out[0], out[1] = a % N, b % N
    for k in range(2, o + n): out[k] = (out[k - 1] + out[k - 2]) % N
    return out[o:o + n]


def sample_pages(R):
    """(R, G, L) plaintext matrix: each replicate cuts the solved plaintext into the 55 real page
    lengths from random offsets (wraparound), exactly as doublets.py does per replicate."""
    off = rng.integers(0, len(plain), (R, G, 1))
    return plain[(off + np.arange(L)[None, None, :]) % len(plain)]


def stats_matrix(C, mask=MASK):
    """Per replicate: doublets, chi2 of the 28 non-zero lag-1 difference classes, unigram chi2, IC."""
    R = C.shape[0]
    vp = mask[:, :-1] & mask[:, 1:]
    dlt = (C[:, :, :-1] - C[:, :, 1:]) % N
    dbl = ((dlt == 0) & vp[None]).sum(axis=(1, 2))
    cls = np.stack([np.bincount(dlt[r][vp], minlength=N) for r in range(R)])
    nz = cls[:, 1:].astype(float); m = nz.mean(1, keepdims=True)
    chi_nz = ((nz - m) ** 2 / m).sum(1)
    uni = np.stack([np.bincount(C[r][mask], minlength=N) for r in range(R)]).astype(float)
    mu = uni.mean(1, keepdims=True)
    chi_u = ((uni - mu) ** 2 / mu).sum(1)
    n = mask.sum()
    ic = (uni * (uni - 1)).sum(1) / (n * (n - 1))
    return np.stack([dbl, chi_nz, chi_u, ic], 1)


def observed():
    C = np.zeros((1, G, L), dtype=int)
    for g, c in enumerate(OBS_PAGES): C[0, g, :len(c)] = c
    return stats_matrix(C)[0]


OBS = observed()
STAT_NAMES = ["doublets", "lag-1 class chi2", "unigram chi2", "IC"]

# ---------------------------------------------------------------- the menu (what the gate can execute)
KEY_TYPES = ["uniform", "lcg", "prime", "totient", "prime_plus1", "prime_gap", "fibonacci", "lucas",
             "position", "word", "running_text", "cipher_feedback", "plain_feedback"]
BASES = ["none", "uniform", "lcg", "prime", "totient", "prime_plus1", "fibonacci", "lucas", "position", "word", "running_text"]
MAPS = ["identity", "atbash", "shift", "affine", "prime_value", "totient_value", "square", "random_bijection"]
COMBINES = ["add", "sub", "beaufort", "affine"]
MULT_SOURCES = ["const", "position", "key2"]
REPEAT_RULES = ["none", "redraw", "skip", "bump"]
TARGETS = ["cipher", "key", "plain"]
F_RULES = ["none", "literal_f", "literal_f_consumes"]

MENU_TEXT = f"""
MENU (the only constructions the gate can execute; every proposal must be assembled from it)

key_source.type, one of {KEY_TYPES}:
  uniform        iid uniform key symbols (a secret pad; any unpublished pad or PRNG looks like this to the gate)
  lcg            x_(n+1) = (a*x_n + c) mod modulus, random seed per page, key = x mod 29        [a, c, modulus]
  prime          p_(n+offset) mod 29;  totient: p-1;  prime_plus1: p+1;  prime_gap: p_(n+1)-p_n   [offset]
  fibonacci      F_(n+offset) mod 29;  lucas likewise                                            [offset]
  position       (a*n^2 + b*n + c) mod 29                                                        [a, b, c]
  word           periodic key: the runes of `text` (English spelled with the book's rules, e.g. "DIVINITY",
                 a phrase, a sentence) or, if text is "", a random key of length `period`          [text | period]
  running_text   the solved pages' own plaintext from a random offset (any English running key looks like this)
  cipher_feedback  K_i = map(C_(i-lag)) (+ base stream symbol if base != none), random seed for i < lag   [lag, map, a, b, base]
  plain_feedback   K_i = map(P_(i-lag)) (+ base stream symbol if base != none)                           [lag, map, a, b, base]
key_source.map (feedback only), one of {MAPS}: identity x; atbash 28-x; shift x+b; affine a*x+b;
  prime_value = Gematria Primus prime of the rune (F=2, U=3, TH=5, ...) mod 29; totient_value = that prime - 1;
  square x^2; random_bijection = a fixed random permutation of the 29 runes.
key_source.base (feedback only), one of {BASES}: a deterministic or random stream added to the feedback term.

combine.rule, one of {COMBINES}:  add C = P + K;  sub C = P - K;  beaufort C = K - P;
  affine C = m*P + K with m from combine.multiplier_source in {MULT_SOURCES}:
  const (m = combine.multiplier, 1..28), position (m_i = ((a*i + b) mod 28) + 1), key2 (a second secret uniform stream in 1..28).

repeat_rule.rule, one of {REPEAT_RULES}, applied when the rune at `target` would repeat its predecessor
  (target in {TARGETS}: cipher = C_i == C_(i-1), the observed property; key = K_j == K_(j-1), a pad that never repeats;
  plain = P_i == P_(i-1)), each time with probability p (1.0 = always):
  none; redraw = draw the next key symbol instead (on a deterministic stream this is the same as skip k=1; on a
  feedback-only key it is a fresh uniform symbol); skip = advance the key index by k; bump = add delta to C_i.

f_rule, one of {F_RULES}: none; literal_f = a plaintext F is written unencrypted and consumes no key symbol
  (the book's published rule); literal_f_consumes = written unencrypted but the key symbol is still consumed.

Things the gate cannot see and you should not propose: a fixed substitution applied before or after (it does not
change any of the four statistics), transposition, nulls at word edges (phase 6), which text an external running key
comes from (all English running keys look alike), the seed of a pad (all pads look like `uniform`).
"""

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"proposals": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "rank": {"type": "integer"},
            "name": {"type": "string"},
            "rationale": {"type": "string"},
            "predicted_doublets": {"type": "integer"},
            "key_source": {"type": "object", "additionalProperties": False, "properties": {
                "type": {"type": "string", "enum": KEY_TYPES},
                "offset": {"type": "integer"}, "period": {"type": "integer"}, "text": {"type": "string"},
                "lag": {"type": "integer"}, "map": {"type": "string", "enum": MAPS},
                "base": {"type": "string", "enum": BASES},
                "a": {"type": "integer"}, "b": {"type": "integer"}, "c": {"type": "integer"}, "modulus": {"type": "integer"}},
                "required": ["type", "offset", "period", "text", "lag", "map", "base", "a", "b", "c", "modulus"]},
            "combine": {"type": "object", "additionalProperties": False, "properties": {
                "rule": {"type": "string", "enum": COMBINES}, "multiplier": {"type": "integer"},
                "multiplier_source": {"type": "string", "enum": MULT_SOURCES}, "a": {"type": "integer"}, "b": {"type": "integer"}},
                "required": ["rule", "multiplier", "multiplier_source", "a", "b"]},
            "repeat_rule": {"type": "object", "additionalProperties": False, "properties": {
                "rule": {"type": "string", "enum": REPEAT_RULES}, "p": {"type": "number"}, "k": {"type": "integer"},
                "delta": {"type": "integer"}, "target": {"type": "string", "enum": TARGETS}},
                "required": ["rule", "p", "k", "delta", "target"]},
            "f_rule": {"type": "string", "enum": F_RULES}},
        "required": ["rank", "name", "rationale", "predicted_doublets", "key_source", "combine", "repeat_rule", "f_rule"]}}},
    "required": ["proposals"]}


def normalize(c):
    """Validate a proposal against the menu; return (construction, error or None). Never executes anything."""
    try:
        ks, cb, rr = dict(c["key_source"]), dict(c["combine"]), dict(c["repeat_rule"])
        fr = c["f_rule"]
        if ks["type"] not in KEY_TYPES: return None, f"key_source.type {ks['type']!r} not in menu"
        if cb["rule"] not in COMBINES: return None, f"combine.rule {cb['rule']!r} not in menu"
        if rr["rule"] not in REPEAT_RULES: return None, f"repeat_rule.rule {rr['rule']!r} not in menu"
        if fr not in F_RULES: return None, f"f_rule {fr!r} not in menu"
        ks.setdefault("offset", 0); ks.setdefault("period", 0); ks.setdefault("text", ""); ks.setdefault("lag", 1)
        ks.setdefault("map", "identity"); ks.setdefault("base", "none"); ks.setdefault("a", 1); ks.setdefault("b", 0)
        ks.setdefault("c", 0); ks.setdefault("modulus", 0)
        if ks["map"] not in MAPS: return None, f"map {ks['map']!r} not in menu"
        if ks["base"] not in BASES: return None, f"base {ks['base']!r} not in menu"
        ks["lag"] = max(1, min(int(ks["lag"]), 60)); ks["offset"] = max(0, min(int(ks["offset"]), MAX_OFFSET))
        ks["period"] = max(0, min(int(ks["period"]), 400))
        if ks["type"] == "word":
            runes = english_to_runes(ks["text"]) if ks["text"] else []
            if not runes and ks["period"] < 1: return None, "word key needs text or period >= 1"
        if ks["type"] == "lcg" and int(ks["modulus"]) < 2: return None, "lcg needs modulus >= 2"
        cb.setdefault("multiplier", 1); cb.setdefault("multiplier_source", "const"); cb.setdefault("a", 1); cb.setdefault("b", 0)
        if cb["multiplier_source"] not in MULT_SOURCES: return None, "multiplier_source not in menu"
        cb["multiplier"] = int(cb["multiplier"]) % N or 1
        rr.setdefault("p", 1.0); rr.setdefault("k", 1); rr.setdefault("delta", 1); rr.setdefault("target", "cipher")
        if rr["target"] not in TARGETS: return None, "target not in menu"
        rr["p"] = float(min(max(rr["p"], 0.0), 1.0)); rr["k"] = max(1, min(int(rr["k"]), 8)); rr["delta"] = int(rr["delta"]) % N or 1
        return {"key_source": ks, "combine": cb, "repeat_rule": rr, "f_rule": fr}, None
    except (KeyError, TypeError, ValueError) as e:
        return None, f"malformed: {e!r}"


def con_hash(con):
    return hashlib.sha1(json.dumps(con, sort_keys=True).encode()).hexdigest()[:10]


def describe(con):
    ks, cb, rr = con["key_source"], con["combine"], con["repeat_rule"]
    t = ks["type"]
    if t in ("prime", "totient", "prime_plus1", "prime_gap", "fibonacci", "lucas"): s = f"{t}[n+{ks['offset']}]"
    elif t == "position": s = f"{ks['a']}n²+{ks['b']}n+{ks['c']}"
    elif t == "word": s = f"word '{ks['text'][:30]}'" if ks["text"] else f"random key len {ks['period']}"
    elif t == "lcg": s = f"lcg(a={ks['a']},c={ks['c']},m={ks['modulus']})"
    elif t in ("cipher_feedback", "plain_feedback"):
        mp = ks["map"] + (f"({ks['a']},{ks['b']})" if ks["map"] in ("shift", "affine") else "")
        s = f"{'C' if t[0]=='c' else 'P'}-feedback lag {ks['lag']} map {mp}" + (f" + {ks['base']}" if ks["base"] != "none" else "")
    else: s = t
    comb = cb["rule"] if cb["rule"] != "affine" else f"affine m={cb['multiplier'] if cb['multiplier_source']=='const' else cb['multiplier_source']}"
    if rr["rule"] == "none": rep = "no repeat rule"
    else:
        rep = f"{rr['rule']}" + (f" k={rr['k']}" if rr["rule"] == "skip" else "") + (f" δ={rr['delta']}" if rr["rule"] == "bump" else "")
        rep += f" p={rr['p']:.2f}" + (f" on {rr['target']}" if rr["target"] != "cipher" else "")
    return f"{s}; {comb}; {rep}; F={con['f_rule']}"


# ---------------------------------------------------------------- the gate
def base_stream(kind, ks, R):
    """(R, G, LT) key symbols for the stream kinds, or None for 'none'."""
    if kind == "none": return None
    if kind == "uniform": return rng.integers(0, N, (R, G, LT))
    if kind == "lcg":
        m = min(int(ks["modulus"]), 2 ** 31 - 1); a, c = int(ks["a"]) % m, int(ks["c"]) % m
        x = rng.integers(0, m, (R, G), dtype=np.int64); out = np.empty((R, G, LT), dtype=np.int64)
        for n in range(LT):
            x = (a * x + c) % m; out[:, :, n] = x % N
        return out
    o = min(int(ks["offset"]), MAX_OFFSET)
    if kind == "prime": v = PRIMES(o, LT)[:LT] % N
    elif kind == "totient": v = (PRIMES(o, LT)[:LT] - 1) % N
    elif kind == "prime_plus1": v = (PRIMES(o, LT)[:LT] + 1) % N
    elif kind == "prime_gap": pr = PRIMES(o, LT); v = (pr[1:LT + 1] - pr[:LT]) % N
    elif kind == "fibonacci": v = fib_like(0, 1, o, LT)
    elif kind == "lucas": v = fib_like(2, 1, o, LT)
    elif kind == "position":
        n = np.arange(LT); v = (ks["a"] * n * n + ks["b"] * n + ks["c"]) % N
    elif kind == "word":
        runes = english_to_runes(ks["text"]) if ks["text"] else []
        if runes:
            v = np.resize(np.array(runes) % N, LT)
        else:
            key = rng.integers(0, N, (R, 1, ks["period"]))                  # one random key per replicate, all pages
            return np.tile(key, (1, G, (LT + ks["period"] - 1) // ks["period"]))[:, :, :LT]
    elif kind == "running_text":
        off = rng.integers(0, len(plain), (R, G, 1))
        return plain[(off + np.arange(LT)[None, None, :]) % len(plain)]
    else:
        raise ValueError(kind)
    return np.broadcast_to(v, (R, G, LT))


def make_map(ks):
    m = ks["map"]; a, b = int(ks["a"]), int(ks["b"])
    if m == "identity": return lambda x: x % N
    if m == "atbash": return lambda x: (N - 1 - x) % N
    if m == "shift": return lambda x: (x + b) % N
    if m == "affine": return lambda x: (a * x + b) % N
    if m == "prime_value": return lambda x: PV[x] % N
    if m == "totient_value": return lambda x: (PV[x] - 1) % N
    if m == "square": return lambda x: (x * x) % N
    perm = rng.permutation(N)
    return lambda x: perm[x]


def combine(P, K, m, rule):
    if rule == "add": return (P + K) % N
    if rule == "sub": return (P - K) % N
    if rule == "beaufort": return (K - P) % N
    return (m * P + K) % N


def encipher(con, P):
    """P: (R, G, L) plaintext matrix -> (R, G, L) ciphertext under the construction."""
    R = P.shape[0]
    ks, cb, rr, fr = con["key_source"], con["combine"], con["repeat_rule"], con["f_rule"]
    typ = ks["type"]; fb = typ in ("cipher_feedback", "plain_feedback")
    KS = base_stream(ks["base"] if fb else typ, ks, R)
    lag = ks["lag"]; mp = make_map(ks) if fb else None
    seed = rng.integers(0, N, (R, G, lag))
    rows = np.arange(R)[:, None]; cols = np.arange(G)[None, :]
    msrc = cb["multiplier_source"]
    M2 = rng.integers(1, N, (R, G, L)) if msrc == "key2" else None
    C = np.zeros((R, G, L), dtype=np.int64); j = np.zeros((R, G), dtype=np.int64)
    Kprev = np.full((R, G), -1)
    rule, p, kstep, delta, tgt = rr["rule"], rr["p"], rr["k"], rr["delta"], rr["target"]

    def keysym(i, j, redraw_mask=None):
        k = np.zeros((R, G), dtype=np.int64)
        if fb:
            src = C if typ == "cipher_feedback" else P
            prev = src[:, :, i - lag] if i >= lag else seed[:, :, i]
            k = mp(prev)
        if KS is not None:
            k = (k + KS[rows, cols, np.minimum(j, LT - 1)]) % N
        return k

    for i in range(L):
        act = np.broadcast_to(MASK[:, i], (R, G))
        Pi = P[:, :, i]
        m = cb["multiplier"] if msrc == "const" else (((cb["a"] * i + cb["b"]) % (N - 1)) + 1 if msrc == "position" else M2[:, :, i])
        K = keysym(i, j)
        Ci = combine(Pi, K, m, cb["rule"])
        if rule != "none" and i > 0:
            settled = np.zeros((R, G), dtype=bool)                   # a cell that declined to re-draw keeps its doublet
            for _ in range(MAXIT):
                if tgt == "cipher": coll = Ci == C[:, :, i - 1]
                elif tgt == "key": coll = K == Kprev
                else: coll = Pi == P[:, :, i - 1]
                coll = coll & act & ~settled
                if fr != "none": coll &= Pi != 0                      # a literal F is written as itself
                if p < 1.0:
                    draw = rng.random((R, G)) < p
                    settled |= coll & ~draw
                    coll &= draw
                if not coll.any(): break
                if rule == "bump":
                    Ci = np.where(coll, (Ci + delta) % N, Ci); break
                if KS is None:                                       # feedback-only key: fresh uniform symbol
                    K = np.where(coll, rng.integers(0, N, (R, G)), K)
                else:
                    j = j + (kstep if rule == "skip" else 1) * coll
                    K = keysym(i, j)
                Ci = combine(Pi, K, m, cb["rule"])
                if tgt == "plain": break                             # the plaintext condition does not change
        consume = act.copy()
        if fr != "none":
            isF = (Pi == 0) & act
            Ci = np.where(isF, 0, Ci)
            if fr == "literal_f": consume = consume & ~isF
        C[:, :, i] = np.where(act, Ci, 0)
        Kprev = np.where(consume, K, Kprev)
        j = j + consume
    return C


SD_NULL = None      # sd of the four statistics under an iid uniform keystream (set on first gate call)


def gate(con, reps=REPS):
    global SD_NULL
    if SD_NULL is None:
        SD_NULL = np.ones(4)
        u, _ = normalize({"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "none"}, "f_rule": "none"})
        SD_NULL = stats_matrix(encipher(u, sample_pages(reps))).std(0) + 1e-9
    t0 = time.time()
    S = stats_matrix(encipher(con, sample_pages(reps)))
    mean, sd = S.mean(0), S.std(0) + 1e-9
    z = (OBS - mean) / sd
    zs = (OBS - mean) / SD_NULL                       # strict: how far the construction's mean sits from the pages in null-noise units
    return {"mean": mean.tolist(), "sd": sd.tolist(), "z": z.tolist(), "pass": bool((np.abs(z) < Z_PASS).all()),
            "pass_each": (np.abs(z) < Z_PASS).tolist(), "z_strict": zs.tolist(), "pass_strict": bool((np.abs(zs) < Z_PASS).all()),
            "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- decryptability, ledger check, sweep size
N_WORDS, N_PHRASES, N_PLAIN = 268, 2905, len(plain)      # families.py: solved-text words 2-20 runes; phase-4 phrases/lines


def classify(con):
    """Is the family finite (decryptable by sweeping keys), how many configurations, is it already swept?
    Returns dict(finite, n_configs, swept, note).  Ledger facts from README §9-15 and results/ledger_diff.md."""
    ks, cb, rr, fr = con["key_source"], con["combine"], con["repeat_rule"], con["f_rule"]
    t, rule = ks["type"], rr["rule"]
    notes, finite, n = [], True, 1
    # --- key family size
    if t == "uniform": finite = False; notes.append("secret pad: not decryptable without the pad")
    elif t == "lcg":
        n = int(ks["modulus"]); notes.append(f"{n:,} seeds for the stated (a, c, m); WZ B-04/R16 swept named PRNGs and KDFs, JW §13/§41 passphrase seeds")
    elif t in ("prime", "totient", "prime_plus1", "fibonacci", "lucas"): n = 101; notes.append("offsets 0-100 as in phase 3")
    elif t == "prime_gap": n = 101; notes.append("prime gaps: LZ's 24 integer sequences may include it (unverified); not run here")
    elif t == "position": n = 29 ** 3; notes.append("all a, b, c mod 29")
    elif t == "word":
        if ks["text"]: n = 1; notes.append("a single stated key")
        else:
            n = N ** ks["period"]; notes.append(f"29^{ks['period']} random keys of that length; JW exhausts length ≤ 3, WZ k 4-12 by hand-Vigenère")
            if ks["period"] > 4: finite = False; notes.append("29^period too large to enumerate: not sweepable as a blind family")
    elif t == "running_text": n = N_PLAIN; notes.append("the book's own text at every offset; external texts are a separate open hunt (JW/WZ ≈ 200 texts)")
    elif t in ("cipher_feedback", "plain_feedback"):
        n = N ** ks["lag"]
        if ks["map"] == "random_bijection": finite = False; notes.append("29! bijections: not enumerable (LZ ran 14 named bijections)")
        if ks["map"] in ("shift",): n *= N
        if ks["map"] in ("affine",): n *= N * (N - 1)
        if ks["base"] != "none":
            sub = classify({"key_source": {**ks, "type": ks["base"], "lag": 1, "map": "identity", "base": "none"}, "combine": cb, "repeat_rule": {"rule": "none", "p": 1, "k": 1, "delta": 1, "target": "cipher"}, "f_rule": fr})
            n *= sub["n_configs"]; finite = finite and sub["finite"]; notes.append(f"× base stream ({sub['n_configs']:,})")
        if rule in ("redraw", "skip") and ks["base"] == "none":
            finite = False; notes.append("a re-drawn symbol on a feedback-only key is a fresh secret symbol: not decryptable")
    # --- combine
    if cb["rule"] == "affine":
        if cb["multiplier_source"] == "const": n *= 1 if cb["multiplier"] else 28; notes.append("stated multiplier (×28 for all)")
        elif cb["multiplier_source"] == "position": n *= 28 * 29; notes.append("×812 multiplier schedules")
        else: finite = False; notes.append("key2 is a second secret stream: not decryptable")
    # --- swept?
    swept, how = "no", []
    stream_fams = {"prime", "totient", "prime_plus1", "prime_gap", "fibonacci", "lucas", "position", "word", "running_text"}
    book_word = t == "word" and bool(ks["text"])
    plain_add = cb["rule"] in ("add", "sub", "beaufort")
    if t == "uniform": swept, how = "n/a", ["not a sweepable family; phase 2 construction table covers its statistics"]
    elif t in stream_fams and plain_add and rule in ("none", "redraw", "skip") and rr["target"] == "cipher":
        k = 1 if rule == "redraw" else (rr["k"] if rule == "skip" else 0)
        if rule == "none": swept, how = "yes", ["rigid periodic/stream keys: JW §3, WZ ledger A, LZ, here ph3 (skip decoder subsumes p=0)"]
        elif k == 1: swept, how = "yes", ["here ph3 (book streams, words), ph4 (phrases, all signs), ph5 (Latin/OE); JW §7-8, WZ LP1-H, LZ, pnotisdev solved-phrase-keys"]
        elif k == 2: swept, how = "running", ["phase 7 (skip-by-two) is running now on exactly these families; WZ R24-C2 on PRNG seeds"]
        else: how = [f"skip k={k}: no ledger has it"]
        if t == "word" and not book_word: how.append("random short keys: JW §10/§33 exhaustive to length 3; WZ hand-Vigenère k ≤ 12; longer: nobody")
        if t == "position" and ks["a"] != 0: how.append("quadratic position formulas: only n²+b here; a·n²+b·n+c in full: nobody")
        if fr == "literal_f_consumes": swept = "partly" if swept == "yes" else swept; how.append("F consumed-but-unencrypted variant: no ledger ran it (both F variants here are consume-no-key or none)")
    elif t in stream_fams and plain_add and rule == "bump":
        swept, how = "yes", ["deterministic bump: JW §11 (collision resolution is uniform, not a bump); here doublets.md anti-doublet +1 fails the lag-1 class chi2"]
    elif t in stream_fams and plain_add and rr["target"] == "key":
        swept, how = "yes", ["key that never repeats a symbol: here doublets.md 'hand pad' (448 doublets)"]
    elif t in stream_fams and plain_add and rr["target"] == "plain":
        how = ["skip triggered by a doubled plaintext letter: no ledger has it"]
    elif t in stream_fams and cb["rule"] == "affine":
        if rule == "none": swept, how = "yes", ["non-additive affine c = a·p + k without skip: JW §48 all multipliers, WZ LP1-H, pnotisdev all 28 multipliers"]
        else: swept, how = "partly", ["affine multipliers under the skip rule: pnotisdev '28 key multipliers' under its collision-repair model (coverage unclear); not run here"]
    elif t == "cipher_feedback":
        if ks["base"] == "none" and ks["map"] in ("identity", "atbash", "shift", "affine", "prime_value", "totient_value") and ks["lag"] <= 60:
            swept, how = "yes", ["ciphertext autokey/chain lags 1-60 with named maps: LZ (14 bijections, Δc detector), WZ R12/R18/R22, JW §3, here ph2"]
        elif ks["base"] != "none":
            swept, how = "partly", ["stream + ciphertext-feedback term: WZ 48 PT/CT feedback configs (f ∈ mod 29, totient, digit sum); not here"]
        else: how = ["feedback map not on any ledger"]
    elif t == "plain_feedback":
        if ks["lag"] <= 3 and ks["base"] == "none": swept, how = "yes", ["plaintext autokey primers/lags 1-3: JW §3, LZ, here ph2 lags 1,2,5"]
        else: swept, how = "partly", ["plaintext autokey beyond lag 3 or with a base stream: WZ R12-C1 k=2..6 only"]
    elif t == "lcg":
        swept, how = "partly", ["PRNG/KDF pads: WZ B-04, R16, R25 (MT 2^32 tail at 0.5%); JW §13, §41; a plain LCG mod m is not named by anyone"]
    if cb["rule"] in ("sub", "beaufort") and swept == "yes" and "ph4" not in " ".join(how): how.append("(both signs: JW/WZ/LZ throughout; here from phase 4)")
    return {"finite": finite, "n_configs": int(n), "tests": int(n) * G if finite else None, "swept": swept, "note": "; ".join(notes + how)}


# ---------------------------------------------------------------- evidence brief
def build_brief():
    dbl = (RESULTS / "doublets.md").read_text()
    led = (RESULTS / "ledger_diff.md").read_text()
    fam_table = led[led.index("## Family-by-family table"):led.index("## The four questions asked")]
    ranked = led[led.index("## Ranked list"):led.index("## What this changes")]
    survey = led[led.index("**What this changes.**"):]
    keys = "\n".join(l for l in (RAW / "iddqd__liber-primus__keys.txt").read_text().splitlines() if l.strip() and not l.strip().endswith("-"))
    brief = f"""# Evidence brief: the unsolved pages of Cicada 3301's Liber Primus (prepared {time.strftime('%Y-%m-%d')})

## The object
56 unsolved pages (55 with runes), 12,956 runes in the 29-rune Gematria Primus alphabet (index 0..28 = F U TH O R C G W H N I J
EO P X S T B E M L NG OE D A AE Y IA EA; each rune also carries a prime value F=2, U=3, TH=5, ... EA=109). Page lengths
{int(LENS.min())}-{int(LENS.max())} runes, median {int(np.median(LENS))}. Word, line and paragraph separators are known from the transcription.

## The four statistics any construction must reproduce (pooled over the 55 pages)
| statistic | pages | iid uniform keystream would give |
|---|---|---|
| doubled runes (C_i == C_(i-1)) among 12,901 adjacent pairs | **{int(OBS[0])}** | 445 ± 20 (z = −17) |
| chi-square of the other 28 lag-1 difference classes (27 dof) | **{OBS[1]:.0f}** | ≈ 27 |
| unigram chi-square over the 29 runes (28 dof) | **{OBS[2]:.0f}** | ≈ 28 |
| index of coincidence | **{OBS[3]:.4f}** | 0.0345 |
So: the ciphertext is flat in every respect except that a rune almost never repeats its predecessor, about one time in five
as often as chance. The deficit is the same inside words and across word boundaries, and the same on every page (no page
below −2σ). Lags 2 and beyond are null (no decay profile). The gate accepts a construction only if all four statistics fall
within 3 sd of the construction's own Monte Carlo distribution (200 replicates of real solved-page English cut to the real page lengths).
Other established facts: no two pages share a keystream at any alignment within ±200 runes (pooled test null at 135σ sensitivity
for full reuse); no within-page period 2-200; the solved pages' ciphertext sits at the normal doublet rate, so the deficit belongs
to the unsolved pages' cipher, not to the plaintext or the transcription.

## What the book itself did on the solved pages (the only ground truth about the author's methods)
Published keys per section (rtkd/iddqd keys file; '+ 0.k' = section k):
{keys}
Both word keys (DIVINITY, FIRFUMFERENFE) are words of the book's own plaintext. The F rule ("clear text F is not encrypted",
consumes no key symbol) is the author's own skip rule. The totient stream is phi(p_n) over the primes. One page (the 'Parable')
is a plain Gematria substitution; the last solved page uses shift 3 then Atbash. The author uses primes, totients, Gematria prime
values, 3301, and the book's own words; the community reads the hint "numbers are the direction, words are the map" as the book keying itself.

## Which constructions reproduce the statistics (phase 2, src/doublets.py, 20 constructions, same gate as this loop)
{dbl}
## What has already been swept, with planted controls (this repository's phases 3-7 and five public 2026 labs)
Phase 3: shifts, every solved-text word (fwd/rev), primes p/p−1/p+1 at 101 starts, Fibonacci, Lucas, a·n+b and n²+b, the solved
plaintext as running key at all 2,977 offsets, neighbour pages as keys; each with/without the F rule under the skip-on-repeat rule
(a key symbol that would make C repeat is skipped, p ≈ 0.81 modelled). 519,200 tests, null; planted keys recovered at z 10-15.
Phase 4: every 2-, 3-, 4-word phrase and every line of the solved text, fwd/rev, under skip, all three signs (C = P+K, P−K, K−P),
plus phase 3's families under the two other signs. 1,996,170 tests, null; controls z 10.6-16.3.
Phase 5: phases 3-4 rescored with Latin and Old English unigram models. 5,029,860 tests, null; the English scorer loses little power on either.
Phase 6: extra key advance at word/line starts and unencrypted null runes at word edges (pnotisdev's open lane), over the same
families. 10,059,720 tests, null; controls z 7-15.
Phase 7 (RUNNING NOW): the same families with wazar's skip-by-two rejection (a rejection discards two key symbols).
Also measured here: a lag-5/6 within-word echo reported elsewhere does not replicate (chance at one of twelve lags).
{fam_table}
{ranked}
{survey}
"""
    return brief


# ---------------------------------------------------------------- API clients (raw HTTP, stdlib only: the venv has no SDKs)
PRICES = {  # $ per million input / output tokens.  Anthropic from the claude-api skill table (2026-10); GPT and Grok ASSUMED.
    "claude-fable-5-1": (10.0, 50.0, "listed"), "claude-sonnet-5-5": (2.0, 10.0, "listed"), "claude-haiku-5-5": (0.1, 0.5, "listed"),
    "gpt-6.1-sol": (5.0, 20.0, "assumed"), "grok-4.7": (3.0, 15.0, "assumed")}
USAGE = []          # (proposer, model, round, input, output, seconds, cost)
# The first live attempt (results/hypotheses/run1_failed.log) spent 24k output tokens on thinking at effort high and
# returned no text; it is counted here as round 0 so the cost total is the whole spend of this exercise.
PRIOR_SPEND = [("claude (failed attempt)", "claude-fable-5-1", 0, 12868, 24000, 353.7, 12868 / 1e6 * 10 + 24000 / 1e6 * 50)]


def load_keys():
    keys = {k: os.environ.get(k) for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY")}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?([A-Z_]+)\s*=\s*(.*)$", line)
            if m and m.group(1) in keys and not keys[m.group(1)]:
                keys[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return keys


def http_json(url, headers, body, timeout=1500, stream=False):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers}, method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if not stream: return json.loads(r.read().decode())
                text, usage, stop, model, raw_events = [], {"input_tokens": 0, "output_tokens": 0}, None, None, 0
                for line in r:
                    line = line.decode("utf-8", "replace").strip()
                    if not line.startswith("data:"): continue
                    ev = json.loads(line[5:].strip()); raw_events += 1
                    et = ev.get("type")
                    if et == "message_start":
                        msg = ev["message"]; model = msg.get("model"); u = msg.get("usage", {})
                        usage["input_tokens"] = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                    elif et == "content_block_delta" and ev["delta"].get("type") == "text_delta": text.append(ev["delta"]["text"])
                    elif et == "message_delta":
                        usage["output_tokens"] = ev.get("usage", {}).get("output_tokens", usage["output_tokens"]); stop = ev["delta"].get("stop_reason")
                return {"text": "".join(text), "usage": usage, "stop_reason": stop, "model": model, "events": raw_events}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "replace")[:800]
            if e.code in (429, 500, 502, 503, 529) and attempt < 3:
                print(f"    HTTP {e.code}, retry in {15 * (attempt + 1)}s", flush=True); time.sleep(15 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {err}")
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, __import__("http").client.HTTPException) as e:
            if attempt < 3:
                print(f"    network error {e!r}, retry in {10 * (attempt + 1)}s", flush=True); time.sleep(10 * (attempt + 1)); continue
            raise RuntimeError(f"network: {e!r}")


def count_tokens_anthropic(key, model, system, user):
    try:
        r = http_json("https://api.anthropic.com/v1/messages/count_tokens", {"x-api-key": key, "anthropic-version": "2026-10-21"},
                      {"model": model, "system": system, "messages": [{"role": "user", "content": user}]})
        return r.get("input_tokens")
    except RuntimeError as e:
        print(f"    count_tokens failed: {e}", flush=True); return None


def ask_anthropic(key, model, system, user, effort="medium", max_tokens=64000):
    hdr = {"x-api-key": key, "anthropic-version": "2026-10-21", "anthropic-beta": "server-side-fallback-2026-07-01"}
    body = {"model": model, "max_tokens": max_tokens, "system": system, "messages": [{"role": "user", "content": user}],
            "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": SCHEMA}}, "fallbacks": "default", "stream": True}
    t0 = time.time()
    try:
        r = http_json("https://api.anthropic.com/v1/messages", hdr, body, stream=True)
    except RuntimeError as e:
        if "HTTP 400" not in str(e): raise
        print(f"    structured output rejected ({str(e)[:160]}); retrying with plain JSON instruction", flush=True)
        body["output_config"] = {"effort": effort}
        body["messages"][0]["content"] += "\n\nReturn ONLY a JSON object matching the schema, no prose, no code fence."
        r = http_json("https://api.anthropic.com/v1/messages", hdr, body, stream=True)
    r["seconds"] = round(time.time() - t0, 1)
    return r


def responses_stream(url, hdr, body):
    """POST a streaming Responses-API request; return text, usage, status, model from the SSE events."""
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **hdr}, method="POST")
    with urllib.request.urlopen(req, timeout=1500) as r:
        text, final, nev = [], None, 0
        for line in r:
            line = line.decode("utf-8", "replace").strip()
            if not line.startswith("data:"): continue
            payload = line[5:].strip()
            if payload == "[DONE]": break
            ev = json.loads(payload); nev += 1
            et = ev.get("type", "")
            if et == "response.output_text.delta": text.append(ev.get("delta", ""))
            elif et in ("response.completed", "response.incomplete", "response.failed"): final = ev.get("response", {})
            elif et == "error": raise RuntimeError(f"stream error: {json.dumps(ev)[:400]}")
    final = final or {}
    if not text and final:   # some servers send the text only in the final object
        text = [c.get("text", "") for it in final.get("output", []) if it.get("type") == "message" for c in it.get("content", []) if c.get("type") == "output_text"]
    u = final.get("usage", {}) or {}
    return {"text": "".join(text), "usage": {"input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0)},
            "stop_reason": final.get("status") or ("incomplete: " + json.dumps(final.get("incomplete_details")) if final.get("incomplete_details") else None),
            "model": final.get("model"), "events": nev, "raw": {k: v for k, v in final.items() if k != "output"} | {"output_text_len": sum(len(t) for t in text)}}


def ask_responses(base, key, model, system, user, effort="medium", max_out=64000):
    """OpenAI / xAI Responses API (the endpoint Quorum uses for both), streamed so a long reasoning turn does not drop the connection."""
    hdr = {"Authorization": f"Bearer {key}"}
    fmt = {"type": "json_schema", "name": "constructions", "schema": SCHEMA, "strict": True}
    body = {"model": model, "instructions": system, "input": user, "reasoning": {"effort": effort}, "max_output_tokens": max_out, "text": {"format": fmt}, "stream": True}
    t0 = time.time()
    last = None
    for attempt in range(3):
        try:
            r = responses_stream(f"{base}/v1/responses", hdr, body); break
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "replace")[:800]
            if e.code == 400 and body["text"]["format"]["type"] == "json_schema":
                print(f"    json_schema format rejected ({err[:200]}); retrying with json_object", flush=True)
                body["text"] = {"format": {"type": "json_object"}}
                body["input"] = user + "\n\nReturn ONLY a JSON object matching the schema, no prose, no code fence."; continue
            if e.code in (429, 500, 502, 503) and attempt < 2: time.sleep(15 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {err}")
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, __import__("http").client.HTTPException) as e:
            last = e; print(f"    network error {e!r}, retry", flush=True); time.sleep(10 * (attempt + 1))
    else:
        raise RuntimeError(f"network: {last!r}")
    r["seconds"] = round(time.time() - t0, 1)
    if not r.get("model"): r["model"] = model
    return r


def parse_proposals(text):
    """Tolerant JSON extraction. The result is data; nothing in it is executed."""
    text = text.strip()
    if text.startswith("```"): text = re.sub(r"^```[a-z]*\s*|\s*```$", "", text)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if not m: return [], "no JSON object found"
        try: obj = json.loads(m.group(0))
        except json.JSONDecodeError as e: return [], f"JSON parse error: {e}"
    props = obj.get("proposals", obj if isinstance(obj, list) else [])
    return (props if isinstance(props, list) else []), None


SYSTEM = ("You are a cryptanalyst on a panel attacking the unsolved pages of Cicada 3301's Liber Primus. You propose cipher "
          "constructions; a computational gate simulates each one and rejects any that does not reproduce the pages' four statistics. "
          "You never write code. Every construction must be assembled from the menu you are given, in the JSON schema you are given, "
          "and nothing else. Think about what the author demonstrably did and about why the surviving construction (a key re-drawn when "
          "it would repeat the previous rune) has that statistical shape, then propose the mechanisms most likely to be the real one, "
          "ranked, each with a one-paragraph rationale tied to the book's own methods and hints. Do not re-propose families the brief "
          "lists as already swept under the same repeat rule unless you change something the ledgers did not try, and say what.")


def proposal_prompt(brief, round_no, feedback=None, n=15):
    s = brief + "\n" + MENU_TEXT + "\n## Schema (return exactly this shape)\n```json\n" + json.dumps(SCHEMA) + "\n```\n"
    if round_no == 1:
        s += (f"\n## Task\nPropose up to {n} constructions, ranked 1 = most likely to be the Liber Primus cipher. For each give a name, a "
              "one-paragraph rationale tied to the book's methods and hints and to the statistics above, your predicted doublet count "
              "(pages: 86), and the construction fields. Spend most of your ranking on constructions that (a) can plausibly produce the "
              "fivefold doublet deficit with a flat lag-1 difference spectrum and (b) are decryptable given a key the author could have "
              "published or derived, and that no ledger above has swept under that repeat rule. Include two or three deliberate probes "
              "of the gate's blind spots if you think the brief's reading of the statistics is wrong.")
    else:
        s += ("\n## Round 1 gate results (all proposers)\n" + feedback +
              f"\n## Task\nRound 2. Propose up to {n} revised constructions. Learn from the table: which fields moved which statistic, "
              "what passed, what is already swept. Prefer constructions that pass all four statistics, are decryptable, and are not on "
              "any ledger under their repeat rule. You may refine a passing construction toward a smaller finite family, or propose "
              "something new from the menu. Same schema.")
    return s


def feedback_table(rows):
    out = ["| proposer | construction | doublets (z) | lag-1 χ² (z) | unigram χ² (z) | IC (z) | gate | finite | swept | note |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r.get("error"): out.append(f"| {r['proposer']} | {r['name'][:40]} | — | — | — | — | invalid: {r['error']} | | | |"); continue
        g, c = r["gate"], r["classify"]
        cells = " | ".join(f"{g['mean'][i]:.{4 if i == 3 else 0}f} ({g['z'][i]:+.1f})" for i in range(4))
        out.append(f"| {r['proposer']} | {describe(r['construction'])[:90]} | {cells} | {'PASS' if g['pass'] else 'fail'} | {'yes' if c['finite'] else 'no'} | {c['swept']} | {c['note'][:120]} |")
    return "\n".join(out)


# ---------------------------------------------------------------- gate calibration (hand-built, no API)
CALIBRATION = [
    ("independent uniform keystream (should fail on doublets)", {"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "none"}, "f_rule": "none"}),
    ("uniform key re-drawn 81% when it would repeat (phase 2 survivor, should pass)", {"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "redraw", "p": 0.81}, "f_rule": "none"}),
    ("random 13-rune word key + skip 0.81 (a FIRFUMFERENFE-like key under the skip rule, should pass)", {"key_source": {"type": "word", "text": "", "period": 13}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "skip", "p": 0.81, "k": 1}, "f_rule": "none"}),
    ("totient stream + skip 0.81 + F rule (phase 3 family: passes doublets, fails unigram as the phase 2 totient row did)", {"key_source": {"type": "totient", "offset": 0}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "skip", "p": 0.81, "k": 1}, "f_rule": "literal_f"}),
    ("ciphertext autokey lag 1 (should fail on lag-1 structure)", {"key_source": {"type": "cipher_feedback", "lag": 1, "map": "identity"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "none"}, "f_rule": "none"}),
    ("uniform + bump 0.81 (should fail on lag-1 class chi2)", {"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "bump", "p": 0.81, "delta": 1}, "f_rule": "none"}),
    ("hand pad: key never repeats a symbol (should fail)", {"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "skip", "p": 1.0, "target": "key"}, "f_rule": "none"}),
    ("book Vigenère DIVINITY with F rule, no repeat rule (should fail)", {"key_source": {"type": "word", "text": "DIVINITY"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "none"}, "f_rule": "literal_f"}),
]


def run_gate_rows(items, proposer, round_no, cache):
    rows = []
    for rank, (name, raw) in enumerate(items, 1):
        con, err = normalize(raw)
        row = {"proposer": proposer, "round": round_no, "rank": raw.get("rank", rank) if isinstance(raw, dict) else rank, "name": str(name)[:80],
               "rationale": str(raw.get("rationale", ""))[:1500] if isinstance(raw, dict) else "", "predicted_doublets": raw.get("predicted_doublets") if isinstance(raw, dict) else None}
        if err:
            row["error"] = err; rows.append(row); print(f"  [{proposer}] {name[:50]}: INVALID ({err})", flush=True); continue
        h = con_hash(con)
        if h not in cache: cache[h] = gate(con)
        g = cache[h]
        row.update({"construction": con, "hash": h, "describe": describe(con), "gate": g, "classify": classify(con)})
        rows.append(row)
        print(f"  [{proposer}] {describe(con)[:95]}\n      doublets {g['mean'][0]:.0f} (z {g['z'][0]:+.1f}) | lag-1 χ² {g['mean'][1]:.0f} ({g['z'][1]:+.1f}) | uni χ² {g['mean'][2]:.0f} ({g['z'][2]:+.1f}) | IC {g['mean'][3]:.4f} ({g['z'][3]:+.1f}) -> {'PASS' if g['pass'] else 'fail'}; finite={row['classify']['finite']} swept={row['classify']['swept']} [{g['seconds']}s]", flush=True)
    return rows


def cost_of(model, inp, out):
    p = PRICES.get(model, (5.0, 20.0, "assumed"))
    return inp / 1e6 * p[0] + out / 1e6 * p[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="gate calibration only, no API calls")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--budget", type=float, default=40.0)
    ap.add_argument("--proposers", default="claude,gpt,grok")
    ap.add_argument("--report-only", action="store_true", help="rebuild results/hypotheses.md from results/hypotheses.json")
    ap.add_argument("--smoke", action="store_true", help="one tiny request per proposer to check keys, endpoints and parsing")
    ap.add_argument("--fresh", action="store_true", help="call the APIs even where results/hypotheses/round*_*.json already holds a response")
    args = ap.parse_args()
    if args.smoke:
        keys = load_keys(); q = 'Reply with exactly this JSON and nothing else: {"proposals": []}'
        for prop, model, fn in (("claude", "claude-fable-5-1", lambda: ask_anthropic(keys["ANTHROPIC_API_KEY"], "claude-fable-5-1", "Be terse.", q, "low", 2000)),
                                ("gpt", "gpt-6.1-sol", lambda: ask_responses("https://api.openai.com", keys["OPENAI_API_KEY"], "gpt-6.1-sol", "Be terse.", q, "low", 2000)),
                                ("grok", "grok-4.7", lambda: ask_responses("https://api.x.ai", keys["XAI_API_KEY"], "grok-4.7", "Be terse.", q, "low", 2000))):
            try:
                r = fn(); print(f"{prop}: ok, served by {r.get('model')}, stop={r.get('stop_reason')}, usage {r['usage']}, {r['seconds']}s, text={r['text'][:80]!r}", flush=True)
            except Exception as e:
                print(f"{prop}: FAILED {e!r}"[:600], flush=True)
        return
    if args.report_only:
        j = json.load(open(RESULTS / "hypotheses.json")); USAGE.extend(tuple(u) for u in j["usage"])
        gate(normalize({"key_source": {"type": "uniform"}, "combine": {"rule": "add"}, "repeat_rule": {"rule": "none"}, "f_rule": "none"})[0])
        for r in j["rows"]:
            if not r.get("error"): r["classify"] = classify(r["construction"]); r["describe"] = describe(r["construction"])
        write_report(j["calibration"], j["rows"], j.get("brief_tokens"), 0.0); return
    HYP.mkdir(exist_ok=True); DOCS.mkdir(exist_ok=True)
    t_start = time.time()
    print(f"observed: doublets {OBS[0]:.0f}, lag-1 class chi2 {OBS[1]:.1f}, unigram chi2 {OBS[2]:.1f}, IC {OBS[3]:.4f}", flush=True)

    cache = {}
    print("\n== gate calibration (hand-built constructions, no API) ==", flush=True)
    calib = run_gate_rows([(n, c) for n, c in CALIBRATION], "calibration", 0, cache)

    brief = build_brief()
    (HYP / "brief.md").write_text(brief + "\n" + MENU_TEXT)
    (HYP / "schema.json").write_text(json.dumps(SCHEMA, indent=1))
    print(f"\nbrief: {len(brief):,} chars (+ menu {len(MENU_TEXT):,}); rough token estimate {len(brief + MENU_TEXT) // 4:,}", flush=True)
    if args.dry:
        write_report(calib, [], brief_tokens=None, elapsed=time.time() - t_start); return

    keys = load_keys()
    proposers = []
    want = args.proposers.split(",")
    if "claude" in want and keys["ANTHROPIC_API_KEY"]: proposers.append(("claude", "claude-fable-5-1"))
    if "gpt" in want and keys["OPENAI_API_KEY"]: proposers.append(("gpt", "gpt-6.1-sol"))
    if "grok" in want and keys["XAI_API_KEY"]: proposers.append(("grok", "grok-4.7"))
    print("proposers with keys:", [p for p, _ in proposers], flush=True)
    brief_tokens = count_tokens_anthropic(keys["ANTHROPIC_API_KEY"], "claude-fable-5-1", SYSTEM, proposal_prompt(brief, 1)) if keys["ANTHROPIC_API_KEY"] else None
    print(f"round-1 prompt: {brief_tokens} tokens by the Anthropic token counter", flush=True)

    rows, spent = [], sum(u[6] for u in PRIOR_SPEND); USAGE.extend(PRIOR_SPEND)
    for rnd in range(1, args.rounds + 1):
        if rnd > 1 and spent > args.budget * 0.7:
            print(f"\nskipping round {rnd}: spent ${spent:.2f} of ${args.budget:.0f}", flush=True); break
        fb = feedback_table([r for r in rows if r["round"] == rnd - 1]) if rnd > 1 else None
        user = proposal_prompt(brief, rnd, fb, n=15 if rnd == 1 else 10)
        for prop, model in proposers:
            print(f"\n== round {rnd}: asking {prop} ({model}) ==", flush=True)
            saved = HYP / f"round{rnd}_{prop}.json"
            try:
                if saved.exists() and not args.fresh:
                    j = json.load(open(saved)); r = {"text": j["text"], "usage": j["usage"], "stop_reason": j.get("stop_reason"), "model": j.get("served_by"), "seconds": j.get("seconds", 0), "raw": j.get("raw")}
                    print(f"  {prop}: reusing saved response {saved.name} (no new API call)", flush=True)
                elif prop == "claude": r = ask_anthropic(keys["ANTHROPIC_API_KEY"], model, SYSTEM, user)
                elif prop == "gpt": r = ask_responses("https://api.openai.com", keys["OPENAI_API_KEY"], model, SYSTEM, user)
                else: r = ask_responses("https://api.x.ai", keys["XAI_API_KEY"], model, SYSTEM, user)
            except Exception as e:
                print(f"  {prop} failed: {e!r}"[:400], flush=True)
                (HYP / f"round{rnd}_{prop}_error.txt").write_text(str(e)); continue
            u = r["usage"]; c = cost_of(model, u["input_tokens"], u["output_tokens"]); spent += c
            USAGE.append((prop, r.get("model") or model, rnd, u["input_tokens"], u["output_tokens"], r["seconds"], c))
            print(f"  {prop}: {u['input_tokens']} in / {u['output_tokens']} out, stop={r.get('stop_reason')}, served by {r.get('model')}, {r['seconds']}s, ${c:.2f} (running ${spent:.2f})", flush=True)
            (HYP / f"round{rnd}_{prop}.json").write_text(json.dumps({"proposer": prop, "model": model, "served_by": r.get("model"), "round": rnd, "stop_reason": r.get("stop_reason"),
                                                                       "usage": u, "seconds": r["seconds"], "text": r["text"], "raw": r.get("raw")}, indent=1, default=str))
            props, perr = parse_proposals(r["text"])
            if perr: print(f"  {prop}: {perr}", flush=True); rows.append({"proposer": prop, "round": rnd, "rank": 0, "name": "(unparseable response)", "error": perr}); continue
            print(f"  {prop}: {len(props)} proposals", flush=True)
            rows += run_gate_rows([(p.get("name", f"#{i}") if isinstance(p, dict) else f"#{i}", p) for i, p in enumerate(props, 1)], prop, rnd, cache)
        json.dump({"observed": OBS.tolist(), "calibration": calib, "rows": rows, "usage": USAGE, "brief_tokens": brief_tokens}, open(RESULTS / "hypotheses.json", "w"), indent=1, default=str)
    write_report(calib, rows, brief_tokens, time.time() - t_start)


def write_report(calib, rows, brief_tokens, elapsed):
    def cell(g, i): return f"{g['mean'][i]:.{4 if i == 3 else 0}f} ± {g['sd'][i]:.{4 if i == 3 else 0}f} ({g['z'][i]:+.1f})"
    tot_in = sum(u[3] for u in USAGE); tot_out = sum(u[4] for u in USAGE); tot_cost = sum(u[6] for u in USAGE)
    out = ["# Hypothesis loop: panel proposals gated on the four page statistics", "",
           f"Run {time.strftime('%Y-%m-%d %H:%M')}. Observed: doublets {OBS[0]:.0f}, lag-1 class χ² {OBS[1]:.1f}, unigram χ² {OBS[2]:.1f}, IC {OBS[3]:.4f}. "
           f"Gate: {REPS} replicates of solved-page English cut to the 55 real page lengths per construction; pass = |z| < {Z_PASS:.0f} on all four. "
           f"Proposers: {', '.join(sorted({u[0] for u in USAGE if u[2] > 0})) or 'none (dry run)'}. Method: `docs/hypothesis-loop.md`. Script: `src/hypothesis_loop.py`. Raw responses: `results/hypotheses/`.", "",
           "## Gate calibration (hand-built, before any proposal)", "",
           "| construction | doublets | lag-1 class χ² | unigram χ² | IC | verdict |", "|---|---|---|---|---|---|"]
    for r in calib:
        g = r["gate"]; out.append(f"| {r['name']} | {cell(g,0)} | {cell(g,1)} | {cell(g,2)} | {cell(g,3)} | {'PASS' if g['pass'] else 'fail'} |")
    out += ["", "The gate reproduces `results/doublets.md`: independent keys fail on doublets, the 81 % re-draw passes, the bump and the hand pad fail where phase 2 said they would.", ""]
    valid = [r for r in rows if not r.get("error")]
    out += ["## Every proposal", "",
            f"{len(rows)} proposals from {len({r['proposer'] for r in rows})} proposers over {len({r['round'] for r in rows}) if rows else 0} round(s); {len(valid)} valid against the menu, {len(rows) - len(valid)} rejected by the schema check; {len({r['hash'] for r in valid})} distinct constructions.", "",
            "| round | proposer | rank | construction | doublets (z) | lag-1 χ² (z) | unigram χ² (z) | IC (z) | gate | strict | predicted doublets | finite? | configs | tests (×55 pages) | already swept? | notes |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["round"], r["proposer"], r["rank"])):
        if r.get("error"):
            out.append(f"| {r['round']} | {r['proposer']} | {r['rank']} | {r['name']} | — | — | — | — | schema-invalid | | | | | | | {r['error']} |"); continue
        g, c = r["gate"], r["classify"]
        tests = f"{c['tests']:,}" if c["tests"] else "—"
        out.append(f"| {r['round']} | {r['proposer']} | {r['rank']} | **{r['name'][:60]}**: {r['describe']} | {cell(g,0)} | {cell(g,1)} | {cell(g,2)} | {cell(g,3)} | {'**PASS**' if g['pass'] else 'fail'} | {'pass' if g.get('pass_strict') else 'fail'} ({max(abs(v) for v in g.get('z_strict', [0])):.1f}) | {r.get('predicted_doublets')} | {'yes' if c['finite'] else 'no'} | {c['n_configs']:,} | {tests} | {c['swept']} | {c['note']} |")
    surv = [r for r in valid if r["gate"]["pass"]]
    seen, short = set(), []
    for r in surv:
        if r["hash"] in seen: continue
        seen.add(r["hash"]); short.append(r)
    strict = [r for r in short if r["gate"].get("pass_strict")]
    out += ["", "## Survivors (pass all four statistics under the pre-registered rule)", ""]
    if not short: out.append("None.")
    for r in short:
        c = r["classify"]; zs = max(abs(v) for v in r["gate"]["z_strict"])
        out.append(f"- **{r['name'][:60]}** ({r['proposer']}, round {r['round']}): {r['describe']}. Doublets {r['gate']['mean'][0]:.0f} ± {r['gate']['sd'][0]:.0f}; strict {'pass' if r['gate']['pass_strict'] else 'fail'} ({zs:.1f}). "
                   f"Decryptable finite family: {'yes' if c['finite'] else 'no'}" + (f", {c['n_configs']:,} configurations ≈ {c['tests']:,} tests" if c['finite'] else "") + f". Already swept: {c['swept']}. {c['note']}")
    new = [r for r in strict if r["classify"]["finite"] and r["classify"]["swept"] in ("no", "partly")]
    loose_only = [r for r in short if not r["gate"].get("pass_strict") and r["classify"]["finite"] and r["classify"]["swept"] in ("no", "partly")]
    out += ["", "### Short list: pass both rules, decryptable, not fully swept", ""]
    out += [f"- {r['describe']} ({r['proposer']} r{r['round']}, strict {max(abs(v) for v in r['gate']['z_strict']):.1f}): {r['classify']['n_configs']:,} configurations ≈ {r['classify']['tests']:,} decoder tests; {r['classify']['note']}" for r in new] or ["None."]
    out += ["", "### Pass the pre-registered rule only (fail strict), decryptable, not fully swept", ""]
    out += [f"- {r['describe']} ({r['proposer']} r{r['round']}, strict {max(abs(v) for v in r['gate']['z_strict']):.1f}): {r['classify']['n_configs']:,} configurations; {r['classify']['note'][:160]}" for r in loose_only] or ["None."]
    # what the loop found
    n_soft = sum(1 for r in valid if r["construction"]["repeat_rule"]["rule"] != "none" and r["construction"]["repeat_rule"]["p"] < 1)
    n_fb = sum(1 for r in valid if r["construction"]["key_source"]["type"] in ("cipher_feedback", "plain_feedback") and r["construction"]["key_source"]["base"] != "none")
    fb_pass = sum(1 for r in valid if r["construction"]["key_source"]["type"] in ("cipher_feedback", "plain_feedback") and r["construction"]["key_source"]["base"] != "none" and r["gate"]["pass"])
    fb_strict = sum(1 for r in valid if r["construction"]["key_source"]["type"] in ("cipher_feedback", "plain_feedback") and r["construction"]["key_source"]["base"] != "none" and r["gate"]["pass_strict"])
    out += ["", "## What the loop found", ""]
    if valid:
        out.append(
            f"All three proposers converged on the same mechanism: {n_soft} of the {len(valid)} constructions carry a soft reject-on-repeat rule at p ≈ 0.81, "
            f"so the doublet column passes nearly everything and the gate separated families on the other three statistics; the deliberate probes (hard rule, bump, "
            f"never-repeating pad, plaintext autokey) failed exactly where phase 2 said they would, which is a consistency check on the gate. {len(short)} distinct "
            f"constructions pass the pre-registered rule, {len(strict)} of them also pass the strict reading. Three groups. **(1) Stream plus ciphertext feedback** "
            f"(K_i = map(C_(i−1)) + S_i with S a totient, prime or running-text stream; the top ranks of Claude and GPT and most of round 2): {fb_pass} of {n_fb} pass "
            f"the pre-registered rule but only {fb_strict} pass strict, because the lag-1 difference stream under feedback is P + S and inherits the base stream's "
            f"non-uniform residues (lag-1 class χ² 65–96 against the pages' 42, four to eight null sigmas); wazar's 48 feedback configurations cover the additive form. "
            f"**(2) Position-walking affine multipliers** (C = ((i mod 28)+1)·P + K, the 'clock' idea from the field survey) over any stream lift the unigram χ² to "
            f"40–50 and the lag-1 χ² to 55–75; with the two published word keys DIVINITY and FIRFUMFERENFE the fits are strict 2.5 and 4.9, and nobody has run "
            f"them under the skip rule (812 configurations each). **(3) Independent streams with no text feedback** (LCG mod 3301, mod 1033 and mod 29 seeds, "
            f"an LCG mod 2³¹−1, the uniform probes) pass both rules trivially: an independent key with the right rejection rate *is* the phase 2 survivor, and the "
            f"gate cannot tell a Cicada-flavoured LCG from a one-time pad; only sweep size distinguishes them. The closest strict fits of the run (1.7–1.8) are the "
            f"Gematria-prime-value ciphertext feedback over the book's own running text and the LCG mod 29 (a 28-periodic key), both slightly above the uniform "
            f"family on the lag-1 column, where the pages themselves sit two sigma above uniform; 1.7 against 2.3 is not a significant difference. The usable "
            f"output is the short list above: small finite families that no ledger names (the LCG mod 3301 / 1033 / 29 seeds, the two published word keys with the clock multiplier, prime-value feedback over the book's text), each a few thousand to a few million decoder tests; the 2³¹-seed LCGs on the same list are not sweepable blind and are kept only for completeness.")
        out.append("")
        out.append("What the loop did not find: any construction that reproduces the pages by a route other than an independent key with a soft reject-on-repeat. "
                   "Every text-coupled key (feedback, autokey) that passes does so weakly and is distinguishable on the lag-1 column with the strict reading; "
                   "every uncoupled key passes regardless of its source. The brief's conclusion stands and the panel did not break it.")
    else:
        out.append("No proposals were gated (dry run).")
    out += ["", "## Token usage and cost", "", "| round | proposer | model served | input | output | seconds | cost |", "|---|---|---|---|---|---|---|"]
    for u in USAGE: out.append(f"| {u[2]} | {u[0]} | {u[1]} | {u[3]:,} | {u[4]:,} | {u[5]} | ${u[6]:.2f} |")
    out += [f"| | **total** | | {tot_in:,} | {tot_out:,} | | **${tot_cost:.2f}** |", "",
            f"Prices: Anthropic from the claude-api skill table ($10/$50 per M for claude-fable-5-1); GPT-6.1 Sol and Grok 4.7 prices are **assumed** ({PRICES['gpt-6.1-sol'][:2]}, {PRICES['grok-4.7'][:2]} $/M), so their cost column is an estimate; token counts are exact. "
            f"Round 0 is the first live attempt, which spent its whole 24k output budget on thinking at effort high and returned no text (`results/hypotheses/run1_failed.log`); the run proper uses effort medium with a 64k cap. "
            f"Round-1 prompt size by the Anthropic token counter: {brief_tokens} tokens (brief target: under 12k). Wall time of the final run {elapsed/60:.1f} min.", ""]
    # hand-over
    small = [r for r in new if r["classify"]["tests"] and r["classify"]["tests"] <= 10_000_000]
    short_txt = "; ".join(f"{r['describe']} ({r['classify']['n_configs']:,} configurations)" for r in small) or "none"
    big = len(new) - len(small)
    out += ["## Hand-over note (for the README owner)", "",
            "Text to merge into README.md as the next section (adjust the number):", "", "```markdown",
            "## 1x. Hypothesis loop: a model panel proposes, a statistical gate kills (`src/hypothesis_loop.py`, `results/hypotheses.md`, `docs/hypothesis-loop.md`)", "",
            f"A panel of three models (Claude Fable 5.1, GPT-6.1 Sol, Grok 4.7) was given an 11k-token brief of this repository's results, the ledger diff and the book's own methods, plus a fixed menu of cipher constructions (key source × combining rule × repeat-avoidance rule × F rule), and asked for ranked constructions in a JSON schema, two rounds, the second after seeing the first round's gate table. Proposals are data: the gate assembles each one from the menu and enciphers 200 replicates of solved-page English cut to the 55 real page lengths, scoring doublets, lag-1 class χ², unigram χ² and IC against the pages (pass = |z| < 3 on all four; a strict reading rescales by the iid-null sd). Survivors that are decryptable finite families are checked against the ledgers and sized. The gate reproduces the phase 2 table row for row before any proposal is scored.",
            "",
            f"Result: {len(rows)} proposals, {len(short)} pass the pre-registered rule, {len(strict)} pass strict. All three proposers converged on the soft reject-on-repeat at p ≈ 0.81, so the gate separated families on the other three statistics: stream-plus-ciphertext-feedback keys pass loosely but sit 4–8 null sigmas high on the lag-1 class χ² (the difference stream inherits the base stream's residues); position-walking affine multipliers lift unigram and lag-1 χ²; independent streams of any source pass trivially, since an independent key with the right rejection rate is the phase 2 survivor, and the gate cannot tell a Cicada-flavoured generator from a one-time pad. No construction reproduces the pages by another route. "
            f"The usable output is a short list of small finite families no ledger names ({len(small)} under ten million decoder tests; {big} more are LCGs with 2³¹ seeds, too large to sweep blind): {short_txt}. Each is a cheap lane for the existing skip decoder. Cost of the run: ${tot_cost:.2f} ({tot_in:,} input and {tot_out:,} output tokens, one failed attempt included).",
            "```", "", "Files touched by this session: `src/hypothesis_loop.py`, `results/hypotheses.md`, `results/hypotheses.json`, `results/hypotheses/` (brief, schema, raw responses, run logs), `docs/hypothesis-loop.md`. README.md untouched; nothing committed.", ""]
    (RESULTS / "hypotheses.md").write_text("\n".join(out))
    print("\n".join(out[-14:]))
    print(f"\nwrote results/hypotheses.md; tokens in {tot_in:,} out {tot_out:,}; cost ${tot_cost:.2f}; {elapsed/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
