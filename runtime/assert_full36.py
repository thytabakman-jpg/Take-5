"""Current-use full ASSERT coverage contract.

This is an operational compatibility patch, not a claim that the historical
two-layer ASSERT semantics or optimal geometry-selection law are fully recovered.

Normal ASSERT must expose all three surfaces:
1. Layer 1: seven protected ASSERT stages across typed D36_C.
2. Layer 2: twenty-two current question families across typed D36_C.
3. Cognitive: four cognitive operators across typed D36_C.

The larger provenance/architecture problem remains explicitly OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from run_geometry import ModeFace
from scope_ontology import Scope


GEOMETRY = "D36_C"

ASSERT_LAYER_1_STAGES: Tuple[str, ...] = (
    "ASSERT",
    "COMPARE_1",
    "RESOLVE",
    "HERE",
    "COMPARE_2",
    "INQUIRE",
    "REASSERT",
)

ASSERT_LAYER_2_QUESTION_FAMILIES: Tuple[str, ...] = tuple(
    f"Q{i:02d}" for i in range(1, 23)
)

COGNITIVE_OPERATORS: Tuple[str, ...] = (
    "DIFFERENTIATE",
    "RELATE",
    "RECONSTRUCT",
    "STRENGTHEN",
)


@dataclass(frozen=True)
class D36CCell:
    scope: Scope
    mode_face: ModeFace


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
        )


def d36c_cells() -> tuple[D36CCell, ...]:
    cells = tuple(D36CCell(scope, face) for scope in Scope for face in ModeFace)
    if len(cells) != 36:
        raise RuntimeError("D36_C_NOT_36")
    return cells


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
