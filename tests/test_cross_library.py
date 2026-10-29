"""Fast checks of the rebuilt pnotisdev library (README §54): the manifest, the generator's building blocks, and (when the
external download is present) the first runes of their published model-0 decodes."""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import numpy as np
import pnotisdev_library as PL
from lp import LATIN, N

ROOT = Path(__file__).resolve().parent.parent


def manifest():
    rows = [r for r in csv.reader(open(ROOT / "data" / "processed" / "pnotisdev_library_manifest.tsv", encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    return rows[1:]


def test_manifest_counts_match_their_export():
    rows = manifest()
    assert len(rows) == 1439                                   # their 2026-10-18 note: "the library export is unchanged (1,439 streams)"
    assert sum(1 for r in rows if int(r[3]) == 0) == 580       # non-periodic streams (their "581 flat streams" up to one periodicity call)
    fam = {}
    for r in rows: fam[r[1]] = fam.get(r[1], 0) + 1
    assert fam == {"integer": 52, "constant": 12, "cicada": 16, "number2": 22, "constant2": 13, "hash": 520, "payload": 3, "keyword": 801}
    first = {r[2]: r[4] for r in rows}
    assert first["primes"] == "2 3 5 7 11 13 17 19 23 0 2 8" and first["primes-1 (totient)"].startswith("1 2 4 6 10 12")


def test_their_word_to_key_and_keywords():
    assert PL.word_to_key("DIVINITY") == [23, 10, 1, 10, 9, 10, 16, 26]
    assert PL.word_to_key("FIRFUMFERENFE") == [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]
    assert PL.word_to_key("THING") == [2, 21] and PL.word_to_key("KING") == [5, 21]      # ING is one rune in their table
    segs = PL.load_segments()
    assert len(segs) == 18 and [len(PL.runes_of(s)) for s in segs[7:16]] == [729, 1145, 1729, 9, 1894, 1021, 1524, 1589, 3316]
    assert PL.an_end_hash(segs).startswith("36367763ab73783c") and len(PL.an_end_hash(segs)) == 128
    pb = PL.grid_bytes(); assert len(pb) == 256 and pb[:4].hex() == "cbe7a7ba"
    kw = PL.keywords(segs)
    assert "kw:DIVINITY" in kw and "kw:BELIEUE" in kw and kw["kw:DIVINITY"][:8].tolist() == [23, 10, 1, 10, 9, 10, 16, 26]


def test_published_decodes_reproduce_if_download_present():
    """Their library_segments_verify.txt lists the decode of a window under (stream, offset, mult, model 0); the runes before the
    first possible skip must equal a plain decode with the rebuilt stream."""
    vf = ROOT / "data" / "external" / "pnotisdev" / "results" / "kscreen" / "library_segments_verify.txt"
    if not vf.exists() or not PL.CACHE.exists():
        import pytest; pytest.skip("external download not present")
    names, fams, periods, K = PL.load(); idx = {n: i for i, n in enumerate(names)}; segs = PL.load_segments()
    LAT = list(LATIN); LAT[21] = "ING"
    hits = re.findall(r"'([^']+)' offset=(\d+) mult=(\d+) model=0 window=seg0\.(\d+)[^\n]*\n\s+decoded : (\S+)", vf.read_text(encoding="utf-8"))
    assert len(hits) >= 5
    for name, off, mult, seg, decoded in hits:
        off, mult, seg = int(off), int(mult), int(seg); c = PL.runes_of(segs[seg]); k = K[idx[name]].astype(int); out = []; j = off
        for i, ci in enumerate(c[:60]):
            if i > 0 and (ci - c[i - 1] - mult * (k[j + 1] - k[j])) % N == 0: break
            out.append(LAT[(ci - mult * k[j]) % N]); j += 1
        mine = "".join(out); assert len(mine) >= 4 and decoded.startswith(mine), (name, mine, decoded[:40])
