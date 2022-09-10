import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc_context
import pandas as pd
import seaborn as sns
import wandb

PLOTS_DIR = Path(__file__).parent / "../content/plots/hyperparam/"
# if len(sys.argv) > 1:
#     PLOTS_DIR /= sys.argv[1]

api = wandb.Api()
sweep_id = 'zftou44c'
sweep = api.sweep(f"nicoweio/dsea-corn/{sweep_id}")

# filter successful runs
runs = list(filter(lambda run: run.state == 'finished', sweep.runs))

print(f"{len(sweep.runs)} total runs, {len(runs)} finished")

# Each run has multiple values for metrics like wd_all
# Create a new dataframe with one row per *metric*
# The columns shall get the suffix '_single', e.g. wd_all_single

data_list = []
for run in runs:
    metric_keys = [key for key in run.summary.keys() if key.endswith('_all')]
    metric_lengths = [len(run.summary[key]) for key in metric_keys]
    assert len(set(metric_lengths)) == 1, "Not all metrics have same length"
    for i in range(metric_lengths[0]):
        data = {}
        for key in metric_keys:
            newkey = key.replace('_all', '_single')
            data[newkey] = run.summary[key][i]
        data_list.append(
            data | dict(run.config)
        )

df_single = pd.DataFrame(data_list)


PLOTS = [
    {
        'configvar': 'batch_size',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'full',
    },
    {
        'configvar': 'J_factor',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'full',
    },
    {
        'configvar': 'epsilon',
        'metricvar': 'wd',
        'kind': 'scatterplot',
        'style': 'full',
    },
]

STYLES = {
    'full': {
        'figure.figsize': (5.45, 3.64),  # (ratio 3:2)
        'legend.fontsize': 'medium',
    },
    'half': {
        'figure.figsize': (5.45/2, 3.84),
        'legend.fontsize': 'small',
    },
    'small': {
        'figure.figsize': (5.45/2, 3.64/2),
        'legend.fontsize': 'small',
    },
}

for plot in PLOTS:
    with rc_context(STYLES[plot['style']]):
        plt.figure()  # Important! Otherwise, the style is not updated.
        if plot['kind'] == 'boxplot':
            sns.boxplot(data=df_single, y=f"test/{plot['metricvar']}_single", x=plot['configvar'])
        elif plot['kind'] == 'scatterplot':
            sns.scatterplot(data=df_single, y=f"test/{plot['metricvar']}_single", x=plot['configvar'], s=100, marker='s')

        sns.despine()
        # plt.title(f"{plot['configvar']} vs {plot['metricvar']}")
        plt.xlabel(plot['configvar'])
        plt.ylabel(plot['metricvar'])
        plt.grid(zorder=0, axis=('y' if plot['kind'] == 'boxplot' else 'both'))
        plt.tight_layout()
        filename = f"{plot['configvar']}_vs_{plot['metricvar']}_{plot['kind']}_{plot['style']}.pdf"
        plt.savefig(PLOTS_DIR / filename)
        plt.clf()
