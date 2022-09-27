from pathlib import Path

from rich.console import Console

console = Console()

PLOTS_DIR = Path(__file__).parent / "../content/plots/"

BASE_HEIGHT = 3.64
BASE_WIDTH = 5.45

STYLES = {
    'full': {
        'figure.figsize': (BASE_WIDTH, BASE_HEIGHT),  # (ratio 3:2)
        'legend.fontsize': 'medium',
    },
    'halfheight': {
        'figure.figsize': (BASE_WIDTH, BASE_HEIGHT/2),
        'legend.fontsize': 'small',
    },
    'halfwidth': {
        'figure.figsize': (BASE_WIDTH/2, 3.84),
        'legend.fontsize': 'small',
    },
    'lessheight': {
        'figure.figsize': (BASE_WIDTH, BASE_HEIGHT*0.75),
        # 'figure.figsize': (5.45, 3.84*(2/3)), # previous value
        'legend.fontsize': 'small',
    },
    'small': {
        'figure.figsize': (BASE_WIDTH/2, BASE_HEIGHT/2),
        'legend.fontsize': 'small',
    },
    'doubleheight': {
        'figure.figsize': (BASE_WIDTH, BASE_HEIGHT*1.6),  # ⚠️ 1.8 NO, 1.6 YES, 1.7 NO
        'legend.fontsize': 'medium',
    },
}
