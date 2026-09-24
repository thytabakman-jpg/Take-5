from a5_core import ProgramRegistry,ProgramSpec

REGISTRY=ProgramRegistry()

def add(pid,source,job,roles,out,validation="fixture",executable=False):
    REGISTRY.register(ProgramSpec(pid,source,job,tuple(roles.split(",")),(out,),validation,executable))

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


# Shared executable ORIENT-family adapters.
def run_orient(program_id, payload):
    if program_id=="C01":
        kinds=payload.get("admissible_typings",[])
        if len(kinds)==1: return {"status":"ACCEPT","typed_task_context":kinds[0]}
        if not kinds: return {"status":"OPEN","reason":"no admissible typing established"}
        return {"status":"OPEN","alternatives":kinds}
    if program_id=="C02":
        if payload.get("same_lineage") is True: return {"status":"ACCEPT","identity_relation":"SAME_REFERENT"}
        if payload.get("same_lineage") is False: return {"status":"ACCEPT","identity_relation":"DISTINCT_REFERENT"}
        return {"status":"OPEN","identity_relation":"UNRESOLVED"}
    if program_id=="C03":
        nodes=payload.get("versions",[])
        auth=[x for x in nodes if x.get("authoritative")]
        if len(auth)==1: return {"status":"ACCEPT","current":auth[0]["id"]}
        return {"status":"OPEN","authoritative_candidates":[x.get("id") for x in auth]}
    if program_id=="C04":
        return {"status":"ACCEPT","frozen_source_packet":{"source_id":payload["source_id"],"claim":payload["claim"]}}
    if program_id=="C05":
        return {"status":"ACCEPT","frozen_target_contract":{"target":payload["target"],"protected":tuple(payload.get("protected",[]))}}
    if program_id=="C06":
        deps=payload.get("dependencies",[])
        return {"status":"ACCEPT" if all("availability" in d for d in deps) else "OPEN","external_dependency_map":deps}
    raise KeyError(program_id)

for _pid in ("C01","C02","C03","C04","C05","C06"):
    _old=REGISTRY.get(_pid)
    REGISTRY._items[_pid]=ProgramSpec(_old.program_id,_old.source,_old.job,_old.required_roles,_old.protected_outputs,_old.validation_target,True)


def run_map(program_id, payload):
    if program_id == "C07":
        edges = [e for e in payload.get("candidate_edges", []) if e.get("material")]
        return {"status": "ACCEPT" if edges else "NOOP", "typed_dependency_edges": edges}
    if program_id == "C08":
        spines = payload.get("spines", [])
        return {"status": "ACCEPT" if spines else "OPEN", "plural_dependency_spines": spines}
    if program_id == "C09":
        edges = payload.get("edges", [])
        unresolved = [e for e in edges if not e.get("relation_type")]
        return {"status": "OPEN" if unresolved else "ACCEPT", "typed_layer_graph": edges}
    if program_id == "C10":
        reps = payload.get("representations", [])
        results = [repr(x.get("result")) for x in reps]
        invariant = bool(reps) and len(set(results)) <= 1
        return {"status": "ACCEPT" if reps else "OPEN", "invariant": invariant, "representation_residual": [] if invariant else reps}
    if program_id == "C11":
        sensitive = [x["id"] for x in payload.get("coordinates", []) if x.get("changed_result")]
        return {"status": "ACCEPT", "minimal_sensitive_supports": sensitive}
    if program_id == "C12":
        maps = payload.get("sensitivity_maps", [])
        if not maps:
            return {"status": "OPEN", "invariant_core": [], "residual": []}
        sets = [set(x) for x in maps]
        core = set.intersection(*sets)
        residual = set.union(*sets) - core
        return {"status": "ACCEPT", "invariant_core": sorted(core), "residual": sorted(residual)}
    if program_id == "C13":
        edges = payload.get("edges", [])
        unresolved = [e for e in edges if not e.get("attribution")]
        return {"status": "OPEN" if unresolved else "ACCEPT", "attributed_edge_chain": edges}
    if program_id == "C49":
        visited = payload.get("visited", [])
        relevant = [x.get("id") for x in visited if x.get("task_relevant")]
        return {"status": "ACCEPT", "navigation_trace": visited, "exact_object_set": relevant}
    raise KeyError(program_id)

for _pid in ("C07","C08","C09","C10","C11","C12","C13","C49"):
    _old = REGISTRY.get(_pid)
    REGISTRY._items[_pid] = ProgramSpec(_old.program_id, _old.source, _old.job, _old.required_roles, _old.protected_outputs, _old.validation_target, True)


def run_attack(program_id, payload):
    if program_id=="C14":
        findings=[x for x in payload.get("findings",[]) if x.get("material")]
        interactions=[x for x in payload.get("interaction_findings",[]) if x.get("material")]
        residual=findings+interactions
        return {"status":"ACCEPT" if residual else "NOOP","hostile_residuals":residual}
    if program_id=="C15":
        source=set(payload.get("source_effects",[])); target=set(payload.get("target_effects",[]))
        return {"status":"ACCEPT","covered":sorted(source & target),"novel_residual":sorted(target-source),"terminology_only":bool(payload.get("different_terms")) and target<=source}
    if program_id=="C16":
        protected=set(payload.get("protected",[]))
        candidates=payload.get("candidates",[])
        allowed=[x for x in candidates if protected<=set(x.get("preserves",[]))]
        return {"status":"ACCEPT" if allowed else "OPEN","change_frontier":allowed}
    if program_id=="C17":
        failures=[x for x in payload.get("failures",[]) if x.get("material",True)]
        diagnosed=[x for x in failures if x.get("mechanism")]
        unresolved=[x for x in failures if not x.get("mechanism")]
        return {"status":"OPEN" if unresolved else "ACCEPT","mechanism_dispositions":diagnosed,"unresolved":unresolved}
    if program_id=="C18":
        chain=payload.get("causal_chain",[])
        supported=[x for x in chain if x.get("evidence")]
        if not supported: return {"status":"OPEN","root_disposition":None}
        root=supported[-1]
        return {"status":"ACCEPT" if root.get("terminal") else "OPEN","root_disposition":root}
    if program_id=="C19":
        frontier=list(payload.get("seed_frontier",[])); seen=set(); trace=[]
        graph=payload.get("graph",{})
        while frontier:
            x=frontier.pop(0)
            if x in seen: continue
            seen.add(x); trace.append(x)
            for y in graph.get(x,[]):
                if y not in seen: frontier.append(y)
        return {"status":"ACCEPT","discovery_trace":trace,"discovered":sorted(seen)}
    raise KeyError(program_id)

for _pid in ("C14","C15","C16","C17","C18","C19"):
    _old=REGISTRY.get(_pid)
    REGISTRY._items[_pid]=ProgramSpec(_old.program_id,_old.source,_old.job,_old.required_roles,_old.protected_outputs,_old.validation_target,True)
