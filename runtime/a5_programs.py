"""Bounded capability adapters for the A5 registry, not independent evidence providers."""
from collections import deque
from copy import deepcopy
from dataclasses import replace
from a5_core import ProgramRegistry,ProgramSpec

REGISTRY=ProgramRegistry()

def add(pid,source,job,roles,out,validation="fixture",executable=False):
    current = pid.startswith("C") and pid[1:].isdigit()
    configured_run = "RECURSIVE_EPISODE" if current else "UNSPECIFIED"
    recursion_owner = "HOST_HF001" if current else "UNSPECIFIED"
    consequence_scope = "MATERIAL_RESULT_OR_SEARCH_DELTA" if current else "UNSPECIFIED"
    external_escape = "HOLDOUT_FOR_STRONGER_TERMINAL_CLAIM" if current else "UNSPECIFIED"
    REGISTRY.register(ProgramSpec(
        pid,source,job,tuple(roles.split(",")),(out,),validation,executable,
        configured_run,recursion_owner,consequence_scope,external_escape
    ))

def _mark_executable(pid):
    REGISTRY._items[pid]=replace(REGISTRY.get(pid),executable=True)

add("C01","CAPABILITY_REGISTRY_V4_IC022","Task and Object Typing","K,S,O,C","typed_task_context")
add("C02","CAPABILITY_REGISTRY_V4_IC022","Referent Continuity","K,S,O,C","identity_relation")
add("C03","CAPABILITY_REGISTRY_V4_IC022","History Supersession","K,S,O,C","lineage")
add("C04","CAPABILITY_REGISTRY_V4_IC022","Source Result Freeze","K,S,C","frozen_source")
add("C05","CAPABILITY_REGISTRY_V4_IC022","Target Job Freeze","K,S,C","target_contract")
add("C06","CAPABILITY_REGISTRY_V4_IC022","External Dependence","K,S,O,C","dependency_map")
add("C07","CAPABILITY_REGISTRY_V4_IC022","Hidden Dependency","S,O,G","dependency_edges")
add("C08","CAPABILITY_REGISTRY_V4_IC022","Dependency Spine","S,O","dependency_spines")
add("C09","CAPABILITY_REGISTRY_V4_IC022","Layer Control Mapping","S,O,M","typed_graph")
add("C10","CAPABILITY_REGISTRY_V4_IC022","Representation Attack","K,O,M,C","representation_residual")
add("C11","CAPABILITY_REGISTRY_V4_IC022","Result Sensitivity","K,O,M,C","sensitive_support")
add("C12","CAPABILITY_REGISTRY_V4_IC022","Invariant Localization","K,O,M,C","invariant_core")
add("C13","CAPABILITY_REGISTRY_V4_IC022","Attribution Separation","K,S,O,C","attributed_chain")
add("C14","CAPABILITY_REGISTRY_V4_IC022","Hostile Review","K,O,M,C,R","defect_record")
add("C15","CAPABILITY_REGISTRY_V4_IC022","Novelty Comparator","K,S,O,C","collision_residual")
add("C16","CAPABILITY_REGISTRY_V4_IC022","Change Frontier","K,S,O,C,R","change_frontier")
add("C17","CAPABILITY_REGISTRY_V4_IC022","Failure Diagnosis","K,S,O,M,C","mechanism_disposition")
add("C18","CAPABILITY_REGISTRY_V4_IC022","Root Cause Escalation","K,S,O,R","root_disposition")
add("C19","CAPABILITY_REGISTRY_V4_IC022","Recursive Discovery","K,S,O,G,M,R","discovery_trace")
add("C20","CAPABILITY_REGISTRY_V4_IC022","Rival Reconstruction","K,S,O,G,M","rivals")
add("C21","CAPABILITY_REGISTRY_V4_IC022","Successor Generation","K,S,O,G,R","candidates")
add("C22","CAPABILITY_REGISTRY_V4_IC022","Improvement Frontier","K,S,O,R","improvement_frontier")
add("C23","CAPABILITY_REGISTRY_V4_IC022","Source Target Relation","K,S,O,C","typed_relation")
add("C24","CAPABILITY_REGISTRY_V4_IC022","Defect Repair","K,S,O,G,C,U","repaired_candidate")
add("C25","CAPABILITY_REGISTRY_V4_IC022","Behavior Compression","K,S,O,M,C","equivalent_candidate")
add("C26","CAPABILITY_REGISTRY_V4_IC022","System Architecture Improvement","K,S,O,G,M,C,R,U","architecture_successor")
add("C27","CAPABILITY_REGISTRY_V4_IC022","Subsystem Improvement","K,S,O,G,C,U","subsystem_successor")
add("C28","CAPABILITY_REGISTRY_V4_IC022","Component Improvement","K,S,O,G,C,U","component_successor")
add("C29","CAPABILITY_REGISTRY_V4_IC022","Interface Improvement","K,S,O,G,M,C,U","interface_successor")
add("C30","CAPABILITY_REGISTRY_V4_IC022","Boundary Redesign","K,S,O,G,M,C,U","boundary_successor")
add("C31","CAPABILITY_REGISTRY_V4_IC022","Cross Layer Improvement","K,S,O,G,M,C,R,U","synchronized_architecture")
add("C32","CAPABILITY_REGISTRY_V4_IC022","Leverage Routing","K,S,O,R","routes")
add("C33","CAPABILITY_REGISTRY_V4_IC022","Strict Gain","K,S,O,C","gain_disposition")
add("C34","CAPABILITY_REGISTRY_V4_IC022","Regression Check","K,S,O,C","regression_disposition")
add("C35","CAPABILITY_REGISTRY_V4_IC022","Incomparable Successors","K,S,O,C,R","nondominated_set")
add("C36","CAPABILITY_REGISTRY_V4_IC022","Recompute Architecture","K,S,O,R,U","affected_update")
add("C37","CAPABILITY_REGISTRY_V4_IC022","Transfer Provenance","K,S,O,C","provenance_chain")
add("C38","CAPABILITY_REGISTRY_V4_IC022","Transfer License","K,S,C","license_disposition")
add("C39","CAPABILITY_REGISTRY_V4_IC022","Target Effect","K,S,O,C","target_effect")
add("C40","CAPABILITY_REGISTRY_V4_IC022","Existing Coverage","K,S,O,C","coverage")
add("C41","CAPABILITY_REGISTRY_V4_IC022","Downstream Rescue","K,S,O,C","rescue_disposition")
add("C42","CAPABILITY_REGISTRY_V4_IC022","Transfer Disposition","K,S,C","transfer_status")
add("C43","CAPABILITY_REGISTRY_V4_IC022","Consequence Handoff","K,S,C,U","handoff")
add("C44","CAPABILITY_REGISTRY_V4_IC022","Regression Verification","K,S,O,C","verification")
add("C45","CAPABILITY_REGISTRY_V4_IC022","Holdout","K,S,O,C","holdout_result")
add("C46","CAPABILITY_REGISTRY_V4_IC022","Ablation","K,S,O,M,C","causal_effect")
add("C47","CAPABILITY_REGISTRY_V4_IC022","Relative Closure","K,S,O,R,C","closure_disposition")
add("C48","CAPABILITY_REGISTRY_V4_IC022","Raise Ceiling","K,S,O,G,M,C,R","strict_gain_or_failure")
add("C49","CAPABILITY_REGISTRY_V4_IC022","Corpus Navigation","K,S,O,G,R","navigation_trace")
add("CAP-001","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-002","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-003","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-004","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-005","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-006","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-007","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-008","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-009","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-010","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-011","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-012","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-013","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-014","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-015","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-016","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-017","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-018","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-019","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-020","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-021","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-022","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-023","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-024","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-025","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-026","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-027","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-028","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-029","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-030","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-031","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-032","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")
add("CAP-033","HISTORICAL_CAPABILITY_RECOVERY_LEDGER","historical protected behavior","K,S,O,G,M,C,R,U","reconstruction_witness")

