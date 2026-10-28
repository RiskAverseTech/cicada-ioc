"""Shared 5-gram rescoring for the phase lanes' short-page mode (2026-10-28, README §37).
z5(C, decode_fn, decs): decode_fn(Ks) -> decoded (m, n) arrays for keystreams Ks; the null is the
5-gram score of 400 random keystreams' decodes through the same decoder; returns z_5 per decode."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N
from score import S_MAX
import ngram

_T5 = None
SHORT_PAGES = ["LP2-49", "LP2-55", "LP2-51", "LP2-32", "LP2-22", "LP2-14", "LP2-15", "LP2-53", "LP2-06"]
Z_UNI_R, Z_5 = 3.5, 6.0


def tables():
    global _T5
    if _T5 is None: _T5 = ngram.load_dense()
    return _T5


def z5(C, decode_fn, decs, rng, reps=400):
    Kr = rng.integers(0, N, size=(reps, len(C) + S_MAX + 2)); null = ngram.score_batch(decode_fn(Kr), tables())
    s = ngram.score_batch(np.asarray(decs), tables()); return (s - null.mean()) / null.std()


def write_short(tag, title, rows):
    import json
    from lp import RESULTS
    ctr = [r for r in rows if r["kind"] == "control"]; pg = [r for r in rows if r["kind"] == "page"]
    cands = [r for r in pg if r["zu"] >= Z_UNI_R and r["z5"] >= Z_5]
    out = [f"# {title}: 5-gram rescoring (README §37)", "", f"Rule: z_uni >= {Z_UNI_R} and z_5 >= {Z_5} (5-gram over 400 random keystreams through the same decoder) and readable; controls planted at short lengths.", "",
           "## Controls", "", "| n | set | key | F | z_uni | z_5 | rank | pass |", "|---|---|---|---|---|---|---|---|"]
    for c in ctr: out.append(f"| {c['n']} | {c['sign']} | {c['key']} | {c['F']} | {c['zu']:.1f} | {c['z5']:.1f} | {c['rank']} | {'yes' if c['passed'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['passed'] for c in ctr)} of {len(ctr)}.", "", "## Best cell per page", "", "| page | set | F | family | key | z_uni | z_5 | transliteration |", "|---|---|---|---|---|---|---|---|"]
    for p in sorted({r["page"] for r in pg}):
        b = max((r for r in pg if r["page"] == p), key=lambda r: r["zu"]); out.append(f"| {p} | {b['sign']} | {b['F']} | {b['fam']} | {b['key']} | {b['zu']:.2f} | {b['z5']:.1f} | {b['translit'][:50]} |")
    out += ["", "## Candidates", ""] + ([f"- {c}" for c in cands] or ["None."]) + ["", f"Largest z_uni {max((r['zu'] for r in pg), default=0):.2f}; largest z_5 {max((r['z5'] for r in pg), default=0):.2f}.", ""]
    (RESULTS / f"{tag}_short.md").write_text("\n".join(out) + "\n"); json.dump(rows, open(RESULTS / f"{tag}_short.json", "w"), indent=1)
    print("\n".join(out[-4:]))
