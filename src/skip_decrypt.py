"""Phase 3: the skip-on-repeat rule, as encryptor and vectorised decryptor.

Encryption: C_i = P_i + K_j. If that would equal C_{i-1}, the key symbol is skipped
(j += 1) and the next one is used; repeat while it would still repeat.  Optionally the
book's own rule as well: a plaintext F (index 0) is written unencrypted and consumes
no key symbol.

Decryption given a candidate keystream is deterministic: a skip happened at i exactly
when C_i - C_{i-1} == K_{j+1} - K_j (mod 29).  By chance that holds at about one
non-skip position in 29, so a wrong skip is assumed there; the scorer tolerates it.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import N


def encrypt(P, K, f_rule=False, rng=None, soft=1.0):
    C, j, prev = [], 0, None
    for p in P:
        if f_rule and p == 0:
            C.append(0); prev = 0; continue
        c = (p + K[j]) % N
        while prev is not None and c == prev and (rng is None or rng.random() < soft):
            j += 1; c = (p + K[j]) % N
        C.append(c); j += 1; prev = c
    return np.array(C)


def decrypt_many(C, Ks, f_rule=False):
    """C: (n,) ciphertext. Ks: (m, L) candidate keystreams with L >= n + margin.
    Returns (m, n) plaintext candidates, decrypted with the skip rule for all m at once."""
    C = np.asarray(C); m, L = Ks.shape; n = len(C)
    P = np.zeros((m, n), dtype=np.int16)
    j = np.zeros(m, dtype=np.int64)
    rows = np.arange(m)
    for i in range(n):
        c = C[i]
        if f_rule and c == 0:
            P[:, i] = 0; continue               # literal F, no key consumed
        if i > 0:
            # a skip occurred where C_i - C_{i-1} == K_{j+1} - K_j; allow a double skip too
            for _ in range(2):
                jj = np.minimum(j + 1, L - 1)
                skip = ((c - C[i - 1]) - (Ks[rows, jj] - Ks[rows, j])) % N == 0
                if not skip.any(): break
                j = j + skip
        j = np.minimum(j, L - 1)
        P[:, i] = (c - Ks[rows, j]) % N
        j += 1
    return P


if __name__ == "__main__":
    import json
    from lp import PROCESSED
    rng = np.random.default_rng(3301)
    d = json.loads((PROCESSED / "pages.json").read_text())
    plain = np.concatenate([np.array(s["plaintext"]) for s in d["solved"]])
    P = plain[:240]
    ok = 0; tries = 0
    for f_rule in (False, True):
        for trial in range(50):
            K = rng.integers(0, N, 400)
            C = encrypt(P, K, f_rule=f_rule)
            rec = decrypt_many(C, K[None, :], f_rule=f_rule)[0]
            tries += 1; ok += int((rec == P).mean() > 0.95)
            if trial == 0:
                print(f"f_rule={f_rule}: ciphertext length {len(C)}, exact-match fraction {(rec == P).mean():.3f}, doublets in C: {(C[1:]==C[:-1]).sum()}")
    print(f"recovery >95% in {ok}/{tries} random-key trials (the few wrong runes are chance skip-condition hits)")
