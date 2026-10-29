"""Layout follow-up to §50 (2026-10-28, §51), pre-registered.  §50 found, by eye and then by count, that the within-word
lag-5 echo is about twice as strong on pairs that wrap a line (30 of 428 against 14.6) as on same-line pairs (72 of
1,645 against 56.2), two-proportion z +2.24, with lag 4, lag 6 and the lag-6 T relation showing no such dependence.
If a line-filling step is involved, the echo should care WHERE the line break falls relative to the pair.  Two
statistics, their null predictions and the decision rule are fixed here before the check (--register writes them and
is committed first; --check computes LP2):
  A  Split position of wrapping equal pairs.  For a within-word lag-5 pair that straddles a break, s = number of the
     five positions (i-4 .. i) that lie on the new line, s = 1..5 (s = 1: the second rune is the first on its line;
     s = 5: the first rune is the last on its line).  H0 (no layout effect): the 30 equal wrapping pairs are
     distributed over s as all 428 wrapping pairs are.  Test: chi-square with simulated p (5 cells, small counts).
  B  Echo rate by distance of the pair from the nearest line edge, for SAME-LINE pairs: d = min(runes from the first
     rune back to the line start, runes from the second rune forward to the line end), binned 0, 1, 2, 3-4, 5+.
     H0: the equality rate is the same in every bin (72 / 1,645 overall).  Test: chi-square of equal pairs across the
     bins against the bins' shares of all same-line pairs, simulated p; plus a trend z (Cochran-Armitage).
  Decision rule: a p < 0.01 on A or on B counts as support for a layout step; p >= 0.01 on both leaves §50's wrap
  excess as an unexplained 2.2-sigma cut.  Also reported, descriptive only: runes per line, share of lines that end
  inside a word, mean length of words that wrap against words that do not, and the same A and B tables for the lag-6
  T relation and lag-4 equality as controls.
Writes results/layout_followup.md (both phases) and .json (the registration)."""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import stats
from lp import IDX, RAW, RESULTS, N, LATIN
rng = np.random.default_rng(51); S = LATIN.index("S"); T = lambda x: (24 - 2 * x) % N
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
WSEP = set('-.&$§'); LSEP = set('/&$§')
def parse(s):
    runes, wid, lid = [], [], []; w = 0; l = 0; pw = False; pl = False
    for ch in s:
        if ch in IDX:
            if pw: w += 1; pw = False
            if pl: l += 1; pl = False
            runes.append(IDX[ch]); wid.append(w); lid.append(l)
        else:
            if ch in WSEP: pw = True
            if ch in LSEP: pl = True
    return np.array(runes), np.array(wid), np.array(lid)
U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0])]
def geometry(c, w, l):
    n = len(c); pos_from_start = np.zeros(n, int); pos_to_end = np.zeros(n, int)
    for i in range(1, n): pos_from_start[i] = pos_from_start[i - 1] + 1 if l[i] == l[i - 1] else 0
    for i in range(n - 2, -1, -1): pos_to_end[i] = pos_to_end[i + 1] + 1 if l[i] == l[i + 1] else 0
    return pos_from_start, pos_to_end
def tables(pages, lag, rel):
    """A: split position counts (all pairs, equal pairs); B: distance-bin counts (all same-line pairs, equal)."""
    A_all = np.zeros(lag + 1, int); A_eq = np.zeros(lag + 1, int); B_all = np.zeros(5, int); B_eq = np.zeros(5, int)
    for c, w, l in pages:
        ps, pe = geometry(c, w, l)
        for i in range(lag, len(c)):
            if w[i] != w[i - lag]: continue
            hit = (c[i] == c[i - lag]) if rel == "id" else (c[i] == T(c[i - lag]))
            if l[i] != l[i - lag]:
                s = int(ps[i]) + 1                     # runes of the pair's span on the new line = position of i on its line + 1
                s = min(max(s, 1), lag); A_all[s] += 1; A_eq[s] += hit
            else:
                d = min(ps[i - lag], pe[i]); b = 0 if d == 0 else 1 if d == 1 else 2 if d == 2 else 3 if d <= 4 else 4
                B_all[b] += 1; B_eq[b] += hit
    return A_all[1:], A_eq[1:], B_all, B_eq
def sim_p(obs, exp_share, n, reps=20000):
    e = exp_share * n; chi = ((obs - e) ** 2 / np.maximum(e, 1e-9)).sum()
    sims = rng.multinomial(n, exp_share, size=reps); chis = ((sims - e) ** 2 / np.maximum(e, 1e-9)).sum(1)
    return chi, float((np.sum(chis >= chi) + 1) / (reps + 1))
