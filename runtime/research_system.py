"""System architecture: interface, research process, research state, and history-based closure."""
from dataclasses import dataclass,field
from enum import Enum
from state_commit import CommitReceipt,StateRole,require_role

class ClaimStatus(str,Enum):
    PROPOSED="PROPOSED"; WORKING="WORKING"; SUPPORTED="SUPPORTED"; ADMITTED="ADMITTED"

@dataclass
class ResearchState:
    claims:dict=field(default_factory=dict)
    history:list=field(default_factory=list)
    discharged:set=field(default_factory=set)

    def record_claim(self,claim_id,status,evidence=(),*,commit_receipt:CommitReceipt|None=None):
        resolved=ClaimStatus(status)
        if resolved==ClaimStatus.ADMITTED:
            if commit_receipt is None:
                raise PermissionError("ADMITTED_CLAIM_REQUIRES_COMMIT_RECEIPT")
            require_role(commit_receipt,StateRole.RESEARCH_CONTROL)
            if not evidence:
                raise PermissionError("ADMITTED_CLAIM_REQUIRES_EVIDENCE")
        self.claims[claim_id]={"status":resolved,"evidence":tuple(evidence)}
        self.history.append(("CLAIM",claim_id,status))

    def discharge(self,work_id,*,commit_receipt:CommitReceipt):
        require_role(commit_receipt,StateRole.RESEARCH_CONTROL)
        self.discharged.add(work_id)
        self.history.append(("DISCHARGE",work_id))

def history_reconstructible(state):
    return all(e and isinstance(e,tuple) for e in state.history)

def history_workflow_faithful(state):
    admitted=[k for k,v in state.claims.items() if v["status"]==ClaimStatus.ADMITTED]
    return all(state.claims[k]["evidence"] for k in admitted)

def closure_certificate(state,generated_work,open_coordinates=()):
    from endogenous_work import closure_status,WorkStatus
    status=closure_status(generated_work,state.discharged,open_coordinates)
    return {"status":status,"HREC":history_reconstructible(state),"HWF":history_workflow_faithful(state),
            "closed":status==WorkStatus.CLOSED and history_reconstructible(state) and history_workflow_faithful(state)}
