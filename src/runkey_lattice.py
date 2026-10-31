"""The word-lattice joint decoder for English running keys (2026-10-31; registration results/runkey_lattice_registration.md).
Plaintext: dictionary words of the slot's rune length (filler arm: or one shorter with one unkeyed filler); key: the rune 5-gram
with the exact skip branch taken greedily; beam over key contexts.  STAGE=plants | null | pages | merge; SHARD/NSHARD for null and pages.
Reproduce: STAGE=plants .venv/bin/python -I src/runkey_lattice.py, then null, pages, merge.
"""
import os, re, sys, json, time, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, N, IDX, english_to_runes
from score import translit
import ngram, families as F

t0 = time.time(); STAGE = os.environ.get("STAGE", "plants"); BEAM = int(os.environ.get("BEAM", 300)); SMOKE = os.environ.get("SMOKE") == "1"
LOGQ, PEN_FILL, LOGU = np.log(0.81), -2.2, np.log(1 / N)
T = ngram.load_dense(); TF = [t.reshape(-1, N) for t in T]; P29 = [N ** m for m in range(5)]
SIGNS = {"sub": (lambda c, p: (c - p) % N), "add": (lambda c, p: (p - c) % N), "beaufort": (lambda c, p: (c + p) % N)}

# ---------- dictionary
DICT = RESULTS / "rune_dictionary.json"
if not DICT.exists():
    from corpus import TEXTS
    cnt = collections.Counter()
    for name, (loader, *_) in TEXTS.items():
        for w in re.findall(r"[A-Za-z]+", loader()):
            r = tuple(english_to_runes(w.lower()))
            if r: cnt[r] += 1
    json.dump({" ".join(map(str, w)): c for w, c in cnt.items()}, open(DICT, "w"))
raw = json.load(open(DICT)); tot = sum(raw.values()); WORDS, LOGW = {}, {}
for k, c in raw.items():
    w = tuple(int(x) for x in k.split()); WORDS.setdefault(len(w), []).append(w); LOGW.setdefault(len(w), []).append(np.log(c / tot))
WORDS = {L: np.array(v) for L, v in WORDS.items()}; LOGW = {L: np.array(v) for L, v in LOGW.items()}
MAXL = max(WORDS)


_CAND = {}
def candidates(L, filler):
    """(cands (D, L) with -1 for a filler position, logw (D,)); cached per (L, filler)"""
    if (L, filler) in _CAND: return _CAND[(L, filler)]
    parts, lw = [], []
    if L in WORDS: parts.append(WORDS[L]); lw.append(LOGW[L])
    if filler and L - 1 in WORDS and L >= 2:
        base = WORDS[L - 1]
        for s in range(L):
            arr = np.full((len(base), L), -1); arr[:, :s] = base[:, :s]; arr[:, s + 1:] = base[:, s:]; parts.append(arr); lw.append(LOGW[L - 1] + PEN_FILL + LOGU)
    if not parts: parts, lw = [np.full((1, L), -1)], [np.array([PEN_FILL * L])]   # no word of this length: a slot of fillers
    _CAND[(L, filler)] = (np.vstack(parts), np.concatenate(lw)); return _CAND[(L, filler)]


def kgather(ctx, m, k):
    out = np.empty(len(ctx))
    for mm in np.unique(m):
        sel = m == mm; out[sel] = TF[mm][ctx[sel] % P29[mm], k[sel]]
    return out


