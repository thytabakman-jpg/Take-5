# Desired Jane Tool 061

Date: 2026-09-25
Status: IMPLEMENTED ON BRANCH / VALIDATION REQUIRED
Tool id: DesiredJane
Primary question: What does Tzvi want Jane to be?

## Rewritten controlling prompt

Recover from all available evidence what Tzvi wants Jane to be. Do not infer Jane's desired role from her current implementation alone. Separate required behavior, prohibited behavior, unresolved coordinates, and genuine conflicts. Preserve the current Jane/ICC role separation unless the evidence defeats it. Run the full compound ASSERT process on the recovered desired-Jane contract and separately on the tool that recovered it. Reject any requirement invented from repetition, recency, convenience, or architecture aesthetics. Implement the tool as a configured strong-claim tool with OPEN/conflict preservation, recursive closure, and reentry. Then compare the desired-Jane contract against current Jane and report only the material results.

## Tool object

Input:
- evidence rows
- coordinate
- polarity
- source
- statement

Output:
- REQUIRED coordinates
- PROHIBITED coordinates
- OPEN coordinates
- CONFLICT coordinates
- full source-grounded dispositions

Runtime:
- runtime/desired_jane.py

Configured run:
- DesiredJane in runtime/tool_run_registry.py

## First recovered desired-Jane contract

REQUIRED:
- direct conversation interface
- entry-state reconstruction
- canonical currentness bootstrap
- continuity supervision
- question-frontier supervision
- capability visibility
- delegation packaging
- admitted-delta synchronization
- discovery-to-work bridge
- automatic reentry support
- short faithful external surface
- load-bearing semantic object lifecycle supervision
- automatic semantic-package capture obligations

PROHIBITED:
- Jane as primary problem solver
- Jane as primary action selector
- self-authorization
- silent mathematical redefinition
- silent currentness claims
- silent use of newly discovered load-bearing objects without durable semantic capture

OPEN:
- none in the frozen first evidence basis

CONFLICT:
- none in the frozen first evidence basis

## ASSERT on the desired-Jane contract

### ASSERT

Supported:
- Jane is intended to make the system feel continuous, current, and self-carrying across turns and tools.
- Jane is intended to recover enough of the user's entry state that the user does not repeatedly reconstruct target, job, constraints, current state, and finish condition.
- Jane is intended to turn continuity-relevant discoveries into visible work/reentry rather than leaving the user as external scheduler.
- Jane is not intended to replace ICC/Improvement Core as the adaptive solver/controller.
- Jane must not gain authority from evidence, continuity, relevance, or persistence alone.

### COMPARE

Current Jane already realizes:
- entry binding
- capability visibility
- delegation packaging
- question-frontier candidate creation
- supervisory relevance
- admitted-delta synchronization
- user-facing projection

Current Jane does not yet establish:
- entry-state reconstruction from evidence/history
- guaranteed canonical bootstrap at every host entry
- end-to-end question/frontier candidate disposition
- end-to-end discovery-to-work-to-reentry closure without user prompting

### RESOLVE

Resolved:
- desired autonomy does not imply Jane owns tool/action selection.
- desired direct conversation does not imply Jane becomes the solver.
- continuity is a supervisory function; adaptive solution search remains ICC/IC.

### HERE

Current mismatch is concentrated in mediation, not role identity:
Jane's intended role is mostly correct, but several required bridges remain incomplete.

### INQUIRE

The next result-sensitive questions are:
1. How does Jane reconstruct entry state rather than receiving it fully from the caller?
2. How is canonical currentness bootstrap made non-bypassable at host entry?
3. How do Jane-generated frontier candidates acquire guaranteed disposition/consumer/reentry?
4. How is discovery-to-work closure proven prospectively?

### REASSERT

No evidence requires rebuilding Jane as a peer controller.
The next Jane work belongs at narrow interfaces and bridges.

## ASSERT on the tool

PASS:
- evidence and desire are distinct;
- WANT and DO_NOT_WANT remain distinct;
- OPEN remains OPEN;
- contradictory evidence becomes CONFLICT;
- repetition does not create a new coordinate;
- the tool does not self-authorize implementation;
- the tool is a strong-claim configured run;
- current instance is source-grounded and inspectable.

FAIL-CLOSED:
- invalid polarity is rejected.
- conflict prevents assertion-safe closure.

LIMIT:
The frozen Tzvi evidence basis is a current recovered instance, not a claim that no future user correction can revise it. New material preference evidence triggers reentry.

## Comparison with current Jane

MATCH:
- facade/interface role
- continuity supervision
- capability visibility
- delegation packaging
- question-frontier observation
- admitted-delta sync
- non-solver role
- non-action-selector role

PARTIAL:
- currentness bootstrap
- discovery-to-work bridge
- automatic reentry support
- short faithful external surface

MISSING:
- entry-state reconstruction from evidence/history

## Disposition

The tool is coherent and implementation-safe.
Jane's role does not need replacement.
The major next Jane improvement is entry-state reconstruction plus guaranteed propagation of continuity/frontier discoveries into work and reentry.


## Semantic lifecycle clarification

Jane owns the lifecycle invariant, not the mathematics itself.

When a load-bearing object appears, Jane must ensure that it enters durable semantic state immediately.

For externally discovered concepts, a package with BLACK_BOX_OPEN coordinates is legal.

For deliberately created tools/programs, Jane must prevent admission-ready status until the creator/foundry supplies the mathematics required for the advertised job and a current semantic package exists.

This preserves Jane's supervisor/facade role while making semantic capture non-optional.
