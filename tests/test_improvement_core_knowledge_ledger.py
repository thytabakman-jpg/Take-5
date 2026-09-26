import json
import sys
from pathlib import Path

sys.path.insert(0,"runtime")

from improvement_core_knowledge_ledger import KnowledgeLedger


def test_material_idea_survives_restart_with_provenance_and_dependencies(tmp_path):
    path=tmp_path/"knowledge.json"
    ledger=KnowledgeLedger.from_durable(path,autosave=True)
    node=ledger.record(
        kind="IDEA",
        statement="PD bare determinacy has the total-single-valued function skeleton.",
        basis_id="function-first",
        source_episode="chat-1",
        source_route="pd-discovery",
        related_objects=("PD","FUNCTION"),
        dependency_footprint=("PD_CORE","FUNCTION_TYPE"),
        evidence_refs=("reaserch:function-first-pd",),
        disposition="CAPTURED",
    )
    assert path.exists()

    reloaded=KnowledgeLedger.from_durable(path,autosave=False)
    again=reloaded.nodes[node.knowledge_id]
    assert again.statement.startswith("PD bare determinacy")
    assert set(again.related_objects)=={"PD","FUNCTION"}
    assert set(again.dependency_footprint)=={"PD_CORE","FUNCTION_TYPE"}
    assert again.provenance[0]["source_episode"]=="chat-1"


def test_repeated_capture_integrates_without_duplicate_node_and_keeps_history(tmp_path):
    path=tmp_path/"knowledge.json"
    ledger=KnowledgeLedger.from_durable(path,autosave=True)
    kwargs=dict(
        kind="DISTINCTION",
        statement="Configured identity and runtime realization are different layers.",
        basis_id="take5",
        source_episode="episode-a",
    )
    first=ledger.record(**kwargs,evidence_refs=("a",))
    second=ledger.record(
        **(kwargs|{"source_episode":"episode-b"}),
        disposition="ADMITTED",
        evidence_refs=("b",),
    )
    assert first.knowledge_id==second.knowledge_id
    assert len(ledger.nodes)==1
    assert len(ledger.history)==2
    assert ledger.nodes[first.knowledge_id].disposition=="ADMITTED"
    assert set(ledger.nodes[first.knowledge_id].evidence_refs)=={"a","b"}
    assert len(ledger.nodes[first.knowledge_id].provenance)==2


def test_supersession_never_deletes_historical_capture(tmp_path):
    path=tmp_path/"knowledge.json"
    ledger=KnowledgeLedger.from_durable(path,autosave=False)
    node=ledger.record(
        kind="IDEA",
        statement="candidate idea",
        basis_id="b",
        source_episode="e1",
    )
    ledger.record(
        kind="IDEA",
        statement="candidate idea",
        basis_id="b",
        source_episode="e2",
        disposition="SUPERSEDED",
    )
    assert node.knowledge_id in ledger.nodes
    assert ledger.nodes[node.knowledge_id].disposition=="SUPERSEDED"
    assert [x.action for x in ledger.history]==["CAPTURE","INTEGRATE"]


def test_explicit_event_and_material_trace_use_same_durable_spine(tmp_path):
    ledger=KnowledgeLedger.from_durable(tmp_path/"knowledge.json",autosave=False)
    explicit=ledger.record_explicit_event({
        "kind":"RELATION",
        "statement":"A depends on B",
        "basis_id":"b",
        "related_objects":["A","B"],
        "dependency_footprint":["B"],
    },fallback_basis="fallback",source_episode="episode")
    material=ledger.capture_material_trace({
        "iteration":1,
        "selected_job":{"id":"job-1","route_id":"route-1","dependency_footprint":["A"]},
        "delta":{"open_refinement":"new distinction","evidence_refs":["receipt-1"]},
        "progress_effects":["MATERIAL_DISTINCTION_DISCOVERED"],
    },fallback_basis="b",source_episode="episode")
    assert explicit.knowledge_id in ledger.nodes
    assert material is not None
    assert material.knowledge_id in ledger.nodes
    assert len(ledger.nodes)==2


def test_unresolved_exposes_captured_open_blocked_conflict_only(tmp_path):
    ledger=KnowledgeLedger.from_durable(tmp_path/"knowledge.json",autosave=False)
    ids={}
    for disposition in ("CAPTURED","OPEN","BLOCKED","CONFLICT","ADMITTED","REJECTED","SUPERSEDED","CURRENT"):
        node=ledger.record(
            kind="OTHER",statement=f"s-{disposition}",basis_id="b",
            source_episode="e",disposition=disposition,
        )
        ids[disposition]=node.knowledge_id
    unresolved=set(ledger.unresolved())
    assert unresolved=={ids[x] for x in ("CAPTURED","OPEN","BLOCKED","CONFLICT")}
