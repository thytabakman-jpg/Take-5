import sys
sys.path.insert(0,"runtime")

from hashlib import sha256
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from improvement_core_external_acquisition import (
    ExternalDisposition,
    decide_external_acquisition,
    acquire_external,
)
from improvement_core_regime import run_improvement_core_regime
from ic028_operator import GOAL_DIRECTED_STAGES


def _handlers(seen=None):
    seen=seen if seen is not None else []
    handlers={}
    for stage in GOAL_DIRECTED_STAGES:
        def fn(state,stage=stage):
            seen.append((stage,state))
            return {
                "state":{**state,stage:True},
                "material_delta":stage=="EXECUTE",
                "supervisory_relevant":False,
            }
        handlers[stage]=fn
    handlers["REENTER"]=lambda state: {"state":state,"terminal":True}
    return handlers


def _zip(entries):
    buf=BytesIO()
    with ZipFile(buf,"w",ZIP_DEFLATED) as zf:
        for name,payload in entries:
            zf.writestr(name,payload)
    return buf.getvalue()


def _bound_zip_output(data, *, expected_sha=None, generators=None):
    return {
        "external_need_satisfied":True,
        "artifact_kind":"BOUND_ZIP",
        "artifact_ref":{
            "repository":"thytabakman-jpg/Take-5",
            "object_class":"actions_artifact",
            "stable_id":"10901131588",
            "source_ref":"workflow_run:36226293888",
            "observed_name":"take5-validation-receipts",
            "expected_byte_count":len(data),
            "expected_sha256":expected_sha or sha256(data).hexdigest(),
            "observed_at":"2026-09-26T18:41:00-04:00",
        },
        "archive_bytes":data,
        "artifact_generators":generators or {},
    }


def test_external_not_needed_without_signal():
    d=decide_external_acquisition({},available=("web_search",))
    assert d.disposition==ExternalDisposition.NOT_NEEDED


def test_external_gap_is_legal_when_needed_but_unavailable():
    d=decide_external_acquisition(
        {"external_dependency":True},
        available=(),
        allow_gap=True,
    )
    assert d.disposition==ExternalDisposition.OPEN_GAP
    assert d.allow_internal_fallback is False


def test_external_adapter_is_selected_before_internal_work():
    called=[]
    def web(state):
        called.append(True)
        return {
            "external_need_satisfied":True,
            "evidence":["fresh source"],
        }
    r=acquire_external(
        {"currentness_unknown":True},
        {"web_search":web},
    )
    assert r.decision.disposition==ExternalDisposition.ACQUIRE
    assert r.used==("web_search",)
    assert called==[True]


def test_regime_cannot_close_over_unavailable_required_outside_evidence():
    out=run_improvement_core_regime(
        "ImproveCore solve it",
        target="x",
        job="solve",
        basis="current",
        state={"external_dependency":True},
        handlers=_handlers(),
        external_adapters={},
    )
    assert out.status=="OPEN"
    assert out.blocker=="EXTERNAL_ACQUISITION_GAP"
    assert out.external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP


def test_external_evidence_enters_state_before_manager_stages():
    seen=[]
    def web(state):
        return {
            "external_need_satisfied":True,
            "source":"web",
            "fact":"fresh",
        }
    out=run_improvement_core_regime(
        "ImproveCore solve it",
        target="x",
        job="solve",
        basis="current",
        state={"currentness_unknown":True},
        handlers=_handlers(seen),
        external_adapters={"web_search":web},
    )
    assert out.status=="COMPLETE"
    assert out.external_receipt.used==("web_search",)
    first_state=seen[0][1]
    assert first_state["external_evidence"][0]["fact"]=="fresh"


def test_bound_zip_external_output_crosses_archive_and_artifact_intake_before_manager():
    seen=[]
    data=_zip([("events.jsonl",b'{"event":"ok"}\n')])

    def generator(artifact):
        return [{
            "candidate_id":"event-ok",
            "candidate_type":"STATUS_OR_AUTHORITY_CHANGE",
            "source_span":"line:1",
            "load_bearing":True,
        }]

    def repository(state):
        return _bound_zip_output(data,generators={"events":generator})

    out=run_improvement_core_regime(
        "ImproveCore use exact external evidence",
        target="external-evidence",
        job="consume bound archive",
        basis="bound-zip-runtime-test",
        state={"external_dependency":True},
        handlers=_handlers(seen),
        external_adapters={"repository_research":repository},
    )

    assert out.status=="COMPLETE"
    assert out.external_receipt.decision.disposition==ExternalDisposition.ACQUIRE
    first_state=seen[0][1]
    assert len(first_state["external_artifacts"])==1
    assert first_state["external_artifacts"][0].content=='{"event":"ok"}\n'
    assert len(first_state["external_archive_receipts"])==1
    receipt=first_state["external_archive_receipts"][0]
    assert receipt["archive_traversal_complete"] is True
    assert receipt["archive_declared_members"]==1
    assert len(receipt["artifact_traversal_receipts"])==1
    assert len(first_state["obligations"])==1
    assert first_state["obligations"][0].work_id=="artifact-intake:event-ok"

    evidence=first_state["external_evidence"][0]
    assert evidence["bound_zip_processed"] is True
    assert "archive_bytes" not in evidence
    assert "artifact_generators" not in evidence
    assert "artifact_ref" not in evidence


def test_bound_zip_binding_failure_turns_external_need_into_open_gap():
    data=_zip([("a.txt",b"a")])

    def repository(state):
        return _bound_zip_output(data,expected_sha="0"*64)

    out=run_improvement_core_regime(
        "ImproveCore use exact external evidence",
        target="external-evidence",
        job="consume bound archive",
        basis="bound-zip-runtime-test",
        state={"external_dependency":True},
        handlers=_handlers(),
        external_adapters={"repository_research":repository},
    )

    assert out.status=="OPEN"
    assert out.blocker=="EXTERNAL_ACQUISITION_GAP"
    assert out.external_receipt.decision.disposition==ExternalDisposition.OPEN_GAP
    assert any("BOUND_ZIP_BINDING" in x for x in out.external_receipt.unresolved)
    evidence=out.result.state["external_evidence"][0]
    assert evidence["status"]=="BLOCKED"
    assert "archive_bytes" not in evidence
