#!/usr/bin/env python3
"""Load the exact authoritative Take-5 snapshot from a GitHub Actions artifact.

No network, credentials, repository writes or semantic substitution.
The caller independently fetches the current main commit and passes its SHA.
"""
import argparse
import base64
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

def git_object_sha(kind, data):
    return hashlib.sha1(f"{kind} {len(data)}\0".encode() + data).hexdigest()

def git_blob_sha(data):
    return git_object_sha("blob", data)

INTEGRATION_FILES = ("bootstrap.py", "run_packet.py", "document_adapters.py", "README.md")


def read_integration_manifest(path):
    """Expected identities come from the host's authenticated branch fetch, not the ZIP."""
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    commit, blobs = value["commit"], value["blobs"]
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("INTEGRATION_COMMIT_REQUIRED")
    if (not isinstance(blobs, dict) or set(blobs) != set(INTEGRATION_FILES)
            or any(not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha)
                   for sha in blobs.values())):
        raise ValueError("INTEGRATION_BLOB_IDENTITIES_REQUIRED")
    return {"commit": commit, "blobs": blobs}


def verify_integration_files(directory, manifest):
    """Check the actual local companion bytes before importing native tools."""
    directory = Path(directory)
    for name, expected in manifest["blobs"].items():
        path = directory / name
        if path.is_symlink() or not path.is_file() or git_blob_sha(path.read_bytes()) != expected:
            raise ValueError(f"INTEGRATION_FILE_MISMATCH:{name}")


def verify_integration_archive(outer, manifest):
    names = ("integration-commit.txt", *INTEGRATION_FILES)
    if any(outer.namelist().count(name) != 1 for name in names):
        raise ValueError("INTEGRATION_ARCHIVE_MEMBERS_REQUIRED")
    actual = outer.read("integration-commit.txt").decode("ascii").strip()
    if actual != manifest["commit"]:
        raise ValueError(f"STALE_INTEGRATION: expected {manifest['commit']}, got {actual}")
    for name, expected in manifest["blobs"].items():
        if git_blob_sha(outer.read(name)) != expected:
            raise ValueError(f"INTEGRATION_ARCHIVE_BLOB_MISMATCH:{name}")


def git_tree_sha(tree):
    """Reconstruct the Git root tree from the complete recursive blob manifest."""
    root = {}
    for name, (mode, sha) in tree.items():
        p = PurePosixPath(name)
        if (not p.parts or p.is_absolute() or ".." in p.parts or "\\" in name
                or p.as_posix() != name or mode not in ("100644", "100755")
                or not re.fullmatch(r"[0-9a-f]{40}", sha)):
            raise ValueError(f"INVALID_TREE_ENTRY:{name}")
        node = root
        for part in p.parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise ValueError(f"TREE_PATH_COLLISION:{name}")
        if p.name in node:
            raise ValueError(f"TREE_PATH_COLLISION:{name}")
        node[p.name] = (mode, sha)
    def digest_tree(node):
        entries = []
        for name, value in sorted(node.items(), key=lambda item: item[0].encode() + (b"/" if isinstance(item[1], dict) else b"")):
            mode, sha = ("40000", digest_tree(value)) if isinstance(value, dict) else value
            entries.append(mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(sha))
        return git_object_sha("tree", b"".join(entries))
    return digest_tree(root)

def verify_commit_tree(commit, commit_object, tree):
    if git_object_sha("commit", commit_object) != commit:
        raise ValueError("SOURCE_COMMIT_OBJECT_MISMATCH")
    first = commit_object.split(b"\n", 1)[0]
    if not re.fullmatch(rb"tree [0-9a-f]{40}", first):
        raise ValueError("SOURCE_COMMIT_TREE_REQUIRED")
    actual = git_tree_sha(tree)
    if first != b"tree " + actual.encode():
        raise ValueError("SOURCE_TREE_IDENTITY_MISMATCH")
    return actual

