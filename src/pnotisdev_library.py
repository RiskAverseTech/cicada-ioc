"""pnotisdev's keystream library ("KSB1", 1,447 streams), re-implemented from the generator definitions (2026-10-28).

The other lab (github.com/pnotisdev/cicada3301, commit 15200c6, 2026-10-24) screened a library of number-theoretic
sequences, digits of constants, Cicada numbers, hash counter streams of Cicada strings and keyword keys from the solved
pages with an IoC / bigram engine (registry rows lib-sections, multipliers, hyp-streams, open-h1).  The binary export
(work/kscreen/data/library.ksb) is not in their repository; its generator is (work/kscreen/export.py, work/keystreams.py,
work/prng_screen.py, work/grid60.py, work/lp.py, work/ref/errata.tsv).  Those files were downloaded as DATA into
data/external/pnotisdev/ (gitignored; SHA-256 in SOURCES.md) and read; nothing of theirs is executed.  This module
rebuilds every stream from their definitions on this repository's copy of the rtkd/iddqd master transcription, with
their six errata applied (one rune swap on book page 9, five payload bytes).

Families (their names are kept as stream labels):
  integer sequences   primes, primes-1 (totient), primes+1, primes^2, prime gaps, prime index of primes, primes from 3301,
                      cumulative prime sum, n, n^2, n^3, triangular, fibonacci, lucas, pell, phi(n), sigma(n), d(n),
                      cumulative phi(n), composites, emirps, gematria primes cycle, a^n mod 29 (a = 2..28), 3301*n, 1033*n, 3301^n
  constant digits     pi, e, phi, sqrt2, sqrt3, ln2 in base 10 (25,000 significant digits, integer part included) and base 29
  cicada numbers      the two magic squares (rows, columns), the page-30 grid (rows, columns, 3301-x primes, sorted, first 12,
                      last row), the Know This word grid with Gematria sums, the An End hash (bytes, nibbles), the grid
                      caption (runes, prime values, Gematria sums), the digits 3301 and 1033
  new number families primes^3, (p±1)/2, p_n ± n, n p_n, digit sums, reversed digits, popcount, base-29 digit sum, 3301 p_n,
                      p_n mod 3301, 3301 - p_n, p_(n+1) p_n, p_n^2 - 1, mobius, omega, Omega, rad, Carmichael lambda, pi(n), partitions
  more constants      base-29 digits of euler gamma, zeta(3), Catalan, sqrt5, ln3, pi^2, e^pi, cbrt2, ln10, sqrt3301, ln3301, sqrt29, 1/3301
  hash streams        sha256-ctr, sha512-ctr, md5-ctr, sha256-chain of 65 distinct seeds (50 Cicada strings, 12 numbers, the An End hash as
                      hex and as bytes, the payload and its reverse, the payload hex; '3301' and '1033' occur twice), each read mod 29 and by rejection (bytes >= 232 dropped)
  payload             the 256 corrected bytes mod 29, reversed, and the 512 base-60 digits, cycled
  keywords            every word of >= 4 letters and every two-word phrase of the solved pages, 29 extra Cicada words, as repeating keys
Each stream is 20,000 values (periodic ones are exact cycles).  Build: .venv/bin/python -I src/pnotisdev_library.py
(writes data/external/pnotisdev/library_cache.npz, gitignored, and data/processed/pnotisdev_library_manifest.tsv with a
SHA-256 per stream so the other lab can check that the streams decoded here are theirs).
"""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, RAW, PROCESSED, LATIN, RUNES, IDX, ROOT

LEN = 20000
PRIME = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
LATIN_P = list(LATIN); LATIN_P[21] = "ING"          # their Gematria table writes rune 21 as ING, which their word keys inherit
CACHE = ROOT / "data" / "external" / "pnotisdev" / "library_cache.npz"
MANIFEST = PROCESSED / "pnotisdev_library_manifest.tsv"
DIGITS60 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"
# their work/ref/errata.tsv: (book page 1-indexed = their page + 1, master text, verified text) and five payload tokens
ERRATA_RUNES = [(9, "ᛒᛖᛚᛖᛁᚢᛖ", "ᛒᛖᛚᛁᛖᚢᛖ")]
ERRATA_PAYLOAD = {45: "1l", 50: "0l", 165: "0I", 172: "2S", 246: "3I"}


