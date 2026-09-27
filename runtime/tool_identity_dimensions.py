"""Operational identity dimensions for every current configured tool.

FullMath already owns native semantics, wrapper, geometry, protected behavior and
lineage/currentness.  This module adds the dimensions that were repeatedly used
in design conversations but were not enforced as first-class current inventory:
question, job, responsibility and mathematical-object species.

The registry is exhaustive over the current finite MATERIAL_TOOLS repertoire.
C01-C49 project their already-authoritative ProgramSpec jobs/outputs.  Learning
tools project their already-authoritative typed obligations.  Named tools have
explicit nuclei below.  No entry may be absent or silently synthesized from the
tool name alone.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from a5_programs import REGISTRY as A5_REGISTRY
from learning_tool_bridge import SPEC_BY_ID as LEARNING_BY_ID
from tool_manifest import GENERIC_BINDINGS, manifest_for
from tool_run_registry import CONFIGURED_RUNS, MATERIAL_TOOLS


@dataclass(frozen=True)
class ToolOperationalIdentity:
    tool_id:str
    question:str
    job:str
    responsibility:str
    mathematical_object:str
    source_kind:str

    def complete(self)->bool:
        return all((
            self.tool_id.strip(),
            self.question.strip(),
            self.job.strip(),
            self.responsibility.strip(),
            self.mathematical_object.strip(),
            self.source_kind.strip(),
        ))


# Explicit named-tool nuclei.  These are operational projections of current
# canonical semantics, not replacements for FullMath/native runtime authority.
NAMED={
    "ImprovementCore":(
        "What materially remains to solve the governing job, and what admissible work changes that state?",
        "Adaptively generate/select work, execute governed capabilities, admit evidence, replan and control parent terminality.",
        "Own global work selection, admission, replanning and whole-job continuation; never manufacture semantic evidence or authority.",
        "ADAPTIVE_CONTROLLER",
    ),
    "ProjectManager":(
        "What is the current project state, goal gap and next legal bounded project transition?",
        "Maintain authority-bound project-control state and route project-local change.",
        "Own project organization, authority routing, impact/reentry and project-state transitions; not domain truth.",
        "AUTHORITY_GOVERNED_NONDETERMINISTIC_PROJECT_TRANSITION_SYSTEM",
    ),
    "ICC128":(
        "Given the current epistemic state, what questions/work are live and which nondominated package continues the controller?",
        "Generate questions/work, select packages, execute/admit/update and reselect after material delta.",
        "Own endogenous controller continuation and selection; not independent mutation authority.",
        "STATE_RELATIVE_ENDOGENOUS_CONTROLLER",
    ),
    "MT":(
        "Which representation, model or result-sensitive distinction changes the protected answer or reachable work?",
        "Attack/reconstruct representations and expose material black boxes or model distinctions.",
        "Own representation-sensitive analysis and its evidence; not final global completion.",
        "REPRESENTATION_RESULT_SENSITIVITY_OPERATOR",
    ),
    "MTA":(
        "What structural model of the target best preserves the protected behavior and exposes live residuals?",
        "Generate structural hypotheses, select an analysis package and reconstruct a protected model.",
        "Own structural-model reconstruction evidence; not authority to transform the target.",
        "STRUCTURAL_MODEL_RECONSTRUCTION_OPERATOR",
    ),
    "Architecture":(
        "What architecture, interfaces and dependencies realize the protected contract, and where are the structural defects?",
        "Analyze architecture relative to a frozen contract and produce admissible successor frontiers.",
        "Own architecture analysis and candidate successor evidence; not automatic implementation authority.",
        "CONTRACT_RELATIVE_ARCHITECTURE_ANALYZER",
    ),
    "PD":(
        "Which coordinates are minimally result-sensitive under the current representation?",
        "Compute quotient result classes, fibers and minimal result-sensitive coordinate sets.",
        "Own distinction/frame analysis; preserve plurality and OPEN rather than inventing selectors.",
        "RESULT_SENSITIVITY_QUOTIENT_OPERATOR",
    ),
    "PDAudit":(
        "Does the proposed PD/frame preserve raw distinctions and correctly identify sensitivity under the frozen basis?",
        "Audit PD fibers/sensitivity with raw-normalized separation.",
        "Own verification of the PD analysis; not the source of target semantics.",
        "FIXED_FRAME_FIBER_SENSITIVITY_AUDITOR",
    ),
    "GDOS":(
        "What do independent goal-decoupled observers find from the same frozen state?",
        "Run independent observation, reconcile outputs and preserve observer isolation.",
        "Own independent observation evidence; no sibling contamination or target mutation within a round.",
        "INDEPENDENT_OBSERVATION_SWEEP",
    ),
    "Discriminator":(
        "Which candidate interpretation/result survives the available discriminating evidence?",
        "Discriminate among candidate predicates/results while preserving plural OPEN outcomes.",
        "Own discrimination evidence; never force uniqueness when evidence leaves plurality.",
        "PREDICATE_DISCRIMINATOR",
    ),
    "Reconciler":(
        "How can admitted results coexist in one coherent state without erasing conflicts, revisions or OPEN alternatives?",
        "Reconcile admitted results into a coherent joint state.",
        "Own reconciliation bookkeeping and typed conflicts; not source authority for child claims.",
        "STATE_RECONCILIATION_OPERATOR",
    ),
    "DelegatedExecutor":(
        "Can this bounded work be delegated with exact authority, inputs, outputs and reintegration evidence?",
        "Execute bounded delegated work and return an authority-preserving receipt.",
        "Own delegation integrity and reintegration receipts; never expand authority.",
        "BOUNDED_DELEGATION_OPERATOR",
    ),
    "HF001":(
        "After verified work and fresh re-observation, has the governing continuation basis changed, and where must execution reenter?",
        "Regenerate/consume continuation state, classify material deltas and route earliest valid reentry until basis-relative closure.",
        "Own episode-level continuation invalidation, fresh-closure challenge and reentry routing; not same-capability local recurrence or global work selection.",
        "GOVERNED_REENTRY_AND_CLOSURE_CLASSIFIER",
    ),
    "HF002":(
        "After this capability changed its local normalized state, does the same capability have live material local work?",
        "Reapply the same configured capability while material local delta, local liveness and upstream stability hold.",
        "Own capability-local recurrence only; not global tool selection, fresh whole-job discovery or parent terminality.",
        "CAPABILITY_LOCAL_RECURSIVE_CONTINUATION_OPERATOR",
    ),
    "RootCause":(
        "What supported causal mechanism is the earliest actionable root of the observed failure?",
        "Select and verify root causes, then hand unresolved/global work back to ImprovementCore.",
        "Own rootness analysis and local recurrence; not global episode completion.",
        "ROOT_CAUSE_SELECTOR",
    ),
    "TRC":(
        "Have all material consequences of this tool run been harvested, realized, verified and consumed?",
        "Close material run consequences and preserve typed OPEN/BLOCKED residue.",
        "Own tool-run consequence closure; not upstream discovery or reentry selection.",
        "TOOL_RUN_CONSEQUENCE_CLOSURE_OPERATOR",
    ),
    "RTC":(
        "Is there a strictly better preserving successor or only typed no-gain evidence?",
        "Raise the ceiling by testing strict-gain preserving alternatives.",
        "Own strict-gain/no-gain challenge evidence; not unrestricted replacement authority.",
        "STRICT_GAIN_CEILING_OPERATOR",
    ),
    "BiasPerturbation":(
        "Does the protected result remain invariant under admitted nuisance/bias perturbations?",
        "Perturb nuisance dimensions and test invariance.",
        "Own perturbation-invariance evidence; not semantic target redefinition.",
        "NUISANCE_PERTURBATION_AUDITOR",
    ),
    "CurrentnessAudit":(
        "Does the built/current object still match the latest admitted authoritative basis?",
        "Compare built and latest admitted basis and disposition KEEP/PATCH/REPLACE/OPEN.",
        "Own currentness comparison; recency alone never grants authority.",
        "CURRENTNESS_COMPARATOR",
    ),
    "CapabilityFoundry":(
        "What typed new capability candidate would cover a live uncovered role without duplicating existing semantics?",
        "Generate typed capability candidates.",
        "Own candidate generation only; no self-admission, self-authorization or automatic registration.",
        "CAPABILITY_CANDIDATE_GENERATOR",
    ),
    "EmergentAdmission":(
        "Does a proposed load-bearing object satisfy identity, evidence, execution and authority requirements for admission?",
        "Gate admission of emergent formal objects/capabilities.",
        "Own admission disposition; missing evidence remains OPEN.",
        "EMERGENT_OBJECT_ADMISSION_GATE",
    ),
    "HistoricalReconstruction":(
        "Which predecessor/current object preserves the frozen job and protected result under lineage evidence?",
        "Reconstruct historical/current identity and compare protected behavior with execution witnesses.",
        "Own historical reconstruction evidence; history does not self-promote into current authority.",
        "HISTORICAL_IDENTITY_RECONSTRUCTION_OPERATOR",
    ),
    "ZeroRequest":(
        "What task-relevant structure exists in the addressable corpus before a substantive job is supplied?",
        "Run governed observation-only discovery without manufacturing a user goal.",
        "Own zero-request observation and candidate evidence; no invented substantive job.",
        "ZERO_REQUEST_OBSERVATION_EPISODE",
    ),
    "MultiObject":(
        "What result-sensitive relations or interactions appear only when the relevant objects are analyzed together?",
        "Analyze frozen object sets through pair/joint/higher-order relation routes and reconcile results.",
        "Own multi-object relation discovery; preserve irreducible/open/incomparable results.",
        "MULTI_OBJECT_RELATION_OPERATOR",
    ),
    "Diagnosis":(
        "What mechanism explains the observed failure before any repair is selected?",
        "Diagnose failure mechanisms and preserve unresolved causes.",
        "Own mechanism diagnosis; repair selection is downstream.",
        "FAILURE_MECHANISM_DIAGNOSTIC",
    ),
    "ASSERT":(
        "What propositions, conflicts, omissions and live questions are licensed by the accessible evidence after recursive comparison and inquiry?",
        "Run ASSERT→COMPARE→RESOLVE→HERE→COMPARE→INQUIRE→REASSERT to a discovery/world fixed point.",
        "Own compound assertion/discovery state; preserve UNKNOWN/OPEN/BLOCKED/CONFLICT.",
        "COMPOUND_DISCOVERY_FIXED_POINT_ENGINE",
    ),
    "GOAL":(
        "What single governing goal, if any, is grounded, authority-typed and determinate enough for the protected job?",
        "Recover the governing goal G=<X,T,I,Sigma> from admissible candidates/evidence.",
        "Own goal recovery; never invent arbitrary prose goals or mutate the target.",
        "GOVERNING_GOAL_RECOVERY_OPERATOR",
    ),
    "SolutionToMyProblem":(
        "Which candidate solution has the required execution, effect, preservation, verification and closure evidence?",
        "Construct and disposition a candidate solution frontier.",
        "Own solution-candidate evidence and disposition; not automatic implementation.",
        "SOLUTION_FRONTIER_OPERATOR",
    ),
    "DesiredJane":(
        "What Jane coordinates are required, prohibited, OPEN or conflicting under the evidence?",
        "Reconstruct desired Jane state from evidence polarity.",
        "Own desired-state reconstruction; preserve conflict and uncertainty.",
        "EVIDENCE_POLARITY_DESIRED_STATE_RECONSTRUCTOR",
    ),
    "QuestionWorthAsking":(
        "Which live question is nondominated by result sensitivity, information gain, unlock, actionability and burden?",
        "Select a nondominated live question frontier.",
        "Own question selection evidence; it does not answer the question itself.",
        "NONDOMINATED_QUESTION_SELECTOR",
    ),
    "LambdaMath":(
        "Which entry-state equivalence class is licensed by the raw request/evidence before downstream goal-directed work?",
        "Reconstruct set-valued entry state, quotient continuation-equivalent candidates and expose result-sensitive ambiguity.",
        "Own entry-state reconstruction; cannot expand authority or use downstream convenience to force identity.",
        "SET_VALUED_ENTRY_STATE_RECONSTRUCTION_OPERATOR",
    ),
    "SemanticResolutionPipeline":(
        "What configured sequence can resolve this load-bearing black box while preserving typed residuals?",
        "Plan mandatory and conditional semantic-resolution stages for black-box objects.",
        "Own resolution planning and residual routing; no substitution for missing native stages.",
        "BLACK_BOX_RESOLUTION_PIPELINE",
    ),
    "ToolConductor":(
        "Has every registered factor received one fail-closed configured execution disposition under the current repertoire?",
        "Traverse the complete registered repertoire and collect one governed disposition per factor.",
        "Own exhaustive repertoire coverage receipts; reachability is not semantic execution truth.",
        "FINITE_REPERTOIRE_PRODUCT_CONDUCTOR",
    ),
}


def _registered_capability_identity(tool_id:str)->ToolOperationalIdentity:
    spec=A5_REGISTRY.get(tool_id)
    out=", ".join(spec.protected_outputs)
    return ToolOperationalIdentity(
        tool_id=tool_id,
        question=f"What is the {spec.job} disposition for the current protected job?",
        job=spec.job,
        responsibility=(
            f"Own {spec.job} analysis and protected output(s) {out}; "
            "preserve OPEN and do not assume authority beyond the registered capability."
        ),
        mathematical_object="REGISTERED_TYPED_CAPABILITY_OPERATOR",
        source_kind="A5_PROGRAM_SPEC",
    )


def _learning_identity(tool_id:str)->ToolOperationalIdentity:
    spec=LEARNING_BY_ID[tool_id]
    return ToolOperationalIdentity(
        tool_id=tool_id,
        question=f"What update does {spec.obligation} produce for its current typed input?",
        job=spec.obligation,
        responsibility=(
            f"Apply the typed learning operator {spec.input_type} -> {spec.output_type} "
            "only when its required inputs are available; do not treat the lens as globally applicable."
        ),
        mathematical_object="TYPED_LEARNING_OPERATOR",
        source_kind="LEARNING_TOOL_SPEC",
    )


def identity_for(tool_id:str)->ToolOperationalIdentity:
    tool_id=str(tool_id)
    if tool_id in NAMED:
        q,j,r,k=NAMED[tool_id]
        return ToolOperationalIdentity(tool_id,q,j,r,k,"EXPLICIT_NAMED_TOOL_NUCLEUS")
    if tool_id.startswith("C") and tool_id[1:].isdigit():
        return _registered_capability_identity(tool_id)
    if tool_id in LEARNING_BY_ID:
        return _learning_identity(tool_id)
    raise KeyError("TOOL_OPERATIONAL_IDENTITY_UNRECOVERED:"+tool_id)


MASTER_DIMENSION_NAMES=(
    # operational nucleus recovered from prior tool-anatomy work
    "identity","question","job","responsibility","goal","mathematical_object",
    # native/configured semantics
    "native_semantics","inputs","outputs","state",
    "configured_identity","envelope","mode","orchestration","wrapper","geometry",
    # authority/currentness/lifecycle
    "authority","currentness_provenance","lineage","lifecycle",
    "persistence_propagation",
    # realization and reachability
    "runtime_realization","runtime_behavior","executability",
    "controller_reachability","invocation","run_instance","host_capability",
    # placement/relations/stewardship
    "dependencies_transfers","semantic_roles","project_memberships",
    "physical_location","backlog_open_obligations",
    # protection and stopping
    "protected_behavior","closure","reentry","recurrence","verification",
    "evidence_receipts","failure_open_policy","admission_promotion",
    # configured discovery surfaces; these are NOT identity-equivalent to the
    # separate SourceScope x TargetScope 36-cell handoff surface.
    "coverage_surface","question_projection","cognitive_projection",
)

# Backward-compatible name used by the first repair tests.
FULL_DIMENSION_NAMES=MASTER_DIMENSION_NAMES


def _slug(value:str)->str:
    out=[]
    for ch in str(value).lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join(filter(None,"".join(out).split("-")))


ROOT=Path(__file__).resolve().parents[1]
_GENERIC_BEHAVIOR_IDS=frozenset(x.behavior_id for x in GENERIC_BINDINGS)


def _typed_io(tool_id:str,op:ToolOperationalIdentity,native_owner:str):
    if tool_id.startswith("C") and tool_id[1:].isdigit():
        spec=A5_REGISTRY.get(tool_id)
        return (
            "REGISTERED_CAPABILITY_PAYLOAD:"+",".join(spec.roles),
            "PROTECTED_OUTPUT:"+",".join(spec.protected_outputs),
            "PACKET_STATE_DEFINED_BY_CAPABILITY_RUNTIME",
        )
    if tool_id in LEARNING_BY_ID:
        spec=LEARNING_BY_ID[tool_id]
        return (
            spec.input_type,
            spec.output_type,
            "TYPED_LEARNING_STEP_STATE",
        )
    route=f"CANONICAL_NATIVE_CONTRACT@{native_owner}"
    return (
        "INPUT_"+route,
        "OUTPUT_"+route,
        "STATE_"+route,
    )


def full_dimension_projection(tool_id:str)->dict[str,Any]:
    """Project the complete recovered tool-anatomy union without duplicating owners.

    A value may be explicit or an authority route.  ROUTED values are intentional:
    the anti-loss architecture keeps one mutable owner for native runtime details.
    Strong tool-reality separately verifies that the routed runtime is recovered.
    """
    op=identity_for(tool_id)
    manifest=manifest_for(tool_id)
    spec=CONFIGURED_RUNS[tool_id]
    runtime_refs=tuple(dict.fromkeys(
        b.implementation for b in manifest.bindings if b.implementation
    ))
    native_runtime_refs=tuple(dict.fromkeys(
        b.implementation for b in manifest.bindings
        if b.implementation and b.behavior_id not in _GENERIC_BEHAVIOR_IDS
    ))
    witness_refs=tuple(dict.fromkeys(
        b.witness for b in manifest.bindings if b.witness
    ))
    native_owner=(
        native_runtime_refs[0]
        if native_runtime_refs
        else manifest.lineage_contract
    )
    inputs,outputs,state=_typed_io(tool_id,op,native_owner)
    package_root=f"projects/tool-system/current-tools/{_slug(tool_id)}"
    goal=(
        f"Close the live {op.job} obligation for the protected job while "
        f"remaining inside this responsibility boundary: {op.responsibility}"
    )

    return {
        "identity":tool_id,
        "question":op.question,
        "job":op.job,
        "responsibility":op.responsibility,
        "goal":goal,
        "mathematical_object":op.mathematical_object,
        "native_semantics":manifest.native_semantics,
        "inputs":inputs,
        "outputs":outputs,
        "state":state,
        "configured_identity":{
            "registry":"runtime/tool_run_registry.py",
            "complete":spec.complete(),
            "manifest":"runtime/tool_manifest.py",
        },
        "envelope":"FULL_CONFIGURED_HF2_V1 PRE/INTRA/POST/CROSS envelope",
        "mode":"OBSERVER ordinary configured mode",
        "orchestration":"configured plan -> native execution -> TRC -> reentry",
        "wrapper":"FULL_CONFIGURED_HF2_V1",
        "geometry":manifest.geometry_policy,
        "authority":(
            "bounded by operational responsibility; mutation/admission authority "
            f"routes through {package_root}/AUTHORITY_REGISTRY.md"
        ),
        "currentness_provenance":(
            f"{manifest.lineage_contract} + integration/CURRENT_TOOL_REALITY.md"
        ),
        "lineage":manifest.lineage_contract,
        "lifecycle":f"{package_root}/CURRENT_STATE.md",
        "persistence_propagation":(
            f"{package_root}/evidence + runs + history; POST/CROSS bindings"
        ),
        "runtime_realization":{
            "all_implementation_refs":runtime_refs,
            "native_owner_refs":native_runtime_refs or (manifest.lineage_contract,),
        },
        "runtime_behavior":{
            "native_semantics":manifest.native_semantics,
            "implementation_refs":runtime_refs,
        },
        "executability":{
            "configured_complete":spec.complete(),
            "runtime_refs_present":bool(runtime_refs),
            "native_owner_present":bool(native_runtime_refs or manifest.lineage_contract),
        },
        "controller_reachability":(
            "runtime/global_tool_execution.py + runtime/direct_tool_command_gateway.py"
        ),
        "invocation":"FULL_CONFIGURED_HF2_V1 configured invocation",
        "run_instance":"per-run execution/receipt state; never identical to tool identity",
        "host_capability":(
            "Take-5 repository-owned routes only; unrelated external host interception "
            "remains an explicit boundary"
        ),
        "dependencies_transfers":tuple(
            dict.fromkeys(b.implementation for b in manifest.bindings)
        ),
        "semantic_roles":(
            f"question={op.question}",
            f"job={op.job}",
            f"responsibility={op.responsibility}",
        ),
        "project_memberships":("projects/tool-system",package_root),
        "physical_location":package_root,
        "backlog_open_obligations":f"{package_root}/OPEN_QUESTIONS.md",
        "protected_behavior":tuple(sorted(manifest.behavior_ids())),
        "closure":manifest.closure_contract,
        "reentry":manifest.reentry_contract,
        "recurrence":spec.recurrence_engine,
        "verification":witness_refs,
        "evidence_receipts":(
            f"{package_root}/runs + evidence; configured execution/PTI receipts"
        ),
        "failure_open_policy":"OPEN/BLOCKED/CONFLICT preserved; resource stop is not completion",
        "admission_promotion":(
            "registry/currentness/change-control governed; no tool self-promotes"
        ),
        "coverage_surface":"Scope x ModeFace = 6 x 6 = 36",
        "question_projection":"Q01-Q22 x 36 = 792",
        "cognitive_projection":"DIFFERENTIATE/RELATE/RECONSTRUCT/STRENGTHEN x 36 = 144",
    }


def audit_current_repertoire()->dict[str,Any]:
    missing=[]
    incomplete=[]
    projections={}
    for tool_id in MATERIAL_TOOLS:
        try:
            op=identity_for(tool_id)
            projection=full_dimension_projection(tool_id)
        except Exception as exc:
            missing.append((tool_id,type(exc).__name__,str(exc)))
            continue
        if not op.complete():
            incomplete.append((tool_id,"OPERATIONAL_IDENTITY"))
        empty=tuple(
            name for name in FULL_DIMENSION_NAMES
            if projection.get(name) in (None,"",(),{},[])
        )
        if empty:
            incomplete.append((tool_id,"EMPTY:"+",".join(empty)))

        manifest=manifest_for(tool_id)
        package_root=ROOT/"projects"/"tool-system"/"current-tools"/_slug(tool_id)
        required_paths=(
            ROOT/"runtime"/"tool_run_registry.py",
            ROOT/"runtime"/"tool_manifest.py",
            ROOT/manifest.lineage_contract,
            package_root/"AUTHORITY_REGISTRY.md",
            package_root/"CURRENT_STATE.md",
            package_root/"OPEN_QUESTIONS.md",
        )
        required_paths += tuple(ROOT/x for x in projection["runtime_realization"]["all_implementation_refs"])
        required_paths += tuple(ROOT/x for x in projection["verification"])
        absent=tuple(str(x.relative_to(ROOT)) for x in required_paths if not x.exists())
        if absent:
            incomplete.append((tool_id,"UNRESOLVED_ROUTE:"+",".join(absent)))
        projections[tool_id]=projection

    parity=set(projections)==set(MATERIAL_TOOLS)
    return {
        "status":"CLOSED_RELATIVE" if parity and not missing and not incomplete else "OPEN",
        "tool_count":len(MATERIAL_TOOLS),
        "projected_count":len(projections),
        "parity":parity,
        "missing":tuple(missing),
        "incomplete":tuple(incomplete),
        "dimension_names":FULL_DIMENSION_NAMES,
        "projections":projections,
    }


if __name__=="__main__":
    result=audit_current_repertoire()
    print({
        "status":result["status"],
        "tool_count":result["tool_count"],
        "projected_count":result["projected_count"],
        "parity":result["parity"],
        "missing":result["missing"],
        "incomplete":result["incomplete"],
    })
    raise SystemExit(0 if result["status"]=="CLOSED_RELATIVE" else 1)
