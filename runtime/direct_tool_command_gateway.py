"""Canonical repository-owned gateway for direct formal-tool commands.

The gateway accepts explicit imperative formal-tool requests or structured ordered
lists/tuples of exact registered tool IDs, binds the current full configured plan, and reuses
the shared configured-tool bridge. The bridge owns HF2 recurrence.

This repository cannot force an unrelated external host to enter this gateway.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Mapping

from formal_object_registry import aliases_by_length, canonical_formal_label
from improvement_core_tool_bridge import (
    ConfiguredToolBatchResult,
    ToolBridgeBlocked,
    bind_selected_tools,
    execute_bound_tools,
)
from tool_run_registry import CONFIGURED_RUNS


class DirectToolCommandBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class DirectToolCommandBinding:
    raw_request:str
    tool_ids:tuple[str,...]
    state:Any
    bindings:tuple

    @property
    def complete(self)->bool:
        return bool(self.tool_ids) and self.tool_ids==tuple(binding.tool_id for binding in self.bindings)


def _known_command_pattern():
    aliases=aliases_by_length()
    labels="|".join(re.escape(alias) for alias in aliases)
    return re.compile(
        rf"\b(?:run|use|execute|apply|call)\s+(?:(?:the|a)\s+)?(?P<label>{labels})(?![\w-])",
        flags=re.IGNORECASE,
    )


KNOWN_COMMAND_PATTERN=_known_command_pattern()

FORMALISH_TOKEN_PATTERN=re.compile(
    r"\b(?:run|use|execute|apply|call)\s+(?:(?:the|a)\s+)?(?P<label>[A-Za-z][A-Za-z0-9_-]*)",
    flags=re.IGNORECASE,
)


def direct_tool_ids(user_text:str|list[str]|tuple[str,...])->tuple[str,...]:
    """Resolve legacy lexical commands or validate an explicit ordered ID list.

    Structured requests are caller-authorized exact identities, not natural
    language. Reject the whole request on invalid or repeated IDs before binding.
    """
    if isinstance(user_text,(list,tuple)):
        if not user_text:
            raise DirectToolCommandBlocked("DIRECT_TOOL_COMMAND_NOT_FOUND")
        ids=[]
        for raw in user_text:
            if not isinstance(raw,str) or raw not in CONFIGURED_RUNS:
                raise DirectToolCommandBlocked(f"DIRECT_TOOL_NOT_REGISTERED:{raw!r}")
            if raw in ids:
                raise DirectToolCommandBlocked(f"DIRECT_TOOL_DUPLICATE_ID:{raw}")
            ids.append(raw)
        return tuple(ids)
    text=str(user_text)
    out=[]

    for match in KNOWN_COMMAND_PATTERN.finditer(text):
        raw=match.group("label")
        try:
            canonical=canonical_formal_label(raw)
        except KeyError as exc:
            raise DirectToolCommandBlocked(
                f"DIRECT_TOOL_IDENTITY_UNRESOLVED:{raw}"
            ) from exc
        if canonical not in CONFIGURED_RUNS:
            raise DirectToolCommandBlocked(
                f"DIRECT_TOOL_NOT_REGISTERED:{canonical}"
            )
        if canonical not in out:
            out.append(canonical)

    # Check every formal-looking command, including mixed registered and
    # unregistered requests. Unknown ordinary prose remains outside the gateway.
    for fallback in FORMALISH_TOKEN_PATTERN.finditer(text):
        raw=fallback.group("label")
        try:
            canonical=canonical_formal_label(raw)
        except KeyError:
            continue
        if canonical not in CONFIGURED_RUNS:
            raise DirectToolCommandBlocked(
                f"DIRECT_TOOL_NOT_REGISTERED:{canonical}"
            )

    return tuple(out)



def bind_direct_tool_commands(
    user_text:str|list[str]|tuple[str,...],
    *,
    state:Any|None=None,
)->DirectToolCommandBinding:
    tool_ids=direct_tool_ids(user_text)
    if not tool_ids:
        raise DirectToolCommandBlocked("DIRECT_TOOL_COMMAND_NOT_FOUND")

    current={} if state is None else state
    if not isinstance(current,dict):
        raise DirectToolCommandBlocked("DIRECT_TOOL_STATE_REQUIRES_MAPPING")

    selected={
        **current,
        "selected_tools":tool_ids,
        "direct_tool_command_raw":str(user_text),
        "direct_tool_command_status":"IDENTIFIED",
    }

    try:
        selection_state,bindings=bind_selected_tools({"selected_tools":tool_ids})
    except ToolBridgeBlocked as exc:
        raise DirectToolCommandBlocked(str(exc)) from exc

    # Inherited controller selections are context, not authorization for this command.
    if tuple(binding.tool_id for binding in bindings)!=tool_ids:
        raise DirectToolCommandBlocked("DIRECT_TOOL_BINDING_IDENTITY_MISMATCH")

    bound_state={
        **selected,
        **selection_state,
        "direct_tool_command_status":"BOUND_FULL_CONFIGURED",
        "direct_tool_ids":tool_ids,
    }

    return DirectToolCommandBinding(
        str(user_text),
        tool_ids,
        bound_state,
        bindings,
    )


def execute_direct_tool_commands(
    user_text:str|list[str]|tuple[str,...],
    *,
    state:Any|None=None,
    adapters:Mapping[str,Callable]|None=None,
)->ConfiguredToolBatchResult:
    binding=bind_direct_tool_commands(user_text,state=state)
    out=execute_bound_tools(binding.state,binding.bindings,adapters)

    if isinstance(out.state,dict):
        next_state={
            **out.state,
            "direct_tool_command_status":(
                "EXECUTED_FULL_CONFIGURED"
                if out.status=="EXECUTED"
                else out.status
            ),
        }
        return ConfiguredToolBatchResult(
            next_state,
            out.executions,
            out.status,
            out.blocker,
        )

    return out
