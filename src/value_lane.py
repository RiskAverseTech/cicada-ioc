"""Value arithmetic as the cipher (2026-10-31; registration results/value_lane_registration.md): 24 rules combining the
Gematria prime (or totient) of plaintext and key by +, -, reverse -, x modulo 29 / 110 / 113, decoded with the general-rule
table hook of score.decode over the book's 7,621 keys and 3,000 prime-stream variants, literal F on and off.  Scores are corrected by
each key's analytic baseline before z (registration amendment of 2026-10-31); the raw z is kept beside it.
SHARD=k NSHARD=8 for the sweep (pages), CONTROLS=1 for the six plants, MERGE=1 to write results/value_lane.md.
Reproduce: for k in 0..7: SHARD=k NSHARD=8 .venv/bin/python -I src/value_lane.py; then MERGE=1 ...
"""
import os, re, sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lp import RAW, RESULTS, N, english_to_runes
from score import decode, translit, S_MAX, LOGU
import families as F

t0 = time.time(); SHARD, NSHARD = int(os.environ.get("SHARD", 0)), int(os.environ.get("NSHARD", 1))
MERGE, CONTROLS = os.environ.get("MERGE") == "1", os.environ.get("CONTROLS") == "1"
NULLK, Z_HIT, SOFT, PEN_UNREACH = 400, 6.0, 0.81, -8.0
GP = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109])
VMAPS = {"prime": GP, "totient": GP - 1}
OPS = {"p+k": lambda a, b: a + b, "p-k": lambda a, b: a - b, "k-p": lambda a, b: b - a, "p*k": lambda a, b: a * b}
MODS = (29, 110, 113)
lu = F.lu


def rule_tables(vm, op, M):
    V = VMAPS[vm]; f = OPS[op]; enc = np.zeros((N, N), int)
    for p in range(N):
        for k in range(N): enc[p, k] = (int(f(V[p], V[k])) % M) % N
    table = np.zeros((N, N), int); tgain = np.full((N, N), PEN_UNREACH)
    for k in range(N):
        for c in range(N):
            cands = np.flatnonzero(enc[:, k] == c)
            if len(cands): best = cands[np.argmax(lu[cands])]; table[c, k] = best; tgain[c, k] = lu[best] - LOGU
    return enc, table, tgain


RULES = [(vm, op, M) for vm in VMAPS for op in OPS for M in MODS]
TABLES = {r: rule_tables(*r) for r in RULES}


