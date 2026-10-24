"""Phase 5: plaintext registers other than English.  Builds rune-unigram models for Latin and
Old English from public-domain corpora, using the same word-by-word transliteration the book
uses for English (digraphs TH, NG, OE, AE, EO, EA, IA, IO never straddle a word; QU -> CW,
V -> U, K -> C, Z -> S).  Old English thorn/eth become TH, ash becomes AE, wynn becomes W, and
vowel-length marks are dropped.  Saves data/processed/registers.json.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N, RAW, PROCESSED, LATIN, english_to_runes
from score import english_model

CORP = RAW / "corpora"


def runes_of(path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    out = []
    for line in txt.splitlines():
        line = re.sub(r"[^A-Za-z' ]", " ", line)
        out.extend(english_to_runes(line))
    return np.array(out, dtype=np.int64)


def model(r):
    uni = np.bincount(r, minlength=N) + 0.5
    return np.log(uni / uni.sum())


if __name__ == "__main__":
    lu_en, _, plain_en = english_model()
    regs = {"en": (lu_en, plain_en)}
    for name, f in (("la", "latin_corpus.txt"), ("ang", "oe_corpus.txt")):
        r = runes_of(CORP / f)
        regs[name] = (model(r), r)
        print(f"{name}: {len(r):,} runes")
    # rune frequency tables side by side
    print(f"{'rune':5s}" + "".join(f"{k:>8s}" for k in regs))
    for i in range(N):
        print(f"{LATIN[i]:5s}" + "".join(f"{np.exp(regs[k][0][i])*100:8.2f}" for k in regs))
    # cross-register scoring: mean log-likelihood ratio per rune of each corpus under each model
    print("\nmean LLR per rune (rows: text; cols: model), relative to uniform:")
    LOGU = np.log(1 / N)
    for tname, (_, text) in regs.items():
        row = []
        for mname, (lu, _) in regs.items():
            row.append((lu[text] - LOGU).mean())
        print(f"  {tname:4s}" + "".join(f"{v:8.3f}" for v in row))
    json.dump({k: {"lu": v[0].tolist(), "n": int(len(v[1]))} for k, v in regs.items()},
              open(PROCESSED / "registers.json", "w"))
    np.savez(PROCESSED / "registers_text.npz", **{k: v[1] for k, v in regs.items()})
    print("saved registers.json / registers_text.npz")
