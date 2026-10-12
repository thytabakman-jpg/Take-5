from tool_manifest import OVERRIDES
from tool_manifest_audit import audit_tool_identities
from tool_run_registry import CONFIGURED_RUNS


def test_portfolio_identity_audit_closes_current_finite_repertoire():
    audit=audit_tool_identities(CONFIGURED_RUNS,OVERRIDES)
    assert audit.status=="CLOSED_RELATIVE"
    assert "MT" in audit.explicit
    assert "ASSERT" in audit.explicit
    assert "HF001" in audit.explicit
    assert "ImprovementCore" in audit.explicit
    assert "ImprovementCore" not in audit.generic_only
    assert "GOAL" in audit.explicit
    assert "GOAL" not in audit.generic_only
    assert "MultiObject" in audit.explicit
    assert "MultiObject" not in audit.generic_only
    for recovered in ("GDOS","Discriminator","RTC","BiasPerturbation","Diagnosis"):
        assert recovered in audit.explicit
        assert recovered not in audit.generic_only
    for recovered in ("MTA","Architecture","PD","PDAudit"):
        assert recovered in audit.explicit
        assert recovered not in audit.generic_only
    assert audit.generic_only==()


def test_explicit_subset_can_close_relative():
    audit=audit_tool_identities(("MT","ASSERT","HF001"),OVERRIDES)
    assert audit.status=="CLOSED_RELATIVE"
    assert audit.generic_only==()


def test_manifest_audit_rejects_duplicate_identity_even_when_name_exists():
    out=audit_tool_identities(("MT","MT"),OVERRIDES)
    assert out.status=="OPEN"
    assert out.dispositions[1].status=="DUPLICATE_TOOL_ID_OPEN"
    assert "MT" in out.unresolved


def test_manifest_audit_rejects_missing_invalid_and_mismatched_explicit_manifest():
    from dataclasses import replace
    for manifest in (
        None,
        replace(OVERRIDES["MT"],tool_id="GOAL"),
        replace(OVERRIDES["MT"],native_semantics=""),
    ):
        out=audit_tool_identities(("MT",),{"MT":manifest})
        assert out.status=="OPEN"
        assert out.unresolved==("MT",)
        assert out.dispositions[0].status=="INVALID_MANIFEST_OPEN"
    missing=audit_tool_identities(("MT","NOT-REGISTERED"),OVERRIDES)
    assert missing.status=="OPEN"
    assert missing.generic_only==("NOT-REGISTERED",)
    blank=audit_tool_identities(("MT",""),OVERRIDES)
    assert blank.status=="OPEN"
    assert blank.dispositions[1].status=="INVALID_TOOL_ID_OPEN"


def test_manifest_audit_never_closes_empty_or_names_only_repertoire():
    assert audit_tool_identities((),OVERRIDES).status=="OPEN"
    status=audit_tool_identities(("MT",),{"MT"})
    assert status.status=="OPEN"
    assert status.dispositions[0].status=="UNVERIFIED_MEMBERSHIP_OPEN"
