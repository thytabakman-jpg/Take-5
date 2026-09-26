"""Loader for the immutable ICC128 Legacy snapshot."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import importlib.util
import sys

DISPLAY_NAME = "ICC128 Legacy"
SOURCE_REPOSITORY = "thytabakman-jpg/Reaserch"
SOURCE_COMMIT = "e4c76c595b44a35fd9efc02cde8979e656ef54e8"
SNAPSHOT_ROOT = Path(__file__).resolve().parents[1] / "legacy" / "icc128-legacy" / "snapshot"
RUNTIME_ROOT = SNAPSHOT_ROOT / "runtime"

@dataclass(frozen=True)
class ICC128LegacyIdentity:
    display_name: str = DISPLAY_NAME
    source_repository: str = SOURCE_REPOSITORY
    source_commit: str = SOURCE_COMMIT
    immutable: bool = True
    current_system_authority: bool = False

def identity() -> ICC128LegacyIdentity:
    return ICC128LegacyIdentity()

def _load(module_name: str, filename: str):
    path = RUNTIME_ROOT / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"ICC128_LEGACY_LOAD_FAILED:{filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def load_controller_module():
    return _load("icc128_legacy_controller", "icc128_autonomous_controller.py")

def load_semantic_generator_module():
    return _load("icc128_legacy_semantic_generator", "icc128_semantic_generator_adapter.py")

def load_rho_policy_module():
    return _load("icc128_legacy_rho_policy", "rho128_policy.py")

def activate() -> dict[str, object]:
    return {
        "identity": identity(),
        "controller": load_controller_module(),
        "semantic_generator": load_semantic_generator_module(),
        "rho_policy": load_rho_policy_module(),
    }
