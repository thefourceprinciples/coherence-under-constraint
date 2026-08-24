import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "experiments" / "fr_fource_formal_013a.py"
spec = importlib.util.spec_from_file_location("atlas013a", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def cfg():
    return mod.load_config(ROOT / "experiments" / "configs" / "fr_fource_formal_013a.json")


def test_seed_firewall_accepts_design_only():
    mod.enforce_firewall([2000, 2009], cfg())


def test_seed_firewall_rejects_calibration():
    try:
        mod.enforce_firewall([3000], cfg())
    except RuntimeError:
        return
    raise AssertionError("calibration seed escaped 013A firewall")


def test_seed_firewall_rejects_heldout():
    try:
        mod.enforce_firewall([4000], cfg())
    except RuntimeError:
        return
    raise AssertionError("held-out seed escaped 013A firewall")


def test_all_generator_families_are_deterministic_and_declared():
    for gid in cfg()["generators"]:
        a = mod.build_generator(gid, 2000)
        b = mod.build_generator(gid, 2000)
        assert a["W"].shape == b["W"].shape
        assert (a["W"] == b["W"]).all()
        assert gid in mod.GENERATOR_SPECS


def test_g6_has_no_declared_positive_truth():
    assert mod.build_generator("G6", 2000)["truth"] == {}
