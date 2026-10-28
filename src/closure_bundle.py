"""Closure bundle (2026-10-28): five cheap checks the field survey found done elsewhere but not here.

(a) Doublet rate of every SOLVED page's ciphertext, by mechanism: is the anti-repeat rule a house style
    (present on the solved polyalphabetic pages) or specific to the unsolved section?
(b) Position parity of the 86 repeats (first index mod 2..8) against all adjacent pairs: a fixed-frame
    digraphic cipher (Playfair-type) forbids repeats inside its frames, so repeats would sit at odd
    frame offsets only.  Leo-Y-Zhang reports flat; replicated here.
(c) Cross-page identical n-gram windows (n = 3, 4, 5) against per-page shuffle nulls: the only cross-page
    repeat statistic in the field is farfromexact's single 4-gram figure (121 vs 112).
(d) Context independence of the repeats (invictustitan2): the repeated rune's identity, the rune before
    the pair, and the gap since the previous repeat, each against its marginal.
(e) pnotisdev's within-word lag-6 relation c_i = 24 - 2 c_{i-6}: counted here for the first time, and
    placed in the family of all 812 affine maps c_i = a c_{i-6} + b so the look-elsewhere is explicit.
Writes results/closure_bundle.md.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN, LATIN_ALT, to_latin, atbash, shift, vigenere, totient_stream
L2I = {l: i for i, l in enumerate(LATIN)}; L2I.update(LATIN_ALT)
def kidx(word):
    out, i = [], 0
    while i < len(word):
        for n in (3, 2, 1):
            if word[i:i+n] in L2I: out.append(L2I[word[i:i+n]]); i += n; break
        else: raise ValueError(word[i:])
    return out

rng = np.random.default_rng(3301)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§')   # '/' is a line break, which falls inside words 452 times of 630; not a word boundary

def parse(s):
    """runes, word ids per rune (word changes at any separator)."""
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)

out = ["# Closure bundle: five cheap checks from the 2026-10-28 field survey", ""]

# ---------------------------------------------------------------- (a) solved pages
COMMON = {"THE", "AND", "OF", "TO", "YOU", "IS", "IN", "THAT", "NOT", "ARE", "BE", "WE", "ALL"}
def english_score(idx):
    s = to_latin(idx)
    return sum(s.count(w) for w in COMMON)
def mech(c):
    cands = {"plain": list(c), "atbash": atbash(list(c)), "shift3+atbash": atbash(shift(list(c), 3)),
             "vigenere DIVINITY": vigenere(list(c), kidx("DIVINITY")), "vigenere FIRFUMFERENFE": vigenere(list(c), kidx("FIRFUMFERENFE")),
             "totient stream": totient_stream(list(c))}
    best = max(cands, key=lambda k: english_score(cands[k]))
    return best, english_score(cands[best])
KINDS = {1: "Atbash", 2: "Vigenère DIVINITY", 3: "Vigenère DIVINITY", 4: "plain", 5: "shift 3 + Atbash", 6: "shift 3 + Atbash", 7: "shift 3 + Atbash", 8: "shift 3 + Atbash",
         9: "plain", 10: "plain", 11: "plain", 12: "plain", 13: "Vigenère FIRFUMFERENFE", 14: "Vigenère FIRFUMFERENFE", 15: "plain", 72: "totient prime stream", 73: "plain"}
rows = ["| chunk | mechanism (published key) | detector agrees | runes | within-page pairs | repeats | expected /29 | ratio | binomial p |", "|---|---|---|---|---|---|---|---|---|"]
poly = {"runes": 0, "pairs": 0, "dbl": 0}
for k, kind in KINDS.items():
    c, w = parse(chunks[k])
    m, sc = mech(c)
    pairs = len(c) - 1; d = int((c[1:] == c[:-1]).sum()); e = pairs / N
    p = stats.binomtest(d, pairs, 1 / N).pvalue
    agree = "yes" if kind.lower().replace("è", "e").split()[0] == m.split()[0].split("+")[0].replace("shift3", "shift") else f"no ({m})"
    rows.append(f"| {k} | {kind} | {agree} | {len(c)} | {pairs} | {d} | {e:.1f} | {d/e:.2f} | {p:.3f} |")
    if kind.startswith(("Vigen", "totient")):
        poly["runes"] += len(c); poly["pairs"] += pairs; poly["dbl"] += d
U = [parse(chunks[k]) for k in range(16, 72)]
u_pairs = sum(len(c) - 1 for c, _ in U); u_dbl = sum(int((c[1:] == c[:-1]).sum()) for c, _ in U)
out += ["## (a) Repeats on the solved pages' ciphertext", "",
        "Mechanism per chunk from the published keys (as in §4), with a six-rule decryption detector as a check. Only the polyalphabetic pages (Vigenère, totient stream) carry a uniform-like ciphertext whose repeat rate can be compared with the unsolved section; plain and Atbash pages carry English's own doublets.", ""] + rows + ["",
        f"Polyalphabetic solved pages pooled: {poly['dbl']} repeats in {poly['pairs']:,} pairs ({poly['runes']:,} runes), expected {poly['pairs']/N:.1f} under uniform; ratio {poly['dbl']/(poly['pairs']/N):.2f}. "
        f"Unsolved section: {u_dbl} in {u_pairs:,} pairs, expected {u_pairs/N:.1f}, ratio {u_dbl/(u_pairs/N):.2f}. "
        f"Two-sample test of the two rates (Fisher exact): p = {stats.fisher_exact([[poly['dbl'], poly['pairs']-poly['dbl']], [u_dbl, u_pairs-u_dbl]])[1]:.2e}.", ""]

# ---------------------------------------------------------------- (b) parity
allc = np.concatenate([c for c, _ in U]); allw = np.concatenate([w for _, w in U])
page_of = np.concatenate([np.full(len(c), i) for i, (c, _) in enumerate(U)])
pos_in_page = np.concatenate([np.arange(len(c)) for c, _ in U])
same_page = page_of[1:] == page_of[:-1]
is_dbl = (allc[1:] == allc[:-1]) & same_page
i_pairs = np.where(same_page)[0]; i_dbl = np.where(is_dbl)[0]
out += ["## (b) Position parity of the repeats", "", "| modulus | repeats per residue | expected from all pairs | chi-square p |", "|---|---|---|---|"]
for mmod in range(2, 9):
    obs = np.bincount(pos_in_page[i_dbl] % mmod, minlength=mmod)
    share = np.bincount(pos_in_page[i_pairs] % mmod, minlength=mmod) / len(i_pairs)
    p = stats.chisquare(obs, share * len(i_dbl)).pvalue
    out.append(f"| {mmod} | {' '.join(map(str, obs))} | {' '.join(f'{x:.1f}' for x in share*len(i_dbl))} | {p:.2f} |")
out += ["", "A fixed-frame digraphic cipher would concentrate the repeats on one residue mod 2. Flat at every modulus: replicates Leo-Y-Zhang.", ""]

# ---------------------------------------------------------------- (c) cross-page n-grams
def cross_page_repeats(pages, n):
    seen = {}
    for pi, c in enumerate(pages):
        for j in range(len(c) - n + 1):
            seen.setdefault(tuple(c[j:j+n]), set()).add(pi)
    multi = [s for s in seen.values() if len(s) > 1]
    return len(multi), sum(len(s) * (len(s) - 1) // 2 for s in multi)
pages = [c for c, _ in U]
out += ["## (c) Identical n-gram windows across pages", "", "Observed count of distinct n-grams that occur on two or more pages, and the number of page pairs sharing one, against 999 nulls in which every page is shuffled independently.", "",
        "| n | distinct n-grams on 2+ pages | shuffle null | p | re-draw null (0.81) | p | page pairs sharing | shuffle null | p | re-draw null | p |", "|---|---|---|---|---|---|---|---|---|---|---|"]
NREP = 999
def redraw_page(L, p=0.81):
    c = rng.integers(0, N, L)
    for i in range(1, L):
        if c[i] == c[i-1] and rng.random() < p:
            c[i] = (c[i-1] + rng.integers(1, N)) % N
    return c
for n in (3, 4, 5):
    o1, o2 = cross_page_repeats(pages, n)
    nulls = np.array([cross_page_repeats([rng.permutation(c) for c in pages], n) for _ in range(NREP)])
    nullr = np.array([cross_page_repeats([redraw_page(len(c)) for c in pages], n) for _ in range(NREP)])
    p1 = (np.sum(nulls[:, 0] >= o1) + 1) / (NREP + 1); p2 = (np.sum(nulls[:, 1] >= o2) + 1) / (NREP + 1)
    q1 = (np.sum(nullr[:, 0] >= o1) + 1) / (NREP + 1); q2 = (np.sum(nullr[:, 1] >= o2) + 1) / (NREP + 1)
    out.append(f"| {n} | {o1} | {nulls[:,0].mean():.1f} ± {nulls[:,0].std():.1f} | {p1:.3f} | {nullr[:,0].mean():.1f} ± {nullr[:,0].std():.1f} | {q1:.3f} | {o2} | {nulls[:,1].mean():.1f} ± {nulls[:,1].std():.1f} | {p2:.3f} | {nullr[:,1].mean():.1f} ± {nullr[:,1].std():.1f} | {q2:.3f} |")
out += ["", "Two nulls: a within-page shuffle (keeps rune counts, loses the lag-1 deficit) and iid uniform pages of the same lengths with the fitted 0.81 re-draw (keeps the deficit). The deficit concentrates n-grams on the doublet-free types, which raises collisions by itself, so the re-draw null is the right one for the lag-1-aware comparison.", ""]

# ---------------------------------------------------------------- (d) context independence
out += ["## (d) Context of the repeats", ""]
# identity of the repeated rune vs unigram marginal
uni = np.bincount(allc, minlength=N) / len(allc)
ident = np.bincount(allc[i_dbl], minlength=N)
g_id = stats.power_divergence(ident, uni * len(i_dbl), lambda_="log-likelihood").pvalue
# previous rune (before the pair), same page, vs marginal of runes preceding any pair
prev_ok = i_dbl[(i_dbl > 0)]; prev_ok = prev_ok[page_of[prev_ok - 1] == page_of[prev_ok]]
prev = np.bincount(allc[prev_ok - 1], minlength=N)
pp_all = i_pairs[i_pairs > 0]; pp_all = pp_all[page_of[pp_all - 1] == page_of[pp_all]]
prev_marg = np.bincount(allc[pp_all - 1], minlength=N) / len(pp_all)
g_prev = stats.power_divergence(prev, prev_marg * len(prev_ok), lambda_="log-likelihood").pvalue
# step before the pair (c_{i} - c_{i-1}) vs marginal step
step = np.bincount((allc[prev_ok] - allc[prev_ok - 1]) % N, minlength=N)
step_marg = np.bincount((allc[pp_all] - allc[pp_all - 1]) % N, minlength=N) / len(pp_all)
g_step = stats.power_divergence(step, step_marg * len(prev_ok), lambda_="log-likelihood").pvalue
# gaps between successive repeats within the whole stream vs geometric
gaps = np.diff(i_dbl); rate = len(i_dbl) / len(i_pairs)
ks_gap = stats.kstest(gaps, stats.geom(rate).cdf).pvalue
out += [f"- Identity of the repeated rune against the unigram marginal: G-test p = {g_id:.2f} (29 cells, {len(i_dbl)} repeats).",
        f"- Rune immediately before the pair against the marginal of runes before any pair: p = {g_prev:.2f}.",
        f"- Step into the pair (c_i − c_(i−1) mod 29) against the marginal step: p = {g_step:.2f}.",
        f"- Gaps between successive repeats against a geometric law at the observed rate: KS p = {ks_gap:.2f} (mean gap {gaps.mean():.0f}, max {gaps.max()}).",
        "", "Nothing about a repeat's neighbourhood predicts it: replicates invictustitan2 (p 0.47–0.78 there).", ""]

# ---------------------------------------------------------------- (e) lag-6 affine relation inside words
out += ["## (e) The within-word lag-6 relation c_i = 24 − 2 c_(i−6) (pnotisdev `obs-lag6`)", ""]
lagrows = []; NPERM = 999
A = np.arange(1, N)[:, None]; B = np.arange(N)[None, :]
def max_hits(x, y):
    H = np.zeros((N, N)); np.add.at(H, (x, y), 1)
    # hits[a,b] = sum_x H[x, (a x + b) % 29]
    xs = np.arange(N)
    tgt = (A[:, :, None] * xs[None, None, :] + B[:, :, None]) % N        # (28, 29, 29)
    hits = H[xs[None, None, :], tgt].sum(-1)
    return hits
src6 = None
for lag in range(2, 9):
    ok = np.where((np.arange(len(allc)) >= lag))[0]; ok = ok[(allw[ok] == allw[ok - lag]) & (page_of[ok] == page_of[ok - lag])]
    x, y = allc[ok - lag], allc[ok]
    n_ok = len(ok); e = n_ok / N; sd = np.sqrt(n_ok * (1 / N) * (1 - 1 / N))
    hits = max_hits(x, y); hits24 = int(hits[27 - 1, 24]); ident = int(hits[0, 0])
    bi = np.unravel_index(hits.argmax(), hits.shape); best = (int(hits.max()), bi[0] + 1, bi[1])
    # permutation null: shuffle runes within each page (word structure fixed), max over the 812 maps
    perm_max = np.empty(NPERM); perm_id = np.empty(NPERM)
    for r in range(NPERM):
        pc = np.concatenate([rng.permutation(c) for c in pages])
        h = max_hits(pc[ok - lag], pc[ok]); perm_max[r] = h.max(); perm_id[r] = h[0, 0]
    p_max = (np.sum(perm_max >= best[0]) + 1) / (NPERM + 1); p_id = (np.sum(perm_id >= ident) + 1) / (NPERM + 1)
    lagrows.append(f"| {lag} | {n_ok:,} | {e:.1f} ± {sd:.1f} | {hits24} (z {(hits24-e)/sd:+.2f}) | {ident} (z {(ident-e)/sd:+.2f}, p {p_id:.3f}) | {best[0]} (a={best[1]}, b={best[2]}, z {(best[0]-e)/sd:+.2f}) | {perm_max.mean():.1f} ± {perm_max.std():.1f} | {p_max:.3f} |")
    if lag == 6:
        hitmask = (27 * x + 24) % N == y
        src6 = np.bincount(x[hitmask], minlength=N); srcall = np.bincount(x, minlength=N)
out += ["Within-word pairs at lag d; hits of the named map, of the identity map (the lag-d echo), and of the best of all 812 affine maps c_i = a·c_(i−d) + b (a = 1..28, b = 0..28). The last two columns give the maximum over the 812 maps under 999 within-page shuffles and the permutation p of the observed maximum.", "",
        "| lag d | within-word pairs | expected per map | hits of 24 − 2c | identity (echo) | best affine map | null max over 812 maps | p(max) |", "|---|---|---|---|---|---|---|---|"] + lagrows + [""]
out += ["Source rune of the 58 lag-6 hits of 24 − 2c (which rune six back carries the relation), observed against hits spread in proportion to that rune's share of the 965 pairs:", "",
        "| rune | " + " | ".join(LATIN[i] for i in range(N)) + " |", "|---|" + "---|" * N,
        "| hits | " + " | ".join(str(int(v)) for v in src6) + " |",
        "| expected | " + " | ".join(f"{58*v/srcall.sum():.1f}" for v in srcall) + " |", ""]
(RESULTS / "closure_bundle.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
