"""Standalone reference realization of the frozen ICC128 Legacy controller mathematics.

No Take-5 or Reaserch imports are used.  The file deliberately preserves the
higher-order nature of the frozen controller: open-ended semantic generation,
capability execution, admission, update, and optional discovery closure are
bindings with explicit contracts rather than hidden implementations.

The exact Take-5 activation adds a GitHub-report receipt gate.  This module
models that gate but does not claim that an unrelated environment owns GitHub.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Mapping, Protocol
import hashlib
import json

TERMINAL=frozenset({"COMPLETE","OPEN","BLOCKED","CONFLICT"})
CONTINUE="CONTINUE"

Q_FIELDS=frozenset({
    "question_id","question","live_candidate_answers",
    "enabling_discovery_or_distinction","unresolved_structure",
    "downstream_dependency",
})
W_FIELDS=frozenset({
    "work_id","question_id","probe_or_test",
    "candidate_answers_discriminated","expected_search_space_effect",
    "required_inputs_or_sources","execution_or_semantic_route",
})
UPSTREAM_FIELDS=frozenset({
    "origin_mode","source_job_id","job_basis",
    "source_relations","candidate_universe_delta",
})

DEEP_FLAGS=frozenset({
    "target_or_job_identity_open",
    "hidden_dependency_plausible",
    "representation_result_sensitive",
    "recurrence_or_prior_failure",
    "multiple_material_packages_fit",
    "project_local_capability_may_matter",
    "transfer_or_external_route_may_matter",
    "state_delta_invalidates_prior_selection",
    "capability_or_tool_selection_is_itself_the_job",
})

CHEAP_FLAGS=(
    "task_and_job_well_typed",
    "one_validated_capability_clearly_fits",
    "consequence_bounded",
    "no_material_rival_exposed",
)

F128=("L","O","R_123","D_PD","G","A","M_MT","T_2","E","V")


class SemanticModel(Protocol):
    def __call__(self,payload:dict[str,Any])->dict[str,Any]: ...

class QuestionGenerator(Protocol):
    def __call__(self,state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...

class WorkGenerator(Protocol):
    def __call__(self,questions:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...

class Selector(Protocol):
    def __call__(self,questions:list[dict[str,Any]],work:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...

class Executor(Protocol):
    def __call__(self,selected:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...

class Admitter(Protocol):
    def __call__(self,results:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]: ...

class Updater(Protocol):
    def __call__(self,state:dict[str,Any],memory:dict[str,Any],delta:dict[str,Any])->tuple[dict[str,Any],dict[str,Any]]: ...

class DiscoveryClosure(Protocol):
    def __call__(self,delta:dict[str,Any],state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]: ...


@dataclass(frozen=True)
class Package:
    id:str
    jobs:frozenset[str]
    burden:int=1
    info_gain:int=0
    dependency_leverage:int=0
    continuation_value:int=0
    protected:bool=True
    authority_ok:bool=True
    inputs_ok:bool=True


@dataclass
class Trace:
    iteration:int
    questions:list[dict[str,Any]]
    work:list[dict[str,Any]]
    selected:list[dict[str,Any]]
    results:list[dict[str,Any]]
    admitted_delta:dict[str,Any]
    state_after:dict[str,Any]
    memory_after:dict[str,Any]
    terminal:str


@dataclass
class Controller:
    gq:QuestionGenerator
    gw:WorkGenerator
    select:Selector
    execute:Executor
    admit:Admitter
    update:Updater
    dcc:DiscoveryClosure|None=None
    max_iterations:int=64
    traces:list[Trace]=field(default_factory=list)

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        z=dict(state)
        mi=dict(memory)
        self.traces=[]
        for i in range(self.max_iterations):
            terminal=str(z.get("terminal",CONTINUE))
            if terminal in TERMINAL:
                return {
                    "status":terminal,
                    "state":z,
                    "memory":mi,
                    "traces":[asdict(t) for t in self.traces],
                }

            q=self.gq(z,mi)
            if bool(z.get("admitted_continuation",False)) and not q:
                raise RuntimeError("ICC128_LIVENESS_FAILURE:G_Q_empty_with_admitted_continuation")

            w=self.gw(q,z,mi)
            selected=self.select(q,w,z,mi)
            if q and not selected and not z.get("selection_blocked"):
                raise RuntimeError("ICC128_SELECTION_FAILURE:live_questions_without_selected_or_blocked_work")

            results=self.execute(selected,z,mi)
            delta=self.admit(results,z,mi)

            if delta.get("candidate_discovery_deltas"):
                if self.dcc is None:
                    raise RuntimeError("ICC128_DCC_REQUIRED:discovery_delta_without_dcc_binding")
                delta=self.dcc(delta,z,mi)
                if not delta.get("dcc_receipt"):
                    raise RuntimeError("ICC128_DCC_RECEIPT_MISSING:normalized_delta_without_receipt")

            z2,mi2=self.update(z,mi,delta)
            terminal2=str(z2.get("terminal",CONTINUE))
            self.traces.append(Trace(
                i,q,w,selected,results,delta,z2,mi2,terminal2
            ))
            z,mi=z2,mi2

            if terminal2==CONTINUE and not z.get("admitted_continuation",False):
                raise RuntimeError("ICC128_REENTRY_FAILURE:CONTINUE_without_admitted_continuation")

        raise RuntimeError("ICC128_RESOURCE_BOUND:max_iterations")


def _require(obj:Mapping[str,Any],fields:frozenset[str],kind:str)->None:
    missing=fields-set(obj)
    if missing:
        raise ValueError(f"{kind}_MISSING_FIELDS:{sorted(missing)}")


def semantic_generate(
    model:SemanticModel,
    state:dict[str,Any],
    memory:dict[str,Any],
    upstream_context:dict[str,Any]|None=None,
)->dict[str,Any]:
    upstream=None
    if upstream_context is not None:
        _require(upstream_context,UPSTREAM_FIELDS,"UPSTREAM_CONTEXT")
        upstream=dict(upstream_context)
        if upstream["origin_mode"] not in {"ZERO_REQUEST","DIRECTED_UPSTREAM_DISCOVERY"}:
            raise ValueError("UPSTREAM_ORIGIN_MODE_INVALID")
        if (
            upstream["origin_mode"]=="ZERO_REQUEST"
            and upstream.get("job_basis")=="user_supplied_substantive_job"
        ):
            raise ValueError("ZERO_REQUEST_ORIGIN_CONTAMINATION")

    payload={
        "mode":"ICC128_OLD_RECURSIVE_PD_GENERATOR",
        "state":state,
        "memory":memory,
        "upstream_context":upstream,
        "instructions":(
            "reconstruct current epistemic state",
            "preserve live competing interpretations",
            "identify candidate-space before",
            "identify the distinction/discovery that changes the inquiry",
            "generate only questions newly available from unresolved current structure",
            "for each question generate a discriminating test/probe",
            "record expected candidate-space/search-space effect",
            "preserve upstream origin evidence when present",
        ),
    }
    out=model(payload)
    qs=list(out.get("questions",()))
    ws=list(out.get("work",()))
    for q in qs:
        _require(q,Q_FIELDS,"QUESTION")
    for w in ws:
        _require(w,W_FIELDS,"WORK")
    qids={q["question_id"] for q in qs}
    for w in ws:
        if w["question_id"] not in qids:
            raise ValueError(f"WORK_ORPHAN:{w['work_id']}")
    if state.get("unresolved") and state.get("admitted_continuation") and not qs:
        raise ValueError("GQ_LIVENESS_FAILURE")

    witness=None
    if upstream is not None:
        returned=out.get("upstream_origin_witness")
        if returned is None:
            raise ValueError("UPSTREAM_ORIGIN_WITNESS_MISSING")
        _require(returned,frozenset({"source_job_id","job_basis","source_relations"}),"UPSTREAM_ORIGIN_WITNESS")
        for key in ("source_job_id","job_basis"):
            if returned[key]!=upstream[key]:
                raise ValueError(f"UPSTREAM_ORIGIN_WITNESS_MISMATCH:{key}")
        if list(returned["source_relations"])!=list(upstream["source_relations"]):
            raise ValueError("UPSTREAM_ORIGIN_WITNESS_MISMATCH:source_relations")
        witness=dict(returned)

    return {
        "questions":qs,
        "work":ws,
        "search_space_delta":out.get("search_space_delta",{}),
        "upstream_origin_witness":witness,
    }


def activation(state:Mapping[str,Any])->str:
    if any(bool(state.get(k)) for k in DEEP_FLAGS):
        return "FIRE"
    if (
        all(bool(state.get(k)) for k in CHEAP_FLAGS)
        and not state.get("recurrence_or_prior_failure")
        and not state.get("major_state_change")
    ):
        return "CHEAP_DIRECT"
    return "OPEN"


def dominates(a:Package,b:Package,required_jobs:set[str])->bool:
    if not (a.protected and a.authority_ok and a.inputs_ok):
        return False
    if not (b.protected and b.authority_ok and b.inputs_ok):
        return True
    ca=required_jobs.issubset(a.jobs)
    cb=required_jobs.issubset(b.jobs)
    if ca and not cb:
        return True
    if cb and not ca:
        return False
    da=(a.info_gain,a.dependency_leverage,a.continuation_value,-a.burden)
    db=(b.info_gain,b.dependency_leverage,b.continuation_value,-b.burden)
    return all(x>=y for x,y in zip(da,db)) and any(x>y for x,y in zip(da,db))


def nondominated(packages:list[Package],required_jobs:set[str])->list[Package]:
    admitted=[p for p in packages if p.protected and p.authority_ok and p.inputs_ok]
    covered=[p for p in admitted if required_jobs.issubset(p.jobs)]
    pool=covered or admitted
    return [
        p for p in pool
        if not any(dominates(q,p,required_jobs) for q in pool if q!=p)
    ]


def choose(state:Mapping[str,Any],packages:list[Package],required_jobs:set[str])->dict[str,Any]:
    mode=activation(state)
    frontier=nondominated(packages,required_jobs) if mode in {"CHEAP_DIRECT","FIRE"} else []
    if mode=="CHEAP_DIRECT":
        if not frontier:
            return {"mode":mode,"status":"OPEN","frontier":[],"selected":[]}
        cheapest=min(frontier,key=lambda p:p.burden)
        return {
            "mode":mode,
            "status":"SELECTED",
            "frontier":[p.id for p in frontier],
            "selected":[cheapest.id],
        }
    if mode=="FIRE":
        return {
            "mode":mode,
            "status":"SELECTED" if frontier else "OPEN",
            "frontier":[p.id for p in frontier],
            "selected":[p.id for p in frontier],
        }
    return {"mode":"OPEN","status":"OPEN","frontier":[],"selected":[]}


def needs_reselection(delta:Mapping[str,Any])->bool:
    keys={
        "material_result_delta","material_search_delta","new_OPEN",
        "changed_job_identity","changed_representation","failed_route",
        "new_project_local_capability","changed_authority",
    }
    return any(bool(delta.get(k)) for k in keys)


def build_learning_report(
    run_id:str,
    run_result:dict[str,Any],
    initial_state:dict[str,Any],
    initial_memory:dict[str,Any],
)->dict[str,Any]:
    traces=list(run_result.get("traces",()))
    admitted=[
        t.get("admitted_delta",{}) for t in traces
        if t.get("admitted_delta")
    ]
    return {
        "tool":"ICC128 Legacy",
        "run_id":run_id,
        "learning_persistence":"REPORT_ONLY_EPHEMERAL_CONTROLLER_MEMORY",
        "run_status":run_result.get("status","UNKNOWN"),
        "initial_state":initial_state,
        "initial_memory":initial_memory,
        "iteration_learning":traces,
        "admitted_deltas":admitted,
        "final_state":run_result.get("state",{}),
        "final_ephemeral_memory":run_result.get("memory",{}),
        "ephemeral_memory_disposition":"DISCARD_AFTER_REPORT_SUBMISSION",
    }


def report_hash(report:Mapping[str,Any])->str:
    raw=json.dumps(report,sort_keys=True,separators=(",",":"),default=repr)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def take5_activation_closed(receipt:Mapping[str,Any]|None)->bool:
    if not isinstance(receipt,Mapping):
        return False
    return bool(
        receipt.get("repository")=="thytabakman-jpg/Take-5"
        and str(receipt.get("path","")).startswith("artifacts/icc128-legacy-learning/")
        and str(receipt.get("commit_sha","")).strip()
        and str(receipt.get("report_sha256","")).strip()
    )


PORTABLE_MATH=r"""
BASE:
  Terminal = {COMPLETE, OPEN, BLOCKED, CONFLICT}
  F_128 = {L,O,R_123,D_PD,G,A,M_MT,T_2,E,V}
  MI_t = { I_t^k : k in Objects_t }
  I_t^k = <ObjectID,VersionID,Math,ComponentStatus,WholeStatus,Renderer,Freshness>

