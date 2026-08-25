"""Run configuration read by `nozand` and `zand` -- see ../README.md."""
import numpy as np
import os
from Zandpack.Loader import load_dictionary
from Zandpack.td_constants import hbar          # honours ZANDPACK_HBAR

# Must match the argument given to C.tofile() in chain.py.
name          = 'TDT_Chain'

eps           = 1e-10
t0, t1        = 0, 60
stepsize      = 0.1

usesave          = False
LoadFromFull     = False
print_timings    = False

saveevery        = 50
checkpoints      = []
save_checkpoints = False

n_dm_compress    = 2
save_PI          = False

steps_for_bondcurrent = 10

Adir = name + '/Arrays/'
Arrs = load_dictionary(Adir)
