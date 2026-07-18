"""Run the historical CUC prototype scripts in their required order.

This runner generates toy-model figures for provenance and baseline repair. It
does not run the future v0.2 reference benchmark and does not produce empirical
validation.
"""

from __future__ import annotations

import os
import runpy
import tempfile
from pathlib import Path

SIMULATION_DIR = Path(__file__).resolve().parent
os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "cuc-matplotlib"),
)

import matplotlib  # noqa: E402


matplotlib.use("Agg")

SCRIPTS = [
    "cuc_simulation_v1_coherence_emergence.py",
    "cuc_simulation_v2_phase_diagram.py",
    "cuc_simulation_v3_throughput_survival.py",
    "cuc_simulation_v4_unified_plate.py",
]


def main() -> None:
    original_directory = Path.cwd()
    os.chdir(SIMULATION_DIR)
    try:
        for script_name in SCRIPTS:
            print(f"Running {script_name}...")
            runpy.run_path(str(SIMULATION_DIR / script_name), run_name="__main__")
    finally:
        os.chdir(original_directory)
    print("Historical CUC prototype figures generated successfully.")


if __name__ == "__main__":
    main()
