import numpy as np
from numba import njit
import matplotlib.pyplot as plt
import sisl
from Zandpack.TimedependentTransport import TD_Transport, AdaptiveRK4
from Zandpack.Pulses import box_pulse, zero_dH
from Zandpack.TimedependentTransport import scipy_ode

#from Block_matrices_experimental import Blocksparse2Numpy
#from numba import njit
#from funcs import diff_central, calc_current

tx = 2
t_dev =  1
t_elec = 20

lat_const = 2.5
lineWB = np.linspace(0.0, 0.0, 1) + 1j * 1e-2
lineNL = np.linspace(-15 , 15, 400)  + 1j*1e-2

line = lineWB
line = np.vstack((line,line))

geom_dev   = sisl.geom.sc(lat_const, 'H').tile(tx+2, 0)
geom_ep    = sisl.geom.sc(lat_const, 'H').tile(1, 0).move(np.array([lat_const * (tx+1), 0, 0]))
geom_em    = sisl.geom.sc(lat_const, 'H').tile(1, 0)

geom_dev   = geom_dev.add_vacuum(10,1).add_vacuum(10,2).add_vacuum(10,0)
geom_em    = geom_em. add_vacuum(10,1).add_vacuum(10,2)
geom_ep    = geom_ep. add_vacuum(10,1).add_vacuum(10,2)

Test = TD_Transport([geom_em,geom_ep], geom_dev, kT_i = [0.1, 0.1], mu_i = [0.0, 0.0])
Test.Make_Contour(line, 15 , pole_mode = 'JieHu2011')

Test.Electrodes( semi_infs = ['-a1', '+a1'] )
Test.make_device(
            elec_inds = [[0],[tx+1]],
            Print= False)

elec = sisl.Hamiltonian(sisl.geom.sc(lat_const, sisl.Atom(1, R= 3.0)).add_vacuum(10,1).add_vacuum(10,2))
elec.construct([[0.1, lat_const * 1.1], 
                [0  , t_elec             ]])

Test.run_electrodes(manual_H = [elec, elec])

dev_H = sisl.Hamiltonian(sisl.geom.sc(lat_const, sisl.Atom(1, R= 3.0)).tile(tx+2,0).add_vacuum(10,1).add_vacuum(10,2).add_vacuum(10,0))
dev_H.construct([[0.1, lat_const * 1.1], 
                  [0,   1              ] ])

dev_H[0,1]      =  5**0.5
dev_H[1,0]      =  5**0.5
dev_H[tx+1,tx]  =  5**0.5
dev_H[tx,tx+1]  =  5**0.5
Test.run_device(manual_H = dev_H)
Test.read_data()

# In[read stuff]

#Test.reset_all_fits() # Comment in to reset fits!
NL = 1
min_tol  = -0.0*np.ones(NL)
min_tol1 =  min_tol.copy()
min_tol2 =  min_tol.copy()

def run_mini(its):
    Test.Fit(fact = 1.0, Fallback_W = .5, NumL = NL,
          fit_mode      = 'all',
          force_PSD     = True,
          force_PSD_tol = [min_tol1, min_tol2],
          use_analytical_jac = True,
          min_method = 'SLSQP',
          ebounds = (-5, 5),
          wbounds = (0.01, 0.8),
          gbounds = (None, None),
          tol = -1,
          options = {'disp':True,'maxiter':its, 
                     'gtol':1e-10,
                     'ftol':1e-10,
                     'iprint':1
                     },
          fit_real_part = False,
          specific_bounds = None,#[{(0 ,2) :[(0.1, 0.11), (4,5)]}, {(0 ,5) :[(-0.1, 0.1), (4,5)]}], 
          alpha_PO = 0.01, 
          )

run_mini(0)
Test.diagonalise()
Test.get_propagation_quantities()
Test.get_dense_matrices(1e-8)
Test.Check_input_to_ODE(loose_fermi = True)
f     = Test.make_f()
sig   = Test.sigma
psi   = Test.Psi_vec
omega = Test.omegas
# In[]
Vmax = 1.5
@njit
def dH(t,sigma):
    A = np.zeros(sigma.shape, dtype = np.complex128)
    A[0,0,0] = +Vmax/2 * box_pulse(t, 20, 1, 1)
    A[0,1,1] = -Vmax/2 * box_pulse(t, 20, 1, 1)
    return A
@njit
def delta(t,a):
    if  a == 0:
        return +Vmax * box_pulse(t, 20, 1, 1)
    if  a == 1:
        return -Vmax * box_pulse(t, 20, 1, 1)

t, d = AdaptiveRK4( f, sig, psi, omega, 1e-10,  -10, 40,  dH, delta, Test.Ixi, 0.1, fixed_mode = False, 
                         name = 'DQD')

t1,dm,jl =  scipy_ode(f, sig, psi, omega, -10.0, np.linspace(-10,40,50)+1e-5, dH, delta, Test.Ixi, 
                      dH_given = True, method = 'RK45', dt_guess = None,
                      atol = 1e-8, rtol = 1e-8)

#plt.plot(t, d['current_left'])
#plt.savefig("Croy2009_Jl.svg")
plt.close()
Test.tofile(name = 'TDT_Croy2009')
# np.save('Timearray.npy',t)
# np.save('Jlarray.npy',d['current_left'])
# np.save('SP_t',t)
# np.save('SP_j',jl)
np.savez_compressed("Croy2009_Results.npz",
                    rk4_t   = t,
                    rk4_jl  = d["current_left"],
                    rk4_jr  = d["current_right"],
                    scipy_t = t1,
                    scipy_dm = dm,
                    scipy_jl = jl,
                    )


