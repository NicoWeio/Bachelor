# %%
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

BINS = list(range(10))
true_spectrum = np.random.normal(5, 0.1, 10)
true_spectrum /= np.sum(true_spectrum)
pred_spectrum = np.random.normal(3, 0.1, 10)
pred_spectrum /= np.sum(pred_spectrum)

# %%
fig, axs = plt.subplots(2, 1, sharex=True)  # figsize=(10, 6)

# plt.hist(BINS[:-1], BINS, weights=spectrum_from_labels(labels), color='red', label='true class')

axs[0].plot(BINS, true_spectrum, drawstyle='steps-mid', color='C1', linewidth=2, label='true class')
# axs[0].plot(BINS, spectrum_from_labels(predicted_labels), drawstyle='steps-mid', color='royalblue', label='predicted class')
axs[0].plot(BINS, pred_spectrum, drawstyle='steps-mid', color='C0', zorder=10, label='predicted probas')
axs[0].set_ylabel('count') # TODO
axs[0].set_yscale('log')
axs[0].legend()


axs[1].bar(BINS, (pred_spectrum - true_spectrum) / true_spectrum, color='C2')
axs[1].set_ylabel('relative deviation')

for ax in axs:
    ax.set_xlabel('class')
    ax.set_xticks(BINS)
    ax.set_axisbelow(True)
    ax.grid()

sns.despine()
plt.tight_layout()
plt.savefig('../content/plots/bootstrap:spectrum.pdf')
# %%
# TODO: Für single_events / per_bin_spectra: https://seaborn.pydata.org/tutorial/axis_grids.html
