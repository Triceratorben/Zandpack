"""Overlay the stitched leg1+leg2 currents on the uninterrupted run.

If restarting from a checkpoint is lossless the two traces coincide. The legs
overlap slightly (leg 1 runs a little past the checkpoint that leg 2 resumes
from), which shows up as a doubled-back segment around t = tmid -- the plot
sorts by time so it reads as a small kink rather than a jump.

Run through run.sh, which exports MPLBACKEND=Agg and ZANDPACK_MPL so that this
works on a headless node: the figure is written to disk instead of opened in a
window, which would otherwise block run_zandpack_tests forever.
"""
import numpy as np
from Zandpack.plot import plt, J

REF  = "restart_results.npz"
SAVE = "TDT_Restart_save"

R    = np.load(REF)
TMID = float(R["tmid"])

t_full, j_full = J([SAVE + "_full"])
# J() takes a list of save directories and concatenates them in order, which is
# exactly how a restarted run is put back together.
t_join, j_join = J([SAVE + "_leg1", SAVE + "_leg2"])

order  = np.argsort(t_join)
t_join = np.asarray(t_join)[order]
j_join = [np.asarray(j)[order] for j in j_join]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(R["rk4_t"], R["rk4_jl"], label="AdaptiveRK4 left")
ax.plot(t_full, j_full[0], linestyle="dashed", label="nozand full, left")
ax.plot(t_join, j_join[0], linestyle="dotted", label="nozand leg1+leg2, left")
ax.axvline(TMID, color="grey", linewidth=0.8)
ax.annotate("checkpoint", (TMID, ax.get_ylim()[1]), ha="center", va="top")
ax.set_xlabel("Time")
ax.set_ylabel("Current")
ax.legend()

fig.tight_layout()
fig.savefig("Restart_compare.svg")
plt.close(fig)
print("Wrote Restart_compare.svg")
