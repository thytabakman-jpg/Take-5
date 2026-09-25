"""Question-frontier supervision for Jane.

Unknown epistemic relevance defaults to probe candidacy. Jane observes and
hands candidates to the active controller; she does not select episode actions.
"""
from dataclasses import dataclass, field

@dataclass
class QuestionFrontierWatch:
    stale_projects:list=field(default_factory=list)
    uncompiled_projects:list=field(default_factory=list)
    unresolved_handoffs:list=field(default_factory=list)
    order_questions:list=field(default_factory=list)
    transfer_candidates:list=field(default_factory=list)

def epistemic_alert(kind, detail, relevance="UNKNOWN"):
    disposition="PROBE_CANDIDATE" if relevance=="UNKNOWN" else "WORK_CANDIDATE"
    return {"kind":kind,"detail":detail,"relevance":relevance,"disposition":disposition}

def needs_operator(alert):
    return alert.get("disposition") in {"PROBE_CANDIDATE","WORK_CANDIDATE"}
