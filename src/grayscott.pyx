cimport cython

import numpy as np
cimport numpy as np

from scipy.signal import convolve2d

DTYPE = np.float32

cdef class GSSystem:

    def __init__(self, int n, double f, double k, double dA, double dB, double dt):
        self.A = np.ones((n, n), dtype=DTYPE)
        self.B = np.zeros((n, n), dtype=DTYPE)
        self._f = f
        self._k = k
        self._dA = dA
        self._dB = dB
        self._dt = dt

    cpdef void seed(self, int count, int duration):
        cdef int m, n, i
        cdef list ypts, xpts

        m = self.B.shape[0]
        n = self.B.shape[1]

        ypts = [m/2] + [np.random.randint(0,m) for i in xrange(count-1)]
        xpts = [n/2] + [np.random.randint(0,n) for i in xrange(count-1)]

        for i in xrange(duration):
            self.B[ypts, xpts] += 0.1
            self.update()

    cpdef void update(self):
        cdef np.ndarray lapA, lapB, conv, deltaA, deltaB
        cdef np.ndarray kernel = np.array(
            [[ 0.05, 0.20, 0.05 ],
             [ 0.20,-1.00, 0.20 ],
             [ 0.05, 0.20, 0.05 ]], dtype=DTYPE)

        lapA = convolve2d(self.A, kernel, mode="same", boundary="wrap")
        lapB = convolve2d(self.B, kernel, mode="same", boundary="wrap")
        conv = self.A * self.B * self.B
        deltaA = self._dA * lapA - conv + self._f * (1 - self.A)
        deltaB = self._dB * lapB + conv - (self._k + self._f) * self.B
        self.A += self._dt * deltaA
        self.B += self._dt * deltaB
