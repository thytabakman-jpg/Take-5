# PD Audit — KERNEL 001

Date: 2026-09-24
Status: CANDIDATE DEFINITION / OPEN UNDER EXTERNAL COMPARISON
Target: foundation-before-migration

## Problem

Historical artifacts use kernel for:
1. K, the semantic context/contract role;
2. an inner execution kernel such as <O,G,M,C>;
3. the repository/runtime authority substrate;
4. the protected invariant layer of a successor architecture;
5. occasionally the whole foundation.

These usages are not extensionally identical.

## PD result

For the current architecture task, define KERNEL functionally as the smallest always-on privileged contract/mechanism set whose correct operation is required to preserve system identity, legality, protected behavior, and admissible transitions across every execution episode in its declared scope.

Candidate:
Kernel_B,K(N) iff
AlwaysOn(N) AND Privileged(N) AND
PreservesIdentityLegality_B,K(N) AND
MinimalUnderPrivilege(N).

Privilege means other components are constrained by or depend on N in a way ordinary replaceable capabilities are not. It does not mean production authority.

Therefore:
KERNEL != SYSTEM CORE.
KERNEL != all foundational machinery.
KERNEL != controller.
KERNEL != semantic worker.
KERNEL != runtime merely because runtime executes.
KERNEL != K solely by historical notation.

## Candidate kernel responsibilities from current evidence

Strong candidates:
- target/object identity contract;
- type/admission semantics required globally;
- authority/grant legality;
- protected-behavior/invariant contract;
- completion/terminal semantics;
- transition legality;
- OPEN/incomparability preservation where globally protected;
- exact provenance/currentness requirements needed for legal continuation.

Possible non-kernel factors unless ablation says otherwise:
- adaptive problem selection;
- PD candidate generation;
- quotient algorithm;
- domain operators;
- most generators/modifiers;
- runtime workers;
- persistent evidence values;
- benchmark machinery;
- promotion decision.

## Distinction from K

Existing K=<Identity,Semantics,EvidenceContract,GovernanceContract,PreservationContract,CompletionContract,ResourceContract,ExternalInterfaceContract> is a strong candidate semantic-contract object.

PD does NOT yet license Kernel = K.

Some K coordinates may be episode configuration rather than privileged invariant machinery. Conversely executable transition/authority mechanisms may be kernel responsibilities even when not naturally represented as static K values.

## Distinction from core

Core asks what is irreducible to reconstruct protected system behavior.
Kernel asks what irreducible subset must be privileged/always-on to govern every episode.

Thus Kernel is expected to be a proper subset or privileged projection of System Core, not a synonym.

## OPEN

Exact privilege boundary; whether state-transition legality belongs wholly in kernel or as kernel contract plus replaceable U; whether resource/external-interface contracts are kernel coordinates; whether observation/action boundary enters kernel in closed agent-environment scope.
