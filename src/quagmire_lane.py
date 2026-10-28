"""Keyword-mixed alphabets under the book's keys: the quagmire family (2026-10-28).  Pre-registered.

Every decoder in every lab, this repository's included, assumes the key is added to the plaintext
in the fixed rune order (C = P ± K, or K − P).  If the author used a keyword-mixed alphabet on either
side, the classical quagmire constructions, every additive sweep was blind to the correct key, and the
anti-repeat fingerprint is unchanged because the rule acts on the output.  pnotisdev lists a
"keyword-mixed outer alphabet" as open; no ledger records a run.

Model.  A mixed alphabet A is a permutation of the 29 runes: a keyword's runes in order without
repeats, then the remaining runes in Gematria order.  With π_A(p) = position of p in A:
  Q1  C = π_A(P) + K            (mixed plaintext alphabet, straight ciphertext alphabet)
  Q2  C = A^{-1}... i.e. C = B[P + K]     (straight plaintext, mixed ciphertext alphabet B)
  Q3  C = A[π_A(P) + K]        (the same mixed alphabet on both sides)
  Q4  C = B[π_A(P) + K]        (two different mixed alphabets)
all with the skip-on-repeat rule, three sign conventions and both F variants.  Decoding is the
additive decoder on the relabelled ciphertext C' = π_B(C) with the unigram model relabelled by A,
then P = A[P'].  Alphabet keywords: every distinct word of three or more runes in the solved pages
plus the eleven Know-This words and a dozen Cicada terms; Q4 pairs are drawn from the 30 most salient
of those.  Keys: the §9 word keys forward and reversed and the prime, totient, prime+1, Fibonacci
and Lucas streams at every start (869 keys).

Two tiers as in §31.  Tier 1: first 80 runes of LP2-00, LP2-01, LP2-02, every config × key × 6 cells;
survivor at z ≥ 4.5 over the window's random-keystream null (the null is computed per (page, F, mode)
with the straight alphabet and SHARED across alphabets; the smoke test measures how far a mixed
ciphertext alphabet moves it and the result is recorded).  Tier 2: full page, z_uni ≥ 6 and 5-gram
z_5 ≥ 6, then readable.  Controls: eight plants, two per quagmire form, random keyword(s) and key,
signs and F cycled, 262-rune solved English under the soft rule; pass = tier-1 rank 1 for its page
among all configs and keys, tier-2 above both bars.
Usage: SHARD=k NSHARD=m python -I src/quagmire_lane.py ; MERGE=1 ; SMOKE=1.
"""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F, ngram

SMOKE = os.environ.get("SMOKE") == "1"
SHARD, NSHARD, MERGE = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)), os.environ.get("MERGE") == "1"
rng = np.random.default_rng(2929 + SHARD)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
T1_PAGES, WIN = [0, 1, 2], 80
Z_T1, Z_UNI, Z_5, NREPS = 4.5, 6.0, 6.0, (200 if SMOKE else 2000)
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))

# ---------- alphabets ----------
def mixed(word):
    r = english_to_runes(word); seen = []
    for x in r:
        if x not in seen: seen.append(x)
    return np.array(seen + [x for x in range(N) if x not in seen])
