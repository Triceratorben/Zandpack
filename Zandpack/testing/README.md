# Zandpack test scenarios

Each subdirectory here is one **scenario**: a small transport problem that is
solved twice — once by an in-package reference integrator, once by the MPI
drivers `nozand` and `zand` — so the two can be compared.

Run them all with:

```console
run_zandpack_tests Dir=/path/to/empty/dir /path/to/pseudopotentials
```

The runner copies each registered scenario into the target directory and
executes its `run.sh`. It reports PASS/FAIL per scenario and exits non-zero if
any of them fail.

## Prerequisites

- **An MPI runtime.** Every `run.sh` calls `mpirun -np N`, where `N` must be at
  least *number of electrodes + 1* — one rank drives the density matrix, the
  rest are electrode workers. The two-electrode scenarios use `-np 3`.
- **TBtrans, and pseudopotentials.** Every registered scenario builds its
  Hamiltonians with `manual_H`, which skips SIESTA itself — but
  `TD_Transport.run_device` calls `Dev.fdf()` and then
  `Dev.run_tbtrans_in_dir(DOS_GF=True)` *unconditionally*, so `tbtrans` must be
  on `PATH` and the pseudopotentials passed as the second argument to
  `run_zandpack_tests` must be present. Only the unregistered scenarios need
  a full SIESTA run on top of that.
- **An empty target directory.** The runner refuses to start otherwise, so that
  results from a previous run cannot be mistaken for a new one. `clean.sh` is
  the one file it ignores; run it to make a used directory reusable.

## Layout of a scenario

| File | Purpose |
|---|---|
| `Initial.py` | Run configuration read by the MPI drivers |
| `Bias.py` | Time-dependent driving: `bias`, `dH`, `dissipator` |
| `<Reference>.py` | Builds the device, runs the reference integrators, writes the results archive |
| `compare.py` | Overlays driver output on the reference results |
| `run.sh` | Ties it together |

`_template/` holds a commented skeleton of all five. It is not a runnable
scenario and is not registered with the runner — copy it and fill it in.

### The driver import contract

This is not a style convention; it is enforced. `mpi/zand` and `mpi/nozand` do:

```python
from Initial import Arrs, t0, t1, stepsize, print_timings, usesave, saveevery, \
                     name, eps, hbar, n_dm_compress, save_PI, checkpoints, \
                     save_checkpoints, LoadFromFull
from Bias    import dH, bias, dissipator
```

A missing name is an immediate `ImportError` before any physics runs. In
particular `dissipator` is required even when it returns `0.0`, and `hbar` must
be imported into `Initial.py` from `Zandpack.td_constants` rather than
hardcoded — see the environment section below.

### Ordering

`Initial.py` calls `load_dictionary(name + '/Arrays/')` **at import time**, so
the device must already be on disk when a driver starts. That is why `run.sh`
always runs the reference script first: it ends with
`C.tofile('TDT_<Name>')`, which writes the `Arrays/` folder that `Initial.py`
then reads. The `name` in `Initial.py` must match the `tofile` argument.

### Naming

A driver writes its output to `<name>_save/`. Since both drivers run in the same
directory, `run.sh` renames after each one:

```sh
mpirun -np 3 nozand Dir=$PWD
mv ${NAME}_save ${NAME}_save_nozand
mpirun -np 3 zand Dir=$PWD
mv ${NAME}_save ${NAME}_save_zand
```

`compare.py` then reads both with
`Zandpack.mpi_tools.combine_currents` (exported as `J` from `Zandpack.plot`),
which takes a *list* of save directories and stitches them in time order — that
is how the restart scenario joins its two legs.

### The results archive

The reference script writes `<name>_results.npz` with these keys, so that every
`compare.py` looks the same:

| Key | Contents |
|---|---|
| `rk4_t`, `rk4_jl`, `rk4_jr` | time and left/right currents from `AdaptiveRK4` |
| `scipy_t`, `scipy_jl`, `scipy_dm` | the same from `scipy_ode` (`solve_ivp`), where the scenario runs it |

`scipy_jl` is shaped `(nt, n_elec)`, unlike `rk4_jl` which is a single lead.

## Environment

`run.sh` exports five variables, and all five matter:

| Variable | Why |
|---|---|
| `ZANDPACK_HBAR=1.0` | Natural units. `Zandpack/td_constants.py` reads this; do **not** hand-edit that file, and do not hardcode `hbar` in `Initial.py`. |
| `OMP_NUM_THREADS=1`, `NUMBA_NUM_THREADS=1` | One thread per MPI rank; otherwise ranks oversubscribe the node. |
| `MPLBACKEND=Agg` | `compare.py` must never open a window — an interactive backend blocks the runner indefinitely. |
| `ZANDPACK_MPL=NOLATEX` | `Zandpack/plot.py` turns on `text.usetex` unless this is set to something other than `LATEX`; without it plotting needs a LaTeX install. |

`compare.py` writes an `.svg` rather than calling `plt.show()`, for the same
reason.

## Registering a scenario

Add the directory name to the `Tests` list in `run_zandpack_tests`.

## Scenarios

| Directory | What it checks | Registered |
|---|---|---|
| `Croy2009` | Two-level dot under a bias pulse, against Croy & Saalmann (2009) | yes |
| `PopescuCroy2016` | Tight-binding chain under a bias staircase, against Popescu & Croy (2016) | yes |
| `Honeychurch2018` | Driven chain, against Honeychurch & Kosov (2018) | yes |
| `scipy_ode_vs_AdaptiveRK4` | `AdaptiveRK4` vs `AdaptiveRK4_Opti` vs `scipy.integrate.solve_ivp` on a 1D chain | yes |
| `restart_check` | A run stopped at a checkpoint and resumed reproduces the uninterrupted run | yes |
| `scipy_ode_vs_Adaptive_PBC` | The integrator cross-check on k-sampled graphene | no — calls `run_electrodes()`/`run_device()` without `manual_H`, i.e. a full SIESTA run |
| `Rib` | Graphene nanoribbon with antidots | no — needs SIESTA, a 61-Lorentzian fit, and pickles that are not in the repo |
| `SR` | STM tip on graphene | no — same |
| `scipy_vs_ARK4_Zand` | Three-terminal graphene | no — same |

The four unregistered ones are kept as-is for reference. Converting them means
either committing the fitted-device pickles as fixtures or running the full
SIESTA pipeline inside `run.sh`, which is a separate decision — their value is
precisely the SIESTA path, so rewriting them with `manual_H` would remove what
they test.
