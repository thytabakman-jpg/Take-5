"""Recovered native runtimes for formal objects whose mathematics existed before runtime promotion.

These functions are tool-specific. Domain semantics remain explicit callables where the
historical contract requires an environment/domain oracle. Missing semantic bindings fail
closed rather than being replaced by generic prose reasoning.
"""
from __future__ import annotations
from itertools import combinations
from typing import Any, Callable, Iterable, Mapping, Sequence

SUCCESS="RELATIVE_CLOSE"

def _call(fn,name):
    if not callable(fn):
        raise TypeError(name+"_CALLABLE_REQUIRED")
    return fn

def _provider(raw,required,name):
    if not isinstance(raw,Mapping):
        return {"status":"BLOCKED","blocker":name+"_INVALID_RETURN"}
    missing=[k for k in required if k not in raw]
    if missing:
        return {"status":"OPEN","blocker":name+"_OUTPUT_MISSING:"+",".join(missing),"result":dict(raw)}
    result=dict(raw)
    open_value=result.get("OPEN",result.get("Open",()))
    status="OPEN" if open_value else SUCCESS
    return {"status":status,"result":result}

def run_mta(target,shared_math,evidence,contract,*,generate_structural_hypotheses,select_analysis_package,reconstruct_protected_model):
    """MTA_sem=<GenerateStructuralHypotheses,SelectAnalysisPackage,ReconstructProtectedModel>."""
    hypotheses=_call(generate_structural_hypotheses,"MTA_GENERATOR")(target,shared_math,evidence,contract)
    package=_call(select_analysis_package,"MTA_SELECTOR")(target,hypotheses,shared_math,evidence,contract)
    raw=_call(reconstruct_protected_model,"MTA_RECONSTRUCTOR")(target,hypotheses,package,shared_math,evidence,contract)
    required=("Model","Findings","FactorBasis","Residual","MaterialDeltas","DiscoveryDeltas",
              "NewOrChangedObjects","Evidence","Coverage","VerificationObligations","OPEN")
    return _provider(raw,required,"MTA")

def run_architecture_analysis(architecture,contract,*,analyze_architecture):
    """AA_K(A) typed contract-relative architecture analysis."""
    raw=_call(analyze_architecture,"ARCHITECTURE_ANALYZER")(architecture,contract)
    required=("ArchClass","Violations","LocalizationFamilies","DependencyState","InteractionState",
              "TransformationFrontier","SuccessorFrontier","Coverage","OpenConflictBlocked","Provenance")
    out=_provider(raw,required,"ARCHITECTURE")
    if out.get("result") is not None:
        ocb=out["result"].get("OpenConflictBlocked")
        if ocb:
            out["status"]="OPEN"
    return out

def _quotient(cases,rho,approx):
    groups=[]
    for case in cases:
        value=rho(case)
        for g in groups:
            if approx(value,g["representative"]):
                g["cases"].append(case); break
        else:
            groups.append({"representative":value,"cases":[case]})
    return groups

def _min_sensitive(cases,rho,approx,representation):
    values=[tuple(representation(c)) for c in cases]
    if not values:
        return ()
    n=len(values[0])
    if any(len(v)!=n for v in values):
        raise ValueError("PD_REPRESENTATION_ARITY_DRIFT")
    sensitive=[]
    for size in range(1,n+1):
        for J in combinations(range(n),size):
            J=set(J)
            if any(set(prev).issubset(J) for prev in sensitive):
                continue
            outside=[k for k in range(n) if k not in J]
            found=False
            for i in range(len(cases)):
                for j in range(i+1,len(cases)):
                    if all(values[i][k]==values[j][k] for k in outside) and not approx(rho(cases[i]),rho(cases[j])):
                        found=True; break
                if found: break
            if found:
                sensitive.append(tuple(sorted(J)))
    return tuple(sensitive)

def run_pd(cases,*,rho,approx,representations):
    """PD identifies quotient-result-changing minimal sensitive coordinates."""
    cases=tuple(cases)
    rho=_call(rho,"PD_RHO"); approx=_call(approx,"PD_APPROX")
    if not isinstance(representations,Mapping) or not representations:
        return {"status":"OPEN","blocker":"PD_REPRESENTATION_REQUIRED"}
    groups=_quotient(cases,rho,approx)
    result={
        "result_classes":tuple(g["representative"] for g in groups),
        "fibers":tuple(tuple(g["cases"]) for g in groups),
        "minimal_sensitive":{name:_min_sensitive(cases,rho,approx,_call(fn,"PD_REPRESENTATION")) for name,fn in representations.items()},
        "OPEN":(),
    }
    return {"status":SUCCESS,"result":result}

def run_pd_audit(cases,*,rho,approx,representations,kappa_cases=None,kappa_representations=None):
    """PDAudit_1.1 result quotient, fibers, pair-difference relation and sensitivity."""
    base=run_pd(cases,rho=rho,approx=approx,representations=representations)
    if base["status"]!="RELATIVE_CLOSE":
        return base
    cases=tuple(cases)
    pairs=[]
    for i,a in enumerate(cases):
        for b in cases[i+1:]:
            if not approx(rho(a),rho(b)):
                pairs.append((a,b))
    result=dict(base["result"])
    result.update({
        "pair_difference_relation":tuple(pairs),
        "kappa_A":None if kappa_cases is None else kappa_cases(cases),
        "kappa_Lambda":None if kappa_representations is None else kappa_representations(representations),
        "raw_output_immutable":True,
        "normalized_separately":True,
    })
    return {"status":SUCCESS,"result":result}

