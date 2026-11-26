"""Configured-run registry for foundation and admitted learning capabilities."""
from configured_run import (
    DEFAULT_RECURRENCE_ENGINE,
    SELF_RECURRENCE_ENGINE,
    ConfiguredRunSpec,
)
from learning_tool_bridge import SPECS as LEARNING_SPECS
from execution_profile import recurrence_engine_for
from program_registry import ProgramRegistry, ProgramSpec
from types import MappingProxyType

# I. Registered identity inventory.
# Declared capability metadata is not evidence of an executable binding.
_SPECS = []


def _define(pid, source, job, roles, out):
    _SPECS.append(ProgramSpec(
        pid, source, job, tuple(roles.split(",")), (out,), "fixture", False,
        "RECURSIVE_EPISODE", "HOST_HF001", "MATERIAL_RESULT_OR_SEARCH_DELTA",
        "HOLDOUT_FOR_STRONGER_TERMINAL_CLAIM",
    ))


_define("C01","CAPABILITY_REGISTRY_V4_IC022","Task and Object Typing","K,S,O,C","typed_task_context")
_define("C02","CAPABILITY_REGISTRY_V4_IC022","Referent Continuity","K,S,O,C","identity_relation")
_define("C03","CAPABILITY_REGISTRY_V4_IC022","History Supersession","K,S,O,C","lineage")
_define("C04","CAPABILITY_REGISTRY_V4_IC022","Source Result Freeze","K,S,C","frozen_source")
_define("C05","CAPABILITY_REGISTRY_V4_IC022","Target Job Freeze","K,S,C","target_contract")
_define("C06","CAPABILITY_REGISTRY_V4_IC022","External Dependence","K,S,O,C","dependency_map")
_define("C07","CAPABILITY_REGISTRY_V4_IC022","Hidden Dependency","S,O,G","dependency_edges")
_define("C08","CAPABILITY_REGISTRY_V4_IC022","Dependency Spine","S,O","dependency_spines")
_define("C09","CAPABILITY_REGISTRY_V4_IC022","Layer Control Mapping","S,O,M","typed_graph")
_define("C10","CAPABILITY_REGISTRY_V4_IC022","Representation Attack","K,O,M,C","representation_residual")
_define("C11","CAPABILITY_REGISTRY_V4_IC022","Result Sensitivity","K,O,M,C","sensitive_support")
_define("C12","CAPABILITY_REGISTRY_V4_IC022","Invariant Localization","K,O,M,C","invariant_core")
_define("C13","CAPABILITY_REGISTRY_V4_IC022","Attribution Separation","K,S,O,C","attributed_chain")
_define("C14","CAPABILITY_REGISTRY_V4_IC022","Hostile Review","K,O,M,C,R","defect_record")
_define("C15","CAPABILITY_REGISTRY_V4_IC022","Novelty Comparator","K,S,O,C","collision_residual")
_define("C16","CAPABILITY_REGISTRY_V4_IC022","Change Frontier","K,S,O,C,R","change_frontier")
_define("C17","CAPABILITY_REGISTRY_V4_IC022","Failure Diagnosis","K,S,O,M,C","mechanism_disposition")
_define("C18","CAPABILITY_REGISTRY_V4_IC022","Root Cause Escalation","K,S,O,R","root_disposition")
_define("C19","CAPABILITY_REGISTRY_V4_IC022","Recursive Discovery","K,S,O,G,M,R","discovery_trace")
_define("C20","CAPABILITY_REGISTRY_V4_IC022","Rival Reconstruction","K,S,O,G,M","rivals")
_define("C21","CAPABILITY_REGISTRY_V4_IC022","Successor Generation","K,S,O,G,R","candidates")
_define("C22","CAPABILITY_REGISTRY_V4_IC022","Improvement Frontier","K,S,O,R","improvement_frontier")
_define("C23","CAPABILITY_REGISTRY_V4_IC022","Source Target Relation","K,S,O,C","typed_relation")
_define("C24","CAPABILITY_REGISTRY_V4_IC022","Defect Repair","K,S,O,G,C,U","repaired_candidate")
_define("C25","CAPABILITY_REGISTRY_V4_IC022","Behavior Compression","K,S,O,M,C","equivalent_candidate")
_define("C26","CAPABILITY_REGISTRY_V4_IC022","System Architecture Improvement","K,S,O,G,M,C,R,U","architecture_successor")
_define("C27","CAPABILITY_REGISTRY_V4_IC022","Subsystem Improvement","K,S,O,G,C,U","subsystem_successor")
_define("C28","CAPABILITY_REGISTRY_V4_IC022","Component Improvement","K,S,O,G,C,U","component_successor")
_define("C29","CAPABILITY_REGISTRY_V4_IC022","Interface Improvement","K,S,O,G,M,C,U","interface_successor")
_define("C30","CAPABILITY_REGISTRY_V4_IC022","Boundary Redesign","K,S,O,G,M,C,U","boundary_successor")
_define("C31","CAPABILITY_REGISTRY_V4_IC022","Cross Layer Improvement","K,S,O,G,M,C,R,U","synchronized_architecture")
_define("C32","CAPABILITY_REGISTRY_V4_IC022","Leverage Routing","K,S,O,R","routes")
_define("C33","CAPABILITY_REGISTRY_V4_IC022","Strict Gain","K,S,O,C","gain_disposition")
_define("C34","CAPABILITY_REGISTRY_V4_IC022","Regression Check","K,S,O,C","regression_disposition")
_define("C35","CAPABILITY_REGISTRY_V4_IC022","Incomparable Successors","K,S,O,C,R","nondominated_set")
_define("C36","CAPABILITY_REGISTRY_V4_IC022","Recompute Architecture","K,S,O,R,U","affected_update")
_define("C37","CAPABILITY_REGISTRY_V4_IC022","Transfer Provenance","K,S,O,C","provenance_chain")
_define("C38","CAPABILITY_REGISTRY_V4_IC022","Transfer License","K,S,C","license_disposition")
_define("C39","CAPABILITY_REGISTRY_V4_IC022","Target Effect","K,S,O,C","target_effect")
_define("C40","CAPABILITY_REGISTRY_V4_IC022","Existing Coverage","K,S,O,C","coverage")
_define("C41","CAPABILITY_REGISTRY_V4_IC022","Downstream Rescue","K,S,O,C","rescue_disposition")
_define("C42","CAPABILITY_REGISTRY_V4_IC022","Transfer Disposition","K,S,C","transfer_status")
_define("C43","CAPABILITY_REGISTRY_V4_IC022","Consequence Handoff","K,S,C,U","handoff")
_define("C44","CAPABILITY_REGISTRY_V4_IC022","Regression Verification","K,S,O,C","verification")
_define("C45","CAPABILITY_REGISTRY_V4_IC022","Holdout","K,S,O,C","holdout_result")
_define("C46","CAPABILITY_REGISTRY_V4_IC022","Ablation","K,S,O,M,C","causal_effect")
_define("C47","CAPABILITY_REGISTRY_V4_IC022","Relative Closure","K,S,O,R,C","closure_disposition")
_define("C48","CAPABILITY_REGISTRY_V4_IC022","Raise Ceiling","K,S,O,G,M,C,R","strict_gain_or_failure")
_define("C49","CAPABILITY_REGISTRY_V4_IC022","Corpus Navigation","K,S,O,G,R","navigation_trace")

