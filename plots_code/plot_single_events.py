# %%
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import wandb
from matplotlib import rc_context

from common import PLOTS_DIR, STYLES, console

# %%
PLOT_XLIM = (10**2, 10**5.5)

# XTICKS = np.logspace(np.log10(lower_limit), np.log10(upper_limit), NUM_BINS+1)
XTICKS = np.geomspace(10**2, 10**8, (8-2+1))

# %%
api = wandb.Api()

run = api.run("nicoweio/dsea-corn/22zxe3xf")
STYLE = 'lessheight'
# %%
singleevents = np.array(run.summary['single_events'])

# %%
with rc_context(STYLES[STYLE]), console.status(f"Plotting single events…"):
    fig, axs = plt.subplots(
        2, 2,
        # sharex=True,
        # sharey=True,
    )
    BIN_INDEX_TUPLES = [
        (2, 0),
        (4, 0),
        (6, 1),
        (8, 1),
    ]
    assert len(BIN_INDEX_TUPLES) == axs.size

    for ax, BIN_INDEX_TUPLE in zip(axs.flat, BIN_INDEX_TUPLES):
        sevs_thisbin = singleevents[BIN_INDEX_TUPLE[0]]  # all single_events for this bin
        sev = sevs_thisbin[BIN_INDEX_TUPLE[1]]  # first single_event for this bin
        ax.bar(
            range(len(sev)),
            sev,
            edgecolor='black',
        )

        # █ plot
        # ax.bar(edges[:-1], hist, width=np.diff(edges), ec='k', align='edge')
        ax.axvline(BIN_INDEX_TUPLE[0], color='C1', linestyle='--')
        ax.set_xticks(range(10))
        ax.set_yticks([0.0, 0.5])
        ax.set_xlabel("bin index")
        ax.set_ylabel("confidence")
        # ax.set_title(f"Bin {BIN_INDEX_TUPLE[0]+1}")

    # fig.text(0.5, 0.04, "bin index", ha='center')
    # fig.text(0.04, 0.5, "confidence", va='center', rotation='vertical')

    plt.tight_layout()
    # %%
    plt.savefig(PLOTS_DIR / f"single_events_{STYLE}.pdf")
