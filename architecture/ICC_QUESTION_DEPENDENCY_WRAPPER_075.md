# ICC Question-Dependency Wrapper — Candidate Architecture 075

Status: CANDIDATE / NOT YET CANONICAL  
Date: 2026-09-25  
Provenance: `integration/ICC_WRAPPER_REDESIGN_CONVERSATION_CAPTURE_074_2026-09-25.md`

## Governing objective

ICC is not primarily a next-tool selector.

ICC's governing control question is:

> What remains unsolved relative to the governing goal, and what dependent question must be resolved next to finish it?

Tool selection is downstream of question dependency.

## Candidate pipeline

```
Bind current state
→ Observe^36
→ Freeze
→ ASSERT_pre^36
→ PROBLEM^36
→ ROOT^36
→ 36-question coverage
→ DIFFERENTIATE
→ RELATE
→ RECONSTRUCT
→ STRENGTHEN
→ MTPD^36
→ HF1_local
→ GOAL^36
→ ARCHITECT^36
→ IC-028 inquiry loop
→ ICC-123 residual-distinction pass
→ ICC-128 admission/reentry/closure control
→ PLAN / SOLUTION
→ EXECUTE + receipt + observed effect
→ VERIFY^36
→ ASSERT_post^36
→ GOAL-GAP
→ residual routing
→ TRC^36
→ Update
→ Jane Sync
→ HF1_terminal^36
→ Final Observe^36
→ Response
```

## MTPD block

```
MT_pre^36
→ PD^36
→ PD_Audit^36
→ PD_Multi^36
→ [Blackbox → BasicMath → VerifyMath] when required
→ MT_post^36
```

Purpose:

> Enrich and test the representation enough to define a valid goal.

## GOAL

Question:

> What are we actually trying to accomplish, and exactly what state counts as accomplishing it?

GOAL receives the output of MTPD rather than the raw incoming prompt/state.

## ARCHITECT

Question:

> Given the goal, what design best achieves it under the governing constraints?

"Best"/"ideal" is not primitive. The comparison relation remains an explicit open dependency.

## Four core cognitive operations

The 36-question coverage pass compresses through:

```
DIFFERENTIATE
RELATE
RECONSTRUCT
STRENGTHEN
```

These are coverage/compression operations, not a command to run 36 separate tools blindly.

## ICC lineage integration

- IC-028 supplies inquiry recursion: question → probe/work → evidence → state update → new question.
- ICC-123 supplies residual distinction/reframe/separator discovery.
- ICC-128 supplies admission/state recomputation/reentry/closure control.
- These are dependency-routed, not unconditional tool-smash stages once the full graph is formalized.

## Residual routing

```
diagnostic gap      → PROBLEM / ROOT
representation gap  → 36Q / MTPD
goal gap            → GOAL
design gap          → ARCHITECT
inquiry gap         → IC-028 / ICC-123
execution gap       → PLAN / EXECUTE
verification gap    → VERIFY
no relevant gap     → closure path
```

## Wrapper invariants retained from earlier iterations

- bind current version/authority before analysis;
- Observe before inference;
- Freeze the episode;
- full wrapper + full 36D for registered formal tools unless explicitly diagnostic;
- fail closed rather than silently downgrading;
- execution truth requires receipt/observed effect;
- selection and verification remain separate;
- TRC governs licensed transitions;
- update only after authorized transition;
- Jane synchronization follows update;
- HF1 detects invalidation/reentry;
- final Observe precedes emission.

## HF1

HF1 is treated as both:

1. a local invariant after material discovery stages; and
2. a terminal reentry/closure controller.

Exact HF1 mathematics remains open.

## Deferred architecture problem

Reorganize the entire tool system as a graph of question dependencies.

Provisional tool schema:

```
Tool = <Question, Prerequisites, AnswerType, Enables>
```

This work is deliberately deferred from the current wrapper stabilization task.

## Authority rule

This file is a candidate architecture record. It does not supersede existing canonical wrapper/runtime contracts until audited, reconciled, and explicitly promoted.
