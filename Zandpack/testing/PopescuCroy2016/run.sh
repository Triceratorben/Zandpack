#!/bin/sh
# Canonical Zandpack scenario runner -- see ../README.md for the format.
set -e

export ZANDPACK_HBAR=1.0
export OMP_NUM_THREADS=1
export NUMBA_NUM_THREADS=1
# Headless-safe plotting: no LaTeX, and no interactive window that would
# block run_zandpack_tests.
export MPLBACKEND=Agg
export ZANDPACK_MPL=NOLATEX

NAME=TDT_Croy2016
NP=3          # must be >= number of electrodes + 1

python Croy2016.py
# No steady-state initialisation needed for this scenario.
mpirun -np $NP nozand Dir=$PWD
mv ${NAME}_save ${NAME}_save_nozand
mpirun -np $NP zand Dir=$PWD
mv ${NAME}_save ${NAME}_save_zand

python compare.py
