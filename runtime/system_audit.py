"""Canonical whole-system audit for Take-5.

Minimal audit algebra:
Observe -> Distinguish -> Root -> Quotient -> Verify -> Reenter.

Existing audits are evidence-producing modules. This tool owns whole-system
coverage, TR-style compression, closure, and machine-readable findings.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from a5_programs import REGISTRY, EXPECTED_C
from capability_router import TRIGGER_TAGS

AUDIT_KERNEL=("OBSERVE","DISTINGUISH","ROOT","QUOTIENT","VERIFY","REENTER")

AUDIT_MODULES={
    "PD": frozenset({"distinction","result_sensitivity","representation"}),
    "ROOT_CAUSE": frozenset({"failure","mechanism","recurrence","root_generator"}),
    "CURRENTNESS": frozenset({"basis","material_delta","reverification"}),
    "TOOL_MATURITY": frozenset({"trigger","execution_binding","configured_run"}),
    "HOSTILE_REVIEW": frozenset({"adversarial_residual","interaction_failure"}),
    "REGRESSION": frozenset({"protected_behavior","fixture","holdout"}),
    "ARCHITECTURE": frozenset({"identity","ownership","placement","boundary"}),
}

@dataclass(frozen=True)
class Finding:
    code:str
    root_class:str
    target:str
    detail:str
    blocking:bool=True

@dataclass(frozen=True)
class RootFinding:
    root_class:str
    codes:tuple[str,...]
    targets:tuple[str,...]
    details:tuple[str,...]
    blocking:bool

@dataclass(frozen=True)
class AuditReceipt:
    kernel:tuple[str,...]
    modules:tuple[str,...]
    raw:tuple[Finding,...]
    roots:tuple[RootFinding,...]
    closed:bool

def tr_quotient(findings:Iterable[Finding])->tuple[RootFinding,...]:
    """Collapse behaviorally equivalent findings by defect-generating root class."""
    groups={}
    for f in findings:
        g=groups.setdefault(f.root_class,{"codes":set(),"targets":set(),"details":set(),"blocking":False})
        g["codes"].add(f.code); g["targets"].add(f.target); g["details"].add(f.detail)
        g["blocking"] = g["blocking"] or f.blocking
    return tuple(
        RootFinding(
            root,
            tuple(sorted(v["codes"])),
            tuple(sorted(v["targets"])),
            tuple(sorted(v["details"])),
            bool(v["blocking"]),
        )
        for root,v in sorted(groups.items())
    )

def audit_audits():
    """Return audit-module coverage and the common kernel without multiplying tools."""
    covered=set()
    overlap=set()
    for invs in AUDIT_MODULES.values():
        overlap |= covered & set(invs)
        covered |= set(invs)
    return {
        "kernel":AUDIT_KERNEL,
        "modules":tuple(sorted(AUDIT_MODULES)),
        "invariants":tuple(sorted(covered)),
        "overlap":tuple(sorted(overlap)),
        "policy":"modules produce evidence; canonical audit owns quotient, closure, and reentry",
    }

def _registry_findings():
    out=[]
    current={x for x in REGISTRY.ids() if x.startswith("C") and x[1:].isdigit()}
    if current != EXPECTED_C:
        out.append(Finding("REGISTRY_COVERAGE","CAPABILITY_IDENTITY_LOSS","runtime/a5_programs.py",
                           f"expected {len(EXPECTED_C)} current capabilities; found {len(current)}"))
    for pid in sorted(EXPECTED_C):
        if pid not in REGISTRY.ids():
            continue
        spec=REGISTRY.get(pid)
        if not spec.executable:
            out.append(Finding("EXECUTION_BINDING", "CONFIGURED_TOOL_IDENTITY_LOSS", pid,
                               "semantic capability is not runtime-bound"))
        if pid not in TRIGGER_TAGS:
            out.append(Finding("TRIGGER_CONTRACT","CONFIGURED_TOOL_IDENTITY_LOSS",pid,
                               "missing routing trigger contract"))
        if not spec.configured_run_complete():
            out.append(Finding("CONFIGURED_RUN","CONFIGURED_TOOL_IDENTITY_LOSS",pid,
                               "semantic capability survived but configured-run identity is incomplete"))
    return out

def _workflow_findings(root:Path):
    wfdir=root/".github"/"workflows"
    if not wfdir.exists():
        return [Finding("WORKFLOW_MISSING","EXECUTION_TRUTH_LOSS",str(wfdir),"workflow directory missing")]
    files=sorted([*wfdir.glob("*.yml"),*wfdir.glob("*.yaml")])
    texts={p:p.read_text(encoding="utf-8") for p in files}
    runtime_triggers=[p for p,t in texts.items() if "runtime/**" in t]
    out=[]
    if len(runtime_triggers)>1:
        out.append(Finding("WORKFLOW_AMPLIFICATION","TRANSITION_COST_AMPLIFICATION",".github/workflows",
                           f"{len(runtime_triggers)} workflows trigger on runtime changes"))
    if runtime_triggers:
        t=texts[runtime_triggers[0]]
        if "cancel-in-progress: true" not in t or "concurrency:" not in t:
            out.append(Finding("STALE_RUN_CANCELLATION","TRANSITION_COST_AMPLIFICATION",str(runtime_triggers[0]),
                               "runtime validation does not cancel obsolete runs"))
        if "system_audit.py" not in t:
            out.append(Finding("AUDIT_NOT_GATED","AUDIT_CLOSURE_GAP",str(runtime_triggers[0]),
                               "whole-system audit is not in the validation gate"))
    else:
        out.append(Finding("RUNTIME_VALIDATION_MISSING","EXECUTION_TRUTH_LOSS",".github/workflows",
                           "no workflow validates runtime changes"))
    return out

def _structural_findings(root:Path):
    out=[]
    required={
        "runtime/recursive_episode.py":"CONFIGURED_TOOL_IDENTITY_LOSS",
        "runtime/reflexive_currentness.py":"ARCHITECTURE_BASIS_EXTERNALIZATION",
        "runtime/evidence_ledger.py":"EVIDENCE_AUTHORITY_CONFLATION",
        "runtime/tool_maturity.py":"TOOL_CURRENTNESS_GAP",
        "tests/test_system_architecture_currentness.py":"ARCHITECTURE_BASIS_EXTERNALIZATION",
        "tests/test_all_capabilities_execute.py":"EXECUTION_TRUTH_LOSS",
    }
    for rel,root_class in required.items():
        if not (root/rel).exists():
            out.append(Finding("STRUCTURAL_GUARD_MISSING",root_class,rel,"required guard or regression witness missing"))
    return out

def run_audit(root="."):
    root=Path(root)
    raw=tuple(_registry_findings()+_workflow_findings(root)+_structural_findings(root))
    roots=tr_quotient(raw)
    closed=not any(x.blocking for x in roots)
    return AuditReceipt(AUDIT_KERNEL,tuple(sorted(AUDIT_MODULES)),raw,roots,closed)

def main():
    receipt=run_audit(Path(__file__).resolve().parents[1])
    print(f"AUDIT closed={receipt.closed} raw={len(receipt.raw)} roots={len(receipt.roots)}")
    for r in receipt.roots:
        print(f"{r.root_class}: codes={','.join(r.codes)} targets={','.join(r.targets)}")
    raise SystemExit(0 if receipt.closed else 1)

if __name__=="__main__":
    main()
