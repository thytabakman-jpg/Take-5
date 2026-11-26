"""Build and validate the universal configured execution plan and its coverage."""
from __future__ import annotations

from dataclasses import dataclass
from configured_run import ConfiguredRunSpec
from execution_profile import (
    COGNITIVE_OPERATORS, DEFAULT_GEOMETRY, DEFAULT_MODE, QUESTION_FAMILIES,
    FULL_INVOCATION_PROFILE, recurrence_engine_for,
)
from run_geometry import ModeFace
from scope_ontology import Scope


class ToolExecutionBlocked(RuntimeError):
    pass


# Universal configured execution plan and coverage validation.

@dataclass(frozen=True)
class D36CCell:
    scope: Scope
    mode_face: ModeFace


@dataclass(frozen=True)
class ToolExecutionPlan:
    tool_id: str
    mode: str
    wrapper_required: bool
    geometry: str
    recurrence_required: bool
    recurrence_engine: str
    invocation_profile: str
    cells: tuple[D36CCell, ...]
    native: tuple[tuple[str, D36CCell], ...]
    questions: tuple[tuple[str, D36CCell], ...]
    cognitive: tuple[tuple[str, D36CCell], ...]

    def summary(self, *, include_native_layers: bool = False) -> dict[str, object]:
        """Return shared configured-plan metadata without consumer-specific claims."""
        return {
            "tool_id": self.tool_id,
            "mode": self.mode,
            "wrapper_required": self.wrapper_required,
            "geometry": self.geometry,
            "cell_count": len(self.cells),
            **({"native_layers": tuple(dict.fromkeys(layer for layer, _ in self.native))}
               if include_native_layers else {}),
            "question_count": len(self.questions),
            "cognitive_count": len(self.cognitive),
            "recurrence_required": self.recurrence_required,
            "recurrence_engine": self.recurrence_engine,
            "invocation_profile": self.invocation_profile,
        }

    @property
    def complete(self) -> bool:
        # Cardinality is not coverage: repeated coordinates could displace
        # an entire Scope x ModeFace or question/operator coordinate.
        expected_cells=tuple(D36CCell(scope,face) for scope in Scope for face in ModeFace)
        if (not self.tool_id or self.mode != DEFAULT_MODE or not self.wrapper_required
                or self.geometry != DEFAULT_GEOMETRY or not self.recurrence_required
                or self.invocation_profile != FULL_INVOCATION_PROFILE
                or self.recurrence_engine != recurrence_engine_for(self.tool_id)
                or len(self.cells)!=36 or set(self.cells)!=set(expected_cells)
                or len(set(self.cells))!=36):
            return False
        if (len(self.questions)!=len(QUESTION_FAMILIES)*36
                or set(self.questions)!={(q,c) for q in QUESTION_FAMILIES for c in expected_cells}):
            return False
        if (len(self.cognitive)!=len(COGNITIVE_OPERATORS)*36
                or set(self.cognitive)!={(op,c) for op in COGNITIVE_OPERATORS for c in expected_cells}):
            return False
        if not self.native:
            return False
        layers={name for name,cell in self.native if isinstance(name,str) and name}
        if not layers or len(self.native)!=len(layers)*36:
            return False
        return set(self.native)=={(layer,cell) for layer in layers for cell in expected_cells}


def d36c_cells() -> tuple[D36CCell, ...]:
    cells=tuple(D36CCell(scope,face) for scope in Scope for face in ModeFace)
    if len(cells)!=36:
        raise ToolExecutionBlocked("D36_C_NOT_36")
    return cells


def build_tool_execution_plan(spec: ConfiguredRunSpec, *, requested_mode: str | None=None) -> ToolExecutionPlan:
    if not spec.complete():
        raise ToolExecutionBlocked(f"INCOMPLETE_CONFIGURED_RUN:{spec.tool_id}")

    mode=requested_mode or spec.default_mode
    if mode != DEFAULT_MODE:
        raise ToolExecutionBlocked(f"NON_OBSERVER_TOOL_RUN_FORBIDDEN:{spec.tool_id}")

    cells=d36c_cells()
    plan=ToolExecutionPlan(
        tool_id=spec.tool_id,
        mode=mode,
        wrapper_required=spec.wrapper_required,
        geometry=spec.geometry,
        recurrence_required=spec.recurrence_required,
        recurrence_engine=spec.recurrence_engine,
        invocation_profile=spec.invocation_profile,
        cells=cells,
        native=tuple((layer,cell) for layer in spec.required_layers for cell in cells),
        questions=tuple((question,cell) for question in spec.question_families for cell in cells),
        cognitive=tuple((op,cell) for op in spec.required_cognitive_ops for cell in cells),
    )
    if not plan.complete:
        raise ToolExecutionBlocked(f"GLOBAL_TOOL_EXECUTION_INCOMPLETE:{spec.tool_id}")
    return plan
