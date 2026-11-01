"""Quorum's ask (registration: results/discovery_replay_registration.md, commit f816cfc): the joint discovery replay and the
word-end anchoring check, on the audit's K-fixed arrangements.

R: three scans as the field ran them, inside every null arrangement: (i) within-word equality at lags 2-12, max z over lags;
(ii) within-word affine maps c = a c' + b (812) at lags 2-8, max z over 5,684 cells; (iii) rune concentration at the equality
sites of the lag that won (i), max over 29 runes of (count - n f_r) / sqrt(n f_r (1 - f_r)).  Each cell standardized by its own
null mean and sd; family-wise p per scan; the joint share of arrangements with all three maxima at least the observed; the
adjacency of the winning lags.  E: for lag-5 sites and lag-6 hits, the later rune's distance from the word's end; the share at
distance 0 or 1 against the null.  Reproduce: .venv/bin/python -I src/discovery_replay.py
"""
import sys, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN
from kfixed import kfixed_step, doublets

t0 = time.time(); rng = np.random.default_rng(1034); NREP, BURN, THIN = 999, 20, 4; S = LATIN.index("S")
LAGS_EQ = list(range(2, 13)); LAGS_AF = list(range(2, 9)); A = np.arange(1, N); B = np.arange(N); XS = np.arange(N)
TGT = (A[:, None, None] * XS[None, None, :] + B[None, :, None]) % N                 # (28, 29, 29): target rune for (a, b, x)
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%"); SEP = set('-.&$§')
def log(*a): print(*a, f"[{time.time()-t0:.0f}s]", flush=True)


def parse(s):
    runes, wid = [], []; w = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w)
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int)


U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0]) > 6]; assert len(U) == 55
ALL = np.concatenate([c for c, _ in U]); FREQ = np.bincount(ALL, minlength=N) / len(ALL)
# distance of each position from the end of its word, fixed by the word structure (arrangements permute runes, not words)
ENDD = []
for c, w in U:
    d = np.zeros(len(c), int); last = {}
    for i in range(len(c) - 1, -1, -1):
        last.setdefault(w[i], i); d[i] = last[w[i]] - i
    ENDD.append(d)


def scans(pages):
    """equality counts per lag (11), affine hit counts per lag x map (7, 812), rune counts at equality sites per lag (11, 29),
    end-distance shares: lag-5 sites and lag-6 hits at distance 0 or 1 (counts and totals)"""
    eq = np.zeros(len(LAGS_EQ), int); af = np.zeros((len(LAGS_AF), 28 * N), int); rc = np.zeros((len(LAGS_EQ), N), int)
    e5 = [0, 0]; h6 = [0, 0]
    for k, (c, w) in enumerate(pages):
        L = len(c); dend = ENDD[k]
        for j, d in enumerate(LAGS_EQ):
            if L <= d: continue
            i = np.arange(d, L); m = w[i] == w[i - d]; e = m & (c[i] == c[i - d]); eq[j] += int(e.sum()); rc[j] += np.bincount(c[i[e]], minlength=N)
            if d == 5: e5[0] += int((dend[i[e]] <= 1).sum()); e5[1] += int(e.sum())
        for j, d in enumerate(LAGS_AF):
            if L <= d: continue
            i = np.arange(d, L); m = w[i] == w[i - d]; x, y = c[i[m] - d], c[i[m]]
            Hm = np.zeros((N, N), int); np.add.at(Hm, (x, y), 1)
            af[j] += Hm[XS[None, None, :], TGT].sum(-1).reshape(-1)
            if d == 6:
                hit = y == (24 - 2 * x) % N; h6[0] += int((dend[i[m][hit]] <= 1).sum()); h6[1] += int(hit.sum())
    return eq, af, rc, np.array(e5), np.array(h6)


obs = scans(U); log("observed: lag-5 equal", obs[0][3], "lag-6 24-2c hits", obs[1][4][(27 - 1) * N + 24], "S at lag-5 sites", obs[2][3][S], "end-share lag5", obs[3], "lag6", obs[4])
cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
for c, _ in cur: kfixed_step(c, BURN * len(c), rng)
EQ = np.zeros((NREP, len(LAGS_EQ)), int); AF = np.zeros((NREP, len(LAGS_AF), 28 * N), np.int32); RC = np.zeros((NREP, len(LAGS_EQ), N), int); E5 = np.zeros((NREP, 2), int); H6 = np.zeros((NREP, 2), int)
for r in range(NREP):
    for c, _ in cur: kfixed_step(c, THIN * len(c), rng)
    EQ[r], AF[r], RC[r], E5[r], H6[r] = scans(cur)
    if (r + 1) % 100 == 0: log("rep", r + 1)
