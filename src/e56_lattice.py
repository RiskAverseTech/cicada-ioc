"""The E56w+n decoder on a word-lattice plaintext, for known keys (2026-10-31; registration results/e56_lattice_registration.md).

Per word slot the plaintext is a dictionary word of the slot's length, or one shorter with one unkeyed filler, or out of
dictionary; per rune the cipher is explained by the plain transition, the soft reject-on-repeat skip (q = 0.81, up to two),
the filler, the spent echo (lag 5 copy / lag 6 24 - 2c inside the word, gate r = 0.5 per word) or literal F.  Hypotheses are
enumerated by depth-first search over the slot with the known key and hashed into the dictionary; a Viterbi over the key
offset at word boundaries keeps the best BEAM states (amendment: beam of 8, recorded before the power stage).
STAGE=plants | controls | sweep | primes | merge; SHARD/NSHARD over plants or pages.
Reproduce: STAGE=plants .venv/bin/python -I src/e56_lattice.py, then controls, sweep, primes, merge.
"""
import os, re, sys, json, time
from math import log
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, N, english_to_runes
from score import decode as decode_plain, translit, S_MAX
import families as F

t0 = time.time(); STAGE = os.environ.get("STAGE", "plants"); SMOKE = os.environ.get("SMOKE") == "1"
BEAM = int(os.environ.get("BEAM", 8)); NNULL = 20 if SMOKE else int(os.environ.get("NNULL", 2000))
Q, R_GATE, P_FILL, P_OOD = 0.81, 0.5, 0.40, 0.04
LQ, L1Q, LR, L1R, LF, LNF, LOOD, LU, L28 = log(Q), log(1 - Q), log(R_GATE), log(1 - R_GATE), log(P_FILL), log(1 - P_FILL), log(P_OOD), log(1 / N), log(1 / 28)
def T6(c): return (24 - 2 * c) % N
JMAX = 10 ** 9                                                   # set per decode: runes + S_MAX, the furthest key offset a hypothesis may reach

raw = json.load(open(RESULTS / "rune_dictionary.json")); tot = sum(raw.values())
DICT = {tuple(int(x) for x in k.split()): log(c / tot) for k, c in raw.items()}
MODES = {"sub": (lambda c, k: (c - k) % N, lambda p, k: (p + k) % N), "beaufort": (lambda c, k: (k - c) % N, lambda p, k: (k - p) % N)}


