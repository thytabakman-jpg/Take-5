"""Heterogeneous holdout encodings for typed_effect_ir."""
from tool_run_registry import MATERIAL_TOOLS
from typed_effect_ir import EffectSignature,ProgramContract,atom,branch,loop,product,seq,transform,validate

E_OPEN=EffectSignature.of("OPEN","BLOCKED","CONFLICT")
E_EVIDENCE=EffectSignature.of("EVIDENCE","PROVENANCE")
E_EXEC=EffectSignature.of("EXECUTION_TRUTH","CURRENTNESS")
E_DISCOVERY=EffectSignature.of("DISCOVERY","REENTRY")
E_AUTH=EffectSignature.of("AUTHORITY")
E_PERSIST=EffectSignature.of("PERSISTENCE")

def _configured(name,native,directed_scope=False,hf2=True):
    node=native
    if directed_scope: node=transform("DirectedScopeLift",node)
    node=transform("FTW",node,effects=E_EXEC.join(E_AUTH))
    node=transform("DCC",node,effects=E_DISCOVERY)
    node=transform("TRC",node,effects=E_PERSIST)
    node=transform("HF1",node,effects=E_DISCOVERY)
    if hf2: node=transform("HF2",node,effects=E_DISCOVERY)
    return transform(f"Configured:{name}",node)

def pd_program():
    return _configured("PD",seq("PDNativePipeline",
        atom("FreezeTarget",effects=E_EVIDENCE),
        atom("DifferentiateFrame",effects=E_DISCOVERY),
        atom("ResultSensitivity",effects=E_DISCOVERY),
        atom("PreserveOpen",effects=E_OPEN)))

def pdaudit_program():
    return _configured("PDAudit",seq("PDAuditNativePipeline",
        atom("FreezeTarget",effects=E_EVIDENCE),
        atom("ImmutableRawBaseline",effects=E_EVIDENCE),
        atom("NormalizeSeparately",effects=E_EVIDENCE),
        atom("InteractionYield",effects=E_DISCOVERY),
        atom("ZeroYieldAccounting",effects=E_EVIDENCE),
        atom("PreserveOpen",effects=E_OPEN)))

def mt_program():
    return _configured("MT",seq("MTNativePipeline",
        atom("WholeObjectObserve",effects=E_DISCOVERY),
        atom("LocalQuestionGenerate",effects=E_DISCOVERY),
        atom("CrossObjectRelationSearch",effects=E_DISCOVERY),
        atom("ReobserveOnMaterialChange",effects=E_DISCOVERY),
        atom("PreserveNegativeMemory",effects=E_EVIDENCE)),directed_scope=True)

def architect_program():
    return _configured("Architect",seq("ArchitectNativePipeline",
        atom("FreezeArchitectureContract",effects=E_EVIDENCE),
        atom("ViolationLocalization",effects=E_DISCOVERY),
        atom("DependencyRecovery",effects=E_DISCOVERY),
        atom("InteractionChallenge",effects=E_DISCOVERY),
        atom("SuccessorFrontier",effects=E_OPEN.join(E_AUTH))),directed_scope=True)

def icc123_program():
    return _configured("ICC123",seq("ICC123NativePipeline",
        atom("FreezeRepresentation",effects=E_EVIDENCE),
        atom("GenerateResidualCandidates",effects=E_DISCOVERY),
        atom("ClassifySeparatorOrOmission",effects=E_DISCOVERY),
        atom("ResidualPacket",effects=E_OPEN.join(E_EVIDENCE))))

def icc128_program():
    body=seq("ICC128ControllerBody",
        atom("GenerateQuestionsAndWork",effects=E_DISCOVERY),
        atom("SelectAdmissiblePackage",effects=E_AUTH),
        atom("ExecuteSelectedPackage",effects=E_EXEC),
        atom("AdmitAndUpdateState",effects=E_DISCOVERY.join(E_PERSIST)),
        atom("VerifyClosureBoundary",effects=E_OPEN.join(E_EVIDENCE)))
    guard=atom("ICC128ContinuationGuard",output_type="Bool",effects=E_OPEN.join(E_DISCOVERY))
    return loop("ICC128ManagerRecurrence",guard,body)

