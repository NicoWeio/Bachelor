from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from matplotlib import rc_context

from common import PLOTS_DIR, STYLES, console

PLOTS = [
    {
        'name': "dataset:raw:histogram",
        'style': 'full',
    },
    {
        'name': "dataset_500k:discretized:histogram",
        'style': 'full',
    },
]

for i, plot in enumerate(PLOTS):
    with open(f"data/{plot['name']}.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with rc_context(STYLES[plot['style']]), console.status(f"Plotting ({i+1}/{len(PLOTS)})…"):
        plt.hist(
            config['bin_edges'][:-1], bins=config['bin_edges'], weights=config['hist'],
            edgecolor='black',
            # linewidth=1.2,
        )
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(r'\texttt{MCPrimary.energy} \mathbin{/} \si{\giga\electronvolt}')
        plt.ylabel(r'Count')
        plt.grid()
        plt.gca().set_axisbelow(True)
        # sns.despine()
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / f"{plot['name']}_{plot['style']}.pdf")
        plt.clf()