def slot_hyps(c, K, j0, prev, mode, f_rule):
    """every way the slot's runes c (list of ints) can be explained from key offset j0 after cipher rune prev;
    yields (gain, j_end, plaintext tuple with -1 at the filler, nfill, necho)"""
    dec, comb = MODES[mode]; L = len(c); out = []
    stack = [(0, j0, prev, 0.0, (), False, 0)]                       # t, j, prev, gain, path, filler used, echoes
    while stack:
        t, j, pv, g, path, used, ne = stack.pop()
        if t == L:
            if ne:                                                   # an active word must echo wherever the plaintext repeats and the cipher allows it
                ok = True
                for u in range(5, L):
                    if path[u] < 0: continue
                    if path[u - 5] == path[u] and c[u - 5] != c[u] and c[u - 5] != c[u - 1]: ok = False; break
                    if u >= 6 and path[u - 5] != path[u] and path[u - 6] == path[u] and T6(c[u - 6]) != c[u] and T6(c[u - 6]) != c[u - 1]: ok = False; break
                if not ok: continue
            out.append((g + (LR if ne else L1R), j, path, used, ne)); continue
        ct = c[t]
        if f_rule and ct == 0: stack.append((t + 1, j, 0, g, path + (0,), used, ne))            # literal F: plaintext F unkeyed
        p = dec(ct, K[j]); stack.append((t + 1, j + 1, ct, g + (L1Q if ct == pv else 0.0), path + (p,), used, ne))   # plain
        if ct != pv:
            p1 = dec(ct, K[j + 1])
            if comb(p1, K[j]) == pv:                                                                         # one skip
                stack.append((t + 1, j + 2, ct, g + LQ, path + (p1,), used, ne))
                p2 = dec(ct, K[j + 2])
                if comb(p2, K[j]) == pv and comb(p2, K[j + 1]) == pv: stack.append((t + 1, j + 3, ct, g + 2 * LQ, path + (p2,), used, ne))
            if not used and L >= 2: stack.append((t + 1, j, ct, g + LF - log(L) + L28, path + (-1,), True, ne))   # the filler, written to differ from its left neighbour
            if t >= 5 and ct == c[t - 5] and path[t - 5] >= 0: stack.append((t + 1, j + 1, ct, g, path + (path[t - 5],), used, ne + 1))   # lag-5 echo, key spent
            elif t >= 6 and ct == T6(c[t - 6]) and path[t - 6] >= 0: stack.append((t + 1, j + 1, ct, g, path + (path[t - 6],), used, ne + 1))   # lag-6 echo
    res = []
    for g, j, path, used, ne in out:
        w = tuple(p for p in path if p >= 0); lw = DICT.get(w)
        if lw is None: continue
        res.append((g + lw + (0.0 if used else LNF), j, path, int(used), ne))
    # out of dictionary: L runes at the uniform rate, with the three offsets a filler or a skip would leave
    base = LOOD + L * LU
    res += [(base + LNF, j0 + L, (-2,) * L, 0, 0), (base + LF - log(L) + L28, j0 + L - 1, (-2,) * L, 1, 0), (base + LNF + log(L * Q / N), j0 + L + 1, (-2,) * L, 0, 0)]   # the extra key needs a skip somewhere in the word
    return [r for r in res if r[1] <= JMAX]


def decode_e56(words, K, mode, f_rule, beam=BEAM):
    """words: list of cipher rune arrays (slots); K: key array (ints, length >= runes + S_MAX).  Returns score, plaintext (-1 filler,
    -2 out-of-dictionary), fillers placed, echoes placed."""
    global JMAX
    nr = sum(len(w) for w in words); JMAX = nr + S_MAX; K = [int(k) for k in K]; K = K + [0] * max(0, JMAX + 4 - len(K)); states = {0: (0.0, None)}; hist = []; prev = -1
    for c in words:
        c = [int(x) for x in c]; nxt = {}
        for j0, (s0, _) in states.items():
            for g, j, path, nf, ne in slot_hyps(c, K, j0, prev, mode, f_rule):
                s = s0 + g
                if j not in nxt or s > nxt[j][0]: nxt[j] = (s, (j0, path, nf, ne))
        if len(nxt) > beam: nxt = dict(sorted(nxt.items(), key=lambda kv: -kv[1][0])[:beam])
        hist.append(nxt); states = {j: (s, None) for j, (s, _) in nxt.items()}; prev = c[-1]
    j = max(states, key=lambda k: states[k][0]); best = states[j][0]; P = []; nf = ne = 0
    for h in reversed(hist):
        s, (j0, path, f_, e_) = h[j]; P.append(path); nf += f_; ne += e_; j = j0
    return best, np.concatenate([np.array(p) for p in P[::-1]]), nf, ne


# ---------- pages, libraries, plants
def page_words():
    txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§'); out = []
    from lp import IDX
    for k in range(16, 72):
        words, cur = [], []
        for ch in chunks[k]:
            if ch in IDX: cur.append(IDX[ch])
            elif ch in SEP and cur: words.append(np.array(cur)); cur = []
        if cur: words.append(np.array(cur))
        if words: out.append((f"LP2-{k-16:02d}", words))
    return out
