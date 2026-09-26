"""Audit canonical tool-identity reconstruction coverage."""
from dataclasses import dataclass

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
    def status(self):
        return "CLOSED_RELATIVE" if not self.generic_only else "OPEN"

def audit_tool_identities(tool_ids, explicit_tool_ids):
    explicit=set(str(x) for x in explicit_tool_ids)
    rows=[]
    for tool_id in tuple(dict.fromkeys(str(x) for x in tool_ids)):
        status="EXPLICIT_MANIFEST" if tool_id in explicit else "GENERIC_ONLY_OPEN"
        rows.append(ToolIdentityDisposition(tool_id,status))
    return PortfolioIdentityAudit(tuple(rows))