PRUNE = int(os.environ.get("PRUNE", 1500))
def score_pairs(c, cand, logw, ctx, jk, prev_c, f, f_rule, score=None):
    """score every (state, candidate) pair over the slot's runes; returns (scores, key contexts, key counts) flattened state-major"""
    L = len(c); D = len(cand); B = len(ctx)
    cx = np.repeat(ctx, D); jj = np.repeat(jk, D); sc = (np.repeat(score, D) if score is not None else np.zeros(B * D)) + np.tile(logw, B); pw = np.tile(cand, (B, 1)); pc = prev_c
    for t in range(L):
        ct = int(c[t]); p = pw[:, t]; m = np.minimum(jj, 4)
        isfill = p < 0; litF = (f_rule & (ct == 0) & (p == 0)) if f_rule else np.zeros(len(p), bool)
        k = f(ct, np.where(p < 0, 0, p)); a = kgather(cx, m, k)
        if pc is not None:
            ks = f(int(pc), np.where(p < 0, 0, p)); cx2 = (cx * N + ks) % P29[4]; m2 = np.minimum(jj + 1, 4)
            b = kgather(cx, m, ks) + LOGQ + kgather(cx2, m2, k); skip = b > a
        else: skip = np.zeros(len(p), bool); b = a; cx2 = cx
        gain = np.where(skip, b, a); gain = np.where(isfill | litF, 0.0, gain); sc = sc + gain
        consumed = ~(isfill | litF)
        cx_new = np.where(skip, (cx2 * N + k) % P29[4], (cx * N + k) % P29[4]); cx = np.where(consumed, cx_new, cx)
        jj = jj + np.where(consumed, np.where(skip, 2, 1), 0); pc = ct
    return sc, cx, jj