EXPECTED_C={f"C{i:02d}" for i in range(1,50)}
EXPECTED_CAP={f"CAP-{i:03d}" for i in range(1,34)}


def _sequence(value):
    return value if isinstance(value, (list, tuple)) else None


def _rows(value):
    rows = _sequence(value)
    return rows if rows is not None and all(isinstance(row, dict) for row in rows) else None


def _label_set(value):
    if not isinstance(value, (list, tuple, set, frozenset)):
        return None
    try:
        return set(value)
    except TypeError:
        return None


def _same_result(left, right):
    """Type-sensitive structural equality; mapping insertion order is not evidence."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same_result(left[k], right[k]) for k in left)
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(_same_result(a, b) for a, b in zip(left, right))
    return left == right


# Shared executable ORIENT-family adapters.
def run_orient(program_id, payload):
    if program_id=="C01":
        kinds=_sequence(payload.get("admissible_typings"))
        if kinds and len(kinds)==1 and kinds[0]: return {"status":"ACCEPT","typed_task_context":kinds[0]}
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
        unresolved=[x for x in nodes if type(x.get("authoritative")) is not bool or not x.get("id")]
        if len(auth)==1 and not unresolved:
            return {"status":"ACCEPT","current":auth[0]["id"]}
        return {"status":"OPEN","authoritative_candidates":[x.get("id") for x in auth],"unresolved":unresolved}
    if program_id=="C04":
        if not payload.get("source_id") or "claim" not in payload:
            return {"status":"OPEN","frozen_source_packet":None}
        return {"status":"ACCEPT","frozen_source_packet":deepcopy({"source_id":payload["source_id"],"claim":payload["claim"]})}
    if program_id=="C05":
        protected=_sequence(payload.get("protected"))
        if not payload.get("target") or protected is None:
            return {"status":"OPEN","frozen_target_contract":None}
        return {"status":"ACCEPT","frozen_target_contract":deepcopy({"target":payload["target"],"protected":tuple(protected)})}
    if program_id=="C06":
        deps=_rows(payload.get("dependencies"))
        return {"status":"ACCEPT" if deps is not None and all(d.get("availability") is not None for d in deps) else "OPEN","external_dependency_map":deps}
    raise KeyError(program_id)

for _pid in ("C01","C02","C03","C04","C05","C06"):
    _mark_executable(_pid)


def run_map(program_id, payload):
    if program_id == "C07":
        candidates = _rows(payload.get("candidate_edges"))
        if candidates is None:
            return {"status":"OPEN","typed_dependency_edges":[]}
        edges = [e for e in candidates if e.get("material") is True]
        unresolved = [e for e in candidates if type(e.get("material")) is not bool]
        return {"status":"OPEN" if unresolved else ("ACCEPT" if edges else "NOOP"),"typed_dependency_edges":edges,**({"unresolved":unresolved} if unresolved else {})}
    if program_id == "C08":
        spines = _sequence(payload.get("spines"))
        return {"status": "ACCEPT" if spines else "OPEN", "plural_dependency_spines": spines}
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
        invariant = all(_same_result(reps[0]["result"], row["result"]) for row in reps[1:])
        return {"status":"ACCEPT","invariant":invariant,"representation_residual":[] if invariant else reps}
    if program_id == "C11":
        coordinates = _rows(payload.get("coordinates"))
        if coordinates is None:
            return {"status":"OPEN","minimal_sensitive_supports":[]}
        sensitive = [x["id"] for x in coordinates if x.get("changed_result") is True and x.get("id")]
        unresolved = [x for x in coordinates if type(x.get("changed_result")) is not bool or not x.get("id")]
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
            if row.get("task_relevant") is True and row.get("id") and row["id"] not in relevant:
                relevant.append(row["id"])
        unresolved = [x for x in visited if type(x.get("task_relevant")) is not bool or not x.get("id")]
        return {"status":"OPEN" if unresolved else "ACCEPT","navigation_trace":visited,"exact_object_set":relevant,**({"unresolved":unresolved} if unresolved else {})}
    raise KeyError(program_id)

for _pid in ("C07","C08","C09","C10","C11","C12","C13","C49"):
    _mark_executable(_pid)


def run_attack(program_id, payload):
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
        diagnosed=[x for x in failures if identified(x)]
        unresolved=[x for x in failures if not identified(x)]
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
        if _label_set(seeds) is None or any(
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

for _pid in ("C14","C15","C16","C17","C18","C19"):
    _mark_executable(_pid)


# Generic binding for the remaining typed capability contracts.
# These bindings validate or relay supplied evidence. ACCEPT is a bounded native
# result, not proof of independent semantic work, authorization, or HF2 closure.
def run_generic(program_id, payload):
    if program_id in {"C20","C21","C22","C23"}:
        key={"C20":"rivals","C21":"candidates","C22":"improvement_frontier","C23":"typed_relation"}[program_id]
        value=payload.get(key)
        return {"status":"ACCEPT" if value else "OPEN",key:value}
    if program_id in {"C24","C25","C26","C27","C28","C29","C30","C31"}:
        key=REGISTRY.get(program_id).protected_outputs[0]
        value=payload.get(key,payload.get("candidate"))
        protected=_label_set(payload.get("protected"))
        preserves=_label_set(payload.get("preserves"))
        consistent=key not in payload or "candidate" not in payload or _same_result(value,payload["candidate"])
        ok=bool(value) and consistent and protected is not None and preserves is not None and protected<=preserves
        return {"status":"ACCEPT" if ok else "OPEN",key:value if ok else None}
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
        ok=payload["protected_before"]==payload["protected_after"]
        return {"status":"ACCEPT" if ok else "FAIL","regression_disposition":"PASS" if ok else "REGRESSION"}
    if program_id=="C35":
        frontier=_sequence(payload.get("nondominated_set"))
        if frontier is None:
            return {"status":"OPEN","nondominated_set":None,"unresolved_candidates":payload.get("candidates")}
        return {"status":"ACCEPT","nondominated_set":frontier}
    if program_id in {"C36","C37","C38","C39","C40","C41","C42","C43"}:
        key=REGISTRY.get(program_id).protected_outputs[0]
        value=payload.get(key)
        return {"status":"ACCEPT" if value is not None else "OPEN",key:value}
    if program_id=="C44":
        if any(key not in payload for key in ("expected","actual")):
            return {"status":"OPEN","verification":"UNESTABLISHED"}
        ok=payload["expected"]==payload["actual"]
        return {"status":"ACCEPT" if ok else "FAIL","verification":"PASS" if ok else "FAIL"}
    if program_id=="C45":
        if any(type(payload.get(key)) is not bool for key in ("preregistered","pass")):
            return {"status":"OPEN","holdout_result":"UNESTABLISHED"}
        ok=payload["preregistered"] and payload["pass"]
        return {"status":"ACCEPT" if ok else "FAIL","holdout_result":"PASS" if ok else "FAIL"}
    if program_id=="C46":
        if any(key not in payload for key in ("with_component","without_component")):
            return {"status":"OPEN","causal_effect":None}
        return {"status":"ACCEPT","causal_effect":payload["with_component"]!=payload["without_component"]}
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

for _pid in tuple(f"C{i:02d}" for i in range(20,49)):
    _mark_executable(_pid)
