"""Cicada's own words as Vigenère keys under the skip rule (2026-10-29, §53).  Pre-registered.

Ledger: pnotisdev's `solved-phrase-keys` row covers words and phrases of the solved pages and of the 2014 signed
messages (<= 24 runes, 8 spellings, layer2 engine); `signed-streams` covers the 2014 payload bytes; `p60-lp1-key`
the solved translation as a book key.  Nothing covers the group's 2012 and 2013 prose.  Corpus: every PGP-signed
message body 2012-2017 and the quoted unsigned texts (the 2012 and 2013 opening images, the 2013 parable, the 2016
outguess text), assembled from scream314/cicada3301's year narratives into data/corpus/raw/cicada_own_words_2012_2017.txt.
Keys: every distinct word of 2+ runes, every contiguous 2-, 3- and 4-word phrase, every line, forwards and reversed,
in the book's digraph spelling (english_to_runes); 3 signs x 2 F variants; all 55 pages; the §9 Viterbi.
Rule: z_uni >= 6 over 2,000 random keystreams AND 5-gram z_5 >= 6 AND readable.  Controls: 6 plants (262 runes of
English, a corpus key, soft rule 0.81, signs and F cycled) at rank 1 with z_uni >= 6.  Writes results/cicada_words.md/.json.
Usage: SMOKE=1 for a quick check."""
import json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *
from score import decode, translit, S_MAX
from skip_decrypt import encrypt
import families as F, ngram
SMOKE = os.environ.get("SMOKE") == "1"; rng = np.random.default_rng(3301)
lu, plain = F.lu, F.plain; pages = [(p, C) for p, C in F.pages if len(C) > 0]; LMAX = F.LMAX
Z_UNI, Z_5, NREPS = 6.0, 6.0, (200 if SMOKE else 2000); T5 = ngram.load_dense()
if SMOKE: pages = pages[:2]
raw = (RAW.parent / "corpus" / "raw" / "cicada_own_words_2012_2017.txt").read_text()
texts = [re.sub(r"^\[[^\]]*\]\n", "", blk).strip() for blk in raw.split("\n\n") if blk.strip()]
keys = {}
def add(fam, label, r):
    t = tuple(r)
    if 2 <= len(t) <= 400 and t not in keys: keys[t] = (fam, label)
for t in texts:
    for line in t.splitlines():
        words = re.findall(r"[A-Za-z']+", line)
        for w in words:
            r = english_to_runes(w); add("word", w, r); add("word-rev", w + "ʳ", r[::-1])
        for n in (2, 3, 4):
            for i in range(len(words) - n + 1):
                ph = " ".join(words[i:i + n]); r = english_to_runes(ph); add(f"phrase-{n}", ph, r); add(f"phrase-{n}-rev", ph + "ʳ", r[::-1])
        if len(words) >= 5:
            r = english_to_runes(" ".join(words)); add("line", line[:50], r); add("line-rev", line[:50] + "ʳ", r[::-1])
labels = list(keys.values()); Ks = np.stack([np.resize(np.array(k) % N, LMAX) for k in keys]).astype(np.int64)
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
t0 = time.time(); print(f"{len(Ks)} keys x 6 cells x {len(pages)} pages = {len(Ks)*6*len(pages):,} tests", flush=True)
def null_cell(C, f_rule, mode):
    Kr = rng.integers(0, N, size=(NREPS, len(C) + S_MAX + 2)); sc, _, dec = decode(C, Kr, lu, f_rule, mode)
    s5 = ngram.score_batch(dec, T5); return sc.mean(), sc.std(), s5.mean(), s5.std()
def score_all(C, f_rule, sign, mode, nul, batch=1500):
    K = (-Ks) % N if sign == "add" else Ks; m0, s0, m5, s5 = nul; zu = np.empty(len(K)); z5 = np.full(len(K), np.nan); decs = {}
    for b in range(0, len(K), batch):
        sc, _, dec = decode(C, K[b:b + batch], lu, f_rule, mode); zu[b:b + batch] = (sc - m0) / s0
        for k in np.where(zu[b:b + batch] >= Z_UNI - 1)[0]: z5[b + k] = (ngram.score_batch(dec[k:k + 1], T5)[0] - m5) / s5; decs[b + k] = dec[k]
    return zu, z5, decs
