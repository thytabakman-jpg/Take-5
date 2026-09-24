#!/usr/bin/env python3
import json
from pathlib import Path

STATE=Path("runtime/state.json")\n# IC-026 execution trigger 001
OUT=Path("runtime/receipt.json")

def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"episode":0,"target":"TAKE5_FIXTURE","constraint":False,"repaired":False,"maps":[],"history":[]}

def verify(s):
    checks={
      "target_preserved":s["target"]=="TAKE5_FIXTURE",
      "constraint_recovered":s["constraint"] is True,
      "repair_applied":s["repaired"] is True,
      "state_persisted":s["episode"]>=1,
    }
    return {"checks":checks,"pass":all(checks.values())}

def worker(s,action,grant):
    n=dict(s); n["history"]=list(s["history"])
    if action=="recover_constraint":
        assert grant.get("representation")=="CHOOSE"
        n["constraint"]=True
    elif action=="repair":
        assert s["constraint"]
        n["repaired"]=True
    elif action=="capture_map":
        n["maps"]=list(s["maps"])+["fixture-map"]
    n["history"].append(action)
    return n

def run():
    s=load(); pre=dict(s); s["episode"]+=1
    trace=[]
    grant={"goal":"LOCKED","object":"LOCKED","representation":"CHOOSE"}
    for action in ["recover_constraint","repair","capture_map"]:
        before=dict(s); s=worker(s,action,grant)
        trace.append({"action":action,"before":before,"after":dict(s)})
    v=verify(s)
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(s,indent=2)+"\n")
    receipt={"pre":pre,"post":s,"trace":trace,"verification":v,"reentry":"TERMINATE" if v["pass"] else "RESELECT"}
    OUT.write_text(json.dumps(receipt,indent=2)+"\n")
    assert v["pass"]
    assert grant["goal"]=="LOCKED" and grant["object"]=="LOCKED"
    print("TAKE5_CLOSED_LOOP: PASS")

if __name__=="__main__": run()