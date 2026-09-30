"""Canonical tool identity and reconstruction manifests.

A configured tool is complete only when its canonical manifest reconstructs
every protected behavior required by that tool's current identity.

The manifest references implementation/witness surfaces. It does not duplicate
their semantics.
"""
from dataclasses import dataclass
from a5_programs import REGISTRY as A5_REGISTRY
from learning_tool_bridge import SPECS as LEARNING_SPECS

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
    ProtectedBinding(
        "CONFIGURED_HF2_RECURRENCE",
        "CROSS",
        "runtime/configured_hf2_execution.py",
        "tests/test_full_invocation_portfolio.py",
    ),
    ProtectedBinding(
        "FULL_CONFIGURED_INVOCATION_PROFILE",
        "CROSS",
        "runtime/global_tool_execution.py",
        "tests/test_full_invocation_portfolio.py",
    ),
)

ICC128_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "ICC128_ENDOGENOUS_CONTROLLER_LOOP",
        "INTRA",
        "runtime/icc128_autonomous_controller.py",
        "tests/test_icc128_current.py",
    ),
    ProtectedBinding(
        "ICC128_TOOL_CONDUCTOR_PREWORK_CONSULTATION",
        "INTRA",
        "runtime/controller_tool_conductor.py",
        "tests/test_icc128_current.py",
    ),
    ProtectedBinding(
        "ICC128_STATE_RELATIVE_SELECTOR",
        "INTRA",
        "runtime/rho128_policy.py",
        "tests/test_icc128_current.py",
    ),
    ProtectedBinding(
        "ICC128_RESELECTION_ON_MATERIAL_DELTA",
        "POST",
        "runtime/rho128_policy.py",
        "tests/test_icc128_current.py",
    ),
    ProtectedBinding(
        "ICC128_SEMANTIC_GENERATION",
        "PRE",
        "runtime/icc128_semantic_generator_adapter.py",
        "tests/test_icc128_current.py",
    ),
    ProtectedBinding(
        "ICC128_JANE_CONTINUITY_HANDOFF",
        "PRE",
        "runtime/jane_icc128_bridge.py",
        "tests/test_jane_icc128_bridge.py",
    ),
    ProtectedBinding(
        "ICC128_MINIMAL_RESPONSE_SELECTION",
        "POST",
        "runtime/adaptive_response_selector.py",
        "tests/test_adaptive_response_selector.py",
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
        "IMPROVEMENTCORE_TOOL_CONDUCTOR_PRESELECTION_CONSULTATION",
        "INTRA",
        "runtime/controller_tool_conductor.py",
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
        "IMPROVEMENTCORE_CONFIGURED_TOOL_DURABLE_KNOWLEDGE_CAPTURE",
        "CROSS",
        "runtime/improvement_core_regime.py",
        "tests/test_improvement_core_regime.py",
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
    ProtectedBinding(
        "IMPROVEMENTCORE_PROSE_RETURN_GATE",
        "POST",
        "runtime/improvement_core_return_gate.py",
        "tests/test_prose_transition_layers.py",
    ),
)

PROJECT_MANAGER_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding("PROJECTMANAGER_PROJECT_IDENTITY_BINDING","PRE","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_PROJECT_PACKAGE_VALIDATION","PRE","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_SINGLE_OWNER_AUTHORITY","INTRA","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_LOCAL_CHANGE_ROUTING","INTRA","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_OPEN_PRESERVATION","POST","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_WBS_SCHEDULE_SEPARATION","INTRA","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_IMPACT_REENTRY","POST","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_SELF_MANAGEMENT","CROSS","projects/project-manager/SELF_MANAGEMENT.md","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_IMPROVEMENTCORE_HANDOFF","CROSS","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_TRANSFERCORE_EVIDENCE_ONLY","CROSS","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_PREPROJECT_ADMISSION_GATE","PRE","runtime/project_manager.py","tests/test_project_manager.py"),
    ProtectedBinding("PROJECTMANAGER_MANDATORY_MANAGEMENT_SPINE","PRE","runtime/project_manager_management_spine.py","tests/test_project_manager_management_spine.py"),
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

