from Cython.Build import cythonize
from Cython.Distutils import build_ext

import numpy as np

try:
    from setuptools import setup
    from setuptools.extension import Extension

except Exception:
    from distutils.core import setup
    from distutils.extension import Extension

_extra = [ '-O3' , '-ffast-math' ]

exts = [
    Extension('grayscott',
              sources=['./src/grayscott.pyx'],
              include_dirs=[np.get_include()],
              extra_compile_args=_extra)]

setup(
    name = "grayscott",
    cmdclass = {"build_ext": build_ext},
    inlude_dirs = [np.get_include()],
    ext_modules = cythonize(exts))
