# A5 Behavioral Architecture Candidate 004

Date 2026-09-24
Status FORMAL CANDIDATE READY FOR NONPRODUCTION IMPLEMENTATION TESTING
Migration authority NONE

Goal
Build and validate a nonproduction successor foundation that can orient, discover, select, execute, verify, reenter, preserve knowledge and capabilities, and improve its own methods under governed transitions. Recover historical protected behavior. Stop before migration.

Core algebra
T=<K,S,O,G,M,C,R,U>
O={DIFFERENTIATE,RELATE,RECONSTRUCT,STRENGTHEN}

K contracts identity, semantics, evidence, governance, preservation, completion, resources and external interface.
S carries identity/topology, active semantic content, epistemic/evidence status, authority/license, history/temporal trace and search/failure memory.
G produces candidate jobs, rivals and successors but grants no authority.
M changes representation, hierarchy, arity, composition/order and reentry conditions.
C evaluates proposals and effect-scoped admission.
R selects eligible nondominated continuation while preserving plurality.
U performs typed partial/set-valued state transition.

Authoritative transition
Represent each authoritative edge as s -[p,w,a,e]_K-> s2.
Require a=C_K(s,p,w), Allows_K(a,p,e,s,s2), and s2 in U_K(s,p,w,a,e).
Admission of one effect does not license another.
Persistence is not authority. Evidence is not authority.
Self-modification is governed by the same transition rule except genesis.

Tool/program model
A concrete tool is a typed composition over <O,G,M,C,R,U> operating on S under K.
Historical capability h is recovered when such a program contextually reconstructs h under its frozen job and licensed composition contexts.

Role ablation
Remove K: loses global identity, semantics, preservation, completion and authority contracts. Recreating them recreates K. NECESSARY relative recovered behavior.
Remove S: loses durable identity, evidence, authority, lineage, OPEN, failure memory and trajectory. NECESSARY.
Remove O: control can move candidates but lacks substantive differentiation/relation/reconstruction/strengthening. NECESSARY substantive role; exact four-factor minimality remains to test.
Remove G: no candidate/rival/successor/job producer. NECESSARY.
Remove M: cannot reconstruct representation attack, higher-order residuals and order-sensitive composition without duplicating modifier semantics. NECESSARY.
Remove C: candidate production/state update becomes self-licensing or admission logic moves elsewhere. NECESSARY.
Remove R: no explicit eligible next-work selection, reentry, anti-loop or nondominated frontier. NECESSARY.
Remove U: accepted candidate and realized state effect collapse. NECESSARY.
Result: all eight roles are relatively necessary up to role-equivalent reconstruction. This is not a global minimality theorem.

Architecture analysis
Responsibilities:
Foundation semantics K,S.
Epistemic engine O,G,M.
Governance/control C,R,U under K.
Program level typed compositions implementing capabilities.
Validation programs regression, holdout, ablation, independent replication, relative closure and artifact reality.
Runtime durable controller/event history, worker adapters and external action boundary.
These are responsibility partitions, not mandatory software layers.

Diagnosis
Main predecessor defect: named-tool architecture mixed reusable behavior, composition, control and implementation.
Root cause: wrong unit of analysis plus insufficiently explicit authoritative transition boundary.
Repair: behavior-first programs over typed algebra plus effect-scoped admitted transitions.

PD OPEN
Contextual reconstructibility basis.
Exact state quotient.
Exact C product schema.
Distributed enforcement equivalence.
Genesis authority.
External action/environment model.
These can remain typed OPEN while first implementation proceeds.

RTC
Role ablation does not support removing a role without recreating equivalent responsibility.
Raise ceiling through pluggable typed interfaces, new programs without schema mutation, explicit residual/OPEN channels, governed self-modification and replayable witnesses.

Artifact reality
This document is research evidence, not runtime authority. Current Take-5 runtime does not yet implement A5.

Build-ready interfaces
ContractK: identity, semantics, authority, preservation, completion, external action license.
StateStoreS: snapshot, history, currentness, evidence, authority state, search/failure memory.
OperatorO: differentiate, relate, reconstruct, strengthen.
GeneratorG: generate candidates.
ModifierM: representation, arity, order, hierarchy, composition, reentry.
AdmissionC: evaluate proposal/witness/effect to typed disposition.
RouterR: eligibility, frontier, selection/plurality.
UpdaterU: proposed transition, admitted effect, retract/invalidate, noncommutation.
Program declares job, roles, authority, protected outputs, closure and validation.
Witness carries proposal, before-state, evidence, authority, effect scope, admission, after-state, provenance and verification obligations.

Test gates
T1 C01-C49 executable crosswalk.
T2 CAP-001..033 executable crosswalk.
T3 high-value composites.
T4 historical regression.
T5 zero-request corpus-only.
T6 blind unfamiliar holdout.
T7 delegation/authority/bypass.
T8 concurrency/noncommutation.
T9 governed self-modification.
T10 artifact-reality persistent change.
T11 role/operator ablation.
T12 independent replication barrier.
T13 relative closure with OPEN.
T14 external action boundary.

Status
Architecture candidate BUILT.
Ready to start nonproduction implementation and testing.
Not validated. Not migration ready.
