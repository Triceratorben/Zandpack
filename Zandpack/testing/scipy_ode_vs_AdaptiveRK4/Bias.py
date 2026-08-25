"""Time-dependent driving, read by `nozand`, `zand` and by chain.py.

Was previously split across shared.py (which named the bias `delta`) and a
Bias.py that only aliased it. Both drivers and the reference script now import
from here, so they cannot disagree.
"""
import numpy as np
from numba import njit


@njit
def bias(t, a):
    if a == 0:
        return +np.sin(t / 20)
    return -np.sin(t / 20)


@njit
def dH(t, sigma):
    out = np.zeros(sigma.shape, dtype=sigma.dtype)
    out[0,  0,  0] = np.sin(t / 10)
    out[0,  5,  5] = np.sin(t / 6)
    out[0, 13, 13] = np.sin(t / 2)
    return out


def dissipator(t, s):
    return 0.0
