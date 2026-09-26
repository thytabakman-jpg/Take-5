"""Global configured-run identity for all registered tools."""
from dataclasses import dataclass

DEFAULT_GEOMETRY="D36_C"
DEFAULT_MODE="OBSERVER"
QUESTION_FAMILIES=tuple(f"Q{i:02d}" for i in range(1,23))
COGNITIVE_OPERATORS=("DIFFERENTIATE","RELATE","RECONSTRUCT","STRENGTHEN")

@dataclass(frozen=True)
class ConfiguredRunSpec:
    tool_id:str
    recursive:bool
    closure_required:bool
    reentry_required:bool
    external_challenge:str
    preserves_open:bool=True
    wrapper_required:bool=True
    default_mode:str=DEFAULT_MODE
    geometry:str=DEFAULT_GEOMETRY
    required_layers:tuple[str,...]=("NATIVE_TOOL",)
    question_families:tuple[str,...]=QUESTION_FAMILIES
    required_cognitive_ops:tuple[str,...]=COGNITIVE_OPERATORS

    def complete(self):
        return (
            bool(self.tool_id)
            and self.recursive
            and self.closure_required
            and self.reentry_required
            and self.external_challenge in {"NONE","WHEN_STRONG_CLAIM","ALWAYS"}
            and self.preserves_open
            and self.wrapper_required
            and self.default_mode == DEFAULT_MODE
            and self.geometry == DEFAULT_GEOMETRY
            and bool(self.required_layers)
            and self.question_families == QUESTION_FAMILIES
            and self.required_cognitive_ops == COGNITIVE_OPERATORS
        )

def validate_specs(specs):
    ids=[s.tool_id for s in specs]
    return len(ids)==len(set(ids)) and all(s.complete() for s in specs)
