"""Artifact-to-work intake bridge.

This module does not decide truth or canonical authority. It guarantees that every
admitted artifact presented to the bridge receives a traversal receipt, that every
configured extraction generator is accounted for, and that material extracted
candidates can enter the existing emergent-admission and Work lifecycle.

Traversal completeness is not semantic completeness.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Callable, Iterable, Mapping, Any

from emergent_admission import ObjectCandidate, Admission, admit
from endogenous_work import WorkItem, WorkKind, WorkStatus


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    content: str
    provenance: tuple[str, ...] = ()

    @property
    def sha256(self) -> str:
        return sha256(self.content.encode("utf-8")).hexdigest()

    @property
    def byte_count(self) -> int:
        return len(self.content.encode("utf-8"))


@dataclass(frozen=True)
class ExtractedCandidate:
    candidate_id: str
    candidate_type: str
    source_artifact: str
    source_span: str
    load_bearing: bool
    known_equivalent: str | None = None
    executable_claim: bool = False
    bound: bool = False
    provenance: tuple[str, ...] = ()
    affected: tuple[str, ...] = ()


@dataclass(frozen=True)
class TraversalReceipt:
    artifact_id: str
    sha256: str
    bytes_covered: int
    complete: bool = True


@dataclass(frozen=True)
class GeneratorReceipt:
    artifact_id: str
    generator_id: str
    status: str
    candidate_ids: tuple[str, ...] = ()
    error: str | None = None


@dataclass(frozen=True)
class IntakeResult:
    traversal: tuple[TraversalReceipt, ...]
    generator_receipts: tuple[GeneratorReceipt, ...]
    candidates: tuple[ExtractedCandidate, ...]
    unresolved_extraction: tuple[str, ...]

    @property
    def traversal_complete(self) -> bool:
        return bool(self.traversal) and all(r.complete for r in self.traversal)


def _normalize_candidate(value: Any, artifact: ArtifactRecord) -> ExtractedCandidate:
    if isinstance(value, ExtractedCandidate):
        return value
    if not isinstance(value, Mapping):
        raise TypeError("generator candidates must be ExtractedCandidate or mapping")
    return ExtractedCandidate(
        candidate_id=str(value.get("candidate_id", "")),
        candidate_type=str(value.get("candidate_type", "")),
        source_artifact=str(value.get("source_artifact", artifact.artifact_id)),
        source_span=str(value.get("source_span", "")),
        load_bearing=bool(value.get("load_bearing", False)),
        known_equivalent=value.get("known_equivalent"),
        executable_claim=bool(value.get("executable_claim", False)),
        bound=bool(value.get("bound", False)),
        provenance=tuple(value.get("provenance", artifact.provenance)),
        affected=tuple(value.get("affected", ())),
    )


def intake(
    artifacts: Iterable[ArtifactRecord],
    generators: Mapping[str, Callable[[ArtifactRecord], Iterable[Any]]],
) -> IntakeResult:
    artifacts = tuple(artifacts)
    traversal = tuple(
        TraversalReceipt(a.artifact_id, a.sha256, a.byte_count, True)
        for a in artifacts
    )

    receipts: list[GeneratorReceipt] = []
    candidates: list[ExtractedCandidate] = []
    unresolved: list[str] = []
    seen: set[tuple[str, str, str]] = set()

    for artifact in artifacts:
        for generator_id, generator in sorted(generators.items()):
            try:
                produced = tuple(
                    _normalize_candidate(x, artifact)
                    for x in generator(artifact)
                )
            except Exception as exc:
                unresolved.append(f"{artifact.artifact_id}:{generator_id}:{type(exc).__name__}")
                receipts.append(
                    GeneratorReceipt(
                        artifact.artifact_id,
                        generator_id,
                        "ERROR",
                        (),
                        f"{type(exc).__name__}:{exc}",
                    )
                )
                continue

            ids = []
            for c in produced:
                key = (c.candidate_id, c.candidate_type, c.source_artifact)
                if key not in seen:
                    seen.add(key)
                    candidates.append(c)
                ids.append(c.candidate_id)
            receipts.append(
                GeneratorReceipt(
                    artifact.artifact_id,
                    generator_id,
                    "COMPLETE",
                    tuple(ids),
                    None,
                )
            )

    return IntakeResult(
        traversal,
        tuple(receipts),
        tuple(candidates),
        tuple(unresolved),
    )


def candidate_admission(candidate: ExtractedCandidate) -> Admission:
    return admit(
        ObjectCandidate(
            object_id=candidate.candidate_id,
            object_type=candidate.candidate_type,
            load_bearing=candidate.load_bearing,
            known_equivalent=candidate.known_equivalent,
            executable_claim=candidate.executable_claim,
            bound=candidate.bound,
        )
    )


def to_work_items(result: IntakeResult) -> tuple[WorkItem, ...]:
    """Route unresolved/admissible material candidates into existing Work state.

    MERGE candidates already resolve to an existing object.
    REJECT candidates are non-load-bearing under the current extraction judgment.
    ACCEPT and OPEN candidates remain visible work so downstream admission/currentness
    can decide their exact effect.
    """
    out = []
    for c in result.candidates:
        disposition = candidate_admission(c)
        if disposition in {Admission.MERGE, Admission.REJECT}:
            continue
        out.append(
            WorkItem(
                work_id=f"artifact-intake:{c.candidate_id}",
                obligation=f"{disposition.value}:{c.candidate_type}:{c.candidate_id}",
                material=True,
                licensed=True,
                reachable=True,
                kind=WorkKind.CANDIDATE,
                status=WorkStatus.CANDIDATE,
                provenance=tuple(c.provenance) + (c.source_artifact, c.source_span),
                target=c.candidate_id,
                relations=tuple(c.affected),
            )
        )
    return tuple(out)


def generator_basis_changed(previous: Iterable[str], current: Iterable[str]) -> bool:
    """Any generator-basis change requires affected-artifact re-evaluation."""
    return tuple(sorted(previous)) != tuple(sorted(current))