GOAL_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "GOAL_EVIDENCE_GROUNDED_ADMISSION",
        "PRE",
        "runtime/goal.py",
        "tests/test_goal.py",
    ),
    ProtectedBinding(
        "GOAL_CONSTRAINT_SEPARATION",
        "INTRA",
        "runtime/goal.py",
        "tests/test_goal.py",
    ),
    ProtectedBinding(
        "GOAL_OBJECT_X_T_I_SIGMA",
        "INTRA",
        "runtime/goal.py",
        "tests/test_goal.py",
    ),
    ProtectedBinding(
        "GOAL_PLURALITY_FAIL_OPEN",
        "POST",
        "runtime/goal.py",
        "tests/test_goal.py",
    ),
    ProtectedBinding(
        "GOAL_ROBUST_MT_PREREQUISITE",
        "PRE",
        "runtime/goal.py",
        "tests/test_goal.py",
    ),
    ProtectedBinding(
        "GOAL_FULL_TOOL_IDENTITY",
        "PRE",
        "architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md",
        "tests/test_goal_fullmath_identity.py",
    ),
)

MULTIOBJECT_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "MO_FROZEN_OBJECT_IDENTITY",
        "PRE",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_REQUIRED_PAIR_COVERAGE",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_PAIR_ROUTE_ISOLATION",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_INDEPENDENT_FULL_JOINT_ROUTE",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_LOWER_ORDER_SYNTHESIS",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_TYPED_RECONCILIATION",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_REDUCIBILITY_CHALLENGE",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_OPEN_CONFLICT_INCOMPARABILITY_PRESERVATION",
        "POST",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_GATED_VIEW_EXPANSION",
        "INTRA",
        "runtime/multiobject.py",
        "tests/test_multiobject.py",
    ),
    ProtectedBinding(
        "MO_CONFIGURED_ADEQUACY_BOUNDARY",
        "CROSS",
        "architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md",
        "tests/test_multiobject_fullmath_identity.py",
    ),
    ProtectedBinding(
        "MO_FULL_TOOL_IDENTITY",
        "PRE",
        "architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md",
        "tests/test_multiobject_fullmath_identity.py",
    ),
)

GDOS_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "GDOS_FROZEN_INDEPENDENT_OBSERVATION",
        "INTRA",
        "runtime/gdos.py",
        "tests/test_recovered_native_tools_20260927.py",
    ),
)

DISCRIMINATOR_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "DISCRIMINATOR_PRESERVE_PLURAL_OPEN",
        "INTRA",
        "runtime/discriminator.py",
        "tests/test_recovered_native_tools_20260927.py",
    ),
)

RTC_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "RTC_STRICT_GAIN_PRESERVATION_GATE",
        "INTRA",
        "runtime/raise_the_ceiling.py",
        "tests/test_recovered_native_tools_20260927.py",
    ),
)

BIAS_PERTURBATION_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "BIAS_PERTURBATION_INVARIANCE_GUARD",
        "INTRA",
        "runtime/bias_perturbation.py",
        "tests/test_recovered_native_tools_20260927.py",
    ),
)

DIAGNOSIS_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "DIAGNOSIS_MECHANISM_BEFORE_REPAIR",
        "INTRA",
        "runtime/diagnosis.py",
        "tests/test_recovered_native_tools_20260927.py",
    ),
)



FOUR_TOOL_RECOVERY_BINDINGS={
    "MTA":GENERIC_BINDINGS+(
        ProtectedBinding(
            "MTA_STRUCTURAL_MODEL_RECONSTRUCTION",
            "INTRA",
            "runtime/mta.py",
            "tests/test_four_tool_recovery_20260927.py",
        ),
    ),
    "Architecture":GENERIC_BINDINGS+(
        ProtectedBinding(
            "ARCHITECTURE_CONTRACT_RELATIVE_ANALYSIS",
            "INTRA",
            "runtime/architecture_analysis.py",
            "tests/test_four_tool_recovery_20260927.py",
        ),
        ProtectedBinding(
            "ARCHITECTURE_PROTECTED_PROSE_CONSTRAINT_BINDING",
            "POST",
            "runtime/architecture_analysis.py",
            "tests/test_prose_transition_layers.py",
        ),
        ProtectedBinding(
            "ARCHITECTURE_UNIT_JOB_PURITY_GATE",
            "INTRA",
            "runtime/architecture_analysis.py",
            "tests/test_prose_transition_layers.py",
        ),
    ),
    "PD":GENERIC_BINDINGS+(
        ProtectedBinding(
            "PD_MINIMAL_RESULT_SENSITIVITY",
            "INTRA",
            "runtime/pd.py",
            "tests/test_four_tool_recovery_20260927.py",
        ),
    ),
    "PDAudit":GENERIC_BINDINGS+(
        ProtectedBinding(
            "PDAUDIT_FRAME_FIBER_SENSITIVITY",
            "INTRA",
            "runtime/pd_audit.py",
            "tests/test_four_tool_recovery_20260927.py",
        ),
        ProtectedBinding(
            "PDAUDIT_RAW_NORMALIZATION_SEPARATION",
            "POST",
            "runtime/pd_audit.py",
            "tests/test_four_tool_recovery_20260927.py",
        ),
    ),
}