assert all(doublets(c) == k for (c, _), k in zip(cur, ks))

# ---------- standardize, maxima, family-wise and joint
mu_eq, sd_eq = EQ.mean(0), EQ.std(0); mu_af, sd_af = AF.mean(0), AF.std(0); sd_af[sd_af == 0] = np.inf
z_eq_obs = (obs[0] - mu_eq) / sd_eq; z_eq_null = (EQ - mu_eq) / sd_eq
z_af_obs = (obs[1] - mu_af) / sd_af; z_af_null = (AF - mu_af) / sd_af
def rune_z(rc_row):
    n = rc_row.sum(); return (rc_row - n * FREQ) / np.sqrt(n * FREQ * (1 - FREQ)) if n > 0 else np.zeros(N)
best_eq_obs = int(np.argmax(z_eq_obs)); m1_obs = float(z_eq_obs.max()); m2_obs = float(z_af_obs.max()); m3_obs = float(rune_z(obs[2][best_eq_obs]).max())
best_af_obs = int(np.unravel_index(np.argmax(z_af_obs), z_af_obs.shape)[0]); adj_obs = abs(LAGS_EQ[best_eq_obs] - LAGS_AF[best_af_obs]) == 1
m1 = z_eq_null.max(1); m2 = z_af_null.reshape(NREP, -1).max(1); best_eq = z_eq_null.argmax(1)
m3 = np.array([rune_z(RC[r, best_eq[r]]).max() for r in range(NREP)]); best_af = np.array([np.unravel_index(np.argmax(z_af_null[r]), z_af_null[r].shape)[0] for r in range(NREP)])
adj = np.abs(np.array(LAGS_EQ)[best_eq] - np.array(LAGS_AF)[best_af]) == 1
p1 = float((np.sum(m1 >= m1_obs) + 1) / (NREP + 1)); p2 = float((np.sum(m2 >= m2_obs) + 1) / (NREP + 1)); p3 = float((np.sum(m3 >= m3_obs) + 1) / (NREP + 1))
joint = (m1 >= m1_obs) & (m2 >= m2_obs) & (m3 >= m3_obs); pj = float(joint.mean()); pja = float((joint & adj).mean()); padj = float(adj.mean())
# end anchoring
sh5_obs = obs[3][0] / obs[3][1]; sh6_obs = obs[4][0] / obs[4][1]; sh5 = E5[:, 0] / np.maximum(E5[:, 1], 1); sh6 = H6[:, 0] / np.maximum(H6[:, 1], 1)
b5 = (float(np.percentile(sh5, 2.5)), float(np.percentile(sh5, 97.5))); b6 = (float(np.percentile(sh6, 2.5)), float(np.percentile(sh6, 97.5)))
pe5 = float((np.sum(sh5 >= sh5_obs) + 1) / (NREP + 1)); pe6 = float((np.sum(sh6 >= sh6_obs) + 1) / (NREP + 1))
# descriptive: end-distance distribution of the observed sites
dist5, dist6 = [], []
for k, (c, w) in enumerate(U):
    L = len(c); d = ENDD[k]
    i = np.arange(5, L); e = (w[i] == w[i - 5]) & (c[i] == c[i - 5]); dist5 += d[i[e]].tolist()
    i = np.arange(6, L); m = (w[i] == w[i - 6]); h = m & (c[i] == (24 - 2 * c[i - 6]) % N); dist6 += d[i[h]].tolist()
hist = lambda v: [int(sum(1 for x in v if x == t)) for t in range(4)] + [int(sum(1 for x in v if x >= 4))]