vocab = sorted({w.upper() for line in F.lines for w in line if len(english_to_runes(w)) >= 3})
EXTRA = ["CICADA", "CIRCUMFERENCE", "FIRFUMFERENFE", "LIBER", "PRIMUS", "LIBERPRIMUS", "INSTAR", "EMERGENCE", "THEWAY", "PILGRIMAGE", "GEMATRIA", "SHADOWS", "AETHEREAL", "BUFFERS", "VOID", "CARNAL", "OBSCURA", "FORM", "MOBIUS", "ANALOG", "MOURNFUL", "CABAL"]
KW = sorted(set(vocab) | set(EXTRA))
SALIENT = ["DIVINITY", "CIRCUMFERENCE", "FIRFUMFERENFE", "CICADA", "INSTAR", "PILGRIM", "PRIMES", "TOTIENT", "SACRED", "ENCRYPTED", "CONSUMPTION", "PRESERVATION", "ADHERENCE", "DIVINE", "SHADOWS", "AETHEREAL", "BUFFERS", "VOID", "CARNAL", "OBSCURA", "FORM", "MOBIUS", "ANALOG", "MOURNFUL", "CABAL", "WISDOM", "KOAN", "TRUTH", "EMERGE", "DECEPTION"]
ALPH = {w: mixed(w) for w in set(KW) | set(SALIENT)}
IDENT = np.arange(N)
configs = [("Q1", w, None) for w in KW] + [("Q2", None, w) for w in KW] + [("Q3", w, w) for w in KW] + [("Q4", a, b) for a in SALIENT for b in SALIENT if a != b]
if SMOKE: configs = configs[:6] + [c for c in configs if c[0] == "Q2"][:3] + [c for c in configs if c[0] == "Q3"][:3] + [c for c in configs if c[0] == "Q4"][:3]

# ---------- keys ----------
sign_, mode_, Ks_all, labs_all = F.ALLSETS[3]
want = {"vigenere-word", "vigenere-word-rev", "primes", "primes-1 (totient)", "primes+1", "fibonacci", "lucas"}
kidx = [i for i, (f, _) in enumerate(labs_all) if f in want]
Ks = Ks_all[kidx]; KL = [labs_all[i] for i in kidx]
print(f"{len(KW)} keywords, {len(configs)} alphabet configs, {len(Ks)} keys -> tier-1 {len(configs)*len(Ks)*6*len(T1_PAGES):,} tests", flush=True)


def relabel(C, A, B):
    """ciphertext through the ciphertext alphabet, unigram model through the plaintext alphabet"""
    A = IDENT if A is None else ALPH[A]; B = IDENT if B is None else ALPH[B]
    invB = np.empty(N, np.int64); invB[B] = np.arange(N)
    return invB[np.asarray(C)], lu[A], A


def null_stats(Cp, lup, f_rule, mode, with5=False, A=IDENT):
    Kr = rng.integers(0, N, size=(NREPS, len(Cp) + S_MAX + 2)); sc, _, dec = decode(Cp, Kr, lup, f_rule, mode)
    if not with5: return sc.mean(), sc.std()
    s5 = ngram.score_batch(A[dec], T5); return sc.mean(), sc.std(), s5.mean(), s5.std()


def enc_quag(P, K, form, A, B, sign, f_rule):
    """plant: P -> π_A(P) additive with K under the soft rule -> through B"""
    Ap = IDENT if A is None else ALPH[A]; Bp = IDENT if B is None else ALPH[B]
    piA = np.empty(N, np.int64); piA[Ap] = np.arange(N)
    Pp = piA[P] if form in ("Q1", "Q3", "Q4") else P
    # the F rule is applied to the plaintext F before relabelling: keep rune 0 fixed when f_rule (A keeps F at 0 only if word lacks F); so apply F rule on original P
    Cp = encrypt(Pp, K, f_rule=False, rng=rng, soft=0.81, mode=sign) if not f_rule else _enc_f(P, Pp, K, sign)
    return Bp[Cp]


def _enc_f(P, Pp, K, sign):
    """F rule on the ORIGINAL plaintext F: emitted as rune 0 unencrypted, consuming no key; otherwise additive on Pp with the soft rule"""
    from skip_decrypt import combine
    C, j, prev = [], 0, None
    for p, pp in zip(P, Pp):
        if p == 0: C.append(0); prev = 0; continue
        c = combine(pp, K[j], sign)
        while prev is not None and c == prev and rng.random() < 0.81: j += 1; c = combine(pp, K[j], sign)
        C.append(c); j += 1; prev = c
    return np.array(C)


