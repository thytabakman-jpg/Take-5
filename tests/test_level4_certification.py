"""Adversarial acceptance tests for a Level 4 claim/repair receipt."""
import sys
from copy import deepcopy
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from level4_certification import assess_level4, level4_required_for_request
from improvement_core_return_gate import evaluate_parent_return


def valid_packet():
    return {
        "target_ref": "project/node/file.md",
        "authority_ref": "project/node/README.md",
        "purpose": "Check scientific knowledge and its applicable claims.",
        "purpose_verified": True,
        "reviewer_ref": "source-specific specialist",
        "evidence_refs": ["project:source:scope"],
        "claim_inventory_verified": True,
        "inspection_refs": ["review:claim-and-defect-census"],
        "requirements": [{"id": "GOAL", "applicable": True, "status": "PASS", "evidence_refs": ["review:goal"]}],
        "claims": [
            {"id": "CLAIM", "kind": "FACTUAL_ASSERTION",
             "baseline_kind": "FACTUAL_ASSERTION", "text": "Scoped theorem T.",
             "disposition": "SUBSTANTIATED", "evidence_refs": ["owner:proof-T"]},
            {"id": "OPEN1", "kind": "OPEN_RESEARCH_QUESTION",
             "baseline_kind": "OPEN_RESEARCH_QUESTION", "text": "Does T extend to other systems?",
             "asserted_as_fact": False},
        ],
        "dependencies": [{"id": "D1", "owner_ref": "mathematics/current.md",
                          "status": "VERIFIED", "evidence_refs": ["math:proof"]}],
        "defects": [],
        "reverified": True,
        "reverification_refs": ["run:recheck-after-review"],
    }


def check_bad(mutator, marker):
    p = valid_packet()
    mutator(p)
    status, issues = assess_level4(p)
    assert status == "INCOMPLETE"
    assert any(marker in x for x in issues), issues


def test_honest_open_research_is_compatible_with_level4():
    assert assess_level4(valid_packet()) == ("PASS", ())


def test_unsupported_fact_blocks_even_when_declared_pass():
    check_bad(lambda p: p["claims"][0].update(evidence_refs=[], disposition="OPEN"), "UNRESOLVED_FACT")


def test_factual_claim_cannot_be_silently_reclassified_open():
    def defect(p):
        p["claims"][0].update(kind="OPEN_RESEARCH_QUESTION", asserted_as_fact=False,
                              text="Could theorem T hold?", baseline_kind="FACTUAL_ASSERTION")
    check_bad(defect, "FACT_RELABELED_OPEN")


def test_open_question_that_asserts_its_answer_is_blocked():
    check_bad(lambda p: p["claims"][1].update(asserted_as_fact=True), "OPEN_ASSERTS_FACT")


def test_justified_correction_may_pass_with_original_goals_met():
    p = valid_packet()
    p["claims"][0].update(kind="OPEN_RESEARCH_QUESTION", asserted_as_fact=False,
                           text="Does T hold under weaker guards?", correction_verified=True,
                           correction_refs=["owner:correction"], prior_text="Scoped theorem T.")
    assert assess_level4(p) == ("PASS", ())


def test_corrected_factual_statement_must_have_evidence_and_recheck():
    p = valid_packet()
    p["claims"][0].update(disposition="CORRECTED", text="T holds only for finite models.",
                          prior_text="Scoped theorem T.", correction_verified=True,
                          correction_refs=["owner:edit"])
    assert assess_level4(p) == ("PASS", ())
    check_bad(lambda q: q["claims"][0].update(disposition="CORRECTED"), "UNVERIFIED_CORRECTION")


def test_unsatisfied_requirement_blocks():
    check_bad(lambda p: p["requirements"][0].update(status="INCOMPLETE"), "REQUIREMENT_UNSATISFIED")


def test_false_nonapplicability_needs_justification():
    check_bad(lambda p: p["requirements"][0].update(applicable=False), "REQUIREMENT_NOT_JUSTIFIED")


