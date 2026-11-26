"""Shared program identity and registry schema, independent of executable or historical inventories."""
from dataclasses import dataclass


# I. Generic program specification.
@dataclass(frozen=True)
class ProgramSpec:
    program_id: str
    source: str
    job: str
    required_roles: tuple[str,...]
    protected_outputs: tuple[str,...]
    validation_target: str
    executable: bool=False
    configured_run: str="UNSPECIFIED"
    recursion_owner: str="UNSPECIFIED"
    consequence_scope: str="UNSPECIFIED"
    external_escape: str="UNSPECIFIED"

    def configured_run_complete(self)->bool:
        return all(x!="UNSPECIFIED" for x in (
            self.configured_run,
            self.recursion_owner,
            self.consequence_scope,
            self.external_escape,
        ))

# II. Generic registry operations (no concrete capability inventory).
# The current C01-C49 definitions remain in tool_run_registry.py; importing
# them here would couple the generic schema to a concrete registry.
class ProgramRegistry:
    VALID_ROLES={"K","S","O","G","M","C","R","U"}

    def __init__(self):
        self._items={}

    def register(self,spec:ProgramSpec):
        if spec.program_id in self._items:
            raise ValueError("duplicate program id")
        if not spec.required_roles or not set(spec.required_roles)<=self.VALID_ROLES:
            raise ValueError("invalid or missing role binding")
        if not spec.protected_outputs:
            raise ValueError("missing protected output")
        if not spec.validation_target:
            raise ValueError("missing validation target")
        self._items[spec.program_id]=spec

    def get(self,pid):
        return self._items[pid]

    def ids(self):
        return set(self._items)

    def coverage(self,prefix):
        return {x for x in self._items if x.startswith(prefix)}

    def executable_ids(self):
        return {x for x,s in self._items.items() if s.executable}
