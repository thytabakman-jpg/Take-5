#!/usr/bin/env python3
"""Load the exact authoritative Take-5 snapshot from a GitHub Actions artifact.

No network, credentials, repository writes or semantic substitution.
The caller independently fetches the current main commit and passes its SHA.
"""
import argparse
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

TESTS = [
    "test_direct_tool_command_gateway.py", "test_goal.py",
    "test_multiobject.py", "test_prose.py",
    "test_full_invocation_portfolio.py", "test_configured_hf2_execution.py",
    "test_portable_tool_conductor.py", "test_tool_system_every_tool_sweep.py",
    "test_mt_semantic_return_gate.py", "test_assert_compound.py",
    "test_assert_full36.py", "test_currentness_audit.py",
    "test_prose_transition_layers.py", "test_goal_fullmath_identity.py",
    "test_multiobject_fullmath_identity.py",
    "test_improvement_core_hf2_default.py", "test_hf2_fixed_point_closure.py",
]

def git_blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def install(artifact, destination, expected):
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise ValueError("Expected full Git commit SHA required")
    with zipfile.ZipFile(artifact) as outer:
        commit = outer.read("source-commit.txt").decode().strip()
        if commit != expected:
            raise ValueError(f"STALE_SOURCE: expected {expected}, got {commit}")
        source = outer.read("take5-source.zip")
        archive_hash = hashlib.sha256(source).hexdigest()
        if archive_hash != outer.read("SHA256SUMS").decode().split()[0]:
            raise ValueError("ARCHIVE_CHECKSUM_MISMATCH")
        tree = {}
        for line in outer.read("git-tree.txt").decode().splitlines():
            metadata, name = line.split("\t", 1)
            mode, typ, sha = metadata.split()
            if typ == "blob":
                if name in tree:
                    raise ValueError(f"DUPLICATE_TREE_PATH: {name}")
                tree[name] = (mode, sha)
        with zipfile.ZipFile(io.BytesIO(source)) as z:
            seen = set()
            for info in z.infolist():
                p = PurePosixPath(info.filename)
                if p.is_absolute() or ".." in p.parts or "\\" in info.filename:
                    raise ValueError(f"UNSAFE_PATH: {info.filename}")
                if info.is_dir():
                    continue
                if info.filename in seen or info.filename not in tree:
                    raise ValueError(f"UNEXPECTED_OR_DUPLICATE_PATH: {info.filename}")
                mode, sha = tree[info.filename]
                if mode not in ("100644", "100755"):
                    raise ValueError(f"UNSUPPORTED_FILE_MODE: {info.filename} {mode}")
                if git_blob_sha(z.read(info)) != sha:
                    raise ValueError(f"BLOB_MISMATCH: {info.filename}")
                seen.add(info.filename)
            if seen != set(tree):
                raise ValueError(f"MISSING_TRACKED_BLOBS: {sorted(set(tree)-seen)}")
            root = Path(destination).resolve() / commit
            root.mkdir(parents=True, exist_ok=False)
            for name in sorted(seen):
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(z.read(name))
    return root, {
        "source_commit": commit, "archive_sha256": archive_hash,
        "verified_files":len(seen), "tracked_blob_count":len(tree),
        "runtime_python_files":sum(n.startswith("runtime/") and n.endswith(".py") for n in seen),
    }

def smoke(root):
    env = {**os.environ, "PYTHONPATH": str(root/"runtime")+os.pathsep+str(root)}
    tests = ["tests/"+t for t in TESTS]
    absent = [t for t in tests if not (root/t).is_file()]
    if absent:
        raise ValueError(f"MISSING_REGRESSION_TESTS: {absent}")
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", *tests],
                       cwd=root, env=env, capture_output=True, text=True, timeout=120)
    registry_code = """from dataclasses import asdict
import json
from full_invocation_portfolio import audit_full_invocation_portfolio
from portable_tool_conductor import compile_repertoire
a=audit_full_invocation_portfolio()
print(json.dumps({'routing_audit':asdict(a),'registry':[asdict(w) for w in compile_repertoire()]}))
raise SystemExit(int(a.status!='CLOSED_RELATIVE'))
"""
    q = subprocess.run([sys.executable, "-c", registry_code],
                       cwd=root, env=env, capture_output=True, text=True, timeout=120)
    return {
        "test_files":tests, "returncode":p.returncode, "stdout":p.stdout,
        "stderr":p.stderr, "registry_returncode":q.returncode,
        "registry":json.loads(q.stdout) if q.returncode==0 else None,
        "registry_stderr":q.stderr,
        "python":sys.version,
        "dependency_versions":{n:importlib.metadata.version(n) for n in ("pytest","PyYAML")},
        "audit_scope":"Native regressions and synthetic invocation-route coverage only",
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--expected-commit", required=True)
    ap.add_argument("--destination",type=Path, default=Path("take5-runtime"))
    ap.add_argument("--receipt",type=Path, default=Path("bootstrap-receipt.json"))
    args=ap.parse_args()
    root, receipt = install(args.artifact,args.destination,args.expected_commit)
    receipt["runtime_path"]=str(root)
    receipt["smoke"]=smoke(root)
    receipt["status"]="BOOTSTRAP_VERIFIED" if (receipt["smoke"]["returncode"]==0 and receipt["smoke"]["registry_returncode"]==0) else "OPEN_TEST_FAILURE"
    receipt["semantic_execution_status"]="OPEN_UNTIL_TOOL_SPECIFIC_ADAPTERS_ARE_BOUND"
    args.receipt.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k!="smoke"},indent=2))
    print(receipt["smoke"]["stdout"])
    print("Registry audit:", (receipt["smoke"]["registry"] or {}).get("routing_audit"))
    return int(receipt["status"]!="BOOTSTRAP_VERIFIED")

if __name__=="__main__":
    raise SystemExit(main())
