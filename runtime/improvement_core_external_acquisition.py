"""External evidence/tool acquisition policy for ImprovementCore.

ImprovementCore must not default to expensive internal reconstruction when a
live outside source/tool can reduce uncertainty or execution cost.

This module is host-agnostic. Hosts expose outside capabilities as named
adapters. The policy decides whether to use them, continue internally, or
leave a typed OPEN gap.

Typed BOUND_ZIP outputs are consumed before controller stages. Exact bytes are
verified by the bound-ZIP adapter, text members cross the existing ArtifactRecord
and artifact-intake path, generated material work is lifted into obligations,
and raw archive bytes are not persisted in controller evidence.
"""
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Mapping

from archive_artifact_intake import (
    ArchiveBindingError,
    GitHubArtifactRef,
    expand_bound_zip,
)
from artifact_intake import intake as intake_artifacts
from artifact_intake import to_work_items


class ExternalDisposition(str, Enum):
    NOT_NEEDED="NOT_NEEDED"
    ACQUIRE="ACQUIRE"
    OPEN_GAP="OPEN_GAP"


@dataclass(frozen=True)
class ExternalAcquisitionDecision:
    disposition: ExternalDisposition
    preferred: tuple[str,...]
    reasons: tuple[str,...]
    allow_internal_fallback: bool
    expected_value: float


@dataclass(frozen=True)
class ExternalAcquisitionReceipt:
    decision: ExternalAcquisitionDecision
    used: tuple[str,...]
    outputs: tuple[dict,...]
    unresolved: tuple[str,...]


DEFAULT_PRIORITY=(
    "connected_sources",
    "repository_research",
    "web_search",
    "external_tools",
)

EXTERNAL_SIGNAL_KEYS={
    "external_dependency",
    "currentness_unknown",
    "fresh_information_required",
    "outside_evidence_required",
    "prior_art_required",
    "literature_required",
    "research_needed",
    "external_tool_candidate",
    "tool_gap",
    "unknown_external_fact",
}

BOUND_ZIP_KIND="BOUND_ZIP"


def _truthy_signals(state:Any)->tuple[str,...]:
    if not isinstance(state,dict):
        return ()
    found=[]
    for key in EXTERNAL_SIGNAL_KEYS:
        if state.get(key):
            found.append(key)
    tags=set(state.get("tags",()) or ())
    if {"external_dependency","novelty","prior_art","stale_version","currentness"} & tags:
        found.extend(sorted({"tag:"+x for x in tags & {"external_dependency","novelty","prior_art","stale_version","currentness"}}))
    return tuple(sorted(set(found)))


def decide_external_acquisition(
    state:Any,
    *,
    available:tuple[str,...]=(),
    force_external:bool=False,
    allow_gap:bool=True,
    internal_cost:float=1.0,
    external_cost:float=0.25,
    uncertainty_reduction:float=1.0,
)->ExternalAcquisitionDecision:
    signals=_truthy_signals(state)
    needed=force_external or bool(signals)
    if not needed:
        return ExternalAcquisitionDecision(
            ExternalDisposition.NOT_NEEDED,(),(),True,0.0
        )

    preferred=tuple(x for x in DEFAULT_PRIORITY if x in set(available))
    ev=float(uncertainty_reduction + internal_cost - external_cost)

    if preferred and ev>0:
        return ExternalAcquisitionDecision(
            ExternalDisposition.ACQUIRE,
            preferred,
            signals or ("forced_external",),
            False,
            ev,
        )

    if allow_gap:
        return ExternalAcquisitionDecision(
            ExternalDisposition.OPEN_GAP,
            preferred,
            signals or ("forced_external",),
            False,
            ev,
        )

    return ExternalAcquisitionDecision(
        ExternalDisposition.NOT_NEEDED,
        (),
        signals or ("forced_external",),
        True,
        ev,
    )