def verify_installed_tree(root, commit, commit_object, tree, expected_tree):
    """Verify exact installed files and directories, including absence of extras."""
    root = Path(root).resolve()
    source_tree = verify_commit_tree(commit, commit_object, tree)
    if source_tree != expected_tree:
        raise ValueError("BOOTSTRAP_SOURCE_TREE_MISMATCH")
    expected_dirs = {parent.as_posix() for name in tree
                     for parent in PurePosixPath(name).parents if parent != PurePosixPath(".")}
    seen = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise ValueError(f"RUNTIME_UNVERIFIED_SYMLINK:{relative}")
            if name in dirs:
                if relative not in expected_dirs:
                    raise ValueError(f"RUNTIME_UNTRACKED_DIRECTORY:{relative}")
            else:
                if relative not in tree:
                    raise ValueError(f"RUNTIME_UNTRACKED_FILE:{relative}")
                if not path.is_file() or git_blob_sha(path.read_bytes()) != tree[relative][1]:
                    raise ValueError(f"RUNTIME_SOURCE_CHANGED:{relative}")
                seen.add(relative)
    if seen != set(tree):
        raise ValueError(f"RUNTIME_MISSING_TRACKED_FILES:{sorted(set(tree)-seen)}")
    return source_tree


def verify_bootstrap_receipt(root, boot, integration_manifest):
    """Revalidate a previously verified runtime before any native imports."""
    root = Path(root).resolve()
    if boot.get("status") != "BOOTSTRAP_VERIFIED" or Path(boot["runtime_path"]).resolve() != root:
        raise ValueError("VERIFIED_BOOTSTRAP_RECEIPT_REQUIRED")
    if boot.get("integration_manifest") != integration_manifest:
        raise ValueError("BOOTSTRAP_INTEGRATION_IDENTITY_MISMATCH")
    verify_integration_files(Path(__file__).resolve().parent, integration_manifest)
    commit = boot["source_commit"]
    source_tree = verify_installed_tree(root, commit,
        base64.b64decode(boot["source_commit_object"], validate=True),
        boot["tracked_tree"], boot.get("source_tree"))
    return commit, source_tree


def install(artifact, destination, expected, integration_manifest):
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise ValueError("Expected full Git commit SHA required")
    with zipfile.ZipFile(artifact) as outer:
        verify_integration_archive(outer, integration_manifest)
        commit = outer.read("source-commit.txt").decode().strip()
        if commit != expected:
            raise ValueError(f"STALE_SOURCE: expected {expected}, got {commit}")
        source = outer.read("take5-source.zip")
        archive_hash = hashlib.sha256(source).hexdigest()
        if archive_hash != outer.read("SHA256SUMS").decode().split()[0]:
            raise ValueError("ARCHIVE_CHECKSUM_MISMATCH")
        tree = {}
        commit_object = outer.read("source-commit-object.txt")
        for line in outer.read("git-tree.txt").split(b"\0"):
            if not line:
                continue
            metadata, name_bytes = line.split(b"\t", 1)
            name = name_bytes.decode("utf-8")
            mode, typ, sha = metadata.decode("ascii").split()
            if typ != "blob":
                raise ValueError(f"UNSUPPORTED_TREE_OBJECT: {name} {typ}")
            if name in tree:
                raise ValueError(f"DUPLICATE_TREE_PATH: {name}")
            tree[name] = (mode, sha)
        source_tree = verify_commit_tree(commit, commit_object, tree)
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
        "source_commit": commit, "source_tree": source_tree, "archive_sha256": archive_hash,
        "integration_manifest": integration_manifest,
        "source_commit_object": base64.b64encode(commit_object).decode("ascii"),
        "tracked_tree": tree,
        "verified_files":len(seen), "tracked_blob_count":len(tree),
        "runtime_python_files":sum(n.startswith("runtime/") and n.endswith(".py") for n in seen),
    }

