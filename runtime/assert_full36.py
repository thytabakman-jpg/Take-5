"""ASSERT-specific projection of the shared configured coverage geometry.

Layer 1 uses the compound ASSERT stage order. Layer 2 and cognitive
coordinates use the shared configured execution definitions. This plan
checks coordinate coverage only; full semantic execution and the optimal
geometry-selection law remain unestablished by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from run_geometry import ModeFace
from scope_ontology import Scope
from configured_run import DEFAULT_GEOMETRY as GEOMETRY, QUESTION_FAMILIES as ASSERT_LAYER_2_QUESTION_FAMILIES, COGNITIVE_OPERATORS
from global_tool_execution import D36CCell, d36c_cells
from assert_compound import ASSERT_STAGE_ORDER as ASSERT_LAYER_1_STAGES


@dataclass(frozen=True)
class AssertFull36Plan:
    geometry: str
    cells: tuple[D36CCell, ...]
    layer_1: tuple[tuple[str, D36CCell], ...]
    layer_2: tuple[tuple[str, D36CCell], ...]
    cognitive: tuple[tuple[str, D36CCell], ...]

    @property
    def complete(self) -> bool:
        return (
            self.geometry == GEOMETRY
            and len(self.cells) == 36
            and len(self.layer_1) == len(ASSERT_LAYER_1_STAGES) * 36
            and len(self.layer_2) == len(ASSERT_LAYER_2_QUESTION_FAMILIES) * 36
            and len(self.cognitive) == len(COGNITIVE_OPERATORS) * 36
            and set(self.cells) == set(d36c_cells())
            and set(self.layer_1) == {(stage, cell) for stage in ASSERT_LAYER_1_STAGES for cell in self.cells}
            and set(self.layer_2) == {(question, cell) for question in ASSERT_LAYER_2_QUESTION_FAMILIES for cell in self.cells}
            and set(self.cognitive) == {(op, cell) for op in COGNITIVE_OPERATORS for cell in self.cells}
        )


def build_assert_full36_plan() -> AssertFull36Plan:
    cells = d36c_cells()
    plan = AssertFull36Plan(
        geometry=GEOMETRY,
        cells=cells,
        layer_1=tuple((stage, cell) for stage in ASSERT_LAYER_1_STAGES for cell in cells),
        layer_2=tuple((question, cell) for question in ASSERT_LAYER_2_QUESTION_FAMILIES for cell in cells),
        cognitive=tuple((op, cell) for op in COGNITIVE_OPERATORS for cell in cells),
    )
    if not plan.complete:
        raise RuntimeError("ASSERT_FULL36_COVERAGE_INCOMPLETE")
    return plan