def improvement_core_program():
    ordinary=seq("ImprovementCoreOrdinaryPath",
        atom("ObserveFreeze",effects=E_EVIDENCE),
        atom("CoDiscoverJobWorkCapability",effects=E_DISCOVERY),
        atom("SelectNondominatedPackage",effects=E_AUTH),
        atom("ExecuteAndAdmit",effects=E_EXEC.join(E_PERSIST)),
        atom("UpdateControllerState",effects=E_DISCOVERY))
    zero=seq("ImprovementCoreZeroRequestPath",
        atom("ObserveCorpusWithoutInventedGoal",effects=E_DISCOVERY),
        atom("CandidateJobDiscovery",effects=E_DISCOVERY),
        atom("AuthorityGate",effects=E_AUTH.join(E_OPEN)),
        atom("UpdateControllerState",effects=E_DISCOVERY))
    selector=atom("ImprovementCoreEntryModeSelector",output_type="BranchKey",effects=E_OPEN)
    routed=branch("ImprovementCoreEntryMode",selector,ordinary,zero)
    routed=transform("DCC",routed,effects=E_DISCOVERY)
    routed=transform("TRC",routed,effects=E_PERSIST)
    routed=transform("HF1",routed,effects=E_DISCOVERY)
    guard=atom("ImprovementCoreContinuationGuard",output_type="Bool",effects=E_OPEN.join(E_DISCOVERY))
    return loop("ImprovementCoreManagerRecurrence",guard,routed)

def tool_conductor_program():
    children=tuple(atom(f"ToolRef:{t}",input_type="ConductorInput",output_type="ToolDisposition",
                        effects=E_OPEN.join(E_EXEC)) for t in MATERIAL_TOOLS)
    return transform("CompilationWitnessAccounting",
        product("ExhaustiveRepertoireProduct",*children,output_type="ConductorLedger"),
        effects=E_EVIDENCE.join(E_EXEC))

PROGRAMS={"PD":pd_program,"PDAudit":pdaudit_program,"MT":mt_program,"Architect":architect_program,
          "ICC123":icc123_program,"ICC128":icc128_program,
          "ImprovementCore":improvement_core_program,"ToolConductor":tool_conductor_program}

CONTRACTS={
"PD":ProgramContract("PD",("FreezeTarget","ResultSensitivity","PreserveOpen"),("FTW","DCC","TRC","HF1","HF2"),("PD",)),
"PDAudit":ProgramContract("PDAudit",("ImmutableRawBaseline","NormalizeSeparately","ZeroYieldAccounting"),("FTW","DCC","TRC","HF1","HF2"),("PDAudit",)),
"MT":ProgramContract("MT",("WholeObjectObserve","LocalQuestionGenerate","ReobserveOnMaterialChange"),("DirectedScopeLift","FTW","DCC","TRC","HF1","HF2"),("MT",)),
"Architect":ProgramContract("Architect",("FreezeArchitectureContract","DependencyRecovery","SuccessorFrontier"),("DirectedScopeLift","FTW","DCC","TRC","HF1","HF2"),("Architect","ARCHITECTURE-ANALYSIS")),
"ICC123":ProgramContract("ICC123",("GenerateResidualCandidates","ResidualPacket"),("FTW","DCC","TRC","HF1","HF2"),("ICC123","ICC-123")),
"ICC128":ProgramContract("ICC128",("GenerateQuestionsAndWork","SelectAdmissiblePackage","AdmitAndUpdateState","ICC128ContinuationGuard"),(),("ICC128","ICC-128")),
"ImprovementCore":ProgramContract("ImprovementCore",("CoDiscoverJobWorkCapability","SelectNondominatedPackage","UpdateControllerState","ImprovementCoreEntryModeSelector","ImprovementCoreContinuationGuard"),("DCC","TRC","HF1"),("ImprovementCore",)),
"ToolConductor":ProgramContract("ToolConductor",tuple(f"ToolRef:{t}" for t in MATERIAL_TOOLS),("CompilationWitnessAccounting",),("ToolConductor",)),
}

def validate_holdouts():
    return {name:validate(builder(),CONTRACTS[name]) for name,builder in PROGRAMS.items()}
