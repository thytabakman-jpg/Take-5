"""Canonical tool identity and reconstruction manifests.

A configured tool is complete only when its canonical manifest reconstructs
every protected behavior required by that tool's current identity.

The manifest references implementation/witness surfaces. It does not duplicate
their semantics.
"""
from dataclasses import dataclass

PHASES={"PRE","INTRA","POST","CROSS"}

@dataclass(frozen=True)
class ProtectedBinding:
    behavior_id:str
    phase:str
    implementation:str
    witness:str

    def complete(self)->bool:
        return (
            bool(self.behavior_id)
            and self.phase in PHASES
            and bool(self.implementation)
            and bool(self.witness)
        )

@dataclass(frozen=True)
class ToolManifest:
    tool_id:str
    native_semantics:str
    geometry_policy:str
    closure_contract:str
    reentry_contract:str
    bindings:tuple[ProtectedBinding,...]=()
    lineage_contract:str="research/TOOL_LINEAGE_RECOVERY_CONTRACT_001_2026-09-25.md"

    def behavior_ids(self)->frozenset[str]:
        return frozenset(b.behavior_id for b in self.bindings)

    def complete(self)->bool:
        ids=[b.behavior_id for b in self.bindings]
        return (
            bool(self.tool_id)
            and bool(self.native_semantics)
            and bool(self.geometry_policy)
            and bool(self.closure_contract)
            and bool(self.reentry_contract)
            and len(ids)==len(set(ids))
            and all(b.complete() for b in self.bindings)
        )

GENERIC_BINDINGS=(
    ProtectedBinding(
        "CONFIGURED_RUN_WRAPPER",
        "CROSS",
        "architecture/FULL_RUN_DEFAULT_DISPATCH_CONTRACT_066.md",
        "tests/test_configured_run_spec.py",
    ),
    ProtectedBinding(
        "TOOL_RUN_CLOSURE",
        "POST",
        "runtime/tool_run_closure.py",
        "tests/test_tool_run_closure.py",
    ),
    ProtectedBinding(
        "REENTRY_REQUIRED",
        "POST",
        "runtime/configured_run.py",
        "tests/test_configured_run_spec.py",
    ),
    ProtectedBinding(
        "OPEN_PRESERVATION",
        "CROSS",
        "runtime/configured_run.py",
        "tests/test_configured_run_spec.py",
    ),
)

MT_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "MT_BLACK_BOX_SEMANTIC_RETURN_GATE",
        "INTRA",
        "runtime/mt_semantic_return_gate.py",
        "tests/test_mt_semantic_return_gate.py",
    ),
)

ASSERT_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "ASSERT_COMPOUND_STAGE_ORDER",
        "INTRA",
        "runtime/assert_compound.py",
        "tests/test_assert_compound.py",
    ),
    ProtectedBinding(
        "ASSERT_SECOND_COMPARE_REQUIRED",
        "INTRA",
        "runtime/assert_compound.py",
        "tests/test_assert_compound.py",
    ),
    ProtectedBinding(
        "ASSERT_DISCOVERY_WORLD_FIXED_POINT_REENTRY",
        "INTRA",
        "runtime/assert_compound.py",
        "tests/test_assert_compound.py",
    ),
    ProtectedBinding(
        "ASSERT_FULL36_THREE_SURFACE_COVERAGE",
        "INTRA",
        "runtime/assert_full36.py",
        "tests/test_assert_full36.py",
    ),
)

IMPROVEMENT_CORE_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "IC_INQUIRY_BEFORE_PACKAGE_SELECTION",
        "INTRA",
        "runtime/improvement_core.py",
        "tests/test_improvement_core.py",
    ),
    ProtectedBinding(
        "IC_UNMAPPED_QUESTION_FAILS_OPEN",
        "INTRA",
        "runtime/improvement_core.py",
        "tests/test_improvement_core.py",
    ),
    ProtectedBinding(
        "IC_GOVERNED_DELEGATED_EXECUTION",
        "INTRA",
        "runtime/controller_episode.py",
        "tests/test_controller_episode.py",
    ),
    ProtectedBinding(
        "IC_MATERIAL_DELTA_REENTRY_ROUTING",
        "POST",
        "runtime/improvement_core.py",
        "tests/test_improvement_core.py",
    ),
)

HF001_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "HF001_OBLIGATION_TO_PACKAGE_ROUTING",
        "INTRA",
        "runtime/hf_controller.py",
        "tests/test_hf_current_controller.py",
    ),
    ProtectedBinding(
        "HF001_BLOCKED_OPEN_WITHOUT_REACHABLE_PACKAGE",
        "INTRA",
        "runtime/hf_controller.py",
        "tests/test_hf_current_controller.py",
    ),
    ProtectedBinding(
        "HF001_MATERIAL_DELTA_REENTER_OR_REVERIFY",
        "POST",
        "runtime/hf_controller.py",
        "tests/test_hf_current_controller.py",
    ),
    ProtectedBinding(
        "HF001_WORLD_OR_DISCOVERY_DELTA_REENTERS_OBSERVE",
        "POST",
        "runtime/hf_controller.py",
        "tests/test_hf_current_controller.py",
    ),
    ProtectedBinding(
        "HF001_RESULT_SENSITIVE_DELTA_REVERIFIES",
        "POST",
        "runtime/hf_controller.py",
        "tests/test_hf_current_controller.py",
    ),
)

OVERRIDES={
    "MT":ToolManifest(
        tool_id="MT",
        native_semantics="MT",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=MT_BINDINGS,
    ),
    "ASSERT":ToolManifest(
        tool_id="ASSERT",
        native_semantics="ASSERT",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=ASSERT_BINDINGS,
    ),
    "ImprovementCore":ToolManifest(
        tool_id="ImprovementCore",
        native_semantics="ImprovementCore",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=IMPROVEMENT_CORE_BINDINGS,
    ),
    "HF001":ToolManifest(
        tool_id="HF001",
        native_semantics="HF001",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=HF001_BINDINGS,
    ),
}

def has_specific_manifest(tool_id:str)->bool:
    return str(tool_id) in OVERRIDES

def manifest_for(tool_id:str)->ToolManifest:
    tool_id=str(tool_id)
    if tool_id in OVERRIDES:
        return OVERRIDES[tool_id]
    return ToolManifest(
        tool_id=tool_id,
        native_semantics=tool_id,
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=GENERIC_BINDINGS,
    )

def reconstructs(tool_id:str,required_behaviors=())->bool:
    m=manifest_for(tool_id)
    required=frozenset(required_behaviors)
    return m.complete() and required<=m.behavior_ids()

def require_reconstruction(tool_id:str,required_behaviors=()):
    m=manifest_for(tool_id)
    if not m.complete():
        raise RuntimeError(f"TOOL_MANIFEST_INCOMPLETE:{tool_id}")
    missing=frozenset(required_behaviors)-m.behavior_ids()
    if missing:
        raise RuntimeError(
            "TOOL_PROTECTED_BEHAVIOR_UNRECOVERED:"
            +tool_id+":"+",".join(sorted(missing))
        )
    return m
