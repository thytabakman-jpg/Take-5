# IC-028 Advanced Root Cause + Architect Campaign 047

Date: 2026-09-24
Controller lease: IC-028
Status: EXECUTED SEMANTIC ARCHITECTURE DECISION
Sequence: MT -> MTA -> PD/PDAudit -> Architect -> Multi-Object/MO-MT -> Architect -> Root Cause -> Architect -> RTC/MTOS -> Architect -> Consequence Closure

## Rewritten prompt

Take ownership of the current system-design episode. Recover the strongest configured versions of the meta-tools rather than their names. Analyze the new IC-028/Jane/Foundation relationship, especially JaneAlert -> WorkCandidate -> IC-028 and IC-028 admitted delta/receipt -> Jane update. Determine the correct wrapper, role assignment law, backlog ownership, tool-ensemble design, and lab strategy. Design a stable "throw everything at it" configured program from a deliberately chosen high-value tool basis rather than blind invocation. Determine whether 20 tool families is justified and how the 36-cell scope/mode surface applies. Preserve the current kernel while testing successor foundations in labs. Execute only changes supported by the analysis.

## 1 MT / MTA

Key objects:
Kernel, Foundation, JaneSupervisor, IC028Operator, Alert, WorkCandidate, AdmittedDelta, Receipt, Backlog, RoleAssignment, Wrapper, ToolFamily, ToolEnsemble, ScopeMode36, Lab, SuccessorFoundation, TestTwoBehavior.

MTA result:
- Alert is evidence-bearing observation, not Work.
- WorkCandidate is a typed proposed obligation, not admitted Work.
- AdmittedDelta is state-changing evidence/result with admission status.
- Receipt is execution/evidence trace, not the delta itself.
- Backlog is a VIEW over typed Work, not an owner.
- Wrapper is configured-run semantics, not a tool.
- RoleAssignment is a routing/governance function and is independently result-sensitive.
- ToolEnsemble is a configured program over tool families; it is not a new semantic capability merely because it contains many tools.
- ScopeMode36 is a coverage/challenge surface for each family/program, not 36 versions of the tool.
- "Test Two behavior" is a protected behavioral program to reconstruct, not a repository to resurrect.

## 2 PD / PD Audit

Hidden selector found:
"whose job is it?" was previously answered by names/components.
Correct selector is obligation ownership.

For obligation w, assign role by:
Role(w)=nondominated eligible owner(s) under
<semantic responsibility, authority, required state access, execution capability, continuity horizon, evidence burden, conflict cost>.

Preserve SHARED_INTERFACE/OPEN_OWNER when no unique owner is justified.

PD Audit counterexample:
A Jane alert about stale currentness can originate in Jane, require Foundation evidence, and become Operator work. Origin != owner != executor.

Therefore role assignment requires at least:
Origin(w), SemanticOwner(w), AuthorityOwner(w), Executor(w), Verifier(w), StateConsumer(w).

## 3 Architect pass A

Architecture object:
A=<V,E,B,I,C,Gamma,Sigma,tau>.

V:
User, Kernel, FoundationServices, JaneSupervisor, IC028Operator, Workers/Tools, ExternalExecutionEnvironment, Labs.

Critical E:
User<->JaneInterface
JaneSupervisor->CandidateObligation
Foundation->JaneSupervisor material-state update
JaneSupervisor->IC028 evidence/context
IC028->Foundation proposed/admitted transitions
IC028->Workers selection/binding
Workers->IC028 returned results
IC028->Jane admitted-delta/receipt projection
Labs->IC028 challenger evidence
Kernel constrains all authoritative transitions.

No component owns "Backlog." Typed Work state does. IC-028 owns work policy. Jane watches continuity/staleness and can generate candidate obligations.

## 4 Multi-Object / MO-MT

Alert x WorkCandidate x Operator:
Alert must pass objectification/admission before becoming active Work. Prevents Jane from silently becoming a second controller.

Delta x Receipt x Jane:
Jane needs both WHAT changed (delta) and WHY/WHETHER it really happened (receipt). Sending only delta loses execution truth; sending only receipt loses semantic consequence.

Jane x IC028 x Foundation:
three-way residual is a synchronization protocol:
Foundation material commit -> supervisory update obligation -> Jane projection/watch update -> IC028 next-round context.

Wrapper x Jane:
Jane update belongs in Tool Run Closure after admitted persistent consequence and before next HF/IC reentry when the delta can change continuity/currentness context.

Therefore configured round becomes:

ToolRound
-> ReturnAdmission
-> PersistentConsequence
-> TRC
-> JaneSync
-> HF/IC028 Reentry
-> NextRound.

JaneSync is conditional on material supervisory-relevant delta, not every atomic no-op.

## 5 Advanced Root Cause

Target symptom family:
user repeatedly remembers missing tools/behaviors; system accumulates components but does not reliably compose/propagate them; architecture repeatedly changes names/roles.

Immediate causes:
A. no canonical high-level ensemble invocation;
B. role ownership was name-based rather than obligation-based;
C. Jane/Operator synchronization was not in wrapper;
D. tool families preserved semantics but not always configured-run identity;
E. old Test-Two behavior was remembered as a feeling/repository property rather than reconstructed as a first-class configured program.

Deeper cause:
CONFIGURATION AND OWNERSHIP ARE SECOND-CLASS RELATIVE TO SEMANTIC INVENTORY.

Root generator:
the system optimized "what capabilities exist?" faster than "who owns each obligation and what configured program composes those capabilities end-to-end?"