def sieve(limit):
    m = np.ones(limit + 1, dtype=bool); m[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if m[i]: m[i * i::i] = False
    return np.nonzero(m)[0].tolist()


_PRIMES = sieve(3_500_000)


def _arr(seq):
    return np.array([int(x) % N for x in list(seq)[:LEN]], dtype=np.int64)


def _cycle(vals):
    vals = list(vals); return _arr((vals * (LEN // len(vals) + 1))[:LEN])


# ---------------------------------------------------------------- their transcription parsing, on this repository's master file
def master_text():
    t = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8")
    body = t.split("\n\n", 1)[1]
    pages = body.split("%")
    for page, old, new in ERRATA_RUNES:                                   # their page index p is book page p+1
        assert pages[page - 1].count(old) == 1, (page, old)
        pages[page - 1] = pages[page - 1].replace(old, new)
    return "%".join(pages)


def load_segments():
    """Their lp.load_segments: tokens are rune indices or separators ' ' (word), '.', '\\n', '&', '%', and '#...' numerals."""
    body = master_text().split("§")[0]
    segs = []
    for raw in body.split("$"):
        toks = []
        for ch in raw:
            if ch in IDX: toks.append(IDX[ch])
            elif ch == "-": toks.append(" ")
            elif ch == ".": toks.append(".")
            elif ch == "/": toks.append("\n")
            elif ch in "&%": toks.append(ch)
            elif ch.isalnum():
                if toks and isinstance(toks[-1], str) and toks[-1].startswith("#"): toks[-1] += ch
                else: toks.append("#" + ch)
        if any(isinstance(t, int) for t in toks): segs.append(toks)
    return segs


def runes_of(toks):
    return [t for t in toks if isinstance(t, int)]


def word_spans(toks, plain):
    spans, cur, start, pos = [], [], 0, 0
    for t in toks + [" "]:
        if isinstance(t, int):
            if not cur: start = pos
            cur.append(LATIN_P[plain[pos]]); pos += 1
        elif t in ("\n", "%"): continue
        elif cur: spans.append(("".join(cur), start, pos)); cur = []
    return spans


def word_to_key(word):
    """Their lp.word_to_key: greedy on the longest Gematria spelling (ING, then TH EO OE AE IA EA, then letters; V K Z Q aliased)."""
    order = sorted(range(N), key=lambda i: -len(LATIN_P[i])); w, out = word.upper(), []
    while w:
        for i in order:
            if w.startswith(LATIN_P[i]): out.append(i); w = w[len(LATIN_P[i]):]; break
        else:
            out.append({"V": 1, "K": 5, "Z": 15, "Q": 5}[w[0]]); w = w[1:]
    return out


def _keyed(c, keyfn, literal=()):
    out, j = [], 0
    for i, x in enumerate(c):
        if i in literal: out.append(x); continue
        out.append((x - keyfn(j)) % N); j += 1
    return out


_DIV = word_to_key("DIVINITY"); _FIR = word_to_key("FIRFUMFERENFE"); _P2000 = _PRIMES[:2000]
KNOWN = {0: lambda c: [(N - 1 - x) % N for x in c], 1: lambda c: _keyed(c, lambda j: _DIV[j % 8], {48, 74, 84, 132, 159, 160, 250, 421, 443, 465, 514}),
         2: lambda c: c, 3: lambda c: [(N - 1 - ((x - 3) % N)) % N for x in c], 4: lambda c: c,
         5: lambda c: _keyed(c, lambda j: _FIR[j % 13], {49, 58}), 6: lambda c: c, 16: lambda c: _keyed(c, lambda j: _P2000[j] - 1, {56}), 17: lambda c: c}


# ---------------------------------------------------------------- the payload (their grid60.py, with the five byte errata)
def grid_tokens():
    pages = master_text().split("%"); toks = []
    for p in (64, 65, 66): toks += re.findall(r"\b[0-4][0-9A-Za-x]\b", pages[p])
    for k, v in ERRATA_PAYLOAD.items(): toks[k] = v
    return toks


def grid_bytes():
    toks = grid_tokens(); vals = [DIGITS60.index(t[0]) * 60 + DIGITS60.index(t[1]) for t in toks]
    assert len(vals) == 256 and max(vals) <= 255, (len(vals), max(vals)); return bytes(vals)


def an_end_hash(segs):
    return "".join(t[1:] for t in segs[16] if isinstance(t, str) and t.startswith("#")).lower()


# ---------------------------------------------------------------- families
def integer_sequences():
    out = {}; ps = _PRIMES[:LEN + 10]; pset = set(_PRIMES[:LEN * 4])
    out["primes"] = _arr(ps); out["primes-1 (totient)"] = _arr([p - 1 for p in ps]); out["primes+1"] = _arr([p + 1 for p in ps])
    out["primes^2"] = _arr([p * p for p in ps]); out["prime gaps"] = _arr([b - a for a, b in zip(ps, ps[1:])])
    out["prime index of primes"] = _arr([_PRIMES[p - 1] for p in ps[:LEN] if p - 1 < len(_PRIMES)])
    out["primes from 3301"] = _arr([p for p in _PRIMES[:LEN + 500] if p >= 3301])
    out["cumulative prime sum"] = _arr(np.cumsum(np.array(ps, dtype=object)))
    out["n"] = _arr(range(1, LEN + 1)); out["n^2"] = _arr([i * i for i in range(1, LEN + 1)]); out["n^3"] = _arr([i ** 3 for i in range(1, LEN + 1)])
    out["triangular"] = _arr([i * (i + 1) // 2 for i in range(1, LEN + 1)])
    fib, luc, pell = [0, 1], [2, 1], [0, 1]
    while len(fib) < LEN:
        fib.append((fib[-1] + fib[-2]) % N); luc.append((luc[-1] + luc[-2]) % N); pell.append((2 * pell[-1] + pell[-2]) % N)
    out["fibonacci"] = _arr(fib); out["lucas"] = _arr(luc); out["pell"] = _arr(pell)
    M = LEN + 2; phi = list(range(M))
    for i in range(2, M):
        if phi[i] == i:
            for j in range(i, M, i): phi[j] -= phi[j] // i
    sigma = [0] * M; divs = [0] * M
    for i in range(1, M):
        for j in range(i, M, i): sigma[j] += i; divs[j] += 1
    out["phi(n)"] = _arr(phi[1:]); out["sigma(n)"] = _arr(sigma[1:]); out["d(n)"] = _arr(divs[1:])
    out["cumulative phi(n)"] = _arr(np.cumsum(np.array(phi[1:], dtype=object)))
    out["composites"] = _arr([i for i in range(4, 3 * LEN) if i not in pset])
    big = set(_PRIMES)
    out["emirps"] = _arr([p for p in _PRIMES if p > 10 and str(p) != str(p)[::-1] and int(str(p)[::-1]) in big])
    out["gematria primes cycle"] = _cycle(PRIME)
    for a in range(2, N): out[f"{a}^n mod 29"] = _arr([pow(a, i, N) for i in range(LEN)])
    out["3301*n"] = _arr([3301 * i for i in range(1, LEN + 1)]); out["1033*n"] = _arr([1033 * i for i in range(1, LEN + 1)])
    out["3301^n"] = _arr([pow(3301, i, N) for i in range(1, LEN + 1)])
    return out


def _base29_frac(v, L):
    import mpmath
    x = int(mpmath.floor((v - mpmath.floor(v)) * mpmath.mpf(N) ** L)); dig = []
    while x: x, d = divmod(x, N); dig.append(d)
    return (dig + [0] * (L - len(dig)))[::-1]


def constant_digits():
    import mpmath
    out = {}; mpmath.mp.dps = 32000
    consts = {"pi": mpmath.pi, "e": mpmath.e, "phi": (1 + mpmath.sqrt(5)) / 2, "sqrt2": mpmath.sqrt(2), "sqrt3": mpmath.sqrt(3), "ln2": mpmath.log(2)}
    for name, v in consts.items():
        s = mpmath.nstr(v, 25000, strip_zeros=False).replace(".", "")
        out[f"{name} digits (base 10)"] = _arr([int(ch) for ch in s])
    for name, v in consts.items(): out[f"{name} digits (base 29)"] = _arr(_base29_frac(v, LEN))
    return out


def more_constants():
    import mpmath
    mpmath.mp.dps = 32000
    consts = {"euler gamma": mpmath.euler, "zeta(3)": mpmath.zeta(3), "catalan G": mpmath.catalan, "sqrt5": mpmath.sqrt(5), "ln3": mpmath.log(3),
              "pi^2": mpmath.pi ** 2, "e^pi": mpmath.e ** mpmath.pi, "cbrt2": mpmath.cbrt(2), "ln10": mpmath.log(10), "sqrt3301": mpmath.sqrt(3301),
              "ln3301": mpmath.log(3301), "sqrt29": mpmath.sqrt(29), "1/3301": mpmath.mpf(1) / 3301}
    return {f"{name} digits (base 29)": _arr(_base29_frac(v, LEN)) for name, v in consts.items()}


def cicada_numbers(segs):
    out = {}
    def nums(seg): return [int(t[1:]) for t in segs[seg] if isinstance(t, str) and t.startswith("#") and t[1:].isdigit()]
    sq14 = nums(6)[:25]; out["page-14 square rows"] = _cycle(sq14); out["page-14 square cols"] = _cycle([sq14[r * 5 + c] for c in range(5) for r in range(5)])
    g30 = nums(10)[:16]; out["page-30 grid rows"] = _cycle(g30); out["page-30 grid cols"] = _cycle([g30[r * 4 + c] for c in range(4) for r in range(4)])
    vals, cur = [], []
    for t in segs[2] + [" "]:
        if isinstance(t, int): cur.append(t)
        else:
            if cur: vals.append(sum(PRIME[x] for x in cur)); cur = []
            if t.startswith("#"): vals.append(int(t[1:]))
    out["1033 square rows"] = _cycle(vals[-25:])
    h = an_end_hash(segs); out["An End hash bytes"] = _cycle(bytes.fromhex(h)); out["An End hash nibbles"] = _cycle([int(ch, 16) for ch in h])
    grid_primes = [3301 - x for x in g30[:12]]
    out["page-30 grid primes (3301-x)"] = _cycle(grid_primes); out["page-30 grid primes sorted"] = _cycle(sorted(grid_primes))
    out["page-30 grid first 12"] = _cycle(g30[:12]); out["page-30 last row"] = _cycle(g30[12:])
    out["caption 0.10 gematria sums"] = _cycle([149, 489]); out["caption 0.10 runes"] = _cycle(runes_of(segs[10]))
    out["caption 0.10 prime values"] = _cycle([PRIME[x] for x in runes_of(segs[10])])
    out["3301 digits"] = _cycle([3, 3, 0, 1]); out["1033 digits"] = _cycle([1, 0, 3, 3])
    return out


def new_number_families():
    L = LEN; ps = _PRIMES[:L + 10]; out = {}
    arr = lambda g: np.array([int(x) % N for x in g], dtype=np.int64)
    out["primes^3"] = arr(p ** 3 for p in ps[:L]); out["(p-1)/2"] = arr((p - 1) // 2 for p in ps[1:L + 1]); out["(p+1)/2"] = arr((p + 1) // 2 for p in ps[1:L + 1])
    out["p_n + n"] = arr(p + i for i, p in enumerate(ps[:L], 1)); out["p_n - n"] = arr(p - i for i, p in enumerate(ps[:L], 1)); out["n * p_n"] = arr(p * i for i, p in enumerate(ps[:L], 1))
    out["primes digit sum"] = arr(sum(map(int, str(p))) for p in ps[:L]); out["primes reversed digits"] = arr(int(str(p)[::-1]) for p in ps[:L])
    out["primes popcount"] = arr(bin(p).count("1") for p in ps[:L]); out["primes base-29 digit sum"] = arr(sum(np.base_repr(p, 29).encode()) for p in ps[:L])
    out["3301 * p_n"] = arr(3301 * p for p in ps[:L]); out["p_n mod 3301"] = arr(p % 3301 for p in ps[:L]); out["3301 - p_n"] = arr(3301 - p for p in ps[:L])
    out["p_(n+1) * p_n"] = arr(a * b for a, b in zip(ps, ps[1:L + 1])); out["p_n^2 - 1"] = arr(p * p - 1 for p in ps[:L])
    M = L + 2; spf = list(range(M))
    for i in range(2, int(M ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, M, i):
                if spf[j] == j: spf[j] = i
    def factor(x):
        f = {}
        while x > 1: p = spf[x]; f[p] = f.get(p, 0) + 1; x //= p
        return f
    fs = [factor(i) for i in range(1, L + 1)]
    out["mobius mu(n)"] = arr(0 if any(e > 1 for e in f.values()) else (-1) ** len(f) for f in fs)
    out["omega(n)"] = arr(len(f) for f in fs); out["Omega(n)"] = arr(sum(f.values()) for f in fs)
    out["rad(n)"] = arr(int(np.prod([p for p in f], dtype=object)) if f else 1 for f in fs)
    from math import lcm
    def carmichael(f):
        v = 1
        for p, e in f.items():
            lam = (p - 1) * p ** (e - 1)
            if p == 2 and e >= 3: lam //= 2
            v = lcm(v, lam)
        return v
    out["carmichael lambda(n)"] = arr(carmichael(f) for f in fs)
    pi_n, cnt, pset = [], 0, set(_PRIMES[:L])
    for i in range(1, L + 1): cnt += i in pset; pi_n.append(cnt)
    out["prime counting pi(n)"] = arr(pi_n)
    part = [1] + [0] * L; pent = []; k = 1
    while True:
        g1, g2 = k * (3 * k - 1) // 2, k * (3 * k + 1) // 2
        if g1 > L: break
        pent.append((g1, 1 if k % 2 else -1)); pent.append((g2, 1 if k % 2 else -1)); k += 1
    for m in range(1, L + 1):
        s = 0
        for g, sg in pent:
            if g > m: break
            s += sg * part[m - g]
        part[m] = s % N
    out["partitions p(n)"] = arr(part[1:])
    return out


SEED_STRINGS = ["3301", "1033", "cicada", "cicada3301", "Cicada 3301", "liber primus", "liberprimus", "LIBER PRIMUS", "intus", "INTUS", "instar", "INSTAR",
                "divinity", "DIVINITY", "firfumferenfe", "FIRFUMFERENFE", "circumference", "CIRCUMFERENCE", "primes", "totient", "pilgrim", "PILGRIM", "welcome",
                "parable", "koan", "an end", "AN END", "deep web", "emergence", "INSTAR EMERGENCE", "self-reliance", "7A35090F", "0x7A35090F", "FULMAEAYOEA",
                "the primes are sacred", "THE PRIMES ARE SACRED", "the totient function is sacred", "all things should be encrypted", "ALL THINGS SHOULD BE ENCRYPTED",
                "a warning", "some wisdom", "an instruction", "know this", "question all things", "command your own self", "program your mind", "program reality",
                "within", "emerge", "shadows aethereal buffers void carnal obscura form mobius analog void mournful aethereal cabal"]
SEEDS_EXTRA = [3301, 1033, 29, 1729, 729, 7, 31, 2014, 20140104, 1311, 434, 3258]


def hash_streams(segs):
    """Their export.hash_streams: counter and chain streams of the seeds of prng_screen.seeds(), the An End hash bytes, the payload and its reverse."""
    payload = grid_bytes(); h = an_end_hash(segs)
    seeds = [s.encode() for s in SEED_STRINGS] + [h.encode(), payload.hex().encode()] + [str(s).encode() for s in SEEDS_EXTRA]
    seeds += [payload, bytes.fromhex(h), payload[::-1]]
    labels = [s.decode("latin-1")[:40] if len(s) < 120 else f"<{len(s)} bytes {s[:4].hex()}>" for s in seeds]
    need = LEN * 2; out = {}
    for sb, lab in zip(seeds, labels):
        streams = {}
        for hn, H in (("sha256", hashlib.sha256), ("sha512", hashlib.sha512), ("md5", hashlib.md5)):
            raw, i = bytearray(), 0
            while len(raw) < need: raw += H(sb + i.to_bytes(4, "big")).digest(); i += 1
            streams[f"{hn}-ctr"] = bytes(raw)
        raw, x = bytearray(), hashlib.sha256(sb).digest()
        while len(raw) < need: raw += x; x = hashlib.sha256(x).digest()
        streams["sha256-chain"] = bytes(raw)
        for gname, raw in streams.items():
            b = np.frombuffer(raw, dtype=np.uint8).astype(np.int64)
            out[f"{gname} mod :{lab}"] = (b % N)[:LEN]; out[f"{gname} reject :{lab}"] = (b[b < 232] % N)[:LEN]
    pb = np.frombuffer(payload, dtype=np.uint8).astype(np.int64)
    out["payload bytes mod 29 (cycled)"] = np.resize(pb % N, LEN); out["payload bytes reversed mod 29 (cycled)"] = np.resize(pb[::-1] % N, LEN)
    digs = [DIGITS60.index(ch) for t in grid_tokens() for ch in t]
    out["payload base-60 digits mod 29 (cycled)"] = np.resize(np.array(digs) % N, LEN)
    return out


EXTRA_WORDS = ["DIVINITY", "FIRFUMFERENFE", "CIRCUMFERENCE", "INSTAR", "EMERGENCE", "PRIMALITY", "TOTIENT", "PILGRIM", "CICADA", "LIBERPRIMUS", "INTUS", "PARABLE",
               "KOAN", "WELCOME", "DEEPWEB", "SELFRELIANCE", "AGRIPPA", "THELEMA", "MOBIUS", "AETHEREAL", "OBSCURA", "CABAL", "ANALOG", "MOURNFUL", "SHADOWS",
               "BUFFERS", "CARNAL", "VOID", "FULMAEAYOEA"]


def keywords(segs):
    words, phrases = set(), set()
    for i, f in KNOWN.items():
        plain = f(runes_of(segs[i])); ws = [w for w, _, _ in word_spans(segs[i], plain)]
        words.update(w for w in ws if len(w) >= 4)
        for a in range(len(ws) - 1): phrases.add(" ".join(ws[a:a + 2]))
    out = {}
    for w in sorted(words | set(EXTRA_WORDS)) + sorted(phrases):
        key = word_to_key(re.sub(r"[^A-Z]", "", w))
        if key: out[f"kw:{w}"] = _cycle(key)
    return out


FAMILY_OF = {}


def library():
    """name -> (family, int64 array of LEN values mod 29), in their insertion order."""
    segs = load_segments(); ks = {}
    for fam, d in (("integer", integer_sequences()), ("constant", constant_digits()), ("cicada", cicada_numbers(segs)), ("number2", new_number_families()),
                   ("constant2", more_constants()), ("hash", hash_streams(segs)), ("keyword", keywords(segs))):
        for k, v in d.items():
            v = np.asarray(v, dtype=np.int64) % N
            if len(v) < LEN: v = np.resize(v, LEN)
            ks[k] = (fam if k.split(" ")[0] not in ("payload",) else "payload", v)
    return ks


def period(v, max_p=5000, probe=3000):
    for p in (np.flatnonzero(v[1:max_p + 1] == v[0]) + 1):
        if np.array_equal(v[p:p + probe], v[:probe]): return int(p)
    return 0


def load():
    """(names, families, periods, K int8 (n, LEN)); builds and caches on first use."""
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=False); return list(z["names"]), list(z["families"]), z["periods"].tolist(), z["K"]
    ks = library(); names = list(ks); fams = [ks[k][0] for k in names]; K = np.stack([ks[k][1] for k in names]).astype(np.int8)
    periods = [period(ks[k][1]) for k in names]
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, names=np.array(names), families=np.array(fams), periods=np.array(periods), K=K)
    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("# pnotisdev's KSB1 keystream library rebuilt here (src/pnotisdev_library.py); sha256 of the 20,000 values as bytes 0..28\n")
        f.write("index\tfamily\tname\tperiod\tfirst_12_values\tsha256\n")
        for i, (n_, fam, p) in enumerate(zip(names, fams, periods)):
            f.write(f"{i}\t{fam}\t{n_}\t{p}\t{' '.join(map(str, K[i][:12].tolist()))}\t{hashlib.sha256(K[i].astype(np.uint8).tobytes()).hexdigest()}\n")
    return names, fams, periods, K


if __name__ == "__main__":
    import time; t0 = time.time()
    if CACHE.exists(): CACHE.unlink()
    names, fams, periods, K = load()
    from collections import Counter
    print(f"{len(names)} streams in {time.time()-t0:.0f}s; by family: {dict(Counter(fams))}; periodic: {sum(1 for p in periods if p)}; non-periodic: {sum(1 for p in periods if not p)}")
    for i in (0, 1, 2, 30, 56, 70, 100):
        print(f"  {names[i]!r} period {periods[i]}: {K[i][:16].tolist()}")
