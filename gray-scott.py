import string, time, random
import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage, signal
from PIL import Image

def update(A, B, dA, dB, f, k, dt=0.5, kernel=np.array(
         [[ 0.104, 0.146, 0.104 ],
          [ 0.146,-1.000, 0.146 ],
          [ 0.104, 0.146, 0.104 ]])):
    lapA = signal.convolve2d(A, kernel, mode='same', boundary='wrap')
    lapB = signal.convolve2d(B, kernel, mode='same', boundary='wrap')
    return A + dt * (dA * lapA - A * B * B + f * (1 - A)),\
           B + dt * (dB * lapB + A * B * B - (k + f) * B)

def randseed(A, B, dA, dB, f, k, dt=0.5, count=10, duration=30):
    m, n = B.shape
    ps = [(random.randint(0,m-1), random.randint(0,n-1)) for i in range(count)]
    for i in range(duration):
        for (m,n) in ps:
            B[m,n] += 0.1
        A, B = update(A, B, dA, dB, f, k, dt)
    return A, B

def arr_stretch(arr, shape):
    m0, n0 = arr.shape
    m1, n1 = shape
    return np.kron(arr, [[1] * (n1 / n0)] * (m1 / m0))

def save_png(arr, filename, mapper, size, smooth=True):
    temp = arr_stretch(arr, (size, size))
    if smooth:
        temp = ndimage.gaussian_filter(temp, 2)
    im = Image.fromarray(np.uint8(mapper.to_rgba(temp)*255))
    im = im.resize((size, size))
    im.save(filename)

if __name__ == "__main__":
    NORM      = plt.Normalize(vmin=0, vmax=0.336)
    CMAPPER   = plt.cm.ScalarMappable(norm=NORM, cmap=plt.cm.magma)
    GRID_SIZE = 500
    MAX_TIME  = 18000

    A = np.ones((GRID_SIZE, GRID_SIZE))
    B = np.zeros((GRID_SIZE, GRID_SIZE))

    dA = 1.0
    dB = 0.5
    f = 0.037
    k = 0.059

    f_str = string.zfill(int(f*10**5), 5)
    k_str = string.zfill(int(k*10**5), 5)

    A, B = randseed(A, B, dA, dB, f, k)

    for n in range(MAX_TIME+1):
        A, B = update(A, B, dA, dB, f, k)
        if n % (MAX_TIME / 300) == 0:
            filename = "grayscott-%s-%s-%d.png" % (f_str, k_str, n)
            #filename = "grayscott-%d.png" % int(time.time())
            save_png(B, filename, CMAPPER, 1000, False)
            #save_png(B, filename, CMAPPER, 1000, False)
