"""Canonical repository-owned gateway for direct formal-tool commands.

The gateway recognizes explicit imperative formal-tool requests, resolves the
current registered identity, binds the current full configured plan, and reuses
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
        return bool(self.tool_ids) and len(self.tool_ids)==len(self.bindings)


def _known_command_pattern():
    aliases=aliases_by_length()
    labels="|".join(re.escape(alias) for alias in aliases)
    return re.compile(
        rf"\b(?:run|use|execute|apply|call)\s+(?:(?:the|a)\s+)?(?P<label>{labels})(?=\b|$)",
        flags=re.IGNORECASE,
    )


KNOWN_COMMAND_PATTERN=_known_command_pattern()

FORMALISH_TOKEN_PATTERN=re.compile(
    r"\b(?:run|use|execute|apply|call)\s+(?:(?:the|a)\s+)?(?P<label>[A-Za-z][A-Za-z0-9_-]*)",
    flags=re.IGNORECASE,
)


def direct_tool_ids(user_text:str)->tuple[str,...]:
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

    if out:
        return tuple(out)

    # Fail closed for formal-looking single-token commands outside the current
    # configured repertoire, while ordinary prose such as "use this" remains
    # outside the formal-tool gateway.
    fallback=FORMALISH_TOKEN_PATTERN.search(text)
    if fallback:
        raw=fallback.group("label")
        try:
            canonical=canonical_formal_label(raw)
        except KeyError:
            return ()
        if canonical not in CONFIGURED_RUNS:
            raise DirectToolCommandBlocked(
                f"DIRECT_TOOL_NOT_REGISTERED:{canonical}"
            )

    return ()


def bind_direct_tool_commands(
    user_text:str,
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
        bound_state,bindings=bind_selected_tools(selected)
    except ToolBridgeBlocked as exc:
        raise DirectToolCommandBlocked(str(exc)) from exc

    bound_state={
        **bound_state,
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
    user_text:str,
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
