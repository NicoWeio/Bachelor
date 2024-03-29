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


# RUN_ID = '24sfwi8p'  # ??? | without multi/train_spectra!
# RUN_ID = 'ffzxcq98'  # ??? | without multi/train_spectra!
# RUN_ID = 'p0iam6rs' # bias (<50 iters), small epsilon
# RUN_ID = 'hcoro29d'  # 2 Mio. events
RUN_ID = 'r3dx5m3y'  # v3

run = api.run(f"nicoweio/dsea-corn/{RUN_ID}")
BIN_EDGES = np.array(run.summary['bin_edges'])
STYLE = 'full'
# %%

pred_spectra = np.vstack(run.summary['multi/pred_spectra'])
true_spectra = np.vstack(run.summary['multi/true_spectra'])
# train_spectra = np.vstack(run.summary['multi/train_spectra'])
# ↓ COULDDO: Though not really wrong, this is just a workaround for old runs without this key
train_spectra = np.vstack(run.summary.get('multi/train_spectra', true_spectra))

# repeat the last entry to match the number of bin EDGES
pred_spectra = np.append(pred_spectra, pred_spectra[:, -1, np.newaxis], axis=1)
true_spectra = np.append(true_spectra, true_spectra[:, -1, np.newaxis], axis=1)
train_spectra = np.append(train_spectra, train_spectra[:, -1, np.newaxis], axis=1)

# %%
# determine median and 68% confidence interval
pred_spectrum = np.median(pred_spectra, axis=0)
true_spectrum = np.median(true_spectra, axis=0)
train_spectrum = np.median(train_spectra, axis=0)

pred_spectrum_error = np.percentile(pred_spectra, [16, 84], axis=0)
true_spectrum_error = np.percentile(true_spectra, [16, 84], axis=0)
train_spectrum_error = np.percentile(train_spectra, [16, 84], axis=0)

# %%
rel_errors = (pred_spectra - true_spectra) / true_spectra
rel_error = np.median(rel_errors, axis=0)
# rel_error = (pred_spectrum - true_spectrum) / true_spectrum

pred_percentiles_as_err = np.array([
    # matplotlib expects [lower, upper]
    pred_spectrum - pred_spectrum_error[0],
    pred_spectrum_error[1] - pred_spectrum,
])

rel_error_percentiles_as_err = np.array([
    # matplotlib expects [lower, upper]
    rel_error - np.percentile(rel_errors, 16, axis=0),
    np.percentile(rel_errors, 84, axis=0) - rel_error,
])
# %%
with rc_context(STYLES[STYLE]), console.status(f"Plotting spectrum…"):
    fig, axs = plt.subplots(
        2, 1,
        sharex=True,
        gridspec_kw={'height_ratios': [2, 1]},
    )

    # plt.hist(BINS[:-1], BINS, weights=spectrum_from_labels(labels), color='red', label='true class')

    if run.config['stratify_train'] or run.config['stratify_test']:  # untested
        axs[0].step(BIN_EDGES, train_spectrum, where='post', drawstyle='steps-mid',
                    color='C3', linewidth=2, label="training: true")
    axs[0].step(BIN_EDGES, true_spectrum, where='post', drawstyle='steps-mid', color='C1', linewidth=2, label="test: true")
    axs[0].step(BIN_EDGES, pred_spectrum, where='post', drawstyle='steps-mid', color='C0', zorder=10, label="test: predicted")

    # get the middle points of the bin edges
    # bin_centers = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2
    # NOTE: We need to account for the log scale
    bin_centers = np.exp((np.log(BIN_EDGES[:-1]) + np.log(BIN_EDGES[1:])) / 2)

    # manually set the last center, because we crop the plot…
    # bin_centers[-1] = (BIN_EDGES[-2] + PLOT_XLIM[1]) / 2
    bin_centers[-1] = np.exp((np.log(BIN_EDGES[-2]) + np.log(PLOT_XLIM[1])) / 2)

    axs[0].errorbar(bin_centers,
                    pred_spectrum[:-1],
                    yerr=pred_percentiles_as_err[:, :-1],
                    zorder=20,
                    linewidth=0,
                    elinewidth=1,
                    ecolor='C0',
                    )

    axs[0].set_ylabel(r"normalized \# of events")
    axs[0].set_yscale('log')
    axs[0].legend()

    axs[1].step(BIN_EDGES, rel_error, where='post', color='C2')
    axs[1].set_ylabel("relative deviation")
    axs[1].set_xscale('log')
    # axs[1].set_yscale('symlog')
    axs[1].set_xlabel(r"$\text{energy} \mathbin{/} \si{\giga\electronvolt}$")

    # for single_rel_error in rel_errors:
    #     axs[1].step(BIN_EDGES, single_rel_error, where='post', color='C2')

    axs[1].errorbar(bin_centers,
                    rel_error[:-1],
                    # yerr=pred_spectrum_error,
                    yerr=rel_error_percentiles_as_err[:, :-1],
                    drawstyle='steps-post',
                    # color='blue',
                    zorder=20,
                    # label="predicted probas (bootstrap median, 68%ile)"
                    linewidth=0,
                    elinewidth=1,
                    ecolor='C2',
                    )

    # print relative deviation in percent
    ore_offset = (axs[1].get_ylim()[1] - axs[1].get_ylim()[0]) * 0.025
    for onebin_center, onebin_rel_error in list(zip(bin_centers, rel_error)):
        # ore_textpos = onebin_rel_error + np.sign(onebin_rel_error) * 0.05/5
        ore_textpos = onebin_rel_error + np.sign(onebin_rel_error) * ore_offset
        axs[1].text(onebin_center, ore_textpos, f"{onebin_rel_error:.1%}",
                    fontsize=6,
                    va=('bottom' if onebin_rel_error > 0 else 'top'),
                    )

    # connect grid lines
    ax3 = fig.add_subplot(111, zorder=-1)
    for _, spine in ax3.spines.items():
        spine.set_visible(False)
    ax3.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
    ax3.set_xscale('log')
    ax3.get_shared_x_axes().join(ax3, axs[0])
    ax3.grid(axis='x')

    for ax in axs:
        # ax.set_xticks(BIN_EDGES)
        ax.set_xticks(XTICKS)
        ax.set_axisbelow(True)
        ax.grid()
        # Crop the x-axis so the overflow bin does not take up too much space;
        # suggestion by Karolin.
        ax.set_xlim(*PLOT_XLIM)

    # grey out under-/overflow
    # for ax in axs:
    for ax in plt.gcf().axes:
        COMMON_AXVSPAN_KWARGS = {
            'alpha': 0.3,
            'color': 'grey',
            # 'facecolor': 'grey', # Edges cause artifacts between subplots; but this looks at least as bad.
            'hatch': '///',
        }
        ax.axvspan(LOWER_LIMIT, BIN_EDGES[0], **COMMON_AXVSPAN_KWARGS)
        ax.axvspan(BIN_EDGES[-1], UPPER_LIMIT, **COMMON_AXVSPAN_KWARGS)

    sns.despine()
    plt.tight_layout()
    # %%
    # plt.savefig(PLOTS_DIR / f"bootstrap:spectrum_{STYLE}.pdf")
    plt.savefig(PLOTS_DIR / f"bias:spectrum_{STYLE}.pdf")
