import os
import sys
import time
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation

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

def animate_gs(gs, cm, vmn, vmx, frame_step=None):
    fig = plt.figure()
    im = plt.imshow(gs.B, cmap=cm, vmin=vmn, vmax=vmx)

    try:
        img_dir = "./img/grayscott-{}".format(int(time.time()))
        os.mkdir(img_dir)

    except IOError:
        frame_step = None
        print "To save frames of animation, run main.py from the grayscott directory."

    def anim_func(t):
        gs.update()
        im.set_data(gs.B)

        if frame_step > 0 and t % frame_step == 0:
            plt.savefig(img_dir + "/grayscott-{}.png".format(t),
                        bbox_inches="tight")

        return im

    anim = animation.FuncAnimation(fig, anim_func, interval=0)
    plt.show()
