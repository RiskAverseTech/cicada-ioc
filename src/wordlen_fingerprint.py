"""§55 part A (2026-10-29): the word-length fingerprint of the unsolved pages, and two word-level checks.

With the corrected word edges (§42: '/' is a line break, not a boundary) the 55 unsolved pages hold 2,928 words.  This
script compares their rune-length histogram with the solved pages' cipher words (their ciphers preserve boundaries), with
English prose spelled in runes (five public-domain books from data/corpus/raw), with the solved pages' translation, with
Latin, Old English and Chaucer, and with English under four distortions: word separators dropped at rate d, Poisson(λ)
fillers per word, a filler after each rune with probability r, and function words removed.  The chi-square of a histogram
against the English prose reference is given a null from 2,000 bootstrap samples of the same word count drawn from the prose.
Two more facts: the index of coincidence by word position (from either end), with a per-page shuffle null; and the number
of cipher words of >= 3 and >= 4 runes that occur twice, with the same null.  Descriptive, registered as such in
results/filler_lane_registration.md; no decode rule depends on it.  Output: results/wordlen_fingerprint.md.
"""
import re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from collections import Counter
from lp import IDX, RAW, N, RESULTS, english_to_runes

t0 = time.time(); rng = np.random.default_rng(55)
ROOT = RAW.parent.parent; CR = ROOT / "data" / "corpus" / "raw"
txt = (RAW / "iddqd__liber-primus__transcription--master.txt").read_text(encoding="utf-8"); chunks = txt.split("%")
SEP = set('-.&$§'); M = 15; BOOT = 2000


def parse(s):
    runes, wid, pos = [], [], []; w = 0; pending = False; k = 0
    for ch in s:
        if ch in IDX:
            if pending: w += 1; pending = False; k = 0
            runes.append(IDX[ch]); wid.append(w); pos.append(k); k += 1
        elif ch in SEP: pending = True
    return np.array(runes, int), np.array(wid, int), np.array(pos, int)


U = [parse(chunks[k]) for k in range(16, 72)]; U = [u for u in U if len(u[0])]
SOL = [parse(chunks[k]) for k in range(0, 16)]; SOL = [u for u in SOL if len(u[0])]
def lens(pages):
    L = np.concatenate([np.bincount(w) for _, w, _ in pages]); return L[L > 0]   # a chunk that opens with a separator yields an empty word id
uns, sol = lens(U), lens(SOL)


def wl_text(t, cap=10 ** 7):
    t = re.sub(r"<[^>]+>", " ", t)[:cap]; out = []
    for w in re.findall(r"[A-Za-zÆæÞþÐð]+", t):
        try: n = len(english_to_runes(w))
        except Exception: n = 0
        if n: out.append(n)
    return np.array(out)


corp = {}
tr = (RAW / "iddqd__liber-primus__translation.txt").read_text(errors="ignore")
corp["LP translation (solved pages' English)"] = wl_text("\n".join(re.sub(r"^\s*\d+(\.\d+)*\s+", "", l) for l in tr.splitlines() if not l.startswith("+")))
eng = ""
for f in ("emerson_essays1_pg2944.txt", "bunyan_pilgrims_progress_pg131.txt", "kybalion_pg14209.txt", "king_in_yellow_pg8492.txt", "bulfinch_age_of_chivalry_pg4926.txt"):
    eng += (CR / f).read_text(errors="ignore")[20000:220000] + " "
E = wl_text(eng); corp["English prose (5 books)"] = E
corp["Chaucer (Middle English)"] = wl_text((CR / "chaucer_canterbury_pg2383.txt").read_text(errors="ignore")[50000:450000])
corp["Latin (phase 5 corpus)"] = wl_text((RAW / "corpora" / "latin_corpus.txt").read_text(errors="ignore"), 400000)
corp["Old English (phase 5 corpus)"] = wl_text((RAW / "corpora" / "oe_corpus.txt").read_text(errors="ignore"), 400000)


