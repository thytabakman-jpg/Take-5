#!/usr/bin/env python3
from runtime.icc118_favored_successor_candidate import (
    Action,Reality,Residual,completion,live,nondominated,reality_status,PROTECTED_BEHAVIORS
)

def run():
    assert reality_status(Reality(True,False,True))=="RUNTIME_BLOCKED"
    assert reality_status(Reality(False,True,True))=="SEMANTIC_UNAVAILABLE"
    assert reality_status(Reality(True,True,False))=="AUTHORITY_BLOCKED"
    assert reality_status(Reality(True,True,True))=="EXECUTABLE"

    cheap=Action("cheap",1.0,1.0,1.0,1.0)
    broad=Action("broad",1.0,1.0,1.0,5.0)
    assert [x.action_id for x in nondominated((cheap,broad))]==["cheap"]

    a=Action("a",1.0,1.0,0.6,1.0)
    b=Action("b",0.7,0.7,1.0,0.5)
    assert {x.action_id for x in nondominated((a,b))}=={"a","b"}

    r=Residual("live",False,("probe",))
    assert live(r) and not completion(True,(r,))

    ext=Residual(
        "runner",False,(),
        "EXTERNAL_CONTROL",True,("runner_admission_changes",)
    )
    assert not live(ext)
    assert completion(True,(ext,))

    uncert=Residual("unknown",False,(),"EVIDENCE_EXHAUSTED",False,())
    assert live(uncert)
    assert not completion(True,(uncert,))

    required={
      "REALITY_TRIAD_SEPARATION","STATE_RELATIVE_WORK_SELECTION",
      "STRUCTURAL_STEWARDSHIP_AND_OWNER_SEPARATION",
      "NO_PREMATURE_UNRESOLVED_RELEASE","EXECUTION_TRUTH",
      "USER_DOES_NOT_SCRIPT_INTERNAL_TOOL_SEQUENCE"
    }
    assert required <= set(PROTECTED_BEHAVIORS)
    print("ICC118 favored successor candidate: PASS (12/12)")

if __name__=="__main__":run()