REG = RESULTS / "layout_followup.json"
if "--register" in sys.argv:
    # null predictions use only the pair populations (no equality counts are read)
    A_all, _, B_all, _ = tables(U, 5, "id")
    reg = dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), A_pairs=A_all.tolist(), A_null_share=(A_all / A_all.sum()).tolist(), B_pairs=B_all.tolist(), B_null_share=(B_all / B_all.sum()).tolist(), rule="p < 0.01 on A or B supports a layout step")
    json.dump(reg, open(REG, "w"), indent=1)
    lines = ["# Layout follow-up: registration", "", f"Written {reg['written']}. Null shares come from the pair populations only; no equality count was read.", "",
             "| A: split position s | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|", "| wrapping lag-5 pairs | " + " | ".join(map(str, A_all)) + " |", "| null share | " + " | ".join(f"{v:.3f}" for v in A_all / A_all.sum()) + " |", "",
             "| B: distance to line edge d | 0 | 1 | 2 | 3-4 | 5+ |", "|---|---|---|---|---|---|", "| same-line lag-5 pairs | " + " | ".join(map(str, B_all)) + " |", "| null share | " + " | ".join(f"{v:.3f}" for v in B_all / B_all.sum()) + " |", "",
             "Decision rule: simulated chi-square p < 0.01 on A or on B counts as support for a layout step."]
    (RESULTS / "layout_followup.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
elif "--check" in sys.argv:
    reg = json.load(open(REG)); out = ["# Layout follow-up: check", "", f"Registered {reg['written']}; checked afterwards."]
    for lag, rel, name in ((5, "id", "lag-5 equality"), (6, "T", "lag-6 T relation (control)"), (4, "id", "lag-4 equality (control)")):
        A_all, A_eq, B_all, B_eq = tables(U, lag, rel)
        chiA, pA = sim_p(A_eq, A_all / A_all.sum(), A_eq.sum()); chiB, pB = sim_p(B_eq, B_all / B_all.sum(), B_eq.sum())
        # trend across distance bins (Cochran-Armitage with scores 0..4)
        sc = np.arange(5); pbar = B_eq.sum() / B_all.sum(); num = (sc * (B_eq - pbar * B_all)).sum(); den = np.sqrt(pbar * (1 - pbar) * ((sc ** 2 * B_all).sum() - (sc * B_all).sum() ** 2 / B_all.sum()))
        zt = num / den if den > 0 else 0.0
        out += ["", f"## {name}", "", "| A: split position s | " + " | ".join(str(s) for s in range(1, lag + 1)) + " |", "|---|" + "---|" * lag,
                "| all wrapping pairs | " + " | ".join(map(str, A_all)) + " |", "| equal (hit) pairs | " + " | ".join(map(str, A_eq)) + " |", "| hits expected under H0 | " + " | ".join(f"{v:.1f}" for v in A_eq.sum() * A_all / A_all.sum()) + " |", "| hit rate | " + " | ".join(f"{h/max(t,1)*100:.1f}%" for h, t in zip(A_eq, A_all)) + " |",
                "", f"A: chi-square {chiA:.2f}, simulated p = {pA:.3f} ({A_eq.sum()} hits among {A_all.sum()} wrapping pairs).", "",
                "| B: distance to line edge | 0 | 1 | 2 | 3-4 | 5+ |", "|---|---|---|---|---|---|", "| all same-line pairs | " + " | ".join(map(str, B_all)) + " |", "| equal (hit) pairs | " + " | ".join(map(str, B_eq)) + " |", "| hits expected under H0 | " + " | ".join(f"{v:.1f}" for v in B_eq.sum() * B_all / B_all.sum()) + " |", "| hit rate | " + " | ".join(f"{h/max(t,1)*100:.1f}%" for h, t in zip(B_eq, B_all)) + " |",
                "", f"B: chi-square {chiB:.2f}, simulated p = {pB:.3f}; trend z toward the line edge {-zt:+.2f} (positive = higher rate nearer the edge)."]
    # descriptive line geometry
    ll = []; wrap_words = set(); all_words = {}
    for c, w, l in U:
        for L in np.unique(l): ll.append(int((l == L).sum()))
        for i in range(1, len(c)):
            all_words[(id(c), w[i])] = all_words.get((id(c), w[i]), 0) + 1
            if l[i] != l[i - 1] and w[i] == w[i - 1]: wrap_words.add((id(c), w[i]))
        all_words[(id(c), w[0])] = all_words.get((id(c), w[0]), 0) + 1
    nl = len(ll); nwrap_lines = sum(1 for c, w, l in U for i in range(1, len(c)) if l[i] != l[i - 1] and w[i] == w[i - 1])
    lw = [n for k, n in all_words.items() if k in wrap_words]; lo = [n for k, n in all_words.items() if k not in wrap_words]
    out += ["", "## Line geometry (descriptive)", "", f"{nl:,} lines on the 55 pages; runes per line mean {np.mean(ll):.1f}, sd {np.std(ll):.1f}, min {min(ll)}, max {max(ll)}; {nwrap_lines} line breaks fall inside a word ({nwrap_lines/nl:.0%} of lines); words that wrap are {np.mean(lw):.2f} runes long on average against {np.mean(lo):.2f} for words that do not.", "",
            "Reading is in README §51."]
    (RESULTS / "layout_followup.md").write_text("\n".join(out) + "\n"); print("\n".join(out))
