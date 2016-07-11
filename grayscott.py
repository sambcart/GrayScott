"""
grayscott.py
~~~~~~~~~~~~

Library for modeling a Gray-Scott reaction-diffusion
system using numpy, scipy, and matplotlib. If problems
arise from matplotlib's backend, either install QtPy, GTK,
or try your luck with "template"...

Usage only allows for variables in default_kwargs to be
modified:

    [n] is the size of the grid,
    [f] is the feed rate of A into the system,
    [k] is the kill rate of B from the system,
    [dA/dB] are the rates of diffusion, typically with
      ratio dA / dB = 2.

The following are all valid uses of grayscott.py:
    
    $ python grayscott.py
    $ python grayscott.py n=80
    $ python grayscott.py f=0.031 k=0.059 n=80
"""

#### Libraries
# Standard libraries
import sys
import math
import random

# Third-party libraries
import numpy as np
import matplotlib

matplotlib.rcParams["backend"] = "Qt4Agg"

from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import signal


class GSSystem(object):

    def __init__(self, n, f, k, dA, dB, dt=1):
        self.A = np.ones((n, n))
        self.B = np.zeros((n, n))
        self.f = f
        self.k = k
        self.dA = dA
        self.dB = dB
        self.dt = dt

    def seed(self, count, duration=30):
        m, n = self.B.shape
        ypts = [m/2] + [random.randint(0, m-1) for i in xrange(count-1)]
        xpts = [n/2] + [random.randint(0, n-1) for i in xrange(count-1)]
        for i in xrange(duration):
            self.B[ypts, xpts] += 0.1
            self.update()

    def update(self, kernel=np.array(
              [[ 0.05, 0.20, 0.05 ],
               [ 0.20,-1.00, 0.20 ],
               [ 0.05, 0.20, 0.05 ]])):
        lapA = signal.convolve2d(self.A, kernel, mode="same", boundary="wrap")
        lapB = signal.convolve2d(self.B, kernel, mode="same", boundary="wrap")
        conv = self.A * self.B * self.B
        delta_A = self.dA * lapA - conv + self.f * (1 - self.A)
        delta_B = self.dB * lapB + conv - (self.k + self.f) * self.B
        self.A += self.dt * delta_A
        self.B += self.dt * delta_B

    def animate(self, CMAP, VMIN=0, VMAX=0.4):
        fig = plt.figure()
        im = plt.imshow(self.B, cmap=CMAP, vmin=VMIN, vmax=VMAX)

        def anim_func(_):
            self.update()
            im.set_data(self.B)
            return im

        anim = animation.FuncAnimation(fig, anim_func, interval=0)
        plt.show()


def get_colormap():
    if matplotlib.__version__ >= "1.5.1":
        return plt.cm.magma
    else:
        return plt.cm.afmhot

if __name__ == "__main__":

    # Default values
    default_kwargs = {
        'n': 100,
        'f': 0.016,
        'k': 0.041,
        'dA': 0.64,
        'dB': 0.32
    }

    kwargs = default_kwargs.copy()

    try:
        f_args = map(lambda f_arg: f_arg.split("="), sys.argv[1:])

        for key, val in f_args:
            assert(key in default_kwargs.keys())
            kwargs[key] = float(val)

    except (TypeError, AssertionError, ValueError):
        print "Bad usage, using default values."
        kwargs = default_kwargs.copy()

    cmap = get_colormap()
    size = kwargs["n"]
    seed_count = int(math.ceil(size * size / 900))

    gs = GSSystem(**kwargs)
    gs.seed(seed_count)
    gs.animate(cmap)
