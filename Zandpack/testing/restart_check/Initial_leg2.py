"""Leg 2: resume from leg 1's checkpoint and run on to 10.

`usesave = True` with `LoadFromFull = False` makes the driver read, from
<name>_save/:

    last_sig.npy, last_time.npy, last_stepsize.npy   (rank 0)
    last_Psi_Worker<N>.npy, last_Omg_Worker<N>.npy   (each worker rank)

so `t0` below is only a fallback if those files are missing -- the real start
time comes from last_time.npy.

Two consequences, both handled in run.sh:

  * <name>_save must still be in place when this leg starts, so run.sh *copies*
    leg 1's output aside rather than moving it.
  * the worker files are per-rank and their shapes are asserted on load, so
    leg 2 must run with the same number of MPI ranks as leg 1.

`eps` and `stepsize` match Initial_full.py and Initial_leg1.py.
"""
import numpy as np
import os
from Zandpack.Loader import load_dictionary
from Zandpack.td_constants import hbar          # honours ZANDPACK_HBAR

name          = 'TDT_Restart'

eps           = 1e-8
t0, t1        = 5, 10           # t0 overridden by last_time.npy
stepsize      = 0.1

usesave          = True
LoadFromFull     = False
print_timings    = False

saveevery        = 50
checkpoints      = []
save_checkpoints = False

n_dm_compress    = 1
save_PI          = False

steps_for_bondcurrent = 10

Adir = name + '/Arrays/'
Arrs = load_dictionary(Adir)
