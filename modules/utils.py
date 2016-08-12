import sys
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
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

def animate_gs(gs, cm, vmn, vmx):
    fig = plt.figure()
    im = plt.imshow(gs.B, cmap=cm, vmin=vmn, vmax=vmx)

    def anim_func(_):
        gs.update()
        im.set_data(gs.B)
        return im

    anim = animation.FuncAnimation(fig, anim_func, interval=0)
    plt.show()