SOLUTION_TO_MY_PROBLEM_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "SolutionToMyProblem_EXPLICIT_NATIVE_IDENTITY",
        "INTRA",
        "runtime/solution_to_my_problem.py",
        "tests/test_explicit_native_manifests.py",
    ),
    ProtectedBinding(
        "SOLUTION_PROTECTED_PROSE_PRESERVATION",
        "INTRA",
        "runtime/solution_to_my_problem.py",
        "tests/test_prose_transition_layers.py",
    ),
)

PROSE_BINDINGS=GENERIC_BINDINGS+(
    ProtectedBinding(
        "Prose_EXPLICIT_NATIVE_IDENTITY",
        "INTRA",
        "runtime/prose.py",
        "tests/test_explicit_native_manifests.py",
    ),
    ProtectedBinding(
        "PROSE_PROTECTED_CONTRACT_ACCEPTANCE",
        "PRE",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_AFFIRMATIVE_FIRST_GATE",
        "INTRA",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_FIRST_MENTION_PERSON_DATES",
        "INTRA",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_NUMERIC_YEAR_DATING_GATE",
        "INTRA",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_ORDERED_ANCHOR_GATE",
        "INTRA",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_SEMANTIC_STRENGTH_NO_INFLATION_RECEIPTS",
        "POST",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
    ProtectedBinding(
        "PROSE_READER_LOAD_GATE",
        "INTRA",
        "runtime/prose.py",
        "tests/test_prose.py",
    ),
)

OVERRIDES={
    "ProjectManager":ToolManifest(
        tool_id="ProjectManager",
        native_semantics="authority-governed nondeterministic labeled project-transition system with supervisory frontier policy",
        geometry_policy="D36_C",
        closure_contract="PROJECT_CONTROL_RELATIVE_CLOSE_PLUS_TRC",
        reentry_contract="HF002_THEN_HF001_OR_IMPROVEMENTCORE",
        bindings=PROJECT_MANAGER_BINDINGS,
        lineage_contract="architecture/PROJECT_MANAGER_FULL_TOOL_MATH_003_2026-09-27.md",
    ),
    "MTA":ToolManifest(
        tool_id="MTA",
        native_semantics="MTA_sem=<GenerateStructuralHypotheses,SelectAnalysisPackage,ReconstructProtectedModel>",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF002_THEN_HF001",
        bindings=FOUR_TOOL_RECOVERY_BINDINGS["MTA"],
        lineage_contract="architecture/FOUR_TOOL_STRONG_REALITY_RECOVERY_162_2026-09-27.md",
    ),
    "Architecture":ToolManifest(
        tool_id="Architecture",
        native_semantics="contract-relative AA_K(A) architecture analysis and successor frontier with protected unit-job purity",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF002_THEN_HF001",
        bindings=FOUR_TOOL_RECOVERY_BINDINGS["Architecture"],
        lineage_contract="architecture/PROSE_ARCHITECTURE_READER_LOAD_MATHEMATICS_004_2026-09-30.md",
    ),
    "PD":ToolManifest(
        tool_id="PD",
        native_semantics="quotient result classes, fibers, and representation-relative minimal result-sensitive coordinate sets",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF002_THEN_HF001",
        bindings=FOUR_TOOL_RECOVERY_BINDINGS["PD"],
        lineage_contract="architecture/FOUR_TOOL_STRONG_REALITY_RECOVERY_162_2026-09-27.md",
    ),
    "PDAudit":ToolManifest(
        tool_id="PDAudit",
        native_semantics="PDAudit_1.1 fixed-frame fiber/sensitivity evaluator with raw-normalized separation",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF002_THEN_HF001",
        bindings=FOUR_TOOL_RECOVERY_BINDINGS["PDAudit"],
        lineage_contract="architecture/FOUR_TOOL_STRONG_REALITY_RECOVERY_162_2026-09-27.md",
    ),
    "ICC128":ToolManifest(
        tool_id="ICC128",
        native_semantics="ICC128",
        geometry_policy="D36_C",
        closure_contract="ICC128_CONTROLLER_CLOSE_PLUS_TRC",
        reentry_contract="STATE_RELATIVE_RESELECT_THEN_HF001",
        bindings=ICC128_BINDINGS,
        lineage_contract="legacy/icc128-legacy/snapshot/math/ICC128_FULL_TOOL_MATH_002_2026-09-26.md",
    ),
    "ImprovementCore":ToolManifest(
        tool_id="ImprovementCore",
        native_semantics="IC-028",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_HF002_LOCAL_RELATIVE_CLOSE",
        reentry_contract="HF001_OR_IMPROVEMENTCORE_PARENT_REPLAN",
        bindings=IMPROVEMENT_CORE_BINDINGS,
    ),
    "SolutionToMyProblem":ToolManifest(
        tool_id="SolutionToMyProblem",
        native_semantics="candidate solution frontier with protected-prose preservation receipts",
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF002_THEN_HF001",
        bindings=SOLUTION_TO_MY_PROBLEM_BINDINGS,
        lineage_contract="architecture/PROSE_PROTECTED_TRANSITION_MATHEMATICS_001_2026-09-30.md",
    ),
    "Prose":ToolManifest(
        tool_id="Prose",
        native_semantics="protected reader-facing prose acceptance under frozen contract with semantic-strength-no-inflation and reader-load receipts",
        geometry_policy="D36_C",
        closure_contract="PROSE_PASS_OR_TYPED_REPAIR_OPEN_BLOCKED_PLUS_TRC",
        reentry_contract="HF002_THEN_HF001",
        bindings=PROSE_BINDINGS,
        lineage_contract="architecture/PROSE_ARCHITECTURE_READER_LOAD_MATHEMATICS_004_2026-09-30.md",
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
    "GOAL":ToolManifest(
        tool_id="GOAL",
        native_semantics="GOAL",
        geometry_policy="D36_C",
        closure_contract="GOAL_ADMISSIBILITY_PLUS_TRC",
        reentry_contract="HF001",
        bindings=GOAL_BINDINGS,
        lineage_contract="architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md",
    ),
    "MultiObject":ToolManifest(
        tool_id="MultiObject",
        native_semantics="MULTIOBJECT_V0_2_ADAPTIVE",
        geometry_policy="D36_C_PLUS_NATIVE_ARITY_DIRECTION_VIEW",
        closure_contract="BASIS_RELATIVE_RELATION_CLOSURE_PLUS_TRC",
        reentry_contract="HF002_THEN_HF001",
        bindings=MULTIOBJECT_BINDINGS,
        lineage_contract="architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md",
    ),
    "GDOS":ToolManifest(
        tool_id="GDOS",
        native_semantics="GOAL_DECOUPLED_OBSERVATION_SWEEP",
        geometry_policy="D36_C",
        closure_contract="OBSERVE_CAPTURE_RECONCILE_PLUS_TRC",
        reentry_contract="HF001",
        bindings=GDOS_BINDINGS,
        lineage_contract="architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md",
    ),
    "Discriminator":ToolManifest(
        tool_id="Discriminator",
        native_semantics="PREDICATE_DISCRIMINATION",
        geometry_policy="D36_C",
        closure_contract="UNIQUE_PLURAL_OPEN_PLUS_TRC",
        reentry_contract="HF001",
        bindings=DISCRIMINATOR_BINDINGS,
        lineage_contract="architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md",
    ),
    "RTC":ToolManifest(
        tool_id="RTC",
        native_semantics="RAISE_THE_CEILING_C48_SPECIALIZATION",
        geometry_policy="D36_C",
        closure_contract="STRICT_GAIN_OR_TYPED_NO_GAIN_PLUS_TRC",
        reentry_contract="HF001",
        bindings=RTC_BINDINGS,
        lineage_contract="architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md",
    ),
    "BiasPerturbation":ToolManifest(
        tool_id="BiasPerturbation",
        native_semantics="NUISANCE_PERTURBATION_INVARIANCE_AUDIT",
        geometry_policy="D36_C",
        closure_contract="PERTURBATION_COVERAGE_PLUS_TRC",
        reentry_contract="HF001",
        bindings=BIAS_PERTURBATION_BINDINGS,
        lineage_contract="architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md",
    ),
    "Diagnosis":ToolManifest(
        tool_id="Diagnosis",
        native_semantics="FAILURE_DIAGNOSIS_C17_SPECIALIZATION",
        geometry_policy="D36_C",
        closure_contract="MECHANISM_DISPOSITION_PLUS_TRC",
        reentry_contract="HF001",
        bindings=DIAGNOSIS_BINDINGS,
        lineage_contract="architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md",
    ),

}

# Registry-defined capabilities have tool-specific identity in their executable
# registries. These backfills do not invent new semantics; they project those
# already-typed identities into the canonical manifest layer.
for _i in range(1,50):
    _pid=f"C{_i:02d}"
    _spec=A5_REGISTRY.get(_pid)
    OVERRIDES.setdefault(_pid,ToolManifest(
        tool_id=_pid,
        native_semantics=f"{_spec.job} -> {','.join(_spec.protected_outputs)}",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=GENERIC_BINDINGS+(
            ProtectedBinding(
                f"{_pid}_REGISTERED_CAPABILITY_IDENTITY",
                "INTRA",
                "runtime/a5_programs.py",
                "tests/test_a5_registry.py",
            ),
        ),
        lineage_contract="architecture/EXPLICIT_TOOL_MANIFEST_BACKFILL_161_2026-09-27.md",
    ))

for _spec in LEARNING_SPECS:
    OVERRIDES.setdefault(_spec.program_id,ToolManifest(
        tool_id=_spec.program_id,
        native_semantics=f"{_spec.obligation}: {_spec.input_type} -> {_spec.output_type}",
        geometry_policy="D36_C",
        closure_contract="TRC",
        reentry_contract="HF001",
        bindings=GENERIC_BINDINGS+(
            ProtectedBinding(
                f"{_spec.program_id}_TYPED_LEARNING_IDENTITY",
                "INTRA",
                "runtime/learning_tool_bridge.py",
                "tests/test_learning_tool_configured_runs.py",
            ),
        ),
        lineage_contract="architecture/EXPLICIT_TOOL_MANIFEST_BACKFILL_161_2026-09-27.md",
    ))

_DEDICATED_NATIVE={
    "Reconciler":(
        "admitted results -> coherent joint state with conflicts/subsumptions/revisions/relations/OPEN",
        "runtime/reconcile.py",
    ),
    "DelegatedExecutor":(
        "bounded authority-preserving delegation with exact input/output hashes and reintegration receipt",
        "runtime/delegation.py",
    ),
    "TRC":(
        "recursive material consequence closure with typed disposition, verification and consumption",
        "runtime/tool_run_closure.py",
    ),
    "CurrentnessAudit":(
        "built basis vs latest admitted basis -> KEEP/PATCH/REPLACE/OPEN",
        "runtime/currentness_audit.py",
    ),
    "CapabilityFoundry":(
        "typed capability candidate generation without self-admission or self-authorization",
        "runtime/capability_foundry.py",
    ),
    "EmergentAdmission":(
        "load-bearing object admission guard preserving OPEN and executable binding requirements",
        "runtime/emergent_admission.py",
    ),
    "HistoricalReconstruction":(
        "frozen-job protected-result predecessor/successor comparison with execution witnesses",
        "runtime/historical_reconstruction.py",
    ),
    "ZeroRequest":(
        "observation-only governed episode over an addressable corpus without manufacturing a substantive job",
        "runtime/zero_request_episode.py",
    ),
    "SolutionToMyProblem":(
        "candidate solution frontier requiring execution/effect/preservation/verification/closure receipts",
        "runtime/solution_to_my_problem.py",
    ),
    "Prose":(
        "protected prose contract audit with semantic-strength-no-inflation acceptance receipts",
        "runtime/prose.py",
    ),
    "DesiredJane":(
        "evidence-polarity reconstruction of required/prohibited/open/conflicting Jane coordinates",
        "runtime/desired_jane.py",
    ),
    "QuestionWorthAsking":(
        "nondominated live-question selection over result sensitivity, information gain, unlock, actionability and burden",
        "runtime/question_worth_asking.py",
    ),
    "LambdaMath":(
        "set-valued entry-state reconstruction with continuation-equivalence quotienting and result-sensitive ambiguity",
        "runtime/lambda_math.py",
    ),
    "SemanticResolutionPipeline":(
        "configured black-box semantic-resolution stage plan with typed residual activation",
        "runtime/semantic_resolution_pipeline.py",
    ),
    "ToolConductor":(
        "exhaustive product over registered repertoire with one fail-closed execution disposition per factor",
        "runtime/portable_tool_conductor.py",
    ),
}

for _pid,(_sem,_impl) in _DEDICATED_NATIVE.items():
    OVERRIDES.setdefault(_pid,ToolManifest(
        tool_id=_pid,
        native_semantics=_sem,
        geometry_policy="D36_C",
        closure_contract="TRC_PLUS_TYPED_OPEN",
        reentry_contract="HF001",
        bindings=GENERIC_BINDINGS+(
            ProtectedBinding(
                f"{_pid}_EXPLICIT_NATIVE_IDENTITY",
                "INTRA",
                _impl,
                "tests/test_explicit_native_manifests.py",
            ),
        ),
        lineage_contract="architecture/EXPLICIT_TOOL_MANIFEST_BACKFILL_161_2026-09-27.md",
    ))


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
