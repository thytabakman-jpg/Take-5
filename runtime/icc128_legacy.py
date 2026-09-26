"""Loader for the immutable ICC128 Legacy snapshot."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import importlib.util
import sys
try:
    from . import icc128_legacy_reporting as legacy_reporting
except ImportError:
    import icc128_legacy_reporting as legacy_reporting

DISPLAY_NAME = "ICC128 Legacy"
SOURCE_COMMIT = "e4c76c595b44a35fd9efc02cde8979e656ef54e8"
LEGACY_ROOT = Path(__file__).resolve().parents[1] / "legacy" / "icc128-legacy"
MANIFEST = LEGACY_ROOT / "MANIFEST.yaml"
SNAPSHOT_ROOT = LEGACY_ROOT / "snapshot"

def _manifest_source_value(key: str) -> str:
    in_source = False
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if raw and not raw.startswith(" "):
            in_source = raw.strip() == "source:"
            continue
        if in_source:
            stripped = raw.strip()
            if stripped.startswith(f"{key}:"):
                return stripped.split(":", 1)[1].strip().strip('"')
    raise RuntimeError(f"ICC128_LEGACY_MANIFEST_SOURCE_MISSING:{key}")

SOURCE_REPOSITORY = _manifest_source_value("repository")
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
        "reporting": legacy_reporting,
        "reporting_required": True,
        "learning_persistence": "REPORT_ONLY_EPHEMERAL_CONTROLLER_MEMORY",
    }
