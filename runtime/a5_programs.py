"""Bounded capability adapters for the A5 registry, not independent evidence providers."""
from collections import deque
from collections.abc import Mapping
from math import isfinite
from copy import deepcopy
from dataclasses import replace
from types import MappingProxyType
from a5_core import ProgramRegistry,ProgramSpec

# I. Current capability definitions (identity and contract metadata).
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


# II. Bounded capability implementations.
# ACCEPT is not independent semantic evidence, mutation authority, or HF2 closure.

def _sequence(value):
    return value if isinstance(value, (list, tuple)) else None


def _rows(value):
    rows = _sequence(value)
    return rows if rows is not None and all(isinstance(row, dict) for row in rows) else None


def _label(value):
    # IDs are nonblank text or exact integers, never Boolean/numeric aliases.
    return (type(value) is str and bool(value.strip())) or type(value) is int


def _label_set(value):
    if not isinstance(value, (list, tuple, set, frozenset)):
        return None
    return set(value) if all(_label(x) for x in value) else None


def _result_key(value):
    """Canonical typed key for finite, acyclic built-in result values."""
    kind = type(value)
    if kind in (type(None), bool, int, str, bytes):
        return kind, value
    if kind is float and isfinite(value):
        return kind, value
    if kind in (list, tuple):
        return kind, tuple(_result_key(x) for x in value)
    if kind is dict:
        return kind, frozenset((_result_key(k), _result_key(v)) for k, v in value.items())
    if kind in (set, frozenset):
        return kind, frozenset(_result_key(x) for x in value)
    raise ValueError("unsupported result value")


def _same_result(left, right):
    """True/False for comparable values; None for unestablished comparison."""
    try:
        return _result_key(left) == _result_key(right)
    except (ValueError, RecursionError):
        return None


def _payload(value):
    """Malformed envelopes supply no admissible evidence."""
    return value if isinstance(value, Mapping) else {}


# Orientation: C01-C06.
def run_orient(program_id, payload):
    payload = _payload(payload)
    if program_id=="C01":
        kinds=_sequence(payload.get("admissible_typings"))
        if kinds and len(kinds)==1 and _label(kinds[0]): return {"status":"ACCEPT","typed_task_context":kinds[0]}
        if not kinds: return {"status":"OPEN","reason":"no admissible typing established"}
        return {"status":"OPEN","alternatives":kinds}
    if program_id=="C02":
        if payload.get("same_lineage") is True: return {"status":"ACCEPT","identity_relation":"SAME_REFERENT"}
        if payload.get("same_lineage") is False: return {"status":"ACCEPT","identity_relation":"DISTINCT_REFERENT"}
        return {"status":"OPEN","identity_relation":"UNRESOLVED"}
    if program_id=="C03":
        nodes=_rows(payload.get("versions"))
        if nodes is None:
            return {"status":"OPEN","authoritative_candidates":[]}
        auth=[x for x in nodes if x.get("authoritative") is True]
        unresolved=[x for x in nodes if type(x.get("authoritative")) is not bool or not _label(x.get("id"))]
        ids = [x["id"] for x in nodes if _label(x.get("id"))]
        if len(ids) != len(set(ids)):
            return {"status":"OPEN","authoritative_candidates":[x.get("id") for x in auth],"reason":"duplicate version identity"}
        if len(auth)==1 and not unresolved:
            return {"status":"ACCEPT","current":auth[0]["id"]}
        return {"status":"OPEN","authoritative_candidates":[x.get("id") for x in auth],"unresolved":unresolved}
    if program_id=="C04":
        if not _label(payload.get("source_id")) or "claim" not in payload:
            return {"status":"OPEN","frozen_source_packet":None}
        return {"status":"ACCEPT","frozen_source_packet":deepcopy({"source_id":payload["source_id"],"claim":payload["claim"]})}
    if program_id=="C05":
        protected=_sequence(payload.get("protected"))
        if not _label(payload.get("target")) or protected is None or _label_set(protected) is None:
            return {"status":"OPEN","frozen_target_contract":None}
        return {"status":"ACCEPT","frozen_target_contract":deepcopy({"target":payload["target"],"protected":tuple(protected)})}
    if program_id=="C06":
        deps=_rows(payload.get("dependencies"))
        return {"status":"ACCEPT" if deps is not None and all(_label(d.get("availability")) or type(d.get("availability")) is bool for d in deps) else "OPEN","external_dependency_map":deps}
    raise KeyError(program_id)


