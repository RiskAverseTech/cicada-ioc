"""Digits of pi, e, sqrt(2) and phi in base 10 and base 29 (2026-10-28), pure integer arithmetic.
Writes data/processed/irrational_digits.json: {"pi": {"b10": "1415...", "b29": [..]}, ...} with D fractional
digits each; the leading integer digit is dropped.  Checked against the known first 15 digits.
"""
import json, sys
from math import isqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lp import PROCESSED

D = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
G = 10 ** (D + 20)          # guard digits

def arctan_inv(x):           # arctan(1/x) * G
    total = term = G // x; x2 = x * x; k = 1; sign = -1
    while term:
        term //= x2; total += sign * (term // (2 * k + 1)); k += 1; sign = -sign
    return total

def pi_scaled(): return 4 * (4 * arctan_inv(5) - arctan_inv(239))
def e_scaled():
    total = term = G; k = 1
    while term: term //= k; total += term; k += 1
    return total
def sqrt_scaled(n): return isqrt(n * G * G)
def phi_scaled(): return (G + sqrt_scaled(5)) // 2

def frac_digits(scaled, base):
    frac = scaled % G; out = []
    for _ in range(D):
        frac *= base; out.append(frac // G); frac %= G
    return out

consts = {"pi": pi_scaled(), "e": e_scaled(), "sqrt2": sqrt_scaled(2), "phi": phi_scaled()}
known = {"pi": "14159265358979", "e": "71828182845904", "sqrt2": "41421356237309", "phi": "61803398874989"}
out = {}
for name, v in consts.items():
    b10 = "".join(map(str, frac_digits(v, 10)))
    assert b10.startswith(known[name]), (name, b10[:20])
    out[name] = {"b10": b10, "b29": frac_digits(v, 29)}
    print(name, b10[:20], out[name]["b29"][:12])
(PROCESSED / "irrational_digits.json").write_text(json.dumps(out))
print("written", D, "digits each")
