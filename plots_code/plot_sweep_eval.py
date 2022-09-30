import matplotlib.pyplot as plt
import numpy as np
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
        'sweep_id': 'ef962wf1',  # v3
    },
    {
        'configvar': 'epsilon',
        # 'configvar_filter': lambda x: x <= 1e-4 or str(x).endswith(('1', '05')),
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        'sweep_id': [
            '5efslxfk',  # v3
            'r1p3zu52',  # v3, extra values
        ],
    },
    {
        'configvar': 'J',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        # 'sweep_id': ['ruwybza6', 'iqnnx67c'],
        'sweep_id': [
            '8b5afo8h',  # v3
            'w8vdkf4x',  # v3, extra values
        ],
    },
    {
        'configvar': 'num_epochs',
        'metricvar': 'wd',
        'kind': 'boxplot',
        'style': 'lessheight',
        'sweep_id': [
            '2alop93j',  # v3
            '19h34dc7',  # v3, extra values
        ],
    },
]

# PLOTS = [PLOTS[1]]

AXIS_LABEL_MAP = {
    'wd': 'Wasserstein distance',
    # ---
    'batch_size': 'batch size',
    'J_factor': r'$J$-factor',
    'J': r'number of clusters $J$',
    'num_epochs': 'number of epochs',
    'epsilon': r'convergence threshold $\epsilon$',
}

METRIC_OBJECTIVE_MAP = {
    'wd': 'min',
    'accuracy': 'max',
}


def listify(x):
    if isinstance(x, list):
        return x
    return [x]


for i, plot in enumerate(PLOTS):
    # If sweep_id is a list, merge the results
    sweep_ids = listify(plot['sweep_id'])
    dfs = [sweep.get_sweep_df(sweep_id) for sweep_id in sweep_ids]
    df_single = pd.concat(dfs, ignore_index=True)

    # Manually add J (for old sweeps)
    if 'J' not in df_single.columns:
        df_single['J'] = df_single['J_factor'] * 10

    # Apply configvar filter
    if 'configvar_filter' in plot:
        filter_mask = np.array([plot['configvar_filter'](x) for x in df_single[plot['configvar']]])
        df_single = df_single[filter_mask]
        assert len(df_single) > 0, "No data left after filtering"

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