def test_unverified_dependency_blocks():
    check_bad(lambda p: p["dependencies"][0].update(status="OPEN"), "UNVERIFIED_DEPENDENCY")


def test_unresolved_defect_blocks_and_repair_without_recheck_also_blocks():
    check_bad(lambda p: p["defects"].append({"id": "broken-proof", "status": "OPEN"}), "UNRESOLVED_DEFECT")
    check_bad(lambda p: p["defects"].append({"id": "broken-proof", "status": "RESOLVED",
                                             "repair_refs": ["edit:fixed"]}), "UNRESOLVED_DEFECT")


def test_verified_repair_can_pass():
    p=valid_packet()
    p["defects"]=[{"id":"broken-proof","status":"RESOLVED","repair_refs":["commit:repair"],
                   "recheck_refs":["run:after-repair"]}]
    assert assess_level4(p) == ("PASS", ())


def test_missing_reverification_and_inventory_blocks():
    check_bad(lambda p: p.update(reverified=False), "NOT_VERIFIED_REVERIFIED")
    check_bad(lambda p: p.update(claim_inventory_verified=False), "NOT_VERIFIED_CLAIM_INVENTORY_VERIFIED")


def test_absent_packet_blocks_and_intent_helper():
    assert assess_level4(None)[0] == "INCOMPLETE"
    assert level4_required_for_request("Run a Level 4 on this file")
    assert level4_required_for_request("Level four certification")
    assert not level4_required_for_request("Explain the third level")


def _stable(state, memory, context):
    return {"status": "NO_GAIN", "owned_work_remaining": False,
            "evidence": [f"fresh:{context['challenge_index']}"],
            "challenge_id": f"fresh-{context['challenge_index']}"}


def _verifier(state, memory, context):
    return {"disposition": "RETURN", "terminal": "COMPLETE",
            "goal_closed": True, "owned_work_remaining": False,
            "consequence_closed": True, "evidence": ["review:goal-closed"]}


def _parent(state, required):
    return evaluate_parent_return(
        candidate_status="COMPLETE", candidate_blocker=None, state=state, memory={},
        context={"controller":"ImprovementCore","target":"x","job":"complete ordinary task",
                 "basis":"current","parent_round":0,"hf2_status":"RELATIVE_CLOSE",
                 "level4_certification_required":required},
        verifier=_verifier, fresh_reobserve=_stable,
    )


def test_parent_level4_fails_closed_without_packet():
    with pytest.raises(RuntimeError, match="WITHOUT_LEVEL4_CERTIFICATION"):
        _parent({"terminal": "COMPLETE"}, True)


def test_parent_level4_fails_closed_on_open_defect():
    p=valid_packet()
    p["defects"]=[{"id":"missing-proof","status":"OPEN"}]
    with pytest.raises(RuntimeError, match="INVALID_LEVEL4_CERTIFICATION"):
        _parent({"terminal":"COMPLETE","level4_certification_packets":[p]}, True)


def test_parent_level4_accepts_valid_packet():
    out=_parent({"terminal":"COMPLETE","level4_certification_packets":[valid_packet()]}, True)
    assert out.terminal=="COMPLETE"
    assert out.receipt["level4_certification_residuals"]==()


def test_non_level4_job_not_forced_to_supply_packet():
    assert _parent({"terminal":"COMPLETE"}, False).terminal=="COMPLETE"


def test_parent_detects_unflagged_level4_user_request():
    from improvement_core_return_gate import evaluate_parent_return
    with pytest.raises(RuntimeError, match="WITHOUT_LEVEL4_CERTIFICATION"):
        evaluate_parent_return(
            candidate_status="COMPLETE", candidate_blocker=None,
            state={"terminal":"COMPLETE"}, memory={},
            context={"controller":"ImprovementCore","target":"x",
                     "job":"Run Level 4 on the document", "basis":"current",
                     "parent_round":0,"hf2_status":"RELATIVE_CLOSE"},
            verifier=_verifier, fresh_reobserve=_stable,
        )
