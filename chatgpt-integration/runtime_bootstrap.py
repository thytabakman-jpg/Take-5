#!/usr/bin/env python3
"""Load the exact authoritative Take-5 snapshot from a verified local archive.

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
from time import perf_counter
import zipfile

# I. Integration identity and validation configuration.
INTEGRATION_FILES = ("runtime_bootstrap.py", "execute_tool_packet.py", "document_tool_adapters.py", "README.md")


# II. Git identity primitives and integration verification.
# Owns Git-object hashing primitives. Runtime verification remains SHA-1;
# document providers may explicitly request SHA-256 for admitted source bytes.
def git_object_sha(kind, data, *, algorithm="sha1"):
    """Hash Git object bytes; bootstrap callers retain the SHA-1 default."""
    if algorithm not in {"sha1", "sha256"}:
        raise ValueError("GIT_OBJECT_HASH_ALGORITHM_UNSUPPORTED")
    return hashlib.new(algorithm, f"{kind} {len(data)}\0".encode() + data).hexdigest()

def git_blob_sha(data):
    return git_object_sha("blob", data)


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


# III. Authenticated source tree and installed runtime verification.
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


def verify_bootstrap_receipt(root, boot, integration_manifest, *, expected_commit):
    """Revalidate a previously verified runtime before any native imports."""
    root = Path(root).resolve()
    if boot.get("status") != "BOOTSTRAP_VERIFIED" or Path(boot["runtime_path"]).resolve() != root:
        raise ValueError("VERIFIED_BOOTSTRAP_RECEIPT_REQUIRED")
    if boot.get("integration_manifest") != integration_manifest:
        raise ValueError("BOOTSTRAP_INTEGRATION_IDENTITY_MISMATCH")
    verify_integration_files(Path(__file__).resolve().parent, integration_manifest)
    verify_smoke_basis(boot.get("smoke"))
    commit = boot["source_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", expected_commit) or commit != expected_commit:
        raise ValueError("BOOTSTRAP_SOURCE_COMMIT_NOT_CURRENT")
    source_tree = verify_installed_tree(root, commit,
        base64.b64decode(boot["source_commit_object"], validate=True),
        boot["tracked_tree"], boot.get("source_tree"))
    return commit, source_tree


# IV. Archive admission and installation.
def verified_archive_members(z, tree):
    """Verify the complete archive against the authenticated tree before any write."""
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
    return seen


def _read_tracked_tree(raw):
    tree = {}
    for line in raw.split(b"\0"):
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
    return tree


def cached_source_blobs(source_cache, tree):
    """Read cache bytes by content identity; never trust cached names or metadata."""
    needed = {sha for _, sha in tree.values()}
    cached = {}
    if source_cache is None:
        return cached
    with zipfile.ZipFile(source_cache) as outer:
        with zipfile.ZipFile(io.BytesIO(outer.read('take5-source.zip'))) as source:
            for member in source.infolist():
                if member.is_dir():
                    continue
                data = source.read(member)
                sha = git_blob_sha(data)
                if sha in needed:
                    cached[sha] = data
                    needed.remove(sha)
                    if not needed:
                        break
    return cached


def assemble_verified_archive(output, expected, commit_object, tree, blob_dir,
                              integration_manifest, integration_dir, source_cache=None):
    """Assemble from authenticated identities and local blob bytes, without a runner.

    Cache bytes have no authority: every reused or fetched blob must match the
    independently selected current tree. The ordinary installer remains the
    final archive-admission and regression-test path.
    """
    verify_commit_tree(expected, commit_object, tree)
    verify_integration_files(integration_dir, integration_manifest)
    output=Path(output).resolve()
    if source_cache is not None and output==Path(source_cache).resolve():
        raise ValueError('RECONSTRUCTION_OUTPUT_OVERWRITES_CACHE')
    blob_dir=Path(blob_dir)
    cached=cached_source_blobs(source_cache,tree)
    reused_paths=0
    rebuilt=io.BytesIO()
    with zipfile.ZipFile(rebuilt,'w',zipfile.ZIP_DEFLATED) as source:
        for name,(mode,sha) in sorted(tree.items()):
            if sha in cached:
                data=cached[sha]
                reused_paths+=1
            else:
                blob=blob_dir/sha
                if blob.is_symlink() or not blob.is_file():
                    raise ValueError(f'RECONSTRUCTION_BLOB_REQUIRED:{name}:{sha}')
                data=blob.read_bytes()
            if git_blob_sha(data)!=sha:
                raise ValueError(f'RECONSTRUCTION_BLOB_MISMATCH:{name}')
            member=zipfile.ZipInfo(name)
            member.create_system=3
            member.external_attr=int(mode,8)<<16
            member.compress_type=zipfile.ZIP_DEFLATED
            source.writestr(member,data)
    data=rebuilt.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        verified_archive_members(source,tree)
    archive=io.BytesIO()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as outer:
        for name in INTEGRATION_FILES:
            outer.writestr(name,(Path(integration_dir)/name).read_bytes())
        outer.writestr('integration-commit.txt',integration_manifest['commit']+'\n')
        outer.writestr('source-commit.txt',expected+'\n')
        outer.writestr('source-commit-object.txt',commit_object)
        outer.writestr('git-tree.txt',b''.join(f'{mode} blob {sha}\t{name}'.encode()+b'\0'
                           for name,(mode,sha) in sorted(tree.items())))
        outer.writestr('take5-source.zip',data)
        outer.writestr('SHA256SUMS',hashlib.sha256(data).hexdigest()+'  take5-source.zip\n')
    # Do not overwrite an existing archive; installation still rechecks all bytes.
    with output.open('xb') as handle:
        handle.write(archive.getvalue())
    return {'source_commit':expected,'verified_blobs':len(tree),'reused_cache_blobs':reused_paths,
            'fetched_blobs':len(tree)-reused_paths,
            'unique_cached_blob_count':len(cached),
            'unique_required_blob_count':len({sha for _,sha in tree.values()}-cached.keys()),'archive_sha256':hashlib.sha256(data).hexdigest()}


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
        commit_object = outer.read("source-commit-object.txt")
        tree = _read_tracked_tree(outer.read("git-tree.txt"))
        source_tree = verify_commit_tree(commit, commit_object, tree)
        with zipfile.ZipFile(io.BytesIO(source)) as z:
            seen = verified_archive_members(z, tree)
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

# V. Runtime validation inventory and execution.
# Keep this bootstrap-specific acceptance inventory independent of the native
# routing audit and implementation manifests.
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
    "test_execution_responsibility_boundaries.py",
]


def observed_test_environment():
    """Coordinates observed by the bootstrap suite, not a proof of total environment identity."""
    return {
        "python": sys.version,
        "dependency_versions": {n: importlib.metadata.version(n) for n in ("pytest", "PyYAML")},
    }


def verify_smoke_basis(receipt):
    """Reject stale or incomplete local bootstrap regression evidence on reuse."""
    if not isinstance(receipt, dict):
        raise ValueError("BOOTSTRAP_SMOKE_RECEIPT_REQUIRED")
    if any(type(receipt.get(key)) is not int or receipt[key] != 0
           for key in ("returncode", "registry_returncode")):
        raise ValueError("BOOTSTRAP_SMOKE_NOT_PASSED")
    if receipt.get("test_files") != ["tests/" + name for name in TESTS]:
        raise ValueError("BOOTSTRAP_TEST_INVENTORY_CHANGED")
    registry = receipt.get("registry")
    if not isinstance(registry, dict) or not isinstance(registry.get("routing_audit"), dict) or registry["routing_audit"].get("status") != "CLOSED_RELATIVE":
        raise ValueError("BOOTSTRAP_ROUTING_AUDIT_NOT_CLOSED")
    if any(receipt.get(key) != value for key, value in observed_test_environment().items()):
        raise ValueError("BOOTSTRAP_TEST_ENVIRONMENT_CHANGED")


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
        **observed_test_environment(),
        "audit_scope":"Native regressions and synthetic invocation-route coverage only",
    }

# VI. Failure receipts and command-line orchestration.
# Packet-specific result receipts remain owned by execute_tool_packet.py;
# this helper serves pre-dispatch failure reporting only.
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
    ap.add_argument("--assemble-tree",type=Path,help="Authenticated recursive tracked-tree manifest")
    ap.add_argument("--assemble-commit-object",type=Path,help="Exact current Git commit object bytes")
    ap.add_argument("--assemble-blobs",type=Path,help="Directory of fetched bytes named by Git blob SHA")
    ap.add_argument("--source-cache",type=Path,help="Optional earlier local archive; bytes reverified against the current tree")
    args=ap.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", args.expected_commit):
        target=(args.destination.resolve()/args.expected_commit).resolve()
        if args.receipt.resolve().is_relative_to(target):
            print("RECEIPT_INSIDE_VERIFIED_RUNTIME", file=sys.stderr)
            return 1
    phase = "INSTALL"
    timings = {}
    started = perf_counter()
    context = {"expected_commit": args.expected_commit}
    try:
        integration_manifest = read_integration_manifest(args.integration_manifest)
        context["integration_commit"] = integration_manifest["commit"]
        verify_integration_files(Path(__file__).resolve().parent, integration_manifest)
        assembly_args=(args.assemble_tree,args.assemble_commit_object,args.assemble_blobs)
        assembly=None
        if any(assembly_args) or args.source_cache is not None:
            phase="LOCAL_ARCHIVE_ASSEMBLY"
            if not all(assembly_args):
                raise ValueError("COMPLETE_RECONSTRUCTION_INPUT_REQUIRED")
            target=(args.destination.resolve()/args.expected_commit).resolve()
            if args.artifact.resolve().is_relative_to(target):
                raise ValueError("ARCHIVE_INSIDE_VERIFIED_RUNTIME")
            stage = perf_counter()
            assembly=assemble_verified_archive(args.artifact,args.expected_commit,
                args.assemble_commit_object.read_bytes(),_read_tracked_tree(args.assemble_tree.read_bytes()),
                args.assemble_blobs,integration_manifest,Path(__file__).resolve().parent,args.source_cache)
            timings["local_assembly_seconds"] = perf_counter() - stage
        phase="INSTALL"
        stage = perf_counter()
        root, receipt = install(args.artifact,args.destination,args.expected_commit,integration_manifest)
        timings["install_seconds"] = perf_counter() - stage
        if assembly is not None:
            receipt["local_assembly"]=assembly
        receipt["runtime_path"]=str(root)
        context.update(source_commit=receipt["source_commit"], source_tree=receipt["source_tree"],
                       runtime_path=str(root))
        phase = "SMOKE_TESTS"
        stage = perf_counter()
        receipt["smoke"]=smoke(root)
        timings["smoke_seconds"] = perf_counter() - stage
        phase = "POST_TEST_INTEGRITY"
        stage = perf_counter()
        verify_installed_tree(root, receipt["source_commit"],
            base64.b64decode(receipt["source_commit_object"], validate=True),
            receipt["tracked_tree"], receipt["source_tree"])
        timings["post_test_integrity_seconds"] = perf_counter() - stage
        timings["total_local_seconds"] = perf_counter() - started
        receipt["local_timings"] = timings
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
