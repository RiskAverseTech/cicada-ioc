"""G: the echo gate as a property of the word (registration: results/clue_table_registration.md, commit a0b5915).

For every word of the 55 pages long enough to host a within-word lag-5 equality (six runes or more) or a lag-6 affine hit
24 - 2c (seven or more), ten word properties against site-carrying, each a chi-square stratified by exact word length and summed
over strata; the null permutes the site labels within each length stratum (2,000 permutations); the family-wise level is the
permutation distribution of the largest statistic over the ten properties.  Power: synthetic site labels on the real words with
the per-length counts kept and one property (first rune at or above S) raising the odds of a site by 2 or 3, 200 draws each.
Reproduce: .venv/bin/python -I src/gate_property.py
"""
import sys, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, IDX, N, primes

t0 = time.time(); rng = np.random.default_rng(2026); NPERM = 2000; NPOW = 200; NPERM_POW = 400
VALUE = np.array(primes(N)); S_IDX = 15; VOWELS = {1, 3, 10, 12, 18, 24, 25, 26, 27, 28}      # U O I EO E A AE Y IA EA (§74's class 0)
SEP = set('-.&$§')


def parse(s):
    """runes with word id and line id; a '/' ends a line, and the word continues across it unless a separator precedes"""
    runes, wid, lid = [], [], []; w = 0; l = 0; pending = False
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False
            runes.append(IDX[ch]); wid.append(w); lid.append(l)
        elif ch in SEP: pending = True
        elif ch == "/": l += 1
    return np.array(runes), np.array(wid), np.array(lid)


chunks = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8").split("%")
pages = [parse(chunks[k]) for k in range(16, 72)]; pages = [p for p in pages if len(p[0])]; assert len(pages) == 55

words = []                                                          # one record per word
for k, (r, w, l) in enumerate(pages):
    nw = w.max() + 1; line_first = {}; line_last = {}
    for i in range(len(r)): line_first.setdefault(l[i], i); line_last[l[i]] = i
    for m in range(nw):
        idx = np.flatnonzero(w == m); x = r[idx]; L = len(x)
        if L == 0: continue                                            # a page that opens with a separator leaves word id 0 empty
        s5 = any(x[i] == x[i - 5] for i in range(5, L)); s6 = any(x[i] == (24 - 2 * x[i - 6]) % N for i in range(6, L))
        starts = idx[0] in line_first.values(); ends = idx[-1] in line_last.values(); crosses = l[idx[0]] != l[idx[-1]]
        g = int(VALUE[x].sum())
        words.append(dict(page=k, m=m, L=L, s5=s5, s6=s6,
                          P=[int(x[0] in VOWELS), int(x[0] >= S_IDX), int(x[-1] in VOWELS), g % 2, g % 3, int(x.sum() % N < 15), m % 2,
                             1 if starts else (2 if ends else 0), int(crosses), int(k >= 28)]))
PROPS = ["first rune a vowel", "first rune at or above S", "last rune a vowel", "Gematria sum even", "Gematria sum mod 3", "index sum mod 29 below 15",
         "word index even", "starts / ends a line", "crosses a line end", "second half of the section"]
NV = [2, 2, 2, 2, 3, 2, 2, 3, 2, 2]


def table(sel, site_key):
    ws = [x for x in words if sel(x)]; L = np.array([x["L"] for x in ws]); site = np.array([x[site_key] if isinstance(site_key, str) else site_key(x) for x in ws], int)
    P = np.array([x["P"] for x in ws]); strata = np.unique(L); sid = np.searchsorted(strata, L)
    return L, sid, len(strata), site, P


