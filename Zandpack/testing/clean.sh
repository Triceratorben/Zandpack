#!/bin/sh
# Remove everything a test run leaves behind, so the directory passed to
# run_zandpack_tests can be reused. run_zandpack_tests deliberately ignores
# this file when it checks that the target directory is empty.
#
# Run from the directory you handed to run_zandpack_tests.
set -e

rm -rf ./*_save ./*_save_* ./*_save_nozand ./*_save_zand
rm -f  ./*.npz ./*.svg ./*.png ./*.npy ./*.xz
rm -rf ./__pycache__ ./*/__pycache__

# The scenario directories themselves are copies made by run_zandpack_tests.
for d in Croy2009 PopescuCroy2016 Honeychurch2018 \
         scipy_ode_vs_AdaptiveRK4 scipy_ode_vs_Adaptive_PBC restart_check; do
    rm -rf "./$d"
done

echo "Cleaned."
