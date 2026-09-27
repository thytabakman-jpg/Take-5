"""Fail-closed admission for authoritative formal-system claims.

Recovery, comparison, diagnosis, and candidate construction may operate on OPEN
objects.  A stronger claim that some displayed mathematics is the CURRENT,
CANONICAL, or EXACT_CURRENT mathematics of a formal object may not.

This gate exists between reconstruction and authoritative emission.  It requires:
- exact object/version/basis/authority identity;
- job-relevant coordinate recovery;
- explicit currentness of the root object;
- explicit admission of any frozen historical dependency;
- dependency closure;
- composition type checking;
- source and authority consistency.

It is deliberately separate from specification_before_transformation.py.
Reconstruction is legal on an OPEN object; authoritative promotion of that
reconstruction is not.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


AUTHORITATIVE_SCOPES = frozenset({
    "CURRENT",
    "CANONICAL",
    "EXACT_CURRENT",
    "CURRENT_FULL",
})

EXACT_NONCURRENT_SCOPES = frozenset({
    "HISTORICAL",
    "CANDIDATE",
    "RECOVERY",
})

KNOWN_SCOPES = AUTHORITATIVE_SCOPES | EXACT_NONCURRENT_SCOPES

PASS_STATUSES = frozenset({"PASS", "RECOVERED", "ADMITTED", "VERIFIED", "CURRENT"})
IDENTIFIED_STATUSES = frozenset({"IDENTIFIED"})
CURRENT_ROOT_STATUSES = frozenset({"CURRENT"})
HISTORICAL_ROOT_STATUSES = frozenset({"CURRENT", "HISTORICAL", "SUPERSEDED"})
CANDIDATE_ROOT_STATUSES = frozenset({"CANDIDATE", "OPEN"})
RECOVERY_ROOT_STATUSES = frozenset({
    "CURRENT", "HISTORICAL", "SUPERSEDED", "CANDIDATE", "OPEN", "BLOCKED", "CONFLICT"
})
DEPENDENCY_DISPOSITIONS = frozenset({
    "CURRENT",
    "ADMITTED_FROZEN",
    "EVIDENCE_ONLY",
})


def _norm(value: Any) -> str:
    return str(value or "").strip().upper()


@dataclass(frozen=True)
class FormalObjectBinding:
    object_id: str
    version_id: str
    basis_id: str
    authority_id: str
    role: str
    identification_status: str
    currentness_status: str
    required_coordinates: frozenset[str]
    recovered_coordinates: frozenset[str]
    invariant_coordinates: frozenset[str] = frozenset()
    source_refs: tuple[str, ...] = ()
    dependency_disposition: str = "CURRENT"
    admitted_by_authority: str | None = None
    load_bearing: bool = True

    @property
    def licensed_coordinates(self) -> frozenset[str]:
        return self.recovered_coordinates | self.invariant_coordinates


@dataclass(frozen=True)
class FormalCompositionPacket:
    claim_scope: str
    bindings: tuple[FormalObjectBinding, ...]
    composition_typecheck: str
    dependency_closure: str
    authority_consistency: str
    source_consistency: str


@dataclass(frozen=True)
class FormalClaimReceipt:
    status: str
    claim_scope: str
    root_object_id: str | None
    root_version_id: str | None
    root_authority_id: str | None
    residuals: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    @property
    def green_licensed(self) -> bool:
        return self.status == "PASS" and not self.residuals


def binding_from_mapping(value: Mapping[str, Any]) -> FormalObjectBinding:
    return FormalObjectBinding(
        object_id=str(value.get("object_id", "")).strip(),
        version_id=str(value.get("version_id", "")).strip(),
        basis_id=str(value.get("basis_id", "")).strip(),
        authority_id=str(value.get("authority_id", "")).strip(),
        role=_norm(value.get("role") or "DEPENDENCY"),
        identification_status=_norm(value.get("identification_status")),
        currentness_status=_norm(value.get("currentness_status")),
        required_coordinates=frozenset(
            str(x) for x in value.get("required_coordinates", ()) if str(x)
        ),
        recovered_coordinates=frozenset(
            str(x) for x in value.get("recovered_coordinates", ()) if str(x)
        ),
        invariant_coordinates=frozenset(
            str(x) for x in value.get("invariant_coordinates", ()) if str(x)
        ),
        source_refs=tuple(str(x) for x in value.get("source_refs", ()) if str(x)),
        dependency_disposition=_norm(
            value.get("dependency_disposition") or "CURRENT"
        ),
        admitted_by_authority=(
            str(value.get("admitted_by_authority")).strip()
            if value.get("admitted_by_authority")
            else None
        ),
        load_bearing=bool(value.get("load_bearing", True)),
    )


def packet_from_mapping(value: Mapping[str, Any] | None) -> FormalCompositionPacket | None:
    if not isinstance(value, Mapping):
        return None
    raw_bindings = value.get("bindings", ())
    if not isinstance(raw_bindings, Sequence) or isinstance(raw_bindings, (str, bytes)):
        return None
    bindings = tuple(
        binding_from_mapping(row)
        for row in raw_bindings
        if isinstance(row, Mapping)
    )
    return FormalCompositionPacket(
        claim_scope=_norm(value.get("claim_scope")),
        bindings=bindings,
        composition_typecheck=_norm(value.get("composition_typecheck")),
        dependency_closure=_norm(value.get("dependency_closure")),
        authority_consistency=_norm(value.get("authority_consistency")),
        source_consistency=_norm(value.get("source_consistency")),
    )


def _root_status_allowed(scope: str, currentness: str) -> bool:
    if scope in AUTHORITATIVE_SCOPES:
        return currentness in CURRENT_ROOT_STATUSES
    if scope == "HISTORICAL":
        return currentness in HISTORICAL_ROOT_STATUSES
    if scope == "CANDIDATE":
        return currentness in CANDIDATE_ROOT_STATUSES
    if scope == "RECOVERY":
        return currentness in RECOVERY_ROOT_STATUSES
    return False


def _binding_residuals(
    binding: FormalObjectBinding,
    *,
    claim_scope: str,
    root_authority_id: str | None,
) -> list[str]:
    residuals: list[str] = []
    tag = binding.object_id or "UNIDENTIFIED"

    if not binding.object_id:
        residuals.append("OBJECT_ID_REQUIRED")
    if not binding.version_id:
        residuals.append(f"VERSION_ID_REQUIRED:{tag}")
    if not binding.basis_id:
        residuals.append(f"BASIS_ID_REQUIRED:{tag}")
    if not binding.authority_id:
        residuals.append(f"AUTHORITY_ID_REQUIRED:{tag}")
    if binding.identification_status not in IDENTIFIED_STATUSES:
        residuals.append(f"IDENTIFICATION_NOT_CLOSED:{tag}")
    if binding.load_bearing and not binding.required_coordinates:
        residuals.append(f"REQUIRED_COORDINATES_REQUIRED:{tag}")
    if binding.load_bearing:
        missing = sorted(binding.required_coordinates - binding.licensed_coordinates)
        residuals.extend(f"UNRECOVERED_COORDINATE:{tag}:{name}" for name in missing)
    if not binding.source_refs:
        residuals.append(f"SOURCE_REFERENCE_REQUIRED:{tag}")

    if binding.role == "ROOT":
        if not _root_status_allowed(claim_scope, binding.currentness_status):
            residuals.append(
                f"ROOT_CURRENTNESS_MISMATCH:{tag}:{binding.currentness_status or 'MISSING'}"
            )
    elif binding.load_bearing:
        disposition = binding.dependency_disposition
        if disposition not in DEPENDENCY_DISPOSITIONS:
            residuals.append(f"DEPENDENCY_DISPOSITION_INVALID:{tag}:{disposition}")
        elif claim_scope in AUTHORITATIVE_SCOPES:
            if binding.currentness_status == "CURRENT" and disposition == "CURRENT":
                pass
            elif disposition == "ADMITTED_FROZEN":
                if not root_authority_id:
                    residuals.append(f"ROOT_AUTHORITY_REQUIRED_FOR_FROZEN:{tag}")
                elif binding.admitted_by_authority != root_authority_id:
                    residuals.append(
                        f"FROZEN_DEPENDENCY_NOT_ADMITTED_BY_ROOT_AUTHORITY:{tag}"
                    )
            elif disposition == "EVIDENCE_ONLY":
                residuals.append(f"LOAD_BEARING_EVIDENCE_ONLY_DEPENDENCY:{tag}")
            else:
                residuals.append(
                    f"DEPENDENCY_CURRENTNESS_MISMATCH:{tag}:{binding.currentness_status or 'MISSING'}"
                )

    return residuals


def assess_formal_claim(
    packet: FormalCompositionPacket | Mapping[str, Any] | None,
) -> FormalClaimReceipt:
    if isinstance(packet, Mapping):
        packet = packet_from_mapping(packet)
    if packet is None:
        return FormalClaimReceipt(
            status="OPEN",
            claim_scope="",
            root_object_id=None,
            root_version_id=None,
            root_authority_id=None,
            residuals=("FORMAL_COMPOSITION_PACKET_REQUIRED",),
            evidence_refs=(),
        )

    scope = _norm(packet.claim_scope)
    residuals: list[str] = []
    if scope not in KNOWN_SCOPES:
        residuals.append("CLAIM_SCOPE_REQUIRED")

    roots = tuple(b for b in packet.bindings if b.role == "ROOT" and b.load_bearing)
    if len(roots) != 1:
        residuals.append(f"EXACTLY_ONE_LOAD_BEARING_ROOT_REQUIRED:{len(roots)}")
        root = roots[0] if roots else None
    else:
        root = roots[0]

    root_authority_id = root.authority_id if root else None

    for binding in packet.bindings:
        if not binding.load_bearing and binding.role != "ROOT":
            # Non-load-bearing evidence may be stale by design, but it still needs
            # exact identity/provenance when cited as evidence.
            if not binding.object_id:
                residuals.append("EVIDENCE_OBJECT_ID_REQUIRED")
            if not binding.version_id:
                residuals.append(
                    f"EVIDENCE_VERSION_ID_REQUIRED:{binding.object_id or 'UNIDENTIFIED'}"
                )
            if not binding.source_refs:
                residuals.append(
                    f"EVIDENCE_SOURCE_REFERENCE_REQUIRED:{binding.object_id or 'UNIDENTIFIED'}"
                )
            continue
        residuals.extend(
            _binding_residuals(
                binding,
                claim_scope=scope,
                root_authority_id=root_authority_id,
            )
        )

    checks = (
        ("COMPOSITION_TYPECHECK", packet.composition_typecheck),
        ("DEPENDENCY_CLOSURE", packet.dependency_closure),
        ("AUTHORITY_CONSISTENCY", packet.authority_consistency),
        ("SOURCE_CONSISTENCY", packet.source_consistency),
    )
    for name, status in checks:
        if status not in PASS_STATUSES:
            residuals.append(f"{name}_NOT_PASS:{status or 'MISSING'}")

    evidence_refs = tuple(
        dict.fromkeys(
            ref
            for binding in packet.bindings
            for ref in binding.source_refs
            if ref
        )
    )

    status = "PASS" if not residuals else "OPEN"
    if any("CONFLICT" in r for r in residuals):
        status = "CONFLICT"
    if any(b.currentness_status == "BLOCKED" for b in packet.bindings if b.load_bearing):
        status = "BLOCKED"

    return FormalClaimReceipt(
        status=status,
        claim_scope=scope,
        root_object_id=root.object_id if root else None,
        root_version_id=root.version_id if root else None,
        root_authority_id=root.authority_id if root else None,
        residuals=tuple(dict.fromkeys(residuals)),
        evidence_refs=evidence_refs,
    )


def claim_green_licensed(
    packet: FormalCompositionPacket | Mapping[str, Any] | None,
) -> bool:
    return assess_formal_claim(packet).green_licensed


FORMAL_OUTPUT_MARKERS=(
    "show me the math",
    "actual math",
    "full math",
    "current math",
    "current mathematics",
    "canonical math",
    "canonical mathematics",
    "exact math",
    "exact mathematics",
    "equation",
    "equations",
)

FORMAL_SYSTEM_MARKERS=(
    "tool",
    "device",
    "controller",
    "system",
    "core",
    "icc",
    "assert",
    "goal",
    "mt",
    "pd",
    "hf1",
    "hf2",
    "wrapper",
    "improvementcore",
    "improve core",
)


def request_requires_formal_claim_receipt(
    user_text: str,
    *,
    target: str | None = None,
    job: str | None = None,
) -> bool:
    """Detect repository-governed requests that emit formal-system mathematics.

    This is intentionally narrower than every mathematical question.  It looks
    for an explicit math/equation request plus a formal-system/device target.
    Callers may also force the requirement by placing
    formal_claim_receipt_required=True in the parent-return context.
    """
    combined=" ".join(
        str(x or "") for x in (user_text,target,job)
    ).lower()
    wants_formal_output=any(marker in combined for marker in FORMAL_OUTPUT_MARKERS)
    names_system=any(marker in combined for marker in FORMAL_SYSTEM_MARKERS)
    return wants_formal_output and names_system
