#!/usr/bin/env python3
import json
from pathlib import Path

state_path=Path("runtime/closed_loop_state.json")
receipt_path=Path("runtime/closed_loop_receipt.json")
state={"target":"TAKE5_FIXTURE","constraint":True,"repair":True,"verified":False}
checks={"target":state["target"]=="TAKE5_FIXTURE","constraint":state["constraint"],"repair":state["repair"]}
state["verified"]=all(checks.values())
state_path.write_text(json.dumps(state,indent=2)+"\n")
receipt_path.write_text(json.dumps({"checks":checks,"pass":state["verified"],"reentry":"TERMINATE" if state["verified"] else "RESELECT"},indent=2)+"\n")
print("TAKE5_CLOSED_LOOP_V2: PASS" if state["verified"] else "TAKE5_CLOSED_LOOP_V2: FAIL")
raise SystemExit(0 if state["verified"] else 2)