# Mapping and representation: C07-C13, C49.
def run_map(program_id, payload):
    payload = _payload(payload)
    if program_id == "C07":
        candidates = _rows(payload.get("candidate_edges"))
        if candidates is None:
            return {"status":"OPEN","typed_dependency_edges":[]}
        edges = [e for e in candidates if e.get("material") is True]
        unresolved = [e for e in candidates if type(e.get("material")) is not bool]
        return {"status":"OPEN" if unresolved else ("ACCEPT" if edges else "NOOP"),"typed_dependency_edges":edges,**({"unresolved":unresolved} if unresolved else {})}
    if program_id == "C08":
        spines = _sequence(payload.get("spines"))
        valid = bool(spines) and all(_sequence(x) and _label_set(x) is not None for x in spines)
        return {"status": "ACCEPT" if valid else "OPEN", "plural_dependency_spines": spines}
    if program_id == "C09":
        edges = _rows(payload.get("edges"))
        if edges is None:
            return {"status":"OPEN","typed_layer_graph":None}
        unresolved = [e for e in edges if not e.get("relation_type")]
        return {"status": "OPEN" if unresolved else "ACCEPT", "typed_layer_graph": edges}
    if program_id == "C10":
        reps = _rows(payload.get("representations"))
        if not reps or len(reps)<2 or any("result" not in row for row in reps):
            return {"status":"OPEN","invariant":False,"representation_residual":reps or []}
        comparisons = [_same_result(reps[0]["result"], row["result"]) for row in reps[1:]]
        if any(x is None for x in comparisons):
            return {"status":"OPEN","invariant":False,"representation_residual":reps,"reason":"unestablished result comparison"}
        invariant = all(comparisons)
        return {"status":"ACCEPT","invariant":invariant,"representation_residual":[] if invariant else reps}
    if program_id == "C11":
        coordinates = _rows(payload.get("coordinates"))
        if coordinates is None:
            return {"status":"OPEN","minimal_sensitive_supports":[]}
        sensitive = [x["id"] for x in coordinates if x.get("changed_result") is True and _label(x.get("id"))]
        unresolved = [x for x in coordinates if type(x.get("changed_result")) is not bool or not _label(x.get("id"))]
        ids = [x["id"] for x in coordinates if _label(x.get("id"))]
        if len(ids) != len(set(ids)):
            return {"status":"OPEN","minimal_sensitive_supports":[],"unresolved":coordinates,"reason":"duplicate coordinate identity"}
        return {"status":"OPEN" if unresolved else "ACCEPT","minimal_sensitive_supports":sensitive,**({"unresolved":unresolved} if unresolved else {})}
    if program_id == "C12":
        maps = _sequence(payload.get("sensitivity_maps"))
        sets = [_label_set(x) for x in maps] if maps else []
        if not sets or any(x is None for x in sets):
            return {"status":"OPEN","invariant_core":[],"residual":[]}
        core = set.intersection(*sets)
        residual = set.union(*sets) - core
        try:
            return {"status":"ACCEPT","invariant_core":sorted(core),"residual":sorted(residual)}
        except TypeError:
            return {"status":"OPEN","invariant_core":[],"residual":[],"reason":"incomparable coordinate labels"}
    if program_id == "C13":
        edges = _rows(payload.get("edges"))
        if edges is None:
            return {"status":"OPEN","attributed_edge_chain":None}
        unresolved = [e for e in edges if not e.get("attribution")]
        return {"status": "OPEN" if unresolved else "ACCEPT", "attributed_edge_chain": edges}
    if program_id == "C49":
        visited = _rows(payload.get("visited"))
        if visited is None:
            return {"status":"OPEN","navigation_trace":[],"exact_object_set":[]}
        relevant = []
        for row in visited:
            if row.get("task_relevant") is True and _label(row.get("id")) and row["id"] not in relevant:
                relevant.append(row["id"])
        unresolved = [x for x in visited if type(x.get("task_relevant")) is not bool or not _label(x.get("id"))]
        conflicts = {x["id"] for x in visited if _label(x.get("id")) and x.get("task_relevant") is False} & set(relevant)
        if conflicts:
            unresolved.extend(x for x in visited if _label(x.get("id")) and x["id"] in conflicts)
            relevant = [x for x in relevant if x not in conflicts]
        return {"status":"OPEN" if unresolved else "ACCEPT","navigation_trace":visited,"exact_object_set":relevant,**({"unresolved":unresolved} if unresolved else {})}
    raise KeyError(program_id)


