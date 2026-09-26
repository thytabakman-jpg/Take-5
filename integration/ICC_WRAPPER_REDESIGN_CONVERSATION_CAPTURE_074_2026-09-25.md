# ICC Wrapper Redesign Conversation Capture — 2026-09-25

Status: DURABLE CONVERSATION/IDEA CAPTURE  
Repository role: recovery/provenance record  
Authority: not automatically canonical; intended to prevent loss of reasoning and provide reconstruction provenance.

## Why this file exists

The user explicitly requested that the current conversation and its ideas be preserved in GitHub so the path by which the current architecture was reached is recoverable even if chat context is later lost.

This file captures the discussion in chronological semantic order. It preserves both accepted ideas and still-open ideas. It must not be treated as proof that every formula below is final.

## Conversation thread captured

### 1. GOAL invocation rule strengthened

User established:

- whenever GOAL runs, the new robust MT runs first;
- GOAL then runs with the full current wrapper;
- GOAL runs in the full 36-dimensional variant;
- bare/core GOAL is diagnostic-only when explicitly requested.

Recovered invocation form:

```
X
→ Wrapper[MT_robust^36]
→ X'
→ Wrapper[GOAL^36](X')
```

The key semantic requirement is that GOAL receives the state after MT's material discoveries have been incorporated.

### 2. MT, PD, PD Audit, Blackbox relationship

The discussion separated their jobs:

- MT = transformation/re-representation engine. Question: what changes, survives, appears, or disappears under transformation?
- PD = distinction-space expansion. Question: what admissible distinction, assumption, frame, variable, representation, or alternative can change the result?
- PD Audit = result-sensitivity test. Question: which generated distinctions actually alter the protected result?
- Blackbox = unresolved load-bearing state/escalation trigger rather than merely another serial tool.

A useful cycle emerged:

```
MT_pre
→ PD
→ PD Audit
→ PD Multi-Object
→ Blackbox / BasicMath / VerifyMath as required
→ MT_post
```

Reason for MT at both ends: the second MT operates on a richer state produced by PD-family discovery and formal recovery.

### 3. PD Multi-Object

Recovered role:

- do not only run PD independently on x1, x2, x3;
- inspect relations and higher-order structure that only appears jointly;
- route newly discovered distinctions back into PD rather than assuming a one-way chain.

### 4. Candidate combined MTPD block

The combined epistemic-recovery block was provisionally treated as:

```
MTPD*
=
MT_pre
→ PD
→ PD Audit
→ PD Multi
→ Blackbox/Math/Verify
→ MT_post
```

This block belongs before GOAL because the problem representation needs to be enriched before the target is frozen.

### 5. GOAL and ARCHITECT distinction reconstructed

GOAL was sharpened to:

> What are we actually trying to accomplish, and exactly what state counts as accomplishing it?

Architect was corrected away from mere architecture-description and back toward the user's intended optimization question:

> Given the goal, what design best achieves it under the relevant constraints?

Important open issue: "best"/"ideal" are load-bearing and require an explicit comparison relation rather than being left as intuition.

Architect drift diagnosed:

```
design optimization
→ requirements analysis
→ architecture description
```

The lost function was goal-relative design comparison/selection.

GOAL and Architect remain distinct mathematically but may be packaged operationally as a compound DESIGN-like sequence:

```
GOAL → ARCHITECT
```

### 6. Tool system reframed as a dependency graph of questions

Major conceptual discovery:

A tool is fundamentally a question operator whose output is required by some downstream question.

Provisional object:

```
T = <Q_T, Prereq(T), AnswerType(T), Enables(T)>
```

Meaning:

- Q_T = question answered by the tool
- Prereq(T) = questions that must already be answered
- AnswerType(T) = state produced
- Enables(T) = downstream questions made answerable

This creates a deferred GitHub architecture problem: reorganize the tool system by question dependency instead of a flat list. This redesign is intentionally deferred so it does not derail the current ICC-wrapper work.

### 7. Core pre-goal dependency spine

The conversation converged on:

```
ASSERT_pre
→ PROBLEM
→ ROOT
→ MTPD
→ GOAL
```

Questions:

- ASSERT: What can actually be established about the current state?
- PROBLEM: What problem, if any, exists?
- ROOT: What upstream structure generates the problem?
- MTPD: Is the representation rich enough to define the correct target?
- GOAL: What exact state are we trying to make true, and what counts as success?

### 8. From GOAL to intervention

The downstream spine became:

```
GOAL
→ ARCHITECT
→ SOLUTION / PLAN
→ EXECUTE
→ VERIFY
→ ASSERT_post
→ GOAL-GAP
```

Architect selects/designs relative to GOAL.  
Execution must produce receipts/observed effects.  
VERIFY does not self-certify.  
ASSERT_post establishes what is actually true after execution.  
GOAL-GAP compares actual state to the success state.

### 9. ICC controller question identified as wrong

A major diagnosis emerged:

Earlier ICC/ICC-128 framing drifted toward:

> What inquiry/control action or tool comes next?

That can optimize for tool choice rather than problem completion and can explain premature stopping/asking.

