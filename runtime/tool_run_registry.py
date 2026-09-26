"""Configured-run registry for foundation and admitted learning capabilities."""
from configured_run import ConfiguredRunSpec
from learning_tool_bridge import SPECS as LEARNING_SPECS

LEARNING_TOOLS=tuple(spec.program_id for spec in LEARNING_SPECS)

MATERIAL_TOOLS=tuple([f"C{i:02d}" for i in range(1,50)]+[
"ImprovementCore","MT","MTA","Architecture","PD","PDAudit","GDOS","Discriminator","Reconciler",
"DelegatedExecutor","HF001","TRC","RTC","BiasPerturbation","CurrentnessAudit",
"CapabilityFoundry","EmergentAdmission","HistoricalReconstruction","ZeroRequest","MultiObject","Diagnosis",
"ASSERT","GOAL","SolutionToMyProblem","DesiredJane","QuestionWorthAsking","LambdaMath","SemanticResolutionPipeline"
]+list(LEARNING_TOOLS))

ASSERT_LAYERS=("ASSERT_LAYER_1","ASSERT_LAYER_2")

def _spec(tool):
    strong=(
        tool in {
            "ImprovementCore","MT","MTA","Architecture","PD","PDAudit","GDOS","RTC",
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
    )

CONFIGURED_RUNS={t:_spec(t) for t in MATERIAL_TOOLS}
