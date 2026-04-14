import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

outdir = Path("/mnt/data")
sim1 = outdir / "cuc_simulation_v1_plot.png"
sim2 = outdir / "cuc_simulation_v2_phase_diagram.png"
sim3a = outdir / "cuc_simulation_v3_throughput_dissipation.png"
sim3b = outdir / "cuc_simulation_v3_survival_boundary.png"

plate_path = outdir / "cuc_simulation_v4_unified_figure.png"

imgs = [mpimg.imread(str(p)) for p in [sim1, sim2, sim3a, sim3b]]

fig = plt.figure(figsize=(14, 12))

axes = [
    plt.subplot(2, 2, 1),
    plt.subplot(2, 2, 2),
    plt.subplot(2, 2, 3),
    plt.subplot(2, 2, 4),
]

titles = [
    "Figure 1A. Coherence Emergence Under Constraint",
    "Figure 1B. Coupling–Constraint Phase Diagram",
    "Figure 1C. Throughput–Dissipation Survival Map",
    "Figure 1D. Survival Boundary",
]

for ax, img, title in zip(axes, imgs, titles):
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")

fig.suptitle(
    "CUC Simulation 4: Unified Computational Figure Set",
    fontsize=18,
    y=0.98
)

caption = (
    "Unified result plate for the Coherence Under Constraint framework. "
    "1A shows time-domain coherence emergence in three regimes. "
    "1B maps sustained coherence across coupling strength K and constraint strength B. "
    "1C maps sustained coherence across throughput E and dissipation D. "
    "1D estimates the minimum throughput required to maintain coherence above threshold as dissipation rises."
)
fig.text(0.5, 0.02, caption, ha="center", va="bottom", wrap=True, fontsize=10)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig(plate_path, dpi=240, bbox_inches="tight")