def stats(sid, nstr, site, P):
    """chi-square per property, stratified by exact length and summed; strata with no sites or all sites contribute 0"""
    out = np.zeros(len(PROPS))
    for j in range(len(PROPS)):
        nv = NV[j]; code = (sid * nv + P[:, j]) * 2 + site; cnt = np.bincount(code, minlength=nstr * nv * 2).reshape(nstr, nv, 2).astype(float)
        row = cnt.sum(2, keepdims=True); col = cnt.sum(1, keepdims=True); tot = cnt.sum((1, 2), keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            E = row * col / tot; chi = np.where(E > 0, (cnt - E) ** 2 / E, 0.0)
        out[j] = chi.sum()
    return out


def permute_within(sid, site, nstr, rng):
    s = site.copy()
    for k in range(nstr):
        ix = np.flatnonzero(sid == k)
        if len(ix) > 1: s[ix] = s[rng.permutation(ix)]
    return s


def test(sel, site_key, nperm, rng):
    L, sid, nstr, site, P = table(sel, site_key); obs = stats(sid, nstr, site, P)
    perm = np.array([stats(sid, nstr, permute_within(sid, site, nstr, rng), P) for _ in range(nperm)])
    p = (perm >= obs[None, :]).mean(0); fw = (perm.max(1)[:, None] >= obs[None, :]).mean(0)
    return dict(n=len(L), sites=int(site.sum()), obs=obs, p=p, fw=fw, sid=sid, nstr=nstr, site=site, P=P)


def power(sel, site_key, OR, ndraw, nperm, rng, driver=1):
    """synthetic labels: per stratum the same number of sites, drawn without replacement with weight OR where the driver property is 1"""
    L, sid, nstr, site, P = table(sel, site_key); hits = 0
    for _ in range(ndraw):
        syn = np.zeros_like(site)
        for k in range(nstr):
            ix = np.flatnonzero(sid == k); ns = int(site[ix].sum())
            if ns == 0 or ns >= len(ix): syn[ix] = site[ix]; continue
            wgt = np.where(P[ix, driver] == 1, OR, 1.0); wgt = wgt / wgt.sum(); syn[ix[rng.choice(len(ix), size=ns, replace=False, p=wgt)]] = 1
        obs = stats(sid, nstr, syn, P); perm = np.array([stats(sid, nstr, permute_within(sid, syn, nstr, rng), P) for _ in range(nperm)])
        hits += int((perm.max(1) >= obs.max()).mean() < 0.05)
    return hits / ndraw


res = {"lag-5": test(lambda x: x["L"] >= 6, "s5", NPERM, rng), "lag-6": test(lambda x: x["L"] >= 7, "s6", NPERM, rng),
       "pooled": test(lambda x: x["L"] >= 6, lambda x: int(x["s5"] or x["s6"]), NPERM, rng)}
print("tests done", f"[{time.time()-t0:.0f}s]", flush=True)
pw = {OR: power(lambda x: x["L"] >= 6, lambda x: int(x["s5"] or x["s6"]), OR, NPOW, NPERM_POW, rng) for OR in (2.0, 3.0)}
print("power done", pw, f"[{time.time()-t0:.0f}s]", flush=True)

o = ["# G. The echo gate as a property of the word", "",
     f"Registration: `results/clue_table_registration.md` (G). Words of six runes or more: {res['lag-5']['n']} ({res['lag-5']['sites']} carry a lag-5 equality site); of seven or more: {res['lag-6']['n']} ({res['lag-6']['sites']} carry a lag-6 affine site); pooled (either site, six or more): {res['pooled']['sites']} of {res['pooled']['n']}. Chi-square stratified by exact word length, summed; null {NPERM} permutations of the site labels within each length stratum; family-wise p from the largest statistic over the ten properties.", "",
     "| property | lag-5 χ² | p | family-wise p | lag-6 χ² | p | family-wise p | pooled χ² | p | family-wise p |", "|---|---|---|---|---|---|---|---|---|---|"]
for j, name in enumerate(PROPS):
    o.append(f"| {name} | " + " | ".join(f"{res[k]['obs'][j]:.1f} | {res[k]['p'][j]:.3f} | {res[k]['fw'][j]:.3f}" for k in ("lag-5", "lag-6", "pooled")) + " |")
o += ["", f"Power (synthetic sites on the real words, per-length counts kept, the property \"first rune at or above S\" raising the odds of a site; {NPOW} draws, {NPERM_POW} permutations each; share of draws with family-wise p < 0.05): odds ratio 2: **{pw[2.0]:.2f}**; odds ratio 3: **{pw[3.0]:.2f}**.", "",
      "## Registered predictions", "",
      f"- G1 (no property at family-wise p < 0.05 for either echo or pooled): smallest family-wise p {min(min(res[k]['fw']) for k in res):.3f} → {'holds' if min(min(res[k]['fw']) for k in res) >= 0.05 else 'fails'}.",
      f"- G2 (power at odds ratio 3 at least 0.8): {pw[3.0]:.2f} → {'holds' if pw[3.0] >= 0.8 else 'fails'}.", "",
      f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/gate_property.py`.", ""]
(RESULTS / "gate_property.md").write_text("\n".join(o)); print("\n".join(o))
json.dump({k: dict(n=v["n"], sites=v["sites"], obs=v["obs"].tolist(), p=v["p"].tolist(), fw=v["fw"].tolist()) for k, v in res.items()} | {"power": pw, "props": PROPS}, open(RESULTS / "gate_property.json", "w"), indent=1)
