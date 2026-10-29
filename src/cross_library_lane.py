"""Cross-library lane (2026-10-28, §54): pnotisdev's keystream library under this repository's decoders.  Pre-registered.

THE GAP.  Every lab's key material has met only its own decoder.  pnotisdev screened a library of 1,447 streams (number
theory, constants, Cicada numbers, hash counters of Cicada strings, keyword keys of the solved pages) at every start offset
on the first 300 runes of the 8 unsolved sections with a flat-IoC / bigram engine under two anti-repeat models (registry rows
lib-sections, multipliers, hyp-streams, open-h1; 409 M + 5.7 G decodes; 0 verified hits).  This repository decoded only the
book's own words, phrases, sentences and a few hundred streams, with the exact skip Viterbi (§9, §12), the free-null decoder
(§22) and the echo-aware decoder (§48).  Here their library (rebuilt from their generator definitions, src/pnotisdev_library.py)
goes through this repository's three decoders.

LIBRARY.  Every stream of their KSB1 export: 20,000 values each; periodic streams (keywords, cycles) at every offset of one period,
non-periodic streams at every start offset 0 .. 20,000 - 327 (327 = longest page + the decoder's key margin), so that the
same offset can be re-decoded on the full page.  "Every offset they used" is this set (their windows were 300 runes).

DECODERS AND TIERS (the two-tier form of §31 / §44; the hold decoder is 3-4 times slower and needs longer windows, §23):
  plain  score.decode, soft skip rule (phases 3-9).        Tier 1: first 80 runes of LP2-00, LP2-01, LP2-02; every offset.
  echo   score.decode with echo_mask / echo_gain (§48, spent echoes at the positions where c_i = c_(i-5) or c_i = 24 - 2 c_(i-6)
         inside a word; LP2-00/01/02 carry 3, 1 and 2 such positions in their first 80 runes).  Tier 1 as plain.
  hold   score.decode with null_mask at every position, prior -0.8 (§22's free-null decoder: a rune may be an unkeyed null that
         consumes no key value).  Tier 1: first 160 runes of the same three pages (80 % power at 160 runes, §23); every offset of
         the periodic streams and offsets 0 .. 999 of the non-periodic ones (a stream started at the section's first rune reaches
         LP2-02 at offset 528 + skips; pnotisdev's own H1 slice used 2,000 offsets).  Stated as a coverage limit.
  Each tier-1 cell: 3 signs (C = P + K, C = P - K, C = K - P) x 2 F variants (literal F or not).  A cell survives tier 1 at
  z >= 4.5 over that window's null of 2,000 random keystreams through the same decoder.
  Tier 2: the survivor's full page under all three decoders.  Candidate rule: plain / echo: z_uni >= 6 over the full-page null
  AND rune 5-gram z_5 >= 6 AND readable; hold: z_uni >= 6 AND free-null score at least 20 nats above the plain decoder's score for
  the same key (§22's rule; §27 showed the 5-gram is the wrong second statistic when nulls break the n-grams) AND readable.
  A candidate stream is then decoded on every page at every offset of its tier (plain / echo) or offsets 0 .. 999 (hold).
CONTROLS (fixed before the run; 6 per decoder = 18): 262 runes of English encrypted under the matching mechanism with a stream from
their library at a random offset (4 non-periodic + 2 periodic streams of period >= 8 per decoder; signs and F cycled): plain = soft skip rule
q 0.81 (solved plaintext); echo = E56w spent echoes, r 0.5 (English in its own words, as §48); hold = hard rule with uniform nulls
at 0.22 (as §22).  A control passes when its tier-1 window finds the true offset at rank 1 among the stream's 4,096 neighbouring
offsets (periodic streams: among every offset of every periodic stream) with z >= 4.5, and tier 2 meets the candidate rule.
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/cross_library_lane.py (shards split the streams); MERGE=1 -> results/cross_library.md;
       SMOKE=1 for a quick check (3 streams, 300 offsets, 2 controls per decoder, 200 nulls).
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, LOGU
from skip_decrypt import encrypt, combine
import families as F, ngram, corpus, pnotisdev_library as PL

SMOKE = os.environ.get("SMOKE") == "1"; CONTROLS_ONLY = os.environ.get("CONTROLS_ONLY") == "1"
SHARD, NSHARD, MERGE = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)), os.environ.get("MERGE") == "1"
rng = np.random.default_rng(1447 + SHARD)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
EDGES = json.load(open(PROCESSED / "edges.json"))
T1_PAGES = [0, 1, 2]; WIN, WIN_H = 80, 160
Z_T1, Z_UNI, Z_5, NREPS = 4.5, 6.0, 6.0, (200 if SMOKE else 2000)
PEN, R_GATE, Q_SOFT, Q_NULL, FREE_BASE = -0.8, 0.5, 0.81, 0.22, 20.0
GAIN = float(np.log(R_GATE * 0.062) - LOGU)
HOLD_OFFSETS = 1000
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
DECODERS = ("plain", "echo", "hold")
MARGIN = max(len(C) for _, C in pages) + S_MAX + 2
T = lambda x: (24 - 2 * x) % N
names, fams, periods, K = PL.load()
LEN = K.shape[1]
NONPER = [i for i, p in enumerate(periods) if not p]; PER = [i for i, p in enumerate(periods) if p]
PER_CTRL = [i for i in PER if periods[i] >= 8]      # control plants use keyword keys of at least 8 runes
RES = RESULTS


def offsets_of(i, hold=False):
    p = periods[i]
    if p: return np.arange(min(p, LEN - MARGIN))
    n = LEN - MARGIN if not SMOKE else 300
    return np.arange(min(n, HOLD_OFFSETS) if hold else n)


def keyrows(i, offs, L):
    offs = np.asarray(offs, dtype=np.int64); return K[i].astype(np.int64)[offs[:, None] + np.arange(L)[None, :]]


def word_ids(pid, n):
    w = np.zeros(n, int)
    for i in EDGES[pid]["word_initial"]: w[i:] += 1
    return w


def echo_mask_of(C, w):
    m = np.zeros(len(C), int); pos = np.zeros(len(C), int)
    for i in range(1, len(C)): pos[i] = pos[i - 1] + 1 if w[i] == w[i - 1] else 0
    for i in range(len(C)):
        if pos[i] >= 5 and C[i] == C[i - 5]: m[i] = 5
        elif pos[i] >= 6 and C[i] == T(C[i - 6]): m[i] = 6
    return m


def dec(C, Ks, f_rule, mode, variant, mask=None):
    if variant == "plain": return decode(C, Ks, lu, f_rule, mode)
    if variant == "echo": return decode(C, Ks, lu, f_rule, mode, echo_mask=mask, echo_gain=GAIN)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, null_mask=nm, penalty=PEN)


def null_stats(C, f_rule, mode, variant, mask, reps=NREPS, with5=False, batch=500):
    sc, dcs = [], []
    for b in range(0, reps, batch):
        Kr = rng.integers(0, N, size=(min(batch, reps - b), len(C) + S_MAX + 2)); s, _, d = dec(C, Kr, f_rule, mode, variant, mask); sc.append(s); dcs.append(d)
    sc = np.concatenate(sc)
    if not with5: return float(sc.mean()), float(sc.std())
    s5 = ngram.score_batch(np.concatenate(dcs), T5); return float(sc.mean()), float(sc.std()), float(s5.mean()), float(s5.std())


# ---------- plants
text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(wd) for wd in text.split()]; EW = [wd for wd in EW if wd]


def encrypt_echo(n, Kst, sign, f_rule, r=R_GATE, q=Q_SOFT):
    wi = int(rng.integers(0, len(EW) - 500)); P, W = [], []; k = 0
    while len(P) < n:
        wd = EW[wi]; wi += 1; P += wd; W += [k] * len(wd); k += 1
    P, W = np.array(P[:n]), np.array(W[:n])
    C = np.empty(n, int); j = 0; prev = -1; pos = 0; active = False; n_echo = 0
    for i in range(n):
        if i == 0 or W[i] != W[i - 1]: pos = 0; active = rng.random() < r
        else: pos += 1
        p = P[i]
        if active:
            x = -1
            if pos >= 5 and P[i - 5] == p: x = C[i - 5]
            elif pos >= 6 and P[i - 6] == p: x = T(C[i - 6])
            if x != -1 and x != prev: C[i] = x; prev = x; n_echo += 1; j += 1; continue
        if f_rule and p == 0: C[i] = 0; prev = 0; continue
        c = combine(p, Kst[j], sign)
        while prev != -1 and c == prev and rng.random() < q: j += 1; c = combine(p, Kst[j], sign)
        C[i] = c; prev = c; j += 1
    return C, P, W, n_echo


def encrypt_nulls(P, Kst, f_rule, sign, q=Q_NULL):
    n = len(P); C, j, pi, prev, nulls = [], 0, 0, None, 0
    while len(C) < n and pi < len(P):
        p = P[pi]; pi += 1
        if f_rule and p == 0: C.append(0); prev = 0
        else:
            c = combine(p, Kst[j], sign)
            while prev is not None and c == prev: j += 1; c = combine(p, Kst[j], sign)
            C.append(c); j += 1; prev = c
        if len(C) < n and rng.random() < q: C.append(int(rng.integers(0, N))); prev = C[-1]; nulls += 1
    return np.array(C), nulls


# ---------- merge
if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RES.glob("cross_library_shard*.json"))]
    ctr = [c for d in shards for c in d["controls"]]; surv = [s for d in shards for s in d["survivors"]]; cands = [c for d in shards for c in d["candidates"]]
    nt1 = {v: sum(d["ntests_t1"][v] for d in shards) for v in DECODERS}; nt2 = sum(d["ntests_t2"] for d in shards)
    rows = {v: sum(d["rows"][v] for d in shards) for v in DECODERS}
    zmax = {v: max(d["zmax"][v] for d in shards) for v in DECODERS}
    nstreams = sum(d["nstreams"] for d in shards)
    if (RES / "cross_library_controls.json").exists(): ctr = json.load(open(RES / "cross_library_controls.json"))["controls"]   # the same plants, rerun with the outranking rows recorded
    out = [f"# Cross-library lane: pnotisdev's {len(names)} keystreams under this repository's three decoders", "",
           f"Library rebuilt from their generator definitions (`src/pnotisdev_library.py`, manifest `data/processed/pnotisdev_library_manifest.tsv`): {len(NONPER)} non-periodic streams of 20,000 values and {len(PER)} periodic ones. Streams swept: {nstreams}.",
           f"(stream, offset) rows: plain {rows['plain']:,}, echo {rows['echo']:,}, hold {rows['hold']:,} (hold: periodic streams at every offset, non-periodic at offsets 0-{HOLD_OFFSETS-1}).",
           f"Tier 1 (first 80 runes of LP2-00/01/02, 160 for hold; 3 signs x 2 F): plain {nt1['plain']:,}, echo {nt1['echo']:,}, hold {nt1['hold']:,} window decodes; survivors at z >= {Z_T1}: {len(surv)}. Tier 2: {nt2:,} full-page decodes (three decoders each). Candidates: {len(cands)}. Rule in the module docstring.", "",
           "## Controls", "", "| decoder | stream | offset | sign | F | tier-1 z (rank) | outranked by | tier-2 z_uni | z_5 | free − base | pass |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in ctr:
        ob = "—" if c["rank1"] == 1 else ("; ".join(f"{s_[:24]} @{o}" if s_ != c["stream"] else f"own offset {o:+d}".replace("+", "+") for s_, o in [(s_, o - c["offset"]) for s_, o in c.get("beaten_by", [])]) or "not recorded")
        out.append(f"| {c['variant']} | {c['stream'][:40]} | {c['offset']} | {c['sign']} | {c['F']} | {c['z1']:.1f} ({c['rank1']}) | {ob} | {c['z2']:.1f} | {c['z5']:.1f} | {c['fb']:+.1f} | {'yes' if c['passed'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['passed'] for c in ctr)} of {len(ctr)} (" + ", ".join(f"{v} {sum(c['passed'] for c in ctr if c['variant']==v)}/{sum(1 for c in ctr if c['variant']==v)}" for v in DECODERS) + ").", "",
            "## Tier-1 survivors (top 25 by tier-2 z_uni of the finding decoder)", "", "| decoder | stream | offset | page | sign | F | tier-1 z | tier-2 z_uni plain / echo / hold | z_5 | free − base | transliteration |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s_ in sorted(surv, key=lambda r: -r["z2"][r["variant"]])[:25]:
        out.append(f"| {s_['variant']} | {s_['stream'][:40]} | {s_['offset']} | {s_['page']} | {s_['sign']} | {s_['F']} | {s_['z1']:.2f} | {s_['z2']['plain']:.2f} / {s_['z2']['echo']:.2f} / {s_['z2']['hold']:.2f} | {s_['z5'][s_['variant']]:.1f} | {s_['fb']:+.1f} | {s_['translit'][:50]} |")
    out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["",
            "Largest tier-1 z per decoder: " + ", ".join(f"{v} {zmax[v]:.2f}" for v in DECODERS) + f". Largest tier-2 z_uni: {max((s_['z2'][s_['variant']] for s_ in surv), default=0):.2f}; largest z_5: {max((s_['z5'][s_['variant']] for s_ in surv), default=0):.2f}.",
            f"Runtime, longest shard: {max(d['seconds'] for d in shards)/3600:.1f} hours on {len(shards)} shards.", ""]
    (RES / "cross_library.md").write_text("\n".join(out) + "\n")
    json.dump(dict(ntests=sum(nt1.values()) + nt2, ntests_t1=nt1, ntests_t2=nt2, rows=rows, nstreams=nstreams, library=len(names), nonperiodic=len(NONPER), periodic=len(PER),
                   controls=ctr, survivors=surv, candidates=cands, zmax=zmax, hold_offsets=HOLD_OFFSETS, z_t1=Z_T1, z_uni=Z_UNI, z_5=Z_5, pen=PEN, gain=GAIN), open(RES / "cross_library.json", "w"), indent=1)
    print("\n".join(out[:5] + out[-3:])); sys.exit(0)

T5 = ngram.load_dense()
t0 = time.time()
my = list(range(len(names)))[SHARD::NSHARD]
if SMOKE: my = [NONPER[0], [i for i in NONPER if fams[i] == "hash"][0], PER[0]]
rows_plan = {"plain": sum(len(offsets_of(i)) for i in my), "hold": sum(len(offsets_of(i, True)) for i in my)}; rows_plan["echo"] = rows_plan["plain"]
print(f"shard {SHARD}/{NSHARD}: {len(my)} streams; rows plain/echo {rows_plan['plain']:,}, hold {rows_plan['hold']:,}; tier-1 decodes {rows_plan['plain']*36 + rows_plan['hold']*18:,}", flush=True)

# window and full-page nulls for the tier-1 pages, per decoder
MASK = {pi_: echo_mask_of(pages[pi_][1], word_ids(pages[pi_][0], len(pages[pi_][1]))) for pi_ in T1_PAGES}
WNULL, FULL = {}, {}
for pi_ in T1_PAGES:
    pid, C = pages[pi_]
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"):
            for v in DECODERS:
                w = WIN_H if v == "hold" else WIN
                WNULL[(pi_, f_rule, mode, v)] = null_stats(C[:w], f_rule, mode, v, MASK[pi_][:w])
                FULL[(pi_, f_rule, mode, v)] = null_stats(C, f_rule, mode, v, MASK[pi_], with5=True)
print(f"nulls ready [{time.time()-t0:.0f}s]", flush=True)


def tier1(i, offs, pi_, sign, mode, f_rule, variant):
    pid, C = pages[pi_]; w = WIN_H if variant == "hold" else WIN
    Ks = keyrows(i, offs, w + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
    m0, s0 = WNULL[(pi_, f_rule, mode, variant)]; sc = dec(C[:w], Ks, f_rule, mode, variant, MASK[pi_][:w])[0]
    return (sc - m0) / s0


def tier2(i, off, pi_, sign, mode, f_rule):
    """Full page under all three decoders at this offset: z_uni per decoder, z_5 per decoder, free - base, transliteration (finding decoder's is picked by the caller)."""
    pid, C = pages[pi_]; Ks = keyrows(i, [off], len(C) + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
    z2, z5, tr, raw = {}, {}, {}, {}
    for v in DECODERS:
        m0, s0, m5, s5 = FULL[(pi_, f_rule, mode, v)]; sc, _, d = dec(C, Ks, f_rule, mode, v, MASK[pi_])
        z2[v] = float((sc[0] - m0) / s0); z5[v] = float((ngram.score_batch(d, T5)[0] - m5) / s5); tr[v] = translit(d[0][:80]); raw[v] = float(sc[0])
    return z2, z5, tr, raw["hold"] - raw["plain"]


def is_candidate(variant, z2, z5, fb):
    return z2[variant] >= Z_UNI and ((z5[variant] >= Z_5) if variant != "hold" else (fb >= FREE_BASE))


def all_pages(i, sign, mode, f_rule, variant):
    """A candidate stream on every page: best offset per page under the finding decoder (offsets of its tier)."""
    out = []
    for pi_, (pid, C) in enumerate(pages):
        mask = echo_mask_of(C, word_ids(pid, len(C))); m0, s0 = null_stats(C, f_rule, mode, variant, mask, reps=400)
        offs = offsets_of(i, variant == "hold"); best = (-9, -1)
        for b in range(0, len(offs), 1024):
            Ks = keyrows(i, offs[b:b + 1024], len(C) + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
            z = (dec(C, Ks, f_rule, mode, variant, mask)[0] - m0) / s0; k = int(z.argmax())
            if z[k] > best[0]: best = (float(z[k]), int(offs[b + k]))
        out.append(dict(page=pid, z=best[0], offset=best[1]))
    return out


# ---------- controls (shard 0 / smoke)
controls = []
if SHARD == 0:
    ncon = 2 if SMOKE else 6
    for v in DECODERS:
        for ci in range(ncon):
            sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 3) % 2); periodic = ci >= 4
            i = int(rng.choice(PER_CTRL if periodic else NONPER)); n = 262
            offs_all = offsets_of(i, v == "hold"); off = int(rng.choice(offs_all))
            Kst = K[i].astype(np.int64)[off:off + n + S_MAX + 2] if not periodic else np.take(K[i].astype(np.int64), np.arange(off, off + n + S_MAX + 2), mode="wrap")
            if v == "plain":
                o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]; C = encrypt(P, Kst, f_rule=f_rule, rng=rng, soft=Q_SOFT, mode=sign); W = None
            elif v == "echo":
                C, P, W, n_echo = encrypt_echo(n, Kst, sign, f_rule)
            else:
                o = int(rng.integers(0, len(plain) - n - 1)); C, nnul = encrypt_nulls(plain[o:o + n], Kst, f_rule, sign)
            w = WIN_H if v == "hold" else WIN
            mask = echo_mask_of(C, W) if v == "echo" else np.zeros(len(C), int)
            # tier 1: the plant's window against the stream's neighbouring offsets (or every periodic row)
            if periodic:
                cand = [(j, o_) for j in PER for o_ in offsets_of(j)]; Ks = np.concatenate([keyrows(j, [o_], w + S_MAX + 2) for j, o_ in cand]); pos = cand.index((i, off))
            else:
                lo = max(0, off - 2048); block = np.arange(lo, min(lo + 4096, len(offs_all))); pos = int(np.where(block == off)[0][0]); Ks = keyrows(i, block, w + S_MAX + 2)
            Ks = (-Ks) % N if sign == "add" else Ks
            m0, s0 = null_stats(C[:w], f_rule, mode, v, mask[:w], reps=400); z1 = np.empty(len(Ks))
            for b in range(0, len(Ks), 2048): z1[b:b + 2048] = (dec(C[:w], Ks[b:b + 2048], f_rule, mode, v, mask[:w])[0] - m0) / s0
            rank1 = int((z1 > z1[pos]).sum()) + 1
            above = [int(x) for x in np.where(z1 > z1[pos])[0]]       # the rows that outrank the plant: its own neighbouring offsets, or another stream
            beaten = [(names[cand[x][0]], int(cand[x][1])) if periodic else (names[i], int(block[x])) for x in above]
            # tier 2: the full plant
            m0f, s0f, m5, s5 = null_stats(C, f_rule, mode, v, mask, reps=400, with5=True); Kf = Ks[pos:pos + 1]
            Kf = keyrows(i, [off], n + S_MAX + 2) if not periodic else np.take(K[i].astype(np.int64), np.arange(off, off + n + S_MAX + 2), mode="wrap")[None, :]
            Kf = (-Kf) % N if sign == "add" else Kf
            sc, _, d = dec(C, Kf, f_rule, mode, v, mask); z2 = float((sc[0] - m0f) / s0f); z5 = float((ngram.score_batch(d, T5)[0] - m5) / s5)
            fb = float(sc[0] - dec(C, Kf, f_rule, mode, "plain")[0][0]) if v == "hold" else 0.0
            passed = z1[pos] >= Z_T1 and rank1 == 1 and z2 >= Z_UNI and ((z5 >= Z_5) if v != "hold" else (fb >= FREE_BASE))
            controls.append(dict(variant=v, stream=names[i], offset=off, periodic=periodic, sign=sign, F=f_rule, z1=float(z1[pos]), rank1=rank1, z2=z2, z5=z5, fb=fb, passed=bool(passed), beaten_by=beaten))
            print(f"  control {v} {names[i][:30]!r} off {off} {sign} F={f_rule}: tier1 z {z1[pos]:.1f} rank {rank1} of {len(Ks)}; tier2 z_uni {z2:.1f} z_5 {z5:.1f} free-base {fb:+.1f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

if CONTROLS_ONLY:
    json.dump(dict(controls=controls), open(RES / "cross_library_controls.json", "w"), indent=1); print("controls written"); sys.exit(0)

# ---------- the sweep
survivors, candidates = [], []
nt1 = {v: 0 for v in DECODERS}; nt2 = 0; zmax = {v: -9.0 for v in DECODERS}; rows = {v: 0 for v in DECODERS}
for si_, i in enumerate(my):
    for v in DECODERS:
        offs = offsets_of(i, v == "hold"); rows[v] += len(offs); B = 1024 if v == "hold" else 2048
        for b in range(0, len(offs), B):
            ob = offs[b:b + B]
            for pi_ in T1_PAGES:
                for sign, mode in SIGNS:
                    for f_rule in (False, True):
                        z = tier1(i, ob, pi_, sign, mode, f_rule, v); nt1[v] += len(ob); zmax[v] = max(zmax[v], float(z.max()))
                        for k in np.where(z >= Z_T1)[0]:
                            off = int(ob[k]); z2, z5, tr, fb = tier2(i, off, pi_, sign, mode, f_rule); nt2 += 1
                            row = dict(variant=v, stream=names[i], family=fams[i], offset=off, page=pages[pi_][0], sign=sign, F=f_rule, z1=float(z[k]), z2=z2, z5=z5, fb=float(fb), translit=tr[v])
                            survivors.append(row)
                            if is_candidate(v, z2, z5, fb):
                                row = dict(row, all_pages=all_pages(i, sign, mode, f_rule, v)); candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    if si_ % 10 == 0 or SMOKE:
        print(f"  [{si_+1}/{len(my)}] {names[i][:40]!r} ({fams[i]}, period {periods[i]}): tier-1 so far " + ", ".join(f"{v} {nt1[v]:,} (max z {zmax[v]:.2f})" for v in DECODERS) + f"; {len(survivors)} survivors, {len(candidates)} candidates  [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests_t1=nt1, ntests_t2=nt2, rows=rows, zmax=zmax, nstreams=len(my), streams=[names[i] for i in my], seconds=time.time() - t0),
          open(RES / ("cross_library_smoke.json" if SMOKE else f"cross_library_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} written: " + ", ".join(f"{v} {nt1[v]:,}" for v in DECODERS) + f" tier-1 decodes, {nt2} tier-2, {len(survivors)} survivors, {len(candidates)} candidates [{time.time()-t0:.0f}s]", flush=True)
