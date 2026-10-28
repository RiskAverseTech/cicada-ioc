"""The echo statistics on the image-derived stream (2026-10-28, §49).  §38's blind re-reading classified every glyph of
the unsolved page images without the transcription (3-NN on crops, labels from the solved pages).  Here the resolved
blind readings are aligned to the transcription (difflib, as in §38), every aligned position takes the BLIND rune,
every unresolved or unaligned position is marked unknown, and the lag-5 equality, the S..S count and the lag-6
relation are recomputed on pairs whose two runes are both blind-read.  Word structure is the transcription's (the
re-reading has no word marks; pnotisdev audited the word dots against the images: 0 of 2,334 missing).  The same
statistics on the transcription restricted to the same pairs are shown beside them.  Writes results/reread_echoes.md."""
import json, sys, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
S = LATIN.index("S"); T = lambda x: (24 - 2 * x) % N
d = json.load(open(RESULTS / "reread.json")); R = d["readings"]; THR = d["T"]
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
pages = []
for nn in sorted(int(k) for k in R):
    chunk = nn - 1; truth, w = parse(chunks[chunk])
    if len(truth) == 0: continue
    pr_all, mg = R[str(nn)]["pred"], R[str(nn)]["margin"]; pr = [p for p, m in zip(pr_all, mg) if m >= THR]
    blind = np.full(len(truth), -1, int)
    sm = difflib.SequenceMatcher(a=list(truth), b=pr, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and (i2 - i1) == (j2 - j1) and (i2 - i1) <= 3):
            blind[i1:i2] = pr[j1:j2]
    pages.append((truth, blind, w))
tot = sum(len(t) for t, _, _ in pages); known = sum(int((b >= 0).sum()) for _, b, _ in pages); dis = sum(int(((b >= 0) & (b != t)).sum()) for t, b, _ in pages)
def stats(pages, use_blind):
    L5 = L5S = L6 = n5 = n6 = D = nD = 0
    for t, b, w in pages:
        c = b if use_blind else t; ok = b >= 0
        for i in range(5, len(c)):
            if w[i] == w[i - 5] and ok[i] and ok[i - 5]:
                n5 += 1
                if c[i] == c[i - 5]: L5 += 1; L5S += (c[i] == S)
        for i in range(6, len(c)):
            if w[i] == w[i - 6] and ok[i] and ok[i - 6]:
                n6 += 1; L6 += (c[i] == T(c[i - 6]))
        for i in range(1, len(c)):
            if ok[i] and ok[i - 1]: nD += 1; D += (c[i] == c[i - 1])
    return dict(n5=n5, L5=L5, L5S=L5S, n6=n6, L6=L6, nD=nD, D=D)
sb, st = stats(pages, True), stats(pages, False)
out = ["# The echo statistics on the image-derived stream", "",
       f"{tot:,} transcription positions; {known:,} ({known/tot:.1%}) carry a blind reading (resolved and aligned); the blind reading differs from the transcription at {dis} of them. Statistics below use only pairs whose two runes are both blind-read; the transcription column is restricted to the same pairs.", "",
       "| statistic | blind reading | transcription, same pairs | expected if uniform |", "|---|---|---|---|",
       f"| within-word pairs at lag 5 | {sb['n5']:,} | {st['n5']:,} | |",
       f"| equal at lag 5 | {sb['L5']} | {st['L5']} | {sb['n5']/N:.1f} |",
       f"| of which S..S | {sb['L5S']} | {st['L5S']} | {sb['n5']/N**2:.1f} |",
       f"| within-word pairs at lag 6 | {sb['n6']:,} | {st['n6']:,} | |",
       f"| c = 24 − 2c′ at lag 6 | {sb['L6']} | {st['L6']} | {sb['n6']/N:.1f} |",
       f"| adjacent pairs | {sb['nD']:,} | {st['nD']:,} | |",
       f"| adjacent repeats | {sb['D']} | {st['D']} | {sb['nD']/N:.1f} |", "",
       "Reading: the blind reading was produced from the page images by a classifier that never saw the transcription of these pages; if the three structures were artefacts of the transcription's lineage, typography conventions or rune indexing, they would not survive here. The word structure is the transcription's, which the image audit of pnotisdev confirms separately.", ""]
(RESULTS / "reread_echoes.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
