import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rc_context

import sweep
from common import PLOTS_DIR, STYLES, console

PLOTS = [
    {
        'configvar': 'batch_size',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        'sweep_id': 'ci6ro33c',
    },
    {
        'configvar': 'epsilon',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        # 'sweep_id': 'ju79broz',  # new version with correct binning and batch_size=512
        'sweep_id': '61nuutm1',  # new version with correct binning and batch_size=4096
    },
    {
        'configvar': 'J',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        # 'sweep_id': ['ruwybza6', 'iqnnx67c'],
        'sweep_id': 'ruwybza6',
    },
    {
        'configvar': 'num_epochs',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        'sweep_id': 'zftou44c',
    },
]

AXIS_LABEL_MAP = {
    'wd': 'Wasserstein distance',
    # ---
    'batch_size': 'batch size',
    'J_factor': r'$J$-factor',
    'J': r'$J$',
    'num_epochs': 'number of epochs',
    'epsilon': r'convergence threshold $\epsilon$',
}

METRIC_OBJECTIVE_MAP = {
    'wd': 'min',
    'accuracy': 'max',
}

for i, plot in enumerate(PLOTS):
    # If sweep_id is a list, merge the results
    sweep_ids = (plot['sweep_id'] if isinstance(plot['sweep_id'], list) else [plot['sweep_id']])
    dfs = [sweep.get_sweep_df(sweep_id) for sweep_id in sweep_ids]
    df_single = pd.concat(dfs, ignore_index=True)

    # Manually add J (for old sweeps)
    if 'J' not in df_single.columns:
        df_single['J'] = df_single['J_factor'] * 10

    with rc_context(STYLES[plot['style']]), console.status(f"Plotting ({i+1}/{len(PLOTS)})…"):
        plt.figure()  # Important! Otherwise, the style is not updated.
        if plot['kind'] == 'boxplot':
            sns.boxplot(
                data=df_single, y=f"test/{plot['metricvar']}_single", x=plot['configvar'],
                color='C0',  # all boxes should be in the same color (tugreen)
            )

            # Plot an axhline for the smallest median
            medians = df_single.groupby(plot['configvar']).median()[f"test/{plot['metricvar']}_single"]
            best_val = getattr(medians, METRIC_OBJECTIVE_MAP[plot['metricvar']])()
            plt.axhline(best_val, color='C1', linestyle='--', zorder=-1)

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
        plt.savefig(PLOTS_DIR / "hyperparam" / filename)
        plt.clf()
