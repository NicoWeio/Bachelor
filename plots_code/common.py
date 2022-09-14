from pathlib import Path

from rich.console import Console

console = Console()

PLOTS_DIR = Path(__file__).parent / "../content/plots/"
# if len(sys.argv) > 1:
#     PLOTS_DIR /= sys.argv[1]


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
    'doubleheight': {
        'figure.figsize': (5.45, 3.64*2),
        'legend.fontsize': 'medium',
    },
}
