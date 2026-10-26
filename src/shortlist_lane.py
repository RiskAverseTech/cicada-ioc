"""Short-list lane: the finite families the hypothesis loop (results/hypotheses.md) left as "pass both
gate rules, decryptable, on no ledger, under ten million tests", run through the skip decoder with
planted controls.

Families (each under the soft reject-on-repeat rule, three sign conventions, both F variants):
  A  LCG mod 3301:  x -> a*x + c mod 3301, key = x mod 29, every seed, (a, c) in {(1033, 0), (3, 0), (7, 1)}
  B  LCG mod 1033:  (a, c) = (3301 mod 1033, 29), every seed, rejection one and two (Grok proposed skip-by-two)
  C  LCG mod 29:    every a in 2..28, c, seed (a = 1 is the affine position formula of phase 3); distinct sequences
  D  DIVINITY and FIRFUMFERENFE with the clock multiplier: C = m_i*P + K_j, m_i = ((a*i + b) mod 28) + 1, all (a, b)
  E  prime-gap stream (p_(n+1) - p_n) with the clock multiplier, offsets 0..100 and 3301 (as proposed), sign add only
  F  Gematria prime-value (and totient-value) ciphertext feedback over the book's own text:
     C_i = P_i + f(C_(i-1)) + plaintext[o + j], every offset o, rejection one and two

Decoding.  The forced-skip condition of score.decode, C_i - C_(i-1) == K_j - K_(j-1), is unchanged by a
per-position multiplier (both the skipped and the used symbol multiply the same plaintext) and by a
ciphertext-feedback term (both carry the same f(C_(i-1))), so the same Viterbi runs with two changes:
the plaintext is read as P = m_i^-1 (C_i - K_j) and, for feedback, from C'_i = C_i - f(C_(i-1)).
decode_lane below is score.decode's path with those two hooks; with neither it is bit-identical (asserted).

PRE-REGISTERED RULE (as phases 3-7): a page counts as decrypted only if its best configuration scores
z >= 6 above that page's own random-keystream null under the same decoder mode, AND reads as English.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, PROCESSED, RESULTS, primes
from score import english_model, decode, S_MAX, LOGU, translit
from hypothesis_loop import sieve

rng = np.random.default_rng(3301 * 7)
lu, lb, plain = english_model()
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
LMAX = max(len(c) for _, c in pages) + S_MAX + 2
PV = np.array(primes(N))
INV = np.array([0] + [pow(a, -1, N) for a in range(1, N)])
DIVINITY = [23, 10, 1, 10, 9, 10, 16, 26]
FIRFUMFERENFE = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]
MAPS = {"prime_value": lambda x: PV[x] % N, "totient_value": lambda x: (PV[x] - 1) % N}


def decode_lane(C, Ks, lu, f_rule=False, mode="sub", minv=None, Cx=None, rejection="one", free_first=False):
    """score.decode with two hooks: minv (m, n) per-row per-position multiplier inverses, Cx the ciphertext
    the plaintext is read from (the skip condition and the literal-F test still use C).  free_first zeroes
    the gain at position 0 (unknown feedback seed)."""
    C = np.asarray(C); Cx = C if Cx is None else np.asarray(Cx); m, L = Ks.shape; n = len(C)
    T0 = int((C == 0).sum()) if f_rule else 0
    S = T0 + S_MAX + 1; NEG = -1e9
    dp = np.full((m, S), NEG); dp[:, T0] = 0.0
    back = np.zeros((n, m, S), dtype=np.int8)
    rows = np.arange(m); jbase = np.arange(S) - T0; gF = lu[0] - LOGU
    for i in range(n):
        c = C[i]; cx = Cx[i]
        j = np.clip(i + jbase, 0, L - 1); Kj = Ks[:, j]
        P = ((cx - Kj) if mode == "sub" else (Kj - cx)) % N
        if minv is not None: P = (minv[:, i][:, None] * P) % N
        gain = lu[P] - LOGU
        if free_first and i == 0: gain = np.zeros_like(gain)
        cand = dp + gain; src = np.zeros((m, S), dtype=np.int8)
        if i > 0 and rejection == "one":
            Kprev = Ks[:, np.clip(j - 1, 0, L - 1)]
            cond = ((c - C[i - 1]) - (Kj - Kprev)) % N == 0
            skip = np.full((m, S), NEG); skip[:, 1:] = np.where(cond[:, 1:], dp[:, :-1] + gain[:, 1:], NEG)
            take = skip > cand; cand = np.where(take, skip, cand); src = np.where(take, 1, src)
            Kprev2 = Ks[:, np.clip(j - 2, 0, L - 1)]
            cond2 = cond & (Kprev == Kprev2)
            skip2 = np.full((m, S), NEG); skip2[:, 2:] = np.where(cond2[:, 2:], dp[:, :-2] + gain[:, 2:], NEG)
            take = skip2 > cand; cand = np.where(take, skip2, cand); src = np.where(take, 2, src)
        elif i > 0 and rejection == "two":
            Kprev2 = Ks[:, np.clip(j - 2, 0, L - 1)]
            cond2 = ((c - C[i - 1]) - (Kj - Kprev2)) % N == 0
            skip2 = np.full((m, S), NEG); skip2[:, 2:] = np.where(cond2[:, 2:], dp[:, :-2] + gain[:, 2:], NEG)
            take = skip2 > cand; cand = np.where(take, skip2, cand); src = np.where(take, 2, src)
        if f_rule and c == 0:
            lit = np.full((m, S), NEG); lit[:, :-1] = dp[:, 1:] + gF
            take = lit > cand; cand = np.where(take, lit, cand); src = np.where(take, -1, src)
        dp = cand; back[i] = src
    best = dp.max(1); t_best = dp.argmax(1)
    out = np.zeros((m, n), dtype=np.int16); t = t_best.copy()
    for i in range(n - 1, -1, -1):
        c = C[i]; cx = Cx[i]
        src = back[i][rows, t]
        j = np.clip(i + (t - T0), 0, L - 1); Kj = Ks[rows, j]
        dec = ((cx - Kj) if mode == "sub" else (Kj - cx)) % N
        if minv is not None: dec = (minv[:, i] * dec) % N
        out[:, i] = np.where(src == -1, 0, dec)
        t = t - (src == 1) - 2 * (src == 2) + (src == -1)
    return best, t_best - T0, out


# ---------------------------------------------------------------- key material
def lcg_rows(a, c, m, L=LMAX):
    """One row per seed: x_1, x_2, ... mod 29 (the symbol after the first update, as the gate did)."""
    x = np.arange(m, dtype=np.int64); out = np.empty((m, L), dtype=np.int64)
    for n in range(L):
        x = (a * x + c) % m; out[:, n] = x % N
    return out


def dedupe(K, labels):
    _, idx = np.unique(K, axis=0, return_index=True); idx = np.sort(idx)
    return K[idx], [labels[i] for i in idx]


def clock_schedules():
    """All 812 (a, b): m_i = ((a*i + b) mod 28) + 1 for page positions i; returns (812, LMAX) inverses and labels."""
    i = np.arange(LMAX)
    M, labs = [], []
    for a in range(28):
        for b in range(29):
            M.append(INV[((a * i + b) % 28) + 1]); labs.append(f"m=((({a}i+{b}) mod 28)+1)")
    return np.stack(M), labs


_PR = sieve(400000)
def prime_gap(o, L=LMAX): return (_PR[o + 1:o + L + 1] - _PR[o:o + L]) % N


def rep(v, L=LMAX): return np.resize(np.asarray(v) % N, L)


# families: list of dicts {name, Ks (m,L), labels, minv (m,L) or None, feedback map or None, rejections, signs}
def build_families():
    fams = []
    # A
    K, lab = [], []
    for a, c in ((1033, 0), (3, 0), (7, 1)):
        K.append(lcg_rows(a, c, 3301)); lab += [f"lcg3301(a={a},c={c})@{s}" for s in range(3301)]
    K, lab = dedupe(np.concatenate(K), lab)
    fams.append(dict(name="A lcg mod 3301", Ks=K, labels=lab, minv=None, fb=None, rejections=("one",), signs=("add", "sub", "beaufort")))
    # B
    K, lab = dedupe(lcg_rows(3301 % 1033, 29, 1033), [f"lcg1033(a=202,c=29)@{s}" for s in range(1033)])
    fams.append(dict(name="B lcg mod 1033", Ks=K, labels=lab, minv=None, fb=None, rejections=("one", "two"), signs=("add", "sub", "beaufort")))
    # C
    K, lab = [], []
    for a in range(2, N):
        for c in range(N):
            K.append(lcg_rows(a, c, N)); lab += [f"lcg29(a={a},c={c})@{s}" for s in range(N)]
    K, lab = dedupe(np.concatenate(K), lab)
    fams.append(dict(name="C lcg mod 29", Ks=K, labels=lab, minv=None, fb=None, rejections=("one",), signs=("add", "sub", "beaufort")))
    # D
    MI, mlab = clock_schedules()
    K = np.concatenate([np.tile(rep(DIVINITY), (812, 1)), np.tile(rep(FIRFUMFERENFE), (812, 1))])
    lab = [f"DIVINITY {l}" for l in mlab] + [f"FIRFUMFERENFE {l}" for l in mlab]
    fams.append(dict(name="D word keys with clock multiplier", Ks=K, labels=lab, minv=np.concatenate([MI, MI]), fb=None, rejections=("one",), signs=("add", "sub", "beaufort")))
    # E
    offs = list(range(0, 101)) + [3301]
    K = np.concatenate([np.tile(prime_gap(o), (812, 1)) for o in offs]); lab = [f"gap[n+{o}] {l}" for o in offs for l in mlab]
    fams.append(dict(name="E prime-gap stream with clock multiplier", Ks=K, labels=lab, minv=np.tile(MI, (len(offs), 1)), fb=None, rejections=("one",), signs=("add",)))
    # F
    K = np.stack([np.take(plain, np.arange(o, o + LMAX), mode="wrap") for o in range(len(plain))]); lab = [f"plaintext@{o}" for o in range(len(plain))]
    for mp in ("prime_value", "totient_value"):
        fams.append(dict(name=f"F {mp} ciphertext feedback over the book text", Ks=K, labels=lab, minv=None, fb=mp, rejections=("one", "two"), signs=("add", "sub", "beaufort")))
    return fams


def prepared(C, fam, sign):
    """Decoder inputs for a page under a family and sign: (Ks, mode, Cx, free_first)."""
    Ks = fam["Ks"] if sign != "sub" else (-fam["Ks"]) % N
    mode = "beaufort" if sign == "beaufort" else "sub"
    Cx, free = None, False
    if fam["fb"]:
        f = MAPS[fam["fb"]]; prev = np.concatenate([[0], C[:-1]]); fv = f(prev)
        Cx = (C + fv) % N if sign == "sub" else (C - fv) % N; free = True   # C = P - f - S  ->  P = (C + f) + S
    return Ks, mode, Cx, free


def decode_family(C, fam, sign, f_rule, rejection, batch=4000):
    Ks, mode, Cx, free = prepared(C, fam, sign)
    m = len(Ks); scores = np.empty(m); skips = np.empty(m, dtype=int); tops = {}
    for b in range(0, m, batch):
        mi = None if fam["minv"] is None else fam["minv"][b:b + batch]
        s, t, out = decode_lane(C, Ks[b:b + batch], lu, f_rule, mode, mi, Cx, rejection, free)
        scores[b:b + batch] = s; skips[b:b + batch] = t
        for k in np.argsort(-s)[:2]: tops[b + k] = out[k]
    return scores, skips, tops


def null_scores(C, f_rule, mode, rejection, reps=2000):
    Ks = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2))
    return decode_lane(C, Ks, lu, f_rule, mode, None, None, rejection)[0]


# ---------------------------------------------------------------- encryptor for the controls
def encrypt_lane(P, K, sign, f_rule, mult=None, fb=None, soft=0.81, skip_by=1):
    C, j, prev = [], 0, None
    f = MAPS[fb] if fb else None
    for i, p in enumerate(P):
        if f_rule and p == 0: C.append(0); prev = 0; continue
        def c_of(j):
            k = int(K[j]) + (int(f(np.array(prev if prev is not None else 0))) if f else 0)
            mp = (int(mult[i]) if mult is not None else 1) * int(p)
            return (mp + k) % N if sign == "add" else ((mp - k) % N if sign == "sub" else (k - mp) % N)
        c = c_of(j)
        while prev is not None and c == prev and rng.random() < soft:
            j += skip_by; c = c_of(j)
        C.append(c); j += 1; prev = c
    return np.array(C)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, nargs=2, metavar=("I", "K"), help="process pages I::K and write results/shortlist_shard{I}.json")
    ap.add_argument("--merge", action="store_true", help="merge the shard files into results/shortlist.md")
    args = ap.parse_args()
    if args.merge: return merge()
    t0 = time.time()
    fams = build_families()
    shard_i, shard_k = args.shard if args.shard else (0, 1)
    my_pages = pages[shard_i::shard_k]
    for f in fams: print(f"{f['name']}: {len(f['Ks']):,} keystreams x {len(f['signs'])} signs x {len(f['rejections'])} rejection modes", flush=True)
    nconf = sum(len(f["Ks"]) * len(f["signs"]) * len(f["rejections"]) for f in fams)
    ntests = nconf * len(pages) * 2
    print(f"{nconf:,} configurations per page x {len(pages)} pages x 2 F variants = {ntests:,} tests; chance max ~ {np.sqrt(2*np.log(ntests)):.1f} sigma", flush=True)

    ctrl = []
    if shard_i != 0: print(f"shard {shard_i}/{shard_k}: {len(my_pages)} pages, controls and checks run in shard 0", flush=True)
    # decoder identity check against score.decode (no hooks)
    C0 = pages[0][1]; Kt = rng.integers(0, N, (40, LMAX))
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            for rj in ("one", "two"):
                a = decode(C0, Kt, lu, f_rule, mode, rejection=rj); b = decode_lane(C0, Kt, lu, f_rule, mode, None, None, rj)
                assert np.allclose(a[0], b[0]) and (a[1] == b[1]).all() and (a[2] == b[2]).all(), (f_rule, mode, rj)
    print("decode_lane == score.decode without hooks: ok", flush=True)
    # does a multiplier schedule or a feedback-corrected ciphertext change the random-keystream null?  (it should not)
    base = null_scores(C0, False, "sub", "one", 1000)
    MI, _ = clock_schedules()
    Kr = rng.integers(0, N, (1000, LMAX)); mi = MI[rng.integers(0, 812, 1000)]
    alt = decode_lane(C0, Kr, lu, False, "sub", mi, None, "one")[0]
    Cx = (C0 - MAPS["prime_value"](np.concatenate([[0], C0[:-1]]))) % N
    alt2 = decode_lane(C0, Kr, lu, False, "sub", None, Cx, "one", True)[0]
    print(f"null check on {pages[0][0]}: plain {base.mean():.1f} ± {base.std():.1f}; with multiplier schedules {alt.mean():.1f} ± {alt.std():.1f}; with feedback-corrected C {alt2.mean():.1f} ± {alt2.std():.1f}", flush=True)

    # ---------- controls: two plants per family
    for fi, fam in enumerate(fams if shard_i == 0 else []):
        for ci in range(2):
            sign = fam["signs"][(fi + ci) % len(fam["signs"])]; f_rule = bool((fi + ci) % 2); rj = fam["rejections"][ci % len(fam["rejections"])]
            ki = int(rng.integers(0, len(fam["Ks"])))
            o = int(rng.integers(0, len(plain) - 240)); P = plain[o:o + 240]
            mult = None if fam["minv"] is None else INV[fam["minv"][ki]]          # the forward multipliers
            C = encrypt_lane(P, fam["Ks"][ki], sign, f_rule, mult, fam["fb"], 0.81, 1 if rj == "one" else 2)
            Ks, mode, Cx, free = prepared(C, fam, sign)
            nul = null_scores(C, f_rule, mode, rj, 500)
            sc, sk, tops = decode_family(C, fam, sign, f_rule, rj)
            z = (sc - nul.mean()) / nul.std(); rank = int((z > z[ki]).sum()) + 1
            mi = None if fam["minv"] is None else fam["minv"][ki:ki + 1]
            rec = decode_lane(C, Ks[ki:ki + 1], lu, f_rule, mode, mi, Cx, rj, free)[2][0]
            row = [fam["name"], sign, f_rule, rj, fam["labels"][ki], float(z[ki]), rank, float((rec == P).mean()), float(z.max())]
            ctrl.append(row)
            print(f"  control {fam['name'][:2]} {sign} F={f_rule} {rj} '{fam['labels'][ki][:40]}': z {z[ki]:.1f}, rank {rank}, recovered {row[7]:.3f}, best z in family {z.max():.1f}", flush=True)
    print(f"controls done in {time.time()-t0:.0f}s", flush=True)

    # ---------- the sweep
    results = []; nulls = {}
    t1 = time.time()
    for pi, (pid, C) in enumerate(my_pages):
        best_page = -9
        for f_rule in (False, True):
            nul_cache = {}
            for fam in fams:
                for sign in fam["signs"]:
                    mode = "beaufort" if sign == "beaufort" else "sub"
                    for rj in fam["rejections"]:
                        key = (mode, rj)
                        if key not in nul_cache: nul_cache[key] = null_scores(C, f_rule, mode, rj)
                        nul = nul_cache[key]; nulls[f"{pid}|{f_rule}|{mode}|{rj}"] = (float(nul.mean()), float(nul.std()), float(nul.max()))
                        sc, sk, tops = decode_family(C, fam, sign, f_rule, rj)
                        z = (sc - nul.mean()) / nul.std()
                        for k in np.argsort(-z)[:2]:
                            results.append((pid, fam["name"], sign, f_rule, rj, fam["labels"][k], float(z[k]), int(sk[k]), translit(tops[k][:80]) if k in tops else ""))
                        best_page = max(best_page, float(z.max()))
        print(f"  {pid} done ({pi+1}/{len(my_pages)}), best z {best_page:.2f}  [{time.time()-t1:.0f}s]", flush=True)
        json.dump({"ntests": ntests, "controls": ctrl, "results": sorted(results, key=lambda r: -r[6]), "nulls": nulls, "pages_done": pi + 1, "shard": [shard_i, shard_k],
                   "families": [(f["name"], len(f["Ks"]), list(f["signs"]), list(f["rejections"])) for f in fams], "nconf": nconf, "seconds": time.time() - t0},
                  open(RESULTS / f"shortlist_shard{shard_i}.json", "w"), indent=1)
    print(f"shard {shard_i}/{shard_k} done in {(time.time()-t0)/60:.0f} min", flush=True)
    if shard_k == 1: merge()


def merge():
    import glob
    shards = [json.load(open(f)) for f in sorted(glob.glob(str(RESULTS / "shortlist_shard*.json")))]
    assert shards, "no shard files"
    pages_done = sum(s["pages_done"] for s in shards)
    ctrl = next((s["controls"] for s in shards if s["controls"]), [])
    results = sorted((tuple(r) for s in shards for r in s["results"]), key=lambda r: -r[6])
    nulls = {k: v for s in shards for k, v in s["nulls"].items()}
    fams = [dict(name=n, n=k, signs=sg, rejections=rj) for n, k, sg, rj in shards[0]["families"]]
    nconf = shards[0]["nconf"]; ntests = nconf * len(pages) * 2
    wall = max(s["seconds"] for s in shards) / 60
    zmax = results[0][6]
    out = ["# Short-list lane: the hypothesis loop's surviving finite families under the skip decoder", "",
           f"Families and sizes: " + "; ".join(f"{f['name']} ({f['n']:,} keystreams, signs {'/'.join(f['signs'])}, rejection {'/'.join(f['rejections'])})" for f in fams) + ".",
           f"{nconf:,} configurations per page x {len(pages)} pages x 2 F variants = **{ntests:,} tests** ({pages_done} of {len(pages)} pages done); chance maximum about {np.sqrt(2*np.log(ntests)):.1f}. "
           "Per page, F variant, decoder mode and rejection mode the null is 2,000 random keystreams through the same decoder. Pre-registered rule: z >= 6 over that null and readable English.", "",
           "Decoder: `decode_lane` in `src/shortlist_lane.py`, score.decode's Viterbi with a per-position multiplier inverse and a feedback-corrected ciphertext; identical to score.decode without the hooks (asserted at run time). "
           "The random-keystream null is unchanged by either hook (checked on one page at run time, see `results/shortlist.log`).", "",
           "## Planted controls (soft skip 0.81, two per family)", "",
           "| family | sign | F | rejection | planted key | z of true key | rank in family | runes recovered | best z in family |", "|---|---|---|---|---|---|---|---|---|"]
    for r in ctrl: out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4][:45]} | {r[5]:.1f} | {r[6]} | {r[7]:.3f} | {r[8]:.1f} |")
    out += ["", f"Controls recovered at z >= 6 and rank 1: {sum(1 for r in ctrl if r[5] >= 6 and r[6] == 1)} of {len(ctrl)}.", "",
            "## Unsolved pages: top 25 configurations overall", "",
            "| page | family | sign | F | rejection | key | z | skips | transliteration (first 80 runes) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in results[:25]: out.append(f"| {r[0]} | {r[1][:34]} | {r[2]} | {r[3]} | {r[4]} | {r[5][:45]} | {r[6]:.2f} | {r[7]} | {r[8]} |")
    out += ["", "## Per family: largest z over all pages", "", "| family | largest z | page | key |", "|---|---|---|---|"]
    for fam in fams:
        rr = max((r for r in results if r[1] == fam["name"]), key=lambda r: r[6])
        out.append(f"| {fam['name']} | {rr[6]:.2f} | {rr[0]} | {rr[5][:45]} |")
    out += ["", f"Largest z over all {ntests:,} tests: {zmax:.2f} ({results[0][0]}, {results[0][1]}, '{results[0][5][:45]}').", "", "## Verdict", "",
            ("**No page decrypts.** " if zmax < 6 else "**At least one configuration clears z = 6: inspect the transliteration above before believing it.** ") +
            "The six families the hypothesis loop left standing (LCG seeds mod 3301, 1033 and 29; the two published word keys and the prime-gap stream with every clock multiplier; "
            "Gematria prime-value and totient-value ciphertext feedback over the book's own text at every offset), under the soft reject-on-repeat rule at the stated sign conventions "
            "and both F variants, are excluded at the sensitivity the controls demonstrate.", f"", f"Wall time {wall:.0f} min (longest shard)."]
    (RESULTS / "shortlist.md").write_text("\n".join(out) + "\n")
    json.dump({"ntests": ntests, "controls": ctrl, "results": results[:300], "nulls": nulls, "pages_done": pages_done}, open(RESULTS / "shortlist.json", "w"), indent=1)
    print("\n".join(out[-8:]), flush=True)


if __name__ == "__main__":
    main()
