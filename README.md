# GrayScott
Library for modeling a Gray-Scott reaction-diffusion system using numpy, scipy, and matplotlib. If problems arise from matplotlib's backend, either install QtPy, GTK, or try your luck with "template"...

The following are all valid uses of grayscott.py:
    
    $ python grayscott.py
    $ python grayscott.py n=80
    $ python grayscott.py f=0.031 k=0.059 n=80

Command line options include:

    [n], the size of the grid;
    [f], the feed rate of A into the system;
    [k], the kill rate of B from the system;
    [dA/dB], the rates of diffusion, typically with ratio dA / dB = 2.
