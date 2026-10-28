# Plant-and-recover benchmark

`plants.json`: 25 planted ciphertexts (five page lengths from 66 to 262 runes, five key families, all three sign conventions and both F variants) made from solved-page English under the soft anti-repeat rule this repository's analyses identify (re-draw with probability 0.81 when the output would repeat the previous rune). Each record carries the ciphertext, the true plaintext and the key stream.

Two uses. **Decoder check:** given ciphertext and key stream, a skip-aware decoder should recover the plaintext (this repository's `score.decode` recovers 89–100 % of positions, median 100 %). **Sweep check:** given only the ciphertext and the family, a sweep should rank the true key first and clear its own detection bar; the share that does so, by length, is the sweep's power (README §23 and §27 report ours).

Run this repository's decoder on them:

    .venv/bin/python -I - <<'EOF'
    import json, sys; sys.path.insert(0, "src"); import numpy as np
    from score import decode, english_model
    lu, _, _ = english_model(); b = json.load(open("benchmarks/plants.json"))
    for p in b["plants"]:
        C, P, K = (np.array(p[k]) for k in ("ciphertext", "plaintext", "key_stream"))
        Kd = (-K) % 29 if p["sign"] == "add" else K
        dec = decode(C, Kd[None, :], lu, p["F_rule"], "beaufort" if p["sign"] == "beaufort" else "sub")[2][0]
        print(p["id"], p["length"], p["family"], f"recovered {(dec == P).mean():.2f}")
    EOF