controls = []
for ci in range(2 if SMOKE else 6):
    sign, mode = SIGNS[ci % 3]; f_rule = bool(ci % 2); ki = int(rng.integers(0, len(Ks))); n = 262
    Kt = Ks[ki] if sign != "add" else (-Ks[ki]) % N; o = int(rng.integers(0, len(plain) - n - 1)); P = plain[o:o + n]
    C = encrypt(P, Kt, f_rule=f_rule, rng=rng, soft=0.81, mode=sign); nul = null_cell(C, f_rule, mode); zu, z5, decs = score_all(C, f_rule, sign, mode, nul)
    rank = int((zu > zu[ki]).sum()) + 1; passed = zu[ki] >= Z_UNI and rank == 1
    controls.append(dict(key=labels[ki], sign=sign, F=f_rule, zu=float(zu[ki]), z5=float(z5[ki]) if not np.isnan(z5[ki]) else None, rank=rank, passed=bool(passed)))
    print(f"  control {ci}: {labels[ki]} {sign} F={f_rule}: z_uni {zu[ki]:.1f} rank {rank} -> {'PASS' if passed else 'miss'}  [{time.time()-t0:.0f}s]", flush=True)
cells, cands = [], []
for pid, C in pages:
    for f_rule in (False, True):
        for sign, mode in SIGNS:
            nul = null_cell(C, f_rule, mode); zu, z5, decs = score_all(C, f_rule, sign, mode, nul); k = int(zu.argmax())
            cells.append(dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1][:40], zu=float(zu[k]), z5=float(z5[k]) if not np.isnan(z5[k]) else None))
            for k in np.where((zu >= Z_UNI) & (np.nan_to_num(z5, nan=-9) >= Z_5))[0]:
                c = dict(page=pid, sign=sign, F=f_rule, fam=labels[k][0], key=labels[k][1][:40], zu=float(zu[k]), z5=float(z5[k]), translit=translit(decs[k][:80])); cands.append(c); print("  CANDIDATE", c, flush=True)
    print(f"  {pid}: best z_uni {max(c['zu'] for c in cells if c['page']==pid):.2f}  [{time.time()-t0:.0f}s]", flush=True)
best = sorted(cells, key=lambda c: -c["zu"])[:10]
out = [f"# Cicada's own words (2012–2017) as Vigenère keys under the skip rule", "", f"{len(Ks):,} keys (words, 2–4-word phrases and lines of {len(texts)} texts, forwards and reversed) x 3 signs x 2 F x {len(pages)} pages = {len(Ks)*6*len(pages):,} tests; rule z_uni >= {Z_UNI} and z_5 >= {Z_5} and readable; null {NREPS} keystreams per cell.", "",
       "## Controls", "", "| key | sign | F | z_uni | z_5 | rank | pass |", "|---|---|---|---|---|---|---|"] + [f"| {c['key'][1][:30]} ({c['key'][0]}) | {c['sign']} | {c['F']} | {c['zu']:.1f} | {c['z5'] if c['z5'] is None else round(c['z5'],1)} | {c['rank']} | {'yes' if c['passed'] else 'no'} |" for c in controls]
out += ["", f"Controls passing: {sum(c['passed'] for c in controls)} of {len(controls)}.", "", "## Top 10 cells", "", "| page | sign | F | family | key | z_uni | z_5 |", "|---|---|---|---|---|---|---|"] + [f"| {c['page']} | {c['sign']} | {c['F']} | {c['fam']} | {c['key']} | {c['zu']:.2f} | {'' if c['z5'] is None else round(c['z5'],1)} |" for c in best]
out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"Largest z_uni {max(c['zu'] for c in cells):.2f}. Runtime {(time.time()-t0)/60:.0f} minutes.", ""]
tag = "_smoke" if SMOKE else ""
(RESULTS / f"cicada_words{tag}.md").write_text("\n".join(out) + "\n"); json.dump(dict(controls=controls, cells=cells, candidates=cands, ntests=len(Ks) * 6 * len(pages), nkeys=len(Ks)), open(RESULTS / f"cicada_words{tag}.json", "w"), indent=1)
print("\n".join(out[:3] + out[-3:]))