def decode_lattice(words, sign, f_rule, filler, beam=BEAM):
    """words: list of cipher rune arrays (one per slot).  Returns joint score, plaintext (runes, -1 for fillers), key runes used."""
    f = SIGNS[sign]; ctx = np.zeros(1, np.int64); jk = np.zeros(1, np.int64); score = np.zeros(1); hist = []; prev_c = None
    for c in words:
        L = len(c); cand, logw = candidates(L, filler); B = len(score)
        if len(cand) > PRUNE:                                                   # candidate prescreen (amendment before the power stage): score every candidate against the ten best states, keep the best PRUNE
            sel = np.argsort(-score)[:10]; sc0 = score_pairs(c, cand, logw, ctx[sel], jk[sel], prev_c, f, f_rule)[0].reshape(len(sel), len(cand)).max(0)
            top = np.argpartition(-sc0, PRUNE)[:PRUNE]; cand, logw = cand[top], logw[top]
        D = len(cand)
        sc, cx, jj = score_pairs(c, cand, logw, ctx, jk, prev_c, f, f_rule, score)
        prev_c = int(c[-1])
        top = np.argpartition(-sc, min(20 * beam, len(sc) - 1))[:20 * beam] if len(sc) > 20 * beam else np.arange(len(sc))
        order = top[np.argsort(-sc[top])]; key = np.where(jj[order] >= 4, cx[order], cx[order] + P29[4] * (jj[order] + 1)); _, first = np.unique(key, return_index=True); keep = order[np.sort(first)][:beam]
        hist.append((keep // D, cand[keep % D])); ctx, jk, score = cx[keep], jj[keep], sc[keep]
    b = int(score.argmax()); P = []
    for parent, cw in reversed(hist): P.append(cw[b]); b = int(parent[b])
    P = np.concatenate(P[::-1]); C = np.concatenate(words)
    return float(score.max()), P, key_of(C, P, f, f_rule)


def key_of(C, P, f, f_rule):
    """the key stream the decoder's greedy rule implies for a plaintext: used runes with the skipped ones, fillers and literal F consume none"""
    K, ctx, j, pc = [], 0, 0, None
    for i in range(len(C)):
        c, p = int(C[i]), int(P[i])
        if p < 0 or (f_rule and c == 0 and p == 0): pc = c; continue
        k = int(f(c, p)); m = min(j, 4); a = TF[m][ctx % P29[m], k]
        if pc is not None:
            ks = int(f(pc, p)); ctx2 = (ctx * N + ks) % P29[4]; m2 = min(j + 1, 4); bsc = TF[m][ctx % P29[m], ks] + LOGQ + TF[m2][ctx2 % P29[m2], k]
            if bsc > a: K.append(ks); ctx = ctx2; j += 1
        K.append(k); ctx = (ctx * N + k) % P29[4]; j += 1; pc = c
    return np.array(K)


def ngram_z(P, rng, cache={}):
    P = np.asarray(P); P = P[P >= 0]; n = len(P)
    if n < 2: return float("nan")
    if n not in cache: cache[n] = ngram.score_batch(rng.integers(0, N, size=(2000, n)), T)
    nul = cache[n]; return float((ngram.score_batch(P[None, :], T)[0] - nul.mean()) / nul.std())


def encrypt_words(pwords, K, sign, rng, soft=0.81, p_fill=0.0):
    comb = {"sub": lambda p, k: (p + k) % N, "add": lambda p, k: (p - k) % N, "beaufort": lambda p, k: (k - p) % N}[sign]
    out, j, prev = [], 0, None
    for w in pwords:
        slot = int(rng.integers(0, len(w) + 1)) if (p_fill and len(w) >= 2 and rng.random() < p_fill) else -1; cw = []
        for t, p in enumerate(list(w) + [None]):
            if t == slot: fch = int(rng.integers(0, N - 1)); fch = fch if (prev is None or fch < prev) else fch + 1; cw.append(fch); prev = fch
            if p is None: break
            c = comb(int(p), int(K[j]))
            while prev is not None and c == prev and rng.random() < soft: j += 1; c = comb(int(p), int(K[j]))
            cw.append(c); j += 1; prev = c
        out.append(np.array(cw))
    return out


def page_words():
    txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§'); out = []
    for k in range(16, 72):
        words, cur = [], []
        for ch in chunks[k]:
            if ch in IDX: cur.append(IDX[ch])
            elif ch in SEP and cur: words.append(np.array(cur)); cur = []
        if cur: words.append(np.array(cur))
        if words: out.append((f"LP2-{k-16:02d}", words))
    return out


PAGES = page_words(); assert len(PAGES) == 55
for (pid, ws), (pid2, C) in zip(PAGES, [p for p in F.pages if len(p[1])]): assert pid == pid2 and np.array_equal(np.concatenate(ws), C), pid
rng = np.random.default_rng(69)
if STAGE == "plants":
    bun = np.array(json.loads((RAW.parent / "corpus" / "corpus_pilgrim.json").read_text())["bunyan_pilgrims_progress"]["runes"])
    bw = [np.array(english_to_runes(w.lower())) for w in re.findall(r"[A-Za-z]+", (RAW.parent / "corpus" / "raw" / "bunyan_pilgrims_progress_pg131.txt").read_text(errors="ignore"))]; bw = [w for w in bw if len(w)]
    cells = [("sub", 0.0)] * (3 if SMOKE else 30) + [("sub", 0.4)] * (2 if SMOKE else 30) + [("add", 0.0)] * (1 if SMOKE else 6) + [("beaufort", 0.0)] * (1 if SMOKE else 6); out = []
    k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
    for ci, (sign, pf) in enumerate(cells):
        rng = np.random.default_rng(700 + ci)
        if ci % m != k: continue
        a = int(rng.integers(0, len(bw) - 200)); pw = []; n = 0
        while n < 262: pw.append(bw[a + len(pw)]); n += len(pw[-1])
        b = (int(rng.integers(0, len(bun) - 600))); K0 = bun[b:b + 600]
        cw = encrypt_words(pw, K0, sign, rng, p_fill=pf); s, P, K = decode_lattice(cw, sign, False, filler=pf > 0)
        P0 = np.concatenate(pw); dec_words = []; i = 0
        for w in cw: dec_words.append(P[i:i + len(w)]); i += len(w)
        wacc = float(np.mean([np.array_equal(d[d >= 0], w) for d, w in zip(dec_words, pw)])); Pr = P[P >= 0]; racc = float((Pr == P0).mean()) if len(Pr) == len(P0) else float("nan")
        out.append(dict(cell=ci, sign=sign, p_fill=pf, n=int(sum(len(w) for w in cw)), score=s, wacc=wacc, racc=racc, zp=ngram_z(P, rng), zk=ngram_z(K, rng), tr=translit(Pr[:60])))
        print(f"plant {ci} {sign} fill {pf}: words {len(pw)} wacc {wacc:.2f} racc {racc:.2f} joint {s:.0f} zp {out[-1]['zp']:+.1f} zk {out[-1]['zk']:+.1f} | {out[-1]['tr'][:44]} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / ("runkey_lattice_plants_smoke.json" if SMOKE else f"runkey_lattice_plants_{k}.json"), "w"), indent=1)
elif STAGE == "null":                                                 # SHARD k of NSHARD over (F, arm, page) cells
    k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)); cells = [(f, arm, j) for f in (False, True) for arm in (False, True) for j in range(len(PAGES))]
    cells = [c for i, c in enumerate(cells) if i % m == k]; out = []
    for f_rule, arm, j in (cells[:2] if SMOKE else cells):
        pid, ws = PAGES[j]; rr = np.random.default_rng(1000 * j + 10 * arm + f_rule); reps = 1 if SMOKE else 2
        for r in range(reps):
            rw = [rr.integers(0, N, size=len(w)) for w in ws]; s, P, K = decode_lattice(rw, "sub", f_rule, arm)
            out.append(dict(page=pid, F=f_rule, arm=arm, n=int(sum(len(w) for w in ws)), score=s))
        print(f"null {pid} F={int(f_rule)} arm={int(arm)}: {out[-1]['score']:.0f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / ("runkey_lattice_null_smoke.json" if SMOKE else f"runkey_lattice_null_{k}.json"), "w"), indent=1)
elif STAGE == "pages":
    k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)); out = []
    for j, (pid, ws) in enumerate(PAGES):
        if j % m != k: continue
        for f_rule in (False, True):
            for arm in (False, True):
                for sign in SIGNS:
                    s, P, K = decode_lattice(ws, sign, f_rule, arm); Pr = P[P >= 0]
                    out.append(dict(page=pid, sign=sign, F=f_rule, arm=arm, n=int(sum(len(w) for w in ws)), score=s, zp=ngram_z(P, rng), zk=ngram_z(K, rng), tr=translit(Pr[:80]), key_tr=translit(K[:60]), fillers=int((P < 0).sum())))
        print(f"{pid}: best joint {max(o['score'] for o in out if o['page'] == pid):.0f} [{time.time()-t0:.0f}s]", flush=True)
        if SMOKE and j >= 1: break
    json.dump(out, open(RESULTS / ("runkey_lattice_pages_smoke.json" if SMOKE else f"runkey_lattice_pages_{k}.json"), "w"), indent=1)
