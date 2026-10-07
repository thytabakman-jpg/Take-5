"""Resolve canonical repository authority from Take-5 migration state.

This module turns the already-authoritative migration declaration into a reusable
fail-closed task-entry decision. It does not create a second repository authority map.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
MIGRATION_STATE=ROOT/"MIGRATION_STATE.yaml"


@dataclass(frozen=True)
class RepositoryAuthorityDecision:
    requested_repository:str
    canonical_repository:str
    operation:str
    status:str
    disposition:str
    evidence:tuple[str,...]
    blocker:str|None=None


class RepositoryAuthorityError(RuntimeError):
    pass


def _state()->dict:
    return yaml.safe_load(MIGRATION_STATE.read_text(encoding="utf-8")) or {}


def resolve_repository_authority(
    requested_repository:str,
    *,
    operation:str="READ",
)->RepositoryAuthorityDecision:
    data=_state()
    canonical=str(data.get("current_repository") or "")
    legacy=str((data.get("legacy_baseline") or {}).get("repository") or "")
    legacy_disposition=str((data.get("legacy_baseline") or {}).get("disposition") or "")
    op=str(operation).upper()

    evidence=(
        "MIGRATION_STATE.yaml",
        f"current_repository:{canonical}",
        f"legacy_repository:{legacy}",
        f"legacy_disposition:{legacy_disposition}",
    )

    if not canonical:
        return RepositoryAuthorityDecision(
            str(requested_repository),canonical,op,"OPEN","AUTHORITY_UNRESOLVED",
            evidence,"CANONICAL_REPOSITORY_UNRESOLVED",
        )

    requested=str(requested_repository)
    if requested==canonical:
        return RepositoryAuthorityDecision(
            requested,canonical,op,"PASS","CANONICAL_WORKING",evidence,None,
        )

    if requested==legacy:
        if op in {"READ","RECOVER","COMPARE","RECONCILE","PROVENANCE"}:
            return RepositoryAuthorityDecision(
                requested,canonical,op,"PASS","LEGACY_PROVENANCE_ONLY",evidence,None,
            )
        return RepositoryAuthorityDecision(
            requested,canonical,op,"BLOCKED","LEGACY_PROVENANCE_ONLY",evidence,
            "POST_CUTOVER_LEGACY_MUTATION_REQUIRES_TAKE5_RECONCILIATION",
        )

    return RepositoryAuthorityDecision(
        requested,canonical,op,"BLOCKED","UNKNOWN_REPOSITORY_AUTHORITY",evidence,
        "REPOSITORY_NOT_ADMITTED_BY_MIGRATION_STATE",
    )


def require_repository_authority(
    requested_repository:str,
    *,
    operation:str="READ",
)->RepositoryAuthorityDecision:
    out=resolve_repository_authority(requested_repository,operation=operation)
    if out.status!="PASS":
        raise RepositoryAuthorityError(
            f"REPOSITORY_AUTHORITY_{out.status}:{out.blocker}:"
            f"requested={out.requested_repository}:canonical={out.canonical_repository}"
        )
    return out
