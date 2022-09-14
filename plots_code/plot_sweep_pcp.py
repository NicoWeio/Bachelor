import matplotlib.pyplot as plt
import pandas as pd

import sweep
from pcp import pcp

# df = sweep.get_sweep_df('zftou44c')

runs = sweep.get_sweep_rundata('zftou44c')
df = pd.DataFrame([dict(run.summary) | dict(run.config) for run in runs])


labels = ['batch_size', 'epsilon', 'learning_rate', 'num_epochs', 'test/wd_mean']
labels_plt = ['batch size', r'convergence threshold $\epsilon$', 'learning rate', 'epochs', 'Wasserstein distance (mean)']
data = df[labels].values.tolist()

fig = pcp(
    data,
    # labels,
    labels_plt,
    # alpha=0.5,
    ytype=['categorical', 'log', 'linear', 'linear', 'linear'],
    # ylabels=['Batch Size', 'Epsilon', 'Learning Rate', 'Num Epochs', 'Weight Decay'],
)


fig.savefig('../content/plots/hyperparam/combined_pcplot_full.pdf')
