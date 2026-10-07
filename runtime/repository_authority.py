"""Fail-closed repository authority routing for Take-5 governed work.

Authority is derived from MIGRATION_STATE.yaml. This module does not mint a new
authority registry. It makes the existing migration authority executable.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import yaml

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/"MIGRATION_STATE.yaml"

CANONICAL_MUTATION_OPS={
    "MUTATE","WRITE","CREATE","UPDATE","DELETE","PROMOTE","MERGE","CANONICAL_CHANGE"
}
READ_ONLY_OPS={"READ","SEARCH","INSPECT","COMPARE","RECOVER_EVIDENCE"}

@dataclass(frozen=True)
class RepositoryAuthorityReceipt:
    repository:str
    operation:str
    status:str
    role:str
    canonical_effect:bool
    mutation_allowed:bool
    current_repository:str
    evidence_only:bool
    reason:str

    def payload(self)->dict[str,Any]:
        return asdict(self)

class RepositoryAuthorityError(RuntimeError):
    pass

def _load()->dict[str,Any]:
    data=yaml.safe_load(STATE.read_text(encoding="utf-8")) or {}
    if not isinstance(data,dict):
        raise RepositoryAuthorityError("REPOSITORY_AUTHORITY_STATE_INVALID")
    return data

def assess_repository_operation(repository:str, operation:str)->RepositoryAuthorityReceipt:
    data=_load()
    current=str(data.get("current_repository") or "")
    roles=data.get("repository_roles") or {}
    if not current:
        raise RepositoryAuthorityError("REPOSITORY_AUTHORITY_CURRENT_REPOSITORY_MISSING")
    if not isinstance(roles,dict):
        raise RepositoryAuthorityError("REPOSITORY_AUTHORITY_ROLES_INVALID")

    op=str(operation or "").strip().upper()
    repo=str(repository or "").strip()
    row=roles.get(repo)
    if not isinstance(row,dict):
        return RepositoryAuthorityReceipt(
            repository=repo,
            operation=op,
            status="OPEN",
            role="UNRESOLVED",
            canonical_effect=False,
            mutation_allowed=False,
            current_repository=current,
            evidence_only=True,
            reason="REPOSITORY_ROLE_UNRESOLVED",
        )

    role=str(row.get("role") or "UNRESOLVED")
    canonical_effect=bool(row.get("canonical_effect"))
    is_current=(repo==current and canonical_effect)

    if op in READ_ONLY_OPS:
        return RepositoryAuthorityReceipt(
            repository=repo,
            operation=op,
            status="ADMITTED",
            role=role,
            canonical_effect=canonical_effect,
            mutation_allowed=False,
            current_repository=current,
            evidence_only=not is_current,
            reason="READ_OR_EVIDENCE_ROUTE",
        )

    if op in CANONICAL_MUTATION_OPS:
        if is_current:
            return RepositoryAuthorityReceipt(
                repository=repo,
                operation=op,
                status="ADMITTED",
                role=role,
                canonical_effect=True,
                mutation_allowed=True,
                current_repository=current,
                evidence_only=False,
                reason="CANONICAL_REPOSITORY_MATCH",
            )
        return RepositoryAuthorityReceipt(
            repository=repo,
            operation=op,
            status="BLOCKED",
            role=role,
            canonical_effect=False,
            mutation_allowed=False,
            current_repository=current,
            evidence_only=True,
            reason="NONCANONICAL_REPOSITORY_MUTATION_REQUIRES_RECONCILIATION_TO_CURRENT",
        )

    return RepositoryAuthorityReceipt(
        repository=repo,
        operation=op,
        status="OPEN",
        role=role,
        canonical_effect=canonical_effect,
        mutation_allowed=False,
        current_repository=current,
        evidence_only=not is_current,
        reason="OPERATION_CLASS_UNRESOLVED",
    )

def require_canonical_mutation(repository:str, operation:str="MUTATE")->RepositoryAuthorityReceipt:
    receipt=assess_repository_operation(repository,operation)
    if receipt.status!="ADMITTED" or not receipt.mutation_allowed:
        raise RepositoryAuthorityError(
            f"REPOSITORY_AUTHORITY_BLOCKED:{repository}:{operation}:{receipt.reason}:current={receipt.current_repository}"
        )
    return receipt
