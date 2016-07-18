import sys
import matplotlib

matplotlib.rcParams["backend"] = "Qt4Agg"

import matplotlib.pyplot as plt
from grayscott import GSSystem


def get_colormap():
    if matplotlib.__version__ >= "1.5.1":
        return plt.cm.magma
    else:
        return plt.cm.afmhot

def handle_cli_input(default_kwargs):
    kwargs = default_kwargs.copy()
    try:
        f_args = map(lambda f_arg: f_arg.split("="), sys.argv[1:])
        for key, val in f_args:
            assert(key in default_kwargs.keys())
            kwargs[key] = eval(val)

    except (TypeError, AssertionError, ValueError):
        print "Bad usage, using default values."
        kwargs = default_kwargs.copy()

    return kwargs

def main():
    default_kwargs = {
        'n': 100,
        'f': 0.016,
        'k': 0.041,
        'dA': 0.64,
        'dB': 0.32
    }

    kwargs = handle_cli_input(default_kwargs)

    CMAP = get_colormap()
    SIZE = kwargs["n"]

    seed_count = (SIZE*SIZE / 900) + 1

    gs = GSSystem(**kwargs)
    gs.seed(seed_count)
    gs.animate(CMAP)

if __name__ == "__main__":
    main()
