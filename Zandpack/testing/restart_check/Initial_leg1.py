"""Leg 1: 0 -> 6, dumping a full system state when the run passes t = 5.

`checkpoints` must lie strictly inside (t0, t1): the driver does
`checkpoints = np.array(checkpoints)` and then filters with `> t0` and `< t1`,
so a checkpoint at either endpoint is silently dropped and leg 2 has nothing to
resume from. t1 is 6 rather than 5 so the checkpoint is comfortably inside; the
5 -> 6 stretch is simply redone by leg 2 and shows up as a short overlap in
compare.py.

`eps` and `stepsize` match Initial_full.py and Initial_leg2.py.
"""
import numpy as np
import os
from Zandpack.Loader import load_dictionary
from Zandpack.td_constants import hbar          # honours ZANDPACK_HBAR

name          = 'TDT_Restart'

eps           = 1e-8
t0, t1        = 0, 6
stepsize      = 0.1

usesave          = False
LoadFromFull     = False
print_timings    = False

saveevery        = 50
checkpoints      = [5.0]        # must match TMID in restart.py
save_checkpoints = True

n_dm_compress    = 1
save_PI          = False

steps_for_bondcurrent = 10

Adir = name + '/Arrays/'
Arrs = load_dictionary(Adir)
