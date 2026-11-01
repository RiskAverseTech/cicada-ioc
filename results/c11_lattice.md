# C11, the lattice step: the twelve cells above the free-null line under the §70 lattice decoder

Registration: `results/quorum_checks_registration.md`, "C11, the lattice step". Null: 2000 random keystreams per (page, F); rank: every offset of the cell's registered window under the same decoder (offsets within 3 of the cell's count as the same hypothesis).

| stream | page | sign | F | offset | free-null z | lattice z | above null max | rank in window | window max z | fillers / echoes placed | decode (first 60) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 0 | 3308 | 6.54 | -0.03 | no | 196 of 462 | 2.42 | 1 / 0 | `WAYONTHEA` |
| pn:sha512-ctr reject :PILGRIM | LP2-44 | sub | 0 | 9769 | 6.41 | 1.86 | no | 62 of 1170 | 3.51 | 6 / 0 | `ASITDOSOAFORSHE` |
| pn:sha256-ctr mod :program your mind | LP2-25 | add | 1 | 5340 | 6.33 | 0.39 | no | 225 of 700 | 4.73 | 8 / 0 | `NOTHESOIIHAOFCATSTHE` |
| pn:sha512-ctr reject :know this | LP2-20 | sub | 1 | 4437 | 6.27 | -0.67 | no | 434 of 585 | 3.33 | 6 / 0 | `DEWTOMYOHOFWEMYITIAM` |
| pn:md5-ctr reject :2014 | LP2-39 | sub | 1 | 8493 | 6.25 | 1.27 | no | 71 of 1041 | 3.26 | 6 / 0 | `IANUPMYCRABWEPITMYON` |
| pn:sha512-ctr mod :emergence | LP2-38 | sub | 0 | 8924 | 6.21 | -0.83 | no | 815 of 1019 | 3.61 | 6 / 0 | `BYIOFORORBYISA` |
| pn:md5-ctr reject :2014 | LP2-55 | add | 0 | 11864 | 6.16 | -1.29 | no | 1300 of 1389 | 3.18 | 0 / 0 | `LO` |
| pn:sha256-ctr mod :program your mind | LP2-15 | beaufort | 1 | 3592 | 6.11 | 1.05 | no | 69 of 462 | 2.59 | 6 / 0 | `WRENTHEGOSTYOFSA` |
| pn:sha256-ctr reject :pilgrim | LP2-44 | add | 0 | 9859 | 6.06 | -0.16 | no | 593 of 1170 | 3.36 | 3 / 0 | `MYMECLEFTAITUSEDEATSFEOH` |
| pn:sha256-ctr reject :a warning | LP2-24 | sub | 0 | 5680 | 6.06 | 0.73 | no | 149 of 673 | 3.64 | 7 / 0 | `BUTHEBYUPGOLINNGASINHEHUEA` |
| pn:md5-ctr reject :an end | LP2-11 | add | 1 | 2673 | 6.02 | -0.71 | no | 301 of 367 | 2.83 | 5 / 0 | `HEINDOEATINOTHE` |
| pn:sha256-ctr mod :self-reliance | LP2-21 | add | 0 | 4645 | 6.02 | 0.51 | no | 155 of 612 | 5.54 | 5 / 0 | `THEMEHERTATINATWOI` |

Plants (Bunyan words in E56w+n form under a library stream at the page's cumulative offset):

| plant | page | stream | sign | F | lattice z | rank in window | accuracy | fillers (placed) | echoes (placed) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | LP2-05 | pn:3301 - p_n | sub | 0 | 99.1 | 1 of 222 | 0.96 | 28 (29) | 2 (2) |
| 1 | LP2-14 | pn:sha256-ctr reject :instar | add | 0 | 72.6 | 1 of 448 | 0.91 | 9 (9) | 4 (2) |
| 2 | LP2-23 | pn:md5-ctr reject :PILGRIM | beaufort | 0 | 69.9 | 1 of 652 | 0.83 | 20 (19) | 0 (0) |
| 3 | LP2-32 | pn:md5-ctr mod :pilgrim | sub | 1 | 53.9 | 1 of 885 | 0.97 | 13 (13) | 0 (0) |
| 4 | LP2-41 | pn:prime gaps | add | 1 | 90.7 | 1 of 1089 | 1.00 | 23 (23) | 0 (0) |
| 5 | LP2-51 | pn:sha512-ctr reject :primes | beaufort | 1 | 41.9 | 1 of 1313 | 0.81 | 12 (12) | 1 (1) |

## Registered predictions

- L1 (every plant rank 1 at lattice z ≥ 8): holds.
- L2 (no cell at lattice z ≥ 8): largest 1.86 → holds.
- L3 (no readable decode): by inspection of the decode column.

Runtime 435 s. Reproduce: `.venv/bin/python -I src/c11_lattice_followup.py`.
