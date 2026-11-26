#!/usr/bin/env python3
"""Bind an explicit, frozen document-analysis packet to the original Take-5 gateway.

Built-in bindings are owned by document_tool_adapters.py (finite PD/PDAudit and Prose).
Other tools require an explicitly supplied trusted Python adapter module.
Never fabricates semantic-worker, independence, or full-coverage receipts.
No research-document mutation.
"""
import argparse
from collections.abc import Mapping
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def _load_adapter_module(path, name):
    """Load a specific companion or explicitly authorized provider by path."""
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise TypeError("ADAPTER_MODULE_LOADER_REQUIRED")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def builtin_adapters(packet, digest):
    """Compatibility entry point; the companion adapter module owns the bindings."""
    mod=_load_adapter_module(Path(__file__).resolve().with_name("document_tool_adapters.py"),
                             "take5_builtin_document_adapters")
    return mod.builtin_adapters(packet,digest)


def admit_external_adapters(packet, ids, adapters, adapter_module, allowed):
    """Authorize provider bindings separately from gateway execution."""
    provider=None
    admitted_external=set()
    admission_errors={}
    provider_error=None
    if adapter_module:
        mod_path=adapter_module.resolve()
        provider={"path":str(mod_path),"sha256":None,"status":"OPEN"}
        try:
            provider["sha256"]=sha256(mod_path.read_bytes())
            mod=_load_adapter_module(mod_path,"take5_explicit_host_adapter")
            binder=getattr(mod,"bind_adapters",None)
            if not callable(binder):
                raise TypeError("ADAPTER_BINDER_REQUIRED")
            external=binder(packet)
            if not isinstance(external,Mapping):
                raise TypeError("ADAPTER_MAPPING_REQUIRED")
            offered=list(external.items())
            admitted={}
            provider["offered_tools"]=[tool for tool,_ in offered]
            for tool,binding in offered:
                if tool not in ids:
                    continue
                if tool in adapters and tool not in allowed:
                    admission_errors[tool]="ADAPTER_OVERRIDE_NOT_AUTHORIZED"
                elif not callable(binding):
                    admission_errors[tool]="ADAPTER_NOT_CALLABLE"
                else:
                    admitted[tool]=binding
            adapters.update(admitted)
            admitted_external.update(admitted)
            provider["status"]="LOADED"
        except Exception as exc:
            provider_error=f"{type(exc).__name__}:{exc}"
            provider.update(status="BLOCKED",blocker=provider_error)
    return provider,admitted_external,admission_errors,provider_error


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime", type=Path, required=True)
    p.add_argument("--bootstrap-receipt", type=Path, default=Path("bootstrap-receipt.json"),
                   help="Receipt from verified bootstrap installation")
    p.add_argument("--integration-manifest", type=Path, required=True,
                   help="Independently fetched current integration commit and Git blob identities")
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--adapter-module",type=Path,help="Explicit trusted local module exposing bind_adapters(packet)")
    p.add_argument("--allow-adapter-override",action="append",default=[],metavar="TOOL",
                   help="Explicitly allow an external binding to replace this built-in tool (repeatable)")
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    from runtime_bootstrap import verify_bootstrap_receipt, write_failure_receipt, read_integration_manifest
    phase = "RUNTIME_VERIFICATION"
    context = {}
    try:
        root=a.runtime.resolve()
        boot=json.loads(a.bootstrap_receipt.read_text(encoding="utf-8"))
        integration_manifest = read_integration_manifest(a.integration_manifest)
        source_commit, source_tree = verify_bootstrap_receipt(root, boot, integration_manifest)
        context.update(source_commit=source_commit, source_tree=source_tree,
                       integration_commit=integration_manifest["commit"])
        # Keep the verified installation free of generated import caches.
        sys.dont_write_bytecode = True
        sys.pycache_prefix = None
        sys.path.insert(0,str(root))
        sys.path.insert(0,str(root/"runtime"))
        phase = "GATEWAY_LOAD"
        from direct_tool_command_gateway import execute_direct_tool_commands, direct_tool_ids
        phase = "PACKET_ADMISSION"
        raw=a.packet.read_bytes()
        digest=sha256(raw)
        context["packet_sha256"] = digest
        packet=json.loads(raw)
        ids=direct_tool_ids(packet["command"])
        context["tool_ids"] = ids
        adapters=builtin_adapters(packet,digest)
    except Exception as exc:
        return write_failure_receipt(a.receipt, "PACKET", phase, exc, context)
    allowed=set(a.allow_adapter_override)
    provider,admitted_external,admission_errors,provider_error=admit_external_adapters(
        packet,ids,adapters,a.adapter_module,allowed
    )
    # Independent requested tools retain their own receipts. A failed external
    # provider cannot suppress unrelated built-ins or silently authorize fallback.
    results=[]
    def binding_identity(tool):
        if tool in admitted_external:
            return {"kind":"EXPLICIT_MODULE","path":provider["path"],"sha256":provider["sha256"]}
        if tool in adapters:
            return {"kind":"BUILTIN","path":"document_tool_adapters.py",
                    "git_blob_sha":integration_manifest["blobs"]["document_tool_adapters.py"]}
        return {"kind":"MISSING"}
    for tool in ids:
        if tool in admission_errors:
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":admission_errors[tool],
                            "adapter_disposition":"INCOMPATIBLE_BINDING","native_invocation":"NOT_INVOKED"})
            continue
        if provider_error and (tool not in adapters or tool in allowed):
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":provider_error,
                            "adapter_disposition":"PROVIDER_INITIALIZATION_FAILED","native_invocation":"NOT_INVOKED"})
            continue
        if tool in allowed and (provider is None or tool not in provider.get("offered_tools",())):
            results.append({"tool_id":tool,"status":"OPEN","blocker":"AUTHORIZED_OVERRIDE_NOT_SUPPLIED",
                            "adapter_disposition":"MISSING_OVERRIDE","native_invocation":"NOT_INVOKED"})
            continue
        try:
            out=execute_direct_tool_commands([tool],state={"packet_sha256":digest},adapters=adapters)
            row=asdict(out)
            row["tool_id"]=tool
            row["adapter_disposition"]="BOUND" if tool in adapters else "MISSING_ADAPTER"
            row["provider_binding_identity"]=binding_identity(tool)
            results.append(row)
        except (KeyError,ValueError,TypeError) as exc:
            # An exception alone cannot establish whether validation or execution
            # failed; keep the original exception and avoid guessing its cause.
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":f"{type(exc).__name__}:{exc}",
                            "adapter_disposition":"INPUT_OR_EXECUTION_ERROR","native_invocation":"UNKNOWN",
                            "provider_binding_identity":binding_identity(tool)})
        except Exception as exc:
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":f"{type(exc).__name__}:{exc}",
                            "adapter_disposition":"EXECUTION_ERROR","native_invocation":"UNKNOWN",
                            "provider_binding_identity":binding_identity(tool)})
    receipt={"source_commit":source_commit,"source_tree":source_tree,
             "integration_manifest":integration_manifest,"packet_sha256":digest,"tool_ids":ids,
             "adapter_module":provider,"authorized_overrides":sorted(allowed),"scope":"Explicit bounded native input; no independent semantic adjudication or full geometric coverage asserted",
             "results":results}
    a.receipt.write_text(json.dumps(receipt,indent=2,default=str)+"\n")
    print(json.dumps({"source_commit":source_commit,"tool_ids":ids,"statuses":[r.get("status") for r in results],"receipt":str(a.receipt)},indent=2))
    return int(not ids or any(r.get("status")!="EXECUTED" for r in results))

if __name__=="__main__":
    raise SystemExit(main())
