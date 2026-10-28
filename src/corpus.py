"""Build the external running-key corpus (2026-10-27): the texts Cicada demonstrably pointed at,
transliterated into the 29-rune Gematria Primus, with provenance.  Raw files live in
data/corpus/raw/ (fetched by hand, URLs and SHA-256 below); this script never downloads.
Output: data/corpus/corpus.json  {name: {runes: [...], runes_nodigraph: [...], source, sha256, words}}
Transliteration V1 = lp.english_to_runes (longest match first: ING, TH/EO/NG/OE/AE/IA/IO/EA, QU->CW,
V->U, K->C, Z->S, word by word).  V2 ("nodigraph") maps letter by letter with the same folds and no
digraphs, the convention a solver would use if they transliterated without the book's ligatures.
Gibson's Agrippa is under copyright: its raw file and rune stream stay out of git (data/corpus/.gitignore);
only its hash is recorded.
Usage: .venv/bin/python -I src/corpus.py
"""
import hashlib, html, json, os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import english_to_runes, LATIN, LATIN_ALT

RAW = Path(__file__).resolve().parent.parent / "data" / "corpus" / "raw"
OUT = RAW.parent / "corpus.json"


def strip_html(h):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>|</p>|</div>|</h\d>", "\n", t)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def gutenberg_body(t):
    s = re.search(r"\*\*\* ?START OF TH[EI]S? PROJECT GUTENBERG EBOOK.*?\*\*\*", t)
    e = re.search(r"\*\*\* ?END OF TH[EI]S? PROJECT GUTENBERG EBOOK", t)
    return t[(s.end() if s else 0):(e.start() if e else len(t))]


def between(t, start_heading, end_heading, occurrence=None):
    """Text from an occurrence of start_heading to the next end_heading after it.  With occurrence=None
    the occurrence giving the longest span is used (a table of contents lists the heading too, and an
    index or note may repeat it later)."""
    starts = [m.start() for m in re.finditer(start_heading, t)]
    if not starts: raise ValueError(f"heading not found: {start_heading}")
    spans = []
    for s in (starts if occurrence is None else [starts[occurrence]]):
        e = re.search(end_heading, t[s + len(start_heading):])
        spans.append(t[s:(s + len(start_heading) + e.start()) if e else len(t)])
    return max(spans, key=len)


def nodigraph(text):
    table = {l: i for i, l in enumerate(LATIN) if len(l) == 1}; table.update({k: v for k, v in LATIN_ALT.items() if len(k) == 1})
    out = []
    for ch in re.sub(r"[^A-Z]", "", text.upper().replace("QU", "CW").replace("Q", "C")):
        if ch in table: out.append(table[ch])
    return out


def wiki_text(path):
    d = json.loads(Path(path).read_text()); return strip_html(d["parse"]["text"])


TEXTS = {
    # name: (loader, source, public_domain)
    "liber_al": (lambda: wiki_text(RAW / "liber_al_wikisource.json"),
                 "Crowley, Liber AL vel Legis (1909); en.wikisource.org/wiki/Liber_AL_vel_Legis, rendered page", True),
    "blake_mhh": (lambda: wiki_text(RAW / "blake_mhh_wikisource.json"),
                  "Blake, The Marriage of Heaven and Hell (1793); en.wikisource.org, rendered page", True),
    "rune_poem": (lambda: wiki_text(RAW / "rune_poem_wikisource.json"),
                  "The Anglo-Saxon Rune Poem, Dickins 1915 edition (Old English text and translation); en.wikisource.org", True),
    "self_reliance": (lambda: between(gutenberg_body((RAW / "emerson_essays1_pg2944.txt").read_text(errors="ignore")), r"SELF-RELIANCE", r"COMPENSATION"),
                      "Emerson, Self-Reliance, from Essays: First Series, Project Gutenberg #2944 (gutenberg.pglaf.org)", True),
    "emerson_essays1": (lambda: gutenberg_body((RAW / "emerson_essays1_pg2944.txt").read_text(errors="ignore")),
                        "Emerson, Essays: First Series, Project Gutenberg #2944", True),
    "lady_fountain_guest": (lambda: between(gutenberg_body((RAW / "mabinogion_guest_pg5160.txt").read_text(errors="ignore")), r"THE LADY OF THE FOUNTAIN", r"PEREDUR THE SON OF EVRAWC"),
                            "The Lady of the Fountain, Guest's Mabinogion, Project Gutenberg #5160", True),
    "mabinogion_guest": (lambda: gutenberg_body((RAW / "mabinogion_guest_pg5160.txt").read_text(errors="ignore")),
                         "The Mabinogion, Guest translation, Project Gutenberg #5160", True),
    "lady_fountain_bulfinch": (lambda: between(gutenberg_body((RAW / "bulfinch_age_of_chivalry_pg4926.txt").read_text(errors="ignore")), r"THE LADY OF THE FOUNTAIN", r"GERAINT,? THE SON OF ERBIN|PEREDUR|KILWICH|TALIESIN|PWYLL|BRANWEN"),
                               "Bulfinch, The Lady of the Fountain, from The Age of Chivalry, Project Gutenberg #4926 (the 2012 book-cipher text)", True),
    "cypherpunk_manifesto": (lambda: strip_html((RAW / "cypherpunk_manifesto.html").read_text(errors="ignore")),
                             "Eric Hughes, A Cypherpunk's Manifesto (1993); activism.net/cypherpunk/manifesto.html", True),
    "kybalion": (lambda: gutenberg_body((RAW / "kybalion_pg14209.txt").read_text(errors="ignore")),
                 "The Kybalion (1908), Project Gutenberg #14209", True),
    "king_in_yellow": (lambda: gutenberg_body((RAW / "king_in_yellow_pg8492.txt").read_text(errors="ignore")),
                       "Chambers, The King in Yellow (1895), Project Gutenberg #8492", True),
    "agrippa_gibson": (lambda: (RAW / "agrippa_gibson_diskimage.txt").read_text(errors="ignore"),
                       "Gibson, Agrippa (A Book of the Dead) (1992), text extracted from the disk image, agrippa.english.ucsb.edu (freek); COPYRIGHTED, raw file and rune stream kept out of git", False),
}

