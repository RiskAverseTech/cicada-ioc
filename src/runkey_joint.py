"""English running keys as a class: a library-free joint decoder (2026-10-31; registration results/runkey_joint_registration.md).
Beam search over (plaintext context, key context) with the English 5-gram on both streams; soft skip modelled exactly; literal F
optional.  STAGE=plants | null | pages | merge.  Reproduce: STAGE=plants .venv/bin/python -I src/runkey_joint.py, then null, pages, merge.
"""
import os, re, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, N, english_to_runes
from score import translit
import ngram, families as F

t0 = time.time(); STAGE = os.environ.get("STAGE", "plants"); BEAM = int(os.environ.get("BEAM", 2000)); SMOKE = os.environ.get("SMOKE") == "1"
LOGQ = np.log(0.81); T = ngram.load_dense(); TF = [t.reshape(-1, N) for t in T]; P29 = [N ** m for m in range(5)]
SIGNS = {"sub": (lambda c, p: (c - p) % N), "add": (lambda c, p: (p - c) % N), "beaufort": (lambda c, p: (c + p) % N)}


def rows(ctx, m):
    """log P(w | last m runes) for each beam row; ctx the base-29 context integer (older rune most significant), m per row"""
    out = np.empty((len(ctx), N))
    for mm in np.unique(m):
        sel = m == mm; out[sel] = TF[mm][ctx[sel] % P29[mm]]
    return out


def decode_joint(C, sign, f_rule, beam=BEAM):
    C = np.asarray(C); n = len(C); f = SIGNS[sign]
    ctxp = np.zeros(1, np.int64); ctxk = np.zeros(1, np.int64); jk = np.zeros(1, np.int64); score = np.zeros(1); hist = []
    pv = np.arange(N)
    for i in range(n):
        c = int(C[i]); B = len(score); mp = np.full(B, min(i, 4)); mk = np.minimum(jk, 4)
        LP = rows(ctxp, mp)                                       # (B, 29) over p
        RK = rows(ctxk, mk); kv = f(c, pv); LK = RK[:, kv]        # key rune implied by p, no skip
        cand = [(score[:, None] + LP + LK, 0, kv)]
        if i > 0:                                                 # skip branch: the skipped key rune would have reproduced C[i-1]
            ks = f(int(C[i - 1]), pv); LS = RK[:, ks] + LOGQ
            ctx2 = (ctxk[:, None] * N + ks[None, :]) % P29[4]; m2 = np.minimum(jk + 1, 4)
            LK2 = np.empty((B, N))
            for p in range(N): LK2[:, p] = rows(ctx2[:, p], m2)[np.arange(B), kv[p]]
            cand.append((score[:, None] + LP + LS + LK2, 1, kv))
        tot = np.concatenate([x[0].ravel() for x in cand]); br = np.concatenate([np.full(B * N, x[1]) for x in cand])
        parent = np.tile(np.repeat(np.arange(B), N), len(cand)); psel = np.tile(np.tile(pv, B), len(cand))
        if f_rule and c == 0:                                     # literal F: plaintext F, key not consumed
            tot = np.concatenate([tot, score + LP[:, 0]]); br = np.concatenate([br, np.full(B, 2)]); parent = np.concatenate([parent, np.arange(B)]); psel = np.concatenate([psel, np.zeros(B, int)])
        # new states
        new_ctxp = (ctxp[parent] * N + psel) % P29[4]
        kused = f(c, psel); kskip = f(int(C[i - 1]), psel) if i > 0 else np.zeros_like(psel)
        new_ctxk = np.where(br == 0, (ctxk[parent] * N + kused) % P29[4], np.where(br == 1, ((ctxk[parent] * N + kskip) % P29[4] * N + kused) % P29[4], ctxk[parent]))
        new_jk = jk[parent] + np.where(br == 0, 1, np.where(br == 1, 2, 0))
        order = np.argsort(-tot); key = new_ctxp[order] * P29[4] + new_ctxk[order]; _, first = np.unique(key, return_index=True); keep = order[np.sort(first)][:beam]
        hist.append((parent[keep], psel[keep], br[keep], kused[keep], kskip[keep]))
        ctxp, ctxk, jk, score = new_ctxp[keep], new_ctxk[keep], new_jk[keep], tot[keep]
    b = int(score.argmax()); P = np.zeros(n, int); K = []
    for i in range(n - 1, -1, -1):
        parent, psel, br, kused, kskip = hist[i]; P[i] = psel[b]
        if br[b] == 2: K.append(-1)
        else:
            K.append(int(kused[b]))
            if br[b] == 1: K.append(int(kskip[b]))
        b = int(parent[b])
    return float(score.max()), P, np.array(K[::-1])


