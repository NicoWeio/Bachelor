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

run = api.run("nicoweio/dsea-corn/22zxe3xf")
# BIN_EDGES = np.array(run.summary['bin_edges'])
STYLE = 'lessheight'
# %%
singleevents = np.array(run.summary['single_events'])

# %%
with rc_context(STYLES[STYLE]), console.status(f"Plotting single events…"):
    fig, axs = plt.subplots(
        # 5, 2,
        2, 2,
        # 1, 2,
        # sharex=True,
        # sharey=True,
    )
    # BIN_INDICES = list(range(10))
    BIN_INDICES = [2, 4, 6, 8]
    # BIN_INDICES = [2, 8]
    assert len(BIN_INDICES) == axs.size

    for ax, BIN_INDEX in zip(axs.flat, BIN_INDICES):
        sevs_thisbin = singleevents[BIN_INDEX]  # all single_events for this bin
        sev = sevs_thisbin[0]  # first single_event for this bin
        ax.bar(
            range(len(sev)),
            sev,
            edgecolor='black',
        )

        # plot
        # ax.bar(edges[:-1], hist, width=np.diff(edges), ec='k', align='edge')
        ax.axvline(BIN_INDEX, color='C1', linestyle='--')
        ax.set_xticks(range(10))
        ax.set_yticks([0.0, 0.5])
        ax.set_xlabel("bin index")
        ax.set_ylabel("confidence")
        # ax.set_title(f"Bin {BIN_INDEX+1}")

    # fig.text(0.5, 0.04, "bin index", ha='center')
    # fig.text(0.04, 0.5, "confidence", va='center', rotation='vertical')

    plt.tight_layout()
    # %%
    plt.savefig(PLOTS_DIR / f"single_events_{STYLE}.pdf")