## 6 Architect pass B

Repair architecture with two new first-class control objects, not new kernel primitives:

RoleAssignmentRecord =
<Obligation,Origin,SemanticOwner,AuthorityOwner,Executor,Verifier,StateConsumers,Status,Evidence>.

ConfiguredEnsemble =
<FamilySet,SelectionPolicy,OrderPolicy,ScopeModeCoverage,Wrapper,StopRule,Receipts>.

These belong above Kernel, in control/runtime architecture.

## 7 The "throw everything at it" ensemble

Do NOT make a new IC whose semantics are "blindly run 20 tools."
Create an IC-028 configured ensemble named FULL-SPECTRUM-20 whose policy is:
all 20 families receive a disposition; relevant families execute in optimized adaptive order; non-applicable/subsumed families receive explicit disposition.

Candidate 20 families:

1 Goal/Target Freeze
2 DOS/Goal-Decoupled Observation
3 MTA
4 MT/Mode Sweep
5 PD
6 PD Audit
7 Multi-Object/MO-MT
8 Architecture Analysis
9 Diagnosis/Root Cause
10 ARA/Artifact Reality
11 Orphan/Ghost/Conflict
12 Currentness/Supersession
13 Role Assignment/Owner Closure
14 Consequence Closure/Affected Cone
15 RTC/Raise the Ceiling
16 MTOS (MTA<->RTC)
17 TransferCore
18 Execution Truth/Activation
19 A16/Holdout/Ablation Verification
20 Goal Completion/CompletionCert

HF-001/TRC recursive wrapper is NOT counted as one of 20 because it wraps every material family.
Capability router is infrastructure, not one of 20.
JaneSync is wrapper/control infrastructure, not one of 20.

Status of 20:
CANDIDATE BASIS, not proven minimal or complete.
It must be tested against C01-C49 and historical protected behaviors for reconstruction/residuals.

## 8 20 x 36 correction

Each family can be challenged/covered on C36=Scope6 x ModeFace6.

Potential coverage surface = 20 x 36 = 720 cells.

This does NOT mean execute 720 runs every time.

Coverage policy:
high-information cells first;
expand only on residual, uncertainty, noncommutation, failed sufficiency, or strong completion claim.

Therefore:
FullSpectrum(x) != brute_force_720(x).

## 9 Order optimization

No single total order is globally valid because tools can be noncommuting and result-sensitive.

Default partial order:

Freeze
-> Observe
-> MTA/PD early discrimination
-> Architect placement
-> Multi-Object interaction
-> Root Cause
-> Architect repair
-> ARA/Orphan/Currentness
-> RoleAssignment
-> ConsequenceClosure
-> RTC/MTOS
-> Transfer/Holdout/Ablation
-> CompletionCert

Reentry:
any material delta -> TRC -> JaneSync -> IC028/HF replan.

Architect appears multiple times intentionally:
before interaction to expose roles,
after interaction/root-cause to place residuals,
after RTC to verify successor structure.

## 10 Test Two reconstruction

Do not alter current kernel mid-episode.

Create a first-class configured program:
BROAD-REFINERY / TEST-TWO-RECONSTRUCTION.

Protected behavior:
messy corpus
-> independent broad observation
-> semantic connection map
-> recursive tool selection/application
-> artifact/state repair
-> human organization
-> reobserve/reenter.

Build it in the experimental labs and as a nonauthoritative Take-5 tool.
Compare behavior against historical fixtures.
Only migrate kernel/foundation changes after strict-gain + preservation evidence.

## 11 Three labs

Take-2: historical/independent kernel-lineage behavior witness.
Take-3: clean-room control; reconstruct FULL-SPECTRUM/role assignment without inheriting Take-5.
Take-4 successor branch: aggressive informed successor using current evidence.

New matched experiment:
same messy corpus + same protected goal + same authority.
Measure:
connection discovery, relevant-tool activation, continuation without prompting, semantic organization, execution receipts, propagation, latency/cost, protected-result quality.

## 12 RTC / Raise the Ceiling

Successor candidates:
S1 current role split only.
S2 + RoleAssignmentRecord.
S3 + JaneSync wrapper.
S4 + FULL-SPECTRUM-20.
S5 + Test-Two configured program/lab validation.
S6 = S2+S3+S4+S5.

S6 dominates on current semantic criteria if realizable, but runtime dominance remains OPEN pending fixtures.

## 13 Architect pass C

Do not change Kernel now.
Kernel changes require lab evidence because kernel is legality substrate.

Change above-kernel architecture now:
- admit RoleAssignmentRecord;
- add JaneSync to recursive configured wrapper;
- add candidate FULL-SPECTRUM-20 ensemble;
- formalize Test-Two behavior as configured program candidate;
- route backlog through typed Work/IC028 policy with Jane continuity alerts.

## 14 IC-028 decision

1 IC-028 remains primary episode operator.
2 Jane remains supervisory/interface sidecar.
3 JaneSync enters wrapper after admitted/persisted material consequences and before reentry.
4 Role assignment becomes explicit and obligation-based.
5 Backlog belongs to Work state; IC-028 policies it; Jane detects continuity/staleness and proposes work.
6 FULL-SPECTRUM-20 becomes the canonical candidate meaning of "throw everything at it," subject to reconstruction validation.
7 36 is coverage geometry, not multiplication mandate.
8 Architect is deliberately interleaved multiple times.
9 Reconstruct Test-Two as an active configured program.
10 Do not mutate Kernel until matched lab evidence supports a strict-gain successor.