PAGES = page_words(); assert len(PAGES) == 55
LKEY = max(sum(len(w) for w in ws) for _, ws in PAGES) + S_MAX + 2
SIGNSETS = {"sub": (0, 3, "sub"), "add": (1, 4, "sub"), "beaufort": (2, 5, "beaufort")}
def library(sign):
    a, b, mode = SIGNSETS[sign]; Ka, La = F.ALLSETS[a][2], F.ALLSETS[a][3]; Kb, Lb = F.ALLSETS[b][2], F.ALLSETS[b][3]
    return np.vstack([Ka, Kb])[:, :LKEY], [f"{x} {y}" for x, y in list(La) + list(Lb)], mode
def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)
def prime_library(sign):
    P = sieve(20000); ks, ls = [], []
    for s in range(1000):
        seg = P[s:s + LKEY]
        for name, arr in (("p", seg), ("p-1", seg - 1), ("p+1", seg + 1)): ks.append(arr % N); ls.append(f"prime {name} s={s}")
    Kp = np.array(ks); mode = "beaufort" if sign == "beaufort" else "sub"
    return ((-Kp) % N if sign == "add" else Kp), ls, mode


def encrypt_e56(pwords, K, mode, f_rule, rng, p_fill=P_FILL, r=R_GATE, q=Q):
    """§58's E56w+n with a given key: fillers at p_fill per word of >= 2 runes (uniform slot), per-word gate r, lag-5 copy and
    lag-6 affine echoes with the key spent, the soft skip q up to four, filler and echo runes written to differ from the previous
    cipher rune; literal F unkeyed when f_rule.  Returns cipher slots, plaintext with -1 at fillers, filler mask, echo mask."""
    comb = MODES[mode][1]; out, P, FM, EM = [], [], [], []; j = 0; prev = -1
    for w in pwords:
        word = list(int(x) for x in w)
        if len(word) >= 2 and rng.random() < p_fill: word.insert(int(rng.integers(0, len(word) + 1)), -1)
        active = rng.random() < r; cw = []
        for t, p in enumerate(word):
            if active and p >= 0:
                x = -1
                if t >= 5 and word[t - 5] == p: x = cw[t - 5]
                elif t >= 6 and word[t - 6] == p: x = T6(cw[t - 6])
                if x != -1 and x != prev: cw.append(x); prev = x; j += 1; P.append(p); FM.append(False); EM.append(True); continue
            if p == -1:
                x = int(rng.integers(0, N))
                while x == prev: x = int(rng.integers(0, N))
                cw.append(x); prev = x; P.append(-1); FM.append(True); EM.append(False); continue
            if f_rule and p == 0: cw.append(0); prev = 0; P.append(0); FM.append(False); EM.append(False); continue
            x = comb(p, int(K[j]))
            if x == prev and rng.random() < q:
                for _ in range(4):
                    j += 1; x = comb(p, int(K[j]))
                    if x != prev: break
            cw.append(x); prev = x; j += 1; P.append(p); FM.append(False); EM.append(False)
        out.append(np.array(cw))
    return out, np.array(P), np.array(FM), np.array(EM)


def ztest(words, Ktrue, Klib, mode, f_rule, rng):
    """this decoder on the true key, the library and NNULL random keystreams: (score, rank in library, z, plaintext, nfill, necho)"""
    s, P, nf, ne = decode_e56(words, Ktrue, mode, f_rule)
    lib = np.array([decode_e56(words, k, mode, f_rule)[0] for k in Klib])
    nul = np.array([decode_e56(words, k, mode, f_rule)[0] for k in rng.integers(0, N, size=(NNULL, LKEY))])
    return s, int((lib > s).sum()) + 1, float((s - nul.mean()) / nul.std()), P, nf, ne, lib, nul


def bunyan_words():
    bw = [np.array(english_to_runes(w.lower())) for w in re.findall(r"[A-Za-z]+", (RAW.parent / "corpus" / "raw" / "bunyan_pilgrims_progress_pg131.txt").read_text(errors="ignore"))]
    return [w for w in bw if len(w)]