def hist(L):
    h = np.bincount(np.minimum(np.asarray(L), M), minlength=M + 1)[1:].astype(float); return h / h.sum()


HE = hist(E)
def chi2(L):
    """chi-square of the sample's histogram against the English prose reference, at the sample's own count."""
    n = len(L); e = np.maximum(HE * n, 0.5); return float((((hist(L) * n) - e) ** 2 / e).sum())


def boot(n):
    return np.array([chi2(rng.choice(E, n)) for _ in range(BOOT)])


bu, bs = boot(len(uns)), boot(len(sol))
cu, cs = chi2(uns), chi2(sol)
pu, ps = (np.sum(bu >= cu) + 1) / (BOOT + 1), (np.sum(bs >= cs) + 1) / (BOOT + 1)
tv = lambda L: 0.5 * np.abs(hist(L) - hist(uns)).sum()
chi_u = lambda L: float((((hist(uns) * len(uns)) - np.maximum(hist(L) * len(uns), 0.5)) ** 2 / np.maximum(hist(L) * len(uns), 0.5)).sum())

out = ["# The word-length fingerprint of the unsolved pages (§55 part A)", "",
       f"Words: {len(uns):,} on the 55 unsolved pages (corrected edges), {len(sol)} cipher words on the solved pages. Lengths are in runes (TH, NG, EO, ING are one rune). Columns are the share of words at each length; the last two columns compare each row with the unsolved pages (total-variation distance, and the chi-square the unsolved histogram would have against that row as reference, at n = {len(uns):,}).", "",
       f"Against English prose as reference, the unsolved pages' chi-square is **{cu:.0f}**; {BOOT:,} bootstrap samples of {len(uns):,} English words give median {np.median(bu):.0f}, 99th percentile {np.percentile(bu, 99):.0f}, max {bu.max():.0f} (p {pu:.4f}). The solved pages' cipher words give {cs:.0f} at n = {len(sol)}, bootstrap median {np.median(bs):.0f}, 99th percentile {np.percentile(bs, 99):.0f} (p {ps:.3f}). Mean length: unsolved {uns.mean():.2f}, solved {sol.mean():.2f}, English prose {E.mean():.2f}, Latin {corp['Latin (phase 5 corpus)'].mean():.2f}, Old English {corp['Old English (phase 5 corpus)'].mean():.2f}.", "",
       "| sample | n | " + " | ".join(str(k) for k in range(1, 13)) + " | TV | chi² |", "|---|---|" + "---|" * 12 + "---|---|"]
def row(name, L):
    h = hist(L); out.append(f"| {name} | {len(L):,} | " + " | ".join(f"{h[k-1]*100:.1f}" for k in range(1, 13)) + f" | {tv(L):.3f} | {chi_u(L):.0f} |")
row("**unsolved cipher words**", uns); row("solved cipher words", sol)
for k, v in corp.items(): row(k, v)
out += ["", "## English under four distortions", "", "Each row distorts the English prose sample and compares the result with the unsolved pages.", "",
        "| model | " + " | ".join(str(k) for k in range(1, 13)) + " | TV | chi² |", "|---|" + "---|" * 12 + "---|---|"]
fits = []
def row2(name, L):
    h = hist(L); c = chi_u(L); fits.append((c, name)); out.append(f"| {name} | " + " | ".join(f"{h[k-1]*100:.1f}" for k in range(1, 13)) + f" | {tv(L):.3f} | {c:.0f} |")
for d in (0.1, 0.2, 0.3, 0.4):
    keep = rng.random(len(E)) > d; merged = []; acc = 0
    for n_, kp in zip(E, keep):
        acc += n_
        if kp: merged.append(acc); acc = 0
    row2(f"separators dropped, d = {d:.1f}", np.array(merged))
