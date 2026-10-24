"""Append README section 13 from results/phase5.json (run once, after the sweep)."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
r = json.load(open(R / "results/phase5.json"))
ctr = r["controls"]; top = r["top"]
def reg(name): return [c for c in ctr if c[1] == name]
def zrange(rows, i): return f"{min(x[i] for x in rows):.1f}–{max(x[i] for x in rows):.1f}"
la, ang = reg("la"), reg("ang")
best = {k: max(t[6] for t in top if t[0] == k) for k in ("la", "ang")}
sec = f"""
## 13. Phase 5: Latin and Old English plaintext models (`results/phase5.md`)

Every lab's negatives were English-register negatives, and wazar showed that under its quadgram
scorer a correct key over a Latin or Old English plaintext scores as noise. `src/registers.py`
builds rune-unigram models from public-domain corpora transliterated with the book's own rules:
Latin from Caesar's Gallic War and Cicero's Catilinarians (68,000 words, 379,331 runes); Old
English from Beowulf and eighteen prose and verse texts of Bright's Anglo-Saxon Reader (36,863
words, 159,508 runes; thorn and eth to TH, ash to AE, length marks dropped). `src/sweep_registers.py`
reruns every phase 3 and 4 family (22,863 configurations, three signs) on all 55 pages, both F
variants, with the decoder's model set to each language: **{r['ntests']:,} tests**.

**Controls.** Twelve planted keys per register on windows of that language's corpus, decoded
with the register's own model and, separately, with the English model. Latin: own model
z {zrange(la, 6)}, {sum(1 for c in la if c[7]==1)} of 12 rank 1; English model z {zrange(la, 9)},
{sum(1 for c in la if c[10]==1)} of 12 rank 1. Old English: own model z {zrange(ang, 6)},
{sum(1 for c in ang if c[7]==1)} of 12 rank 1; English model z {zrange(ang, 9)},
{sum(1 for c in ang if c[10]==1)} of 12 rank 1. So the English unigram scorer loses little power
on either register: the blind spot wazar reported belongs to quadgram scorers, and phases 3 and 4
already covered Latin and Old English plaintexts at only slightly reduced sensitivity.

**Result: null.** Largest z under the Latin model {best['la']:.2f}, under the Old English model
{best['ang']:.2f}, both inside the chance range for this many tests; the top transliterations
are gibberish in either language. The book families and phrase keys under the skip rule are
excluded for Latin and Old English plaintexts at the controls' sensitivity.

Context from the wider survey (§11, `results/ledger_diff.md`): the October 2026 campaign's
language lane found Latin ten to thirty times worse than English on word-length statistics and
could not fetch Old English prose at all, so the Old English prose lane here was the only
genuinely untested register; it is now closed for these families.
"""
p = R / "README.md"; s = p.read_text()
if "## 13. Phase 5" not in s:
    p.write_text(s + sec); print("README section 13 appended")
else: print("already present")
