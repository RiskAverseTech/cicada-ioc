"""Regenerate the README table of contents with GitHub-compatible anchors.

GitHub builds a heading's anchor from the full heading text: lower-case,
drop every character that is not a letter, digit, space, hyphen or
underscore (back-ticks, parentheses, dots, colons, en dashes all go),
replace spaces with hyphens, and suffix -1, -2 ... for repeats.  The earlier
TOC dropped the trailing file list, so 33 of 38 links pointed nowhere.

Usage: python src/toc.py [--check]   (--check only reports broken links)
"""
import re
import sys
import unicodedata
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- toc:start -->", "<!-- toc:end -->"


def slug(text: str, seen: dict) -> str:
    t = text.strip().lower()
    out = []
    for ch in t:
        cat = unicodedata.category(ch)
        if ch == " ":
            out.append("-")
        elif ch in "-_" or cat[0] in "LN" or cat.startswith("M"):
            out.append(ch)
    s = "".join(out)
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"


def headings(md: str):
    """(level, text, anchor) for every ATX heading outside fenced code."""
    seen: dict = {}
    fence = False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            yield len(m.group(1)), m.group(2), slug(m.group(2), seen)


def short_title(text: str) -> str:
    """'24. Short-page lane: a secondary ... (`src/x.py`)' -> ('24', 'Short-page lane')."""
    text = re.sub(r"\s*\(`[^)]*\)\s*$", "", text)          # drop trailing file list
    m = re.match(r"^(\d+)\.\s+(.*)$", text)
    if not m:
        return "", text
    num, rest = m.group(1), m.group(2)
    rest = re.split(r":\s", rest, maxsplit=1)[0]
    rest = re.sub(r"\s*\((?!`)[^)]*\)\s*$", "", rest) if len(rest) > 60 else rest
    return num, rest.rstrip(" ,:;")


def build(md: str) -> str:
    items = []
    for level, text, anchor in headings(md):
        if level != 2:
            continue
        if text.startswith("Phase 1") or text in ("Reproduce",):
            continue
        num, title = short_title(text)
        if not num or int(num) < 4 or (int(num) < 6 and "Decision" in text or "For the debate" in text):
            continue
        items.append(f"[{num}]({'#' + anchor}) {title}")
    phase1 = next((a for l, t, a in headings(md) if t.startswith("Phase 1")), None)
    head = f"[Phase 1: key reuse](#{phase1}) · " if phase1 else ""
    return "**Sections.** " + head + " · ".join(items)


def main():
    md = README.read_text(encoding="utf-8")
    anchors = {a for _, _, a in headings(md)}
    links = sorted(set(re.findall(r"\]\(#([^)]+)\)", md)))
    broken = [l for l in links if l not in anchors]
    if "--check" in sys.argv:
        print(f"{len(links)} internal links, {len(broken)} broken")
        for b in broken:
            print("  ", b)
        sys.exit(1 if broken else 0)
    i, j = md.index(START) + len(START), md.index(END)
    new = md[:i] + "\n" + build(md) + "\n" + md[j:]
    README.write_text(new, encoding="utf-8")
    anchors = {a for _, _, a in headings(new)}
    links = sorted(set(re.findall(r"\]\(#([^)]+)\)", new)))
    broken = [l for l in links if l not in anchors]
    print(f"TOC rewritten: {len(links)} internal links, {len(broken)} broken")
    for b in broken:
        print("  ", b)


if __name__ == "__main__":
    main()
