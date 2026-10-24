"""Phase 2, step 2: which cipher constructions reproduce the unsolved pages' signature?

Signature (phase 1 + doublet_audit): 86 doublets in 12,901 adjacent pairs (uniform gives
445), ciphertext IC 0.0345 and flat unigrams (chi2 26 on 28 dof), lag-1 difference classes
other than 0 nearly uniform (classes 20, 27, 16, 19 at +2.5 to +3.1 sigma).

Each construction enciphers resampled solved-page plaintext cut into the 55 real page
lengths, 200 replicates, and is scored on the same statistics as the real pages.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import *

rng = np.random.default_rng(3301)
PI = 1 / N
d = json.loads((PROCESSED / "pages.json").read_text())
LENS = [u["length"] for u in d["unsolved"] if u["length"] > 0]
plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
P_FREQ = np.bincount(plain, minlength=N) / len(plain)
PRIMES = np.array(primes(400))
REPS = 200


def sample_pages():
    """Plaintext cut into the real page lengths, each from a random offset (wraparound)."""
    out = []
    for L in LENS:
        o = rng.integers(0, len(plain))
        out.append(np.take(plain, np.arange(o, o + L), mode="wrap"))
    return out


def stats(pages):
    allc = np.concatenate(pages)
    dbl = sum(int((x[:-1] == x[1:]).sum()) for x in pages)
    lag = np.concatenate([(x[:-1] - x[1:]) % N for x in pages])
    cls = np.bincount(lag, minlength=N)
    nz = cls[1:]
    chi_nz = float(((nz - nz.mean()) ** 2 / nz.mean()).sum())          # non-uniformity among non-zero classes
    uni = np.bincount(allc, minlength=N)
    chi_u = float(((uni - uni.mean()) ** 2 / uni.mean()).sum())         # unigram flatness
    c = np.bincount(allc, minlength=N)
    ic = float((c * (c - 1)).sum() / (len(allc) * (len(allc) - 1)))
    return dbl, chi_nz, chi_u, ic


# ---------- constructions: P (one page) -> C ----------
def uniform(P):
    return (P + rng.integers(0, N, len(P))) % N

def plain_autokey(k, seed_word=None):
    def f(P):
        seed = rng.integers(0, N, k) if seed_word is None else np.array(seed_word[:k])
        K = np.concatenate([seed, P[:-k]]) if k < len(P) else seed[:len(P)]
        return (P + K) % N
    return f

def cipher_autokey(k):
    def f(P):
        C = np.zeros(len(P), dtype=int)
        seed = rng.integers(0, N, k)
        for i in range(len(P)):
            C[i] = (P[i] + (seed[i] if i < k else C[i - k])) % N
        return C
    return f

def cipher_autokey_offset(c):
    def f(P):
        C = np.zeros(len(P), dtype=int); prev = rng.integers(0, N)
        for i in range(len(P)):
            C[i] = (P[i] + prev + c) % N; prev = C[i]
        return C
    return f

def running_key(P):
    o = rng.integers(0, len(plain))
    return (P + np.take(plain, np.arange(o, o + len(P)), mode="wrap")) % N

def vigenere_norepeat(P, klen=8):
    key = rng.integers(0, N, klen); C = np.zeros(len(P), dtype=int); j = 0
    for i in range(len(P)):
        C[i] = (P[i] + key[j % klen]) % N
        if i > 0 and C[i] == C[i - 1]:
            j += 1; C[i] = (P[i] + key[j % klen]) % N     # step the key once
        j += 1
    return C

def anti_doublet(prob):
    def f(P):
        C = (P + rng.integers(0, N, len(P))) % N
        for i in range(1, len(P)):
            if C[i] == C[i - 1] and rng.random() < prob:
                C[i] = (C[i] + 1) % N
        return C
    return f

def hand_pad(P):
    K = np.zeros(len(P), dtype=int); K[0] = rng.integers(0, N)
    for i in range(1, len(P)):
        K[i] = (K[i - 1] + rng.integers(1, N)) % N          # key never repeats a symbol
    return (P + K) % N

def book_vigenere(key):
    def f(P):
        C = np.zeros(len(P), dtype=int); j = 0
        for i in range(len(P)):
            if P[i] == 0:
                C[i] = 0; continue                            # plaintext F left unencrypted
            C[i] = (P[i] + key[j % len(key)]) % N; j += 1
        return C
    return f

def totient(P):
    C = np.zeros(len(P), dtype=int); j = 0
    for i in range(len(P)):
        if P[i] == 0:
            C[i] = 0; continue
        C[i] = (P[i] + PRIMES[j] - 1) % N; j += 1
    return C

def soft_reroll(prob):
    """Keystream re-rolled when it would repeat the previous rune, with probability prob."""
    def f(P):
        C = np.zeros(len(P), dtype=int); C[0] = (P[0] + rng.integers(0, N)) % N
        for i in range(1, len(P)):
            k = rng.integers(0, N)
            while (P[i] + k) % N == C[i - 1] and rng.random() < prob:
                k = rng.integers(0, N)
            C[i] = (P[i] + k) % N
        return C
    return f

def reroll_until_distinct(P):
    """Keystream chosen so the ciphertext never repeats the previous rune (hard rule)."""
    C = np.zeros(len(P), dtype=int); C[0] = (P[0] + rng.integers(0, N)) % N
    for i in range(1, len(P)):
        k = rng.integers(0, N)
        while (P[i] + k) % N == C[i - 1]:
            k = rng.integers(0, N)
        C[i] = (P[i] + k) % N
    return C

CONSTRUCTIONS = [
    ("independent uniform keystream (control)", uniform),
    ("running key from English (solved text, random offset)", running_key),
    ("hand pad: uniform key that never repeats a symbol", hand_pad),
    ("plaintext autokey, lag 1", plain_autokey(1)), ("plaintext autokey, lag 2", plain_autokey(2)),
    ("plaintext autokey, lag 5", plain_autokey(5)),
    ("ciphertext autokey, lag 1", cipher_autokey(1)), ("ciphertext autokey, lag 2", cipher_autokey(2)),
    ("ciphertext autokey, lag 5", cipher_autokey(5)),
    ("ciphertext autokey, lag 1, offset so doublet⇔EA", cipher_autokey_offset((-28) % N)),
    ("ciphertext autokey, lag 1, offset so doublet⇔EO (never)", cipher_autokey_offset((-12) % N)),
    ("Vigenère key 8, step key when a doublet would form", vigenere_norepeat),
    ("book Vigenère DIVINITY with F-skip", book_vigenere([23, 10, 1, 10, 9, 10, 16, 26])),
    ("book totient prime stream with F-skip", totient),
    ("uniform key + anti-doublet rule (always +1)", anti_doublet(1.0)),
    ("uniform key + anti-doublet rule (81% of the time)", anti_doublet(0.81)),
    ("keystream re-rolled until no doublet (hard rule)", reroll_until_distinct),
    ("keystream re-rolled when it would repeat, 81% of the time (soft rule)", soft_reroll(0.81)),
    ("keystream re-rolled when it would repeat, 70% of the time", soft_reroll(0.70)),
    ("keystream re-rolled when it would repeat, 90% of the time", soft_reroll(0.90)),
]

# observed
obs_pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
OBS = stats(obs_pages)
rows = []
for name, enc in CONSTRUCTIONS:
    S = np.array([stats([enc(P) for P in sample_pages()]) for _ in range(REPS)])
    m, s = S.mean(0), S.std(0) + 1e-9
    z = (np.array(OBS) - m) / s
    rows.append((name, m, s, z))

out = ["# Which constructions reproduce the signature?", "",
       f"Observed on the unsolved pages: doublets {OBS[0]}, non-zero lag-1 class chi² {OBS[1]:.0f} (27 dof), unigram chi² {OBS[2]:.0f} (28 dof), IC {OBS[3]:.4f}.",
       f"Each construction: {REPS} replicates of solved-page plaintext cut into the 55 real page lengths. z = (observed − construction mean) / construction sd;",
       "a construction is consistent with the pages when every |z| is small. Doublets is the discriminating column.", "",
       "| construction | doublets (mean ± sd) | z | lag-1 class chi² | z | unigram chi² | z | IC | z | verdict |",
       "|---|---|---|---|---|---|---|---|---|---|"]
for name, m, s, z in rows:
    ok = all(abs(v) < 3 for v in z)
    dbl_ok = abs(z[0]) < 3
    verdict = "**consistent on all four**" if ok else ("matches doublets, fails lag-1 structure" if dbl_ok and abs(z[1]) >= 3 else ("matches doublets, fails elsewhere" if dbl_ok else "ruled out"))
    out.append(f"| {name} | {m[0]:.0f} ± {s[0]:.0f} | {z[0]:+.1f} | {m[1]:.0f} | {z[1]:+.1f} | {m[2]:.0f} | {z[2]:+.1f} | {m[3]:.4f} | {z[3]:+.1f} | {verdict} |")
out += ["", "## Reading", "",
        "- Anything additive with a key independent of the text (uniform, running key, hand pad, the book's own Vigenère and totient streams) gives",
        "  doublets at the uniform rate: a doublet needs P_i − P_{i+1} ≡ K_{i+1} − K_i, and an independent key hits that one time in 29 whatever it does.",
        "- Autokeys tie the key to the text and change the doublet rate, but not downward enough (plaintext autokey raises it; ciphertext autokey makes a",
        "  doublet a plaintext F, about 1.6%) and they leave a non-flat lag-1 structure that the pages do not show.",
        "- A ciphertext-feedback rule with a chosen offset can hit any doublet rate, including the observed one, but then the lag-1 difference stream is",
        "  the plaintext shifted, with IC 0.06, and the pages' lag-1 stream is flat (IC 0.0353). Ruled out on that column.",
        "- What matches is a key that is otherwise random and is rejected, most of the time, exactly when it would repeat the previous rune: a soft",
        "  anti-repeat rule applied to about four doublets in five. A hard rule (never repeat) overshoots to zero doublets; the pages have 86.", ""]
(RESULTS / "doublets.md").write_text("\n".join(out) + "\n")
json.dump({"observed": OBS, "rows": [(n, m.tolist(), s.tolist(), z.tolist()) for n, m, s, z in rows]}, open(RESULTS / "doublets.json", "w"), indent=1)
print("\n".join(out))
