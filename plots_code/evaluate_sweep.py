import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc_context
import pandas as pd
import seaborn as sns
import wandb
from rich.console import Console
console = Console()

PLOTS_DIR = Path(__file__).parent / "../content/plots/hyperparam/"
# if len(sys.argv) > 1:
#     PLOTS_DIR /= sys.argv[1]
# CACHE_DIR = Path(__file__).parent / "cache"

api = wandb.Api()


def get_sweep_rundata(sweep_id: str):
    with console.status(f"Getting sweep data for {sweep_id}…"):
        sweep = api.sweep(f"nicoweio/dsea-corn/{sweep_id}")

    # filter successful runs
    runs = list(filter(lambda run: run.state == 'finished', sweep.runs))

    print(f"Loaded sweep {sweep_id}: {len(sweep.runs)} total runs, {len(runs)} finished")
    return runs


SWEEP_CACHE = {}


def get_sweep_df(sweep_id: str):
    # Each run has multiple values for metrics like wd_all
    # Create a new dataframe with one row per *metric*
    # The columns shall get the suffix '_single', e.g. wd_all_single
    if sweep_id in SWEEP_CACHE:
        return SWEEP_CACHE[sweep_id]

    runs = get_sweep_rundata(sweep_id)

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
    SWEEP_CACHE[sweep_id] = df_single
    return df_single


PLOTS = [
    {
        'configvar': 'batch_size',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'full',
        'sweep_id': 'rncluvl4',
        # 'sweep_id': 'zftou44c',  # TEST
    },
    {
        'configvar': 'epsilon',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'full',
        'sweep_id': '8lyjmuch',
        # 'sweep_id': 'zftou44c',  # TEST
    },
    # {
    #     'configvar': 'J_factor',
    #     'metricvar': 'wd',
    #     'kind': 'boxplot',
    #     'style': 'full',
    #     'sweep_id': 'zftou44c',
    # },
    # {
    #     'configvar': 'num_epochs',
    #     'metricvar': 'wd',
    #     'kind': 'boxplot',
    #     'style': 'full',
    #     'sweep_id': 'zftou44c',
    # },
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

AXIS_LABEL_MAP = {
    'wd': 'Wasserstein distance',
    # ---
    'batch_size': 'Batch size',
    'J_factor': r'$J$-factor',
    'num_epochs': 'Number of epochs',
    'epsilon': r'$\epsilon$',
}

for i, plot in enumerate(PLOTS):
    df_single = get_sweep_df(plot['sweep_id'])

    with rc_context(STYLES[plot['style']]), console.status(f"Plotting ({i+1}/{len(PLOTS)})…"):
        plt.figure()  # Important! Otherwise, the style is not updated.
        if plot['kind'] == 'boxplot':
            sns.boxplot(
                data=df_single, y=f"test/{plot['metricvar']}_single", x=plot['configvar'],
                color='C0',  # all boxes should be in the same color (tugreen)
            )
        elif plot['kind'] == 'scatterplot':
            sns.scatterplot(
                data=df_single, y=f"test/{plot['metricvar']}_single", x=plot['configvar'],
                s=100, marker='s',
            )

        sns.despine()
        # plt.title(f"{plot['configvar']} vs {plot['metricvar']}")
        plt.xlabel(AXIS_LABEL_MAP.get(plot['configvar'], plot['configvar']))
        plt.ylabel(AXIS_LABEL_MAP.get(plot['metricvar'], plot['metricvar']))
        plt.gca().set_axisbelow(True)  # zorder doesn't work for some reason
        plt.grid(axis=('y' if plot['kind'] == 'boxplot' else 'both'))
        plt.tight_layout()
        filename = f"{plot['configvar']}_vs_{plot['metricvar']}_{plot['kind']}_{plot['style']}.pdf"
        plt.savefig(PLOTS_DIR / filename)
        plt.clf()
