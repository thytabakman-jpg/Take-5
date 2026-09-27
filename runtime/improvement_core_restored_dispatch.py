"""Governed repository dispatch for Legacy-restored ImprovementCore.

The restored controller requires open-ended semantic generation bindings from the host.
Repository code can govern, validate, persist, and execute those bindings; it cannot
manufacture them. Therefore this dispatch fails OPEN when the semantic provider is absent
or incomplete. It never silently substitutes the older fixed-stage controller while
claiming restored execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from improvement_core_dispatch import (
    IMPROVEMENT_CORE_CONTROLLER,
    resolve_improvement_core_invocation,
)
from improvement_core_legacy_restored import (
    LegacyRestoredResult,
    run_improvement_core_legacy_restored,
)
from improvement_core_upstream import discover_upstream_seed


REQUIRED_PROVIDER_FIELDS=(
    "generate_questions",
    "generate_work",
    "admit_results",
    "update_state",
    "verify_return",
    "fresh_reobserve",
)


@dataclass(frozen=True)
class RestoredSemanticProvider:
    generate_questions:Callable
    generate_work:Callable
    admit_results:Callable
    update_state:Callable
    verify_return:Callable
    fresh_reobserve:Callable
    execute_work:Callable|None=None
    observer_prepare:Callable|None=None
    discovery_closure:Callable|None=None
    provider_id:str="host-semantic-provider"


@dataclass(frozen=True)
class RestoredDispatchResolution:
    controller:str
    entrypoint:str
    provider_id:str|None


@dataclass(frozen=True)
class RestoredDispatchResult:
    resolution:RestoredDispatchResolution
    status:str
    blocker:str|None
    result:LegacyRestoredResult|None


def resolve_restored_improvement_core_invocation(
    user_text:str,
    provider:RestoredSemanticProvider|None,
)->RestoredDispatchResolution:
    current=resolve_improvement_core_invocation(user_text)
    return RestoredDispatchResolution(
        controller=current.controller,
        entrypoint=(
            "runtime.improvement_core_restored_dispatch."
            "dispatch_improvement_core_restored"
        ),
        provider_id=None if provider is None else str(provider.provider_id),
    )


def _provider_missing(provider:Any)->tuple[str,...]:
    if provider is None:
        return REQUIRED_PROVIDER_FIELDS
    missing=[]
    for field in REQUIRED_PROVIDER_FIELDS:
        value=getattr(provider,field,None)
        if not callable(value):
            missing.append(field)
    return tuple(missing)


def dispatch_improvement_core_restored(
    user_text:str,
    *,
    state:Mapping[str,Any]|None,
    semantic_provider:RestoredSemanticProvider|None,
    target:str|None=None,
    job:str|None=None,
    basis:str|None=None,
    corpus:Iterable[Any]|None=None,
    memory:Mapping[str,Any]|None=None,
    configured_tool_adapters:Mapping[str,Callable]|None=None,
    external_adapters:Mapping[str,Callable]|None=None,
    force_external:bool=False,
    allow_external_gap:bool=True,
    authority=frozenset(),
    boundary=None,
    explicit_mode=None,
    observer_risk=None,
    knowledge_ledger=None,
    episode_id:str="restored-dispatch",
    hf2_enabled:bool=True,
    hf2_max_rounds:int=6,
    max_iterations:int=32,
    parent_max_rounds:int=16,
)->RestoredDispatchResult:
    """Dispatch into restored ImprovementCore only when semantic bindings are real."""
    resolution=resolve_restored_improvement_core_invocation(
        user_text,semantic_provider
    )
    if resolution.controller!=IMPROVEMENT_CORE_CONTROLLER:
        return RestoredDispatchResult(
            resolution,"BLOCKED","RESTORED_CONTROLLER_IDENTITY_MISMATCH",None
        )

    missing=_provider_missing(semantic_provider)
    if missing:
        blocker=(
            "RESTORED_SEMANTIC_PROVIDER_REQUIRED"
            if semantic_provider is None
            else "RESTORED_SEMANTIC_PROVIDER_INCOMPLETE:"+",".join(missing)
        )
        return RestoredDispatchResult(resolution,"OPEN",blocker,None)

    supplied=(target is not None,job is not None,basis is not None)
    if any(supplied) and not all(supplied):
        return RestoredDispatchResult(
            resolution,"OPEN","RESTORED_PARTIAL_ENTRY_COORDINATES",None
        )

    prepared=dict(state or {})
    if not any(supplied):
        if corpus is None:
            return RestoredDispatchResult(
                resolution,"OPEN","RESTORED_CORPUS_REQUIRED_FOR_UPSTREAM_DISCOVERY",None
            )
        try:
            seed=discover_upstream_seed(corpus)
        except Exception as exc:
            return RestoredDispatchResult(
                resolution,"OPEN",
                f"RESTORED_UPSTREAM_DISCOVERY_OPEN:{type(exc).__name__}:{exc}",
                None,
            )
        target,job,basis=seed.target,seed.job,seed.basis
        prepared.update(seed.state_delta)

    provider=semantic_provider
    result=run_improvement_core_legacy_restored(
        user_text,
        target=str(target),
        job=str(job),
        basis=str(basis),
        state=prepared,
        memory=dict(memory or {}),
        generate_questions=provider.generate_questions,
        generate_work=provider.generate_work,
        execute_work=provider.execute_work,
        admit_results=provider.admit_results,
        update_state=provider.update_state,
        configured_tool_adapters=configured_tool_adapters,
        discovery_closure=provider.discovery_closure,
        external_adapters=external_adapters,
        force_external=force_external,
        allow_external_gap=allow_external_gap,
        authority=authority,
        boundary=boundary,
        explicit_mode=explicit_mode,
        observer_risk=observer_risk,
        observer_prepare=provider.observer_prepare,
        knowledge_ledger=knowledge_ledger,
        episode_id=episode_id,
        hf2_enabled=hf2_enabled,
        hf2_max_rounds=hf2_max_rounds,
        max_iterations=max_iterations,
        return_verifier=provider.verify_return,
        fresh_reobserve=provider.fresh_reobserve,
        parent_max_rounds=parent_max_rounds,
    )
    return RestoredDispatchResult(
        resolution,result.status,result.blocker,result
    )
