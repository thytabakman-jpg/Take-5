# What Is the Solution to My Problem Contract 060

Date: 2026-09-25
Status: CURRENT CANDIDATE CONFIGURED PROGRAM
Program ID: SolutionToMyProblem
Supersedes: SOLUTION_TO_MY_PROBLEM_CONTRACT_059.md

## Anti-cheat correction

Contract 059 allowed candidate-local fields such as Executable, Verified, Resolves, and Preserves to participate directly in SOLVED. That permitted a proposal to carry the facts needed to certify itself.

This contract forbids candidate self-certification.

Candidate proposal:

s = <Id, ProposedAttacks, ProposedEffects, ProposedPreservations, Cost>

External receipt:

r = <CandidateId, Source, ExecutionStage, ObservedAttacks, ObservedEffects,
     ObservedPreservations, ObservedViolations, VerificationStatus,
     ClosureStatus, Evidence>

Proposal claims and observed evidence are different object types.

## Governing question

What externally evidenced intervention solves the diagnosed generator while producing every required effect, preserving protected behavior, and reaching verified closure?

## Solution law

Solved(s,P,r) iff:

CandidateId(r)=Id(s)
AND Source(r) is explicit
AND ExecutionStage(r)=CONSUMED
AND Generator(P) subseteq ObservedAttacks(r)
AND RequiredEffects(P) subseteq ObservedEffects(r)
AND Protected(P) subseteq ObservedPreservations(r)
AND ObservedViolations(r)=empty
AND VerificationStatus(r)=PASS
AND ClosureStatus(r)=CLOSED
AND Evidence(r) is nonempty.

Candidate-local declarations cannot satisfy any receipt coordinate.

## Proposal relevance

A proposal may enter the candidate frontier when its proposed attack/effect/preservation coverage matches the diagnosed job. This is only a reason to test it. It is not evidence that it works.

## Terminal states

SOLVED
  At least one nondominated candidate has a valid external receipt satisfying the solution law.

VERIFY_REQUIRED
  A relevant candidate exists but no valid external receipt establishes execution + observed effect + preservation + verification + closure.

OPEN
  The problem generator is absent or no proposal addresses the diagnosed job.

BLOCKED
  Reserved for an explicit execution/authority/resource blocker supplied by the wrapper.

## Required evidence separation

Generated != admitted.
Proposed effect != observed effect.
Proposed preservation != verified preservation.
Executable design != executed intervention.
Executed != consumed.
Verification claim != verification receipt.
Local pass != closure.

## Current problem disposition

The binding-currentness invariant remains a candidate solution:

SemanticDelta(x)
=> RevalidateBinding(x)
=> ExplicitBindingState(x)
=> InvocationVerification(x).

It remains VERIFY_REQUIRED until the actual system implementation produces external execution, effect, preservation, verification, and closure receipts.