CORE:
  ICC_128 = C_128(Z_t,F_128,MI_t)
  Q_t = rho_128(Z_t,MI_t) subseteq F_128
  Y_t = Run_128(Q_t,Z_t,MI_t)
  MI_(t+1) = Sync_128(MI_t,Y_t)
  Z_(t+1) = U_128(Z_t,Y_t,MI_(t+1))

MINIMAL STATE:
  Z^min_(J,K) = Hist_(J,K) / ~^Z_(J,K)
  h ~^Z_(J,K) h'
    iff every admitted MI state, authority/run context, and future continuation
    induces protected-equivalent ICC-128 observations from h and h'.

  MI^min_(J,K) = MIState / ~^MI_(J,K)
  m ~^MI_(J,K) m'
    iff every admitted minimal controller state and continuation induces
    protected-equivalent rho_128, Run_128, Sync_128, U_128, tau_128 behavior.

SEMANTIC GENERATION:
  G_Q(Z,M) = finite Q such that every q in Q is a record
    <id,question,live_candidate_answers,enabling_discovery_or_distinction,
     unresolved_structure,downstream_dependency>
    and each q is newly licensed by unresolved structure in the current epistemic state.

  G_W(Q,Z,M) = finite W such that every w in W is a record
    <id,question_id,probe_or_test,candidate_answers_discriminated,
     expected_search_space_effect,required_inputs_or_sources,
     execution_or_semantic_route>
    and question_id(w) belongs to ids(Q).

  admitted_continuation(Z)=1 => G_Q(Z,M) != empty.

