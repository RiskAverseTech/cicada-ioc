"""Seeded-generator lane (2026-10-27), narrowed by the ledgers before it ran.

ALREADY DONE ELSEWHERE (results/ledger_diff.md; pnotisdev INDEX rows 69-80, wazar LEDGER B-01/B-04/
R16/R19-R26): php mt_rand, glibc rand/random, .NET Random, Python 3 and 2.7 MT19937 (integer, string
and timestamp seeds), mt32/mt31, Java, MSVC, drand48, Ruby, bash $RANDOM, Perl rand, TeX RNGs, over all
2^32 seeds (GPU, skip-aware bigram score) and small seeds per page; 199,088 OEIS sequences; 19.2 M
passphrases through MD5/SHA-1/SHA-256/SHA-512 and 719,280 KDF streams; 323 semantic seeds including 3301.
So neither the common generators with the squares as seeds nor book words through hashes are run here.

RUN HERE: generators no ledger lists, each a one-screen routine a 2012-14 programmer might have pasted:
  xorshift32 (13,17,5), xorshift64 (13,7,17; high 32 bits), xorshift128 (Marsaglia 2003 constants with x
  replaced by the seed), pcg32 (O'Neill reference, stream 54), minstd16807, minstd48271, randu (65539,
  2^31), splitmix64 (high 32 bits).  Three reductions of each 32-bit output: mod 29; top bits
  floor(x/2^32*29); rejection (low 5 bits, values 29-31 discarded).  Seeds: every seed 1..2^18 (dense) and
  the NAMED seeds (3301, 1033, 809, the 50 values of the two Know This squares, 2012/2013/2014, 20140104,
  509, 503, 845145127) on top.  Two keying modes are covered by construction: a stream restarted at index
  0 on every page, and one global stream (page 0 at index 0; later pages at their cumulative offset plus
  the skips consumed, scanned over +0..+130).

TWO TIERS.  Tier 1 decodes the first 80 runes of pages LP2-00, LP2-01 and LP2-02 under every seed x
reduction x 3 signs x 2 F with the soft-rule Viterbi; a (generator, reduction, seed, page) cell survives
at z_uni >= 4.5 over that window's random-keystream null (about 90 % of true keys at 80 runes, §23).
Tier 2 decodes the survivor's full page: candidate at z_uni >= 6 and 5-gram z_5 >= 6 and readable; a
candidate is then run on every page in both keying modes.  Controls: one plant per generator (8), random
seed below 2^18, reduction, sign and F random, 262-rune solved English under the soft rule; a control
passes tier 1 at rank 1 for its page and tier 2 at z_uni >= 6, z_5 >= 6.
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/generator_lane.py  (shards split the seed range);
       MERGE=1 -> results/generators.md; SMOKE=1 for a quick check.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F, ngram

SMOKE = os.environ.get("SMOKE") == "1"
SHARD, NSHARD, MERGE = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)), os.environ.get("MERGE") == "1"
rng = np.random.default_rng(65539 + SHARD)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
T1_PAGES = [0, 1, 2]; WIN = 80
SEEDMAX = 2 ** 18 if not SMOKE else 2 ** 12
NAMED = sorted({3301, 1033, 809, 2012, 2013, 2014, 20140104, 509, 503, 845145127} | {434, 1311, 312, 278, 966, 204, 812, 934, 280, 1071, 626, 620, 272, 138, 341, 131, 151, 366, 199, 130, 320, 18, 226, 245, 91})
Z_T1, Z_UNI, Z_5, NREPS = 4.5, 6.0, 6.0, (200 if SMOKE else 2000)
M32, M64 = np.uint64(0xFFFFFFFF), np.uint64(0xFFFFFFFFFFFFFFFF)


# ---------- generators: seeds (m,) uint64 -> outputs (m, L) uint32 ----------
def g_xorshift32(seeds, L):
    x = (seeds & M32).astype(np.uint64); x[x == 0] = 1; out = np.empty((len(x), L), np.uint32)
    for i in range(L):
        x ^= (x << np.uint64(13)) & M32; x ^= x >> np.uint64(17); x ^= (x << np.uint64(5)) & M32; out[:, i] = x
    return out
def g_xorshift64(seeds, L):
    x = seeds.astype(np.uint64); x[x == 0] = 1; out = np.empty((len(x), L), np.uint32)
    for i in range(L):
        x ^= x << np.uint64(13); x ^= x >> np.uint64(7); x ^= x << np.uint64(17); out[:, i] = (x >> np.uint64(32)).astype(np.uint32)
    return out
def g_xorshift128(seeds, L):
    m = len(seeds); x = (seeds & M32).astype(np.uint64); x[x == 0] = 1
    y = np.full(m, 362436069, np.uint64); z = np.full(m, 521288629, np.uint64); w = np.full(m, 88675123, np.uint64); out = np.empty((m, L), np.uint32)
    for i in range(L):
        t = (x ^ ((x << np.uint64(11)) & M32)) & M32; x, y, z = y, z, w
        w = (w ^ (w >> np.uint64(19)) ^ (t ^ (t >> np.uint64(8)))) & M32; out[:, i] = w
    return out
def g_pcg32(seeds, L):
    mult = np.uint64(6364136223846793005); inc = np.uint64((54 << 1) | 1)
    st = np.zeros(len(seeds), np.uint64); st = st * mult + inc; st = (st + seeds.astype(np.uint64)) * mult + inc
    out = np.empty((len(seeds), L), np.uint32)
    for i in range(L):
        old = st; st = old * mult + inc
        xs = (((old >> np.uint64(18)) ^ old) >> np.uint64(27)) & M32; rot = (old >> np.uint64(59)).astype(np.uint32)
        xs32 = xs.astype(np.uint32); out[:, i] = (xs32 >> rot) | (xs32 << ((-rot) & np.uint32(31)))
    return out
def _lcg31(a):
    def g(seeds, L):
        x = (seeds % np.uint64(2147483647)).astype(np.uint64); x[x == 0] = 1; out = np.empty((len(x), L), np.uint32)
        for i in range(L):
            x = (x * np.uint64(a)) % np.uint64(2147483647); out[:, i] = (x << np.uint64(1)).astype(np.uint32)   # scale 31 -> 32 bits
        return out
    return g
def g_randu(seeds, L):
    x = (seeds % np.uint64(2 ** 31)).astype(np.uint64); x[x % np.uint64(2) == 0] += np.uint64(1); out = np.empty((len(x), L), np.uint32)
    for i in range(L):
        x = (x * np.uint64(65539)) % np.uint64(2 ** 31); out[:, i] = (x << np.uint64(1)).astype(np.uint32)
    return out
def g_splitmix64(seeds, L):
    x = seeds.astype(np.uint64); out = np.empty((len(x), L), np.uint32)
    for i in range(L):
        x = x + np.uint64(0x9E3779B97F4A7C15); z = x
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9); z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB); z ^= z >> np.uint64(31)
        out[:, i] = (z >> np.uint64(32)).astype(np.uint32)
    return out
GENS = {"xorshift32": g_xorshift32, "xorshift64": g_xorshift64, "xorshift128": g_xorshift128, "pcg32": g_pcg32, "minstd16807": _lcg31(16807), "minstd48271": _lcg31(48271), "randu": g_randu, "splitmix64": g_splitmix64}


def reduce_(raw, how, L):
    """(m, L') uint32 -> (m, L) runes; rejection consumes extra outputs, so raw is generated longer."""
    if how == "mod29": return (raw[:, :L] % 29).astype(np.int64)
    if how == "top": return ((raw[:, :L].astype(np.float64) / 4294967296.0) * 29).astype(np.int64)
    low = (raw & 31).astype(np.int64); out = np.full((raw.shape[0], L), 0, np.int64)
    for r in range(raw.shape[0]):
        v = low[r][low[r] < 29]
        if len(v) < L: v = np.concatenate([v, np.zeros(L - len(v), np.int64)])
        out[r] = v[:L]
    return out
RED = ("mod29", "top", "rej")
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
LOGU = np.log(1 / N)


def keys_for(gen, how, seeds, L):
    raw = GENS[gen](np.asarray(seeds, dtype=np.uint64), int(L * 1.25) + 8 if how == "rej" else L)
    return reduce_(raw, how, L)


def null_stats(C, f_rule, mode, with5=False):
    Kr = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2)); sc, _, dec = decode(C, Kr, lu, f_rule, mode)
    if not with5: return sc.mean(), sc.std()
    s5 = ngram.score_batch(dec, T5); return sc.mean(), sc.std(), s5.mean(), s5.std()


