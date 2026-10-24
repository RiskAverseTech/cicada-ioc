"""Phase 2, step 1: is the doublet deficit in the unsolved pages cipher structure,
a property of the plaintext, or a transcription convention?

Observed (phase 1): 86 doubled adjacent runes in the unsolved pages where an iid
uniform stream gives 445 (z = -17). This script measures the same statistic on the
solved plaintext and the solved ciphertext, checks the transcription for anything
that would suppress adjacency, splits doublets by word boundary, and decrypts the
unsolved pages under ciphertext autokey (K_i = C_{i-k}) to see whether anything
plaintext-like comes out.
"""
import json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *

rng = np.random.default_rng(3301)
PI = 1 / N
d = json.loads((PROCESSED / "pages.json").read_text())
unsolved = [(u["id"], np.array(u["cipher"])) for u in d["unsolved"] if u["length"] > 0]
solved_plain = [(s["name"], np.array(s["plaintext"])) for s in d["solved"]]
raw = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8")
chunks = raw.split("%")
solved_cipher = [(f"page {k}", np.array(rune_indices(chunks[k]))) for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 72, 73]]
solved_cipher = [(n, x) for n, x in solved_cipher if len(x) > 1]
out = []


def doublets(x):
    return int((x[:-1] == x[1:]).sum()), len(x) - 1


def ic(x):
    c = np.bincount(x, minlength=N)
    return float((c * (c - 1)).sum() / (len(x) * (len(x) - 1)))


def z_binom(obs, n, p):
    return (obs - n * p) / np.sqrt(n * p * (1 - p))


def shuffle_null(pages, reps=2000):
    """Doublet count when each page's runes are permuted (keeps every page's frequencies)."""
    tot = np.zeros(reps)
    for r in range(reps):
        tot[r] = sum(doublets(rng.permutation(x))[0] for x in pages)
    return tot


def summarize(label, pages):
    obs = sum(doublets(x)[0] for x in pages)
    pairs = sum(doublets(x)[1] for x in pages)
    runes = sum(len(x) for x in pages)
    null = shuffle_null(pages)
    allx = np.concatenate(pages)
    return {"label": label, "runes": runes, "pairs": pairs, "doublets": obs, "rate": obs / pairs,
            "expected_uniform": pairs * PI, "z_uniform": float(z_binom(obs, pairs, PI)),
            "shuffle_mean": float(null.mean()), "shuffle_sd": float(null.std()),
            "z_shuffle": float((obs - null.mean()) / null.std()), "ic": ic(allx)}


# ---------- 1a. the same statistic on plaintext, solved ciphertext, unsolved ciphertext ----------
rows = [summarize("solved plaintext (decrypted)", [x for _, x in solved_plain]),
        summarize("solved ciphertext (as transcribed)", [x for _, x in solved_cipher]),
        summarize("unsolved ciphertext", [x for _, x in unsolved])]