def sieve(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.flatnonzero(s)
PRIMES = sieve(20000); LKEY = max(len(C) for _, C in F.pages) + S_MAX + 2
KEYSET = os.environ.get("KEYSET", "book")          # "book": the 2,905 phrase keys + 3,000 prime streams (pass 1); "phase3": the 4,716 word and text keys (pass 2, 2026-10-31)
_, _, Kbook, Lbook = F.ALLSETS[0]; Kbook = Kbook[:, :LKEY]
_, _, Kp3, Lp3 = F.ALLSETS[3]; Kp3 = Kp3[:, :LKEY]; OUTP = "" if KEYSET == "book" else "_p3"
ps = []; pl = []
for s in range(1000):
    seg = PRIMES[s:s + LKEY]
    for name, arr in (("p", seg), ("p-1", seg - 1), ("p+1", seg + 1)): ps.append(arr % N); pl.append((f"prime {name}", f"s={s}"))
KALL = np.vstack([Kbook, np.array(ps)]) if KEYSET == "book" else Kp3; LALL = ([str(l) for l in Lbook] + [f"{a} {b}" for a, b in pl]) if KEYSET == "book" else [str(l) for l in Lp3]
pages = [(pid, np.asarray(C)) for pid, C in F.pages if len(C)]


def encrypt_rule(P, K, enc, f_rule, rng):
    C, j, prev = [], 0, None
    for p in P:
        if f_rule and p == 0: C.append(0); prev = 0; continue
        c = int(enc[p, K[j]])
        while prev is not None and c == prev and rng.random() < SOFT: j += 1; c = int(enc[p, K[j]])
        C.append(c); j += 1; prev = c
    return np.array(C)


def baseline(Ks, tgain, n):
    """expected gain of a key under uniform ciphertext, skips ignored (amendment of 2026-10-31): sum_i mean_c tgain[c, K_i]"""
    return tgain.mean(0)[Ks[:, :n]].sum(1)


def sweep_page(C, rules, Ks, rng, keep=4.5):
    rows, nt, zmax, nullmax = [], 0, -9.0, -9.0; L = len(C) + S_MAX + 2
    for r in rules:
        enc, table, tgain = TABLES[r]; bK = baseline(Ks, tgain, len(C))
        for f_rule in (False, True):
            Kr = rng.integers(0, N, size=(NULLK, L)); nul_raw = decode(C, Kr, lu, f_rule, table=table, tgain=tgain, enc=enc)[0]; nul = nul_raw - baseline(Kr, tgain, len(C))
            m0, s0 = nul.mean(), nul.std(); nullmax = max(nullmax, float(((nul - m0) / s0).max()))
            sc_raw = np.empty(len(Ks))
            for b in range(0, len(Ks), 1000): sc_raw[b:b + 1000] = decode(C, Ks[b:b + 1000, :L], lu, f_rule, table=table, tgain=tgain, enc=enc)[0]
            sc = sc_raw - bK; z = (sc - m0) / s0; zraw = (sc_raw - nul_raw.mean()) / nul_raw.std(); nt += len(Ks); zmax = max(zmax, float(z.max()))
            for j in np.flatnonzero(z >= keep):
                d = decode(C, Ks[j:j + 1, :L], lu, f_rule, table=table, tgain=tgain, enc=enc)[2][0]
                rows.append(dict(rule="%s %s mod %d" % r, F=f_rule, key=LALL[j] if len(Ks) == len(KALL) else str(j), z=float(z[j]), zraw=float(zraw[j]), rank=int((nul > sc[j]).sum()) + 1, tr=translit(d[:70])))
    return rows, nt, zmax, nullmax


if CONTROLS:
    rng = np.random.default_rng(67)
    text = (RAW.parent / "corpus" / "raw" / "emerson_essays1_pg2944.txt").read_text(errors="ignore")[50000:]
    EP = np.concatenate([np.array(english_to_runes(w)) for w in re.findall(r"[A-Za-z]+", text) if english_to_runes(w)])
    picks = [("prime", "p+k", 29), ("totient", "p-k", 110), ("prime", "k-p", 113), ("totient", "p*k", 29), ("prime", "p*k", 110), ("totient", "p+k", 113)]
    ctrl = []
    for ci, r in enumerate(picks):
        f_rule = bool(ci % 2); ki = int(rng.integers(0, len(Kbook))); P = EP[ci * 300: ci * 300 + 262]
        C = encrypt_rule(P, Kbook[ki], TABLES[r][0], f_rule, rng)
        rows, nt, zmax, nullmax = sweep_page(C, [r], Kbook, rng, keep=-99)
        rows = [x for x in rows if x["F"] == f_rule]; top = max(rows, key=lambda x: x["z"]); mine = [x for x in rows if x["key"] == str(ki)][0]
        ok = bool(top["key"] == str(ki) and mine["z"] >= Z_HIT and mine["rank"] == 1)
        acc = float((decode(C, Kbook[ki:ki + 1, :len(C) + S_MAX + 2], lu, f_rule, table=TABLES[r][1], tgain=TABLES[r][2], enc=TABLES[r][0])[2][0] == P).mean())
        ctrl.append(dict(rule="%s %s mod %d" % r, F=f_rule, planted=str(Lbook[ki]), z=mine["z"], rank=mine["rank"], top_is_planted=top["key"] == str(ki), acc=acc, ok=ok))
        print(f"control {ci} {ctrl[-1]} [{time.time()-t0:.0f}s]", flush=True)
    json.dump(ctrl, open(RESULTS / "value_lane_controls.json", "w"), indent=1); sys.exit(0)

if MERGE:
    shards = [json.loads(p.read_text()) for p in sorted(RESULTS.glob("value_lane_shard*.json")) + sorted(RESULTS.glob("value_lane_p3_shard*.json"))]
    ctrl = json.load(open(RESULTS / "value_lane_controls.json")); rows = sorted([r for d in shards for r in d["rows"]], key=lambda r: -r["z"])
    nt = sum(d["ntests"] for d in shards); zmax = max(d["zmax"] for d in shards); nullmax = max(d["nullmax"] for d in shards)
    cands = [r for r in rows if r["z"] >= Z_HIT and r["rank"] == 1 and r["z"] > nullmax]
    out = ["# Value arithmetic as the cipher", "", f"Registration: `results/value_lane_registration.md`. {len(RULES)} rules × {len(Kbook) + len(Kp3) + len(ps):,} keys ({len(Kbook):,} phrase keys and {len(ps):,} prime-stream variants in pass 1, {len(Kp3):,} word and text keys in pass 2) × 2 F × {len(pages)} pages = **{nt:,} decodes**; z against {NULLK} random keys per (page, rule, F). Largest z {zmax:.2f}; largest null z over every null draw {nullmax:.2f}.", "",
           "## Controls (English at page length under the rule, soft 0.81, a random book key; decoded over the 7,621 book keys)", "", "| rule | F | planted key | z | rank | top is planted | rune accuracy | pass |", "|---|---|---|---|---|---|---|---|"]
    for c in ctrl: out.append(f"| {c['rule']} | {c['F']} | {c['planted']} | {c['z']:.1f} | {c['rank']} | {c['top_is_planted']} | {c['acc']:.2f} | {'yes' if c['ok'] else 'no'} |")
    out += ["", f"Controls passing: {sum(c['ok'] for c in ctrl)} of {len(ctrl)}.", "", "## Rows at z ≥ 4.5 (top 25)", "", "| page | rule | F | key | z (corrected) | raw z | rank | transliteration |", "|---|---|---|---|---|---|---|---|"]
    for r in rows[:25]: out.append(f"| {r['page']} | {r['rule']} | {r['F']} | {r['key']} | {r['z']:.2f} | {r['zraw']:.2f} | {r['rank']} | {r['tr'][:60]} |")
    out += ["", "## Candidates", ""] + ([f"- {r}" for r in cands] or ["None. No accepted decoding within the tested configurations at the stated detection limits."])
    out += ["", f"- V1 controls 6/6: **{'holds' if sum(c['ok'] for c in ctrl) == 6 else 'fails'}**.", f"- V2 no candidate: **{'holds' if not cands else 'fails'}**.", "", "Reading: written after the run. [stated — the tables]", "", f"Runtime, longest shard: {max(d['seconds'] for d in shards)/3600:.1f} h on {len(shards)} shards.", ""]
    (RESULTS / "value_lane.md").write_text("\n".join(out)); json.dump(dict(ntests=nt, zmax=zmax, nullmax=nullmax, rows=rows, controls=ctrl, candidates=cands), open(RESULTS / "value_lane.json", "w"), indent=1)
    print("\n".join(out)); sys.exit(0)

rng = np.random.default_rng(1000 + SHARD); mine = [p for j, p in enumerate(pages) if j % NSHARD == SHARD]
allrows, NT, ZMAX, NMAX = [], 0, -9.0, -9.0
for pid, C in mine:
    rows, nt, zmax, nullmax = sweep_page(C, RULES, KALL, rng)
    for r in rows: r["page"] = pid
    allrows += rows; NT += nt; ZMAX = max(ZMAX, zmax); NMAX = max(NMAX, nullmax)
    print(f"  {pid}: {NT:,} tests, zmax {ZMAX:.2f}, null max {NMAX:.2f}, rows {len(allrows)} [{time.time()-t0:.0f}s]", flush=True)
json.dump(dict(rows=allrows, ntests=NT, zmax=ZMAX, nullmax=NMAX, seconds=time.time() - t0), open(RESULTS / f"value_lane{OUTP}_shard{SHARD}.json", "w"), indent=1)
print(f"shard {SHARD}/{NSHARD} done: {NT:,} tests [{time.time()-t0:.0f}s]")
