"""Checkpoint/restart reproducibility on a 1D tight-binding chain.

run.sh propagates this device three times with `nozand`:

    full  : 0 -> T1 in one go
    leg 1 : 0 -> TMID + a little, dumping a full system state at TMID
    leg 2 : restarts from that state (usesave=True) and runs on to T1

compare.py then stitches leg 1 and leg 2 and overlays them on the full run. If
restarting is lossless the two traces lie on top of each other.

This script provides the device and the single-process reference solution.

Note on history: the older Full.py / 1Half.py / 2Half.py trio tested the same
idea through the *Python* integrator's restart path (passing sig0=psi0=omega0=
None so AdaptiveRK4_Opti reloads Chain_last_*.npy). It loaded a `Graw.Timedep`
pickle that is not in the repository -- it came from
scipy_ode_vs_Adaptive_PBC/device.py, which needs a full SIESTA run. The device
below is a self-contained tight-binding replacement, so the scenario no longer
depends on a fixture nobody can regenerate.

That trio also compared runs taken with *different* integrators and *different*
tolerances (Full.py used AdaptiveRK4 at eps=1e-5, h=0.1; the halves used
AdaptiveRK4_Opti at eps=1e-8, h=0.01), which would have made full and halves
differ whether or not restarting worked. Here every leg uses the same eps and
stepsize -- see Initial_full.py and Initial_leg{1,2}.py.
"""
import numpy as np
import sisl

from Zandpack.TimedependentTransport import TD_Transport, AdaptiveRK4
from Zandpack.td_constants import hbar as print_hbar

# The drivers read these same two from Bias.py.
from Bias import bias, dH

# hbar comes from the ZANDPACK_HBAR environment variable, exported by run.sh.
print('hbar is currently set to ', print_hbar)

NAME   = 'TDT_Restart'
T0, T1 = 0.0, 10.0
TMID   = 5.0        # must match `checkpoints` in Initial_leg1.py
EPS    = 1e-8       # must match `eps` in all three Initial_*.py

t_dev     = 1
t_elec    = 1
lat_const = 1.0

line = np.linspace(-2, 2, 151) + 1j * 1e-2
line = np.vstack((line, line))

# ------------------------------------------------------------------ geometry
# 20-orbital chain. dH in Bias.py drives orbitals 0, 5 and 13, so the device
# must be at least 14 orbitals wide.
c = sisl.geom.sc(lat_const, 'H').tile(3, 1).add_vacuum(10, 1).add_vacuum(10, 2)
c.set_nsc((3, 1, 1))
for i in range(c.no):
    c.atoms[i] = sisl.Atom('H', R=2.0)

geom_dev = c.tile(7, 0)
geom_em  = c.copy()
geom_ep  = c.copy().move(geom_dev.cell[0, :] - geom_em.cell[0, :])
geom_dev = geom_dev.remove([10])

C = TD_Transport([geom_em, geom_ep], geom_dev, kT_i=[0.05, 0.05])
C.Make_Contour(line, 15, pole_mode='JieHu2011')

C.Electrodes(semi_infs=['-a1', '+a1'])
C.make_device(elec_inds=[[i for i in range(3)], [i + 17 for i in range(3)]])

elec = sisl.Hamiltonian(c)
elec.construct([[0.1, lat_const * 1.1],
                [0,   t_elec]])
C.run_electrodes(manual_H=[elec, elec])

dev_H = sisl.Hamiltonian(geom_dev)
dev_H.construct([[0.1, lat_const * 1.1],
                 [0,   t_dev]])
C.run_device(manual_H=dev_H)
C.read_data()

C.Fit(fact          = 2.0,
      NumL          = 5,
      fit_mode      = 'all',
      force_PSD     = True,
      force_PSD_tol = [0.0, 0.0],
      min_method    = 'SLSQP',
      ebounds       = (-2, 2),
      wbounds       = (0.1, 1.0),
      gbounds       = (None, None),
      options       = {'disp': True, 'maxiter': 500, 'gtol': 1e-5, 'iprint': 5},
      specific_bounds = None,
      alpha_PO      = 0.001,
      )

C.diagonalise()
C.get_propagation_quantities()
C.get_dense_matrices_purenp()
f = C.make_f_purenp()

# --------------------------------------------------- single-process reference
t_rk, d_rk = AdaptiveRK4(f, C.sigma, C.Psi_vec, C.omegas, EPS, T0, T1,
                         dH, bias, C.Ixi, 0.1, fixed_mode=False,
                         name='RestartRef')

# -------------------------------------------------------------------- outputs
# Must come before any driver runs: Initial.py reads NAME/Arrays/ at import.
C.tofile(NAME)

np.savez_compressed("restart_results.npz",
                    rk4_t  = t_rk,
                    rk4_jl = d_rk['current_left'],
                    rk4_jr = d_rk['current_right'],
                    tmid   = TMID,
                    )
print("Wrote restart_results.npz and " + NAME + "/")
