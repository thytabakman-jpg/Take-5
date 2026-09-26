# ImprovementCore Run — Configured Tool Durable Knowledge Capture

Date: 2026-09-26
Controller: IC-028 / ImprovementCore
Entry mode: OBSERVE_DECOUPLED
Default local recurrence: HF002
Input role: GOAL_RESULT_PLUS_WHOLE_EVIDENCE
Goal result: artifacts/improvecore/GOAL_WHOLE_EVIDENCE_ANTI_LOSS_2026-09-26.md

## Parent reconstruction

ImprovementCore consumed the GOAL result as evidence, not authority.

The parent compared the broader anti-loss objective against:

- current configured-tool execution;
- HF002 round traces;
- current ImprovementCore durable knowledge capture;
- prior whole-history reconstruction;
- conversation-capture failures;
- prior MT persistence observer result.

The parent rejected an MT-only persistence patch because the demonstrated seam is generic to configured tools.

## Real problem selected

A material configured-tool execution can be real, full-profile, HF2-governed, and consumed by the controller while its material result remains only in transient `configured_tool_outputs`.

Existing durable knowledge capture automatically records:

1. explicit `knowledge_events`;
2. recursive ImprovementCore material traces.

It did not automatically record configured-tool material results.

That creates the shared loss path:

configured formal tool
-> execution
-> HF2
-> transient configured_tool_outputs
-?> durable interconnected knowledge.

## Repair

The shared configured-tool bridge now preserves:

- material_delta;
- related_objects;
- dependency_footprint;
- affected_objects.

The ImprovementCore regime now scans configured-tool recurrence traces and durably records every material HF2 round as a MATERIAL_TRANSITION knowledge node.

Each node carries:

- tool identity;
- execution basis;
- provenance route;
- evidence references;
- configured invocation dependencies;
- explicit dependency footprint;
- related objects;
- affected objects;
- execution truth;
- recurrence metadata;
- typed CAPTURED disposition.

When a configured tool uses SELF recurrence or has no HF2 trace, the material final output is captured directly.

Repeated identical knowledge merges by stable knowledge identity rather than multiplying unconnected copies.

## Anti-loss invariant

For every material configured-tool round m for tool T that crosses the governed ImprovementCore path:

MaterialConfiguredRound(m,T)
=>
Exists k [
  DurableKnowledgeNode(k)
  AND Represents(k,m)
  AND Related(k,T)
  AND BasisLinked(k)
  AND ProvenanceLinked(k)
].

Additional dependency/evidence/affected-object links supplied by the tool are retained rather than discarded.

## Why this is the shared repair

This applies to MT, GOAL, ASSERT, PD, RootCause, Architecture, and every other registered configured tool that crosses the ImprovementCore bridge.

It does not redefine MT as a storage subsystem.

It makes material tool output persistence a governed system invariant, which is the broader anti-loss objective recovered from the evidence.

## Raw ZIP boundary

The user reports two ZIP archives in GitHub. Their raw objects were not discoverable through the currently connected repository surfaces searched in this run. Archive-derived normalized evidence already persisted in the repositories was used. No claim of byte-level ZIP consumption is made.

## Validation added

Regression coverage now requires:

- configured-tool output state preserves `material_delta`;
- a two-round material HF2 configured-tool execution creates two durable knowledge nodes;
- related objects survive;
- dependency footprints survive;
- evidence references survive;
- nodes survive a fresh KnowledgeLedger reload.

## Parent disposition

Repository-owned shared generator: REPAIRED_ON_BRANCH.
Universal host capture/interception: OPEN / external boundary.
Exact raw-ZIP evidence consumption: OPEN pending discoverable raw objects.
Global all-history completeness: OPEN.

No new peer architecture was created.
