"""This record's lanes as interchange rows, in the row format proposed on Dukotah/cicada3301's cross-ledger page
(docs/CROSS-LEDGER.md, "Proposed interchange row", as read 2026-11-25), so another ledger can merge or cite them
without reading 84 sections.  Generated from ledger.json; nothing is added that the ledger does not carry.

    .venv/bin/python -I src/export_interchange.py            write results/interchange_rows.json
    .venv/bin/python -I src/export_interchange.py --dates    rebuild results/section_dates.json from the git history first

Fields this record does not hold per lane are null, not guessed: `threshold` and `null` are stated in each section and,
from §49 on, in results/*_registration.md; `threshold_fixed_in_advance` is true for every lane with a registration file and
is left null here because ledger.json does not record which lanes those are.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from toc import headings

REPO = "https://github.com/RiskAverseTech/cicada-ioc"
DATES = ROOT / "results" / "section_dates.json"
OUT = ROOT / "results" / "interchange_rows.json"
MEASURED = ("measured", "genuine", "boundary-blind", "86 vs 445", "deficit at lag 1 only", "0 disagreements", "facts stand", "the two laws stand", "the nulls stand")
INCONCLUSIVE = ("no power", "below power")


def status(verdict):
    if verdict.startswith("null") or verdict.startswith("no match"): return "negative"
    if verdict.startswith(INCONCLUSIVE): return "inconclusive"
    if verdict.startswith(MEASURED): return "measured"
    raise ValueError("unmapped verdict: " + verdict[:60])      # a new verdict form must be mapped by hand, not defaulted


def section_dates():
    """{section number: date of the commit that first carried its heading}, from git; slow, so cached in results/."""
    md = (ROOT / "README.md").read_text(encoding="utf-8"); out = {}
    for n in sorted({int(m) for m in re.findall(r"(?m)^## (\d+)\.", md)}):
        r = subprocess.run(["git", "log", "--format=%ad", "--date=short", f"-S## {n}. ", "--", "README.md"], cwd=ROOT, capture_output=True, text=True)
        ds = r.stdout.split(); out[str(n)] = ds[-1] if ds else None
    return out


def rows(ledger, dates, md):
    sec = {}
    for level, text, anchor in headings(md):
        m = re.match(r"(\d+)\.", text)
        if level == 2 and m: sec[int(m.group(1))] = (anchor, re.findall(r"`([^`]+)`", text))
    out, seen = [], {}
    for l in ledger["lanes"]:
        n = int(re.search(r"\d+", l["section"]).group()); anchor, files = sec[n]
        slug = "-".join(re.findall(r"[a-z0-9]+", l["lane"].lower())[:4]); rid = f"RAT-S{n:02d}-{slug}"
        seen[rid] = seen.get(rid, 0) + 1; rid += f"-{seen[rid]}" if seen[rid] > 1 else ""
        t = l["tests"]; ctrl = (l["controls"] or "").strip()
        out.append(dict(
            id=rid, section=l["section"], hypothesis=l["lane"], status=status(l["verdict"]), result=l["verdict"], date=dates.get(str(n)),
            threshold=None, threshold_fixed_in_advance=None, null=None,
            positive_control="none" if ctrl in ("", "—") else "see control_detail", control_detail=None if ctrl in ("", "—") else ctrl,
            coverage=(f"{t:,} decoder tests" if isinstance(t, int) and t > 0 else None), not_covered=l["coverage_limit"] or None,
            evidence=f"{REPO}/blob/main/README.md#{anchor}", reproduce=("files named in the section heading: " + ", ".join(files)) if files else None))
    return out


def main():
    if "--dates" in sys.argv or not DATES.exists():
        DATES.write_text(json.dumps(section_dates(), indent=1) + "\n"); print(f"wrote {DATES.relative_to(ROOT)}")
    dates = json.loads(DATES.read_text()); ledger = json.loads((ROOT / "ledger.json").read_text(encoding="utf-8")); md = (ROOT / "README.md").read_text(encoding="utf-8")
    r = rows(ledger, dates, md)
    doc = dict(generated_by="src/export_interchange.py", source="ledger.json (written by src/status.py)", repository=REPO, release="v1.0-pause-2026-11-01",
               format="Dukotah/cicada3301 docs/CROSS-LEDGER.md, 'Proposed interchange row', as read 2026-11-25; `section` and `result` are additions",
               note="One row per lane of this record. status: negative = no accepted decoding within the tested configurations at the stated detection limits; measured = a measurement, not a decode; inconclusive = the instrument had no power. "
                    "Null fields are not carried per lane by ledger.json; read them in the linked section. date = the commit date on which the section first appeared.",
               counts={s: sum(1 for x in r if x["status"] == s) for s in ("negative", "measured", "inconclusive")}, rows=r)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"); print(f"wrote {OUT.relative_to(ROOT)}: {len(r)} rows, {doc['counts']}")


if __name__ == "__main__":
    main()
