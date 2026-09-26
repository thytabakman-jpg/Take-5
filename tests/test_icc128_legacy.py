from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from legacy_tool_registry import resolve_legacy_tool
import icc128_legacy

EXPECTED_COMMIT = "e4c76c595b44a35fd9efc02cde8979e656ef54e8"
EXPECTED_BLOBS = {
    "legacy/icc128-legacy/snapshot/runtime/icc128_autonomous_controller.py": "26c1c0cdcf48dbeeaf89b97f8b7556efd084acfa",
    "legacy/icc128-legacy/snapshot/runtime/icc128_semantic_generator_adapter.py": "7902ff2954f39d322a44bec5d8f122c3302e9fc6",
    "legacy/icc128-legacy/snapshot/runtime/rho128_policy.py": "b9688ab3d388ba76e93f0ec4d8713b9ebcea98de",
    "legacy/icc128-legacy/snapshot/contracts/ICC128_AUTONOMOUS_CONTROLLER_CURRENT.yaml": "e0eb421d8b4bf424f0bc1814f152ac98becc7f53",
    "legacy/icc128-legacy/snapshot/contracts/ICC128_RHO_POLICY_CURRENT.yaml": "f916e3f5ccdf9c25bb177cd9dea8da83a5c500ba",
    "legacy/icc128-legacy/snapshot/contracts/ICC128_SEMANTIC_GENERATOR_CURRENT.yaml": "19a6bdc37555dd02bf116bd1308c499c339dc819",
    "legacy/icc128-legacy/snapshot/math/ICC128_FULL_TOOL_MATH_002_2026-09-26.md": "eef6b2df3c7e567e50e5b3402ec9607827f290d5",
    "legacy/icc128-legacy/snapshot/presentation/ICC128_PRESENTATION_CURRENT.yaml": "9b290e5790200e272f021be97d8c2048072d7d7d",
    "legacy/icc128-legacy/snapshot/presentation/ICC_128_CANDIDATE_V12_FRONTIER_CLOSED_2026-09-26.md": "3cbc5345349b539bfad0f3104f803727c1adf8c1",
    "legacy/icc128-legacy/snapshot/validation/ICC128_RUNTIME_AND_HOST_BOUNDARY_CLOSURE_001_2026-09-26.md": "78ae5739092f1d147c2155c890e0e6dcc51e20ad",
}

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def test_activation_phrase_resolves_frozen_tool():
    spec = resolve_legacy_tool("activate ICC128 Legacy")
    assert spec is not None
    assert spec.canonical_name == "ICC128 Legacy"
    assert spec.source_commit == EXPECTED_COMMIT
    assert spec.immutable is True

def test_frozen_snapshot_matches_source_blob_ids():
    for rel, expected in EXPECTED_BLOBS.items():
        assert git_blob_sha((ROOT / rel).read_bytes()) == expected

def test_loader_exposes_historical_runtime():
    active = icc128_legacy.activate()
    assert active["identity"].source_commit == EXPECTED_COMMIT
    assert active["identity"].immutable is True
    assert active["identity"].current_system_authority is False
    assert hasattr(active["controller"], "ICC128Controller")
    assert hasattr(active["semantic_generator"], "generate")
    assert hasattr(active["rho_policy"], "choose")
