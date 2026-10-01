# Affirmative-First Defense-in-Depth Mathematics 001

Date: 2026-10-01
Status: FROZEN BEFORE DEFENSE-IN-DEPTH IMPLEMENTATION
Origin: RootCause on repeated negative-first conversational prose
Controller: ImprovementCore
Protected behavior: AFFIRMATIVE_FIRST

## Root generator

The observed failure is not absence of the preference. The preference and Prose rule already exist.

The stable generator is:

[
G_{AF}=OPTIONAL_ENFORCEMENT_PATHS + HOST_BOUNDARY_BYPASS.
]

A protected style invariant fails whenever any prose-producing path can reach user-visible emission without an affirmative-first check.

## Required invariant

Let (p) be reader-facing prose and (AF(p)) mean that the affirmative proposition is presented before rhetorical rejected alternatives, except where negation is itself load-bearing semantic content.

[
AF(p)=PASS
iff
R_{neg-first}(p)setminus L_{neg}(p)=arnothing.
]

No repository-controlled user-visible prose is admissible unless (AF(p)=PASS).

## Defense layers

Define the enforcement vector

[
D_{AF}=
langle
capture,
contract,
detector,
architecture,
solution,
orchestration,
return,
emission,
regression,
host
angle.
]

Repository-relative closure requires every repository-controlled coordinate to have a witness. Host is separately typed because repository code cannot compel an unrelated external host.

### capture

The preference is explicit: state the positive proposition first. Exclusions and rejected alternatives follow only when materially necessary.

### contract

AFFIRMATIVE_FIRST remains a default Prose constraint.

### detector

The detector covers named negative-first idioms and paragraph-opening rejected-frame constructions. Load-bearing negation remains explicitly allowlistable.

### architecture

Prose-changing architecture carries AFFIRMATIVE_FIRST as a protected constraint and fails open when preservation is unwitnessed.

### solution

Prose-changing candidate solutions preserve AFFIRMATIVE_FIRST and require preservation evidence before SOLVED.

### orchestration

Configured prose work carries the Prose contract through execution rather than relying on informal caller memory.

### return

A controller that claims completion for prose-changing work requires a PASS prose receipt.

### emission

The final repository-controlled assistant-response boundary runs an independent affirmative-first audit. This is a stopgap against upstream omission.

[
Emit(p)Rightarrow AF(p)=PASS.
]

### regression

Exact historical escapes remain permanent fixtures. The Tanach negative-first sentence is one such fixture.

### host

An external ChatGPT host can still bypass repository runtime. Repository code records that boundary as EXTERNAL rather than falsely claiming universal interception.

## Admission logic

For any repository-controlled path (x):

[
Admit(x,p)
iff
AF_{contract}(p)
land
AF_{runtime}(p)
land
AF_{emission}(p).
]

The layers are intentionally redundant. Failure of one layer must not imply failure of the invariant.

## Fail-closed states

- detected negative-first prose -> REPAIR_REQUIRED
- missing required prose receipt on governed prose work -> OPEN
- final response boundary violation -> BLOCKED
- external host bypass -> EXTERNAL_HOST_OPEN

## Mutation rule

This document is the math-first basis for the defense-in-depth repair. Implementation changes are admitted only against this object.
