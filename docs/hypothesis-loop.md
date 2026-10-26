# The hypothesis loop: proposals from a model panel, killed by a statistical gate

`src/hypothesis_loop.py`. Results in `results/hypotheses.md`, machine-readable in `results/hypotheses.json`,
raw model responses in `results/hypotheses/`.

## Why

Six phases of sweeps in this repository and five public 2026 labs have closed every keystream family
anyone could name under the anti-repeat rule (README §9–§15, `results/ledger_diff.md`). What remains is not
compute but ideas: a construction nobody has written down. Models are cheap idea generators and expensive
compute spenders, so the loop is arranged to make ideas free and compute conditional. A panel proposes
constructions; a gate that costs a fraction of a second per construction decides, from the pages' own
statistics, whether the construction could even have produced the ciphertext. Only a construction that
passes, is decryptable given a key, and is on no ledger earns a sweep.

## The four statistics (the gate's yardstick)

Pooled over the 55 unsolved pages with runes (12,956 runes, 12,901 adjacent pairs):

| statistic | pages | iid uniform key |
|---|---|---|
| doubled runes | 86 | 446 ± 20 |
| chi-square of the 28 non-zero lag-1 difference classes (27 dof) | 42 | 27 ± 7 |
| unigram chi-square (28 dof) | 26 | 28 ± 7 |
| index of coincidence | 0.0345 | 0.0345 ± 0.0009 |

These are the statistics of `src/doublets.py` (phase 2), computed by the same code path. The gate's model
of a construction is 200 replicates of the solved pages' verified plaintext (2,977 runes of the book's own
English) cut from random offsets into the 55 real page lengths and enciphered with the construction; the
construction's four statistics then have a mean and a replicate sd. A construction **passes** when the pages
sit within 3 sd of its mean on all four. A **strict** column rescales the same distance by the iid-null sd,
so that a construction whose replicates vary wildly (a random short key, say) cannot pass merely because its
own spread is wide; the pre-registered rule is the first, the strict column is a reading aid.

Calibration before any proposal was gated (hand-built rows in the script): the vectorised encipherer
reproduces the phase 2 table row for row (independent key 446 doublets; 81 % re-draw 86–87; ciphertext
autokey lag 1 about 208 with lag-1 chi-square near 9,900; the +1 bump 85 but lag-1 chi-square about 300;
the never-repeating hand pad 448; DIVINITY with the F rule 506 and unigram chi-square about 2,600).

## The menu (what the gate can execute)

Proposals are data. The gate assembles a construction from four menus and never runs text a model wrote:

- **Key source**: `uniform` (any secret pad), `lcg` (a, c, modulus), `prime` / `totient` / `prime_plus1` /
  `prime_gap` at an offset, `fibonacci`, `lucas`, `position` (a·n² + b·n + c), `word` (the runes of a stated
  English text, or a random key of a stated period), `running_text` (the book's own plaintext at a random
  offset), `cipher_feedback` and `plain_feedback` (K_i = map(X_{i−lag}), optionally plus a base stream) with
  maps identity, Atbash, shift, affine, Gematria prime value, totient of that prime, square, or a fixed random
  bijection.
- **Combining rule**: `add` (C = P + K), `sub` (C = P − K), `beaufort` (C = K − P), `affine` (C = m·P + K) with
  the multiplier constant, a position schedule, or a second secret stream.
- **Repeat-avoidance rule**: `none`; `redraw` (take the next key symbol instead); `skip` by k; `bump` (add δ
  to the ciphertext); each fired with probability p when the rune at the chosen **target** would repeat its
  predecessor (ciphertext, the observed property; key, a pad that never repeats; or plaintext).
- **F rule**: none; the book's published rule (a plaintext F is written unencrypted and consumes no key
  symbol); or the variant where it still consumes one.

A JSON schema fixes these fields with enumerations; every proposal is validated against the menu before it
is executed and schema-invalid proposals are listed as such. Identical constructions from different proposers
are gated once (hash of the normalised construction).

Things the gate cannot see, and the brief says so: a fixed substitution before or after (no statistic
changes), transposition, word-edge nulls (phase 6), which text a running key comes from, the seed of a pad.

## The brief

Built at run time from `README.md`'s numbers, `results/doublets.md` in full, the family-by-family table, the
ranked list and the field survey of `results/ledger_diff.md`, and the rtkd key file for the solved sections.
It states the four statistics and the pass rule, the twenty phase 2 constructions and their verdicts, what
phases 3–7 swept and at what control sensitivity (phase 7, skip-by-two, was running during this run), and the
book's own methods: both word keys were taken from the book's plaintext, the F rule is the author's own skip,
the totient stream over the primes, plain Gematria, shift 3 then Atbash. The round-1 prompt measured by the
Anthropic token counter is reported in `results/hypotheses.md` (target: under 12k tokens).

## Proposers and rounds

Claude Fable 5.1 first (`claude-fable-5-1`, effort high, structured output against the schema, server-side
refusal fallback enabled); GPT-6.1 Sol and Grok 4.7 through the Responses API with the same schema (the models
and endpoint Quorum itself uses). The venv has no vendor SDKs and runs Python 3.9, so the script speaks raw
HTTP with the standard library. API keys come from Quorum's `.env.local` or the environment and are never
printed.

Round 1 asks each proposer for up to 15 ranked constructions with a one-paragraph rationale tied to the
book's methods and a predicted doublet count. Round 2 shows every proposer the full round-1 gate table (all
proposers, pass/fail per statistic, finite?, swept?) and asks for up to 10 refinements. A budget check between
rounds stops the loop at 70 % of the spend cap.

## After the gate

For each construction the script also answers, from fixed rules written against the ledgers: is the family
finite (decryptable by sweeping keys; a secret pad, a 29! bijection, a second secret stream or a re-drawn
symbol on a feedback-only key is not), how many configurations it has and hence how many decoder tests
(configurations × 55 pages), and whether an equivalent family is already on a ledger under the same repeat
rule (this repository's phases 3–7; jens-wedin, wazar, Leo-Y-Zhang, pnotisdev, murphyaidanbusiness-ux as
tabulated in `results/ledger_diff.md`). The survivors section of the report lists the constructions that pass,
are finite and are not fully swept, with their sweep size.

## Limits

- The gate tests reproducibility of four pooled statistics, not decryptability. Anything with an
  independent key and the right rejection rate passes; the gate separates repeat mechanisms, not key sources.
- Three sigma against the construction's own replicate spread is permissive for constructions with a wide
  spread; read the strict column alongside.
- The plaintext model is the book's own English. A non-English plaintext changes the plaintext statistics
  only slightly for these four measures (phase 5 found the English scorer loses little power on Latin or
  Old English), but the gate has not been run with those registers.
- The ledger check is a rule table, not a search of the external repositories; "partly" means a named lab
  ran a neighbouring configuration and the coverage is unclear.
- Model prices for GPT-6.1 Sol and Grok 4.7 are assumed in the cost table; token counts are exact.

## Reproduce

```
.venv/bin/python -I src/hypothesis_loop.py --dry          # gate calibration only, no API
.venv/bin/python -I src/hypothesis_loop.py                # both rounds, all proposers with keys
.venv/bin/python -I src/hypothesis_loop.py --report-only  # rebuild the report from results/hypotheses.json
```