if STAGE == "plants":                                               # 30 plants x 3 decoders; SHARD/NSHARD
    bw = bunyan_words(); k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)); out = []
    cells = [(("sub", "add", "beaufort")[i % 3], bool((i // 3) % 2)) for i in range(3 if SMOKE else 30)]
    for ci, (sign, f_rule) in enumerate(cells):
        if ci % m != k: continue
        rng = np.random.default_rng(800 + ci); Klib, Llib, mode = library(sign)
        a = int(rng.integers(0, len(bw) - 200)); pw = []; n = 0
        while n < 262: pw.append(bw[a + len(pw)]); n += len(pw[-1])
        ki = int(rng.integers(0, len(Klib))); K = Klib[ki]
        cw, P0, FM, EM = encrypt_e56(pw, K, mode, f_rule, rng); C = np.concatenate(cw); real = ~FM
        Ks = np.vstack([Klib, rng.integers(0, N, size=(NNULL, LKEY))]); nm = np.ones(len(C), bool); nm[0] = False
        row = dict(cell=ci, sign=sign, F=f_rule, key=Llib[ki], n=int(len(C)), words=len(pw), fillers=int(FM.sum()), echoes=int(EM.sum()))
        for dec in ("plain", "free-null"):
            sc, _, d = (decode_plain(C, Ks, F.lu, f_rule, mode) if dec == "plain" else decode_plain(C, Ks, F.lu, f_rule, mode, None, nm, -2.2))[:3]
            lib, nul = sc[:len(Klib)], sc[len(Klib):]; z = (sc[ki] - nul.mean()) / nul.std()
            row[dec] = dict(rank=int((lib > sc[ki]).sum()) + 1, z=float(z), acc=float((d[ki][real] == P0[real]).mean()))
        s, rank, z, P, nf, ne, lib, nul = ztest(cw, K, Klib, mode, f_rule, rng)
        acc = float((P[real] == P0[real]).mean()); ffound = float(((P == -1) & FM).sum() / max(FM.sum(), 1))
        row["e56"] = dict(rank=rank, z=z, acc=acc, fillers_placed=nf, fillers_found=ffound, echoes_placed=ne, tr=translit(P[P >= 0][:60]))
        out.append(row); print(f"plant {ci} {sign} F={int(f_rule)} {Llib[ki]}: fillers {int(FM.sum())} echoes {int(EM.sum())} | plain rank {row['plain']['rank']} z {row['plain']['z']:.1f} acc {row['plain']['acc']:.2f} | free-null rank {row['free-null']['rank']} z {row['free-null']['z']:.1f} acc {row['free-null']['acc']:.2f} | e56 rank {rank} z {z:.1f} acc {acc:.2f} fill {nf}/{int(FM.sum())} found {ffound:.2f} echo {ne}/{int(EM.sum())} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / ("e56_lattice_plants_smoke.json" if SMOKE else f"e56_lattice_plants_{k}.json"), "w"), indent=1)

elif STAGE == "controls":                                           # six plants, one per (sign, F), through the full library of their sign
    bw = bunyan_words(); out = []
    for ci, (sign, f_rule) in enumerate([(s, f) for f in (False, True) for s in ("sub", "add", "beaufort")]):
        rng = np.random.default_rng(900 + ci); Klib, Llib, mode = library(sign)
        a = int(rng.integers(0, len(bw) - 200)); pw = []; n = 0
        while n < 262: pw.append(bw[a + len(pw)]); n += len(pw[-1])
        ki = int(rng.integers(0, len(Klib))); K = Klib[ki]; cw, P0, FM, EM = encrypt_e56(pw, K, mode, f_rule, rng)
        s, rank, z, P, nf, ne, lib, nul = ztest(cw, K, Klib, mode, f_rule, rng)
        out.append(dict(cell=ci, sign=sign, F=f_rule, key=Llib[ki], fillers=int(FM.sum()), echoes=int(EM.sum()), rank=rank, z=z, above_max=bool(s > nul.max()), acc=float((P[~FM] == P0[~FM]).mean()), fillers_placed=nf, echoes_placed=ne, tr=translit(P[P >= 0][:60])))
        print(f"control {ci} {sign} F={int(f_rule)} {Llib[ki]}: rank {rank} z {z:.1f} acc {out[-1]['acc']:.2f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / "e56_lattice_controls.json", "w"), indent=1)

elif STAGE in ("sweep", "primes"):                                  # per page: 3 signs x 2 F over the library, and the null per F; SHARD/NSHARD over pages
    k, m = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1)); out = []
    for pi, (pid, ws) in enumerate(PAGES):
        if pi % m != k: continue
        if SMOKE and pi >= 1: break
        rng = np.random.default_rng(5000 + pi); rec = dict(page=pid, n=int(sum(len(w) for w in ws)), null={}, cells=[])
        for f_rule in (False, True):
            nul = np.array([decode_e56(ws, kk, "sub", f_rule)[0] for kk in rng.integers(0, N, size=(NNULL, LKEY))])
            rec["null"][str(int(f_rule))] = dict(mean=float(nul.mean()), sd=float(nul.std()), max=float(nul.max()))
        for sign in ("sub", "add", "beaufort"):
            Klib, Llib, mode = (library if STAGE == "sweep" else prime_library)(sign)
            if SMOKE: Klib, Llib = Klib[:200], Llib[:200]
            for f_rule in (False, True):
                sc = np.array([decode_e56(ws, kk, mode, f_rule)[0] for kk in Klib]); nz = rec["null"][str(int(f_rule))]; z = (sc - nz["mean"]) / nz["sd"]
                top = np.argsort(-sc)[:5]; rows = []
                for i in top:
                    s, P, nf, ne = decode_e56(ws, Klib[i], mode, f_rule); rows.append(dict(key=Llib[i], score=float(s), z=float(z[i]), above_max=bool(s > nz["max"]), fillers=nf, echoes=ne, tr=translit(P[P >= 0][:80])))
                rec["cells"].append(dict(sign=sign, F=f_rule, nkeys=len(Klib), n_z45=int((z >= 4.5).sum()), top=rows))
        out.append(rec); print(f"{pid}: largest z {max(r['top'][0]['z'] for r in rec['cells']):.2f} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(RESULTS / (f"e56_lattice_{STAGE}_smoke.json" if SMOKE else f"e56_lattice_{STAGE}_{k}.json"), "w"), indent=1)

elif STAGE == "merge":
    pl, sw, pr = [], [], []
    for f in sorted(RESULTS.glob("e56_lattice_plants_[0-9]*.json")): pl += json.load(open(f))
    for f in sorted(RESULTS.glob("e56_lattice_sweep_[0-9]*.json")): sw += json.load(open(f))
    for f in sorted(RESULTS.glob("e56_lattice_primes_[0-9]*.json")): pr += json.load(open(f))
    ctl = json.load(open(RESULTS / "e56_lattice_controls.json")) if (RESULTS / "e56_lattice_controls.json").exists() else []
    rec = lambda d: d["rank"] == 1 and d["z"] >= 6
    E1 = sum(rec(r["e56"]) for r in pl) >= 27; E2 = sum(rec(r["e56"]) for r in pl) >= sum(rec(r["free-null"]) for r in pl)
    def cands(S):
        return [(p["page"], c["sign"], c["F"], r) for p in S for c in p["cells"] for r in c["top"][:1] if r["z"] >= 6 and r["above_max"]]
    c3, c4 = cands(sw), cands(pr); E3, E4 = not c3, not c4
    out = ["# The E56w+n decoder on a word-lattice plaintext (known keys)", "", f"Registration: `results/e56_lattice_registration.md`. Beam {BEAM} key-offset states; null {NNULL} random keystreams per (page, F).", "",
           "## Power: 30 E56w+n plants (Bunyan words, 262 runes, library keys, signs and F cycled)", "", "| decoder | recovered (rank 1, z ≥ 6) | median z | median rune accuracy |", "|---|---|---|---|"]
    for dec in ("plain", "free-null", "e56"):
        out.append(f"| {dec} | {sum(rec(r[dec]) for r in pl)} / {len(pl)} | {np.median([r[dec]['z'] for r in pl]):.1f} | {np.median([r[dec]['acc'] for r in pl]):.2f} |")
    out += ["", f"Fillers planted (median) {np.median([r['fillers'] for r in pl]):.0f}, placed by the decoder {np.median([r['e56']['fillers_placed'] for r in pl]):.0f}, share found {np.median([r['e56']['fillers_found'] for r in pl]):.2f}; echoes planted {np.median([r['echoes'] for r in pl]):.0f}, placed {np.median([r['e56']['echoes_placed'] for r in pl]):.0f}.", "",
            "| plant | sign | F | key | fillers | echoes | plain rank / z | free-null rank / z | e56 rank / z / acc | decode (first 44) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in pl: out.append(f"| {r['cell']} | {r['sign']} | {int(r['F'])} | {r['key']} | {r['fillers']} | {r['echoes']} | {r['plain']['rank']} / {r['plain']['z']:.1f} | {r['free-null']['rank']} / {r['free-null']['z']:.1f} | {r['e56']['rank']} / {r['e56']['z']:.1f} / {r['e56']['acc']:.2f} | {r['e56']['tr'][:44]} |")
    if ctl:
        out += ["", "## Controls (six plants through the full library of their sign)", "", "| cell | sign | F | key | rank | z | above null max | accuracy |", "|---|---|---|---|---|---|---|---|"]
        for r in ctl: out.append(f"| {r['cell']} | {r['sign']} | {int(r['F'])} | {r['key']} | {r['rank']} | {r['z']:.1f} | {'yes' if r['above_max'] else 'no'} | {r['acc']:.2f} |")
    for lab, S in (("The book's keys: 7,621 x 3 signs x 2 F x 55 pages", sw), ("Prime streams: 3,000 x 3 signs x 2 F x 55 pages", pr)):
        if not S: continue
        rows = sorted([(p["page"], c["sign"], c["F"], r) for p in S for c in p["cells"] for r in c["top"][:1]], key=lambda x: -x[3]["z"])
        out += ["", f"## {lab}", "", f"Pages {len(S)}; cells {sum(len(p['cells']) for p in S)}; keys at z ≥ 4.5: {sum(c['n_z45'] for p in S for c in p['cells'])}; largest z {rows[0][3]['z']:.2f}.", "",
                "| page | sign | F | key | z | above null max | fillers | echoes | decode (first 60) |", "|---|---|---|---|---|---|---|---|---|"]
        for pid, sign, f_rule, r in rows[:15]: out.append(f"| {pid} | {sign} | {int(f_rule)} | {r['key']} | {r['z']:.2f} | {'yes' if r['above_max'] else 'no'} | {r['fillers']} | {r['echoes']} | {r['tr'][:60]} |")
    out += ["", "## Claims", "", f"- E1 this decoder recovers ≥ 27 of 30 plants: **{'holds' if E1 else 'fails'}**.", f"- E2 its recoveries ≥ the free-null decoder's: **{'holds' if E2 else 'fails'}**.",
            f"- E3 no candidate over the book's keys: **{'holds' if E3 else 'fails'}**" + (f" ({len(c3)} rows)" if c3 else "") + ".", f"- E4 no candidate over the prime streams: **{'holds' if E4 else 'fails'}**" + (f" ({len(c4)} rows)" if c4 else "") + ".", "", "Reading: written after the run. [stated — the tables]", ""]
    (RESULTS / "e56_lattice.md").write_text("\n".join(out)); json.dump(dict(plants=pl, controls=ctl, sweep=sw, primes=pr, E1=E1, E2=E2, E3=E3, E4=E4, candidates=dict(book=c3, primes=c4)), open(RESULTS / "e56_lattice.json", "w"), indent=1, default=float); print("\n".join(out))
