import json
from pathlib import Path
from capability_preservation import evaluate_manifest

ROOT=Path(__file__).resolve().parents[1]

def test_declared_capability_preservation_manifest_is_complete_and_resolvable():
    path=ROOT/"integration"/"CAPABILITY_PRESERVATION_MANIFEST_100.json"
    data=json.loads(path.read_text())
    manifest=data["capabilities"]
    results=evaluate_manifest(manifest)
    assert all(r.preserved for r in results)
    missing=[]
    for cid,w in manifest.items():
        keys=("identity","semantics","reachability","selection","effect","consumer","recovery")
        if w.get("operational",True):
            keys=keys+("execution",)
        for key in keys:
            ref=w[key]
            if not (ROOT/ref).exists():
                missing.append((cid,key,ref))
    assert missing==[]