EXPECTED_C={f"C{i:02d}" for i in range(1,50)}

_definition_registry = ProgramRegistry()
for _definition in _SPECS:
    _definition_registry.register(_definition)
if _definition_registry.ids() != EXPECTED_C:
    raise ValueError("Current capability definition coverage mismatch")
CAPABILITY_DEFINITIONS = MappingProxyType({spec.program_id: spec for spec in _SPECS})

LEARNING_TOOLS=tuple(spec.program_id for spec in LEARNING_SPECS)

MATERIAL_TOOLS=tuple(list(CAPABILITY_DEFINITIONS)+[
"ImprovementCore","ProjectManager","ICC128","MT","MTA","Architecture","PD","PDAudit","GDOS","Discriminator","Reconciler",
"DelegatedExecutor","HF001","HF002","RootCause","TRC","RTC","BiasPerturbation","CurrentnessAudit",
"CapabilityFoundry","EmergentAdmission","HistoricalReconstruction","ZeroRequest","MultiObject","Diagnosis",
"ASSERT","GOAL","SolutionToMyProblem","Prose","DesiredJane","QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline","RecursiveCompiler","ToolConductor"
]+list(LEARNING_TOOLS))

ASSERT_LAYERS=("ASSERT_LAYER_1","ASSERT_LAYER_2")