# Critical examination: C14-C19.
def run_attack(program_id, payload):
    payload = _payload(payload)
    if program_id=="C14":
        findings=_rows(payload.get("findings",[]))
        interactions=_rows(payload.get("interaction_findings",[]))
        if ("findings" not in payload and "interaction_findings" not in payload) or findings is None or interactions is None:
            return {"status":"OPEN","hostile_residuals":[]}
        rows=list(findings)+list(interactions)
        residual=[x for x in rows if x.get("material") is True]
        unresolved=[x for x in rows if type(x.get("material")) is not bool]
        return {"status":"OPEN" if unresolved else ("ACCEPT" if residual else "NOOP"),"hostile_residuals":residual,**({"unresolved":unresolved} if unresolved else {})}
    if program_id=="C15":
        source=_label_set(payload.get("source_effects")); target=_label_set(payload.get("target_effects"))
        if source is None or target is None:
            return {"status":"OPEN","covered":[],"novel_residual":[],"terminology_only":False}
        try:
            return {"status":"ACCEPT","covered":sorted(source & target),"novel_residual":sorted(target-source),"terminology_only":payload.get("different_terms") is True and target<=source}
        except TypeError:
            return {"status":"OPEN","covered":[],"novel_residual":[],"terminology_only":False,"reason":"incomparable effect labels"}
    if program_id=="C16":
        protected=_label_set(payload.get("protected"))
        candidates=_rows(payload.get("candidates"))
        if protected is None or candidates is None:
            return {"status":"OPEN","change_frontier":[]}
        allowed=[]; unresolved=[]
        for candidate in candidates:
            preserves=_label_set(candidate.get("preserves"))
            if preserves is None:
                unresolved.append(candidate)
            elif protected<=preserves:
                allowed.append(candidate)
        return {"status":"OPEN" if unresolved or not allowed else "ACCEPT","change_frontier":allowed,**({"unresolved":unresolved} if unresolved else {})}
    if program_id=="C17":
        inventory=payload.get("failures")
        if not isinstance(inventory,(list,tuple)) or any(not isinstance(x,dict) for x in inventory):
            return {"status":"OPEN","mechanism_dispositions":[],"unresolved":[],"blocker":"FAILURE_INVENTORY_REQUIRED"}
        # Only an explicit negative materiality judgment excludes a failure.
        failures=[x for x in inventory if x.get("material",True) is not False]
        unresolved_labels={"UNKNOWN","OPEN","BLOCKED","CONFLICT","FAILED","FAIL","UNRESOLVED","UNDETERMINED","NOT_DIAGNOSED","NONE","N/A"}
        def identified(row):
            mechanism=row.get("mechanism")
            return isinstance(mechanism,str) and bool(mechanism.strip()) and mechanism.strip().upper() not in unresolved_labels
        diagnosed=[x for x in failures if identified(x) and ("material" not in x or x["material"] is True)]
        unresolved=[x for x in failures if not identified(x) or ("material" in x and x["material"] is not True)]
        return {"status":"OPEN" if unresolved else "ACCEPT","mechanism_dispositions":diagnosed,"unresolved":unresolved}
    if program_id=="C18":
        chain=_rows(payload.get("causal_chain"))
        if not chain:
            return {"status":"OPEN","root_disposition":None}
        root=None
        for index, row in enumerate(chain):
            if not row.get("evidence"):
                return {"status":"OPEN","root_disposition":root,"unresolved":chain[index:]}
            if row.get("terminal") is True and index != len(chain)-1:
                return {"status":"OPEN","root_disposition":row,"unresolved":chain[index+1:]}
            root=row
        return {"status":"ACCEPT" if root.get("terminal") is True else "OPEN","root_disposition":root}
    if program_id=="C19":
        seeds=_sequence(payload.get("seed_frontier")); graph=payload.get("graph")
        if seeds is None or not isinstance(graph,dict):
            return {"status":"OPEN","discovery_trace":[],"discovered":[]}
        if _label_set(seeds) is None or not all(_label(x) for x in graph) or any(
            _sequence(neighbours) is None or _label_set(neighbours) is None
            for neighbours in graph.values()
        ):
            return {"status":"OPEN","discovery_trace":[],"discovered":[]}
        frontier=deque(dict.fromkeys(seeds)); seen=set(seeds); trace=[]
        while frontier:
            x=frontier.popleft(); trace.append(x)
            for y in graph.get(x,[]):
                if y not in seen:
                    seen.add(y); frontier.append(y)
        try:
            return {"status":"ACCEPT","discovery_trace":trace,"discovered":sorted(seen)}
        except TypeError:
            return {"status":"OPEN","discovery_trace":trace,"discovered":trace,"reason":"incomparable object identities"}
    raise KeyError(program_id)