def run_gdos(target,*,observe,protected_context=None):
    """Goal-decoupled observation: observe with solve/improve/optimize pressure suppressed."""
    raw=_call(observe,"GDOS_OBSERVER")(target,protected_context)
    if isinstance(raw,Mapping):
        forbidden={"mutation","mutations","selected_action","rewrite","solution"}
        leaked=sorted(k for k in forbidden if k in raw and raw[k])
        if leaked:
            return {"status":"BLOCKED","blocker":"GDOS_OPTIMIZATION_LEAK:"+",".join(leaked)}
        observations=raw.get("observations",raw)
    else:
        observations=raw
    return {"status":SUCCESS,"result":{"observations":observations,"optimization_pressure":"SUPPRESSED","mutation_performed":False}}

def run_discriminator(left_route,right_route,*,run_route,equivalent,classify_difference=None):
    """Compare two frozen routes under one protected result basis."""
    run_route=_call(run_route,"DISCRIMINATOR_RUNNER"); equivalent=_call(equivalent,"DISCRIMINATOR_EQUIVALENCE")
    left=run_route(left_route); right=run_route(right_route)
    lres=left.get("result",left) if isinstance(left,Mapping) else left
    rres=right.get("result",right) if isinstance(right,Mapping) else right
    if equivalent(lres,rres):
        ltrace=left.get("trace") if isinstance(left,Mapping) else None
        rtrace=right.get("trace") if isinstance(right,Mapping) else None
        cls="COMMUTES_RELATIVE" if ltrace==rtrace else "PATH_ONLY"
    else:
        if not callable(classify_difference):
            return {"status":"OPEN","blocker":"DISCRIMINATOR_DIRECTION_CLASSIFIER_REQUIRED",
                    "result":{"left":left,"right":right}}
        cls=str(classify_difference(left,right))
        if cls not in {"RESULT_ORDER_SENSITIVE","DIRECTIONALLY_DEPENDENT"}:
            return {"status":"BLOCKED","blocker":"DISCRIMINATOR_CLASS_INVALID:"+cls}
    return {"status":SUCCESS,"result":{"class":cls,"left":left,"right":right}}

def run_rtc(state,*,generators,admissible,preserve,strict_gain,dominates):
    """RTC nondominated strict-successor frontier under declared job/basis."""
    cand=[]
    for g in tuple(generators):
        raw=_call(g,"RTC_GENERATOR")(state)
        vals=raw if isinstance(raw,(list,tuple,set)) else (raw,)
        for x in vals:
            if admissible(state,x) and preserve(state,x) and strict_gain(state,x):
                cand.append(x)
    frontier=[]
    for x in cand:
        if not any(y is not x and dominates(y,x) for y in cand):
            frontier.append(x)
    return {"status":SUCCESS,"result":{"SuccessorCandidates":tuple(cand),"ResultFrontier":tuple(frontier),
                                       "maximality_claim":False,"OPEN":()}}

def run_bias_perturbation(variants,*,runner,protected_decision,causal_explanation=None):
    """Bias benchmark: task-irrelevant perturbation must not silently change protected decision."""
    if "BASELINE" not in variants:
        return {"status":"BLOCKED","blocker":"BIAS_BASELINE_REQUIRED"}
    runner=_call(runner,"BIAS_RUNNER"); protected_decision=_call(protected_decision,"BIAS_PROJECTION")
    results={name:runner(payload) for name,payload in variants.items()}
    base=protected_decision(results["BASELINE"])
    signals=[]
    for name,res in results.items():
        if name=="BASELINE": continue
        d=protected_decision(res)
        if d!=base:
            explained=bool(causal_explanation and causal_explanation(name,results["BASELINE"],res))
            if not explained:
                signals.append({"variant":name,"baseline":base,"decision":d,"status":"OPEN_UNEXPLAINED"})
    return {"status":"OPEN" if signals else SUCCESS,
            "result":{"results":results,"bias_signals":tuple(signals),"protected_baseline":base}}

def run_multi_object(objects,*,generate_relations,reconcile_relations):
    """MO_core^2=<G_rel^MO,C_rel^MO>."""
    objects=tuple(objects)
    generated=_call(generate_relations,"MULTIOBJECT_GENERATOR")(objects)
    raw=_call(reconcile_relations,"MULTIOBJECT_RECONCILER")(objects,generated)
    required=("RelationState","LowerOrderSynthesis","Reducibility","HigherOrderResidual","CONFLICT","OPEN")
    out=_provider(raw,required,"MULTIOBJECT")
    if out.get("result") and out["result"].get("CONFLICT"):
        out["status"]="CONFLICT"
    return out

def run_diagnosis(state,*,causal_support,root_selector):
    """Parameterized causal/root diagnosis; rho is an input and output may remain set-valued."""
    causal=tuple(_call(causal_support,"DIAGNOSIS_CAUSAL_SUPPORT")(state))
    roots=tuple(_call(root_selector,"DIAGNOSIS_ROOT_SELECTOR")(causal))
    if any(r not in causal for r in roots):
        return {"status":"BLOCKED","blocker":"DIAGNOSIS_ROOT_NOT_CAUSAL_CANDIDATE"}
    boundary=state.get("B",()) if isinstance(state,Mapping) else ()
    bset={str(x).upper() for x in boundary} if isinstance(boundary,(list,tuple,set)) else {str(boundary).upper()}
    if "BLOCKED" in bset: status="BLOCKED"; det="BLOCKED"
    elif "OPEN" in bset: status="OPEN"; det="OPEN"
    elif len(roots)==1: status=SUCCESS; det="UNIQUE"
    elif len(roots)>1: status=SUCCESS; det="SET_VALUED"
    else: status=SUCCESS; det="UNDERDETERMINED"
    return {"status":status,"result":{"CausalCandidates":causal,"Roots":roots,"DetState":det}}