elif STAGE == "merge":
    pl = []; nul = []; pg = []
    for f in sorted(RESULTS.glob("runkey_lattice_plants_[0-9]*.json")): pl += json.load(open(f))
    for f in sorted(RESULTS.glob("runkey_lattice_null_[0-9]*.json")): nul += json.load(open(f))
    for f in sorted(RESULTS.glob("runkey_lattice_pages_[0-9]*.json")): pg += json.load(open(f))
    def null_stats(F_, arm):
        S = [r for r in nul if r["F"] == F_ and r["arm"] == arm]; x = np.array([r["n"] for r in S]); y = np.array([r["score"] for r in S])
        a, b = np.polyfit(x, y, 1); res = y - (a * x + b); return a, b, float(res.std()), float(res.max())
    for r in pg:
        a, b, sd, mx = null_stats(r["F"], r["arm"]); r["z"] = (r["score"] - (a * r["n"] + b)) / sd; r["above_max"] = bool((r["score"] - (a * r["n"] + b)) > mx)
    for r in pl:
        a, b, sd, mx = null_stats(False, r["p_fill"] > 0); r["z"] = (r["score"] - (a * r["n"] + b)) / sd
    exact = [r for r in pl if r["p_fill"] == 0 and r["sign"] == "sub"]; fill = [r for r in pl if r["p_fill"] > 0]; other = [r for r in pl if r["p_fill"] == 0 and r["sign"] != "sub"]
    L1 = sum(r["wacc"] >= 0.8 for r in exact) >= 15; zp_med = float(np.median([r["zp"] for r in exact if r["wacc"] >= 0.8] or [r["zp"] for r in exact]))
    cands = [r for r in pg if r["z"] >= 6 and r["above_max"] and r["zp"] >= 0.5 * zp_med]; L3 = not cands
    out = ["# English running keys as a class: the word-lattice joint decoder", "", f"Registration: `results/runkey_lattice_registration.md`. Beam {BEAM}; dictionary {sum(len(v) for v in WORDS.values()):,} words; null {len(nul)} random pages with the real pages' word structures.", "",
           "## Power (Bunyan plaintext with its word boundaries, Bunyan key, 262 runes, soft rule 0.81)", "", "| cell | words | word accuracy | rune accuracy | joint z | plaintext 5-gram z | key 5-gram z | decode (first 44) |", "|---|---|---|---|---|---|---|---|"]
    for lab, S in (("sub, exact arm, no fillers", exact), ("add / beaufort, exact arm", other), ("sub, filler arm, §59 fillers p = 0.40", fill)):
        w = np.array([r["wacc"] for r in S]); out.append(f"| **{lab}** ({len(S)} plants) | | ≥ 0.8 on {int((w >= 0.8).sum())}; median {np.median(w):.2f} | median {np.median([r['racc'] for r in S]):.2f} | median {np.median([r['z'] for r in S]):.1f} | median {np.median([r['zp'] for r in S]):+.1f} | median {np.median([r['zk'] for r in S]):+.1f} | |")
        for r in S[:4]: out.append(f"| {r['sign']} fill {r['p_fill']} | | {r['wacc']:.2f} | {r['racc']:.2f} | {r['z']:.1f} | {r['zp']:+.1f} | {r['zk']:+.1f} | {r['tr'][:44]} |")
    out += ["", f"## Pages: {len(pg)} cells (55 pages × 3 signs × 2 F × 2 arms); candidate at joint z ≥ 6, above the null maximum, plaintext 5-gram z ≥ {0.5*zp_med:.1f}, readable", "", "| page | sign | F | arm | joint z | above max | plaintext 5-gram z | key 5-gram z | fillers | plaintext (first 60) | key (first 40) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(pg, key=lambda r: -r["z"])[:20]: out.append(f"| {r['page']} | {r['sign']} | {int(r['F'])} | {'filler' if r['arm'] else 'exact'} | {r['z']:.2f} | {'yes' if r['above_max'] else 'no'} | {r['zp']:+.1f} | {r['zk']:+.1f} | {r['fillers']} | {r['tr'][:60]} | {r['key_tr'][:40]} |")
    out += ["", f"Largest page joint z {max(r['z'] for r in pg):.2f}; largest plaintext 5-gram z {max(r['zp'] for r in pg):+.1f}; cells above the null maximum {sum(r['above_max'] for r in pg)}.", "", "## Claims", "", f"- L1 word accuracy ≥ 0.8 on ≥ 15 of 30 exact-arm plants: **{'holds' if L1 else 'fails'}**.", f"- L3 no candidate on the pages: **{'holds' if L3 else 'fails'}**" + (f" ({len(cands)} rows)" if cands else "") + ".", "", "Reading: written after the run. [stated — the tables]", ""]
    (RESULTS / "runkey_lattice.md").write_text("\n".join(out)); json.dump(dict(plants=pl, pages=pg, null=nul, L1=L1, L3=L3, zp_med=zp_med, candidates=cands), open(RESULTS / "runkey_lattice.json", "w"), indent=1); print("\n".join(out))
