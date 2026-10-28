"""Word-aware mechanism lane (2026-10-28), pre-registered before any simulation was run.

QUESTION.  Which single encryption rule reproduces, together, the three structures of the unsolved
stream: the adjacent-repeat deficit (86 of 12,900 pairs, 63 inside words / 23 across gaps), the within-word
lag-5 equality carried by S (102 of 2,073 pairs, 11 of them S), and the within-word lag-6 relation
c_i = 24 - 2 c_(i-6) (77 of 1,267 pairs)?  pnotisdev's mech25 / mechanism-search rows simulated nine
rules under their statistics; their best fit ("R4": hold-key repair writing T(c_-6), q 0.81, plus one
extra rune in ~45 % of words) reproduces the deficit and the two lag counts but not the S carrier.
Two discriminators are added here that no lab has used: the sharing of words between lag-5 and lag-6
sites (LP2: 18 of the 554 words of length >= 7 carry both, 10.8 expected, p 0.012) and the S carrier
scored jointly with the rest.

SIMULATION.  English plaintext (Emerson, Essays: First Series, book digraph spelling, its own words)
laid into the 55 unsolved pages' exact rune counts; iid uniform key per page; sign sub.  Rules:
  R0   spend repair: on a would-be repeat, with probability q skip to the next key symbol (this
       repository's fitted soft rule; up to 4 skips)
  R0h  hold repair: emit a uniform rune != previous, key position kept, plaintext rune consumed
  R4   hold repair writing T(c_(i-6)) = 24 - 2 c_(i-6) when the position in the word is >= 6 (uniform
       otherwise; uniform if T would repeat)
  R4n  R4 plus one extra uniform rune (checked against its neighbours) at a uniform in-word position in
       45 % of words of length >= 2
  Rc5  hold repair copying c_(i-5) when the position is >= 5 (uniform otherwise)
  RS   R0 plus literal S: plaintext S is written as S and consumes no key (the solved pages' F rule, on S)
  RF   R0 plus literal F (the solved pages' own rule), for reference
  Rq0  R0 with q = 0 (no repair), the no-structure reference
  q = 0.81 unless stated.  200 replicates per rule.
ADDED 2026-10-28 (second run, after §46 found that the lag-5 echo runs in pairs and that a plain period-5 key copies
plaintext differences LP2 does not show).  Echo rules: in a word selected with probability r = 0.5 (fixed from §46's
mixture fit to the equality count, so the equality count is spent and the other statistics are the test), a plaintext
rune equal to the plaintext rune five back is written as the CIPHERTEXT rune five back (identity echo at lag 5), and,
in the E56 rules, a plaintext rune equal to the one six back is written as 24 - 2 c_(i-6) (the T echo at lag 6);
an echo that would make an adjacent repeat is not applied.  Variants: E5w (lag-5 echo, key spent at the echo, base
R0), E5w-hold (key held), E56w (both echoes, key spent, base R0), E56w-hold, E56w+R4n (both echoes on top of R4n),
E5all (lag-5 echo in every word).  A tenth judged statistic BIG = repeated bigrams at lag 5 inside words (LP2: 9).

STATISTICS (all on within-page pairs; "word" = the simulated plaintext's own words, LP2's transcription
words for the real stream):  D (adjacent repeats), D_in (inside words), L3, L4, L5 (within-word equal pairs
at lags 3, 4, 5), L5S (lag-5 equal pairs whose rune is S), L6T (within-word hits of 24 - 2c at lag 6),
L6best (largest hit count over the 812 affine maps at lag 6), SHARE (words of length >= 7 carrying both a
lag-5 and a lag-6 site, minus the hypergeometric expectation), Sfreq (share of S), U (unigram chi-square, 28 df).

RULE (fixed before running).  A rule SURVIVES if LP2 lies within |z| <= 3 of the rule's replicate
distribution on every one of D, D_in, L3, L4, L5, L5S, L6T, SHARE and Sfreq (nine statistics; the
Bonferroni-corrected 5 % level is |z| 2.8).  A rule that fails any one is excluded as the complete
mechanism at this plaintext and key.  Controls: (1) the measurement code applied to LP2 must return
86 / 63 / 102 / 11 / 77 / 18; (2) Rq0 must give D near 445 and L6T near 44; (3) R0 at q 0.81 must give
D near 86 (calibration of q, not a free fit).  Writes results/mechanism.md and .json.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN, english_to_runes
import corpus

rng = np.random.default_rng(2024)
Q = 0.81; NREP = 200; S_IDX = LATIN.index("S")
T = lambda x: (24 - 2 * x) % N
A = np.arange(1, N)[:, None]; B = np.arange(N)[None, :]

# ---------------- LP2 layout and words
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
LP2 = [parse(chunks[k]) for k in range(16, 72)]; LP2 = [(c, w) for c, w in LP2 if len(c)]
LENS = [len(c) for c, _ in LP2]

# ---------------- English words in runes
text = corpus.TEXTS["emerson_essays1"][0]()
EW = [english_to_runes(w) for w in text.split()]; EW = [w for w in EW if w]
print(f"{len(EW):,} English words, {sum(map(len, EW)):,} runes; LP2 {sum(LENS):,} runes on {len(LENS)} pages", flush=True)

# ---------------- statistics
def pairs_at(c, w, lag):
    ok = np.arange(lag, len(c)); ok = ok[w[ok] == w[ok - lag]]; return ok
def measure(pages):
    allc = np.concatenate([c for c, _ in pages]); allw = np.concatenate([w for _, w in pages])
    page = np.concatenate([np.full(len(c), i) for i, (c, _) in enumerate(pages)])
    D = sum(int((c[1:] == c[:-1]).sum()) for c, _ in pages)
    D_in = sum(int(((c[1:] == c[:-1]) & (w[1:] == w[:-1])).sum()) for c, w in pages)
    out = dict(D=D, D_in=D_in)
    sites = {}
    for lag in (3, 4, 5, 6):
        ok = np.concatenate([pairs_at(c, w, lag) + off for (c, w), off in zip(pages, np.cumsum([0] + LENS_CUR[:-1]))])
        x, y = allc[ok - lag], allc[ok]
        if lag < 6:
            eq = x == y; out[f"L{lag}"] = int(eq.sum())
            if lag == 5:
                out["L5S"] = int((eq & (x == S_IDX)).sum()); sites[5] = ok[eq]
                adj = eq[:-1] & eq[1:] & (ok[1:] == ok[:-1] + 1); out["BIG"] = int(adj.sum())
        else:
            H = np.zeros((N, N)); np.add.at(H, (x, y), 1); xs = np.arange(N)
            tgt = (A[:, :, None] * xs[None, None, :] + B[:, :, None]) % N
            hits = H[xs[None, None, :], tgt].sum(-1)
            out["L6T"] = int(hits[26, 24]); out["L6best"] = int(hits.max()); sites[6] = ok[y == (27 * x + 24) % N]
    # word sharing among words of length >= 7
    wl = {}
    for i in range(len(allc)): wl[(page[i], allw[i])] = wl.get((page[i], allw[i]), 0) + 1
    elig = {k for k, L in wl.items() if L >= 7}
    W5 = {(page[i], allw[i]) for i in sites[5]} & elig; W6 = {(page[i], allw[i]) for i in sites[6]} & elig
    out["SHARE"] = len(W5 & W6) - len(W5) * len(W6) / max(1, len(elig))
    out["Sfreq"] = float((allc == S_IDX).mean())
    cnt = np.bincount(allc, minlength=N); out["U"] = float(((cnt - len(allc) / N) ** 2 / (len(allc) / N)).sum())
    return out

# ---------------- simulator
R_GATE = 0.5
def simulate(rule, q=Q, p_null=0.45):
    echo5 = rule.startswith(("E5", "E56")); echo6 = rule.startswith("E56"); hold_echo = rule.endswith("-hold")
    base = "R4n" if rule.endswith("+R4n") else ("R4" if rule.endswith("+R4") else "R0")
    gate_all = rule == "E5all"
    pages = []; wi = int(rng.integers(0, len(EW) - 5000))
    for L in LENS:
        P, W = [], []; w = 0
        while len(P) < L:
            word = list(EW[wi % len(EW)]); wi += 1
            if base == "R4n" and len(word) >= 2 and rng.random() < p_null:
                pos = int(rng.integers(0, len(word) + 1)); word.insert(pos, -1)      # -1 = null rune, filled at encryption
            P += word; W += [w] * len(word); w += 1
        P, W = np.array(P[:L]), np.array(W[:L])
        k = rng.integers(0, N, 2 * L + 16); c = np.empty(L, int); j = 0; prev = -1; wpos = 0; active = False
        for i in range(L):
            if i == 0 or W[i] != W[i - 1]: wpos = 0; active = gate_all or (rng.random() < R_GATE)
            else: wpos += 1
            p = P[i]
            if (echo5 or echo6) and active and p != -1:
                x = -1
                if echo5 and wpos >= 5 and P[i - 5] == p: x = c[i - 5]
                elif echo6 and wpos >= 6 and P[i - 6] == p: x = T(c[i - 6])
                if x != -1 and x != prev:
                    c[i] = x; prev = x
                    if not hold_echo: j += 1
                    continue
            if p == -1:                                             # extra null rune, checked against its neighbours
                x = int(rng.integers(0, N))
                while x == prev: x = int(rng.integers(0, N))
                c[i] = x; prev = x; continue
            if rule == "RS" and p == S_IDX: c[i] = p; prev = p; continue
            if rule == "RF" and p == 0: c[i] = p; prev = p; continue
            x = (p + k[j]) % N
            if x == prev and rng.random() < q:
                if rule in ("R0", "RS", "RF") or (echo5 and base == "R0"):
                    for _ in range(4):
                        j += 1; x = (p + k[j]) % N
                        if x != prev: break
                else:                                               # hold repairs: key position kept
                    if rule == "R4" or rule == "R4n" or base in ("R4", "R4n"):
                        x = T(c[i - 6]) if wpos >= 6 else -1
                    elif rule == "Rc5":
                        x = c[i - 5] if wpos >= 5 else -1
                    else: x = -1
                    if x == -1 or x == prev:
                        x = int(rng.integers(0, N))
                        while x == prev: x = int(rng.integers(0, N))
                    c[i] = x; prev = x; continue
            c[i] = x; prev = x; j += 1
        pages.append((c, W))
    return pages

STATS = ["D", "D_in", "L3", "L4", "L5", "L5S", "BIG", "L6T", "L6best", "SHARE", "Sfreq", "U"]
JUDGE = ["D", "D_in", "L3", "L4", "L5", "L5S", "BIG", "L6T", "SHARE", "Sfreq"]
LENS_CUR = LENS
ref = measure(LP2); print("LP2:", ref, flush=True)
assert (ref["D"], ref["D_in"], ref["L5"], ref["L5S"], ref["L6T"], ref["BIG"]) == (86, 63, 102, 11, 77, 9), ref
RULES = [("Rq0", dict(q=0.0)), ("R0", {}), ("R0h", {}), ("R4", {}), ("R4n", {}), ("Rc5", {}), ("RS", {}), ("RF", {}),
         ("E5w", {}), ("E5w-hold", {}), ("E5all", {}), ("E56w", {}), ("E56w-hold", {}), ("E56w+R4n", {})]
t0 = time.time(); table = {}
for rule, kw in RULES:
    reps = []
    for r in range(NREP):
        pg = simulate(rule.replace("q0", "0") if rule == "Rq0" else rule, **kw); reps.append(measure(pg))
    arr = {s: np.array([d[s] for d in reps], float) for s in STATS}
    z = {s: (ref[s] - arr[s].mean()) / max(arr[s].std(), 1e-9) for s in STATS}
    table[rule] = dict(mean={s: float(arr[s].mean()) for s in STATS}, sd={s: float(arr[s].std()) for s in STATS}, z=z,
                       survives=bool(all(abs(z[s]) <= 3 for s in JUDGE)), fails=[s for s in JUDGE if abs(z[s]) > 3])
    print(f"  {rule}: " + ", ".join(f"{s} {arr[s].mean():.1f}±{arr[s].std():.1f} (z {z[s]:+.1f})" for s in JUDGE) + f"  -> {'survives' if table[rule]['survives'] else 'fails ' + ','.join(table[rule]['fails'])}  [{time.time()-t0:.0f}s]", flush=True)

out = ["# Word-aware mechanism lane: which rule reproduces the three structures together?", "",
       f"English plaintext (Emerson) in the 55 pages' rune counts, iid uniform key, q = {Q}, {NREP} replicates per rule; statistics, rules and the survival criterion are in the module docstring and were fixed before the run. LP2's own values: " + ", ".join(f"{s} {ref[s]:.3g}" for s in STATS) + ".", "",
       "| rule | " + " | ".join(JUDGE) + " | verdict |", "|---|" + "---|" * (len(JUDGE) + 1)]
for rule, _ in RULES:
    d = table[rule]; out.append(f"| {rule} | " + " | ".join(f"{d['mean'][s]:.1f}±{d['sd'][s]:.1f} (z {d['z'][s]:+.1f})" if s != "Sfreq" else f"{d['mean'][s]:.4f} (z {d['z'][s]:+.1f})" for s in JUDGE) + f" | {'survives' if d['survives'] else 'fails: ' + ', '.join(d['fails'])} |")
out += ["", f"Echo rules use a per-word gate r = {R_GATE} fixed before the run from §46's mixture fit to the equality count; that count is therefore spent for them and the other nine statistics are the test.", "", "Cells are the rule's mean ± sd over replicates and the z of LP2's value against them. L6best (largest hit count over the 812 affine maps at lag 6) is reported in the JSON; LP2's is 77, equal to its L6T, so T is LP2's best map.", ""]
(RESULTS / "mechanism.md").write_text("\n".join(out) + "\n")
json.dump(dict(ref=ref, rules=table, nrep=NREP, q=Q), open(RESULTS / "mechanism.json", "w"), indent=1, default=float)
print("\n".join(out))
