"""The red runs as keys, as a stream, as ciphertext and in the clear (2026-10-31; registration results/red_lane_registration.md).
H1 own-page and cross-page repeating keys; H2 the 213-rune red stream as a running key at every offset; H3 the runs as ciphertext
under the book's keys; H4 headings in the clear and self-keyed; controls C1-C4.  Output: results/red_lane.md / .json.
Reproduce: .venv/bin/python -I src/red_lane.py
"""
import sys, json, time, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, N, english_to_runes
from score import decode, translit, S_MAX
from skip_decrypt import encrypt
import families as F

t0 = time.time(); rng = np.random.default_rng(66); NULLK, Z_HIT, SOFT = 400, 6.0, 0.81
LET = "F U TH O R C G W H N I J EO P X S T B E M L NG OE D A AE Y IA EA".split()
runs = [r for r in json.load(open(RESULTS / "red_runs.json")) if r["n"] >= 3]
glyphs = json.load(open(RESULTS / "scan_glyphs.json"))
pages = {pid: np.asarray(C) for pid, C in F.pages if len(C)}
SIGNS = (("sub", "sub"), ("add", "sub"), ("beaufort", "beaufort"))
for r in runs:                                   # page offset of the run's first rune
    lines = glyphs[str(r["chunk"])]["runes"]; r["off"] = sum(len(l) for l in lines[:r["line"] - 1]) + r["start"]
    assert list(pages[r["page"]][r["off"]:r["off"] + r["n"]]) == r["runes"], r["page"]