Desired controller orientation:

> What remains unsolved relative to the governing goal, and what dependent question must be resolved next to finish it?

ICC therefore becomes a controller over the question-dependency graph rather than a tool picker.

### 10. ICC mandatory entry/exit wrapper

The discussion identified a mandatory pre/post frame:

Entry:

```
ASSERT_pre
→ PROBLEM
→ ROOT
→ MTPD
→ GOAL
```

ICC work:

```
GOAL
→ ARCHITECT / ICC control
→ PLAN
→ EXECUTE
```

Exit:

```
VERIFY
→ ASSERT_post
→ GOAL-GAP
→ {CLOSE, REENTER}
```

The user explicitly recognized that this belongs at the front of every ICC invocation and again before any ICC response is emitted.

### 11. Earlier wrapper lessons reincorporated

The current redesign must retain successful wrapper ideas from prior iterations:

- bind current state/version/authority first;
- Observe;
- Freeze;
- full 36-dimensional execution where required;
- execution truth/receipts;
- verification separated from selection;
- TRC / licensed transition control;
- state update;
- Jane synchronization;
- HF1 re-entry;
- final Observe;
- fail closed rather than silently downgrading to bare/core tools.

Older compact wrapper lineage retained:

```
O^36
→ F^36
→ K_T
→ L_36[K_T]
→ G^36
→ E^36
→ C
→ U
→ TRC^36
→ HF1^36
→ O^36
```

New work interprets/unpacks the vague middle rather than discarding that wrapper.

### 12. HF1 placement clarified

HF1 is not only a final checkbox.

Two roles emerged:

- local HF1 invariant after stages capable of invalidating downstream assumptions;
- terminal HF1 after update/synchronization to determine re-entry/closure.

Conceptually:

```
material relevant delta
→ reenter earliest affected dependency
```

Terminal position:

```
TRC
→ Update
→ Jane Sync
→ HF1_terminal
→ Observe
```

### 13. 36-question / four-core cognitive system reintegrated

Earlier ICC/tool-smash work was revisited.

Key lesson: "run every tool" is inferior to dependency-directed routing.

The large 36-question coverage system belongs early, before GOAL, as a coverage/discovery pass. It then compresses through four core cognitive operations:

```
DIFFERENTIATE
RELATE
RECONSTRUCT
STRENGTHEN
```

The 36-question coverage system is not treated as 36 separate always-run tools.

### 14. Other ICC lineage lessons

Recovered roles from earlier ICC work:

- IC-028: question → probe/work → evidence → state update → new question loop
- ICC-123: residual distinctions, reframes, separators, missing possibilities, unresolved structure
- ICC-128: admission, state recomputation, reentry/closure control

Important correction: these are not to be stacked blindly. They are routed by question/job.

### 15. Current proposed end-to-end order after self-application

The self-test produced this current ordered candidate:

```
1. Bind current state
2. Observe^36
3. Freeze
4. ASSERT_pre^36
5. PROBLEM^36
6. ROOT^36
7. 36-question coverage
8. Four-core cognitive compression
   - DIFFERENTIATE
   - RELATE
   - RECONSTRUCT
   - STRENGTHEN
9. MTPD^36
   - MT_pre
   - PD
   - PD Audit
   - PD Multi-Object
   - Blackbox opening when required
   - Basic Math
   - Verify Math
   - MT_post
10. HF1_local
11. GOAL^36
12. ARCHITECT^36
13. IC-028 inquiry loop
14. ICC-123 residual-distinction pass
15. ICC-128 admission/reentry/closure control
16. PLAN / SOLUTION
17. EXECUTE with receipts
18. VERIFY^36
19. ASSERT_post^36
20. GOAL-GAP
21. Route residual by type
22. TRC^36
23. Update
24. Jane Sync
25. HF1_terminal^36
26. Final Observe^36
27. Final response
```

### 16. Residual routing rule

Provisional routing:

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

### 17. Current compact candidate

```
Bind
→ Observe
→ Freeze
→ ASSERT
→ Problem
→ Root
→ 36Q
→ {Differentiate, Relate, Reconstruct, Strengthen}
→ MTPD
→ HF1
→ Goal
→ Architect
→ IC028
→ ICC123
→ ICC128
→ Plan
→ Execute
→ Verify
→ ASSERT
→ Gap
→ TRC
→ Update
→ Sync
→ HF1
→ Observe
→ Response
```

## Open issues intentionally preserved

1. Exact current mathematics of several named tools remains unrecovered.
2. "Best"/"ideal" in Architect requires a formal comparison relation.
3. Exact placement/necessity of ICC-123 and ICC-128 may change once the dependency graph is formalized.
4. The full 36-question set and its exact mapping to the four cognitive operations need authoritative recovery.
5. HF1 exact mathematics remains open even though its architectural job is clearer.
6. MTPD naming and exact internal contract remain provisional.
7. The global tool-system reorganization by question dependency is deferred work and must not be lost.
8. This conversation capture is provenance, not automatic canonical promotion.

## Preservation rule

Do not delete or overwrite this file when the architecture changes. Superseding architecture records may point back here as provenance.