RES = RESULTS
if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RES.glob("generators_shard*.json"))]
    ctr = [c for d in shards for c in d["controls"]]; surv = [s for d in shards for s in d["survivors"]]; cands = [c for d in shards for c in d["candidates"]]
    nt1 = sum(d["ntests_t1"] for d in shards); nt2 = sum(d["ntests_t2"] for d in shards)
    out = [f"# Seeded generators no ledger lists: {len(GENS)} generators x 3 reductions, seeds 1..{SEEDMAX:,} plus {len(NAMED)} named seeds", "",
           f"Tier 1: {nt1:,} window decodes (80 runes, pages LP2-00/01/02, 6 cells); survivors at z >= {Z_T1}: {len(surv)}. Tier 2: {nt2:,} full-page decodes; candidates at z_uni >= {Z_UNI} and z_5 >= {Z_5}: {len(cands)}. Rule and coverage in the module docstring; prior coverage by other labs listed there.", "",
           "## Controls", "", "| generator | reduction | seed | sign | F | tier-1 z (rank) | tier-2 z_uni | z_5 | pass |", "|---|---|---|---|---|---|---|---|---|"]
    for c in ctr: out.append(f"| {c['gen']} | {c['red']} | {c['seed']} | {c['sign']} | {c['F']} | {c['z1']:.1f} ({c['rank1']}) | {c['z2']:.1f} | {c['z5']:.1f} | {'yes' if c['passed'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['passed'] for c in ctr)} of {len(ctr)}.", "", "## Tier-1 survivors (top 20 by tier-2 z_uni)", "", "| generator | reduction | seed | page | sign | F | tier-1 z | tier-2 z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|---|---|"]
    for s_ in sorted(surv, key=lambda r: -r["z2"])[:20]: out.append(f"| {s_['gen']} | {s_['red']} | {s_['seed']} | {s_['page']} | {s_['sign']} | {s_['F']} | {s_['z1']:.2f} | {s_['z2']:.2f} | {s_['z5']:.1f} | {s_['translit'][:50]} |")
    out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"Largest tier-2 z_uni: {max((s_['z2'] for s_ in surv), default=0):.2f}; largest z_5: {max((s_['z5'] for s_ in surv), default=0):.2f}. Runtime, longest shard: {max(d['seconds'] for d in shards)/60:.0f} minutes on {len(shards)} shards.", ""]
    (RES / "generators.md").write_text("\n".join(out) + "\n")
    json.dump(dict(ntests_t1=nt1, ntests_t2=nt2, controls=ctr, survivors=surv, candidates=cands, seedmax=SEEDMAX, named=NAMED), open(RES / "generators.json", "w"), indent=1)
    print("\n".join(out[:4] + out[-3:])); sys.exit(0)