def _github_artifact_ref(value:Any)->GitHubArtifactRef:
    if isinstance(value,GitHubArtifactRef):
        return value
    if not isinstance(value,Mapping):
        raise ArchiveBindingError("BOUND_ZIP_ARTIFACT_REF_REQUIRED")
    required=(
        "repository",
        "object_class",
        "stable_id",
        "source_ref",
        "observed_name",
        "expected_byte_count",
        "expected_sha256",
        "observed_at",
    )
    missing=[key for key in required if key not in value]
    if missing:
        raise ArchiveBindingError(
            "BOUND_ZIP_ARTIFACT_REF_INCOMPLETE:"+",".join(missing)
        )
    return GitHubArtifactRef(
        repository=str(value["repository"]),
        object_class=str(value["object_class"]),
        stable_id=str(value["stable_id"]),
        source_ref=str(value["source_ref"]),
        observed_name=str(value["observed_name"]),
        expected_byte_count=int(value["expected_byte_count"]),
        expected_sha256=str(value["expected_sha256"]),
        observed_at=str(value["observed_at"]),
    )


def _route_bound_zip_output(value:dict)->tuple[dict,tuple[str,...]]:
    if str(value.get("artifact_kind",""))!=BOUND_ZIP_KIND:
        return value,()

    source=_github_artifact_ref(value.get("artifact_ref"))
    data=value.get("archive_bytes")
    if not isinstance(data,(bytes,bytearray)):
        raise ArchiveBindingError("BOUND_ZIP_ARCHIVE_BYTES_REQUIRED")

    expansion=expand_bound_zip(bytes(data),source)
    generators=value.get("artifact_generators") or {}
    if not isinstance(generators,Mapping):
        raise ArchiveBindingError("BOUND_ZIP_GENERATORS_REQUIRE_MAPPING")

    intake_result=intake_artifacts(expansion.text_artifacts,generators)
    work_items=to_work_items(intake_result)

    unresolved=list(expansion.unresolved)
    unresolved.extend(intake_result.unresolved_extraction)
    if bool(value.get("require_semantic_extraction")) and not generators:
        unresolved.append("BOUND_ZIP_SEMANTIC_GENERATOR_BASIS_REQUIRED")

    sanitized={
        key:item for key,item in value.items()
        if key not in {
            "archive_bytes",
            "artifact_ref",
            "artifact_generators",
            "require_semantic_extraction",
        }
    }
    sanitized.update({
        "status":"OPEN" if unresolved else str(value.get("status","EXECUTED")),
        "bound_zip_processed":True,
        "bound_zip_source":asdict(source),
        "archive_byte_count":expansion.archive_byte_count,
        "archive_sha256":expansion.archive_sha256,
        "archive_declared_members":expansion.declared_members,
        "archive_traversal_complete":expansion.traversal_complete,
        "archive_member_receipts":tuple(
            asdict(row) for row in expansion.member_receipts
        ),
        "artifact_traversal_receipts":tuple(
            asdict(row) for row in intake_result.traversal
        ),
        "artifact_generator_receipts":tuple(
            asdict(row) for row in intake_result.generator_receipts
        ),
        "artifact_candidates":tuple(
            asdict(row) for row in intake_result.candidates
        ),
        "external_artifacts":expansion.text_artifacts,
        "artifact_work_items":work_items,
        "unresolved":tuple(unresolved),
    })
    return sanitized,tuple(unresolved)


