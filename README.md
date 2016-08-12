# GrayScott
Library for modeling a Gray-Scott reaction-diffusion system. If problems arise from matplotlib's backend, try installing QtPy or GTK.

![](/img/output_NaVWV5.gif?raw=true "animation")

Dependencies include:

*    `numpy`
*    `scipy`
*    `cython`
*    `matplotlib`

To install, run:

    $ python setup.py install

The following are all valid uses of GrayScott:
    
    $ python main.py
    $ python main.py n=80
    $ python main.py f=0.031 k=0.059 n=80

Command line options include:

    [n], the size of the grid;
    [f], the feed rate of A into the system;
    [k], the kill rate of B from the system;
    [dA/dB], the rates of diffusion, typically with ratio dA / dB = 2.
