"""K-fixed Metropolis sampler shared by src/kfixed_echo.py and src/s_carrier.py (moved here 2026-10-29).

Target: the uniform law over the arrangements of a page's runes that keep its adjacent-repeat count.  Proposal: a
transposition of two positions, symmetric; accepted when the repeat count is unchanged, otherwise the state stays.
The clock counts ATTEMPTED proposals.  A rejected proposal leaves the arrangement in place and still advances time, as
the Metropolis chain requires; the 2026-10-28 versions of both scripts advanced the clock on accepted proposals only,
which samples the embedded jump chain and weights each arrangement by its acceptance rate (found by the second external
review, 2026-10-29; tests/test_validation.py checks the small-case law).
"""
import numpy as np


def doublets(c):
    return int((c[1:] == c[:-1]).sum())


def kfixed_step(c, nattempt, rng):
    """nattempt attempted transpositions of c in place; returns c."""
    L = len(c)
    for i, j in rng.integers(0, L, size=(nattempt, 2)):
        if i == j or c[i] == c[j]: continue
        idx = set()
        for t in (i, j):
            if t > 0: idx.add(t - 1)
            if t < L - 1: idx.add(t)
        before = sum(c[t] == c[t + 1] for t in idx)
        c[i], c[j] = c[j], c[i]
        after = sum(c[t] == c[t + 1] for t in idx)
        if after != before: c[i], c[j] = c[j], c[i]
    return c


def kfixed_step_accepted_clock(c, nacc, rng):
    """The 2026-10-28 clock, kept only for the test that shows its bias: advances on accepted proposals."""
    L = len(c); acc = 0
    while acc < nacc:
        i, j = rng.integers(0, L, 2)
        if i == j or c[i] == c[j]: acc += 1; continue
        idx = set()
        for t in (i, j):
            if t > 0: idx.add(t - 1)
            if t < L - 1: idx.add(t)
        before = sum(c[t] == c[t + 1] for t in idx)
        c[i], c[j] = c[j], c[i]
        after = sum(c[t] == c[t + 1] for t in idx)
        if after != before: c[i], c[j] = c[j], c[i]
        else: acc += 1
    return c
