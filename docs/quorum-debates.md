# The Quorum debates behind this repository

Quorum (quorumsays.com) seats several models, has them answer and cross-examine, and scores the verdict's claims. It was used here as a hypothesis generator and a red team, never as a source of facts: every claim it produced that mattered was tested in the repository, and the sections below record what survived.

| date | debate | what was asked | what it gave | what was tested |
|---|---|---|---|---|
| 2026-10-26 | [8gvLyrvHouBK](https://www.quorumsays.com/q/8gvLyrvHouBK) | Which mechanism leaks 19 % of repeats in an anti-repeat rule, given four new ciphertext premises | Claimed three mechanisms are equivalent on every figure and named lag-2 as the discriminator; flagged two unsourced figures in the asker's take | §21: simulation showed the three are not equivalent (nulls need 22 %, a sticky key fails lag-1 by 2 sigma) and lag-2 discriminates nothing; §22 swept the one breakable survivor |
| 2026-10-27 | [JOkSnnZ5csJf](https://www.quorumsays.com/q/JOkSnnZ5csJf) | Which public texts Cicada demonstrably used as book-cipher keys | Four texts with documented use, the rest theme; use the transcription solvers indexed | §25: all four were in the corpus already; edition sensitivity measured (a mid-page difference of five runes costs about five sigma) |
| 2026-10-28 | [EmEfDcbkkmyy](https://www.quorumsays.com/q/EmEfDcbkkmyy) | Which non-additive mechanisms keep the fingerprint and blind additive sweeps, with a distinguishing statistic each | A stream with one law admits no ciphertext-only mechanism test; only implementation leaks are testable; proposed boundary clustering of the repeats | §32 ran the mixed-alphabet class the take named; §33 tested boundary clustering (none) |

**What the panel is good at.** Naming constructions and the test that would separate them, and catching an asker's unsourced numbers. **What it is not good at.** Facts about repositories and the field (it could not find a 200-text sweep that is public), and numerical predictions nobody derived; its own scorer marks those, and the marks were reliable all three times.

**Pattern that worked.** Pin the measured facts in the question, demand a ciphertext-only statistic for every proposal, let the scorer separate sourced from unsourced, then test the survivors in the repository within the day. Three debates produced two new tests and one new sweep.
