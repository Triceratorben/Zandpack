"""Build the device and solve it with the in-package reference integrators.

run.sh executes this first, because it ends with C.tofile(), which writes the
Arrays/ folder that Initial.py loads at import time.

Rename this file to something descriptive (the published result it reproduces,
or the physics it exercises) and update run.sh to match.
"""
import numpy as np
import sisl
from Zandpack.TimedependentTransport import TD_Transport, AdaptiveRK4, scipy_ode
from Zandpack.td_constants import hbar as print_hbar

# Import the driving from Bias.py rather than redefining it, so the reference
# and the drivers cannot drift apart.
from Bias import bias, dH

# hbar comes from the ZANDPACK_HBAR environment variable, exported by run.sh.
print('hbar is currently set to ', print_hbar)

NAME = 'TDT_Template'
T0, T1 = 0.0, 100.0
EPS = 1e-8

# ---------------------------------------------------------------- geometry
# Build electrode and device geometries with sisl, then hand them to
# TD_Transport. See Croy2009/croy2009.py for a worked two-electrode example.
#
# geom_em, geom_ep, geom_dev = ...
# C = TD_Transport([geom_em, geom_ep], geom_dev, kT_i=[0.025, 0.025],
#                  mu_i=[0.0, 0.0])
# C.Make_Contour(line, 15, pole_mode='JieHu2011')
# C.Electrodes(semi_infs=['-a1', '+a1'])
# C.make_device(elec_inds=[[0], [n - 1]], Print=False)
# C.run_electrodes(manual_H=[elec_H, elec_H])
# C.run_device(manual_H=dev_H)
# C.read_data()

# ------------------------------------------------------- reference solution
# C.diagonalise()
# C.get_propagation_quantities()
# C.get_dense_matrices()
# f = C.make_f()
#
# t, d = AdaptiveRK4(f, C.sigma, C.Psi_vec, C.omegas, EPS, T0, T1,
#                    dH, bias, C.Ixi, 0.1, fixed_mode=False, name=NAME)
#
# t_sp, dm_sp, j_sp = scipy_ode(f, C.sigma, C.Psi_vec, C.omegas, T0,
#                               np.linspace(T0, T1, 50) + 1e-5, dH, bias,
#                               C.Ixi, dH_given=True, method='RK45',
#                               dt_guess=None, atol=1e-8, rtol=1e-7)

# ------------------------------------------------------------------ outputs
# This must come before any driver runs -- Initial.py reads NAME/Arrays/.
# C.tofile(NAME)
#
# np.savez_compressed("template_results.npz",
#                     rk4_t    = t,
#                     rk4_jl   = d['current_left'],
#                     rk4_jr   = d['current_right'],
#                     scipy_t  = t_sp,
#                     scipy_dm = dm_sp,
#                     scipy_jl = j_sp,
#                     )

raise SystemExit(
    "_template is a skeleton, not a runnable scenario. Copy the directory, "
    "fill in the geometry and reference sections, then register it in the "
    "Tests list of run_zandpack_tests."
)
