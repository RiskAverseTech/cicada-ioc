# -*- coding: utf-8 -*-
"""Does another copy of the transcription change anything this record measured?

Compares two transcription files: whether their rune streams are identical, which non-rune characters differ, and the five
counts of docs/replicate.md (runes, doublets, lag-5 equalities, S pairs, lag-6 hits) on the unsolved section of each, the
second also with ',' read as a word separator.  The files are read as data.  Run 2026-11-25 on the pinned file against
cicada-solvers/iddqd master (SHA-256 b0b2e13c...): runes identical, punctuation differs, all five counts unchanged.

    .venv/bin/python -I src/transcription_variant.py data/raw/iddqd__liber-primus__transcription--master.txt OTHER.txt
"""
import sys, collections
RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"; IDX = {r: i for i, r in enumerate(RUNES)}
def pages(path):
    ch = open(path, encoding="utf-8").read().split("%"); return ch
def parse(s, sep):
    runes, wid = [], []; w = 0; pending = False
    for c in s:
        if c in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[c]); wid.append(w)
        elif c in sep: pending = True
    return runes, wid
def counts(chunks, sep, lo=16, hi=72):
    n = k = l5 = l5s = l6 = p5 = p6 = npg = 0
    for s in chunks[lo:hi]:
        c, w = parse(s, sep)
        if len(c) <= 6: continue
        npg += 1; n += len(c); k += sum(c[i] == c[i-1] for i in range(1, len(c)))
        for i in range(5, len(c)):
            if w[i] == w[i-5]:
                p5 += 1
                if c[i] == c[i-5]: l5 += 1; l5s += c[i] == 15
        for i in range(6, len(c)):
            if w[i] == w[i-6]:
                p6 += 1; l6 += c[i] == (24 - 2*c[i-6]) % 29
    return dict(pages=npg, runes=n, doublets=k, pairs5=p5, L5=l5, L5S=l5s, pairs6=p6, L6T=l6)
a, b = pages(sys.argv[1]), pages(sys.argv[2]); print("chunks", len(a), len(b))
ra = "".join(c for c in open(sys.argv[1], encoding="utf-8").read() if c in IDX); rb = "".join(c for c in open(sys.argv[2], encoding="utf-8").read() if c in IDX)
print("rune streams identical (whole file):", ra == rb, len(ra), len(rb))
nonr = lambda p: collections.Counter(c for c in open(p, encoding="utf-8").read() if c not in IDX and not c.isspace())
ca, cb = nonr(sys.argv[1]), nonr(sys.argv[2]); print("non-rune character counts that differ:", {k: (ca[k], cb[k]) for k in set(ca) | set(cb) if ca[k] != cb[k]})
S0 = set("-.&$§")
print("A (pinned) sep -.&$§   :", counts(a, S0))
print("B sep -.&$§            :", counts(b, S0))
print("B sep -.&$§ plus comma :", counts(b, S0 | {","}))
# where do unsolved-section lines differ, by kind
import difflib
ua, ub = "%".join(a[16:72]).split("\n"), "%".join(b[16:72]).split("\n")
d = [l for l in difflib.unified_diff(ua, ub, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
print("differing lines in unsolved section:", sum(l[0] == "-" for l in d), "removed,", sum(l[0] == "+" for l in d), "added")
