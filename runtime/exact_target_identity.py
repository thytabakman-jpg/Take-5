"""Exact immutable target identity for repository-aware governed execution.

This is complementary to configured-tool identity. Tool identity answers which
capability ran. Exact target identity answers which repository object/version the
result is evidence about.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Mapping, Any

MUTABLE_SELECTORS={"current","latest","main","master","head","tip","default_branch","default-branch"}
HEX40=re.compile(r"^[0-9a-fA-F]{40}$")
HEX64=re.compile(r"^[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class ExactTargetIdentity:
    repository:str
    object_id:str
    selector_role:str
    immutable_kind:str
    frozen_ref:str
    authority_status:str

    @classmethod
    def from_mapping(cls,row:Mapping[str,Any])->"ExactTargetIdentity":
        return cls(
            repository=str(row.get("repository") or ""),
            object_id=str(row.get("object_id") or ""),
            selector_role=str(row.get("selector_role") or ""),
            immutable_kind=str(row.get("immutable_kind") or ""),
            frozen_ref=str(row.get("frozen_ref") or ""),
            authority_status=str(row.get("authority_status") or ""),
        )

    def evidence_key(self)->tuple[str,str,str,str]:
        return (
            self.repository,
            self.object_id,
            self.immutable_kind,
            self.frozen_ref,
        )


@dataclass(frozen=True)
class ExactTargetAssessment:
    status:str
    missing:tuple[str,...]
    conflicts:tuple[str,...]
    evidence_key:tuple[str,str,str,str]


class ExactTargetIdentityError(RuntimeError):
    pass


def _immutable(kind:str,ref:str)->bool:
    k=kind.strip().lower()
    value=ref.strip()
    if not value or value.lower() in MUTABLE_SELECTORS:
        return False
    tail=value.rsplit("@",1)[-1]
    if k in {"git_commit","commit","git_sha"}:
        return bool(HEX40.fullmatch(tail))
    if k in {"sha256","content_hash","content_sha256"}:
        if tail.lower().startswith("sha256:"):
            tail=tail.split(":",1)[1]
        return bool(HEX64.fullmatch(tail))
    if k in {"immutable_version","version","generation","stable_run_identity"}:
        return value.lower() not in MUTABLE_SELECTORS
    return False


def assess_exact_target(
    identity:ExactTargetIdentity|Mapping[str,Any],
    *,
    expected_repository:str|None=None,
)->ExactTargetAssessment:
    ident=identity if isinstance(identity,ExactTargetIdentity) else ExactTargetIdentity.from_mapping(identity)
    missing=[]
    for field in ("repository","object_id","selector_role","immutable_kind","frozen_ref","authority_status"):
        if not str(getattr(ident,field)).strip():
            missing.append(field)
    conflicts=[]
    if ident.immutable_kind and ident.frozen_ref and not _immutable(ident.immutable_kind,ident.frozen_ref):
        conflicts.append("IMMUTABLE_TARGET_BASIS_INVALID")
    if expected_repository and ident.repository and ident.repository!=expected_repository:
        conflicts.append(
            f"CANONICAL_REPOSITORY_MISMATCH:{ident.repository}!={expected_repository}"
        )
    status="PASS" if not missing and not conflicts else ("CONFLICT" if conflicts else "OPEN")
    return ExactTargetAssessment(status,tuple(missing),tuple(conflicts),ident.evidence_key())


def require_exact_target(
    identity:ExactTargetIdentity|Mapping[str,Any],
    *,
    expected_repository:str|None=None,
)->ExactTargetAssessment:
    out=assess_exact_target(identity,expected_repository=expected_repository)
    if out.status!="PASS":
        raise ExactTargetIdentityError(
            f"EXACT_TARGET_{out.status}:missing={','.join(out.missing)}:"
            f"conflicts={','.join(out.conflicts)}"
        )
    return out