PILGRIM = {
    "bunyan_pilgrims_progress": (lambda: gutenberg_body((RAW / "bunyan_pilgrims_progress_pg131.txt").read_text(errors="ignore")),
                                 "Bunyan, The Pilgrim's Progress (1678), Project Gutenberg #131 (gutenberg.pglaf.org)", True),
    "bunyan_head": (lambda: gutenberg_body((RAW / "bunyan_pilgrims_progress_pg131.txt").read_text(errors="ignore"))[:72000],
                    "Bunyan, The Pilgrim's Progress, the first 55,000 runes, for the exact every-offset lane", True),
    "chaucer_canterbury": (lambda: gutenberg_body((RAW / "chaucer_canterbury_pg2383.txt").read_text(errors="ignore")),
                           "Chaucer, The Canterbury Tales (Middle English), Project Gutenberg #2383; sentence-start lane only", True),
}
if os.environ.get("CORPUS_SET") == "pilgrim":
    TEXTS = PILGRIM; OUT = RAW.parent / "corpus_pilgrim.json"

if __name__ == "__main__":
    corpus, lines = {}, ["| text | words | runes (V1) | runes (V2) | sha256 of raw file | source |", "|---|---|---|---|---|---|"]
    for name, (loader, source, pd) in TEXTS.items():
        try:
            text = loader()
        except Exception as e:
            print(f"  {name}: SKIPPED ({e})"); continue
        raw_file = [p for p in RAW.iterdir() if p.is_file() and name.split("_")[0] in p.name.lower()]
        sha = hashlib.sha256(sorted(raw_file)[0].read_bytes()).hexdigest()[:16] if raw_file else "?"
        v1, v2 = english_to_runes(text), nodigraph(text)
        # sentence starts (V1 rune index where each sentence begins): the offsets a human would choose
        starts, acc = [], 0
        for sent in re.split(r"(?<=[.!?])\s+", text):
            k = len(english_to_runes(sent))
            if k: starts.append(acc); acc += k
        starts = [x for x in starts if x < len(v1)]      # per-sentence lengths can overrun the whole-text stream by a few runes
        corpus[name] = dict(runes=v1, runes_nodigraph=v2, sentence_starts=starts, source=source, sha256=sha, words=len(text.split()), public_domain=pd)
        lines.append(f"| {name} | {len(text.split()):,} | {len(v1):,} | {len(v2):,} | {sha} | {source} |")
        print(f"  {name}: {len(text.split()):,} words -> {len(v1):,} runes (V1), {len(v2):,} (V2); first: {text.strip()[:70]!r}")
    OUT.write_text(json.dumps(corpus))
    (RAW.parent / ("CORPUS_pilgrim.md" if os.environ.get("CORPUS_SET") == "pilgrim" else "CORPUS.md")).write_text("# External running-key corpus\n\nBuilt by `src/corpus.py` from the raw files in `data/corpus/raw/` (hand-fetched 2026-10-27). "
                                          "V1 = book digraph transliteration, V2 = letter by letter.\n\n" + "\n".join(lines) + "\n")
    print("wrote", OUT, "and CORPUS.md")
