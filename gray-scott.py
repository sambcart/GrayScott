#### Libraries
# Standard library
import random

# Third-party libraries
import numpy as np
import matplotlib

from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import signal

matplotlib.rcParams["backend"] = "Qt4Agg"


class GSSystem(object):

    def __init__(self, A, B, f, k, dA, dB, dt=1):
        self.A = A
        self.B = B
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

    def animate(self):
        fig = plt.figure()
        im = plt.imshow(self.B, cmap=plt.cm.magma, vmin=0, vmax=0.3375)

        def anim_func(_):
            self.update()
            im.set_data(self.B)
            return im

        anim = animation.FuncAnimation(fig, anim_func, interval=1)
        plt.show()


if __name__ == "__main__":
    gs = GSSystem(np.ones((80, 80)),
                  np.zeros((80, 80)),
                  0.03,
                  0.062,
                  0.64,
                  0.32)

    gs.seed(5)
    gs.animate()
