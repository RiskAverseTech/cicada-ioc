"""Shared helpers: Gematria Primus alphabet, page parsing, known-key decryption.

Alphabet order follows the Gematria Primus table (index 0..28 = F U TH O R C G W H N
I J EO P X S T B E M L NG OE D A AE Y IA EA), the order every community tool uses.
"""
from __future__ import annotations
import re
from pathlib import Path

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
LATIN = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
         "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"]
# Multi-letter alternates used when mapping English back onto runes.
LATIN_ALT = {"V": 1, "K": 5, "Z": 15, "ING": 21, "IO": 27}
IDX = {r: i for i, r in enumerate(RUNES)}
N = 29
assert len(RUNES) == N and len(LATIN) == N

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"


def rune_indices(text: str) -> list[int]:
    """Drop everything that is not one of the 29 runes; return 0..28 indices."""
    return [IDX[ch] for ch in text if ch in IDX]


def to_latin(idx) -> str:
    return "".join(LATIN[i] for i in idx)


def load_master_pages(path: Path | None = None) -> list[list[int]]:
    """Return the 74 pages of the rtkd master transcription as index lists (page 1 = item 0).

    The file begins with a short delimiter legend; pages are separated by '%'.
    Non-rune characters (word '-', clause '.', line '/', paragraph '&', segment '$',
    chapter '§', digits and Latin letters used for drawings/numbers) are dropped.
    """
    path = path or RAW / "iddqd__liber-primus__transcription--master.txt"
    raw = path.read_text(encoding="utf-8")
    chunks = raw.split("%")
    pages = [rune_indices(c) for c in chunks]
    # The legend chunk before page 1 holds no runes; a trailing empty chunk may exist.
    pages = [p for p in pages if len(p) > 0]
    return pages


def primes(n: int) -> list[int]:
    out, k = [], 2
    while len(out) < n:
        if all(k % p for p in out if p * p <= k):
            out.append(k)
        k += 1
    return out


def atbash(c):
    return [(N - 1 - x) % N for x in c]


def shift(c, s):
    return [(x - s) % N for x in c]


def vigenere(c, key, skip_f=True):
    """Subtract a repeating key; a ciphertext ᚠ (index 0) is a literal plaintext F
    and does not consume a key symbol (the rule documented for the solved pages)."""
    out, j = [], 0
    for x in c:
        if skip_f and x == 0:
            out.append(0)
            continue
        out.append((x - key[j % len(key)]) % N)
        j += 1
    return out


def totient_stream(c, skip_f=True):
    """Subtract phi(p_n) = p_n - 1 for the n-th prime, with the same F-skip rule."""
    ps = primes(len(c) + 10)
    out, j = [], 0
    for x in c:
        if skip_f and x == 0:
            out.append(0)
            continue
        out.append((x - (ps[j] - 1)) % N)
        j += 1
    return out


def english_to_runes(text: str) -> list[int]:
    """Map English (translation file) onto Gematria Primus indices, word by word so
    digraphs never straddle a word boundary.  Longest match first: ING, then
    TH/EO/NG/OE/AE/IA/IO/EA, then single letters.  QU -> C W is the convention
    the book itself uses (e.g. 'CWESTION'); V -> U, K -> C, Z -> S."""
    table = {**{l: i for i, l in enumerate(LATIN)}, **LATIN_ALT}
    out = []
    for word in re.sub(r"[^A-Z ]", "", text.upper().replace("'", "")).split():
        word = word.replace("QU", "CW").replace("Q", "C")
        i = 0
        while i < len(word):
            for L in (3, 2, 1):
                seg = word[i:i + L]
                if seg in table:
                    out.append(table[seg])
                    i += L
                    break
            else:
                i += 1
    return out