# Candidate development: C20-C23.
def run_candidate_development(program_id, payload):
    payload = _payload(payload)
    if program_id in {"C20","C21","C22","C23"}:
        key={"C20":"rivals","C21":"candidates","C22":"improvement_frontier","C23":"typed_relation"}[program_id]
        value=payload.get(key)
        valid = (isinstance(value, (str, dict)) and bool(value.strip() if isinstance(value, str) else value)) if program_id == "C23" else bool(_sequence(value)) and all(isinstance(x, (str, dict)) and bool(x.strip() if isinstance(x, str) else x) for x in value)
        return {"status":"ACCEPT" if valid else "OPEN",key:value}
    raise KeyError(program_id)


# Structural improvement: C24-C31.
def run_structural_improvement(program_id, payload):
    payload = _payload(payload)
    if program_id in {"C24","C25","C26","C27","C28","C29","C30","C31"}:
        key=REGISTRY.get(program_id).protected_outputs[0]
        value=payload.get(key,payload.get("candidate"))
        protected=_label_set(payload.get("protected"))
        preserves=_label_set(payload.get("preserves"))
        consistent=key not in payload or "candidate" not in payload or _same_result(value,payload["candidate"]) is True
        ok=bool(value) and consistent and protected is not None and preserves is not None and protected<=preserves
        return {"status":"ACCEPT" if ok else "OPEN",key:value if ok else None}
    raise KeyError(program_id)


# Improvement evaluation: C32-C36.
def run_improvement_evaluation(program_id, payload):
    payload = _payload(payload)
    if program_id=="C32":
        routes=_rows(payload.get("routes"))
        if routes is None:
            return {"status":"OPEN","routes":[]}
        x=[r for r in routes if r.get("licensed") is True and r.get("reachable") is True]
        unresolved=[r for r in routes if r.get("licensed") is not False and r.get("reachable") is not False and not (r.get("licensed") is True and r.get("reachable") is True)]
        return {"status":"OPEN" if unresolved or not x else "ACCEPT","routes":x,**({"unresolved":unresolved} if unresolved else {})}
    if program_id=="C33":
        ok=payload.get("strict_gain") is True and payload.get("preserves") is True
        return {"status":"ACCEPT" if ok else "OPEN","gain_disposition":"STRICT_GAIN" if ok else "UNESTABLISHED"}
    if program_id=="C34":
        if any(payload.get(key) is None for key in ("protected_before","protected_after")):
            return {"status":"OPEN","regression_disposition":"UNESTABLISHED"}
        ok=_same_result(payload["protected_before"],payload["protected_after"])
        if ok is None:
            return {"status":"OPEN","regression_disposition":"UNESTABLISHED"}
        return {"status":"ACCEPT" if ok else "FAIL","regression_disposition":"PASS" if ok else "REGRESSION"}
    if program_id=="C35":
        frontier=_sequence(payload.get("nondominated_set"))
        if frontier is None:
            return {"status":"OPEN","nondominated_set":None,"unresolved_candidates":payload.get("candidates")}
        return {"status":"ACCEPT","nondominated_set":frontier}
    if program_id=="C36":
        key=REGISTRY.get(program_id).protected_outputs[0]
        value=payload.get(key)
        return {"status":"ACCEPT" if value is not None else "OPEN",key:value}
    raise KeyError(program_id)


# Knowledge transfer: C37-C43.
def run_knowledge_transfer(program_id, payload):
    payload = _payload(payload)
    if program_id in {"C37","C38","C39","C40","C41","C42","C43"}:
        key=REGISTRY.get(program_id).protected_outputs[0]
        value=payload.get(key)
        return {"status":"ACCEPT" if value is not None else "OPEN",key:value}
    raise KeyError(program_id)


