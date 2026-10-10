# CURRENT ROOT CAUSE — Recovery Anchor 087

Date: 2026-09-26
Status: CURRENT / VALIDATED / MERGED
Canonical repository: thytabakman-jpg/Take-5

## Identity

User names:
- Root Cause
- RootCause
- Rout Cause (orthographic variant only)

Configured tool id:
RootCause

Current mathematics:
architecture/ROOT_CAUSE_MATHEMATICS_087.md

Current runtime:
runtime/root_cause.py

ImprovementCore attachment:
runtime/root_cause_managed.py

Local recurrence:
runtime/hf002_recursive_continuation.py

## Native job

Given a protected recurring failure class F under frozen basis K, identify the
smallest stable upstream generator that:

- explains the recurrence class;
- survives representation changes;
- would break the recurrence if removed/repaired;
- is not dominated by an admitted rival.

Do not stop at the first cause, nearest mechanism, earliest event, or easiest repair.

## Current composition

ImprovementCore parent
-> selects RootCause child
-> RootCause local round
-> TRC
-> HF1 upstream classification
-> HF2 decides same-capability recurrence
-> RootCause attacks its changed causal representation again
-> local relative close / OPEN / BLOCKED / CONFLICT / RETURN_REENTER
-> typed ChildReturn
-> ImprovementCore admission
-> global replan / repair / closure.

RootCause local closure is never global ImprovementCore completion.

## Rootness selector

For candidate c and recurrence F:

RootAdmissible_F(c)

iff

F subseteq Explain(c)
and StableAcrossRepresentation(c)
and BreaksRecurrenceOnRemoval(c)
and CounterEvidence(c)=empty
and Open(c)=empty.

Candidates are compared by Pareto dominance, not a scalar score.

## HF2 protected behavior

The first admissible root candidate receives a same-capability smaller-generator
challenge before local closure.

This is why RootCause is HF2-wrapped rather than one-pass.

## Whole-chat MT basis

research/MT_ROOT_CAUSE_WHOLE_CHAT_088_2026-09-26.md

That reconstruction found the protected semantic meaning of "root":

smallest stable upstream generator of a recurring failure class.

Spelling variation is nonmaterial.

## Current whole-chat test

tests/test_root_cause_hf2.py

The chat-derived recurrence class includes:
- color invariant claimed repaired while emitted response violates it;
- tool exists but ordinary invocation bypasses it;
- full-run invocation downgrades to bare/partial behavior;
- migration preserves artifacts but loses activation;
- recovery state goes stale;
- host reasoning substitutes for controller ownership.

The expected root candidate is:

PROTECTED_TRANSITION_INTEGRITY_FAILURE.

This is a testable current hypothesis, not an eternal ontology.

## Recovery load order

1. integration/CURRENT_ROOT_CAUSE.md
2. architecture/ROOT_CAUSE_MATHEMATICS_087.md
3. research/MT_ROOT_CAUSE_WHOLE_CHAT_088_2026-09-26.md
4. runtime/root_cause.py
5. runtime/root_cause_managed.py
6. runtime/hf002_recursive_continuation.py
7. integration/CURRENT_HF2.md
8. runtime/tool_manifest.py
9. runtime/tool_run_registry.py
10. tests/test_root_cause_hf2.py

## Optional historical RootCause consultation (read-only)

After the **current** failure class has been frozen independently, `runtime/root_cause_managed.py` accepts optional `research_root=<local Reaserch checkout>`. It reads ten [Root Cause question-first knowledge subjects](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/research/consolidations/ROOT_CAUSE_ROLLING_DISCOVERY_KNOWLEDGE.md) through `runtime/root_cause_knowledge_lookup.py`; the return adds `historical_knowledge` with plural candidates, exact subject/content fingerprints and original-source references. Default callers without `research_root` retain the previous result contract. Missing/inaccessible sources and no matches are typed, not invented. Historical evidence does **not** enter the RootCause score vector, certify cause, override the frozen basis or grant ImprovementCore repair authority. Library G11/G12 originals are not copied or marked independently verified.

**Executable lookup for authorized non-RootCause consumers:** `python runtime/root_cause_knowledge_lookup.py --research-root /path/to/Reaserch "premature parent campaign closure"` returns JSON candidates with source references; missing checkout returns `NO_ACCESS` and exit code 2. The adapter exports `record_verified_root_cause_outcome(...)` for **explicit owner-admitted post-repair capture** into the existing ImprovementCore material or negative-learning owner, never during lookup. The verification receipt, basis, route and episode are required; unresolved outcomes cannot write. Neither CLI nor the explicit learning function is automatically invoked by every project or host.

**Validated bounded checks (2026-10-10):** GitHub-byte-identical copies of the [adapter](../runtime/root_cause_knowledge_lookup.py), the [RootCause child attachment](../runtime/root_cause_managed.py) and [seven regression tests](../tests/test_root_cause_knowledge_lookup.py) were executed in an isolated Python environment: `python -m pytest -q tests/test_root_cause_knowledge_lookup.py` → **7 passed**. The imported controller and ImprovementCore dependencies were **controlled stubs**; this is not a full native HF2 or repository-wide test. Additional read-only queries over the actual Reaserch ten-subject GitHub sources discriminated parent-closure, runner/validator, and no-match cases; these latter checks used an equivalent repository-connected script rather than the native Python CLI. Consumer access still requires a deliberately supplied readable Reaserch checkout; universal host binding, production outcome-triggered capture and full configured runtime regression remain OPEN.

## Anti-loss rule

A successor may not reduce RootCause to:
- one-pass diagnosis;
- nearest causal mechanism;
- scalar candidate scoring;
- fixed-depth recursion;
- global completion authority;
- blind repetition without material delta.

Any successor must preserve:
- recurrence-class target;
- rival discrimination;
- representation-stability challenge;
- counterfactual removal challenge;
- smaller-generator challenge;
- HF2 local recurrence;
- HF1 upstream escape;
- ImprovementCore parent authority;
- typed OPEN/BLOCKED/CONFLICT;
- local/global closure separation.

## OPEN

- global minimality of the rootness coordinates;
- automatic rival generation from arbitrary raw corpora;
- causal-cycle formalism;
- external counterfactual intervention execution;
- universal host binding.


## First validated run

PR #65
- merge 691462f614dc026ad199f1b343496d06bca4da1e
- validation run 36222526907
- full Take-5 test suite passed
- canonical whole-system audit passed
- closed-loop fixture passed
- zero-request dump passed

Chat-derived RootCause execution:
- recurrence packet contained six recurring failure classes from the current conversation;
- local HF2 rounds: 2;
- selected root candidate: PROTECTED_TRANSITION_INTEGRITY_FAILURE;
- parent handoff: ImprovementCore / ADMIT_ROOT_CAUSE_AND_REPLAN.

Run record:
research/ROOT_CAUSE_RUN_CURRENT_CHAT_089_2026-09-26.md


## Post-repair recheck

The repair predicted by first run 089 was implemented as Protected Transition Integrity 090.

Validation:
- PR #69
- merge 73639b7292e0e0d2b876b1751109255038e7f69b
- validation 36222874741

Executable recheck:
runtime/protected_transition_root_recheck.py

Result relative to the repaired Take-5 state:

- internal PROTECTED_TRANSITION_INTEGRITY_FAILURE is no longer root-admissible for the remaining residual;
- remaining root candidate: HOST_INTEGRATION_BYPASS;
- meaning: an external host can still bypass Take-5 entirely.

This is a narrower residual than the original whole-chat root.
