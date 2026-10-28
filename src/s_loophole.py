"""Two checks prompted by a Quorum panel (2026-10-28, quorumsays.com/q/XoHCqqb6ziaf): (1) the §47 argument needs the key
UNIFORM at the echo positions, not merely independent of the plaintext; a key that is constant (or zero) inside the
gated words would let plaintext S..S pairs at lag 5 show through as cipher S..S.  How much of that loophole does the
overall S share leave?  (2) swap versus marker: a count-preserving swap that moves an S into the lag-5 slot leaves an
S hole elsewhere in the same word; a marker does not.  Count S elsewhere in the 11 echo words against expectation.
Writes results/s_loophole.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
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
allc = np.concatenate([c for c, _ in U]); n_all = len(allc); s_share = float((allc == S).mean())
# English: S share and the lag-5 S..S rate per within-word pair
text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(wd) for wd in text.split()]; EW = [wd for wd in EW if wd]
Ec = np.array([r for wd in EW for r in wd]); Ew = np.array([i for i, wd in enumerate(EW) for _ in wd])
ok = np.arange(5, len(Ec)); ok = ok[Ew[ok] == Ew[ok - 5]]
e_ss = float(((Ec[ok] == S) & (Ec[ok - 5] == S)).mean()); e_s = float((Ec == S).mean())
n5 = 2073; sd_share = np.sqrt(s_share * (1 - s_share) / n_all)
out = ["# The uniform-key loophole and the swap-versus-marker test", "",
       f"LP2: S share {s_share*100:.2f} % of {n_all:,} runes (binomial sd {sd_share*100:.2f} points); 11 S..S pairs among {n5:,} within-word lag-5 pairs. English (Emerson, rune spelling): S share {e_s*100:.2f} %, S..S at lag 5 {e_ss*100:.2f} % of within-word pairs.", "",
       "## (1) A key that is zero (plaintext in clear) or constant inside a fraction f of the words", "",
       "With key 0 inside the gated words, cipher S..S at lag 5 there is the plaintext rate and the S share rises toward English's. With a constant non-zero key per word, S..S at lag 5 needs plaintext (S − k)..(S − k), which averages over k to no S preference, so zero is the worst case. Predictions by f:", "",
       "| f (words in clear) | S share predicted | sd above LP2 | S..S pairs predicted |", "|---|---|---|---|"]
for f in (0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5):
    share = f * e_s + (1 - f) * s_share; ss = n5 * (f * e_ss + (1 - f) / N ** 2)
    out.append(f"| {f:.2f} | {share*100:.2f} % | {(share - s_share)/sd_share:+.1f} | {ss:.1f} |")
fmax = (s_share + 2 * sd_share - s_share) / (e_s - s_share)
out += ["", f"The S share allows f ≤ {fmax:.2f} at two sd, which predicts at most {n5*(fmax*e_ss+(1-fmax)/N**2):.1f} S..S pairs against 11. So the panel's correction is right (the argument needs a uniform key at the echo positions) and the loophole it opens is bounded by the S share to well under the observed count. [the §47 statement is amended accordingly]", "",
       "## (2) Swap versus marker: S elsewhere in the eleven echo words", ""]
# echo words
rows = []; tot_other = 0; tot_exp = 0.0
for pid, (c, w) in enumerate(U):
    for j in range(5, len(c)):
        if w[j] == w[j - 5] and c[j] == c[j - 5] == S:
            m = w == w[j]; L = int(m.sum()); other = int((c[m] == S).sum()) - 2
            exp = (L - 2) * s_share; tot_other += other; tot_exp += exp
            rows.append(f"| LP2-{pid:02d} | {''.join(LATIN[v] for v in c[m])} | {L} | {other} | {exp:.2f} |")
out += ["| page | word | length | S beyond the pair | expected at the S share |", "|---|---|---|---|---|"] + rows + ["",
        f"Total S beyond the pairs: {tot_other} against {tot_exp:.1f} expected (Poisson p for a deficit = {stats.poisson.cdf(tot_other, tot_exp):.2f}). A count-preserving swap that borrowed each echoed S from the same word would leave a deficit here; a marker or overwrite would not. At eleven words the test has little power either way; it is recorded, not decisive.", ""]
(RESULTS / "s_loophole.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