def ngram_z(P, rng, cache={}):
    n = len(P)
    if n not in cache: cache[n] = ngram.score_batch(rng.integers(0, N, size=(2000, n)), T)
    nul = cache[n]; return float((ngram.score_batch(np.asarray(P)[None, :], T)[0] - nul.mean()) / nul.std())


def encrypt(P, K, sign, rng, soft=0.81, f_rule=False, p_fill=0.0, wid=None):
    """C = P + K (sub), P - K (add), K - P (beaufort) with the soft skip; optional §59 fillers (one uniform rune in a share of words, key not consumed)"""
    comb = {"sub": lambda p, k: (p + k) % N, "add": lambda p, k: (p - k) % N, "beaufort": lambda p, k: (k - p) % N}[sign]
    C, j, prev, real = [], 0, None, []
    words = [np.flatnonzero(wid == w) for w in np.unique(wid)] if wid is not None else [np.arange(len(P))]
    for w in words:
        slot = int(rng.integers(0, len(w) + 1)) if (p_fill and len(w) >= 2 and rng.random() < p_fill) else -1
        for t, idx in enumerate(w):
            if t == slot: fch = int(rng.integers(0, N - 1)); fch = fch if (prev is None or fch < prev) else fch + 1; C.append(fch); real.append(False); prev = fch
            p = int(P[idx])
            if f_rule and p == 0: C.append(0); real.append(True); prev = 0; continue
            c = comb(p, int(K[j]))
            while prev is not None and c == prev and rng.random() < soft: j += 1; c = comb(p, int(K[j]))
            C.append(c); real.append(True); j += 1; prev = c
        if slot == len(w): fch = int(rng.integers(0, N - 1)); fch = fch if (prev is None or fch < prev) else fch + 1; C.append(fch); real.append(False); prev = fch
    return np.array(C), np.array(real)


