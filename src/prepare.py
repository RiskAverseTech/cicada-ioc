"""Build data/processed/pages.json from the raw rtkd transcription.

Solved pages are decrypted with their published keys and checked rune-for-rune
against the rtkd English translation mapped back onto Gematria Primus.  The
Vigenere/totient pages use the book's rule that a plaintext F is written
unencrypted and consumes no key symbol; a ciphertext ᚠ is therefore ambiguous
(literal F, or an encrypted letter that happens to land on ᚠ) and is resolved
with the translation.  Any disagreement between decryption and translation is
printed, so the plaintext used for q is exactly what the published keys give.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import *

DIV = [23, 10, 1, 10, 9, 10, 16, 26]              # DIVINITY
FIRF = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]  # FIRFUMFERENFE


def load_chunks():
    raw = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8")
    return [rune_indices(c) for c in raw.split("%")]   # chunk k = book page k (k = 1..74)


def load_translation():
    txt = (RAW / "iddqd__liber-primus__translation.txt").read_text(encoding="utf-8")
    lines = {}
    for ln in txt.splitlines():
        m = re.match(r"^(\d+\.\d+\.\d+)\.(\d+)\s+(.*)$", ln)
        if m:
            lines.setdefault(m.group(1), []).append(m.group(3))
    return lines  # section "0.1.0" -> list of lines


def reference(trans, sections):
    text = " ".join(" ".join(trans[s]) for s in sections)
    return english_to_runes(text)


def decrypt_with_ref(cipher, key_at, ref):
    """key_at(j) gives the key symbol for the j-th *encrypted* rune.
    Literal-F positions are taken from the reference where cipher is ᚠ."""
    out, j = [], 0
    for i, x in enumerate(cipher):
        if x == 0 and i < len(ref) and ref[i] == 0:
            out.append(0)            # unencrypted plaintext F, key does not advance
            continue
        out.append((x - key_at(j)) % N)
        j += 1
    return out


def compare(name, dec, ref):
    ok = dec == ref
    print(f"{name}: {len(dec)} runes, ref {len(ref)} runes, {'MATCH' if ok else 'MISMATCH'}")
    if not ok:
        for i in range(max(len(dec), len(ref))):
            a = dec[i] if i < len(dec) else None
            b = ref[i] if i < len(ref) else None
            if a != b:
                print(f"   first diff at {i}: dec ...{to_latin(dec[max(0,i-10):i+15])}")
                print(f"                      ref ...{to_latin(ref[max(0,i-10):i+15])}")
                break
    return ok


def main():
    ch = load_chunks()
    tr = load_translation()
    P = primes(400)
    solved = []

    def add(name, pages, dec, sections):
        solved.append({"name": name, "book_pages": pages, "plaintext": dec,
                       "verified_against_translation": compare(name, dec, reference(tr, sections))})

    add("warning", [1], atbash(ch[1]), ["0.0.0"])
    c23 = ch[2] + ch[3]
    add("welcome+wisdom", [2, 3], decrypt_with_ref(c23, lambda j: DIV[j % 8], reference(tr, ["0.1.0", "0.1.1"])), ["0.1.0", "0.1.1"])
    add("some wisdom+know this", [4], ch[4], ["0.1.2", "0.1.3"])
    add("koan 1+instruction", [5, 6, 7, 8], [(2 - x) % N for x in ch[5] + ch[6] + ch[7] + ch[8]], ["0.2.0", "0.2.1"])
    add("loss of divinity", [9, 10, 11, 12], ch[9] + ch[10] + ch[11] + ch[12], ["0.3.0", "0.3.1", "0.3.2"])
    c1314 = ch[13] + ch[14]
    add("koan 2", [13, 14], decrypt_with_ref(c1314, lambda j: FIRF[j % 13], reference(tr, ["0.4.0"])), ["0.4.0"])
    add("instruction+know this", [15], ch[15], ["0.4.1", "0.4.2"])
    add("an end", [72], decrypt_with_ref(ch[72], lambda j: P[j] - 1, reference(tr, ["0.13.0"])), ["0.13.0"])
    add("parable", [73], ch[73], ["0.14.0"])

    unsolved = []
    for k in range(16, 72):
        unsolved.append({"id": f"LP2-{k-16:02d}", "book_page": k, "cipher": ch[k], "length": len(ch[k])})
    nonempty = [u for u in unsolved if u["length"] > 0]
    print(f"unsolved: {len(unsolved)} pages (LP2 00..55), {len(nonempty)} with runes, "
          f"{sum(u['length'] for u in unsolved)} runes total")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    (PROCESSED / "pages.json").write_text(json.dumps({"solved": solved, "unsolved": unsolved}))
    (PROCESSED / "solved_plaintext_latin.txt").write_text(
        "\n\n".join(f"# {s['name']} (book pages {s['book_pages']})\n{to_latin(s['plaintext'])}" for s in solved))
    print("plaintext runes total:", sum(len(s["plaintext"]) for s in solved))


if __name__ == "__main__":
    main()
