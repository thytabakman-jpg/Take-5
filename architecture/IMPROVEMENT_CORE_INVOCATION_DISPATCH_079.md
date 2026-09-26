# Improvement Core Invocation Dispatch 079

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / VALIDATION REQUIRED

## Problem

The rich Improvement Core manager entry could exist while ordinary user
invocation still reached a different surface.

That would preserve the code but not the activation behavior.

## Rule

Ordinary user phrases naming ImproveCore or Improvement Core resolve to:

runtime.improvement_core_manager.run_improvement_core_manager

with controller identity IC-028.

The narrower runtime/improvement_core.py remains a subordinate capability and
is not the user-facing manager identity.

## Fail-closed condition

If the controller cannot resolve to IC-028, dispatch fails rather than silently
falling back to another controller surface.

## Scope

This repairs repository dispatch identity. It does not claim the external chat
host is forced to execute repository code unless it actually loads and uses this
entry path.
