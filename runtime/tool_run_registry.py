"""Configured-run registry for foundation and admitted learning capabilities."""
from configured_run import ConfiguredRunSpec
from learning_tool_bridge import SPECS as LEARNING_SPECS

LEARNING_TOOLS=tuple(spec.program_id for spec in LEARNING_SPECS)

MATERIAL_TOOLS=tuple([f"C{i:02d}" for i in range(1,50)]+[
"ImprovementCore","MTA","Architecture","PD","PDAudit","GDOS","Discriminator","Reconciler",
"DelegatedExecutor","HF001","TRC","RTC","BiasPerturbation","CurrentnessAudit",
"CapabilityFoundry","EmergentAdmission","HistoricalReconstruction","ZeroRequest","MultiObject","Diagnosis",
"ASSERT","SolutionToMyProblem","DesiredJane","QuestionWorthAsking","LambdaMath"
]+list(LEARNING_TOOLS))

def _spec(tool):
    strong=(
        tool in {
            "ImprovementCore","MTA","Architecture","PD","PDAudit","GDOS","RTC",
            "CurrentnessAudit","MultiObject","Diagnosis","ASSERT","SolutionToMyProblem","DesiredJane",
            "QuestionWorthAsking","LambdaMath"
        }
        or tool in LEARNING_TOOLS
    )
    return ConfiguredRunSpec(
        tool,
        True,
        True,
        True,
        "WHEN_STRONG_CLAIM" if strong else "NONE",
    )

CONFIGURED_RUNS={t:_spec(t) for t in MATERIAL_TOOLS}