def smoke(root):
    env = {**os.environ, "PYTHONPATH": str(root/"runtime")+os.pathsep+str(root),
           "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("PYTHONPYCACHEPREFIX", None)
    tests = ["tests/"+t for t in TESTS]
    absent = [t for t in tests if not (root/t).is_file()]
    if absent:
        raise ValueError(f"MISSING_REGRESSION_TESTS: {absent}")
    p = subprocess.run([sys.executable, "-B", "-m", "pytest", "-p", "no:cacheprovider", "-q", *tests],
                       cwd=root, env=env, capture_output=True, text=True, timeout=120)
    registry_code = """from dataclasses import asdict
import json
from full_invocation_portfolio import audit_full_invocation_portfolio
from portable_tool_conductor import compile_repertoire
a=audit_full_invocation_portfolio()
print(json.dumps({'routing_audit':asdict(a),'registry':[asdict(w) for w in compile_repertoire()]}))
raise SystemExit(int(a.status!='CLOSED_RELATIVE'))
"""
    q = subprocess.run([sys.executable, "-B", "-c", registry_code],
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

def write_failure_receipt(path, operation, phase, exc, context):
    """Report pre-dispatch failure without claiming native tool execution."""
    failure = {**context, "status": "BLOCKED", "operation": operation,
               "phase": phase, "blocker": f"{type(exc).__name__}:{exc}",
               "native_tool_execution": False}
    if operation == "PACKET":
        failure.update(results=[])
    payload = json.dumps(failure, indent=2) + "\n"
    try:
        path.write_text(payload, encoding="utf-8")
    except OSError as write_error:
        print(f"FAILURE_RECEIPT_WRITE_ERROR:{write_error}", file=sys.stderr)
    print(payload, file=sys.stderr, end="")
    return 1


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--expected-commit", required=True)
    ap.add_argument("--integration-manifest", type=Path, required=True,
                    help="Independently fetched integration commit and four Git blob identities")
    ap.add_argument("--destination",type=Path, default=Path("take5-runtime"))
    ap.add_argument("--receipt",type=Path, default=Path("bootstrap-receipt.json"))
    args=ap.parse_args()
    phase = "INSTALL"
    context = {"expected_commit": args.expected_commit}
    try:
        integration_manifest = read_integration_manifest(args.integration_manifest)
        context["integration_commit"] = integration_manifest["commit"]
        verify_integration_files(Path(__file__).resolve().parent, integration_manifest)
        root, receipt = install(args.artifact,args.destination,args.expected_commit,integration_manifest)
        receipt["runtime_path"]=str(root)
        context.update(source_commit=receipt["source_commit"], source_tree=receipt["source_tree"],
                       runtime_path=str(root))
        phase = "SMOKE_TESTS"
        receipt["smoke"]=smoke(root)
        phase = "POST_TEST_INTEGRITY"
        verify_installed_tree(root, receipt["source_commit"],
            base64.b64decode(receipt["source_commit_object"], validate=True),
            receipt["tracked_tree"], receipt["source_tree"])
    except Exception as exc:
        return write_failure_receipt(args.receipt, "BOOTSTRAP", phase, exc, context)
    receipt["status"]="BOOTSTRAP_VERIFIED" if (receipt["smoke"]["returncode"]==0 and receipt["smoke"]["registry_returncode"]==0) else "OPEN_TEST_FAILURE"
    receipt["semantic_execution_status"]="OPEN_UNTIL_TOOL_SPECIFIC_ADAPTERS_ARE_BOUND"
    args.receipt.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k!="smoke"},indent=2))
    print(receipt["smoke"]["stdout"])
    print("Registry audit:", (receipt["smoke"]["registry"] or {}).get("routing_audit"))
    return int(receipt["status"]!="BOOTSTRAP_VERIFIED")

if __name__=="__main__":
    raise SystemExit(main())
