"""An audit of the two foreground facts (registration: results/foreground_audit_registration.md, commit c52125f).

The 102 within-word lag-5 equalities with their eleven S pairs, and the 77 within-word lag-6 hits of c = 24 - 2c', re-measured
under §42's K-fixed null and under a word-preserving shuffle; leave-one-page-out z for both facts; concentration of the lag-6
hits by (earlier, later) pair and through the fixed point H; concentration of the lag-5 equalities by rune value, page and
word; the words that carry sites and how often their forms repeat; the eleven S pairs listed in full.
Reproduce: .venv/bin/python -I src/foreground_audit.py
"""
import sys, time, json, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import IDX, RAW, RESULTS, N, LATIN, to_latin
from kfixed import kfixed_step, doublets

t0 = time.time(); rng = np.random.default_rng(1034); NREP, BURN, THIN = 999, 20, 4; S = LATIN.index("S"); H_IDX = LATIN.index("H")
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


def sites(c, w):
    """lag-5 equal pair positions (later index) and lag-6 hit positions (later index) inside words"""
    L = len(c); i5 = np.arange(5, L); e5 = i5[(w[i5] == w[i5 - 5]) & (c[i5] == c[i5 - 5])]
    i6 = np.arange(6, L); h6 = i6[(w[i6] == w[i6 - 6]) & (c[i6] == (24 - 2 * c[i6 - 6]) % N)]
    return e5, h6


def per_page(pages):
    """per page: e5 count, S..S count, h6 count; pooled: lag-6 pair histogram, lag-5 value histogram"""
    e5c, ssc, h6c = np.zeros(len(pages), int), np.zeros(len(pages), int), np.zeros(len(pages), int)
    pair6 = collections.Counter(); val5 = collections.Counter()
    for k, (c, w) in enumerate(pages):
        e5, h6 = sites(c, w); e5c[k] = len(e5); ssc[k] = int((c[e5] == S).sum()); h6c[k] = len(h6)
        pair6.update(zip(c[h6 - 6].tolist(), c[h6].tolist())); val5.update(c[e5].tolist())
    return e5c, ssc, h6c, pair6, val5


def conc(pair6, val5):
    n6 = sum(pair6.values()); n5 = sum(val5.values())
    return dict(max6=(max(pair6.values()) / n6 if n6 else 0.0), dist6=(len(pair6) / n6 if n6 else 0.0), hh=(pair6[(H_IDX, H_IDX)] / n6 if n6 else 0.0),
                max5=(max(val5.values()) / n5 if n5 else 0.0), dist5=(len(val5) / n5 if n5 else 0.0))


# ---------- observed
e5o, sso, h6o, pair6o, val5o = per_page(U); co = conc(pair6o, val5o)
log("observed: lag-5 equal", e5o.sum(), "S..S", sso.sum(), "lag-6 hits", h6o.sum(), "distinct lag-6 pairs", len(pair6o), "max pair", pair6o.most_common(1))

# ---------- K-fixed null, per page samples
cur = [(c.copy(), w) for c, w in U]; ks = [doublets(c) for c, _ in U]
for c, _ in cur: kfixed_step(c, BURN * len(c), rng)
K5, KS, K6 = np.zeros((NREP, 55), int), np.zeros((NREP, 55), int), np.zeros((NREP, 55), int); KC = []
for r in range(NREP):
    for c, _ in cur: kfixed_step(c, THIN * len(c), rng)
    a, b, d, p6, v5 = per_page(cur); K5[r], KS[r], K6[r] = a, b, d; KC.append(conc(p6, v5))
    if (r + 1) % 100 == 0: log("K-fixed rep", r + 1)
assert all(doublets(c) == k for (c, _), k in zip(cur, ks))

# ---------- word-preserving shuffle null
P5, PS, P6 = np.zeros((NREP, 55), int), np.zeros((NREP, 55), int), np.zeros((NREP, 55), int)
for r in range(NREP):
    sh = [(rng.permutation(c), w) for c, w in U]; a, b, d, _, _ = per_page(sh); P5[r], PS[r], P6[r] = a, b, d
log("shuffle null done")


