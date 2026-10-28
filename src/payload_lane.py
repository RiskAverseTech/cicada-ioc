"""The three-page base-60 payload (LP2-49, LP2-50, LP2-51: 80 + 104 + 72 = 256 bytes) as key material
(2026-10-28).  Pre-registered.  Ledger first: wazar tested this payload as a PRF seed expanded by
RC4, AES-CTR, SHA counters, HMAC-DRBG and ChaCha20 (B-05), as an RSA signature under every known
Cicada modulus (E-01), as meta-parameters (E-02), as a direct numeric key at every offset (numeric
round 2) and in a POINTERS track (Round 8); six bytes are contested where the glyphs I/l and O/0 are
ambiguous (RECON-A A-04).  So this lane is a REPLICATION with controls under this repository's
exact decoder of the direct and pointer readings, with both readings of the contested bytes; the PRF
expansions are not repeated.

Readings of the 256 bytes (archive order 49 -> 50 -> 51, and reversed):
  R1 byte mod 29;  R2 rejection (bytes >= 232 dropped, then mod 29);  R3 bit-reversed byte mod 29;
  R4 the base-60 index component (0-59) mod 29;  R5 the digit component (0-4) as a 5-symbol key;
  P  each distinct byte b as an offset into the prime stream p[n+b] and the totient stream;
  W  pointers: the solved plaintext's rune at index b (b < 256), and the solved text's word at index b
     mod word count as a 256-word phrase key.
  Added 2026-10-28 after the field survey (yo-yo-yo-jbo ran these rigidly, Pitchfork-and-Torch every phase
  under an IoC screen): O  all six page orderings of the three pages, forward and reversed, for R1, R4 and R5;
  R6 the base-59 value digit*59 + index mod 29 (base 59 drops F), all orderings and directions.
All under 3 signs x 2 F with the soft-rule decoder on all 55 pages.  Rule: z_uni >= 5 over the page's
2,000-keystream null AND 5-gram z_5 >= 6 AND readable.  Controls: four plants (R1, R2 reversed, a prime
offset, the word-pointer phrase) at 262 and 137 runes; pass at z_uni >= 5, z_5 >= 6, rank 1 in the lane.
Usage: python -I src/payload_lane.py
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX, MAX_SKIP
from skip_decrypt import encrypt
import families as F, ngram

T5 = ngram.load_dense(); rng = np.random.default_rng(256)
lu, plain, pages = F.lu, F.plain, [(p, C) for p, C in F.pages if len(C) > 0]
LMAX = F.LMAX; PR = np.array(primes(LMAX + 400))
pl = json.loads((PROCESSED / "payload.json").read_text())
B = np.array(sum((pl["pages"][p]["bytes_archive"] for p in pl["order"]), [])); Bt = np.array(sum((pl["pages"][p]["bytes_token_reading"] for p in pl["order"]), []))
toks = sum((pl["pages"][p]["tokens"] for p in pl["order"]), [])
assert len(B) == 256
words = [w for line in F.lines for w in line]
rep = lambda v: np.resize(np.asarray(v) % N, LMAX)
keys, labels = [], []
for name, arr in (("archive", B), ("token-reading", Bt)):
    for oname, seq in (("fwd", arr), ("rev", arr[::-1])):
        keys.append(rep(seq)); labels.append(("R1 byte mod 29", f"{name} {oname}"))
        keys.append(rep(seq[seq < 232])); labels.append(("R2 rejection", f"{name} {oname}"))
        keys.append(rep([int(f"{b:08b}"[::-1], 2) for b in seq])); labels.append(("R3 bit-reversed", f"{name} {oname}"))
for oname, seq in (("fwd", toks), ("rev", toks[::-1])):
    ALPH = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    keys.append(rep([ALPH.index(t[1]) for t in seq])); labels.append(("R4 index component", oname))
    keys.append(rep([int(t[0]) for t in seq])); labels.append(("R5 digit component", oname))
for b in sorted(set(B.tolist())):
    keys.append(PR[b:b + LMAX] % N); labels.append(("P prime offset", f"p[n+{b}]"))
    keys.append((PR[b:b + LMAX] - 1) % N); labels.append(("P totient offset", f"phi(p[n+{b}])"))
keys.append(rep(plain[B])); labels.append(("W rune pointer", "solved plaintext[b]"))
keys.append(rep(plain[Bt])); labels.append(("W rune pointer", "solved plaintext[b] token reading"))
keys.append(rep(sum((english_to_runes(words[b % len(words)]) for b in B), []))); labels.append(("W word pointer", "solved words[b mod count]"))
import itertools
ALPH = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
for perm in itertools.permutations(pl["order"]):
    pname = ">".join(p[-2:] for p in perm)
    seqB = np.array(sum((pl["pages"][p]["bytes_archive"] for p in perm), [])); seqT = sum((pl["pages"][p]["tokens"] for p in perm), [])
    for oname, sb, st in (("fwd", seqB, seqT), ("rev", seqB[::-1], seqT[::-1])):
        new_order = list(perm) != pl["order"]
        if new_order:
            keys.append(rep(sb)); labels.append(("O R1 byte mod 29", f"{pname} {oname}"))
            keys.append(rep([ALPH.index(t[1]) for t in st])); labels.append(("O R4 index component", f"{pname} {oname}"))
            keys.append(rep([int(t[0]) for t in st])); labels.append(("O R5 digit component", f"{pname} {oname}"))
        keys.append(rep([int(t[0]) * 59 + ALPH.index(t[1]) for t in st])); labels.append(("R6 base-59 value", f"{pname} {oname}"))
Ks = np.stack(keys); nk = len(Ks)
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort")); Z_UNI, Z_5, NREPS = 5.0, 6.0, 2000
t0 = time.time(); print(f"{nk} keys x 6 cells x {len(pages)} pages = {nk*6*len(pages):,} tests", flush=True)


def null_cell(C, f_rule, mode):
    Kr = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2)); sc, _, dec = decode(C, Kr, lu, f_rule, mode); s5 = ngram.score_batch(dec, T5)
    return sc.mean(), sc.std(), s5.mean(), s5.std()


def score_all(C, f_rule, sign, mode, nul):
    Kb = (-Ks) % N if sign == "add" else Ks; sc, _, dec = decode(C, Kb, lu, f_rule, mode)
    return (sc - nul[0]) / nul[1], (ngram.score_batch(dec, T5) - nul[2]) / nul[3], dec


controls = []
for ci, (ki, n) in enumerate([(0, 262), (7, 137), (20, 262), (nk - 1, 137)]):
    sign, mode = SIGNS[ci % 3]; f_rule = bool(ci // 2)
    o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]; C = encrypt(P, Ks[ki], f_rule=f_rule, rng=rng, soft=0.81, mode=sign)
    nul = null_cell(C, f_rule, mode); zu, z5, dec = score_all(C, f_rule, sign, mode, nul); rank = int((zu > zu[ki]).sum()) + 1
    passed = zu[ki] >= Z_UNI and z5[ki] >= Z_5 and rank == 1
    controls.append(dict(key=labels[ki], n=n, sign=sign, F=f_rule, zu=float(zu[ki]), z5=float(z5[ki]), rank=rank, passed=bool(passed)))
    print(f"  control {labels[ki]} n={n} {sign} F={f_rule}: z_uni {zu[ki]:.1f} z_5 {z5[ki]:.1f} rank {rank} -> {'PASS' if passed else 'miss'}", flush=True)

cells, cands = [], []
for pid, C in pages:
    for f_rule in (False, True):
        nul_by = {}
        for sign, mode in SIGNS:
            if mode not in nul_by: nul_by[mode] = null_cell(C, f_rule, mode)
            zu, z5, dec = score_all(C, f_rule, sign, mode, nul_by[mode])
            for k in np.argsort(-zu)[:2]: cells.append(dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1], zu=float(zu[k]), z5=float(z5[k]), translit=translit(dec[k][:80])))
            for k in np.where((zu >= Z_UNI) & (z5 >= Z_5))[0]: cands.append(dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1], zu=float(zu[k]), z5=float(z5[k]), translit=translit(dec[k])))
    print(f"  {pid}: best z_uni {max(c['zu'] for c in cells if c['page']==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)
best = sorted(cells, key=lambda c: -c["zu"])[:10]
out = [f"# The 256-byte payload of LP2-49/50/51 as key material: {nk} keys x 6 cells x 55 pages = {nk*6*55:,} tests", "",
       "Readings, rule and prior coverage (wazar B-05, E-01, E-02, numeric round 2, Round 8 POINTERS) in the module docstring. Contested bytes (I/l, O/0 glyphs): " + ", ".join(f"{p} positions {pl['pages'][p]['contested']}" for p in pl['order']) + "; both readings run.", "",
       "## Controls", "", "| key | n | sign | F | z_uni | z_5 | rank | pass |", "|---|---|---|---|---|---|---|---|"]
for c in controls: out.append(f"| {c['key'][1]} ({c['key'][0]}) | {c['n']} | {c['sign']} | {c['F']} | {c['zu']:.1f} | {c['z5']:.1f} | {c['rank']} | {'yes' if c['passed'] else 'no'} |")
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Top 10 cells", "", "| page | sign | F | family | key | z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|"]
for c in best: out.append(f"| {c['page']} | {c['sign']} | {c['F']} | {c['fam']} | {c['key']} | {c['zu']:.2f} | {c['z5']:.1f} | {c['translit'][:60]} |")
out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"Largest z_uni {max(c['zu'] for c in cells):.2f}; largest z_5 {max(c['z5'] for c in cells):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
(RESULTS / "payload.md").write_text("\n".join(out) + "\n"); json.dump(dict(nkeys=nk, labels=labels, controls=controls, cells=cells, candidates=cands, seconds=time.time() - t0), open(RESULTS / "payload.json", "w"), indent=1)
print("\n".join(out[-5:]))
