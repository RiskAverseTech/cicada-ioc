"""Echo-aware decoding of the phase 3-4 key library (2026-10-28, §48).  Pre-registered.

MECHANISM UNDER TEST (E56w of §47): an additive cipher with the soft skip rule (q 0.81) in which, inside a word
selected with probability r = 0.5, a plaintext rune equal to the plaintext rune five back is written as the
CIPHER rune five back, and one equal to the rune six back is written as 24 - 2 c_(i-6); the key symbol at an echo
is consumed unused ("spent") or kept ("held").  Ciphertext positions where an echo can have happened are
observable: c_i == c_(i-5) or c_i == 24 - 2 c_(i-6) inside a word, at word position >= 5 / 6.

DECODER.  score.decode with echo_mask at those positions (spent: t unchanged, gain ln(r * P_English(repeat at
lag d)) - ln(1/29) = -0.09; held: null_mask at the same positions with the same penalty).  Everything else as in
phases 3-4: Viterbi over key offset with the skip transitions, unigram English LLR, 5-gram rescoring of candidates.

RULE (fixed before the run).  A page is a hit if its best configuration scores z_uni >= 6 over that page's own null
of 2,000 random keystreams decoded with the same masks AND the rune 5-gram z_5 >= 6 AND the transliteration reads
as English.  Library: families.ALLSETS (phase 3 streams and phase 4 phrase keys, 3 signs, 2 F variants).
Controls: 12 plants (6 spent, 6 held; signs and F cycled; 262 runes of English in its own words with a key drawn
from the library) must be recovered at rank 1 with z_uni >= 6 by the matching echo decoder; the base decoder's z
on the same plants is reported, which measures how much an unaware decoder loses to each variant.
Usage: SMOKE=1 for a quick check; VARIANT=spent|held|both (default both); writes results/echo_lane[_variant].md/.json
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, LOGU
from skip_decrypt import combine
import families as F, ngram, corpus

SMOKE = os.environ.get("SMOKE") == "1"; VARIANT = os.environ.get("VARIANT", "both")
rng = np.random.default_rng(56)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
EDGES = json.load(open(PROCESSED / "edges.json"))
SETS = F.ALLSETS
R_GATE, Q, P_REP = 0.5, 0.81, {5: 0.063, 6: 0.060}
GAIN = float(np.log(R_GATE * 0.062) - LOGU)              # -0.09: the echo's log-probability relative to uniform
Z_UNI, Z_5, NREPS = 6.0, 6.0, (200 if SMOKE else 2000)
T = lambda x: (24 - 2 * x) % N
T5 = ngram.load_dense()
if SMOKE: pages = pages[:2]

def word_ids(pid, n):
    w = np.zeros(n, int)
    for i in EDGES[pid]["word_initial"]: w[i:] += 1
    return w

def echo_mask_of(C, w):
    """0, 5 or 6 per position: where an echo could have produced c_i."""
    m = np.zeros(len(C), int); pos = np.zeros(len(C), int)
    for i in range(1, len(C)): pos[i] = pos[i - 1] + 1 if w[i] == w[i - 1] else 0
    for i in range(len(C)):
        if pos[i] >= 5 and C[i] == C[i - 5]: m[i] = 5
        elif pos[i] >= 6 and C[i] == T(C[i - 6]): m[i] = 6
    return m

def dec(C, Ks, f_rule, mode, mask, variant):
    if variant == "base": return decode(C, Ks, lu, f_rule, mode)
    if variant == "spent": return decode(C, Ks, lu, f_rule, mode, echo_mask=mask, echo_gain=GAIN)
    return decode(C, Ks, lu, f_rule, mode, null_mask=mask > 0, penalty=GAIN)

# ---------- English words for plants
text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(wd) for wd in text.split()]; EW = [wd for wd in EW if wd]

def encrypt_echo(n, K, sign, f_rule, held, r=R_GATE, q=Q):
    """A plant of n runes: English in its own words under the echo mechanism with key K."""
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
            if x != -1 and x != prev:
                C[i] = x; prev = x; n_echo += 1
                if not held: j += 1
                continue
        if f_rule and p == 0: C[i] = 0; prev = 0; continue
        c = combine(p, K[j], sign)
        while prev != -1 and c == prev and rng.random() < q: j += 1; c = combine(p, K[j], sign)
        C[i] = c; prev = c; j += 1
    return C, P, W, n_echo

def null_z(C, f_rule, mode, mask, variant, reps):
    Kr = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2)); s = dec(C, Kr, f_rule, mode, mask, variant)[0]; return s.mean(), s.std()

def scores_all(C, Ks, f_rule, mode, mask, variant, batch=1500):
    sc = np.empty(len(Ks)); tops = {}
    for b in range(0, len(Ks), batch):
        s, _, out = dec(C, Ks[b:b + batch], f_rule, mode, mask, variant); sc[b:b + batch] = s
        for k in np.argsort(-s)[:2]: tops[b + k] = out[k]
    return sc, tops

def z5_of(C, f_rule, mode, mask, variant, decs):
    Kr = rng.integers(0, N, size=(300 if SMOKE else 1000, len(C) + S_MAX + 2)); _, _, outn = dec(C, Kr, f_rule, mode, mask, variant)
    s5n = ngram.score_batch(outn, T5); s5 = ngram.score_batch(np.stack(decs), T5); return (s5 - s5n.mean()) / s5n.std()

variants = ["spent", "held"] if VARIANT == "both" else [VARIANT]
t0 = time.time(); nconf = sum(len(L) for *_, L in SETS)
print(f"{nconf} configurations x {len(pages)} pages x 2 F x {len(variants)} decoders; echo gain {GAIN:+.3f}", flush=True)

# ---------- controls
controls = []
for ci in range(4 if SMOKE else 12):
    held = bool(ci % 2); variant = "held" if held else "spent"
    sign, mode, Ks, labs = SETS[ci % len(SETS)]; f_rule = bool((ci // 6) % 2)
    ki = int(rng.integers(0, len(Ks))); Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
    C, P, W, n_echo = encrypt_echo(262, Ktrue, sign, f_rule, held)
    mask = echo_mask_of(C, W)
    m0, s0 = null_z(C, f_rule, mode, mask, variant, 400); sc, tops = scores_all(C, Ks, f_rule, mode, mask, variant)
    z = (sc - m0) / s0; rank = int((z > z[ki]).sum()) + 1
    mb, sb = null_z(C, f_rule, mode, mask, "base", 400); zb = (dec(C, Ks[ki:ki + 1], f_rule, mode, mask, "base")[0][0] - mb) / sb
    rec = dec(C, Ks[ki:ki + 1], f_rule, mode, mask, variant)[2][0]; acc = float((rec == P).mean())
    passed = z[ki] >= Z_UNI and rank == 1
    controls.append(dict(variant=variant, sign=sign, F=f_rule, family=labs[ki][0], key=labs[ki][1][:30], echoes=n_echo, mask=int((mask > 0).sum()), z=float(z[ki]), rank=rank, z_base=float(zb), acc=acc, passed=bool(passed)))
    print(f"  control {ci}: {variant} {sign} F={f_rule} {labs[ki][0]} echoes {n_echo} (mask {int((mask>0).sum())}): z {z[ki]:.1f} rank {rank}, base z {zb:.1f}, acc {acc:.3f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

# ---------- the sweep
cells, cands = [], []
for pid, C in pages:
    w = word_ids(pid, len(C)); mask = echo_mask_of(C, w)
    for variant in variants:
        for f_rule in (False, True):
            for sign, mode, Ks, labs in SETS:
                m0, s0 = null_z(C, f_rule, mode, mask, variant, NREPS); sc, tops = scores_all(C, Ks, f_rule, mode, mask, variant)
                z = (sc - m0) / s0; k = int(z.argmax())
                row = dict(page=pid, variant=variant, F=f_rule, sign=sign, family=labs[k][0], key=labs[k][1][:40], z=float(z[k]), mask=int((mask > 0).sum()))
                if z[k] >= Z_UNI:
                    ks = [int(x) for x in np.where(z >= Z_UNI)[0]]
                    decs = [dec(C, Ks[x:x + 1], f_rule, mode, mask, variant)[2][0] for x in ks]; z5 = z5_of(C, f_rule, mode, mask, variant, decs)
                    for x, zz5, d in zip(ks, z5, decs):
                        c = dict(page=pid, variant=variant, F=f_rule, sign=sign, family=labs[x][0], key=labs[x][1][:40], z=float(z[x]), z5=float(zz5), translit=translit(d[:80]))
                        cands.append(c); print(f"  z>=6: {c}", flush=True)
                cells.append(row)
    print(f"  {pid} done: best z " + ", ".join(f"{v} {max(r['z'] for r in cells if r['page']==pid and r['variant']==v):.2f}" for v in variants) + f"  [{time.time()-t0:.0f}s]", flush=True)

tag = "" if VARIANT == "both" else f"_{VARIANT}"
hits = [c for c in cands if c["z5"] >= Z_5]
out = [f"# Echo-aware decoding of the phase 3-4 library ({', '.join(variants)} echoes)", "",
       f"{nconf} configurations x {len(pages)} pages x 2 F variants x {len(variants)} decoders = {nconf*len(pages)*2*len(variants):,} tests; null per cell {NREPS} random keystreams through the same decoder; rule z_uni >= {Z_UNI} and z_5 >= {Z_5} and readable. Echo gain {GAIN:+.3f} (r = {R_GATE}).", "",
       "## Controls", "", "| variant | sign | F | family | key | echoes in plant | eligible positions | echo-decoder z (rank) | base-decoder z | plaintext recovered | pass |", "|---|---|---|---|---|---|---|---|---|---|---|"]
for c in controls: out.append(f"| {c['variant']} | {c['sign']} | {c['F']} | {c['family']} | {c['key']} | {c['echoes']} | {c['mask']} | {c['z']:.1f} ({c['rank']}) | {c['z_base']:.1f} | {c['acc']:.3f} | {'yes' if c['passed'] else 'no'} |")
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Best cell per page and decoder", "", "| page | decoder | eligible positions | best z | sign | F | family | key |", "|---|---|---|---|---|---|---|---|"]
for pid, _ in pages:
    for v in variants:
        r = max((r for r in cells if r["page"] == pid and r["variant"] == v), key=lambda r: r["z"]); out.append(f"| {pid} | {v} | {r['mask']} | {r['z']:.2f} | {r['sign']} | {r['F']} | {r['family']} | {r['key']} |")
out += ["", f"## Cells at z_uni >= {Z_UNI} ({len(cands)})", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"## Hits (also z_5 >= {Z_5}): {len(hits)}", ""] + ([f"- {c}" for c in hits] or ["None."]) + ["", f"Largest z_uni over all cells: {max(r['z'] for r in cells):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / f"echo_lane{tag}{'_smoke' if SMOKE else ''}.md").write_text("\n".join(out) + "\n")
json.dump(dict(controls=controls, cells=cells, candidates=cands, hits=hits, ntests=nconf * len(pages) * 2 * len(variants), gain=GAIN, r=R_GATE), open(RESULTS / f"echo_lane{tag}{'_smoke' if SMOKE else ''}.json", "w"), indent=1)
print("\n".join(out[:3] + out[-3:]))
