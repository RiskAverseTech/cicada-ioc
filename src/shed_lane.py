"""The hint-reading family: "shed our own circumferences" read as an operation (2026-10-28, §52). Pre-registered.

The last solved page (a 2013 self-quotation) says "like the instar tunnelling to the surface, we must shed our own
circumferences; find the divinity within and emerge".  Read as instructions on the ciphertext, the field has filled
most of the cells (README §50 table).  Two are empty and cheap:
  WORD   the first and the last rune of every word are written in clear and consume no key value (a literal rune, as the
         solved pages' F); the interior is encrypted with the skip rule.  One- and two-rune words are entirely literal.
  RING   the first and the last line of every page are written in clear and consume no key; the interior lines are
         encrypted with the skip rule.
Decoder: score.decode with null_mask at those positions and penalty +50, which forces the null transition there (the
constant +50 per forced position cancels in z); the anti-repeat comparison still runs against the previous emitted
rune, as the mechanism would.  Library: families.ALLSETS, 3 signs x 2 F variants, all 55 pages.  Rule: z_uni >= 6 over
2,000 random keystreams through the same masks AND 5-gram z_5 >= 6 AND readable.  Controls: 12 plants (6 per kind;
English in its own words or laid into the page's lines, literal edges, skip rule q 0.81, key from the library), pass at
rank 1 with z_uni >= 6.  Usage: SMOKE=1; KIND=word|ring|both.  Writes results/shed_lane.md/.json.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX
from skip_decrypt import combine
import families as F, ngram, corpus

SMOKE = os.environ.get("SMOKE") == "1"; KINDS = ["word", "ring"] if os.environ.get("KIND", "both") == "both" else [os.environ["KIND"]]
rng = np.random.default_rng(761)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
EDGES = json.load(open(PROCESSED / "edges.json"))
SETS = F.ALLSETS; PEN = 50.0; Q = 0.81
Z_UNI, Z_5, NREPS = 6.0, 6.0, (200 if SMOKE else 2000)
T5 = ngram.load_dense()
if SMOKE: pages = pages[:2]

def mask_word(pid, n):
    e = EDGES[pid]; m = np.zeros(n, bool); m[0] = True; m[n - 1] = True
    m[e["word_initial"]] = True; m[e["word_final"]] = True; return m
def mask_ring(pid, n):
    e = EDGES[pid]; li = [0] + list(e["line_initial"]); m = np.zeros(n, bool)
    m[:li[1] if len(li) > 1 else n] = True; m[li[-1]:] = True; return m
MASK = {"word": mask_word, "ring": mask_ring}

def dec(C, Ks, f_rule, mode, mask): return decode(C, Ks, lu, f_rule, mode, null_mask=mask, penalty=PEN)
def null_z(C, f_rule, mode, mask, reps):
    Kr = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2)); s = dec(C, Kr, f_rule, mode, mask)[0]; return s.mean(), s.std()
def scores_all(C, Ks, f_rule, mode, mask, batch=1500):
    sc = np.empty(len(Ks))
    for b in range(0, len(Ks), batch): sc[b:b + batch] = dec(C, Ks[b:b + batch], f_rule, mode, mask)[0]
    return sc
def z5_of(C, f_rule, mode, mask, decs):
    Kr = rng.integers(0, N, size=(300 if SMOKE else 1000, len(C) + S_MAX + 2)); _, _, outn = dec(C, Kr, f_rule, mode, mask)
    s5n = ngram.score_batch(outn, T5); s5 = ngram.score_batch(np.stack(decs), T5); return (s5 - s5n.mean()) / s5n.std()

text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(wd) for wd in text.split()]; EW = [wd for wd in EW if wd]
def english_words(n):
    wi = int(rng.integers(0, len(EW) - 500)); P, W = [], []; k = 0
    while len(P) < n: wd = EW[wi]; wi += 1; P += wd; W += [k] * len(wd); k += 1
    return np.array(P[:n]), np.array(W[:n])

def encrypt_shed(P, mask, K, sign, f_rule, q=Q):
    """Positions in mask are literal (plaintext written, no key consumed); the rest under the skip rule."""
    C = np.empty(len(P), int); j = 0; prev = -1
    for i, p in enumerate(P):
        if mask[i] or (f_rule and p == 0): C[i] = p; prev = p; continue
        c = combine(p, K[j], sign)
        while prev != -1 and c == prev and rng.random() < q: j += 1; c = combine(p, K[j], sign)
        C[i] = c; prev = c; j += 1
    return C

t0 = time.time(); nconf = sum(len(L) for *_, L in SETS)
print(f"{nconf} configurations x {len(pages)} pages x 2 F x {len(KINDS)} kinds", flush=True)
controls = []
for ci in range(4 if SMOKE else 12):
    kind = KINDS[ci % len(KINDS)]; sign, mode, Ks, labs = SETS[ci % len(SETS)]; f_rule = bool((ci // 6) % 2)
    ki = int(rng.integers(0, len(Ks))); Ktrue = Ks[ki] if sign != "add" else (-Ks[ki]) % N
    pid, C0 = pages[ci % len(pages)]; n = len(C0)
    P, W = english_words(n)
    if kind == "word":
        m = np.zeros(n, bool); m[0] = m[-1] = True
        for i in range(1, n):
            if W[i] != W[i - 1]: m[i] = True; m[i - 1] = True
    else: m = mask_ring(pid, n)
    C = encrypt_shed(P, m, Ktrue, sign, f_rule)
    m0, s0 = null_z(C, f_rule, mode, m, 400); sc = scores_all(C, Ks, f_rule, mode, m)
    z = (sc - m0) / s0; rank = int((z > z[ki]).sum()) + 1
    mb, sb = null_z(C, f_rule, mode, None, 400); zb = (decode(C, Ks[ki:ki + 1], lu, f_rule, mode)[0][0] - mb) / sb
    rec = dec(C, Ks[ki:ki + 1], f_rule, mode, m)[2][0]; acc = float((rec == P).mean())
    passed = z[ki] >= Z_UNI and rank == 1
    controls.append(dict(kind=kind, sign=sign, F=f_rule, family=labs[ki][0], key=labs[ki][1][:30], literal=int(m.sum()), n=n, z=float(z[ki]), rank=rank, z_base=float(zb), acc=acc, passed=bool(passed)))
    print(f"  control {ci}: {kind} {sign} F={f_rule} {labs[ki][0]} literal {int(m.sum())}/{n}: z {z[ki]:.1f} rank {rank}, base z {zb:.1f}, acc {acc:.3f} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)

cells, cands = [], []
for pid, C in pages:
    for kind in KINDS:
        m = MASK[kind](pid, len(C))
        for f_rule in (False, True):
            for sign, mode, Ks, labs in SETS:
                m0, s0 = null_z(C, f_rule, mode, m, NREPS); sc = scores_all(C, Ks, f_rule, mode, m)
                z = (sc - m0) / s0; k = int(z.argmax())
                cells.append(dict(page=pid, kind=kind, F=f_rule, sign=sign, family=labs[k][0], key=labs[k][1][:40], z=float(z[k]), literal=int(m.sum()), n=len(C)))
                if z[k] >= Z_UNI:
                    ks = [int(x) for x in np.where(z >= Z_UNI)[0]]; decs = [dec(C, Ks[x:x + 1], f_rule, mode, m)[2][0] for x in ks]; z5 = z5_of(C, f_rule, mode, m, decs)
                    for x, zz5, d in zip(ks, z5, decs):
                        c = dict(page=pid, kind=kind, F=f_rule, sign=sign, family=labs[x][0], key=labs[x][1][:40], z=float(z[x]), z5=float(zz5), translit=translit(d[:80])); cands.append(c); print(f"  z>=6: {c}", flush=True)
    print(f"  {pid} done: best z " + ", ".join(f"{k} {max(r['z'] for r in cells if r['page']==pid and r['kind']==k):.2f}" for k in KINDS) + f"  [{time.time()-t0:.0f}s]", flush=True)

hits = [c for c in cands if c["z5"] >= Z_5]; tag = "_smoke" if SMOKE else ""
out = [f"# Shed the circumferences: word edges and page rings written in clear ({', '.join(KINDS)})", "",
       f"{nconf} configurations x {len(pages)} pages x 2 F variants x {len(KINDS)} kinds = {nconf*len(pages)*2*len(KINDS):,} tests; null per cell {NREPS} random keystreams through the same mask; rule z_uni >= {Z_UNI} and z_5 >= {Z_5} and readable.", "",
       "## Controls", "", "| kind | sign | F | family | key | literal runes / page | decoder z (rank) | base-decoder z | plaintext recovered | pass |", "|---|---|---|---|---|---|---|---|---|---|"]
for c in controls: out.append(f"| {c['kind']} | {c['sign']} | {c['F']} | {c['family']} | {c['key']} | {c['literal']}/{c['n']} | {c['z']:.1f} ({c['rank']}) | {c['z_base']:.1f} | {c['acc']:.3f} | {'yes' if c['passed'] else 'no'} |")
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Best cell per page and kind", "", "| page | kind | literal runes | best z | sign | F | family | key |", "|---|---|---|---|---|---|---|---|"]
for pid, _ in pages:
    for k in KINDS:
        r = max((r for r in cells if r["page"] == pid and r["kind"] == k), key=lambda r: r["z"]); out.append(f"| {pid} | {k} | {r['literal']}/{r['n']} | {r['z']:.2f} | {r['sign']} | {r['F']} | {r['family']} | {r['key']} |")
out += ["", f"## Cells at z_uni >= {Z_UNI} ({len(cands)})", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"## Hits (also z_5 >= {Z_5}): {len(hits)}", ""] + ([f"- {c}" for c in hits] or ["None."]) + ["", f"Largest z_uni over all cells: {max(r['z'] for r in cells):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / f"shed_lane{tag}.md").write_text("\n".join(out) + "\n")
json.dump(dict(controls=controls, cells=cells, candidates=cands, hits=hits, ntests=nconf * len(pages) * 2 * len(KINDS)), open(RESULTS / f"shed_lane{tag}.json", "w"), indent=1)
print("\n".join(out[:3] + out[-3:]))
