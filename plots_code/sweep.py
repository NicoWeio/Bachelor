import pandas as pd
import wandb
from rich.console import Console

console = Console()


api = wandb.Api(timeout=30) # :/


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
