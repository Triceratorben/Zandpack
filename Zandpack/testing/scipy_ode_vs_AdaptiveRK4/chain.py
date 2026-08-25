"""1D tight-binding chain: AdaptiveRK4 vs AdaptiveRK4_Opti vs scipy solve_ivp.

This scenario is the integrator cross-check: the same device is propagated by
three in-package reference integrators, and run.sh then propagates it again
with the MPI drivers so compare.py can put all of them on one axis.

Merged from the older device.py / adap_RK4.py / adap_RK4_opti.py / scipy_ode.py
split, which passed the device between scripts through a `Test.Timedep` pickle.
That handoff is gone -- the object stays in memory here, as in the other
scenarios.

Two code paths are exercised deliberately and must not be collapsed:

  * `get_dense_matrices_purenp()` + `make_f_purenp()`  -> the RK4 integrators
  * `get_dense_matrices()` + `make_f_experimental()`   -> scipy_ode

They are different implementations of the same right-hand side, and comparing
them is part of what this test is for.

No SIESTA, no pseudopotentials: the Hamiltonians are built with sisl and handed
over via `manual_H`.
"""
import numpy as np
import sisl

from Zandpack.TimedependentTransport import TD_Transport, AdaptiveRK4, scipy_ode
from Zandpack.Optimized_RK45 import AdaptiveRK4_Opti
from Zandpack.td_constants import hbar as print_hbar

# Keep the driving in one place -- the MPI drivers read these same two from
# Bias.py, so the reference and the drivers cannot drift apart.
from Bias import bias, dH

# hbar comes from the ZANDPACK_HBAR environment variable, exported by run.sh.
print('hbar is currently set to ', print_hbar)

NAME   = 'TDT_Chain'
T0, T1 = 0.0, 60.0
EPS    = 1e-10

t_dev     = 1
t_elec    = 1
lat_const = 1.0

line = np.linspace(-2, 2, 151) + 1j * 1e-2
line = np.vstack((line, line))

# ------------------------------------------------------------------ geometry
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

# ----------------------------------------------------------- Lorentzian fit
# Small and cheap (5 Lorentzians, SLSQP) -- it runs in-process rather than
# needing a separate make_fit.py step.
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

# ------------------------------------------- reference solutions, purenp path
C.get_dense_matrices_purenp()
f_np = C.make_f_purenp()

t_rk, d_rk = AdaptiveRK4(f_np, C.sigma, C.Psi_vec, C.omegas, EPS, T0, T1,
                         dH, bias, C.Ixi, 0.1, fixed_mode=False, name='Chain')

t_op, d_op = AdaptiveRK4_Opti(f_np, C.sigma, C.Psi_vec, C.omegas, EPS, T0, T1,
                              dH, bias, C.Ixi, 0.1, fixed_mode=False,
                              name='ChainOpti')

# --------------------------------------------- reference solution, dense path
C.get_dense_matrices()
C.Check_input_to_ODE()
f_dense = C.make_f_experimental()

t_sp, dm_sp, j_sp = scipy_ode(f_dense, C.sigma, C.Psi_vec, C.omegas, T0,
                              np.linspace(T0, T1, 200) + 1e-5, dH, bias, C.Ixi,
                              dH_given=True, method='RK45', dt_guess=None,
                              atol=1e-7, rtol=1e-5)

# -------------------------------------------------------------------- outputs
# Must come before either driver runs: Initial.py reads NAME/Arrays/ at import.
C.tofile(NAME)

np.savez_compressed("chain_results.npz",
                    rk4_t    = t_rk,
                    rk4_jl   = d_rk['current_left'],
                    rk4_jr   = d_rk['current_right'],
                    opti_t   = t_op,
                    opti_jl  = d_op['current_left'],
                    opti_jr  = d_op['current_right'],
                    scipy_t  = t_sp,
                    scipy_dm = dm_sp,
                    scipy_jl = j_sp,
                    )
print("Wrote chain_results.npz and " + NAME + "/")
