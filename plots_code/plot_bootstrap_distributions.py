# %%
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import wandb
from matplotlib import rc_context

from common import PLOTS_DIR, STYLES, console

# %%
LOWER_LIMIT = 10**2.1
UPPER_LIMIT = 10**5

PLOT_XLIM = (10**2, 10**5.5)

# XTICKS = np.logspace(np.log10(lower_limit), np.log10(upper_limit), NUM_BINS+1)
XTICKS = np.geomspace(10**2, 10**8, (8-2+1))

# %%
api = wandb.Api()

run = api.run("nicoweio/dsea-corn/24sfwi8p")
BIN_EDGES = np.array(run.summary['bin_edges'])
STYLE = 'doubleheight'
# %%
pred_spectra = np.vstack(run.summary['bootstrap/pred_spectra'])
true_spectra = np.vstack(run.summary['bootstrap/true_spectra'])

# %%
with rc_context(STYLES[STYLE]), console.status(f"Plotting spectrum…"):
    fig, axs = plt.subplots(
        5, 2,
        # sharex=True,
        # sharey=True,
    )
    BIN_INDICES = list(range(10))
    assert len(BIN_INDICES) == axs.size

    for ax, BIN_INDEX in zip(axs.flat, BIN_INDICES):
        hist, edges = np.histogram(
            pred_spectra[:, BIN_INDEX],
            bins=10,
            # range=(0, 1),
            # density=True,
        )
        # plot the histogram
        ax.bar(edges[:-1], hist, width=np.diff(edges), ec='k', align='edge')
        ax.axvline(true_spectra[:, BIN_INDEX].mean(), color='C1', linestyle='--')
        ax.set_xlabel("probability density")
        ax.set_ylabel("count")
        ax.set_title(f"Bin {BIN_INDEX+1}")

    # fig.text(0.5, 0.04, "probability density", ha='center')
    # fig.text(0.04, 0.5, "count", va='center', rotation='vertical')

    plt.tight_layout()

    # %%
    plt.savefig(PLOTS_DIR / f"bootstrap:distributions_{STYLE}.pdf")
