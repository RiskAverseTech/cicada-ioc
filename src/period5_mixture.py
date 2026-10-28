"""Per-word period-5 key: can a key that repeats every five runes inside a fraction f of words explain the lag-5
facts together?  (2026-10-28.)  Under such a key, inside those words c[i+5] - c[i] = p[i+5] - p[i] exactly, so the
within-word lag-5 statistics of those words are English's own: the equality rate, the S..S rate, repeated bigrams,
AND the full 29-cell difference histogram.  The other words contribute uniform differences.  LP2's numbers over its
2,073 within-word lag-5 pairs: 102 equal (4.92 %), 11 S..S, 9 repeated bigrams, difference chi-square 38.9 (28 df).
Measured here on Emerson in rune spelling (own words): the same four per pair; then, for f = 0..1, the predicted LP2
values; which f fits each.  Writes results/period5_mixture.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN, english_to_runes
import corpus
S = LATIN.index("S")
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')
def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)
U = [parse(chunks[k]) for k in range(16, 72)]; U = [(c, w) for c, w in U if len(c)]
def lag5(pages):
    X, Y, X2, Y2 = [], [], [], []
    for c, w in pages:
        ok = np.arange(5, len(c)); ok = ok[w[ok] == w[ok - 5]]
        X.append(c[ok - 5]); Y.append(c[ok])
        ok2 = ok[:-1][(ok[1:] == ok[:-1] + 1)]          # consecutive pairs both inside the word: bigram at lag 5
        X2.append(np.stack([c[ok2 - 5], c[ok2 - 4]], 1)); Y2.append(np.stack([c[ok2], c[ok2 + 1]], 1))
    x, y = np.concatenate(X), np.concatenate(Y); x2, y2 = np.concatenate(X2), np.concatenate(Y2)
    n = len(x); eq = x == y; d = (y - x) % N; cnt = np.bincount(d, minlength=N)
    return dict(n=n, eq=eq.mean(), ss=(eq & (x == S)).mean(), big=(x2 == y2).all(1).mean(), nbig=len(x2),
                hist=cnt / n, chi=((cnt - n / N) ** 2 / (n / N)).sum())
lp = lag5(U)
text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(w) for w in text.split()]; EW = [w for w in EW if w]
# English pages: words laid out with their own boundaries
Ec = np.array([r for w in EW for r in w]); Ew = np.array([i for i, w in enumerate(EW) for _ in w])
en = lag5([(Ec, Ew)])
out = ["# Per-word period-5 key as a mixture: English's own lag-5 statistics against LP2's", "",
       f"LP2: {lp['n']:,} within-word lag-5 pairs; equal {lp['eq']*100:.2f} % (102), S..S {lp['ss']*100:.2f} % (11), repeated bigrams {lp['big']*100:.2f} % ({int(round(lp['big']*lp['nbig']))} of {lp['nbig']:,} adjacent pair-pairs), difference chi-square {lp['chi']:.1f}.",
       f"English (Emerson, {en['n']:,} pairs): equal {en['eq']*100:.2f} %, S..S {en['ss']*100:.2f} %, repeated bigrams {en['big']*100:.2f} %, difference chi-square per 2,073 pairs {en['chi']*2073/en['n']:.1f}.", "",
       "Under a period-5 key in a fraction f of the long words and a uniform-difference cipher elsewhere, the equality, bigram and difference statistics are f·English + (1−f)·uniform. The S..S count is NOT English's: an equal cipher pair takes the value p + k, which is uniform over the key, so it is S with probability 1/29 whatever the plaintext; the prediction is (equal pairs)/29. (The first version of this file used English's own S..S rate here, which was wrong; corrected 2026-10-28 after the §47 simulation showed it.) Predicted values:", "",
       "| f | equal pairs | S..S pairs | repeated bigrams | difference chi-square |", "|---|---|---|---|---|"]
u_eq, u_ss, u_big = 1 / N, (1 / N) * (1 / N), 1 / N ** 2
hist_u = np.full(N, 1 / N)
for f in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0):
    h = f * en["hist"] + (1 - f) * hist_u; chi = lp["n"] * ((h - 1 / N) ** 2 / (1 / N)).sum() + 28
    eqp = lp['n']*(f*en['eq']+(1-f)*u_eq)
    out.append(f"| {f:.1f} | {eqp:.0f} | {eqp/N:.1f} | {lp['nbig']*(f*en['big']+(1-f)*u_big):.1f} | {chi:.0f} |")
out += ["", "LP2 observed: 102 / 11 / 9 / 38.9. The f that fits the equality excess (0.5) predicts 3.5 S..S pairs against 11 and a difference chi-square of 61 against 38.9: the mixture fits one number with one parameter and fails two.", "",
        "English within-word lag-5 difference histogram (share per difference, 0 = equal):", "", "| d | " + " | ".join(str(i) for i in range(N)) + " |", "|---|" + "---|" * N,
        "| English | " + " | ".join(f"{v*100:.1f}" for v in en["hist"]) + " |", "| LP2 | " + " | ".join(f"{v*100:.1f}" for v in lp["hist"]) + " |", ""]
(RESULTS / "period5_mixture.md").write_text("\n".join(out) + "\n"); print("\n".join(out[:18]))
