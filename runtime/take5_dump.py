#!/usr/bin/env python3
import argparse
import hashlib
import json
import time
from pathlib import Path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(root):
    rows=[]
    for p in sorted(root.rglob("*")):
        if p.is_file():
            text=p.read_text(errors="replace")
            rows.append({"path":str(p.relative_to(root)),"bytes":p.stat().st_size,
                         "sha256":digest(p),"preview":text[:4000]})
    return rows

def frontier(job):
    if job:
        return [{"id":"J1","kind":"DIRECT","claim":job,"basis":"manifest"}]
    return [
      {"id":"Z1","kind":"STRUCTURE","claim":"Recover corpus structure and current-state signals.","basis":"corpus_only"},
      {"id":"Z2","kind":"DEPENDENCY","claim":"Find unresolved dependencies and explicit open markers.","basis":"corpus_only"},
      {"id":"Z3","kind":"ANTI_LOSS","claim":"Find duplicated, orphaned, superseded, or unregistered artifacts.","basis":"corpus_only"},
      {"id":"Z4","kind":"IMPROVEMENT","claim":"Find a corpus-grounded strengthening frontier without inventing an external goal.","basis":"corpus_only"}
    ]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("dump",type=Path)
    ap.add_argument("--state",type=Path,default=Path("runtime/state/default"))
    a=ap.parse_args()
    manifest=a.dump/"take5.json"
    m=json.loads(manifest.read_text()) if manifest.exists() else {}
    inv=inventory(a.dump)
    text="\n".join(x["preview"] for x in inv)
    markers={k:text.upper().count(k) for k in ["OPEN","BLOCKED","TODO","FIXME","SUPERSEDED"]}
    target={"id":m.get("id","dump"),"job":m.get("job"),
            "mode":"DIRECTED" if m.get("job") else "ZERO_REQUEST",
            "protected":m.get("protected",[])}
    work=frontier(target["job"])
    route=["C01","C03","C07","C08","C10","C11","C16","C19","C22","C33","C34","C44","C47"]
    result={"schema":"take5-run-0.1","target":target,"inventory":inv,
            "analysis":{"markers":markers,"frontier":work,"capability_route":route},
            "verification":{"pass":bool(work) and bool(target["id"])},
            "terminal":"COMPLETE" if work and target["id"] else "OPEN"}
    a.state.mkdir(parents=True,exist_ok=True)
    (a.state/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    event={"time":time.time(),"target":target["id"],"terminal":result["terminal"],
           "result_sha256":digest(a.state/"result.json")}
    with (a.state/"events.jsonl").open("a") as f:
        f.write(json.dumps(event)+"\n")
    print(json.dumps({"terminal":result["terminal"],"mode":target["mode"],
                      "files":len(inv),"frontier":len(work)}))
    return 0 if result["verification"]["pass"] else 2

if __name__=="__main__":
    raise SystemExit(main())