RES = RESULTS
if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RES.glob("quagmire_shard*.json"))]
    ctr = [c for d in shards for c in d["controls"]]; surv = [s for d in shards for s in d["survivors"]]; cands = [c for d in shards for c in d["candidates"]]
    nt1 = sum(d["ntests_t1"] for d in shards); nt2 = sum(d["ntests_t2"] for d in shards)
    out = [f"# Keyword-mixed alphabets under the book's keys (quagmire I-IV): {len(configs)} alphabet configs x {len(Ks)} keys", "",
           f"Tier 1: {nt1:,} window decodes; survivors at z >= {Z_T1}: {len(surv)}. Tier 2: {nt2:,} full-page decodes; candidates: {len(cands)}. Null invariance check (smoke): {shards[0].get('null_shift','')}. Rule in the module docstring.", "",
           "## Controls", "", "| form | plaintext alphabet | ciphertext alphabet | key | sign | F | tier-1 z (rank) | tier-2 z_uni | z_5 | pass |", "|---|---|---|---|---|---|---|---|---|---|"]
    for c in ctr: out.append(f"| {c['form']} | {c['A']} | {c['B']} | {c['key']} | {c['sign']} | {c['F']} | {c['z1']:.1f} ({c['rank1']}) | {c['z2']:.1f} | {c['z5']:.1f} | {'yes' if c['passed'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['passed'] for c in ctr)} of {len(ctr)}.", "", "## Tier-1 survivors (top 20 by tier-2 z_uni)", "", "| form | A | B | key | page | sign | F | tier-1 z | tier-2 z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s_ in sorted(surv, key=lambda r: -r["z2"])[:20]: out.append(f"| {s_['form']} | {s_['A']} | {s_['B']} | {s_['key']} | {s_['page']} | {s_['sign']} | {s_['F']} | {s_['z1']:.2f} | {s_['z2']:.2f} | {s_['z5']:.1f} | {s_['translit'][:50]} |")
    out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"Largest tier-2 z_uni {max((s_['z2'] for s_ in surv), default=0):.2f}; largest z_5 {max((s_['z5'] for s_ in surv), default=0):.2f}. Runtime, longest shard: {max(d['seconds'] for d in shards)/60:.0f} minutes on {len(shards)} shards.", ""]
    (RES / "quagmire.md").write_text("\n".join(out) + "\n"); json.dump(dict(ntests_t1=nt1, ntests_t2=nt2, controls=ctr, survivors=surv, candidates=cands, nconfigs=len(configs), nkeys=len(Ks)), open(RES / "quagmire.json", "w"), indent=1)
    print("\n".join(out[:4] + out[-3:])); sys.exit(0)

T5 = ngram.load_dense(); t0 = time.time()
W, FULL = {}, {}
for pi_ in T1_PAGES:
    pid, C = pages[pi_]
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            W[(pi_, f_rule, mode)] = null_stats(C[:WIN], lu, f_rule, mode); FULL[(pi_, f_rule, mode)] = null_stats(C, lu, f_rule, mode, with5=True)
# how far does a mixed ciphertext alphabet move the window null?  measured on five random keywords, page 0, sub, F=False
null_shift = []
for w in rng.choice(KW, 5, replace=False):
    Cp, lup, A = relabel(pages[0][1][:WIN], None, w); m, s = null_stats(Cp, lu, False, "sub"); m0, s0 = W[(0, False, "sub")]
    null_shift.append(round(float((m - m0) / s0), 2))
print(f"nulls ready; mixed-alphabet null shift in sd units for five keywords: {null_shift}  [{time.time()-t0:.0f}s]", flush=True)


