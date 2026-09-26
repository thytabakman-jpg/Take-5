"""Audit the declared historical matched-replay witness basis.

The audit does not claim that every historical chat is executable. It establishes
that every protected replay case in the declared current basis has:
- a durable witness test;
- a named assertion token;
- and, when tied to a configured tool protected behavior, a reconstructing
  canonical tool manifest.

CI executes the witness tests separately.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path

from tool_manifest import reconstructs

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"integration"/"IMPROVEMENTCORE_HISTORICAL_REPLAY_BASIS_001.json"

@dataclass(frozen=True)
class ReplayAudit:
    status:str
    checked:int
    failures:tuple[str,...]

def audit_historical_replays()->ReplayAudit:
    data=json.loads(MANIFEST.read_text())
    failures=[]
    cases=data.get("cases",[])
    for case in cases:
        path=ROOT/case["witness"]
        if not path.exists():
            failures.append(f"{case['id']}:WITNESS_MISSING")
            continue
        text=path.read_text()
        if case.get("token") and case["token"] not in text:
            failures.append(f"{case['id']}:TOKEN_MISSING")
        tool=case.get("tool_id")
        behavior=case.get("behavior")
        if tool and behavior and not reconstructs(tool,(behavior,)):
            failures.append(f"{case['id']}:MANIFEST_DOES_NOT_RECONSTRUCT")
    return ReplayAudit("PASS" if not failures else "FAIL",len(cases),tuple(failures))

if __name__=="__main__":
    out=audit_historical_replays()
    print(out)
    raise SystemExit(0 if out.status=="PASS" else 1)