# Verification and closure: C44-C48.
def run_verification(program_id, payload):
    payload = _payload(payload)
    if program_id=="C44":
        if any(key not in payload for key in ("expected","actual")):
            return {"status":"OPEN","verification":"UNESTABLISHED"}
        ok=_same_result(payload["expected"],payload["actual"])
        if ok is None:
            return {"status":"OPEN","verification":"UNESTABLISHED"}
        return {"status":"ACCEPT" if ok else "FAIL","verification":"PASS" if ok else "FAIL"}
    if program_id=="C45":
        if any(type(payload.get(key)) is not bool for key in ("preregistered","pass")):
            return {"status":"OPEN","holdout_result":"UNESTABLISHED"}
        ok=payload["preregistered"] and payload["pass"]
        return {"status":"ACCEPT" if ok else "FAIL","holdout_result":"PASS" if ok else "FAIL"}
    if program_id=="C46":
        if any(key not in payload for key in ("with_component","without_component")):
            return {"status":"OPEN","causal_effect":None}
        same = _same_result(payload["with_component"],payload["without_component"])
        return {"status":"OPEN" if same is None else "ACCEPT","causal_effect":None if same is None else not same}
    if program_id=="C47":
        x=payload.get("blocking_open")
        if not isinstance(x,(list,tuple)):
            return {"status":"OPEN","closure_disposition":"UNESTABLISHED"}
        return {"status":"ACCEPT" if not x else "OPEN","closure_disposition":"RELATIVE_CLOSED" if not x else "BLOCKED_BY_OPEN"}
    if program_id=="C48":
        candidates=payload.get("candidates")
        if not isinstance(candidates,(list,tuple)) or any(not isinstance(c,dict) for c in candidates):
            return {"status":"OPEN","strict_gain_or_failure":"CANDIDATE_INVENTORY_REQUIRED"}
        x=[c for c in candidates if c.get("strict_gain") is True and c.get("preserves") is True]
        unresolved=[c for c in candidates if c.get("strict_gain") is not False and c.get("preserves") is not False
                    and not (c.get("strict_gain") is True and c.get("preserves") is True)]
        if x:
            return {"status":"ACCEPT","strict_gain_or_failure":x,**({"unresolved":unresolved} if unresolved else {})}
        if unresolved:
            return {"status":"OPEN","strict_gain_or_failure":"STRICT_GAIN_OR_PRESERVATION_UNRESOLVED","unresolved":unresolved}
        return {"status":"NOOP","strict_gain_or_failure":"NO_STRICT_GAIN_FOUND"}
    raise KeyError(program_id)


# III. Execution bindings (single source of adapter membership and executability).
_FAMILY_BINDINGS = (
    (run_orient, ("C01", "C02", "C03", "C04", "C05", "C06")),
    (run_map, ("C07", "C08", "C09", "C10", "C11", "C12", "C13", "C49")),
    (run_attack, ("C14", "C15", "C16", "C17", "C18", "C19")),
    (run_candidate_development, ("C20", "C21", "C22", "C23")),
    (run_structural_improvement, ("C24", "C25", "C26", "C27", "C28", "C29", "C30", "C31")),
    (run_improvement_evaluation, ("C32", "C33", "C34", "C35", "C36")),
    (run_knowledge_transfer, ("C37", "C38", "C39", "C40", "C41", "C42", "C43")),
    (run_verification, ("C44", "C45", "C46", "C47", "C48")),
)


def _build_bindings():
    bindings = {}
    for handler, ids in _FAMILY_BINDINGS:
        for pid in ids:
            if pid in bindings:
                raise ValueError(f"Duplicate capability binding: {pid}")
            bindings[pid] = handler
    if set(bindings) != EXPECTED_C or len(_SPECS) != len(EXPECTED_C) or {spec.program_id for spec in _SPECS} != EXPECTED_C:
        raise ValueError("Current capability definition/binding coverage mismatch")
    return MappingProxyType(bindings)


CAPABILITY_BINDINGS = _build_bindings()
REGISTRY = ProgramRegistry()
for _spec in _SPECS:
    REGISTRY.register(replace(_spec, executable=_spec.program_id in CAPABILITY_BINDINGS))


def run_generic(program_id, payload):
    """Compatibility entrypoint for the former C20-C48 generic family."""
    handler = CAPABILITY_BINDINGS[program_id]
    if handler in (run_orient, run_map, run_attack):
        raise KeyError(program_id)
    return handler(program_id, payload)
