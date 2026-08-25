#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 08:33:27 2022

@author: aleksander
"""

import numpy as np
import sisl
from numba import njit
from Zandpack.plot import plt
from Zandpack.TimedependentTransport import TD_Transport as TDT
from Zandpack.TimedependentTransport import AdaptiveRK4  as RK4
from Zandpack.Pulses import zero_dH, zero_bias, stairs
from Zandpack.TimedependentTransport import scipy_ode
print('\n set hbar  = 1 in the constants module\n')

tx = 6
t_dev =  1
t_elec = 1

lat_const = 1.0
line = np.linspace(-2 , 2, 101)  + 1j*1e-2
line = np.vstack((line,line))

### Geometries ###
geom_dev   = sisl.geom.sc(lat_const, 'H').tile(tx+2, 0)
geom_ep    = sisl.geom.sc(lat_const, 'H').tile(1, 0).move(np.array([lat_const * (tx+1), 0, 0]))
geom_em    = sisl.geom.sc(lat_const, 'H').tile(1, 0)
geom_dev   = geom_dev.add_vacuum(5,1).add_vacuum(5,2).add_vacuum(5,0)
geom_em    = geom_em. add_vacuum(5,1).add_vacuum(5,2)
geom_ep    = geom_ep. add_vacuum(5,1).add_vacuum(5,2)

### Our Main calculator object ###
C = TDT([geom_em,geom_ep], geom_dev, kT_i = [0.025, 0.025])
C.Make_Contour(line, 20 ,pole_mode = 'JieHu2011')
C.Electrodes( semi_infs = ['-a1', '+a1'] )
C.make_device(elec_inds = [[0],  [tx+1]] )

# plt.show() would block under an interactive backend; run.sh sets
# MPLBACKEND=Agg, but do not rely on that here.
plt.close()
C.Device.Visualise()
plt.close()
# Create the electronic structures. These are sisl shorthands for creating the Hamiltonians of the leads and device
elec = sisl.Hamiltonian(sisl.geom.sc(lat_const, sisl.Atom(1, R= 3.0)).add_vacuum(10,1).add_vacuum(10,2))
elec.set_nsc((3,1,1))
elec.construct([[0.1, lat_const * 1.1], 
                [0  , t_elec             ]])
dev_H = sisl.Hamiltonian(sisl.geom.sc(lat_const, sisl.Atom(1, R= 3.0)).tile(tx+2,0).add_vacuum(10,1).add_vacuum(10,2).add_vacuum(10,0))
dev_H.construct([[0.1, lat_const * 1.1], 
                [0,    t_dev             ]])

C.run_electrodes(manual_H = [elec, elec])
C.run_device(manual_H = dev_H)
C.read_data()
# In[]
#C.reset_all_fits()
min_tol1, min_tol2 = -0.0, -0.0

def run_fit(its):
    C.Fit(fact = 2.0,             # a number controlling the broadening on the initial guess
          NumL = 16,               # number of Lorentzians used for the fitting
          fit_mode      = 'all',        # We fit the self-energies with lorentzians
          force_PSD     = False,                # the self-energies are not positive semidefinite
          force_PSD_tol = [min_tol1, min_tol2], # 
          min_method    = 'SLSQP',# minimization method used by SciPy
          ebounds = (-2,2),       # bounds on where the Lorentzian centers can be located
          wbounds = (0.1, 1.0), # bounds on the linewidths of the Lorentzians
          gbounds = (None, None), # bounds on the fitting coefficients
          options = {'disp':True, # options keywords passed to the SciPy minimizer. The the docs for more info
                     'maxiter':its,   
                     'gtol':1e-5, 
                     'iprint':5},
          specific_bounds = None,#[{(0 ,5) :[(-0.1, 0.1), (4,5)]}, {(0 ,5) :[(-0.1, 0.1), (4,5)]}], 
          alpha_PO = 0.001,
         )

run_fit(500)

# In this test we dont do any iteration to make the
# fit positive semidefinite. In the paper this is not
# done either


# In[]

C.diagonalise()
C.get_propagation_quantities()
C.get_dense_matrices()
C.Check_input_to_ODE()
f     = C.make_f()
sig   = C.sigma
psi   = C.Psi_vec
omega = C.omegas

teq, deq = RK4( f, sig, psi, omega, 1e-10,  -0, 30,  zero_dH, zero_bias, C.Ixi, 
               0.1, fixed_mode = False, name = 'Chain')

# In[]
@njit
def Staired_delta(t,a):
    if a == 0:
        return  stairs(t, 0.2, 20, 20)
    if a == 1:
        return -stairs(t, 0.2, 20, 20)
ts, ds   = RK4(f, sig,psi, omega, 1e-8, 0, 200, zero_dH, Staired_delta, C.Ixi, name='PChain')
t1,dm,jl =  scipy_ode(f, sig, psi, omega, -10.0, np.linspace(0,200,50)+1e-5, zero_dH, Staired_delta, C.Ixi, 
                      dH_given = True, method = 'RK45', dt_guess = None, 
                      atol = 1e-8, rtol = 1e-7)
print( 'Plot the current times 2 pi to get the Fig.1 in Croy 2016.\n')
print( 'See the units of the second axis for the reason (there is a h, not hbar)')
plt.plot(ts, ds['current_left'])
plt.savefig("Croy2016_Jl.svg")
plt.xlabel("Time")
plt.xlabel("Current")

plt.close()
#C.write_to_file(name = 'TDT_Croy2016')
C.tofile('TDT_Croy2016')
#np.save('Timearray.npy',ts)
#np.save('Jlarray.npy',ds['current_left'])

np.savez_compressed("croy2016_results.npz",
                    scipy_t  = t1,
                    scipy_dm = dm,
                    scipy_jl = jl,
                    rk4_jl   = ds['current_left'],
                    rk4_jr   = ds['current_right'],
                    rk4_t    = ts
                    )
