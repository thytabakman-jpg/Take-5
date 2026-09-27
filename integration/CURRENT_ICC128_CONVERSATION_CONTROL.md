# Current ICC128 Conversation Control

Date: 2026-09-27
Status: VALIDATED CURRENT REPOSITORY STATE

## Current controller

ICC128 is again a registered current configured tool in Take-5.

Active runtime:
- runtime/icc128_autonomous_controller.py
- runtime/icc128_semantic_generator_adapter.py
- runtime/rho128_policy.py

The frozen ICC128 Legacy snapshot remains separate and unchanged.

## Jane handoff

Jane owns continuity/currentness supervision, not substantive action selection.

Active bridge:
- runtime/jane_icc128_bridge.py

A READY Jane continuity packet becomes explicit ICC128 controller state and memory.
Missing continuity fails OPEN rather than silently inventing state.

## Conversation response selection

Active response gate:
- runtime/adaptive_response_selector.py

Admissible responses must match requested artifact identity and requested format, be exact and complete, contain no unsupported claims or abstraction drift, and not reproduce rejected candidates.

Among admissible responses, choose minimum extra output.

User rejection updates durable episode state and forces reselection.

## Historical recovery guard

Active recovery gate:
- runtime/exact_equation_recovery.py

Exact historical recovery requires an external source receipt.
Derived reconstruction is not exact recovery.
Rejected candidates cannot silently return unless explicitly reopened.

The invented four-family big-union recovery was retracted in:
- provenance/EXACT_FOUR_FAMILY_36_UNION_RECOVERY_REPORT_001_2026-09-27.md

The 36x4 configured-run expression is retained only as a source-backed prior-assistant candidate, not as user-confirmed historical identity:
- provenance/RECOVERED_36X4_IMPROVEMENT_CORE_EQUATION_001_2026-09-27.md

## Validation

Take-5 Validation run 36298980965: SUCCESS.

The active repository path now covers:
Jane continuity -> ICC128 state-relative selection -> execution/reselection -> exact recovery gate -> minimal response selection.

## External boundary

Repository code cannot force a ChatGPT host to display a separate ICC128 UI identity or green presence dot and cannot universally intercept a host that bypasses Take-5.

Do not claim that external host state from repository evidence alone.
