cimport cython

import numpy as np
cimport numpy as np

cdef class GSSystem:
    
    cdef public np.ndarray A, B
    cdef double _f, _k, _dA, _dB, _dt

    cpdef void seed(self, int count, int duration)
    cpdef void update(self)
