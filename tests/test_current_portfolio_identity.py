from current_portfolio_identity import audit_current_portfolio_identity
from tool_run_registry import CONFIGURED_RUNS

def test_every_current_configured_tool_has_reconstructible_current_identity():
    out=audit_current_portfolio_identity()
    assert out.status=="CLOSED_RELATIVE"
    assert out.failures==()
    assert out.checked==len(CONFIGURED_RUNS)


def test_current_identity_audit_rejects_registered_key_to_other_tool_spec(monkeypatch):
    from dataclasses import replace
    import current_portfolio_identity as owner
    spec=CONFIGURED_RUNS["MT"]
    monkeypatch.setattr(owner,"CONFIGURED_RUNS",{"MT":replace(spec,tool_id="GOAL")})
    out=owner.audit_current_portfolio_identity()
    assert out.status=="OPEN"
    assert out.checked==1
    assert "MT:CONFIGURED_IDENTITY_MISMATCH" in out.failures


def test_current_identity_audit_rejects_wrong_manifest_identity(monkeypatch):
    from dataclasses import replace
    import current_portfolio_identity as owner
    original=owner.manifest_for
    monkeypatch.setattr(owner,"CONFIGURED_RUNS",{"MT":CONFIGURED_RUNS["MT"]})
    monkeypatch.setattr(owner,"manifest_for",
        lambda name:replace(original(name),tool_id="GOAL"))
    out=owner.audit_current_portfolio_identity()
    assert out.status=="OPEN"
    assert "MT:MANIFEST_INCOMPLETE" in out.failures
