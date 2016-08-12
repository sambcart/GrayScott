import matplotlib
matplotlib.rcParams["backend"] = "Qt4Agg"

if __name__ == "__main__":
    from modules.utils import *
    from grayscott import GSSystem

    SURF_SIZE = 200
    FEED_RATE = 0.016
    KILL_RATE = 0.041
    DIFF_A    = 0.64
    DIFF_B    = 0.32
    DELTA_T   = 1.0

    SEED_CT   = (SURF_SIZE * SURF_SIZE / 900) + 1
    SEED_DUR  = 30

    CMAP = get_colormap()
    VMIN = 0
    VMAX = 0.4

    DEFAULT_GS_KWARGS = {
        "n": SURF_SIZE,
        "f": FEED_RATE,
        "k": KILL_RATE,
        "dA": DIFF_A,
        "dB": DIFF_B,
        "dt": DELTA_T
    }

    gs_kwargs = handle_cli_input(DEFAULT_GS_KWARGS)

    gs = GSSystem(**gs_kwargs)
    gs.seed(SEED_CT, SEED_DUR)
    
    animate_gs(gs, CMAP, VMIN, VMAX)