pages = [(pid, np.asarray(C)) for pid, C in F.pages if len(C)]
rng = np.random.default_rng(68)
if STAGE == "plants":
    bun = np.array(json.loads((RAW.parent / "corpus" / "corpus_pilgrim.json").read_text())["bunyan_pilgrims_progress"]["runes"])
    text = re.findall(r"[A-Za-z]+", (RAW.parent / "corpus" / "raw" / "bunyan_pilgrims_progress_pg131.txt").read_text(errors="ignore"))
    words = [np.array(english_to_runes(w)) for w in text]; words = [w for w in words if len(w)]
    W = np.concatenate([np.full(len(w), i) for i, w in enumerate(words)]); PW = np.concatenate(words)
    out = []; NP = 3 if SMOKE else 30
    cells = [("sub", False, 0.0)] * NP + [("add", False, 0.0)] * (1 if SMOKE else 6) + [("beaufort", False, 0.0)] * (1 if SMOKE else 6) + [("sub", False, 0.4)] * (2 if SMOKE else 30)
    for ci, (sign, f_rule, pf) in enumerate(cells):
        a = int(rng.integers(0, len(PW) - 400)); b = (a + 20000 + int(rng.integers(0, len(bun) - 40000))) % (len(bun) - 400)
        P0 = PW[a:a + 262]; wid = W[a:a + 262]; K0 = bun[b:b + 400]
        C, real = encrypt(P0, K0, sign, rng, f_rule=f_rule, p_fill=pf, wid=wid if pf else None)
        s, P, K = decode_joint(C, sign, f_rule)
        acc = float((P[real] == P0).mean()) if pf == 0 else float((P[real] == P0).mean())
        out.append(dict(cell=ci, sign=sign, F=f_rule, p_fill=pf, n=len(C), score=s, acc=acc, zp=ngram_z(P, rng), zk=ngram_z(K[K >= 0], rng), tr=translit(P[:60]), key_tr=translit(K[K >= 0][:40])))
        print(f"plant {ci} {sign} fill {pf}: n {len(C)} acc {acc:.2f} joint {s:.0f} zp {out[-1]['zp']:+.1f} zk {out[-1]['zk']:+.1f} | {out[-1]['tr'][:40]} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / ("runkey_joint_plants_smoke.json" if SMOKE else "runkey_joint_plants.json"), "w"), indent=1)
elif STAGE == "null":                                            # SHARD=k (0-9) runs one (F, length) cell; the merge gathers runkey_joint_null_*.json
    lengths = (120, 180, 230, 260, 277); NN = 5 if SMOKE else 200; cells = [(f, n) for f in (False, True) for n in lengths]
    k = int(os.environ.get("SHARD", -1)); todo = cells if k < 0 else [cells[k]]; res = {}
    for f_rule, n in todo:
        rng = np.random.default_rng(100 + cells.index((f_rule, n)))
        sc = [decode_joint(rng.integers(0, N, size=n), "sub", f_rule)[0] for _ in range(NN)]
        res[f"{int(f_rule)}_{n}"] = dict(mean=float(np.mean(sc)), sd=float(np.std(sc)), max=float(np.max(sc)), scores=[float(x) for x in sc])
        print(f"null F={int(f_rule)} n={n}: mean {np.mean(sc):.1f} sd {np.std(sc):.1f} max {np.max(sc):.1f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(res, open(RESULTS / ("runkey_joint_null_smoke.json" if SMOKE else f"runkey_joint_null_{max(k,0)}.json"), "w"), indent=1)
elif STAGE == "pages":                                           # SHARD=k NSHARD=m over pages; the merge gathers runkey_joint_pages_*.json
    out = []; k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
    for pid, C in (pages[:2] if SMOKE else [p for j, p in enumerate(pages) if j % m == k]):
        for f_rule in (False, True):
            for sign in SIGNS:
                s, P, K = decode_joint(C, sign, f_rule)
                out.append(dict(page=pid, sign=sign, F=f_rule, n=len(C), score=s, zp=ngram_z(P, rng), zk=ngram_z(K[K >= 0], rng), tr=translit(P[:80]), key_tr=translit(K[K >= 0][:80])))
        print(f"{pid}: best joint {max(o['score'] for o in out if o['page'] == pid):.0f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / ("runkey_joint_pages_smoke.json" if SMOKE else f"runkey_joint_pages_{k}.json"), "w"), indent=1)
elif STAGE == "merge":
    pl = json.load(open(RESULTS / "runkey_joint_plants.json")); nul = {}; pg = []
    for f in sorted(RESULTS.glob("runkey_joint_null_*.json")): nul.update(json.load(open(f)))
    for f in sorted(RESULTS.glob("runkey_joint_pages_*.json")): pg += json.load(open(f))
    def null_at(n, f_rule):
        ls = sorted(int(k.split("_")[1]) for k in nul if k.startswith(f"{int(f_rule)}_")); ms = [nul[f"{int(f_rule)}_{l}"]["mean"] for l in ls]; ss = [nul[f"{int(f_rule)}_{l}"]["sd"] for l in ls]; mx = [nul[f"{int(f_rule)}_{l}"]["max"] for l in ls]
        return float(np.interp(n, ls, ms)), float(np.interp(n, ls, ss)), float(np.interp(n, ls, mx))
    for r in pl + pg:
        m, s, mx = null_at(r["n"], r["F"]); r["z"] = (r["score"] - m) / s; r["above_max"] = r["score"] > mx
    clean = [r for r in pl if r["p_fill"] == 0 and r["sign"] == "sub"]; fill = [r for r in pl if r["p_fill"] > 0]; other = [r for r in pl if r["p_fill"] == 0 and r["sign"] != "sub"]
    J1 = sum(r["acc"] >= 0.8 for r in clean) >= 15; zp_med = float(np.median([r["zp"] for r in clean if r["acc"] >= 0.8] or [r["zp"] for r in clean]))
    cands = [r for r in pg if r["z"] >= 6 and r["above_max"] and r["zp"] >= 0.5 * zp_med]; J2 = not cands
    out = ["# English running keys as a class: the library-free joint decoder", "", f"Registration: `results/runkey_joint_registration.md`. Beam {BEAM}; null from {len(nul['0_260']['scores'])} random pages at each of five lengths per F setting.", "",
           "## Power (Bunyan plaintext and key, 262 runes, soft rule 0.81)", "", "| cell | n | rune accuracy | joint z | plaintext 5-gram z | key 5-gram z | decode (first 40) |", "|---|---|---|---|---|---|---|"]
    for lab, S in (("sub, no fillers", clean), ("add / beaufort, no fillers", other), ("sub, §59 fillers p = 0.40", fill)):
        acc = np.array([r["acc"] for r in S]); out.append(f"| **{lab}** ({len(S)} plants) | | accuracy ≥ 0.8 on {int((acc >= 0.8).sum())}; median {np.median(acc):.2f} | median {np.median([r['z'] for r in S]):.1f} | median {np.median([r['zp'] for r in S]):+.1f} | median {np.median([r['zk'] for r in S]):+.1f} | |")
        for r in S[:4]: out.append(f"| {r['sign']} F={int(r['F'])} fill {r['p_fill']} | {r['n']} | {r['acc']:.2f} | {r['z']:.1f} | {r['zp']:+.1f} | {r['zk']:+.1f} | {r['tr'][:40]} |")
    out += ["", f"## Pages: {len(pg)} cells (55 pages × 3 signs × 2 F); candidate at joint z ≥ 6, above the null maximum, plaintext 5-gram z ≥ {0.5*zp_med:.1f} (half the plants' median {zp_med:.1f}), readable", "", "| page | sign | F | joint z | above null max | plaintext 5-gram z | key 5-gram z | plaintext (first 60) | key (first 40) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(pg, key=lambda r: -r["z"])[:20]: out.append(f"| {r['page']} | {r['sign']} | {int(r['F'])} | {r['z']:.2f} | {'yes' if r['above_max'] else 'no'} | {r['zp']:+.1f} | {r['zk']:+.1f} | {r['tr'][:60]} | {r['key_tr'][:40]} |")
    out += ["", f"Largest page joint z {max(r['z'] for r in pg):.2f}; largest plaintext 5-gram z {max(r['zp'] for r in pg):+.1f}; cells above the null maximum {sum(r['above_max'] for r in pg)}.", "", "## Claims", "", f"- J1 power ≥ 0.5 at page length without fillers (accuracy ≥ 0.8 on ≥ 15 of 30): **{'holds' if J1 else 'fails'}**.", f"- J2 no candidate on the pages: **{'holds' if J2 else 'fails'}**" + (f" ({len(cands)} candidate rows)" if cands else "") + ".", "", "Reading: written after the run. [stated — the tables]", ""]
    (RESULTS / "runkey_joint.md").write_text("\n".join(out)); json.dump(dict(plants=pl, pages=pg, J1=J1, J2=J2, zp_med=zp_med, candidates=cands), open(RESULTS / "runkey_joint.json", "w"), indent=1); print("\n".join(out))
