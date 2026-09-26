"""Heterogeneous holdout encodings for the typed effectful function IR.

These are structural preservation fixtures, not claims that every semantic
coordinate of the named tools is already closed.  They deliberately prohibit
hiding a whole target tool behind one ATOM node.
"""
from __future__ import annotations

from tool_run_registry import MATERIAL_TOOLS
from typed_effect_ir import (
    EffectSignature,
    ProgramContract,
    atom,
    choice,
    loop,
    product,
    seq,
    transform,
    validate,
)

E_OPEN = EffectSignature.of("OPEN", "BLOCKED", "CONFLICT")
E_EVIDENCE = EffectSignature.of("EVIDENCE", "PROVENANCE")
E_EXEC = EffectSignature.of("EXECUTION_TRUTH", "CURRENTNESS")
E_DISCOVERY = EffectSignature.of("DISCOVERY", "REENTRY")
E_AUTH = EffectSignature.of("AUTHORITY")
E_PERSIST = EffectSignature.of("PERSISTENCE")


def _configured(
    name: str,
    native,
    *,
    directed_scope: bool = False,
    hf2: bool = True,
):
    node = native
    if directed_scope:
        node = transform("DirectedScopeLift", node)
    node = transform("FTW", node, effects=E_EXEC.join(E_AUTH))
    node = transform("DCC", node, effects=E_DISCOVERY)
    node = transform("TRC", node, effects=E_PERSIST)
    node = transform("HF1", node, effects=E_DISCOVERY)
    if hf2:
        node = transform("HF2", node, effects=E_DISCOVERY)
    return transform(f"Configured:{name}", node)


def pd_program():
    native = seq(
        "PDNativePipeline",
        atom("FreezeTarget", effects=E_EVIDENCE),
        atom("DifferentiateFrame", effects=E_DISCOVERY),
        atom("ResultSensitivity", effects=E_DISCOVERY),
        atom("PreserveOpen", effects=E_OPEN),
    )
    return _configured("PD", native)


def pdaudit_program():
    native = seq(
        "PDAuditNativePipeline",
        atom("FreezeTarget", effects=E_EVIDENCE),
        atom("ImmutableRawBaseline", effects=E_EVIDENCE),
        atom("NormalizeSeparately", effects=E_EVIDENCE),
        atom("InteractionYield", effects=E_DISCOVERY),
        atom("ZeroYieldAccounting", effects=E_EVIDENCE),
        atom("PreserveOpen", effects=E_OPEN),
    )
    return _configured("PDAudit", native)


def mt_program():
    native = seq(
        "MTNativePipeline",
        atom("WholeObjectObserve", effects=E_DISCOVERY),
        atom("LocalQuestionGenerate", effects=E_DISCOVERY),
        atom("CrossObjectRelationSearch", effects=E_DISCOVERY),
        atom("ReobserveOnMaterialChange", effects=E_DISCOVERY),
        atom("PreserveNegativeMemory", effects=E_EVIDENCE),
    )
    return _configured("MT", native, directed_scope=True)


def architect_program():
    native = seq(
        "ArchitectNativePipeline",
        atom("FreezeArchitectureContract", effects=E_EVIDENCE),
        atom("ViolationLocalization", effects=E_DISCOVERY),
        atom("DependencyRecovery", effects=E_DISCOVERY),
        atom("InteractionChallenge", effects=E_DISCOVERY),
        atom("SuccessorFrontier", effects=E_OPEN.join(E_AUTH)),
    )
    return _configured("Architect", native, directed_scope=True)


def icc123_program():
    native = seq(
        "ICC123NativePipeline",
        atom("FreezeRepresentation", effects=E_EVIDENCE),
        atom("GenerateResidualCandidates", effects=E_DISCOVERY),
        atom("ClassifySeparatorOrOmission", effects=E_DISCOVERY),
        atom("ResidualPacket", effects=E_OPEN.join(E_EVIDENCE)),
    )
    return _configured("ICC123", native)


def icc128_program():
    body = seq(
        "ICC128ControllerBody",
        atom("GenerateQuestionsAndWork", effects=E_DISCOVERY),
        atom("SelectAdmissiblePackage", effects=E_AUTH),
        atom("ExecuteSelectedPackage", effects=E_EXEC),
        atom("AdmitAndUpdateState", effects=E_DISCOVERY.join(E_PERSIST)),
        atom("VerifyClosureBoundary", effects=E_OPEN.join(E_EVIDENCE)),
    )
    return loop("ICC128ManagerRecurrence", body)


