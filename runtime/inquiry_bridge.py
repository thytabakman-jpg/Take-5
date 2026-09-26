"""Inquiry bridge for the governing Improvement Core path.

This restores the IC-028 invariant that question generation and explicit
question-to-tool mapping occur before capability package selection.
"""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class InquiryQuestion:
    question_id:str
    issue:str
    obligations:tuple[str,...]
    source:str

@dataclass(frozen=True)
class InquiryBridgeResult:
    frontier:tuple[InquiryQuestion,...]
    question_tool_map:tuple[tuple[str,tuple[str,...]],...]
    unmapped:tuple[str,...]

def _coerce_question(item:Any, index:int)->InquiryQuestion:
    if isinstance(item, InquiryQuestion):
        return item
    if isinstance(item, dict):
        qid=str(item.get("question_id", item.get("id", f"q{index}")))
        issue=str(item.get("issue", item.get("text", qid)))
        obligations=tuple(str(x) for x in item.get("obligations", ()))
        return InquiryQuestion(qid,issue,obligations,"explicit")
    text=str(item)
    return InquiryQuestion(f"q{index}",text,(text,),"explicit")

def build_question_frontier(packet:dict)->tuple[InquiryQuestion,...]:
    explicit=packet.get("question_frontier")
    if explicit:
        return tuple(_coerce_question(x,i) for i,x in enumerate(explicit,1))

    obligations=tuple(str(x) for x in packet.get("obligations", ()))
    return tuple(
        InquiryQuestion(f"obligation:{i}",o,(o,),"obligation")
        for i,o in enumerate(obligations,1)
    )

def map_questions_to_tools(frontier, package_index):
    rows=[]
    unmapped=[]
    for q in frontier:
        tools=tuple(sorted(
            pid for pid,covers in package_index.items()
            if set(q.obligations) & set(covers)
        ))
        rows.append((q.question_id,tools))
        if not tools:
            unmapped.append(q.question_id)
    return tuple(rows),tuple(unmapped)

def prepare_inquiry(packet:dict, package_index)->InquiryBridgeResult:
    frontier=build_question_frontier(packet)
    qmap,unmapped=map_questions_to_tools(frontier,package_index)
    return InquiryBridgeResult(frontier,qmap,unmapped)
