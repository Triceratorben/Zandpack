import numpy as np
import matplotlib.pyplot as plt
import sisl
from numba import njit
from Zandpack.TimedependentTransport import TD_Transport
from Zandpack.TimedependentTransport import AdaptiveRK4  as RK4
from Zandpack.Pulses import box_pulse, zero_dH
from Zandpack.TimedependentTransport import hbar as print_hbar
from Zandpack.Pulses import air_photonics_pulse as P

# hbar comes from the ZANDPACK_HBAR environment variable, exported by run.sh.
print('hbar is currently set to ', print_hbar)

tx     = 2
t_dev  = 2
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

#tbtrans cant do 1 orbital, so a (almost) noninteracting one is put in.
dev_H[0,1     ]    =  5**0.5
dev_H[1,0     ]    =  5**0.5
dev_H[0,0] = 1e-10
dev_H[1,1] = 2e-10
dev_H[2,2] = 3e-10
dev_H[3,3] = 4e-10

dev_H[1,2] = 1e-8#0.0
dev_H[2,1] = 1e-8#0.0
dev_H[2,3] = 1e-8#0.0
dev_H[3,2] = 1e-8#0.0
dev_H[tx+1, tx-1]  =  5**0.5
dev_H[tx-1, tx+1]  =  5**0.5
#dev_H[tx+1, tx]  =  5**0.5
#dev_H[tx, tx+1]  =  5**0.5


Test.run_device(manual_H = dev_H, )
Test.read_data()

# In[read stuff]

NL = 1
min_tol  = -0.0*np.ones(NL)
min_tol1 =  min_tol.copy()
min_tol2 =  min_tol.copy()

def run_mini(its):
    Test.Fit(fact = 1.0, Fallback_W = 10.0, NumL = NL,
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

run_mini(1)

Test.diagonalise()
Test.get_propagation_quantities()
Test.get_dense_matrices(1e-8)
Test.Check_input_to_ODE(loose_fermi = True)
f     = Test.make_f()
sig   = Test.sigma
psi   = Test.Psi_vec
omega = Test.omegas

# In[]

Vmax = 1.0
T = 0.1
W = 0.1
Tmax=10*np.pi
zeta = Tmax
@njit
def pulse(t):
    return np.cos(W*t)#*np.exp(-1/2*(t/zeta)**2)
@njit
def dH(t,sigma):
    A = np.zeros(sigma.shape, dtype = np.complex128)
    A[0,1,1] = 1 * pulse(t)
    return A
@njit
def delta(t,a):
    if  a == 0:
        return 0.0 * pulse(t) 
    if  a == 1:
        return 0.125 * pulse(t)

t, d = RK4( f, sig, psi, omega, 1e-12,  -3*np.pi/(2*W)-100, 150,  dH, delta, Test.Ixi, 0.1, fixed_mode = False, 
                    name = 'QD')

# In[]
# plt.show() would block under an interactive backend; run.sh sets
# MPLBACKEND=Agg, but do not rely on that here.
plt.close()
Tp = np.pi*2/W
plt.plot(t,np.array(d['current_left']), label = r'$J_l$')
plt.ylabel('Current left')
plt.xlabel('time')
plt.legend()
#plt.plot(t,[pulse(ti)/10 for ti in t])

plt.xlim([0.0, 1*Tp])
#plt.show()

plt.plot(t, d['current_left'])
plt.savefig("HoneyChurch2018_Jl.svg")
plt.close()
np.save('Timearray.npy',t)
np.save('Jlarray.npy',d['current_left'])
Test.tofile(name = 'TDT')


np.savez_compressed("honeychurch2018_results.npz",
                    #scipy_t  = t1,
                    #scipy_dm = dm,
                    #scipy_jl = jl,
                    rk4_jl   = d['current_left'],
                    rk4_jr   = d['current_right'],
                    rk4_t    = t
                    )

