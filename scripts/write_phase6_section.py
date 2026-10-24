"""After src/edges_lane.py: write results/pnotisdev_open-unkeyed_entry.toml (their registry format)
and append README section 14 from results/phase6.json."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
r = json.load(open(R / "results/phase6.json"))
ctr = r["controls"]; top = r["top"]; hits = r["hits"]
KINDS = ("adv", "advline", "nulli", "nullf")
best = {k: max(t[6] for t in top if t[1] == k) for k in KINDS}
bestrow = top[0]
rank1 = sum(1 for c in ctr if c[8] >= 6 and c[9] == 1)
basez = (min(c[11] for c in ctr), max(c[11] for c in ctr))
advc = [c for c in ctr if c[1] in ("adv", "advline")]
nulc = [c for c in ctr if c[1] in ("nulli", "nullf")]
status = "excluded" if not hits else "candidate"
toml = f'''[[experiment]]
id = "open-unkeyed-ext-viterbi"
group = "structure"
title = "Word-edge events under the skip rule, independent run: extra key advance at word starts and at line starts, unencrypted null runes at word starts and at word ends, nu = 0.42, over the solved-text key families (external: cicada-ioc phase 6)"
status = "{status}"
what = "Independent implementation outside this repository (Viterbi over skip count with event transitions and a per-event log prior ln(0.42/0.58); unigram English model; per-page null of 2,000 random keystreams through the same edge decoder). Kinds adv (word-initial extra advance), advline (line-initial extra advance, the registry row's 'line / page breaks' part), nulli, nullf. Key library: 4,716 book keystreams (shifts, solved-text and headline words fwd/rev, primes p/p-1/p+1 at 101 starts, Fibonacci, Lucas, affine and square position formulas, the solved plaintext as running key at every offset) and 2,905 solved-text phrases and lines fwd/rev, each under c = p + k, c = p - k and c = k - p: 22,863 configurations x 55 pages x F rule on/off x 4 kinds = {r['ntests']:,} decodes"
control = "24 plants at nu = 0.42 on the pages' own edge masks (solved English windows, skip 0.81, every kind x sign x F): edge decoder z {min(c[8] for c in ctr):.1f}-{max(c[8] for c in ctr):.1f}, {rank1} of 24 rank 1 in their set (the exception a 3-rune key with aliases); edge minus base score +{min(c[10] for c in ctr):.0f} to +{max(c[10] for c in ctr):.0f} nats; the base decoder scores the same plants at z {basez[0]:.1f}-{basez[1]:.1f} (adv kinds {min(c[11] for c in advc):.1f}-{max(c[11] for c in advc):.1f}, null kinds {min(c[11] for c in nulc):.1f}-{max(c[11] for c in nulc):.1f})"
result = "Largest z {bestrow[6]:.2f} ({bestrow[0]}, {bestrow[1]}, {bestrow[2]}, {bestrow[4]} '{bestrow[5][:30]}'), per kind adv {best['adv']:.2f} / advline {best['advline']:.2f} / nulli {best['nulli']:.2f} / nullf {best['nullf']:.2f}, against a chance maximum of about 5.7 for {r['ntests']:,} tests; cells meeting the pre-registered rule (z >= 6 and edge minus base >= 20 nats): {len(hits)}. {'Negative.' if not hits else 'See results/phase6.md before believing any of them.'}"
gap = "Max-path rather than summed-path likelihood; the anti-repeat check compares with the previous emitted rune, not the previous real rune; nulls inside words; non-uniform null runes; more than one event per position; event rates far from 0.42; the 1,447-stream kscreen library (only this repository's book families and phrases were run); hold/spend/coin channel variants"
log = ["external: github cryptojaz/cicada-ioc README section 14, results/phase6.md"]
files = ["external: src/edges_lane.py, src/edges.py, src/score.py (decode with adv_mask/null_mask), results/phase6.json"]
'''
(R / "results/pnotisdev_open-unkeyed_entry.toml").write_text(toml)
sec = f"""
## 14. Phase 6: word-edge events under the skip rule, pnotisdev's open lane run independently (`results/phase6.md`)

The field survey (§11) found that pnotisdev/cicada3301's registry item `open-unkeyed` (its priority 2:
"unkeyed insertions and extra key advance at word separators / line / page breaks") had an engine,
a one-window pilot and a written campaign queue, but the campaign was never launched for want of a
free CPU, and its line-break part was never built. `src/edges.py` aligns the master transcription's
word and line separators to every unsolved page (3,261 word edges, 539 line edges); `score.decode`
gained two event transitions (an extra key advance before a candidate rune; a candidate rune as an
unencrypted uniform null that consumes no key) with a per-event log prior ln(0.42/0.58), the
default path left bit-identical; `src/edges_lane.py` runs four kinds (adv, advline, nulli, nullf)
over the phase 3 and 4 key families under all three signs and both F variants: **{r['ntests']:,}
tests**. The hit rule was written before any page was scored: z ≥ 6 over the page's own
random-keystream null under the same kind, edge score at least 20 nats above the base decoder's
score for the same configuration (pnotisdev's edge-versus-base margin), and readable English.

**Controls.** Twenty-four plants at the 42 % event rate on the pages' own edge masks: the edge
decoder recovers them at z {min(c[8] for c in ctr):.1f}–{max(c[8] for c in ctr):.1f}, {rank1} of 24 ranked first (the exception a three-rune
key with aliases), while the base decoder without events scores the same plants at z
{basez[0]:.1f}–{basez[1]:.1f}; for the advance kinds the base decoder is blind (z {min(c[11] for c in advc):.1f}–{max(c[11] for c in advc):.1f}), which is
why an event-aware decoder was needed at all.

**Result.** Largest z {bestrow[6]:.2f} ({bestrow[0]}, {bestrow[1]}, {bestrow[2]}, {bestrow[4]} '{bestrow[5][:30]}'); per kind adv {best['adv']:.2f}, advline
{best['advline']:.2f}, nulli {best['nulli']:.2f}, nullf {best['nullf']:.2f}; chance maximum about 5.7. Cells meeting the rule: {len(hits)}.
{'**Null.** ' if not hits else '**Candidates exist: see results/phase6.md.** '}Extra key advances at word or line starts and unencrypted
nulls at word starts or ends, at pnotisdev's fitted rate, over the book's own key families under the
skip rule, are excluded at the controls' sensitivity. The entry in pnotisdev's registry format is
`results/pnotisdev_open-unkeyed_entry.toml`, written to be pasted into their `docs/registry.toml`
with the gaps stated (max-path decoder, emitted-rune anti-repeat check, no in-word nulls, their
1,447-stream library not run).
"""
p = R / "README.md"; s = p.read_text()
if "## 14. Phase 6" not in s: p.write_text(s + sec); print("README section 14 appended")
print("registry entry written")
