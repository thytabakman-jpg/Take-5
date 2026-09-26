"""Configured run identity: tool semantics plus recursive execution contract."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ConfiguredRunSpec:
    tool_id:str
    recursive:bool
    closure_required:bool
    reentry_required:bool
    external_challenge:str
    preserves_open:bool=True
    geometry:str|None=None
    required_layers:tuple[str,...]=()
    required_cognitive_ops:tuple[str,...]=()

    def complete(self):
        base = bool(self.tool_id) and self.closure_required and self.reentry_required and self.external_challenge in {"NONE","WHEN_STRONG_CLAIM","ALWAYS"}
        if self.tool_id == "ASSERT":
            return (
                base
                and self.geometry == "D36_C"
                and self.required_layers == ("ASSERT_LAYER_1","ASSERT_LAYER_2")
                and self.required_cognitive_ops == ("DIFFERENTIATE","RELATE","RECONSTRUCT","STRENGTHEN")
            )
        return base

def validate_specs(specs):
    ids=[s.tool_id for s in specs]
    return len(ids)==len(set(ids)) and all(s.complete() for s in specs)