T5 = ngram.load_dense()
t0 = time.time()
# window nulls for the three tier-1 pages, full-page nulls for them too
W = {}; FULL = {}
for pi_ in T1_PAGES:
    pid, C = pages[pi_]
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            W[(pi_, f_rule, mode)] = null_stats(C[:WIN], f_rule, mode); FULL[(pi_, f_rule, mode)] = null_stats(C, f_rule, mode, with5=True)
print(f"nulls ready [{time.time()-t0:.0f}s]", flush=True)


def tier1(gen, how, seeds, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; Ks = keys_for(gen, how, seeds, WIN + S_MAX + 2)
    Ks = (-Ks) % N if sign == "add" else Ks
    m0, s0 = W[(pi_, f_rule, mode)]; sc = decode(C[:WIN], Ks, lu, f_rule, mode)[0]
    return (sc - m0) / s0


def tier2(gen, how, seed, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; K = keys_for(gen, how, [seed], len(C) + S_MAX + 2); K = (-K) % N if sign == "add" else K
    m0, s0, m5, s5 = FULL[(pi_, f_rule, mode)]; sc, _, dec = decode(C, K, lu, f_rule, mode)
    return float((sc[0] - m0) / s0), float((ngram.score_batch(dec, T5)[0] - m5) / s5), translit(dec[0][:80])


# ---------- controls (shard 0) ----------
controls = []
if SHARD == 0:
    for ci, gen in enumerate(GENS):
        how = RED[ci % 3]; sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 3) % 2); seed = int(rng.integers(1, SEEDMAX))
        pi_ = 0; pid, C0 = pages[pi_]; n = len(C0)
        K = keys_for(gen, how, [seed], n + S_MAX + 2)[0]
        o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
        C = encrypt(P, K, f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
        # tier 1 on the planted ciphertext against 4,096 neighbouring seeds
        block = np.arange(max(1, seed - 2048), seed + 2048); pos = int(np.where(block == seed)[0][0])
        Ks = keys_for(gen, how, block, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
        m0, s0 = null_stats(C[:WIN], f_rule, mode); z1 = (decode(C[:WIN], Ks, lu, f_rule, mode)[0] - m0) / s0; rank1 = int((z1 > z1[pos]).sum()) + 1
        m0f, s0f, m5, s5 = null_stats(C, f_rule, mode, with5=True); Kf = keys_for(gen, how, [seed], n + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
        sc, _, dec = decode(C, Kf, lu, f_rule, mode); z2 = float((sc[0] - m0f) / s0f); z5 = float((ngram.score_batch(dec, T5)[0] - m5) / s5)
        passed = z1[pos] >= Z_T1 and rank1 == 1 and z2 >= Z_UNI and z5 >= Z_5
        controls.append(dict(gen=gen, red=how, seed=seed, sign=sign, F=f_rule, z1=float(z1[pos]), rank1=rank1, z2=z2, z5=z5, passed=bool(passed)))
        print(f"  control {gen}/{how} seed {seed} {sign} F={f_rule}: tier1 z {z1[pos]:.1f} rank {rank1}; tier2 z_uni {z2:.1f} z_5 {z5:.1f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

# ---------- the sweep ----------
all_seeds = np.concatenate([np.arange(1, SEEDMAX + 1), np.array(NAMED)])
my_seeds = all_seeds[SHARD::NSHARD]
survivors, candidates, nt1, nt2 = [], [], 0, 0
zmax = {}
BATCH = 2048
for gen in GENS:
    for how in RED:
        for b in range(0, len(my_seeds), BATCH):
            seeds = my_seeds[b:b + BATCH]
            for pi_ in T1_PAGES:
                for sign, mode in SIGNS:
                    for f_rule in (False, True):
                        z = tier1(gen, how, seeds, pi_, sign, mode, f_rule); nt1 += len(seeds)
                        zmax[(gen, how)] = max(zmax.get((gen, how), -9), float(z.max()))
                        for k in np.where(z >= Z_T1)[0]:
                            z2, z5, tr = tier2(gen, how, int(seeds[k]), pi_, sign, mode, f_rule); nt2 += 1
                            row = dict(gen=gen, red=how, seed=int(seeds[k]), page=pages[pi_][0], sign=sign, F=f_rule, z1=float(z[k]), z2=z2, z5=z5, translit=tr)
                            survivors.append(row)
                            if z2 >= Z_UNI and z5 >= Z_5: candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
        print(f"  {gen}/{how} done: {nt1:,} tier-1 tests, max tier-1 z {zmax[(gen, how)]:.2f}, {len(survivors)} survivors, {len(candidates)} candidates  [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests_t1=nt1, ntests_t2=nt2, zmax={f"{g}/{h}": v for (g, h), v in zmax.items()}, seconds=time.time() - t0), open(RES / (f"generators_smoke.json" if SMOKE else f"generators_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} written [{time.time()-t0:.0f}s]", flush=True)