def zp(obs, samp):
    mu, sd = samp.mean(), samp.std(); return float((obs - mu) / sd), float(mu), float(sd), float((np.sum(samp >= obs) + 1) / (len(samp) + 1))


def loo(obs_pp, samp_pp):
    full = zp(obs_pp.sum(), samp_pp.sum(1)); zs = []
    for k in range(55):
        m = np.ones(55, bool); m[k] = False; zs.append(zp(obs_pp[m].sum(), samp_pp[:, m].sum(1))[0])
    contrib = obs_pp - samp_pp.mean(0); excess = contrib.sum()
    top = sorted(range(55), key=lambda k: -contrib[k])[:5]
    return dict(full=full, loo_min=min(zs), loo_max=max(zs), top=[(f"LP2-{k:02d}", int(obs_pp[k]), round(float(samp_pp[:, k].mean()), 1), round(float(contrib[k] / excess), 2) if excess else None) for k in top], max_share=max(contrib) / excess if excess else None)


R = {"lag-5 equal (K-fixed)": loo(e5o, K5), "S..S (K-fixed)": loo(sso, KS), "lag-6 hits (K-fixed)": loo(h6o, K6),
     "lag-5 equal (shuffle)": loo(e5o, P5), "S..S (shuffle)": loo(sso, PS), "lag-6 hits (shuffle)": loo(h6o, P6)}

# ---------- concentration against the K-fixed null's own hits
def band(key, lo=2.5, hi=97.5):
    v = np.array([k[key] for k in KC]); return float(np.percentile(v, lo)), float(np.percentile(v, hi)), float((np.sum(v >= co[key]) + 1) / (NREP + 1))


# ---------- words that carry sites, word forms, the eleven S pairs
site_words = []; forms_all = collections.Counter()
for k, (c, w) in enumerate(U):
    nw = w.max() + 1; wordforms = {m: tuple(c[w == m].tolist()) for m in range(nw) if (w == m).any()}; forms_all.update(wordforms.values())
    e5, h6 = sites(c, w)
    for i in e5: site_words.append(dict(page=k, word=int(w[i]), kind="lag-5", value=int(c[i]), pos=int(i - np.flatnonzero(w == w[i])[0]), form=wordforms[int(w[i])]))
    for i in h6: site_words.append(dict(page=k, word=int(w[i]), kind="lag-6", value=int(c[i]), pos=int(i - np.flatnonzero(w == w[i])[0]), form=wordforms[int(w[i])]))
form_sites = collections.Counter(s["form"] for s in site_words); max_form_sites = max(form_sites.values())
# a site word's form "recurs" when the same rune string occurs as another word anywhere on the 55 pages (the first run counted a
# word's own second site as a recurrence, a bug caught in the reading and corrected before anything was written)
site_distinct = {(s["page"], s["word"]): s["form"] for s in site_words}; site_forms = list(site_distinct.values())
rep_share = float(np.mean([forms_all[f] >= 2 for f in site_forms]))
all_words = [f for f, n in forms_all.items() for _ in range(n)]; by_len = collections.defaultdict(list)
for f in all_words: by_len[len(f)].append(f)
base = []
for _ in range(200):
    drawn = [by_len[len(f)][rng.integers(len(by_len[len(f)]))] for f in site_forms]; base.append(np.mean([forms_all[f] >= 2 for f in drawn]))
occ6 = 29 * (1 - (28 / 29) ** int(h6o.sum()))                                   # distinct pairs expected if 77 hits fell uniformly on the map's 29 pairs
big_word = max(form_sites, key=form_sites.get); bw_sites = [s for s in site_words if s["form"] == big_word]
e5_wo = int(e5o.sum()) - sum(1 for s in bw_sites if s["kind"] == "lag-5"); h6_wo = int(h6o.sum()) - sum(1 for s in bw_sites if s["kind"] == "lag-6"); ss_wo = int(sso.sum()) - sum(1 for s in bw_sites if s["kind"] == "lag-5" and s["value"] == S)
z_wo = (zp(e5_wo, K5.sum(1))[0], zp(ss_wo, KS.sum(1))[0], zp(h6_wo, K6.sum(1))[0])
s_pairs = [s for s in site_words if s["kind"] == "lag-5" and s["value"] == S]
s_forms = {s["form"] for s in s_pairs}; s_pages = {s["page"] for s in s_pairs}