RHO POLICY:
  Deep = {
    target_or_job_identity_open, hidden_dependency_plausible,
    representation_result_sensitive, recurrence_or_prior_failure,
    multiple_material_packages_fit, project_local_capability_may_matter,
    transfer_or_external_route_may_matter,
    state_delta_invalidates_prior_selection,
    capability_or_tool_selection_is_itself_the_job
  }.

  Cheap = {
    task_and_job_well_typed, one_validated_capability_clearly_fits,
    consequence_bounded, no_material_rival_exposed
  }.

  alpha(Z) =
    FIRE         if exists d in Deep with Z[d]=1
    CHEAP_DIRECT if forall c in Cheap, Z[c]=1
                    and not recurrence_or_prior_failure
                    and not major_state_change
    OPEN         otherwise.

  A package p =
    <id,jobs,burden,info_gain,dependency_leverage,continuation_value,
     protected,authority_ok,inputs_ok>.

  Adm(p) = protected(p) and authority_ok(p) and inputs_ok(p).
  Cover_R(p) = R subseteq jobs(p).
  v(p) = <info_gain(p),dependency_leverage(p),continuation_value(p),-burden(p)>.

  p >_R q iff
    Adm(p) and (
      not Adm(q)
      or (Cover_R(p) and not Cover_R(q))
      or (
        Cover_R(p)=Cover_R(q)
        and v(p) >=componentwise v(q)
        and v(p) != v(q)
      )
    ).

  ND_R(P) = {p in P : not exists q in P with q >_R p}.

  rho_128(Z,MI,P,R) =
    argmin_burden ND_R(P)          when alpha(Z)=CHEAP_DIRECT
    ND_R(P)                        when alpha(Z)=FIRE
    empty                          when alpha(Z)=OPEN.

  Selection is set-valued.  Incomparable packages survive.

