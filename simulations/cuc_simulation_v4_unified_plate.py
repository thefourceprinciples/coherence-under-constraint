"""Combine the four historical CUC prototype figures into one plate."""

from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


OUTPUT_DIR = Path(__file__).resolve().parent
INPUTS = [
    OUTPUT_DIR / "figure_1A_coherence_emergence.png",
    OUTPUT_DIR / "figure_1B_phase_diagram.png",
    OUTPUT_DIR / "figure_1C_throughput_map.png",
    OUTPUT_DIR / "figure_1D_survival_boundary.png",
]
PLATE_PATH = OUTPUT_DIR / "cuc_simulation_v4_unified_figure.png"

missing = [path.name for path in INPUTS if not path.is_file()]
if missing:
    raise FileNotFoundError(
        "Generate the prerequisite figures before building the unified plate: "
        + ", ".join(missing)
    )

images = [mpimg.imread(path) for path in INPUTS]

figure, axes = plt.subplots(2, 2, figsize=(14, 12))
titles = [
    "Figure 1A. Coherence Emergence Under Constraint",
    "Figure 1B. Coupling–Constraint Phase Diagram",
    "Figure 1C. Throughput–Dissipation Coherence Map",
    "Figure 1D. Coherence Threshold Boundary",
]

for axis, image, title in zip(axes.flat, images, titles):
    axis.imshow(image)
    axis.set_title(title)
    axis.axis("off")

figure.suptitle(
    "CUC Historical Prototypes: Unified Computational Figure Set",
    fontsize=18,
    y=0.98,
)

caption = (
    "Historical toy-model outputs. Figure 1A shows time-domain phase coherence; "
    "1B sweeps coupling and an alignment-style constraint; 1C sweeps a throughput "
    "multiplier and noise proxy; 1D extracts an illustrative coherence threshold. "
    "These figures do not constitute empirical validation of CUC."
)
figure.text(0.5, 0.02, caption, ha="center", va="bottom", wrap=True, fontsize=10)
figure.subplots_adjust(
    left=0.03,
    right=0.97,
    top=0.88,
    bottom=0.10,
    hspace=0.28,
    wspace=0.08,
)
figure.savefig(PLATE_PATH, dpi=240)
print("Saved image to:", PLATE_PATH)
plt.show()
