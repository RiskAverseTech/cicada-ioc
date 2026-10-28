# Where the 86 doubled runes sit

12,956 runes, 12,901 within-page adjacent pairs, 86 doublets (unsolved pages, master transcription with its word, clause, line and paragraph separators).

| boundary between the two runes | all within-page pairs | share | doublets | expected if boundary-blind | binomial p |
|---|---|---|---|---|---|
| none | 9,640 | 0.747 | 60 | 64.3 | 0.32 |
| line-wrap inside a word | 388 | 0.030 | 3 | 2.6 | 0.75 |
| word | 2,616 | 0.203 | 22 | 17.4 | 0.23 |
| clause | 136 | 0.011 | 1 | 0.9 | 0.60 |
| line | 116 | 0.009 | 0 | 0.8 | 1.00 |
| paragraph | 3 | 0.000 | 0 | 0.0 | 1.00 |
| segment | 2 | 0.000 | 0 | 0.0 | 1.00 |

KS test of doublet position within the page against uniform: p = 0.63.

**Reading.** The repeats fall inside words 63 times (of which 3 across a line wrap) against 66.8 expected and at word boundaries 22 times against 17.4; every boundary class sits within one sigma of boundary-blind, and their positions within pages are uniform. A chain or stepping cipher that resets at word, line or page starts, and a transcription artefact at line ends, would both have put the repeats at boundaries. Neither did. The anti-repeat mechanism acts uniformly on the stream, which is what a filtered pad or any boundary-blind generator does.