ONE CONTROLLER STEP:
  q := G_Q(z,m)
  require admitted_continuation(z)=0 or q != empty
  w := G_W(q,z,m)
  s := S(q,w,z,m)
  require q=empty or s!=empty or selection_blocked(z)=1
  y := E(s,z,m)
  delta := A(y,z,m)
  if candidate_discovery_deltas(delta)!=empty:
      delta := DCC(delta,z,m)
      require dcc_receipt(delta)
  (z',m') := U(z,m,delta)
  require terminal(z')!=CONTINUE or admitted_continuation(z')=1

RUN:
  (z_0,m_0) given.
  Repeat ONE CONTROLLER STEP until terminal(z_t) in Terminal.
  If no terminal state appears by the declared resource bound, return RESOURCE_BOUND.

CAPABILITY GAP:
  CapabilityGap_(J,K)(F,z,m)
    = RequiredRoles_(J,K)(z,m) - Covered_(J,K)(F,z,m).

  terminal(z)=COMPLETE =>
    CapabilityGap_(J,K)(F_128,z,m)=empty
    or a typed upstream capability-discovery handoff exists.

RESELECTION:
  Reenter(delta)=1 iff any of
    material_result_delta, material_search_delta, new_OPEN,
    changed_job_identity, changed_representation, failed_route,
    new_project_local_capability, changed_authority
  is true.

