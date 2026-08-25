"""Overlay the nozand/zand currents on the in-package reference results.

Run through run.sh, which exports MPLBACKEND=Agg and ZANDPACK_MPL so that this
works on a headless node: the figure is written to disk instead of opened in a
window, which would otherwise block run_zandpack_tests forever.
"""
import numpy as np
from Zandpack.plot import plt, J

REF  = "honeychurch2018_results.npz"
SAVE = "TDT_hc2018_save"

R  = np.load(REF)
T  = R["rk4_t"]
JL = R["rk4_jl"]
JR = R["rk4_jr"]

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(7, 8))

for ax, driver in zip(axes, ["nozand", "zand"]):
    tz, jz = J([SAVE + "_" + driver])
    ax.plot(T, JL, label="rk4 left")
    ax.plot(T, JR, label="rk4 right")
    ax.plot(tz, jz[0], linestyle="dashed", label=driver + " left")
    ax.plot(tz, jz[1], linestyle="dotted", label=driver + " right")
    ax.set_title(driver)
    ax.set_ylabel("Current")
    ax.legend()

axes[-1].set_xlabel("Time")
fig.tight_layout()
fig.savefig("Honeychurch2018_compare.svg")
plt.close(fig)
print("Wrote Honeychurch2018_compare.svg")
