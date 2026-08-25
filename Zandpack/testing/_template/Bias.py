"""Time-dependent driving, read by `nozand` and `zand`.

All three of `bias`, `dH` and `dissipator` are imported by the drivers. Define
all three even when one is trivial.

Keep these identical to whatever the reference script integrates -- if the two
drift apart, the comparison in compare.py silently compares different physics.
The cleanest way to guarantee that is for the reference script to import them
from here rather than redefining them.
"""
import numpy as np
from numba import njit


@njit
def bias(t, a):
    """Electrochemical potential shift of electrode `a` at time `t`."""
    if a == 0:
        return 0.0
    return 0.0


@njit
def dH(t, sig):
    """Addition to the device Hamiltonian. `sig` is the density matrix, so this
    is where any density dependence (Hubbard, Hartree, ...) goes."""
    out = np.zeros(sig.shape, dtype=np.complex128)
    return out


def dissipator(t, s):
    return 0.0