PROTECTED BEHAVIOR:
  dynamic selection; question selection distinct from tool selection;
  result-sensitive differentiation; goal recovery before completion pressure;
  explicit MI currentness; semantic selection distinct from execution;
  child completion distinct from controller completion;
  execution/admission/update/reentry loop;
  OPEN/BLOCKED/CONFLICT preservation;
  material change regenerates frontiers;
  negative-memory-sensitive future selection;
  child identity/currentness invalidation;
  presentation does not change mathematics;
  runtime versus semantic distinction;
  no self-promotion.

CURRENT LEGACY ACTIVATION WRAPPER:
  memory persists within one run.
  after every run, Report(run) is produced.
  controller memory is discarded after report submission.
  exact Take-5 run closure additionally requires a GitHub commit receipt:
    LegacyRunClosed(run) iff GitHubReportCommitReceipt(run) exists.

HIGHER-ORDER BINDING CONTRACT:
  The frozen controller is parameterized by
    <G_Q,G_W,S,E,A,U,DCC>.
  G_Q and G_W obey SEMANTIC GENERATION.
  S obeys RHO POLICY or another binding preserving its protected selector behavior.
  E executes selected work and returns execution truth.
  A admits/reconciles results while preserving OPEN/CONFLICT/provenance/negative evidence.
  U updates controller state and mathematical-interface memory and establishes reentry/terminal state.
  DCC is required exactly when discovery-sensitive deltas are proposed.

PORTABILITY:
  A new reasoning host can instantiate the higher-order controller without repository
  or conversation history when it supplies the above bindings from its own reasoning
  and available execution environment.
  Exact Take-5 activation closure additionally requires the Take-5 GitHub receipt primitive.
"""


def portable_core_package(
    *,
    semantic_reasoner_available:bool,
    execution_interface_available:bool=True,
    controller_bindings_available:bool=True,
)->dict[str,Any]:
    """Package shape consumed by Take-5's SHOW_ME_THE_MATH checker."""
    return {
        "full_math":PORTABLE_MATH,
        "run_spec":{
            "controller":"C_128",
            "bindings":("G_Q","G_W","S","E","A","U","DCC"),
            "terminal":tuple(sorted(TERMINAL)),
            "resource_bound":"declared max_iterations",
        },
        "definitions":{
            "ICC128_LEGACY_CORE":{"dependencies":("CONTROLLER_LOOP","SEMANTIC_GENERATION","RHO_POLICY","CAPABILITY_GAP","RESELECTION")},
            "CONTROLLER_LOOP":{"dependencies":(
                "finite_maps","finite_sequences","boolean_logic",
                "semantic_reasoner","execution_interface",
                "package_compiler","admission_binding","update_binding","discovery_closure_binding"
            )},
            "SEMANTIC_GENERATION":{"dependencies":("finite_maps","finite_sequences","boolean_logic","semantic_reasoner")},
            "RHO_POLICY":{"dependencies":("finite_sets","finite_sequences","integer_order","boolean_logic","package_compiler")},
            "CAPABILITY_GAP":{"dependencies":("finite_sets","set_difference")},
            "RESELECTION":{"dependencies":("finite_maps","boolean_logic")},
        },
        "load_bearing_symbols":("ICC128_LEGACY_CORE",),
        "initialization":{
            "defined":True,
            "state":"finite mapping containing terminal/admitted_continuation plus job state",
            "memory":"finite mapping; initially host-supplied, normally empty for Legacy activation",
        },
        "runtime_primitives":{
            "finite_maps":{"typed_contract":"finite partial map lookup/update","available":True},
            "finite_sequences":{"typed_contract":"finite ordered sequence operations","available":True},
            "finite_sets":{"typed_contract":"finite set operations","available":True},
            "set_difference":{"typed_contract":"A x A -> A","available":True},
            "integer_order":{"typed_contract":"total order on integers","available":True},
            "boolean_logic":{"typed_contract":"Boolean connectives","available":True},
            "semantic_reasoner":{
                "typed_contract":"state x memory -> schema-valid state-relative questions/work",
                "available":bool(semantic_reasoner_available),
            },
            "execution_interface":{
                "typed_contract":"selected work x state x memory -> result records; unavailable external actions return typed BLOCKED",
                "available":bool(execution_interface_available),
            },
            "package_compiler":{
                "typed_contract":"question/work frontier x state x memory x F_128 -> finite candidate package set preserving jobs, inputs, authority, burden and protected plurality",
                "available":bool(controller_bindings_available),
            },
            "admission_binding":{
                "typed_contract":"result records x state x memory -> admitted delta preserving OPEN, CONFLICT, provenance, rejection and negative evidence",
                "available":bool(controller_bindings_available),
            },
            "update_binding":{
                "typed_contract":"state x memory x admitted delta -> successor state x successor memory with stale-support invalidation and typed terminal/reentry state",
                "available":bool(controller_bindings_available),
            },
            "discovery_closure_binding":{
                "typed_contract":"discovery-sensitive admitted delta x state x memory -> normalized delta carrying dcc_receipt; required only when candidate_discovery_deltas is nonempty",
                "available":bool(controller_bindings_available),
            },
        },
        "persistence":{
            "specified":True,
            "core":"within-run memory only",
            "legacy_activation":"final controller memory discarded after report submission; report persists",
        },
        "protected_behavior":(
            "dynamic_state_relative_selection",
            "question_selection_distinct_from_tool_selection",
            "schema_valid_state_relative_semantic_generation",
            "execution_truth_before_admission",
            "discovery_closure_receipt_when_required",
            "typed_terminal_and_reentry",
            "OPEN_BLOCKED_CONFLICT_preservation",
            "negative_memory_affects_future_selection",
            "no_self_promotion",
        ),
        "equivalence_tests":(
            "two_step_fixture_reaches_COMPLETE",
            "empty_GQ_with_live_continuation_raises",
            "live_question_without_selection_raises",
            "discovery_delta_without_DCC_raises",
            "CONTINUE_without_admitted_continuation_raises",
            "rho_policy_matches_frozen dominance/frontier semantics",
        ),
    }