o = ["# Quorum's ask: the joint discovery replay and the word-end anchoring check", "",
     f"Registration: `results/discovery_replay_registration.md`. 55 pages; K-fixed null {NREP} arrangements per page (seed 1034, burn-in {BURN}, thinning {THIN}); every scan recomputed inside every arrangement; each cell standardized by its own null mean and sd.", "",
     "## R. The replay", "", "| scan | cells | observed winner | observed max z | family-wise p over the scan |", "|---|---|---|---|---|",
     f"| (i) within-word equality, lags 2–12 | 11 | lag {LAGS_EQ[best_eq_obs]} ({obs[0][best_eq_obs]} against {mu_eq[best_eq_obs]:.1f} ± {sd_eq[best_eq_obs]:.1f}) | {m1_obs:.2f} | {p1:.3f} |",
     f"| (ii) affine maps a·c′ + b, lags 2–8 | 5,684 | lag {LAGS_AF[best_af_obs]}, map a = {int(np.unravel_index(np.argmax(z_af_obs), z_af_obs.shape)[1]) // N + 1}, b = {int(np.unravel_index(np.argmax(z_af_obs), z_af_obs.shape)[1]) % N} | {m2_obs:.2f} | {p2:.3f} |",
     f"| (iii) rune concentration at the winning equality lag's sites | 29 | {LATIN[int(np.argmax(rune_z(obs[2][best_eq_obs])))]} ({int(obs[2][best_eq_obs].max())} of {int(obs[2][best_eq_obs].sum())}) | {m3_obs:.2f} | {p3:.3f} |", "",
     f"Joint: arrangements with all three maxima at least the observed: **{int(joint.sum())} of {NREP}** (share {pj:.4f}); with the winning lags of (i) and (ii) adjacent as well: **{int((joint & adj).sum())}** (share {pja:.4f}); the winning lags are adjacent in {padj:.3f} of arrangements regardless. Observed winners adjacent: {'yes' if adj_obs else 'no'}. Null maxima: scan (i) median {np.median(m1):.2f}, 99th percentile {np.percentile(m1, 99):.2f}; scan (ii) median {np.median(m2):.2f}, 99th {np.percentile(m2, 99):.2f}; scan (iii) median {np.median(m3):.2f}, 99th {np.percentile(m3, 99):.2f}.", "",
     "## E. Word-end anchoring", "", "| echo | sites | later rune at distance 0 or 1 from the word's end | null share, central 95 % | one-sided p (excess) | distance histogram 0, 1, 2, 3, ≥4 |", "|---|---|---|---|---|---|",
     f"| lag-5 equality | {obs[3][1]} | {obs[3][0]} ({sh5_obs:.3f}) | {b5[0]:.3f}–{b5[1]:.3f} | {pe5:.3f} | {hist(dist5)} |",
     f"| lag-6 affine hit | {obs[4][1]} | {obs[4][0]} ({sh6_obs:.3f}) | {b6[0]:.3f}–{b6[1]:.3f} | {pe6:.3f} | {hist(dist6)} |", "",
     "## Registered predictions", "",
     f"- R1 (scan (i) family-wise p < 0.05): {p1:.3f} → {'holds' if p1 < 0.05 else 'fails'}.", f"- R2 (scan (ii) family-wise p < 0.05): {p2:.3f} → {'holds' if p2 < 0.05 else 'fails'}.",
     f"- R3 (scan (iii) family-wise p < 0.05): {p3:.3f} → {'holds' if p3 < 0.05 else 'fails'}.",
     f"- R4 (joint share < 0.005; joint-and-adjacent share < 0.002): {pj:.4f}, {pja:.4f} → {'holds' if pj < 0.005 and pja < 0.002 else 'fails'}.",
     f"- E1 (lag-6 final-or-penultimate share inside the null's 95 %): {sh6_obs:.3f} in {b6[0]:.3f}–{b6[1]:.3f} → {'holds' if b6[0] <= sh6_obs <= b6[1] else 'fails'}.",
     f"- E2 (lag-5 likewise): {sh5_obs:.3f} in {b5[0]:.3f}–{b5[1]:.3f} → {'holds' if b5[0] <= sh5_obs <= b5[1] else 'fails'}.", "",
     f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/discovery_replay.py`.", ""]
(RESULTS / "discovery_replay.md").write_text("\n".join(o)); print("\n".join(o))
json.dump(dict(m_obs=[m1_obs, m2_obs, m3_obs], p=[p1, p2, p3], joint=pj, joint_adj=pja, adj=padj, m1=m1.tolist(), m2=m2.tolist(), m3=m3.tolist(), end5=[sh5_obs, b5, pe5], end6=[sh6_obs, b6, pe6], dist5=dist5, dist6=dist6), open(RESULTS / "discovery_replay.json", "w"), indent=1)
