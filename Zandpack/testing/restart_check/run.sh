#!/bin/sh
# Zandpack restart scenario -- see ../README.md for the format.
#
# This is the multi-leg variant: the single Initial.py the drivers import
# cannot express a stop and a resume, so the three configurations live in
# Initial_full.py / Initial_leg1.py / Initial_leg2.py and are copied into
# Initial.py in turn. Initial.py is therefore a scratch file here.
set -e

export ZANDPACK_HBAR=1.0
export OMP_NUM_THREADS=1
export NUMBA_NUM_THREADS=1
# Headless-safe plotting: no LaTeX, and no interactive window that would
# block run_zandpack_tests.
export MPLBACKEND=Agg
export ZANDPACK_MPL=NOLATEX

NAME=TDT_Restart
NP=3          # must be >= number of electrodes + 1, and identical for both
              # legs: leg 2 loads per-rank worker state and asserts its shape.

# Builds the device and writes ${NAME}/Arrays/, which Initial.py reads at
# import -- so this has to come before any driver.
python restart.py

# --- control: one uninterrupted run ----------------------------------------
cp Initial_full.py Initial.py
mpirun -np $NP nozand Dir=$PWD
mv ${NAME}_save ${NAME}_save_full

# --- leg 1: run past the checkpoint, dumping a full state at t = 5 ----------
cp Initial_leg1.py Initial.py
mpirun -np $NP nozand Dir=$PWD
# Copy, do not move: leg 2 resumes by reading last_*.npy out of ${NAME}_save.
cp -r ${NAME}_save ${NAME}_save_leg1

# --- leg 2: resume and finish ----------------------------------------------
cp Initial_leg2.py Initial.py
mpirun -np $NP nozand Dir=$PWD
mv ${NAME}_save ${NAME}_save_leg2

python compare.py
