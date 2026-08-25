"""Run configuration read by `nozand` and `zand`.

Every name defined here is imported by the drivers -- see ../README.md for the
exact contract. Removing one of them is an ImportError, not a default.

`load_dictionary` runs at import, so <name>/Arrays/ must already exist: the
reference script writes it with C.tofile(<name>) before run.sh starts a driver.
"""
import numpy as np
import os
from Zandpack.Loader import load_dictionary
from Zandpack.td_constants import hbar          # honours ZANDPACK_HBAR

# Must match the argument given to C.tofile() in the reference script.
name          = 'TDT_Template'

eps           = 1e-8        # adaptive-step error tolerance
t0, t1        = 0, 100      # propagation interval
stepsize      = 0.1         # initial step; the controller adapts from here

usesave          = False    # resume from a previously saved state?
LoadFromFull     = False    # have the results of a previous run been stitched?
print_timings    = False

saveevery        = 50       # how often to write current and density matrix
checkpoints      = []       # times at which to dump the full system state
save_checkpoints = False    # whether to honour `checkpoints` at all

n_dm_compress    = 2        # keep every n-th density matrix
save_PI          = False    # store the Pi matrices (large)

steps_for_bondcurrent = 10

Adir = name + '/Arrays/'
Arrs = load_dictionary(Adir)
