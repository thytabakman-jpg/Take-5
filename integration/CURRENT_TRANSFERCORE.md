# CURRENT TRANSFERCORE

Date: 2026-09-27
Status: CURRENT CANDIDATE UNDER VALIDATION

## Identity

Tool
TransferCore

Full mathematics
architecture/TRANSFERCORE_FULL_TOOL_001_2026-09-27.md

Runtime
runtime/transfer_core.py

Configured registry
runtime/tool_run_registry.py

Protected manifest
runtime/tool_manifest.py

Regression
tests/test_transfer_core.py

## Current job

Determine whether one or more source results license material target-side consequences, preserve
the typed relation and provenance, emit non-authoritative handoffs, bind explicit target authority,
apply only separately authorized target transitions, verify them, and reenter when relation or
verification state changes.

## Recovery lineage

The current candidate is reconstructed from the Reaserch TransferCore current pointer, full math,
handoff contract, vNext target-discovery candidate, Max(T) audit, and stale Take-5 PR 76.

The old PR 76 implementation is not merged wholesale. Its recoverable semantics are lifted onto
the current Take-5 tool contracts and the residuals named by its own full-tool document are
implemented before promotion.

## Authority invariant

Transfer admission never grants target mutation authority.

A durable queue entry is not target authority.

A target-side apply function runs only after a unique authority binding and explicit matching
authorization.

## Current residual

No known local TransferCore implementation residual is intentionally carried forward.

A future material witness reopens the affected coordinate.