# ---------- report
o = ["# An audit of the two foreground facts", "",
     f"Registration: `results/foreground_audit_registration.md`. 55 pages, within-word pairs; K-fixed null {NREP} arrangements per page (burn-in {BURN}, thinning {THIN} attempted transpositions per rune, seed 1034); word-preserving shuffle {NREP} per page.", "",
     "## 1. Reproduction and 7. the second null", "", "| fact | observed | K-fixed mean ± sd | z | p | shuffle mean ± sd | z | p |", "|---|---|---|---|---|---|---|---|"]
for nm, a, b in (("lag-5 equalities", "lag-5 equal (K-fixed)", "lag-5 equal (shuffle)"), ("S..S pairs", "S..S (K-fixed)", "S..S (shuffle)"), ("lag-6 hits of 24 − 2c", "lag-6 hits (K-fixed)", "lag-6 hits (shuffle)")):
    fa, fb = R[a]["full"], R[b]["full"]; obs = {"lag-5 equalities": e5o.sum(), "S..S pairs": sso.sum(), "lag-6 hits of 24 − 2c": h6o.sum()}[nm]
    o.append(f"| {nm} | {obs} | {fa[1]:.1f} ± {fa[2]:.1f} | {fa[0]:+.2f} | {fa[3]:.3f} | {fb[1]:.1f} ± {fb[2]:.1f} | {fb[0]:+.2f} | {fb[3]:.3f} |")
o += ["", "## 2. Leave one page out", "", "| fact (null) | full z | smallest z over the 55 leaves | largest | largest single-page share of the excess | top contributing pages (observed, null mean, share) |", "|---|---|---|---|---|---|"]
for nm, r in R.items(): o.append(f"| {nm} | {r['full'][0]:+.2f} | {r['loo_min']:+.2f} | {r['loo_max']:+.2f} | {r['max_share']:.2f} | " + "; ".join(f"{p} ({a}, {b}, {s})" for p, a, b, s in r["top"]) + " |")
b6, d6, hh = band("max6"), band("dist6"), band("hh")
o += ["", "## 3. Concentration at lag 6", "", f"77 hits in **{len(pair6o)}** distinct (earlier, later) pairs. Largest pair: {', '.join(f'{LATIN[a]}→{LATIN[b]} ({n})' for (a, b), n in pair6o.most_common(5))}.",
      f"Largest pair's share {co['max6']:.3f} (K-fixed null among its own hits: central 95 % {b6[0]:.3f}–{b6[1]:.3f}; p(≥) {b6[2]:.3f}); distinct pairs / hits {co['dist6']:.3f} (null {d6[0]:.3f}–{d6[1]:.3f}, a ratio that falls as hits rise because the map has only 29 pairs: {h6o.sum()} hits falling uniformly on 29 pairs would occupy {occ6:.1f} distinct pairs, and they occupy {len(pair6o)}); share through the fixed point H→H {co['hh']:.3f} (null {hh[0]:.3f}–{hh[1]:.3f}, p {hh[2]:.3f}).", ""]
