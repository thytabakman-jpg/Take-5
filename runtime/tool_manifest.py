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
    ProtectedBinding(
        "PROTECTED_TRANSITION_INTEGRITY",
        "CROSS",
        "runtime/protected_transition_integrity.py",
        "tests/test_protected_transition_integrity.py",
    ),
)

IMPROVEMENT_CORE_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "IMPROVEMENTCORE_CONTROLLER_OWNERSHIP",
        "PRE",
        "runtime/improvement_core_manager.py",
        "tests/test_improvement_core_manager.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_OBSERVER_FIRST_MODE",
        "PRE",
        "runtime/ic028_operator.py",
        "tests/test_improvement_core_manager.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_CONFIGURED_TOOL_EXECUTION",
        "INTRA",
        "runtime/improvement_core_tool_bridge.py",
        "tests/test_improvement_core_regime.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_RECURSIVE_PARENT_CONTROL",
        "INTRA",
        "runtime/improvement_core_recursive_manager.py",
        "tests/test_improvement_core_regime.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_HF002_DEFAULT_LOCAL_RECURRENCE",
        "INTRA",
        "runtime/improvement_core_hf2_default.py",
        "tests/test_improvement_core_hf2_default.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_DURABLE_NEGATIVE_LEARNING",
        "CROSS",
        "runtime/improvement_core_learning_memory.py",
        "tests/test_improvement_core_regime.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_DURABLE_KNOWLEDGE_CAPTURE",
        "CROSS",
        "runtime/improvement_core_knowledge_ledger.py",
        "tests/test_improvement_core_knowledge_ledger.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_STRICT_PROGRESS",
        "POST",
        "runtime/improvement_core_progress_relation.py",
        "tests/test_improvement_core_progress_relation.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_EXTERNAL_ACQUISITION",
        "PRE",
        "runtime/improvement_core_external_acquisition.py",
        "tests/test_improvement_core_external_acquisition.py",
    ),
    ProtectedBinding(
        "IMPROVEMENTCORE_PLURAL_FRONTIER_PRESERVATION",
        "INTRA",
        "runtime/improvement_core_math_spine.py",
        "tests/test_improvement_core_regime.py",
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

HF001_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "HF001_GOVERNED_EPISODE",
        "INTRA",
        "runtime/hf1_episode.py",
        "tests/test_hf1_episode.py",
    ),
)

HF002_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "HF002_LOCAL_RECURSIVE_CONTINUATION",
        "INTRA",
        "runtime/hf002_recursive_continuation.py",
        "tests/test_root_cause_hf2.py",
    ),
)

ROOT_CAUSE_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "ROOT_CAUSE_ROOTNESS_SELECTOR",
        "INTRA",
        "runtime/root_cause.py",
        "tests/test_root_cause_hf2.py",
    ),
    ProtectedBinding(
        "ROOT_CAUSE_HF002_LOCAL_RECURRENCE",
        "INTRA",
        "runtime/root_cause.py",
        "tests/test_root_cause_hf2.py",
    ),
    ProtectedBinding(
        "ROOT_CAUSE_IMPROVEMENTCORE_PARENT_HANDOFF",
        "POST",
        "runtime/root_cause_managed.py",
        "tests/test_root_cause_hf2.py",
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

OVERRIDES={
    "ImprovementCore":ToolManifest(
        tool_id="ImprovementCore",
        native_semantics="IC-028",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_HF002_LOCAL_RELATIVE_CLOSE",
        reentry_contract="HF001_OR_IMPROVEMENTCORE_PARENT_REPLAN",
        bindings=IMPROVEMENT_CORE_BINDINGS,
    ),
    "MT":ToolManifest(
        tool_id="MT",
        native_semantics="MT",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=MT_BINDINGS,
    ),
    "HF001":ToolManifest(
        tool_id="HF001",
        native_semantics="HF001",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=HF001_BINDINGS,
    ),
    "HF002":ToolManifest(
        tool_id="HF002",
        native_semantics="HF002",
        geometry_policy="INHERIT_WRAPPED_CAPABILITY",
        closure_contract="LOCAL_RELATIVE_CLOSE",
        reentry_contract="HF001",
        bindings=HF002_BINDINGS,
    ),
    "RootCause":ToolManifest(
        tool_id="RootCause",
        native_semantics="RootCause",
        geometry_policy="D36_C",
        closure_contract="TRC_LOCAL_ROOT_CLOSE",
        reentry_contract="HF002_THEN_IMPROVEMENTCORE",
        bindings=ROOT_CAUSE_BINDINGS,
    ),
    "ASSERT":ToolManifest(
        tool_id="ASSERT",
        native_semantics="ASSERT",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=ASSERT_BINDINGS,
    ),
}

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
