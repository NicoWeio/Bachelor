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

PLOT_XLIM = (10**2, 10**5.5)

# XTICKS = np.logspace(np.log10(lower_limit), np.log10(upper_limit), NUM_BINS+1)
XTICKS = np.geomspace(10**2, 10**8, (8-2+1))

# %%
api = wandb.Api()

run = api.run("nicoweio/dsea-corn/24sfwi8p")
BIN_EDGES = np.array(run.summary['bin_edges'])
STYLE = 'full'
# %%
pred_spectra = np.vstack(run.summary['bootstrap/pred_spectra'])
true_spectra = np.vstack(run.summary['bootstrap/true_spectra'])

# %%
BIN_INDEX = 0

hist, edges = np.histogram(
    pred_spectra[:, BIN_INDEX],
    bins=10,
    # range=(0, 1),
    # density=True,
)
# %%
# plot the histogram
plt.bar(edges[:-1], hist, width=np.diff(edges), ec='k', align='edge')
plt.xlabel("TODO")
plt.ylabel("count")
# %%
