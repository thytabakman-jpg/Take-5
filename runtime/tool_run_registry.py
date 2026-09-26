"""Configured-run registry for foundation and admitted learning capabilities."""
from configured_run import ConfiguredRunSpec
from learning_tool_bridge import SPECS as LEARNING_SPECS

LEARNING_TOOLS=tuple(spec.program_id for spec in LEARNING_SPECS)

MATERIAL_TOOLS=tuple([f"C{i:02d}" for i in range(1,50)]+[
"ImprovementCore","MT","MTA","Architecture","PD","PDAudit","GDOS","Discriminator","Reconciler",
"DelegatedExecutor","HF001","HF002","RootCause","TRC","RTC","BiasPerturbation","CurrentnessAudit",
"CapabilityFoundry","EmergentAdmission","HistoricalReconstruction","ZeroRequest","MultiObject","Diagnosis",
"ASSERT","GOAL","SolutionToMyProblem","DesiredJane","QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline"
]+list(LEARNING_TOOLS))

ASSERT_LAYERS=("ASSERT_LAYER_1","ASSERT_LAYER_2")

PROTECTED_BEHAVIORS={
    "MT":(
        "MT_BLACK_BOX_SEMANTIC_RETURN_GATE",
        "MT_W1_WHOLE_OBJECT_RECONNAISSANCE",
        "MT_W2_SELF_GENERATED_LOCAL_QUESTIONS",
        "MT_W3_RECONNAISSANCE_NONMUTATION",
        "MT_W4_REOBSERVE_AFTER_MATERIAL_CHANGE",
        "MT_W5_FULL_CONSEQUENCE_CLOSURE",
        "MT_W6_ROOT_OBJECT_PRESERVATION",
        "MT_W7_CROSS_OBJECT_CROSS_SCALE_DISCOVERY",
        "MT_W8_BEHAVIORAL_EQUIVALENCE_NOT_FINAL_ANSWER_ONLY",
    ),
    "HF001":("HF001_GOVERNED_EPISODE",),
    "HF002":("HF002_LOCAL_RECURSIVE_CONTINUATION",),
    "RootCause":(
        "ROOT_CAUSE_ROOTNESS_SELECTOR",
        "ROOT_CAUSE_HF002_LOCAL_RECURRENCE",
        "ROOT_CAUSE_IMPROVEMENTCORE_PARENT_HANDOFF",
    ),
    "ASSERT":(
        "ASSERT_COMPOUND_STAGE_ORDER",
        "ASSERT_SECOND_COMPARE_REQUIRED",
        "ASSERT_DISCOVERY_WORLD_FIXED_POINT_REENTRY",
        "ASSERT_FULL36_THREE_SURFACE_COVERAGE",
    ),
}

def _spec(tool):
    strong=(
        tool in {
            "ImprovementCore","MT","MTA","Architecture","PD","PDAudit","GDOS","RootCause","RTC",
            "CurrentnessAudit","MultiObject","Diagnosis","ASSERT","GOAL","SolutionToMyProblem","DesiredJane",
            "QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline"
        }
        or tool in LEARNING_TOOLS
    )
    layers=ASSERT_LAYERS if tool=="ASSERT" else (tool,)
    return ConfiguredRunSpec(
        tool_id=tool,
        recursive=True,
        closure_required=True,
        reentry_required=True,
        external_challenge="WHEN_STRONG_CLAIM" if strong else "NONE",
        required_layers=layers,
        manifest_id=tool,
        protected_behaviors=PROTECTED_BEHAVIORS.get(tool,()),
    )

CONFIGURED_RUNS={t:_spec(t) for t in MATERIAL_TOOLS}
