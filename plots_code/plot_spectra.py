# %%
import wandb
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rc_context

from common import STYLES, console

# %%
LOWER_LIMIT = 10**2.1
UPPER_LIMIT = 10**5

# XTICKS = np.logspace(np.log10(lower_limit), np.log10(upper_limit), NUM_BINS+1)
XTICKS = np.geomspace(10**2, 10**8, (8-2+1))

# %%
api = wandb.Api()

run = api.run("nicoweio/dsea-corn/3s0n2bmo")
BIN_EDGES = np.array(run.summary['bin_edges'])
STYLE = 'halfwidth'

pred_spectrum = np.array(run.summary['bootstrap/pred_spectra'][0])
pred_spectrum = np.append(pred_spectrum, pred_spectrum[-1])
true_spectrum = np.array(run.summary['bootstrap/true_spectra'][0])
true_spectrum = np.append(true_spectrum, true_spectrum[-1])

# %%
with rc_context(STYLES[STYLE]), console.status(f"Plotting spectrum…"):
    fig, axs = plt.subplots(
        2, 1,
        sharex=True,
        gridspec_kw={'height_ratios': [2, 1]},
    )

    # plt.hist(BINS[:-1], BINS, weights=spectrum_from_labels(labels), color='red', label='true class')

    axs[0].step(BIN_EDGES, true_spectrum, where='post', drawstyle='steps-mid', color='C1', linewidth=2, label='true class')
    axs[0].step(BIN_EDGES, pred_spectrum, where='post', drawstyle='steps-mid', color='C0', zorder=10, label='predicted probas')
    axs[0].set_ylabel('probability')  # TODO
    axs[0].set_yscale('log')
    axs[0].legend()
    # axs[0].set_xlim(100, 10_000)

    axs[1].step(BIN_EDGES, (pred_spectrum - true_spectrum) / true_spectrum, where='post', color='C2')
    axs[1].set_ylabel('relative deviation')
    axs[1].set_xscale('log')
    axs[1].set_xlabel(r'energy \mathbin{/} \si{\giga\electronvolt}')
    # axs[1].set_xlim(100, 10_000)

    # connect grid lines
    ax3 = fig.add_subplot(111, zorder=-1)
    for _, spine in ax3.spines.items():
        spine.set_visible(False)
    ax3.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
    ax3.set_xscale('log')
    ax3.get_shared_x_axes().join(ax3, axs[0])
    ax3.grid(axis="x")

    for ax in axs:
        # ax.set_xticks(BIN_EDGES)
        ax.set_xticks(XTICKS)
        ax.set_axisbelow(True)
        ax.grid()
        # Crop the x-axis so the overflow bin does not take up too much space;
        # suggestion by Karolin.
        ax.set_xlim(10**2, 10**5.5)

    # grey out under-/overflow
    # for ax in axs:
    for ax in plt.gcf().axes:
        COMMON_AXVSPAN_KWARGS = {
            'alpha': 0.3,
            'color': 'grey',
            # 'facecolor': 'grey', # Edges cause artifacts between subplots; but this looks bad, too.
            'hatch': '///',
        }
        ax.axvspan(LOWER_LIMIT, BIN_EDGES[0], **COMMON_AXVSPAN_KWARGS)
        ax.axvspan(BIN_EDGES[-1], UPPER_LIMIT, **COMMON_AXVSPAN_KWARGS)

    sns.despine()
    plt.tight_layout()
    # %%
    plt.savefig(f"../content/plots/bootstrap:spectrum_{STYLE}.pdf")
# %%
# TODO: Für single_events / per_bin_spectra: https://seaborn.pydata.org/tutorial/axis_grids.html
