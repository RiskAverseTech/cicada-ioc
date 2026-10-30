"""§55 part C (2026-10-29): the filler sweep.  The external running-key texts and the rest of pnotisdev's non-periodic
offsets under the free-null decoder.  Pre-registered in results/filler_lane_registration.md; the prior and the go decision
come from part B (results/filler_power.json).

WHY.  The word-length fingerprint (part A) is best fit by filler runes inside words at about one in ten.  Part B measures
what that does to the decoders: the plain decoder loses the key (its power is the power the plain-decoder lanes §25, §40,
§53 had in a filler world), the free-null decoder keeps it.  §22 already ran the free-null decoder over the book's own
7,621 keys and §54 over pnotisdev's streams at offsets 0-999.  Not yet decoded in the filler world: the 16 external
running-key texts (every offset, both directions, texts <= 60,000 runes; sentence starts, forward, for the longer ones)
and pnotisdev's non-periodic streams at offsets 1,000-1,999.

TIERS (as §54's hold decoder).  Tier 1: the first 160 runes of LP2-00, LP2-01, LP2-02, 3 signs x 2 F variants, every offset in
scope, free-null decoder at the part-B prior; survive at z >= 4.5 over that window's null of 2,000 random keystreams through
the same decoder.  Tier 2: the survivor's full page; candidate at z_uni >= 6 over the full-page free-null null AND free-null
score at least 20 nats above the plain decoder's score for the same key (§22's rule) AND readable English.  Offsets within
+-3 in the same text and direction are one hypothesis.  A candidate is then decoded on every page at the found offset and
its +-2,000 neighbours.
CONTROLS (6, shard 0): 262 runes of English under the part-B mechanism (soft rule, fillers at 0.10) with a corpus text at a
random offset and direction, signs and F cycled; pass = tier 1 finds the true offset at rank 1 among the text's 4,096
neighbouring offsets with z >= 4.5 and tier 2 meets the candidate rule.
Usage: SHARD=k NSHARD=m .venv/bin/python -I src/filler_lane.py -> results/filler_lane_shard{k}.json; MERGE=1 -> results/filler_lane.md;
       SMOKE=1 for a quick check; CONTROLS_ONLY=1 for the controls alone; PRIOR=-0.8 overrides the part-B prior.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from lp import *
from score import decode, translit, S_MAX
from skip_decrypt import combine
import families as F, corpus, pnotisdev_library as PL

SMOKE = os.environ.get("SMOKE") == "1"; MERGE = os.environ.get("MERGE") == "1"; CONTROLS_ONLY = os.environ.get("CONTROLS_ONLY") == "1"
SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
rng = np.random.default_rng(5555 + SHARD)
lu = F.lu; pages = [(p, C) for p, C in F.pages if len(C) > 0]
RES = RESULTS; CORP = Path(__file__).resolve().parent.parent / "data" / "corpus"
PB = json.loads((RES / "filler_power.json").read_text()) if (RES / "filler_power.json").exists() else {}
PEN = float(os.environ.get("PRIOR", PB.get("prior", -0.8)))
T1_PAGES = [0, 1, 2]; WIN = 160; Z_T1, Z_UNI, FREE_BASE = 4.5, 6.0, 20.0
NREPS = 200 if SMOKE else 2000; NEIGH = 512 if SMOKE else 4096; CHUNK = 300 if SMOKE else 5000
LIMIT, PN_OFFS = 60_000, tuple(int(x) for x in os.environ.get("PN_OFFS", "1000,2000").split(","))
PN_ALL, TEXTS, OUT = os.environ.get("PN_ALL") == "1", os.environ.get("TEXTS", "1") == "1", os.environ.get("OUT", "filler_lane")   # B2 (2026-10-30): all 1,439 streams, offsets 0-999 (periodic ones below their period), no texts, own output prefix
R_FILL, Q_SOFT, CTRL_N = 0.10, 0.81, 262
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
MARGIN = max(len(C) for _, C in pages) + S_MAX + 2

# ---------- key material
texts = {}
for f in ("corpus.json", "corpus_pilgrim.json", "corpus_cicada.json"):
    for k, v in json.loads((CORP / f).read_text()).items(): texts[k] = (np.asarray(v["runes"], dtype=np.int64), np.asarray(v["sentence_starts"], dtype=np.int64))
EXACT = [k for k, (s, _) in texts.items() if len(s) <= LIMIT]; SENT = [k for k in texts if k not in EXACT]
names, fams, periods, KP = PL.load(); NONPER = [i for i, p in enumerate(periods) if not p]


def stream_of(kind, name, rev):
    if kind == "text": s = texts[name][0]; return s[::-1] if rev else s
    return KP[name].astype(np.int64)


def windows(s, offs, L):
    offs = np.asarray(offs, dtype=np.int64)
    if len(s) < offs.max() + L + 1: s = np.concatenate([s, s[:L + 1]])      # a text wraps on itself (as §25); pnotisdev streams never need it
    return sliding_window_view(s, L)[offs]


units = []                                      # (kind, name, rev, offsets)
for k in (EXACT if TEXTS else []):
    n = len(texts[k][0])
    for rev in (False, True):
        for a in range(0, n, CHUNK): units.append(("text", k, rev, np.arange(a, min(a + CHUNK, n))))
for k in (SENT if TEXTS else []): units.append(("text", k, False, texts[k][1]))
for i in (range(len(names)) if PN_ALL else NONPER):
    hi = min(PN_OFFS[1], periods[i]) if periods[i] else PN_OFFS[1]
    if hi > PN_OFFS[0]: units.append(("pn", i, False, np.arange(PN_OFFS[0], hi)))
if SMOKE: units = units[:2] + [u for u in units if u[0] == "pn"][:2]; units = [(k, n, r, o[:300]) for k, n, r, o in units]
mine = [u for j, u in enumerate(units) if j % NSHARD == SHARD]


def dec(C, Ks, f_rule, mode, free=True):
    if not free: return decode(C, Ks, lu, f_rule, mode)
    nm = np.ones(len(C), bool); nm[0] = False
    return decode(C, Ks, lu, f_rule, mode, None, nm, PEN)


def null_ms(C, f_rule, mode, reps=NREPS, batch=500):
    sc = []
    for b in range(0, reps, batch):
        Kr = rng.integers(0, N, size=(min(batch, reps - b), len(C) + S_MAX + 2)); sc.append(dec(C, Kr, f_rule, mode)[0])
    sc = np.concatenate(sc); return float(sc.mean()), float(sc.std())


# ---------- plants
text = corpus.TEXTS["emerson_essays1"][0](); EP = np.array(english_to_runes(text), dtype=np.int64)
def encrypt_fill(P, K, f_rule, sign, r, n):
    C, j, pi, prev = [], 0, 0, None
    while len(C) < n:
        p = int(P[pi]); pi += 1
        if f_rule and p == 0: C.append(0); prev = 0
        else:
            c = combine(p, K[j], sign)
            while prev is not None and c == prev and rng.random() < Q_SOFT: j += 1; c = combine(p, K[j], sign)
            C.append(int(c)); j += 1; prev = int(c)
        if len(C) < n and rng.random() < r:
            f = int(rng.integers(0, N - 1)); f = f if f < prev else f + 1; C.append(f); prev = f
    return np.array(C[:n])


# ---------- merge
if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RES.glob(f"{OUT}_shard*.json"))] or [json.loads((RES / "filler_lane_smoke.json").read_text())]
    ctr = [c for d in shards for c in d["controls"]]; surv = sorted([s for d in shards for s in d["survivors"]], key=lambda r: -r["z2"])
    cands = [c for d in shards for c in d["candidates"]]; nt = sum(d["ntests"] for d in shards); zmax1 = max(d["zmax1"] for d in shards)
    nunits = sum(d["nunits"] for d in shards); noffs = sum(d["noffs"] for d in shards); secs = max(d["seconds"] for d in shards)
    out = [f"# The filler sweep (§55 part C): external running-key texts and pnotisdev's remaining offsets under the free-null decoder", "",
           f"Decoder: free-null at prior {PEN:.1f} (part B: power {PB.get('power_230', float('nan')):.2f} at 230 runes for running keys with fillers at 0.10). Key material: {len(EXACT)} texts at every offset in both directions ({sum(len(texts[k][0]) for k in EXACT):,} runes), {len(SENT)} longer texts at {sum(len(texts[k][1]) for k in SENT):,} sentence starts (forward), and {len(NONPER)} non-periodic pnotisdev streams at offsets {PN_OFFS[0]:,}–{PN_OFFS[1]-1:,}: {noffs:,} offsets in {nunits} work units. Tier 1: first {WIN} runes of LP2-00/01/02 × 3 signs × 2 F = 18 cells per offset, **{nt:,} window decodes**; survive at z ≥ {Z_T1}. Tier 2: full page, candidate at z_uni ≥ {Z_UNI:.0f} and free − plain ≥ {FREE_BASE:.0f} nats and readable. Chance maximum of z over {nt:,} tests about {np.sqrt(2*np.log(max(nt,2))):.1f}.", "",
           "## Controls (soft rule 0.81, fillers at 0.10, corpus text at a random offset)", "",
           "| control | text | reversed | sign | F | planted offset | tier-1 top offset | tier-1 z | rank | tier-2 z_uni | free − plain | pass |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in ctr: out.append(f"| {c['id']} | {c['text']} | {c['rev']} | {c['sign']} | {c['F']} | {c['offset']} | {c['top']} | {c['z1']:.1f} | {c['rank']} | {c['z2']:.1f} | {c['fb']:+.0f} | {'yes' if c['pass'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['pass'] for c in ctr)} of {len(ctr)}.", "", "## Tier-1 survivors (top 25 by tier-2 z_uni)", "",
            "| source | reversed | page | sign | F | offset | tier-1 z | tier-2 z_uni | free − plain | transliteration (first 60) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for s in surv[:25]: out.append(f"| {s['name']} | {s['rev']} | {s['page']} | {s['sign']} | {s['F']} | {s['offset']} | {s['z1']:.2f} | {s['z2']:.2f} | {s['fb']:+.0f} | {s['tr'][:60]} |")
    out += ["", f"Survivors: {len(surv)}; largest tier-1 z {zmax1:.2f}; largest tier-2 z_uni {max((s['z2'] for s in surv), default=0):.2f}.", "", "## Candidates", ""]
    out += [f"- **{c['name']}** page {c['page']} {c['sign']} F={c['F']} offset {c['offset']}: z_uni {c['z2']:.2f}, free − plain {c['fb']:+.0f}: `{c['tr']}`" for c in cands] or ["None. No accepted decoding within the tested configurations at the stated detection limits."]
    out += ["", f"Coverage limits: window power at 160 runes from part B; the longer texts at sentence starts only; pnotisdev offsets ≥ {PN_OFFS[1]:,}; the free-null decoder at one prior. Runtime, longest shard: {secs/3600:.1f} h on {len(shards)} shards.", ""]
    (RES / f"{OUT}.md").write_text("\n".join(out)); json.dump(dict(ntests=nt, prior=PEN, controls=ctr, survivors=surv, candidates=cands, zmax1=zmax1), open(RES / f"{OUT}.json", "w"), indent=1)
    print("\n".join(out[:3] + out[-6:])); sys.exit(0)

t0 = time.time()
WNULL = {}; FULL = {}
for pi_ in T1_PAGES:
    for f_rule in (False, True):
        for mode in ("sub", "beaufort"): WNULL[(pi_, f_rule, mode)] = null_ms(pages[pi_][1][:WIN], f_rule, mode)
print(f"window nulls ready [{time.time()-t0:.0f}s]; prior {PEN:.1f}; {len(mine)} of {len(units)} units on this shard", flush=True)


def tier2(C, Kfull, f_rule, mode, key):
    if key not in FULL: FULL[key] = null_ms(C, f_rule, mode)
    m0, s0 = FULL[key]; s2, _, d = dec(C, Kfull, f_rule, mode); s1 = dec(C, Kfull, f_rule, mode, free=False)[0]
    return float((s2[0] - m0) / s0), float(s2[0] - s1[0]), translit(d[0][:80])


# ---------- controls
controls = []
if SHARD == 0 or SMOKE or CONTROLS_ONLY:
    for ci in range(6 if not SMOKE else 2):
        sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 3) % 2); tname = EXACT[ci % len(EXACT)]; rev = bool(ci % 2)
        s = stream_of("text", tname, rev); o = int(rng.integers(0, len(s))); L = CTRL_N + S_MAX + 2
        K = windows(s, [o], L)[0]; p0 = int(rng.integers(0, len(EP) - 2 * CTRL_N)); C = encrypt_fill(EP[p0:p0 + 2 * CTRL_N], K, f_rule, sign, R_FILL, CTRL_N)
        offs = np.arange(o - NEIGH // 2, o + NEIGH // 2) % len(s)
        m0, s0 = null_ms(C[:WIN], f_rule, mode); Ks = windows(s, offs, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
        z = (dec(C[:WIN], Ks, f_rule, mode)[0] - m0) / s0; k = int(z.argmax()); top = int(offs[k])
        near = np.abs(np.arange(NEIGH) - NEIGH // 2) <= 3; zt = float(z[near].max())          # offsets within +-3 are one hypothesis (registration)
        rank = int((z[~near] > zt).sum()) + 1
        Kf = windows(s, [o], len(C) + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
        z2, fb, tr = tier2(C, Kf, f_rule, mode, ("ctrl", ci))
        ok = bool(rank == 1 and zt >= Z_T1 and z2 >= Z_UNI and fb >= FREE_BASE)
        controls.append(dict(id=f"control-{ci:02d}", text=tname, rev=rev, sign=sign, F=f_rule, offset=o, top=top, z1=zt, rank=rank, z2=z2, fb=fb, tr=tr, **{"pass": ok}))
        print(f"  control {ci} {tname}{' rev' if rev else ''} {sign} F={int(f_rule)} planted {o}: top {top} z1 {zt:.1f} rank {rank} | z2 {z2:.1f} fb {fb:+.0f} -> {'PASS' if ok else 'miss'} [{time.time()-t0:.0f}s]", flush=True)
    print(f"controls: {sum(c['pass'] for c in controls)}/{len(controls)}", flush=True)
    if CONTROLS_ONLY:
        json.dump(dict(controls=controls), open(RES / "filler_lane_controls.json", "w"), indent=1); sys.exit(0)

# ---------- the sweep
survivors, candidates, ntests, zmax1, noffs = [], [], 0, -9.0, 0
for ui, (kind, name, rev, offs) in enumerate(mine):
    s = stream_of(kind, name, rev); label = name if kind == "text" else f"pn:{names[name]}"; noffs += len(offs)
    for pi_ in T1_PAGES:
        pid, C = pages[pi_]; Cw = C[:WIN]
        for f_rule in (False, True):
            for sign, mode in SIGNS:
                m0, s0 = WNULL[(pi_, f_rule, mode)]
                for b in range(0, len(offs), 1000):
                    ob = offs[b:b + 1000]; Ks = windows(s, ob, WIN + S_MAX + 2); Ks = (-Ks) % N if sign == "add" else Ks
                    z = (dec(Cw, Ks, f_rule, mode)[0] - m0) / s0; ntests += len(ob); zmax1 = max(zmax1, float(z.max()))
                    for k in np.flatnonzero(z >= Z_T1):
                        off = int(ob[k]); Kf = windows(s, [off], len(C) + S_MAX + 2); Kf = (-Kf) % N if sign == "add" else Kf
                        z2, fb, tr = tier2(C, Kf, f_rule, mode, (pi_, f_rule, mode))
                        row = dict(name=label, rev=rev, page=pid, sign=sign, F=f_rule, offset=off, z1=float(z[k]), z2=z2, fb=fb, tr=tr); survivors.append(row)
                        if z2 >= Z_UNI and fb >= FREE_BASE: candidates.append(row); print(f"  CANDIDATE {row}", flush=True)
    if ui % 5 == 0 or ui == len(mine) - 1: print(f"  unit {ui+1}/{len(mine)} {label}{' rev' if rev else ''} ({len(offs)} offsets): {ntests:,} tests, zmax1 {zmax1:.2f}, survivors {len(survivors)} [{time.time()-t0:.0f}s]", flush=True)

json.dump(dict(controls=controls, survivors=survivors, candidates=candidates, ntests=ntests, zmax1=zmax1, nunits=len(mine), noffs=noffs, seconds=time.time() - t0, prior=PEN),
          open(RES / (f"{OUT}_smoke.json" if SMOKE else f"{OUT}_shard{SHARD}.json"), "w"), indent=1)
print(f"shard {SHARD}/{NSHARD}: {ntests:,} tests, {len(survivors)} survivors, {len(candidates)} candidates, {time.time()-t0:.0f}s", flush=True)