def _fixture_model(payload:dict[str,Any])->dict[str,Any]:
    step=int(payload["state"].get("step",0))
    if step>=2:
        return {"questions":[],"work":[]}
    qid=f"q{step+1}"
    return {
        "questions":[{
            "question_id":qid,
            "question":f"fixture question {step+1}",
            "live_candidate_answers":["A","B"],
            "enabling_discovery_or_distinction":"fixture state transition",
            "unresolved_structure":"fixture unresolved coordinate",
            "downstream_dependency":"fixture closure",
        }],
        "work":[{
            "work_id":f"w{step+1}",
            "question_id":qid,
            "probe_or_test":"fixture discriminator",
            "candidate_answers_discriminated":["A","B"],
            "expected_search_space_effect":"one step",
            "required_inputs_or_sources":[],
            "execution_or_semantic_route":"fixture",
        }],
        "search_space_delta":{"material":True},
    }


def _self_test()->int:
    initial={"step":0,"terminal":CONTINUE,"admitted_continuation":True,"unresolved":True}
    memory={}

    def gq(z,m):
        return semantic_generate(_fixture_model,z,m)["questions"]

    def gw(q,z,m):
        return semantic_generate(_fixture_model,z,m)["work"]

    def select(q,w,z,m):
        return w[:1]

    def execute(selected,z,m):
        return [{"work_id":x["work_id"],"finding":"fixture evidence"} for x in selected]

    def admit(results,z,m):
        return {"results":results,"material_result_delta":bool(results)}

    def update(z,m,delta):
        z=dict(z)
        m=dict(m)
        z["step"]+=1
        m[f"step_{z['step']}"]=delta
        if z["step"]>=2:
            z.update({"terminal":"COMPLETE","admitted_continuation":False,"unresolved":False})
        else:
            z.update({"terminal":CONTINUE,"admitted_continuation":True})
        return z,m

    out=Controller(gq,gw,select,execute,admit,update).run(initial,memory)
    if out["status"]!="COMPLETE" or len(out["traces"])!=2:
        return 1

    report=build_learning_report("portable-self-test",out,initial,memory)
    if not report_hash(report):
        return 2

    # Exact Take-5 activation stays fail-closed without a GitHub receipt.
    if take5_activation_closed(None):
        return 3

    # The controller core must preserve liveness failure.
    bad=Controller(lambda z,m:[],gw,select,execute,admit,update)
    try:
        bad.run(initial,memory)
    except RuntimeError as exc:
        if "G_Q_empty" not in str(exc):
            return 4
    else:
        return 5

    print(json.dumps({
        "portable_core":"PASS",
        "iterations":len(out["traces"]),
        "exact_take5_activation_without_github_receipt":"BLOCKED",
        "math_sha256":hashlib.sha256(PORTABLE_MATH.encode("utf-8")).hexdigest(),
    },indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(_self_test())
