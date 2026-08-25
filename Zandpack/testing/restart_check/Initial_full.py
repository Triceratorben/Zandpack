"""Control run: 0 -> 10 uninterrupted.

`eps` and `stepsize` are deliberately identical to Initial_leg1.py and
Initial_leg2.py. An adaptive integrator run at a different tolerance takes a
different sequence of steps, so mismatched settings would make the control and
the legs disagree whether or not restarting works.

run.sh copies this over Initial.py before the run -- see ../README.md.
"""
import numpy as np
import os
from Zandpack.Loader import load_dictionary
from Zandpack.td_constants import hbar          # honours ZANDPACK_HBAR

name          = 'TDT_Restart'

eps           = 1e-8
t0, t1        = 0, 10
stepsize      = 0.1

usesave          = False
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
