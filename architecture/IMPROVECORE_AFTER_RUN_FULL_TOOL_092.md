# ImproveCoreAfterRun Full Tool 092

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE
Tool: ImproveCoreAfterRun
Purpose: make every governed ImprovementCore use produce durable learning and a typed next self-improvement frontier.

## Native semantics

ImproveCoreAfterRun is a post-episode classifier/generator.

For episode e under basis K:

AfterRun(e,K)
=
<Observation, Candidate, Disposition, Learning, Frontier, Open>.

Observation records:
- terminal/nonterminal status;
- blocker;
- material signals;
- unresolved coordinates;
- protected gain evidence.

Candidate is generated only from an observed residual or reusable lesson.

Disposition is one of:
- NO_STRUCTURAL_GAIN
- CANDIDATE_OPEN
- STRICT_GAIN
- NO_GAIN
- REJECTED
- OPEN
- BLOCKED
- CONFLICT.

## Governing invariant

Every ImproveCore episode executes AfterRun exactly once before the regime returns.

The pass always records learning.

Structural mutation is not mandatory and is never self-authorized.

A structural candidate can be applied only when:
1. a strict-gain evaluator returns STRICT_GAIN;
2. an authorized applier is bound;
3. the applier confirms application.

Clean success with no structural residual returns NO_STRUCTURAL_GAIN while still recording GAIN evidence for the route.

## FullMath

N =
<post-episode observation, residual generation, strict-gain disposition, learning update>.

W =
<POST ImproveCore episode -> AfterRun -> LearningMemory -> optional strict-gain evaluator -> optional authorized applier -> return receipt>.

G =
inherits the finished episode basis and claim scope; it does not launch an independent mandatory 36 sweep merely to invent a change.

P =
<after every run, learning always recorded, no forced change, strict-gain gate, authority gate, OPEN preservation, no infinite self-recursion>.

L =
<identity ImproveCoreAfterRun, registered configured tool, runtime implementation in runtime/improvement_core_afterrun.py, regime binding in runtime/improvement_core_regime.py, regression tests>.

## Why this is stronger than blind self-modification

Always improving means every run improves future search state or validates that the current route remains effective.

It does not mean every run edits code.

Forced mutation converts success into drift and defeats cumulative preservation.

## Recursion boundary

ImproveCoreAfterRun does not recursively schedule itself as a new user episode.

Material candidate evaluation can reenter normal ImprovementCore under a later governed episode or through an explicitly bound authorized applier.

This prevents infinite:
ImproveCore -> AfterRun -> ImproveCore -> AfterRun
without a new material discriminator.

## Protected behaviors

- mandatory invocation after every ImproveCore use;
- learning recorded even on clean success;
- residual blocker becomes a typed self-improvement candidate;
- candidate remains OPEN without evaluator;
- strict gain cannot apply without authority;
- NO_GAIN is legal;
- no structural mutation is inferred from recency or novelty.
