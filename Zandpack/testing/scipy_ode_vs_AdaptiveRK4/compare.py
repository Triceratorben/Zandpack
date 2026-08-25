"""Overlay the nozand/zand currents on the three reference integrators.

Run through run.sh, which exports MPLBACKEND=Agg and ZANDPACK_MPL so that this
works on a headless node: the figure is written to disk instead of opened in a
window, which would otherwise block run_zandpack_tests forever.
"""
import numpy as np
from Zandpack.plot import plt, J

REF  = "chain_results.npz"
SAVE = "TDT_Chain_save"

R  = np.load(REF)

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(7, 8))

for ax, driver in zip(axes, ["nozand", "zand"]):
    tz, jz = J([SAVE + "_" + driver])
    ax.plot(R["rk4_t"],  R["rk4_jl"],  label="AdaptiveRK4 left")
    ax.plot(R["opti_t"], R["opti_jl"], linestyle=(0, (3, 1, 1, 1)),
            label="AdaptiveRK4_Opti left")
    ax.plot(R["scipy_t"], np.asarray(R["scipy_jl"])[:, 0], linestyle="dashdot",
            label="scipy left")
    ax.plot(tz, jz[0], linestyle="dashed", label=driver + " left")
    ax.plot(tz, jz[1], linestyle="dotted", label=driver + " right")
    ax.set_title(driver)
    ax.set_ylabel("Current")
    ax.legend()

axes[-1].set_xlabel("Time")
fig.tight_layout()
fig.savefig("Chain_compare.svg")
plt.close(fig)
print("Wrote Chain_compare.svg")
