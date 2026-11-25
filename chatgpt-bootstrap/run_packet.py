#!/usr/bin/env python3
"""Bind an explicit, frozen document-analysis packet to the original Take-5 gateway.

Built-in bindings are finite-frame PD/PDAudit and Prose's explicit contract.
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


def builtin_adapters(packet, digest):
    from pd import run_pd
    from pd_audit import run_pd_audit
    from prose import ProseContract, assess_prose

    def pd_adapter(tool):
        def invoke(current, plan):
            spec = packet.get("pd_frame")
            if not spec:
                return {"status":"OPEN", "blocker":"PD_FRAME_REQUIRED"}
            rows = tuple(spec["cases"])
            names = spec["representations"]
            if not rows or not names or not all(row.get("id") for row in rows):
                raise ValueError("EXPLICIT_PD_CASES_AND_COORDINATES_REQUIRED")
            if len({row["id"] for row in rows}) != len(rows):
                raise ValueError("DUPLICATE_PD_CASE_ID")
            if any(not isinstance(fields,list) or not fields for fields in names.values()):
                raise ValueError("PD_REPRESENTATION_FIELDS_REQUIRED")
            # Result labels and coordinate assignments are inputs, not generated evidence.
            args = dict(rho=lambda x:x["result"], approx=lambda a,b:a==b,
                        representations={name:(lambda x, keys=tuple(fields):tuple(x["coordinates"][k] for k in keys))
                                         for name,fields in names.items()})
            fn = run_pd if tool=="PD" else run_pd_audit
            if tool=="PDAudit":
                args.update(kappa_cases=lambda xs:{"case_count":len(xs)},
                            kappa_representations=lambda reps:{"representation_names":list(reps)})
            out = fn(rows, **args)
            return {"status":out["status"], "result":out, "execution_truth":"IMPLEMENTATION_EXECUTED" if out["status"]=="RELATIVE_CLOSE" else "OPEN",
                    "material_delta":False, "evidence":[f"native:{fn.__module__}.{fn.__name__}",f"packet-sha256:{digest}"],
                    "blocker":out.get("blocker")}
        return invoke

    def prose_adapter(current,plan):
        spec=packet.get("prose")
        if not spec:
            return {"status":"OPEN","blocker":"PROSE_TEXT_AND_CONTRACT_REQUIRED"}
        # Semantic PASS evidence is intentionally not constructed from user labels.
        # A separately reviewed semantic-evidence adapter may be explicitly bound.
        contract=ProseContract(**spec["contract"])
        out=assess_prose(spec["text"],contract,evidence=None)
        return {"status":"BLOCKED" if out.status=="BLOCKED" else "OPEN",
                "execution_truth":"BLOCKED" if out.status=="BLOCKED" else "OPEN",
                "result":asdict(out), "material_delta":False,
                "evidence":["native:prose.assess_prose",f"packet-sha256:{digest}"],
                "blocker":"PROSE_SEMANTIC_EVIDENCE_NOT_BOUND"}

    return {"PD":pd_adapter("PD"),"PDAudit":pd_adapter("PDAudit"),"Prose":prose_adapter}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--adapter-module",type=Path,help="Explicit trusted local module exposing bind_adapters(packet)")
    p.add_argument("--allow-adapter-override",action="append",default=[],metavar="TOOL",
                   help="Explicitly allow an external binding to replace this built-in tool (repeatable)")
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    root=a.runtime.resolve()
    sys.path.insert(0,str(root))
    sys.path.insert(0,str(root/"runtime"))
    from direct_tool_command_gateway import execute_direct_tool_commands, direct_tool_ids
    raw=a.packet.read_bytes()
    packet=json.loads(raw)
    digest=sha256(raw)
    ids=direct_tool_ids(packet["command"])
    adapters=builtin_adapters(packet,digest)
    provider=None
    admission_errors={}
    provider_error=None
    allowed=set(a.allow_adapter_override)
    if a.adapter_module:
        mod_path=a.adapter_module.resolve()
        provider={"path":str(mod_path),"sha256":None,"status":"OPEN"}
        try:
            provider["sha256"]=sha256(mod_path.read_bytes())
            spec=importlib.util.spec_from_file_location("take5_explicit_host_adapter",mod_path)
            if spec is None or spec.loader is None:
                raise TypeError("ADAPTER_MODULE_LOADER_REQUIRED")
            mod=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            binder=getattr(mod,"bind_adapters",None)
            if not callable(binder):
                raise TypeError("ADAPTER_BINDER_REQUIRED")
            external=binder(packet)
            if not isinstance(external,Mapping):
                raise TypeError("ADAPTER_MAPPING_REQUIRED")
            provider["status"]="LOADED"
            provider["offered_tools"]=list(external)
            for tool,binding in external.items():
                if tool not in ids:
                    continue
                if tool in adapters and tool not in allowed:
                    admission_errors[tool]="ADAPTER_OVERRIDE_NOT_AUTHORIZED"
                elif not callable(binding):
                    admission_errors[tool]="ADAPTER_NOT_CALLABLE"
                else:
                    adapters[tool]=binding
        except Exception as exc:
            provider_error=f"{type(exc).__name__}:{exc}"
            provider.update(status="BLOCKED",blocker=provider_error)
    # Independent requested tools retain their own receipts. A failed external
    # provider cannot suppress unrelated built-ins or silently authorize fallback.
    results=[]
    for tool in ids:
        if tool in admission_errors:
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":admission_errors[tool],
                            "adapter_disposition":"INCOMPATIBLE_BINDING"})
            continue
        if provider_error and (tool not in adapters or tool in allowed):
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":provider_error,
                            "adapter_disposition":"PROVIDER_INITIALIZATION_FAILED"})
            continue
        if tool in allowed and (provider is None or tool not in provider.get("offered_tools",())):
            results.append({"tool_id":tool,"status":"OPEN","blocker":"AUTHORIZED_OVERRIDE_NOT_SUPPLIED",
                            "adapter_disposition":"MISSING_OVERRIDE"})
            continue
        try:
            out=execute_direct_tool_commands(f"run {tool}",state={"packet_sha256":digest},adapters=adapters)
            row=asdict(out)
            row["tool_id"]=tool
            row["adapter_disposition"]="BOUND" if tool in adapters else "MISSING_ADAPTER"
            results.append(row)
        except (KeyError,ValueError,TypeError) as exc:
            # An exception alone cannot establish whether validation or execution
            # failed; keep the original exception and avoid guessing its cause.
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":f"{type(exc).__name__}:{exc}",
                            "adapter_disposition":"INPUT_OR_EXECUTION_ERROR"})
        except Exception as exc:
            results.append({"tool_id":tool,"status":"BLOCKED","blocker":f"{type(exc).__name__}:{exc}",
                            "adapter_disposition":"EXECUTION_ERROR"})
    receipt={"source_commit":root.name,"packet_sha256":digest,"tool_ids":ids,
             "adapter_module":provider,"authorized_overrides":sorted(allowed),"scope":"Explicit bounded native input; no independent semantic adjudication or full geometric coverage asserted",
             "results":results}
    a.receipt.write_text(json.dumps(receipt,indent=2,default=str)+"\n")
    print(json.dumps({"source_commit":root.name,"tool_ids":ids,"statuses":[r.get("status") for r in results],"receipt":str(a.receipt)},indent=2))
    return int(not ids or any(r.get("status")!="EXECUTED" for r in results))

if __name__=="__main__":
    raise SystemExit(main())