def improvement_core_program():
    ordinary = seq(
        "ImprovementCoreOrdinaryPath",
        atom("ObserveFreeze", effects=E_EVIDENCE),
        atom("CoDiscoverJobWorkCapability", effects=E_DISCOVERY),
        atom("SelectNondominatedPackage", effects=E_AUTH),
        atom("ExecuteAndAdmit", effects=E_EXEC.join(E_PERSIST)),
        atom("UpdateControllerState", effects=E_DISCOVERY),
    )
    zero_request = seq(
        "ImprovementCoreZeroRequestPath",
        atom("ObserveCorpusWithoutInventedGoal", effects=E_DISCOVERY),
        atom("CandidateJobDiscovery", effects=E_DISCOVERY),
        atom("AuthorityGate", effects=E_AUTH.join(E_OPEN)),
        atom("UpdateControllerState", effects=E_DISCOVERY),
    )
    routed = choice("ImprovementCoreEntryMode", ordinary, zero_request)
    closed = transform("DCC", routed, effects=E_DISCOVERY)
    closed = transform("TRC", closed, effects=E_PERSIST)
    closed = transform("HF1", closed, effects=E_DISCOVERY)
    return loop("ImprovementCoreManagerRecurrence", closed)


def tool_conductor_program():
    children = tuple(
        atom(
            f"ToolRef:{tool_id}",
            input_type="ConductorInput",
            output_type="ToolDisposition",
            effects=E_OPEN.join(E_EXEC),
        )
        for tool_id in MATERIAL_TOOLS
    )
    product_node = product(
        "ExhaustiveRepertoireProduct",
        *children,
        output_type="ConductorLedger",
    )
    return transform(
        "CompilationWitnessAccounting",
        product_node,
        effects=E_EVIDENCE.join(E_EXEC),
    )


PROGRAMS = {
    "PD": pd_program,
    "PDAudit": pdaudit_program,
    "MT": mt_program,
    "Architect": architect_program,
    "ICC123": icc123_program,
    "ICC128": icc128_program,
    "ImprovementCore": improvement_core_program,
    "ToolConductor": tool_conductor_program,
}


CONTRACTS = {
    "PD": ProgramContract(
        "PD",
        required_atoms=("FreezeTarget", "ResultSensitivity", "PreserveOpen"),
        required_transforms=("FTW", "DCC", "TRC", "HF1", "HF2"),
        forbidden_atomic_names=("PD",),
    ),
    "PDAudit": ProgramContract(
        "PDAudit",
        required_atoms=("ImmutableRawBaseline", "NormalizeSeparately", "ZeroYieldAccounting"),
        required_transforms=("FTW", "DCC", "TRC", "HF1", "HF2"),
        forbidden_atomic_names=("PDAudit",),
    ),
    "MT": ProgramContract(
        "MT",
        required_atoms=("WholeObjectObserve", "LocalQuestionGenerate", "ReobserveOnMaterialChange"),
        required_transforms=("DirectedScopeLift", "FTW", "DCC", "TRC", "HF1", "HF2"),
        forbidden_atomic_names=("MT",),
    ),
    "Architect": ProgramContract(
        "Architect",
        required_atoms=("FreezeArchitectureContract", "DependencyRecovery", "SuccessorFrontier"),
        required_transforms=("DirectedScopeLift", "FTW", "DCC", "TRC", "HF1", "HF2"),
        forbidden_atomic_names=("Architect", "ARCHITECTURE-ANALYSIS"),
    ),
    "ICC123": ProgramContract(
        "ICC123",
        required_atoms=("GenerateResidualCandidates", "ResidualPacket"),
        required_transforms=("FTW", "DCC", "TRC", "HF1", "HF2"),
        forbidden_atomic_names=("ICC123", "ICC-123"),
    ),
    "ICC128": ProgramContract(
        "ICC128",
        required_atoms=("GenerateQuestionsAndWork", "SelectAdmissiblePackage", "AdmitAndUpdateState"),
        forbidden_atomic_names=("ICC128", "ICC-128"),
    ),
    "ImprovementCore": ProgramContract(
        "ImprovementCore",
        required_atoms=("CoDiscoverJobWorkCapability", "SelectNondominatedPackage", "UpdateControllerState"),
        required_transforms=("DCC", "TRC", "HF1"),
        forbidden_atomic_names=("ImprovementCore",),
    ),
    "ToolConductor": ProgramContract(
        "ToolConductor",
        required_atoms=tuple(f"ToolRef:{tool_id}" for tool_id in MATERIAL_TOOLS),
        required_transforms=("CompilationWitnessAccounting",),
        forbidden_atomic_names=("ToolConductor",),
    ),
}


def validate_holdouts():
    return {
        name: validate(builder(), CONTRACTS[name])
        for name, builder in PROGRAMS.items()
    }
