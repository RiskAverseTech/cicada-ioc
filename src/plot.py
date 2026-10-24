"""Plot the depth-two scan against its null.  Reads results/depth_two_arrays.npz and
results/depth_two_null.npz written by depth_two.py; builds one fresh within-page
permutation replicate for the histogram overlay."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lp import *
import depth_two

BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})

A = np.load(RESULTS / "depth_two_arrays.npz")
NL = np.load(RESULTS / "depth_two_null.npz")
S = json.loads((RESULTS / "depth_two_summary.json").read_text())
sig, offs, asig, lags = A["sig"], A["offs"], A["asig"], A["lags"]
d = json.loads((PROCESSED / "pages.json").read_text())
pages = [np.array(u["cipher"]) for u in d["unsolved"] if u["length"] > 0]
rng = np.random.default_rng(7)
_, _, s_null, _, _, _, a_null, _, _ = depth_two.scan([rng.permutation(p) for p in pages])

fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), gridspec_kw={"width_ratios": [1.1, 1.3, 1]})
# Panel 1: sigma histogram, observed vs permutation replicate, log y.
obs = sig[np.isfinite(sig)]; nul = s_null[np.isfinite(s_null)]
bins = np.linspace(-5, 9, 71)
ax[0].hist(nul, bins=bins, histtype="step", color=ORANGE, lw=2, label="within-page shuffle (null)")
ax[0].hist(obs, bins=bins, histtype="step", color=BLUE, lw=2, label="observed pairs")
x = np.linspace(-5, 9, 400)
ax[0].plot(x, len(obs) * (bins[1] - bins[0]) * np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi), color=INK2, lw=1, ls="--", label="N(0,1)")
ax[0].axvline(5, color=INK2, lw=1, ls=":")
ax[0].text(5.1, 3e2, "5 sigma", color=INK2, fontsize=9)
ax[0].set_yscale("log"); ax[0].set_ylim(0.5, None)
ax[0].set_xlabel("sigma of difference-stream IC (per pair, per offset)"); ax[0].set_ylabel("count of tests")
ax[0].set_title(f"{len(obs):,} pair-offset tests", loc="left", fontsize=11, color=INK)
ax[0].legend(frameon=False, fontsize=8, loc="upper right")
# Panel 2: pooled z vs offset with permutation band.
zp = depth_two.pooled(sig); nz = NL["null_zp"]
ax[1].fill_between(offs, nz.min(axis=0), nz.max(axis=0), color=ORANGE, alpha=0.25, lw=0, label=f"null range, {nz.shape[0]} shuffles")
ax[1].plot(offs, zp, color=BLUE, lw=1.2, label="observed pooled z")
ax[1].axhline(5, color=INK2, lw=1, ls=":"); ax[1].text(-198, 5.15, "R2 threshold (5)", color=INK2, fontsize=9)
ax[1].set_xlabel("relative offset between the two pages (runes)"); ax[1].set_ylabel("pooled z over all page pairs")
ax[1].set_title("Aligned reuse would spike at one offset", loc="left", fontsize=11, color=INK)
ax[1].set_ylim(-4.5, 6); ax[1].legend(frameon=False, fontsize=8, loc="lower right")
# Panel 3: pooled z vs lag.
za = depth_two.pooled(asig); na = NL["null_za"]
ax[2].fill_between(lags, na.min(axis=0), na.max(axis=0), color=ORANGE, alpha=0.25, lw=0)
ax[2].plot(lags, za, color=BLUE, lw=1.2)
ax[2].axhline(5, color=INK2, lw=1, ls=":")
ax[2].set_xlabel("lag within a page (runes)"); ax[2].set_ylabel("pooled z over all pages")
ax[2].set_title("A short-period generator would spike at its period", loc="left", fontsize=11, color=INK)
ax[2].set_ylim(-4.5, 7.2)
ax[2].annotate(f"lag 1: z = {za[0]:.1f}\n(doublet deficit, see lag1.md)", xy=(1, za[0]), xytext=(40, 6.3), fontsize=8.5, color=INK2, arrowprops={"arrowstyle": "-", "color": INK2, "lw": 0.8})
for a in ax:
    a.grid(axis="y", color=GRID, lw=0.8); a.set_axisbelow(True)
fig.suptitle("Liber Primus unsolved pages: depth-two key-reuse scan vs. null", x=0.01, ha="left", fontsize=13, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(RESULTS / "depth_two.png", dpi=150)
print("wrote", RESULTS / "depth_two.png")
