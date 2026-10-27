"""The two "Know This" squares as key material (2026-10-27).  Pre-registered before any page was scored.

Page 16 carries a 5 x 5 square of numbers whose rows, columns and diagonals sum to 3301; page 5 a
5 x 5 square mixing numbers and rune words whose Gematria values complete a square summing to 1033
(3301 reversed; both prime), the same matrix Cicada handed solvers out of band in the 2014 onion
stage.  The words were chosen for their values.  This lane asks whether either square keys the
unsolved pages under the anti-repeat skip rule.

Key families (every one under 3 sign conventions x 2 F variants, soft-rule base decoder):
  N  the value matrices A (3301) and B (1033), each read in six orders (rows, columns, each reversed,
     spiral in, spiral out), plus A+B and B+A row-wise: as periodic keys, value mod 29; and as the
     concatenated decimal digits mod 29.
  P  the 50 values as offsets into the prime stream p[n+v] mod 29 and the totient stream phi(p[n+v]).
  W  the 11 distinct words as Vigenère keys; the 13 words in row order, in column order and reversed
     as phrase keys.
Not run, and why: LCG seeds drawn from the squares, because the short-list lane (§19) already ran
those generators at EVERY seed; transposition keyed by the squares, because the detection statistic
(unigram Viterbi score) is blind to symbol order, so a page that is scrambled English under any key
tested in §§9-25 would already have scored as a hit and none did.
RULE: a cell is a candidate only if z_uni >= 5 over the page's 2,000-keystream null (about 50,000
tests here, chance maximum about 4.6), z_5 >= 6 on the rune 5-gram rescoring, and it reads as English.
Controls: eight plants of solved English under the soft rule with keys from each family, at 262, 137
and 92 runes, signs and F cycled; a control passes at z_uni >= 5, z_5 >= 6 and rank 1 in the lane.
Usage: .venv/bin/python -I src/square_lane.py
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F, ngram

T5 = ngram.load_dense()
rng = np.random.default_rng(1033)
lu, plain = F.lu, F.plain
pages = [(p, C) for p, C in F.pages if len(C) > 0]
LMAX = F.LMAX
PR = np.array(primes(LMAX + 2000))
GV = {"F": 2, "U": 3, "TH": 5, "O": 7, "R": 11, "C": 13, "G": 17, "W": 19, "H": 23, "N": 29, "I": 31, "J": 37, "EO": 41, "P": 43, "X": 47, "S": 53, "T": 59, "B": 61, "E": 67, "M": 71, "L": 73, "NG": 79, "OE": 83, "D": 89, "A": 97, "AE": 101, "Y": 103, "IA": 107, "EA": 109}
VAL = np.array([GV[l] for l in LATIN])

A = np.array([[434, 1311, 312, 278, 966], [204, 812, 934, 280, 1071], [626, 620, 809, 620, 626], [1071, 280, 934, 812, 204], [966, 278, 312, 1311, 434]])
WORDS = {"SHADOWS": None, "AETHEREAL": None, "BUFFERS": None, "VOID": None, "CARNAL": None, "OBSCURA": None, "FORM": None, "MOBIUS": None, "ANALOG": None, "MOURNFUL": None, "CABAL": None}
for w in WORDS: WORDS[w] = english_to_runes(w)
gval = lambda w: int(VAL[WORDS[w]].sum())
Bcells = [[272, 138, "SHADOWS", 131, 151], ["AETHEREAL", "BUFFERS", "VOID", "CARNAL", 18], [226, "OBSCURA", "FORM", 245, "MOBIUS"], [18, "ANALOG", "VOID", "MOURNFUL", "AETHEREAL"], [151, 131, "CABAL", 138, 272]]
B = np.array([[c if isinstance(c, int) else gval(c) for c in row] for row in Bcells])
assert (A.sum(0) == 3301).all() and (A.sum(1) == 3301).all() and (B.sum(0) == 1033).all() and (B.sum(1) == 1033).all(), "square sums"


def orders(M):
    n = M.shape[0]
    def spiral(M):
        out, m = [], M.tolist()
        while m:
            out += m.pop(0)
            m = [list(r) for r in zip(*m)][::-1]
        return out
    sp = spiral(M)
    return {"rows": M.ravel().tolist(), "cols": M.T.ravel().tolist(), "rows-rev": M.ravel()[::-1].tolist(), "cols-rev": M.T.ravel()[::-1].tolist(), "spiral-in": sp, "spiral-out": sp[::-1]}


def rep(v, L=LMAX): return np.resize(np.asarray(v) % N, L)


keys, labels = [], []
for name, M in (("A3301", A), ("B1033", B)):
    for oname, seq in orders(M).items():
        keys.append(rep(seq)); labels.append(("N value mod 29", f"{name} {oname}"))
        digits = [int(ch) for v in seq for ch in str(v)]
        keys.append(rep(digits)); labels.append(("N digits mod 29", f"{name} {oname}"))
for name, seq in (("A+B", A.ravel().tolist() + B.ravel().tolist()), ("B+A", B.ravel().tolist() + A.ravel().tolist())):
    keys.append(rep(seq)); labels.append(("N value mod 29", f"{name} rows"))
for v in sorted(set(A.ravel().tolist() + B.ravel().tolist())):
    keys.append((PR[v:v + LMAX] % N)); labels.append(("P prime offset", f"p[n+{v}]"))
    keys.append(((PR[v:v + LMAX] - 1) % N)); labels.append(("P totient offset", f"phi(p[n+{v}])"))
for w, r in WORDS.items():
    keys.append(rep(r)); labels.append(("W word", w))
roww = [c for row in Bcells for c in row if isinstance(c, str)]
colw = [c for row in [list(x) for x in zip(*Bcells)] for c in row if isinstance(c, str)]
for pname, ws in (("row order", roww), ("column order", colw), ("row order reversed", roww[::-1])):
    keys.append(rep(sum((WORDS[w] for w in ws), []))); labels.append(("W phrase", pname))
Ks = np.stack(keys); nk = len(Ks)
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
Z_UNI, Z_5, NREPS, SOFT = 5.0, 6.0, 2000, 0.81
LOGU = np.log(1 / N)
t0 = time.time()
print(f"{nk} keys x 6 cells x {len(pages)} pages = {nk*6*len(pages):,} tests", flush=True)


def null_cell(C, f_rule, mode):
    Kr = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2))
    sc, _, dec = decode(C, Kr, lu, f_rule, mode); s5 = ngram.score_batch(dec, T5)
    return sc.mean(), sc.std(), s5.mean(), s5.std()


def score_all(C, f_rule, sign, mode, nul):
    Kb = (-Ks) % N if sign == "add" else Ks
    sc, _, dec = decode(C, Kb, lu, f_rule, mode)
    zu = (sc - nul[0]) / nul[1]; z5 = (ngram.score_batch(dec, T5) - nul[2]) / nul[3]
    return zu, z5, dec


# ---------- controls ----------
controls = []
plan = [(0, 262), (len(keys) - 3, 137), (14, 92), (30, 262), (40, 137), (len(keys) - 8, 262), (2, 92), (len(keys) - 1, 137)]
for ci, (ki, n) in enumerate(plan):
    sign, mode = SIGNS[ci % 3]; f_rule = bool((ci // 3) % 2)
    Ktrue = Ks[ki]                     # encrypt() applies the sign convention itself; the decoder side negates for 'add'
    o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
    C = encrypt(P, Ktrue, f_rule=f_rule, rng=rng, soft=SOFT, mode=sign)
    nul = null_cell(C, f_rule, mode); zu, z5, dec = score_all(C, f_rule, sign, mode, nul)
    rank = int((zu > zu[ki]).sum()) + 1; passed = zu[ki] >= Z_UNI and z5[ki] >= Z_5 and rank == 1
    controls.append(dict(key=labels[ki], n=n, sign=sign, F=f_rule, zu=float(zu[ki]), z5=float(z5[ki]), rank=rank, passed=bool(passed), rec=float((dec[ki] == P).mean())))
    print(f"  control {labels[ki]} n={n} {sign} F={f_rule}: z_uni {zu[ki]:.1f} z_5 {z5[ki]:.1f} rank {rank} -> {'PASS' if passed else 'miss'}", flush=True)

# ---------- pages ----------
cells, cands = [], []
for pid, C in pages:
    for f_rule in (False, True):
        nul_by = {}
        for sign, mode in SIGNS:
            if mode not in nul_by: nul_by[mode] = null_cell(C, f_rule, mode)
            zu, z5, dec = score_all(C, f_rule, sign, mode, nul_by[mode])
            for k in np.argsort(-zu)[:3]:
                cells.append(dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1], zu=float(zu[k]), z5=float(z5[k]), translit=translit(dec[k][:80])))
            for k in np.where((zu >= Z_UNI) & (z5 >= Z_5))[0]:
                cands.append(dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1], zu=float(zu[k]), z5=float(z5[k]), translit=translit(dec[k])))
    print(f"  {pid}: best z_uni {max(c['zu'] for c in cells if c['page']==pid):.2f}, best z_5 {max(c['z5'] for c in cells if c['page']==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)

best = sorted(cells, key=lambda c: -c["zu"])[:15]
out = [f"# The Know This squares as keys: {nk} keys x 6 cells x {len(pages)} pages = {nk*6*len(pages):,} tests", "",
       "Rule and families in the module docstring. Squares: A (page 16) rows/columns/diagonals sum to 3301; B (page 5) with its words replaced by their Gematria values sums to 1033. "
       f"Word values: " + ", ".join(f"{w} {gval(w)}" for w in WORDS) + ".", "",
       "## Controls", "", "| key | n | sign | F | z_uni | z_5 | rank | recovery | pass |", "|---|---|---|---|---|---|---|---|---|"]
for c in controls: out.append(f"| {c['key'][1]} ({c['key'][0]}) | {c['n']} | {c['sign']} | {c['F']} | {c['zu']:.1f} | {c['z5']:.1f} | {c['rank']} | {c['rec']:.2f} | {'yes' if c['passed'] else 'no'} |")
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Top 15 cells over all pages", "", "| page | sign | F | family | key | z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|"]
for c in best: out.append(f"| {c['page']} | {c['sign']} | {c['F']} | {c['fam']} | {c['key']} | {c['zu']:.2f} | {c['z5']:.1f} | {c['translit'][:60]} |")
out += ["", "## Candidates meeting the rule", ""] + ([f"- **{c['page']}** {c['sign']} F={c['F']} {c['fam']} {c['key']}: z_uni {c['zu']:.2f}, z_5 {c['z5']:.1f}: `{c['translit']}`" for c in cands] or ["None."])
out += ["", f"Largest z_uni {max(c['zu'] for c in cells):.2f}; largest z_5 {max(c['z5'] for c in cells):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / "squares.md").write_text("\n".join(out) + "\n")
json.dump(dict(nkeys=nk, labels=labels, A=A.tolist(), B=B.tolist(), controls=controls, cells=cells, candidates=cands, seconds=time.time() - t0), open(RESULTS / "squares.json", "w"), indent=1)
print("\n".join(out[-6:]))