red_pos = {}
for r in runs: red_pos.setdefault(r["page"], set()).update(range(r["off"], r["off"] + r["n"]))
text = (RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(errors="ignore")[40000:]
EP = np.concatenate([np.array(english_to_runes(w)) for w in re.findall(r"[A-Za-z]+", text) if english_to_runes(w)])
NULLMAX = {}; NTESTS = {}


def z_of(C, Ks, f_rule, mode, nul_key):
    """scores of the rows of Ks on C against a cached null of 400 random keys of the same form; nul_key fixes the null's form"""
    sc, _, d = decode(C, Ks, F.lu, f_rule, mode); nul = NULLS[nul_key]
    z = (sc - nul.mean()) / nul.std(); rank = (nul[None, :] > sc[:, None]).sum(1) + 1
    return z, rank, d


NULLS = {}
def null_periodic(C, period, f_rule, mode, tag):
    key = (tag, len(C), period, f_rule, mode)
    if key not in NULLS:
        L = len(C) + S_MAX + 2; Kr = np.array([np.resize(k, L) for k in rng.integers(0, N, size=(NULLK, period))])
        NULLS[key] = decode(C, Kr, F.lu, f_rule, mode)[0]; NULLMAX[tag] = max(NULLMAX.get(tag, -9), float(((NULLS[key] - NULLS[key].mean()) / NULLS[key].std()).max()))
    return key


def null_stream(C, f_rule, mode, tag):
    key = (tag, len(C), 0, f_rule, mode)
    if key not in NULLS:
        NULLS[key] = decode(C, rng.integers(0, N, size=(NULLK, len(C) + S_MAX + 2)), F.lu, f_rule, mode)[0]; NULLMAX[tag] = max(NULLMAX.get(tag, -9), float(((NULLS[key] - NULLS[key].mean()) / NULLS[key].std()).max()))
    return key


def keyrow(K, L, sign): K = np.resize(np.asarray(K), L); return ((-K) % N if sign == "add" else K)[None, :]


# ---------- H1: repeating keys
def h1(C, label, keys, tag="H1"):
    rows = []; L = len(C) + S_MAX + 2
    for kname, K in keys:
        for f_rule in (False, True):
            for sign, mode in SIGNS:
                nk = null_periodic(C, len(K), f_rule, mode, tag); z, rank, d = z_of(C, keyrow(K, L, sign), f_rule, mode, nk); NTESTS[tag] = NTESTS.get(tag, 0) + 1
                rows.append(dict(target=label, key=kname, period=len(K), sign=sign, F=f_rule, z=float(z[0]), rank=int(rank[0]), tr=translit(d[0][:60])))
    return rows


keyset = [(f"{r['page']} L{r['line']} ({r['kind']}, {r['n']})", np.array(r["runes"])) for r in runs]
for pid in sorted(red_pos):
    rr = [r for r in runs if r["page"] == pid]
    if len(rr) > 1: keyset.append((f"{pid} all red ({sum(r['n'] for r in rr)})", np.concatenate([np.array(r["runes"]) for r in rr])))
H1 = []
for pid, C in pages.items():
    H1 += h1(C, pid, keyset)
    if pid in red_pos:
        mask = np.array([i not in red_pos[pid] for i in range(len(C))]); H1 += h1(C[mask], pid + " black", [k for k in keyset if k[0].startswith(pid)])
print(f"H1 done: {NTESTS['H1']:,} tests [{time.time()-t0:.0f}s]", flush=True)

# ---------- H2: the red stream as a running key
S = np.concatenate([np.array(r["runes"]) for r in sorted(runs, key=lambda r: (r["chunk"], r["line"], r["start"]))])
def h2(C, label, tag="H2"):
    rows = []; L = len(C) + S_MAX + 2
    for rev in (False, True):
        s = S[::-1] if rev else S; big = np.concatenate([s] * (L // len(s) + 2))
        Ks = np.array([big[o:o + L] for o in range(len(s))])
        for f_rule in (False, True):
            for sign, mode in SIGNS:
                nk = null_stream(C, f_rule, mode, tag); z, rank, d = z_of(C, (-Ks) % N if sign == "add" else Ks, f_rule, mode, nk); NTESTS[tag] = NTESTS.get(tag, 0) + len(Ks)
                j = int(z.argmax()); rows.append(dict(target=label, rev=rev, sign=sign, F=f_rule, offset=j, z=float(z[j]), rank=int(rank[j]), tr=translit(d[j][:60])))
    return rows
H2 = []
for pid, C in pages.items(): H2 += h2(C, pid)
print(f"H2 done: {NTESTS['H2']:,} tests [{time.time()-t0:.0f}s]", flush=True)

# ---------- H3: red runs as ciphertext under the book's keys
def h3(C, label, tag="H3"):
    rows = []; L = len(C) + S_MAX + 2
    for f_rule in (False, True):
        for sign, mode, Ks, labs in F.ALLSETS:
            nk = null_stream(C, f_rule, mode, tag); z, rank, d = z_of(C, Ks[:, :L], f_rule, mode, nk); NTESTS[tag] = NTESTS.get(tag, 0) + len(Ks)
            j = int(z.argmax()); rows.append(dict(target=label, sign=sign, F=f_rule, key=str(labs[j]), z=float(z[j]), rank=int(rank[j]), tr=translit(d[j][:60])))
    return rows
H3 = []
for r in runs:
    if r["n"] >= 8: H3 += h3(np.array(r["runes"]), f"{r['page']} L{r['line']} ({r['n']})")
print(f"H3 done: {NTESTS['H3']:,} tests [{time.time()-t0:.0f}s]", flush=True)

# ---------- H4: in the clear and self-keyed
def plain_z(C, tag="H4"):
    L = len(C) + S_MAX + 2; nk = null_stream(C, False, "sub", tag); z, rank, d = z_of(C, np.zeros((1, L), int), False, "sub", nk); NTESTS[tag] = NTESTS.get(tag, 0) + 1
    return float(z[0]), translit(d[0])
H4 = []
for r in runs:
    if r["n"] >= 8:
        C = np.array(r["runes"]); zc, tc = plain_z(C); zs, ts = plain_z((15 * C) % N)
        H4.append(dict(target=f"{r['page']} L{r['line']} ({r['kind']}, {r['n']})", z_clear=zc, clear=tc, z_self=zs, self=ts))
print(f"H4 done [{time.time()-t0:.0f}s]", flush=True)

# ---------- controls
ctrl = {}
P = EP[:262]; K1 = np.array(runs[0]["runes"]); C1 = encrypt(P, np.resize(K1, 2000), False, rng, SOFT, "sub")
rows = h1(C1, "control-1", keyset, tag="C1"); top = max(rows, key=lambda r: r["z"]); ctrl["C1"] = dict(top=top, ok=bool(top["key"] == keyset[0][0] and top["sign"] == "sub" and top["F"] is False and top["z"] >= Z_HIT and top["rank"] == 1))
o = int(rng.integers(0, len(S))); big = np.concatenate([S] * 12); C2 = encrypt(EP[300:562], big[o:o + 2000], False, rng, SOFT, "sub")
rows = h2(C2, "control-2", tag="C2"); top = max(rows, key=lambda r: r["z"]); ctrl["C2"] = dict(planted=o, top=top, ok=bool((not top["rev"]) and top["offset"] == o and top["sign"] == "sub" and top["z"] >= Z_HIT and top["rank"] == 1))
_, _, Kb, Lb = F.ALLSETS[0]; ki = int(rng.integers(0, len(Kb)))
for n, name in ((50, "C3"), (12, "C4")):
    Cc = encrypt(EP[700:700 + n], Kb[ki], False, rng, SOFT, "sub"); rows = h3(Cc, name, tag=name); top = max(rows, key=lambda r: r["z"])
    ctrl[name] = dict(planted=str(Lb[ki]), top=top, ok=bool(top["key"] == str(Lb[ki]) and top["sign"] == "sub" and top["z"] >= Z_HIT and top["rank"] == 1))
print(f"controls done [{time.time()-t0:.0f}s]", flush=True)

# ---------- report
def cand(rows): return [r for r in rows if r["z"] >= Z_HIT and r["rank"] == 1]
K1 = all(ctrl[c]["ok"] for c in ("C1", "C2", "C3")); K2 = not cand(H1); K3 = not cand(H2); K4 = not cand(H3); K5 = all(h["z_clear"] < 4 and h["z_self"] < 4 for h in H4)
def table(rows, cols, n=10):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in sorted(rows, key=lambda r: -r["z"])[:n]: out.append("| " + " | ".join(f"{r[c]:.2f}" if isinstance(r[c], float) else str(r[c]) for c in cols) + " |")
    return out
out = ["# The red runs as keys, as a stream, as ciphertext and in the clear", "", f"Registration: `results/red_lane_registration.md`. Data: `results/red_runs.md` ({len(runs)} runs of ≥ 3 runes, {len(S)} runes). Plain decoder with the soft skip; z against {NULLK} random keys of the same form per cell; candidate: z ≥ {Z_HIT:.0f}, rank 1, readable, above the hypothesis's largest null z.", "",
       "## Controls", "", "| control | planted | top: key / offset | sign | F | z | rank | pass |", "|---|---|---|---|---|---|---|---|"]
for c in ("C1", "C2", "C3", "C4"):
    t = ctrl[c]["top"]; out.append(f"| {c} | {ctrl[c].get('planted', keyset[0][0] if c == 'C1' else '')} | {t.get('key', t.get('offset'))} | {t['sign']} | {t['F']} | {t['z']:.1f} | {t['rank']} | {'yes' if ctrl[c]['ok'] else 'no'}{' (power statement, not a claim)' if c == 'C4' else ''} |")
out += ["", f"## H1 repeating keys: {NTESTS['H1']:,} tests, largest z {max(r['z'] for r in H1):.2f}, largest null z {NULLMAX['H1']:.2f}, candidates {len(cand(H1))}", ""] + table(H1, ["target", "key", "sign", "F", "z", "rank", "tr"])
out += ["", f"## H2 the red stream as a running key: {NTESTS['H2']:,} tests, largest z {max(r['z'] for r in H2):.2f}, largest null z {NULLMAX['H2']:.2f}, candidates {len(cand(H2))}", ""] + table(H2, ["target", "rev", "sign", "F", "offset", "z", "rank", "tr"])
out += ["", f"## H3 red runs as ciphertext under the book's keys: {NTESTS['H3']:,} tests, largest z {max(r['z'] for r in H3):.2f}, largest null z {NULLMAX['H3']:.2f}, candidates {len(cand(H3))}", ""] + table(H3, ["target", "sign", "F", "key", "z", "rank", "tr"])
out += ["", "## H4 headings in the clear and self-keyed (P = 15·C)", "", "| run | z as written | as written | z self-keyed | self-keyed |", "|---|---|---|---|---|"] + [f"| {h['target']} | {h['z_clear']:+.1f} | {h['clear']} | {h['z_self']:+.1f} | {h['self']} |" for h in H4]
out += ["", "## Claims", "", f"- K1 controls C1–C3: **{'hold' if K1 else 'fail'}**.", f"- K2 H1 no candidate: **{'holds' if K2 else 'fails'}**.", f"- K3 H2 no candidate: **{'holds' if K3 else 'fails'}**.", f"- K4 H3 nothing at z ≥ 6 rank 1: **{'holds' if K4 else 'fails'}**.", f"- K5 H4 nothing at z ≥ 4: **{'holds' if K5 else 'fails'}**.", "",
        "Reading: written after the run. [stated — the tables]", "", f"Runtime {time.time()-t0:.0f} s. Reproduce: `.venv/bin/python -I src/red_lane.py`.", ""]
(RESULTS / "red_lane.md").write_text("\n".join(out)); json.dump(dict(ntests=NTESTS, nullmax=NULLMAX, controls=ctrl, H1=H1, H2=H2, H3=H3, H4=H4, claims=dict(K1=K1, K2=K2, K3=K3, K4=K4, K5=K5)), open(RESULTS / "red_lane.json", "w"), indent=1, default=str)
print("\n".join(out))