# II. Independently authored admission requirements.
# Independent requirements for configured admission, not a list of actual
# manifest bindings. ConfiguredRunSpec.complete() checks these against the
# manifest; deriving them from that manifest would erase this verification.
REQUIRED_PROTECTED_BEHAVIORS={
    "ProjectManager":(
        "PROJECTMANAGER_PROJECT_IDENTITY_BINDING",
        "PROJECTMANAGER_PROJECT_PACKAGE_VALIDATION",
        "PROJECTMANAGER_SINGLE_OWNER_AUTHORITY",
        "PROJECTMANAGER_LOCAL_CHANGE_ROUTING",
        "PROJECTMANAGER_OPEN_PRESERVATION",
        "PROJECTMANAGER_WBS_SCHEDULE_SEPARATION",
        "PROJECTMANAGER_IMPACT_REENTRY",
        "PROJECTMANAGER_SELF_MANAGEMENT",
        "PROJECTMANAGER_IMPROVEMENTCORE_HANDOFF",
        "PROJECTMANAGER_TRANSFERCORE_EVIDENCE_ONLY",
        "PROJECTMANAGER_PREPROJECT_ADMISSION_GATE",
        "PROJECTMANAGER_MANDATORY_MANAGEMENT_SPINE",
        "PROJECTMANAGER_FAILURE_PREVENTION_ENVELOPE",
        "PROJECTMANAGER_TRANSFORM_IMPACT_VERIFICATION_GATE",
        "PROJECTMANAGER_PROJECT_STATE_TRANSACTION",
        "PROJECTMANAGER_NO_FALSE_CLOSE_WITH_FRONTIER",
        "PROJECTMANAGER_HISTORICAL_FAILURE_HOLDOUT_GATE",
    ),
    "ICC128":(
        "ICC128_ENDOGENOUS_CONTROLLER_LOOP",
        "ICC128_TOOL_CONDUCTOR_PREWORK_CONSULTATION",
        "ICC128_STATE_RELATIVE_SELECTOR",
        "ICC128_RESELECTION_ON_MATERIAL_DELTA",
        "ICC128_SEMANTIC_GENERATION",
        "ICC128_JANE_CONTINUITY_HANDOFF",
        "ICC128_MINIMAL_RESPONSE_SELECTION",
        "ICC128_CANONICAL_TOP_LEVEL_SUBSTANTIVE_OWNERSHIP",
    ),
    "ImprovementCore":(
        "IMPROVEMENTCORE_DELEGATED_EPISODE_CONTROLLER_OWNERSHIP",
        "IMPROVEMENTCORE_TOOL_CONDUCTOR_PRESELECTION_CONSULTATION",
        "IMPROVEMENTCORE_OBSERVER_FIRST_MODE",
        "IMPROVEMENTCORE_CONFIGURED_TOOL_EXECUTION",
        "IMPROVEMENTCORE_RECURSIVE_PARENT_CONTROL",
        "IMPROVEMENTCORE_HF002_DEFAULT_LOCAL_RECURRENCE",
        "IMPROVEMENTCORE_DURABLE_NEGATIVE_LEARNING",
        "IMPROVEMENTCORE_DURABLE_KNOWLEDGE_CAPTURE",
        "IMPROVEMENTCORE_CONFIGURED_TOOL_DURABLE_KNOWLEDGE_CAPTURE",
        "IMPROVEMENTCORE_STRICT_PROGRESS",
        "IMPROVEMENTCORE_EXTERNAL_ACQUISITION",
        "IMPROVEMENTCORE_PLURAL_FRONTIER_PRESERVATION",
        "IMPROVEMENTCORE_PROSE_RETURN_GATE",
    ),
    "MT":("MT_BLACK_BOX_SEMANTIC_RETURN_GATE",),
    "MTA":("MTA_STRUCTURAL_MODEL_RECONSTRUCTION",),
    "Architecture":(
        "ARCHITECTURE_CONTRACT_RELATIVE_ANALYSIS",
        "ARCHITECTURE_PROTECTED_PROSE_CONSTRAINT_BINDING",
        "ARCHITECTURE_UNIT_JOB_PURITY_GATE",
    ),
    "PD":("PD_MINIMAL_RESULT_SENSITIVITY",),
    "PDAudit":(
        "PDAUDIT_FRAME_FIBER_SENSITIVITY",
        "PDAUDIT_RAW_NORMALIZATION_SEPARATION",
    ),
    "HF001":("HF001_GOVERNED_EPISODE",),
    "HF002":(
        "HF002_LOCAL_RECURSIVE_CONTINUATION",
        "HF002_CLEAN_SUCCESSOR_FIXED_POINT",
    ),
    "RootCause":(
        "ROOT_CAUSE_ROOTNESS_SELECTOR",
        "ROOT_CAUSE_HF002_LOCAL_RECURRENCE",
        "ROOT_CAUSE_IMPROVEMENTCORE_PARENT_HANDOFF",
    ),
    "GDOS":(
        "GDOS_FROZEN_INDEPENDENT_OBSERVATION",
    ),
    "Discriminator":(
        "DISCRIMINATOR_PRESERVE_PLURAL_OPEN",
    ),
    "RTC":(
        "RTC_STRICT_GAIN_PRESERVATION_GATE",
    ),
    "BiasPerturbation":(
        "BIAS_PERTURBATION_INVARIANCE_GUARD",
    ),
    "Diagnosis":(
        "DIAGNOSIS_MECHANISM_BEFORE_REPAIR",
    ),
    "SolutionToMyProblem":(
        "SOLUTION_PROTECTED_PROSE_PRESERVATION",
    ),
    "Prose":(
        "PROSE_PROTECTED_CONTRACT_ACCEPTANCE",
        "PROSE_AFFIRMATIVE_FIRST_GATE",
        "PROSE_FIRST_MENTION_PERSON_DATES",
        "PROSE_NUMERIC_YEAR_DATING_GATE",
        "PROSE_ORDERED_ANCHOR_GATE",
        "PROSE_SEMANTIC_STRENGTH_NO_INFLATION_RECEIPTS",
        "PROSE_READER_LOAD_GATE",
        "PROSE_PLAIN_LANGUAGE_GATE",
        "PROSE_QUESTION_TERMINATION_GATE",
        "PROSE_JEWISH_LEXICAL_FORM_GATE",
        "PROSE_RESPONSE_SELECTION_AFFIRMATIVE_FIRST_GATE",
        "PROSE_FINAL_RESPONSE_AFFIRMATIVE_FIRST_GATE",
    ),
    "ASSERT":(
        "ASSERT_COMPOUND_STAGE_ORDER",
        "ASSERT_SECOND_COMPARE_REQUIRED",
        "ASSERT_DISCOVERY_WORLD_FIXED_POINT_REENTRY",
        "ASSERT_FULL36_THREE_SURFACE_COVERAGE",
    ),
    "GOAL":(
        "GOAL_EVIDENCE_GROUNDED_ADMISSION",
        "GOAL_CONSTRAINT_SEPARATION",
        "GOAL_OBJECT_X_T_I_SIGMA",
        "GOAL_PLURALITY_FAIL_OPEN",
        "GOAL_ROBUST_MT_PREREQUISITE",
        "GOAL_FULL_TOOL_IDENTITY",
    ),
    "RecursiveCompiler":(
        "RECURSIVE_COMPILER_CURRENT_FULL_36_ONLY",
        "RECURSIVE_COMPILER_OBSERVER_FOCUSED_OBSERVER",
        "RECURSIVE_COMPILER_ADAPTIVE_HIERARCHY",
        "RECURSIVE_COMPILER_BOTTOM_UP_RECONCILIATION",
        "RECURSIVE_COMPILER_HF2_BOUNDARY_RECURRENCE",
        "RECURSIVE_COMPILER_NO_36_PROFILE_DOWNGRADE",
        "RECURSIVE_COMPILER_PROTECTED_HIERARCHY_CONSTRAINTS_REQUIRED",
        "RECURSIVE_COMPILER_FAIL_CLOSED_ON_CONSTRAINT_ORDER_CONFLICT",
        "RECURSIVE_COMPILER_GLOBAL_CLOSE_REQUIRES_ALL_LEVEL_GATES",
        "RECURSIVE_COMPILER_PROTECTED_DELTA_LINEAGE",
        "RECURSIVE_COMPILER_AFFECTED_CONE_INVALIDATION",
        "RECURSIVE_COMPILER_HF2_ZERO_NEW_DELTA_FIXED_POINT",
        "RECURSIVE_COMPILER_LOCAL_CLOSE_NOT_GLOBAL_CLOSE",
    ),
    "MultiObject":(
        "MO_FROZEN_OBJECT_IDENTITY",
        "MO_REQUIRED_PAIR_COVERAGE",
        "MO_PAIR_ROUTE_ISOLATION",
        "MO_INDEPENDENT_FULL_JOINT_ROUTE",
        "MO_LOWER_ORDER_SYNTHESIS",
        "MO_TYPED_RECONCILIATION",
        "MO_REDUCIBILITY_CHALLENGE",
        "MO_HIGHER_ORDER_RESIDUAL_TYPING",
        "MO_MATERIAL_DELTA_REENTRY",
        "MO_OPEN_CONFLICT_INCOMPARABILITY_PRESERVATION",
        "MO_GATED_VIEW_EXPANSION",
        "MO_CONFIGURED_ADEQUACY_BOUNDARY",
        "MO_FULL_TOOL_IDENTITY",
    ),
}

