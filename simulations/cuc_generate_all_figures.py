# =========================================================
# CUC MASTER FIGURE GENERATOR
# Generates Figures 1A–1D for Coherence Under Constraint
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import os

print("Starting CUC figure generation...\n")

# Ensure output directory exists
output_dir = os.getcwd()

# =========================================================
# FIGURE 1A — Coherence Emergence
# =========================================================

t = np.linspace(0, 10, 500)

def coherence_curve(k):
    return 1 / (1 + np.exp(-k * (t - 5)))

plt.figure()
plt.plot(t, coherence_curve(1), label="Low coupling")
plt.plot(t, coherence_curve(3), label="Balanced regime")
plt.plot(t, coherence_curve(6), label="High coupling")

plt.title("Figure 1A — Coherence Emergence Under Constraint")
plt.xlabel("Time")
plt.ylabel("Coherence R(t)")
plt.legend()

file_1A = os.path.join(output_dir, "figure_1A_coherence_emergence.png")
plt.savefig(file_1A, dpi=300)
plt.close()

print("Saved:", file_1A)

# =========================================================
# FIGURE 1B — Phase Diagram
# =========================================================

coupling = np.linspace(0, 5, 100)
constraint = np.linspace(0, 5, 100)
C, K = np.meshgrid(coupling, constraint)

R = np.tanh(C) * np.exp(-K / 3)

plt.figure()
plt.contourf(C, K, R, levels=20)
plt.colorbar(label="Coherence R")

plt.title("Figure 1B — Phase Diagram")
plt.xlabel("Coupling Strength")
plt.ylabel("Constraint Strength")

file_1B = os.path.join(output_dir, "figure_1B_phase_diagram.png")
plt.savefig(file_1B, dpi=300)
plt.close()

print("Saved:", file_1B)

# =========================================================
# FIGURE 1C — Throughput Map
# =========================================================

E = np.linspace(0, 10, 100)
D = np.linspace(0, 10, 100)
E_grid, D_grid = np.meshgrid(E, D)

coherence = np.tanh(E_grid / (D_grid + 1))

plt.figure()
plt.imshow(coherence, origin='lower', extent=[0,10,0,10], aspect='auto')
plt.colorbar(label="Coherence")

plt.title("Figure 1C — Throughput–Dissipation Map")
plt.xlabel("Energy Input (E)")
plt.ylabel("Dissipation (D)")

file_1C = os.path.join(output_dir, "figure_1C_throughput_map.png")
plt.savefig(file_1C, dpi=300)
plt.close()

print("Saved:", file_1C)

# =========================================================
# FIGURE 1D — Survival Boundary
# =========================================================

boundary = E_grid > D_grid

plt.figure()
plt.imshow(boundary, origin='lower', extent=[0,10,0,10], aspect='auto')
plt.colorbar(label="Viable Region")

plt.title("Figure 1D — Survival Boundary")
plt.xlabel("Energy Input (E)")
plt.ylabel("Dissipation (D)")

file_1D = os.path.join(output_dir, "figure_1D_survival_boundary.png")
plt.savefig(file_1D, dpi=300)
plt.close()

print("Saved:", file_1D)

# =========================================================

print("\n✅ All figures generated successfully!")
