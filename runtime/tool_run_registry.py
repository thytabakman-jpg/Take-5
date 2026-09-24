"""Configured-run registry for foundation capabilities."""
from configured_run import ConfiguredRunSpec

MATERIAL_TOOLS=tuple([f"C{i:02d}" for i in range(1,50)]+[
"ImprovementCore","MTA","Architecture","PD","PDAudit","GDOS","Discriminator","Reconciler",
"DelegatedExecutor","HF001","TRC","RTC","BiasPerturbation","CurrentnessAudit",
"CapabilityFoundry","EmergentAdmission","HistoricalReconstruction","ZeroRequest","MultiObject","Diagnosis"
])

def _spec(tool):
    strong=tool in {"ImprovementCore","MTA","Architecture","PD","PDAudit","GDOS","RTC","CurrentnessAudit","MultiObject","Diagnosis"}
    return ConfiguredRunSpec(tool,True,True,True,"WHEN_STRONG_CLAIM" if strong else "NONE")

CONFIGURED_RUNS={t:_spec(t) for t in MATERIAL_TOOLS}