# Preserve the public name for existing consumers. Both names share one inventory.
PROTECTED_BEHAVIORS=REQUIRED_PROTECTED_BEHAVIORS


# III. Configured profile policy and construction.
STRONG_CHALLENGE_TOOLS=frozenset({
            "ImprovementCore","ProjectManager","ICC128","MT","MTA","Architecture","PD","PDAudit","GDOS","RootCause","RTC",
            "CurrentnessAudit","MultiObject","Diagnosis","ASSERT","GOAL","SolutionToMyProblem","Prose","DesiredJane",
            "QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline","RecursiveCompiler","ToolConductor"
        })


def _spec(tool):
    strong=tool in STRONG_CHALLENGE_TOOLS or tool in LEARNING_TOOLS
    layers=ASSERT_LAYERS if tool=="ASSERT" else (tool,)
    return ConfiguredRunSpec(
        tool_id=tool,
        recursive=True,
        closure_required=True,
        reentry_required=True,
        external_challenge="WHEN_STRONG_CLAIM" if strong else "NONE",
        required_layers=layers,
        manifest_id=tool,
        protected_behaviors=REQUIRED_PROTECTED_BEHAVIORS.get(tool,()),
        recurrence_engine=recurrence_engine_for(tool),
    )

def _build_configured_runs(tool_ids):
    ids=tuple(tool_ids)
    if len(ids)!=len(set(ids)):
        raise RuntimeError("TOOL_REGISTRY_DUPLICATE_ID")
    return {t:_spec(t) for t in ids}


CONFIGURED_RUNS=_build_configured_runs(MATERIAL_TOOLS)


def registered_spec(tool_id):
    """Return the authoritative configured specification, or None."""
    return CONFIGURED_RUNS.get(tool_id) if isinstance(tool_id,str) else None


def matches_registered_spec(spec):
    """A structural or experimental specification is not execution authority."""
    if type(spec) is not ConfiguredRunSpec:
        return False
    canonical=registered_spec(spec.tool_id)
    return canonical is not None and spec==canonical and all(
        type(value) is type(vars(canonical)[name]) for name,value in vars(spec).items()
    )