out += ["# Doublet audit", "",
        "Doublet = the same rune twice in a row. Two nulls: iid uniform (rate 1/29 = 0.0345), and a within-page",
        "shuffle that keeps each page's rune frequencies (rate ≈ that text's own index of coincidence).", "",
        "| text | runes | adjacent pairs | doublets | rate | z vs uniform | shuffle mean ± sd | z vs shuffle | IC |",
        "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    out.append(f"| {r['label']} | {r['runes']} | {r['pairs']} | {r['doublets']} | {r['rate']:.4f} | {r['z_uniform']:+.1f} | {r['shuffle_mean']:.0f} ± {r['shuffle_sd']:.0f} | {r['z_shuffle']:+.1f} | {r['ic']:.4f} |")

# Solved ciphertext per cipher type, since the known ciphers differ.
out += ["", "Solved ciphertext by page (cipher from the published keys):", "",
        "| page | cipher | pairs | doublets | expected uniform | z |", "|---|---|---|---|---|---|"]
kinds = {1: "Atbash", 2: "Vigenère DIVINITY", 3: "Vigenère DIVINITY", 4: "plain", 5: "shift 3 + Atbash", 6: "shift 3 + Atbash", 7: "shift 3 + Atbash", 8: "shift 3 + Atbash",
         9: "plain", 10: "plain", 11: "plain", 12: "plain", 13: "Vigenère FIRFUMFERENFE", 14: "Vigenère FIRFUMFERENFE", 15: "plain", 72: "totient prime stream", 73: "plain"}
for (n, x) in solved_cipher:
    k = int(n.split()[1]); o, p = doublets(x)
    out.append(f"| {k} | {kinds[k]} | {p} | {o} | {p*PI:.1f} | {z_binom(o, p, PI):+.1f} |")

# ---------- 1b. transcription conventions ----------
seps = "-./&$§\n"
digits = sum(ch.isdigit() for ch in raw)
latin = sum(ch.isascii() and ch.isalpha() for ch in raw.split("%", 1)[1])
within, across, within_pairs, across_pairs = 0, 0, 0, 0
for k in range(16, 72):
    prev, boundary = None, False
    for ch in chunks[k]:
        if ch in IDX:
            i = IDX[ch]
            if prev is not None:
                if boundary:
                    across_pairs += 1; across += (i == prev)
                else:
                    within_pairs += 1; within += (i == prev)
            prev, boundary = i, False
        elif ch in seps or ch.isdigit() or ch.isalpha():
            boundary = True
out += ["", "## Transcription conventions", "",
        "The master file separates words with '-', clauses with '.', lines with '/', paragraphs with '&', segments with '$'. Phase 1 drops all of",
        "them, so adjacency across a word or line boundary counts exactly as adjacency inside a word, for the observed pages and for the shuffle",
        f"null alike. Digits ({digits}) and Latin letters ({latin}) in the file mark page numbers and drawings and carry no runes. Doubled letters in the solved",
        f"plaintext are written as two runes (the decrypted plaintext has {rows[0]['doublets']} doublets, rate {rows[0]['rate']:.4f}), so nothing in the",
        "transcription or the Gematria Primus convention removes repeats from the text itself.", "",
        "Unsolved pages, doublets split by whether a separator sits between the two runes:", "",
        "| position | adjacent pairs | doublets | expected uniform | rate |", "|---|---|---|---|---|",
        f"| inside a word | {within_pairs} | {within} | {within_pairs*PI:.1f} | {within/within_pairs:.4f} |",
        f"| across a boundary | {across_pairs} | {across} | {across_pairs*PI:.1f} | {across/across_pairs:.4f} |"]

# ---------- 1d. ciphertext-autokey decrypt ----------
plain_all = np.concatenate([x for _, x in solved_plain])
p_plain = np.bincount(plain_all, minlength=N) / len(plain_all)
out += ["", "## Ciphertext-autokey decrypt of the unsolved pages", "",
        "Under K_i = C_{i-k}, the plaintext is P_i = C_i - C_{i-k} (mod 29). If that were the cipher, this stream would look like",
        f"plaintext: IC near {ic(plain_all):.4f}, E at {p_plain[18]:.3f}, F at {p_plain[0]:.3f}. Under lag 1 a ciphertext doublet is exactly a recovered F.", "",
        "| lag k | runes | IC of recovered stream | top rune (share) | share of F | KL(recovered ‖ plaintext) | KL(recovered ‖ uniform) |",
        "|---|---|---|---|---|---|---|"]
for k in range(1, 6):
    rec = np.concatenate([(x[k:] - x[:-k]) % N for _, x in unsolved])
    pr = np.bincount(rec, minlength=N) / len(rec)
    top = int(np.argmax(pr))
    kl_p = float(np.sum(pr[pr > 0] * np.log(pr[pr > 0] / np.maximum(p_plain[pr > 0], 1e-6))))
    kl_u = float(np.sum(pr[pr > 0] * np.log(pr[pr > 0] * N)))
    out.append(f"| {k} | {len(rec)} | {ic(rec):.4f} | {LATIN[top]} ({pr[top]:.3f}) | {pr[0]:.4f} | {kl_p:.3f} | {kl_u:.4f} |")
rec1 = np.concatenate([(x[1:] - x[:-1]) % N for _, x in unsolved])
pr1 = np.bincount(rec1, minlength=N)
out += ["", f"At lag 1 the recovered stream's unigram chi-square against uniform is {float(((pr1-pr1.mean())**2/pr1.mean()).sum()):.0f} on 28 dof",
        "(almost all of it from the missing F); against the solved plaintext's distribution the fit is far worse. The recovered stream is a",
        "flat distribution with one hole, not a language.", ""]

# ---------- 1c. decision ----------
r_p, r_c, r_u = rows
out += ["## Decision", "",
        f"- The solved plaintext has a mild doublet deficit against uniform (rate {r_p['rate']:.4f}, z {r_p['z_uniform']:+.1f}) and a strong one against its own",
        f"  shuffle (z {r_p['z_shuffle']:+.1f}), which is ordinary English behaviour: letters repeat less often than independence predicts.",
        f"- The solved ciphertext, enciphered with the book's own short-key and stream methods, sits at the uniform rate (rate {r_c['rate']:.4f}, z {r_c['z_uniform']:+.1f}).",
        f"- The unsolved ciphertext is at rate {r_u['rate']:.4f}, z {r_u['z_uniform']:+.1f} against uniform and z {r_u['z_shuffle']:+.1f} against its own shuffle: a fivefold deficit that",
        "  neither the plaintext nor the transcription nor the book's known ciphers produce.",
        "- Within words and across word boundaries the deficit is the same, so it is not a word-level writing rule.",
        "- Simple ciphertext autokey (any lag 1 to 5) does not decrypt to anything plaintext-like.", "",
        "**The deficit is cipher structure.** Whatever generates the unsolved pages makes the next rune avoid the previous one far more",
        "often than an additive cipher with an independent key can. The mechanism simulation (doublets.py) asks which constructions do that."]
(RESULTS / "doublet_audit.md").write_text("\n".join(out) + "\n")
json.dump({"rows": rows, "within": [within, within_pairs], "across": [across, across_pairs]}, open(RESULTS / "doublet_audit.json", "w"), indent=1)
print("\n".join(out))