def tier1(form, A, B, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; Cp, lup, Ap = relabel(C[:WIN], A, B)
    Kb = (-Ks) % N if sign == "add" else Ks; m0, s0 = W[(pi_, f_rule, mode)]
    return (decode(Cp, Kb, lup, f_rule, mode)[0] - m0) / s0


def tier2(form, A, B, k, pi_, sign, mode, f_rule):
    pid, C = pages[pi_]; Cp, lup, Ap = relabel(C, A, B); Kb = (-Ks[k:k + 1]) % N if sign == "add" else Ks[k:k + 1]
    m0, s0, m5, s5 = FULL[(pi_, f_rule, mode)]; sc, _, dec = decode(Cp, Kb, lup, f_rule, mode); P = Ap[dec[0]]
    return float((sc[0] - m0) / s0), float((ngram.score_batch(P[None, :], T5)[0] - m5) / s5), translit(P[:80])


controls = []
if SHARD == 0:
    for ci in range(8):
        form = ("Q1", "Q2", "Q3", "Q4")[ci % 4]; sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 4) % 2)
        cf_true = [c for c in configs if c[0] == form][int(rng.integers(0, len([c for c in configs if c[0] == form])))]
        A, B = cf_true[1], cf_true[2]
        k = int(rng.integers(0, len(Ks))); n = len(pages[0][1]); o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
        Ktrue = Ks[k]
        C = enc_quag(P, Ktrue, form, A, B, sign, f_rule)
        # tier 1 over all configs x keys on this planted ciphertext (page-0 window null)
        pages[0] = (pages[0][0], C)   # temporarily substitute the plant for page 0
        zs = {cf: tier1(cf[0], cf[1], cf[2], 0, sign, mode, f_rule) for cf in configs}
        zt = float(zs[(form, A, B)][k]); rank = 1 + sum(int((z > zt).sum()) for z in zs.values()); best = max(float(z.max()) for cf, z in zs.items() if cf != (form, A, B))
        m0f, s0f, m5, s5 = null_stats(*relabel(C, A, B)[:2], f_rule, mode, with5=True, A=(IDENT if A is None else ALPH[A]))
        Cp, lup, Ap = relabel(C, A, B); Kb = (-Ks[k:k + 1]) % N if sign == "add" else Ks[k:k + 1]; sc, _, dec = decode(Cp, Kb, lup, f_rule, mode)
        z2 = float((sc[0] - m0f) / s0f); z5 = float((ngram.score_batch(Ap[dec[0]][None, :], T5)[0] - m5) / s5)
        passed = zt >= Z_T1 and rank == 1 and z2 >= Z_UNI and z5 >= Z_5
        controls.append(dict(form=form, A=A, B=B, key=KL[k][1], sign=sign, F=f_rule, z1=zt, rank1=rank, z2=z2, z5=z5, passed=bool(passed)))
        print(f"  control {form} A={A} B={B} key={KL[k][1]} {sign} F={f_rule}: tier1 z {zt:.1f} rank {rank} (best other {best:.1f}); tier2 z_uni {z2:.1f} z_5 {z5:.1f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)
        pages[0] = (pages[0][0], F.pages[0][1])   # restore

survivors, candidates, nt1, nt2 = [], [], 0, 0
my = configs[SHARD::NSHARD]
for ci, (form, A, B) in enumerate(my):
    for pi_ in T1_PAGES:
        for sign, mode in SIGNS:
            for f_rule in (False, True):
                z = tier1(form, A, B, pi_, sign, mode, f_rule); nt1 += len(Ks)
                for k in np.where(z >= Z_T1)[0]:
                    z2, z5, tr = tier2(form, A, B, int(k), pi_, sign, mode, f_rule); nt2 += 1
                    row = dict(form=form, A=A, B=B, key=KL[k][1], page=pages[pi_][0], sign=sign, F=f_rule, z1=float(z[k]), z2=z2, z5=z5, translit=tr); survivors.append(row)
                    if z2 >= Z_UNI and z5 >= Z_5: candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    if (ci + 1) % 50 == 0 or ci == len(my) - 1: print(f"  {ci+1}/{len(my)} configs: {nt1:,} tier-1 tests, {len(survivors)} survivors, {len(candidates)} candidates  [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests_t1=nt1, ntests_t2=nt2, null_shift=null_shift, seconds=time.time() - t0), open(RES / (f"quagmire_smoke.json" if SMOKE else f"quagmire_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} written [{time.time()-t0:.0f}s]", flush=True)
