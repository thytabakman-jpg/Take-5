"""Audit canonical tool-identity reconstruction coverage.

This audit is an identity/protected-manifest check, not an invocation receipt.
Malformed, duplicate or incomplete explicit registry entries remain OPEN.
"""
from dataclasses import dataclass
from collections.abc import Mapping

@dataclass(frozen=True)
class ToolIdentityDisposition:
    tool_id:str
    status:str

@dataclass(frozen=True)
class PortfolioIdentityAudit:
    dispositions:tuple[ToolIdentityDisposition,...]

    @property
    def explicit(self):
        return tuple(x.tool_id for x in self.dispositions if x.status=="EXPLICIT_MANIFEST")

    @property
    def generic_only(self):
        return tuple(x.tool_id for x in self.dispositions if x.status=="GENERIC_ONLY_OPEN")

    @property
    def unresolved(self):
        return tuple(x.tool_id for x in self.dispositions if x.status!="EXPLICIT_MANIFEST")

    @property
    def status(self):
        return "CLOSED_RELATIVE" if not self.unresolved else "OPEN"

def audit_tool_identities(tool_ids, explicit_tool_ids):
    explicit=set(str(x) for x in explicit_tool_ids)
    rows=[]
    seen=set()
    for raw in tool_ids:
        tool_id=str(raw)
        if not tool_id.strip():
            status="INVALID_TOOL_ID_OPEN"
        elif tool_id in seen:
            status="DUPLICATE_TOOL_ID_OPEN"
        elif tool_id not in explicit:
            status="GENERIC_ONLY_OPEN"
        elif isinstance(explicit_tool_ids,Mapping):
            obj=explicit_tool_ids.get(tool_id)
            try:
                valid=(obj is not None and obj.tool_id==tool_id and obj.complete())
            except (AttributeError,TypeError,ValueError):
                valid=False
            status="EXPLICIT_MANIFEST" if valid else "INVALID_MANIFEST_OPEN"
        else:
            # Non-mapping collections only attest membership, not manifest quality.
            status="EXPLICIT_MANIFEST"
        rows.append(ToolIdentityDisposition(tool_id,status))
        seen.add(tool_id)
    return PortfolioIdentityAudit(tuple(rows))
