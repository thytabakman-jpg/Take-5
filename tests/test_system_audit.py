from pathlib import Path
from system_audit import AUDIT_KERNEL,audit_audits,tr_quotient,Finding,run_audit

ROOT=Path(__file__).resolve().parents[1]

def test_audit_kernel_is_reduced_common_spine():
    assert AUDIT_KERNEL==("OBSERVE","DISTINGUISH","ROOT","QUOTIENT","VERIFY","REENTER")

def test_tr_quotient_collapses_same_generator():
    roots=tr_quotient([
        Finding("A","R","x","one"),
        Finding("B","R","y","two"),
        Finding("C","S","z","three",False),
    ])
    assert len(roots)==2
    r=[x for x in roots if x.root_class=="R"][0]
    assert r.codes==("A","B") and r.targets==("x","y") and r.blocking

def test_audit_of_audits_has_one_kernel_and_modules():
    x=audit_audits()
    assert x["kernel"]==AUDIT_KERNEL
    assert {"PD","ROOT_CAUSE","CURRENTNESS","TOOL_MATURITY","REGRESSION"}<=set(x["modules"])

def test_all_current_capabilities_have_configured_run_identity():
    receipt=run_audit(ROOT)
    assert not [f for f in receipt.raw if f.code=="CONFIGURED_RUN"]

def test_repository_whole_system_audit_closes():
    receipt=run_audit(ROOT)
    assert receipt.closed, receipt.roots