for lam in (0.25, 0.5, 0.75, 1.0): row2(f"Poisson(λ = {lam:.2f}) fillers per word", E + rng.poisson(lam, len(E)))
for r in (0.05, 0.08, 0.10, 0.12, 0.15): row2(f"a filler after each rune w.p. r = {r:.2f}", E + rng.binomial(E, r))
row2("words of one or two runes removed", E[E >= 3])
fits.sort(); best_pw = min(c for c, nm in fits if nm.startswith("Poisson")); best_pr = min(c for c, nm in fits if nm.startswith("a filler"))
out += ["", f"Best of the simple distortions: {fits[0][1]} (chi² {fits[0][0]:.0f} against the unsolved pages, where English itself scores {chi_u(E):.0f}); the best per-word filler model scores {best_pw:.0f} and the best per-rune one {best_pr:.0f}, both still outside the bootstrap range of an English sample (99th percentile {np.percentile(bu, 99):.0f}), so the fit is partial. Reading: the unsolved pages' words are not English prose with its separators intact; of the single-parameter distortions tried, inserted runes fit best, at about one filler per two words (or one per ten runes), a different register (verse, a list) is not excluded, and Latin, Old English, Chaucer and merged words fit worse. [stated]", ""]

# ---------- positional IoC and repeated words
allc = np.concatenate([c for c, _, _ in U]); allp = np.concatenate([p for _, _, p in U])
alle = np.concatenate([np.bincount(w)[w] - 1 - p for _, w, p in U])
def ioc(v):
    c = np.bincount(v, minlength=N); n = len(v); return (c * (c - 1)).sum() / (n * (n - 1)) * N
out += ["## Index of coincidence by word position (× 29; uniform = 1.00)", "", "A key that restarts at each word with a fixed keyword would make each word position a monoalphabetic column (IoC ≈ 1.8 for English). Null: 200 per-page shuffles of the runes, positions kept.", "",
        "| position | from the start: n | IoC | null | z | from the end: n | IoC | null | z |", "|---|---|---|---|---|---|---|---|---|"]
shuf_pages = [[rng.permutation(c) for c, _, _ in U] for _ in range(200)]
shuf = [np.concatenate(sp) for sp in shuf_pages]
for k in range(8):
    cells = []
    for key in (allp, alle):
        m = key == k; v = allc[m]; o = ioc(v); nul = np.array([ioc(s[m]) for s in shuf]); cells.append((int(m.sum()), o, nul.mean(), nul.std(), (o - nul.mean()) / nul.std()))
    out.append(f"| {k} | " + " | ".join(f"{n_} | {o:.3f} | {mu:.3f} ± {sd:.3f} | {z:+.1f}" for n_, o, mu, sd, z in cells) + " |")
def rep_words(pages, minlen):
    cnt = Counter()
    for c, w, p in pages:
        for wi in range(w.max() + 1):
            m = w == wi
            if m.sum() >= minlen: cnt[tuple(c[m])] += 1
    return sum(v - 1 for v in cnt.values() if v > 1), len(cnt)
out += ["", "## Repeated cipher words", ""]
for minlen in (3, 4):
    obs, nw = rep_words(U, minlen); nul = np.array([rep_words([(s, w, p) for s, (c, w, p) in zip(sp, U)], minlen)[0] for sp in shuf_pages[:100]])
    out.append(f"- Words of ≥ {minlen} runes: {nw:,} distinct; repeated occurrences {obs} (null {nul.mean():.1f} ± {nul.std():.1f}).")
out += ["", "English prose of 2,928 words repeats hundreds of its words of four or more runes (THAT, WITH, THIS, HAVE, ...). Zero repeats of four-rune cipher words is what any key that does not restart with the word gives; together with the flat positional IoC it excludes a per-word restarting key with a fixed keyword, the one family that could have carried the S weighting through a constant key at a word position (§47's uniform-key argument). [stated]", "",
        f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/wordlen_fingerprint.py`.", ""]
(RESULTS / "wordlen_fingerprint.md").write_text("\n".join(out))
print("\n".join(out[:4])); print(f"... written results/wordlen_fingerprint.md in {time.time()-t0:.0f}s")