b5, d5 = band("max5"), band("dist5")
o += ["## 4. Concentration at lag 5", "", f"102 equalities over **{len(val5o)}** rune values; largest: {', '.join(f'{LATIN[v]} ({n})' for v, n in val5o.most_common(6))}. Largest value's share {co['max5']:.3f} (null {b5[0]:.3f}–{b5[1]:.3f}; p {b5[2]:.3f}); distinct values / equalities {co['dist5']:.3f} (null {d5[0]:.3f}–{d5[1]:.3f}).",
      f"By page: {int((e5o > 0).sum())} of 55 pages carry a lag-5 equality (largest page {int(e5o.max())}); {int((h6o > 0).sum())} carry a lag-6 hit (largest {int(h6o.max())}).", "",
      "## 5. The words that carry sites", "", f"{len(site_words)} sites in {len(site_distinct)} words. Largest number of sites in one word: **{max_form_sites}** ({to_latin(big_word)}, LP2-{bw_sites[0]['page']:02d}: {sum(1 for s in bw_sites if s['kind'] == 'lag-5')} lag-5 equalities, {sum(1 for s in bw_sites if s['kind'] == 'lag-6')} lag-6 hit; it is the lag-5 trigram run of §46). Without that one word the three facts stand at z {z_wo[0]:+.2f}, {z_wo[1]:+.2f}, {z_wo[2]:+.2f}. Share of site words whose exact rune string occurs as another word anywhere on the pages: **{rep_share:.3f}** (words of the same lengths drawn at random from the pages: {np.mean(base):.3f} ± {np.std(base):.3f}).", "",
      "Word forms carrying two or more sites: " + (", ".join(f"{to_latin(f)} ({n})" for f, n in form_sites.most_common() if n >= 2) or "none") + ".", "",
      "## 6. The eleven S pairs", "", "| page | word | position of the later S | word (Latin) | form recurs among site words |", "|---|---|---|---|---|"]
for s in s_pairs: o.append(f"| LP2-{s['page']:02d} | {s['word']} | {s['pos']} | {to_latin(s['form'])} | {'yes' if site_forms.count(s['form']) > 1 else 'no'} |")
o += ["", f"{len(s_pairs)} S pairs in {len(s_forms)} distinct word forms on {len(s_pages)} pages.", "", "## Registered predictions", ""]
f1 = all(abs(r["loo_min"] - r["full"][0]) <= 1.0 and abs(r["loo_max"] - r["full"][0]) <= 1.0 and r["max_share"] <= 0.2 for k, r in R.items() if "K-fixed" in k and "S..S" not in k)
o.append(f"- F1 (every leave-one-out z within 1.0 of the full z; no page over a fifth of the excess; the two facts under K-fixed): → {'holds' if f1 else 'fails'}.")
f2 = co["max6"] < 0.15 and co["dist6"] >= 0.45 and hh[0] <= co["hh"] <= hh[1]
o.append(f"- F2 (largest lag-6 pair under 15 %; distinct pairs ≥ 45 % of hits; H→H inside the null's 95 %): {co['max6']:.3f}, {co['dist6']:.3f}, {co['hh']:.3f} → {'holds' if f2 else 'fails'}.")
f3 = max_form_sites <= 3 and rep_share < 0.15
o.append(f"- F3 (no word form with more than three sites; under 15 % of site words repeat a form): {max_form_sites}, {rep_share:.3f} → {'holds' if f3 else 'fails'}.")
f4 = len(s_forms) >= 8 and len(s_pages) >= 6
o.append(f"- F4 (the S pairs in ≥ 8 forms on ≥ 6 pages): {len(s_forms)} forms, {len(s_pages)} pages → {'holds' if f4 else 'fails'}.")
f5 = R["lag-5 equal (shuffle)"]["full"][0] >= 3 and R["lag-6 hits (shuffle)"]["full"][0] >= 3
o.append(f"- F5 (both facts at z ≥ 3 under the word-preserving shuffle): {R['lag-5 equal (shuffle)']['full'][0]:+.2f}, {R['lag-6 hits (shuffle)']['full'][0]:+.2f} → {'holds' if f5 else 'fails'}.")
o += ["", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/foreground_audit.py`.", ""]
(RESULTS / "foreground_audit.md").write_text("\n".join(o)); print("\n".join(o))
json.dump(dict(R={k: dict(full=v["full"], loo_min=v["loo_min"], loo_max=v["loo_max"], top=v["top"], max_share=v["max_share"]) for k, v in R.items()}, conc=co, pair6=[[list(k), n] for k, n in pair6o.most_common()], val5=val5o.most_common(),
               s_pairs=[dict(page=s["page"], word=s["word"], pos=s["pos"], form=to_latin(s["form"])) for s in s_pairs], max_form_sites=max_form_sites, rep_share=float(rep_share), base=[float(np.mean(base)), float(np.std(base))]),
          open(RESULTS / "foreground_audit.json", "w"), indent=1)
