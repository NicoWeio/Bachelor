import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc_context

import sweep
from common import PLOTS_DIR, STYLES, console
from pcp import pcp

runs = sweep.get_sweep_rundata('hx0w5y4a')
df = pd.DataFrame([dict(run.summary) | dict(run.config) for run in runs])
# For some reason, not all "finished" runs worked properly. This should not be necessary, but is.
df.dropna(subset=['test/wd_mean'], inplace=True)
# ⚠️ Drop rows with test/wd_mean > 0.011 → should affect only 1 run
df = df[df['test/wd_mean'] <= 0.011]

STYLE = 'full'

label_tuples = [
    (
        'batch_size',
        "batch\nsize",
        'categorical',
    ),
    (
        'epsilon',
        ("convergence\nthreshold " r"$\epsilon$"),
        'log',
    ),
    (
        'learning_rate',
        "learning\nrate",
        'linear',
    ),
    (
        'num_epochs',
        "epochs",
        'linear',
    ),
    (
        'test/wd_mean',
        "Wasserstein distance\n(mean)",
        'linear',
    ),
]

labels, labels_plt, ytypes = zip(*label_tuples)
# labels = list(labels)
# labels_plt = list(labels_plt)
# ytypes = list(ytypes)


data = df[list(labels)].values.tolist()

with rc_context(STYLES[STYLE]), console.status(f"Plotting spectrum…"):
    fig = pcp(
        data,
        # labels,
        labels_plt,
        # alpha=0.5,
        # ytype=['categorical', 'log', 'linear', 'linear', 'linear'],
        ytype=ytypes,
        # ylabels=['Batch Size', 'Epsilon', 'Learning Rate', 'Num Epochs', 'Weight Decay'],
    )
    fig.savefig(PLOTS_DIR / "hyperparam" / f"combined_pcplot_{STYLE}.pdf")