def acquire_external(
    state:Any,
    adapters:Mapping[str,Callable[[Any],dict]]|None,
    *,
    force_external:bool=False,
    allow_gap:bool=True,
)->ExternalAcquisitionReceipt:
    adapters=dict(adapters or {})
    decision=decide_external_acquisition(
        state,
        available=tuple(adapters),
        force_external=force_external,
        allow_gap=allow_gap,
    )
    if decision.disposition!=ExternalDisposition.ACQUIRE:
        unresolved=decision.reasons if decision.disposition==ExternalDisposition.OPEN_GAP else ()
        return ExternalAcquisitionReceipt(decision,(),(),tuple(unresolved))

    used=[]
    outputs=[]
    unresolved=[]
    for name in decision.preferred:
        fn=adapters.get(name)
        if fn is None:
            continue
        out=fn(state)
        used.append(name)
        if isinstance(out,dict):
            routed_unresolved=()
            try:
                out,routed_unresolved=_route_bound_zip_output(out)
            except ArchiveBindingError as exc:
                out={
                    key:item for key,item in out.items()
                    if key not in {
                        "archive_bytes",
                        "artifact_ref",
                        "artifact_generators",
                        "require_semantic_extraction",
                    }
                }
                out.update({
                    "status":"BLOCKED",
                    "bound_zip_processed":False,
                    "bound_zip_error":f"{type(exc).__name__}:{exc}",
                })
                routed_unresolved=(f"{name}:BOUND_ZIP_BINDING:{exc}",)

            outputs.append(out)
            unresolved.extend(routed_unresolved)
            if out.get("status") in {"OPEN","BLOCKED","CONFLICT"}:
                unresolved.append(f"{name}:{out.get('status')}")

            if (
                out.get("external_need_satisfied")
                and out.get("status") not in {"OPEN","BLOCKED","CONFLICT"}
                and not routed_unresolved
            ):
                break
        else:
            outputs.append({"value":out})

    if not used:
        unresolved.extend(decision.reasons)

    unresolved=tuple(dict.fromkeys(str(x) for x in unresolved if str(x)))
    if unresolved and decision.disposition==ExternalDisposition.ACQUIRE and allow_gap:
        decision=ExternalAcquisitionDecision(
            ExternalDisposition.OPEN_GAP,
            decision.preferred,
            tuple(dict.fromkeys(decision.reasons+unresolved)),
            False,
            decision.expected_value,
        )

    return ExternalAcquisitionReceipt(
        decision,
        tuple(used),
        tuple(outputs),
        unresolved,
    )


def merge_external_outputs(state:Any, receipt:ExternalAcquisitionReceipt):
    if not isinstance(state,dict):
        return state
    out=dict(state)
    out["external_acquisition_receipt"]={
        "disposition":receipt.decision.disposition.value,
        "preferred":receipt.decision.preferred,
        "reasons":receipt.decision.reasons,
        "expected_value":receipt.decision.expected_value,
        "used":receipt.used,
        "unresolved":receipt.unresolved,
    }

    evidence=list(out.get("external_evidence",()) or ())
    external_artifacts=list(out.get("external_artifacts",()) or ())
    obligations=list(out.get("obligations",()) or ())
    archive_receipts=list(out.get("external_archive_receipts",()) or ())

    for item in receipt.outputs:
        if not isinstance(item,dict):
            evidence.append(item)
            continue

        external_artifacts.extend(item.get("external_artifacts",()) or ())
        obligations.extend(item.get("artifact_work_items",()) or ())

        if item.get("bound_zip_processed"):
            archive_receipts.append({
                "bound_zip_source":item.get("bound_zip_source"),
                "archive_byte_count":item.get("archive_byte_count"),
                "archive_sha256":item.get("archive_sha256"),
                "archive_declared_members":item.get("archive_declared_members"),
                "archive_traversal_complete":item.get("archive_traversal_complete"),
                "archive_member_receipts":item.get("archive_member_receipts",()),
                "artifact_traversal_receipts":item.get("artifact_traversal_receipts",()),
                "artifact_generator_receipts":item.get("artifact_generator_receipts",()),
                "artifact_candidates":item.get("artifact_candidates",()),
                "unresolved":item.get("unresolved",()),
            })

        evidence.append({
            key:value for key,value in item.items()
            if key not in {"external_artifacts","artifact_work_items"}
        })

    out["external_evidence"]=tuple(evidence)
    if external_artifacts:
        out["external_artifacts"]=tuple(external_artifacts)
    if obligations:
        out["obligations"]=tuple(obligations)
    if archive_receipts:
        out["external_archive_receipts"]=tuple(archive_receipts)
    return out
