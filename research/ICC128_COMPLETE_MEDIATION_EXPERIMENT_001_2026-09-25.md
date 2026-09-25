# ICC-128 Complete-Mediation Experiment 001

Date: 2026-09-25
Status: RESEARCH RESULT / NO RUNTIME EFFECT
Canonical repository: thytabakman-jpg/Take-5
Controller: ICC-128
Parent research: research/ICC123_KERNEL_ENFORCEMENT_TOPOLOGY_001_2026-09-25.md
Major-change freeze: ACTIVE

## Frozen question

Does current Take-5 have one non-bypassable executable effect boundary that mediates every authoritative or persistent state-changing path?

This experiment addresses E1-E5 from the parent enforcement-topology research.

It does not reduce the kernel law set and does not authorize a runtime redesign.

## Corpus

The observation pass enumerated all 70 Python modules currently under runtime/.

A broad mutation-signature scan was followed by targeted full reads of the modules that own system state, controller state, wrapper update, lineage state, research state, supervisory state, and foundation architecture.

Static mutation signatures are candidate evidence only. The final dispositions below use module contracts, tests, and canonical architecture artifacts.

## Candidate state/effect paths

### P1 A5 behavioral skeleton

Path:

Proposal/Witness
-> ContractK.effect_allowed
-> AdmissionC.evaluate
-> UpdaterU.apply
-> A5.State

Evidence:
- runtime/a5_core.py
- tests/test_a5_core.py

Properties:
- effect-scoped authority is checked;
- denied/deferred effects do not update state;
- UpdaterU refuses non-ALLOW admission;
- state transition creates version/history evidence.

Disposition:
LOCAL_COMPLETE_MEDIATION_WITNESS.

Limitation:
a5_core.py explicitly describes itself as a nonproduction behavioral architecture skeleton. It does not establish mediation of the rest of Take-5.

### P2 Improvement Core working-state path

Path:

selected capability
-> run_episode / ActivationBridge
-> delegated worker output
-> ImprovementCore current.update(out)
-> ICResult.final_packet

Evidence:
- runtime/improvement_core.py
- runtime/controller_episode.py
- runtime/activation_bridge.py
- tests/test_improvement_core.py
- tests/test_improvement_core_math_first.py

Properties:
- selected/bound/dispatched/executed/captured/consumed execution is represented;
- delegation authority is bounded;
- worker dictionaries are merged directly into IC working state;
- generic Tool Run Closure is not inside improve().

Disposition:
WORKING_STATE_MUTATION / RESULT_SENSITIVE.

Open:
whether every IC working-state coordinate is nonauthoritative until a later admission boundary, and whether callers consistently enforce that boundary.

### P3 Endogenous system-loop path

Path:

WorkItem
-> ImprovementCore
-> ICResult.final_packet
-> current.update(ic.final_packet)
-> discharged.add(work_id)
-> SystemResult.state

Evidence:
- runtime/system_loop.py
- tests/test_system_loop.py
- runtime/reflexive_currentness.py

Properties:
- system_loop.py declares that the system owns work existence/closure;
- current_basis() describes Improvement Core as policy controller inside the work lifecycle;
- work can be discharged after IC returns a non-OPEN result;
- system_loop.py does not invoke the math-first wrapper or generic Tool Run Closure before current.update().

Disposition:
CURRENT_SYSTEM_STATE_PATH / COMPLETE_MEDIATION_NOT_ESTABLISHED.

This is the strongest observed bypass candidate relative to the abstract wrapper equation.

### P4 Math-first wrapper path

Path:

entry binding
-> Observe
-> Formalize
-> Freeze
-> Goal
-> Architect
-> IC
-> closure_fn
-> update_fn
-> JaneSync
-> reentry/closure

Evidence:
- runtime/math_first_wrapper.py
- tests/test_math_first_wrapper.py
- architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md

Properties:
- bound entry is mandatory;
- target/job/authority drift is guarded;
- frozen mathematical mutation is blocked;
- closure status is evaluated before update;
- OPEN/BLOCKED are preserved;
- state mutation is delegated to caller-supplied update_fn.

Disposition:
CURRENT_WRAPPER_PATH / CONTRACTUAL_MEDIATION.

Limitation:
the wrapper guarantees ordering around update_fn but does not itself prove that every update_fn enforces one shared transition/admission kernel.

### P5 Inquiry/recursive wrapper path

Path:

round/observer
-> closure_fn
-> update_fn
-> terminal/reentry

Evidence:
- runtime/inquiry_session.py
- runtime/recursive_episode.py
- tests/test_inquiry_session.py
- tests/test_recursive_episode.py

Properties:
- closure precedes ordinary update;
- OPEN/BLOCKED can fail closed or carry explicitly admitted terminal state;
- update semantics are callback-defined.

Disposition:
CURRENT_OR_LEGACY_FACADE_PATH / CONTRACTUAL_MEDIATION.

Open:
exact current authority relative to the math-first wrapper remains a lineage/currentness question.

### P6 IC-028 operator/continuation path

Path:

bound EntryContract / ControllerLease
-> ordered stage handlers
-> handler-returned state
-> optional JaneSync
-> REENTER

Evidence:
- runtime/ic028_operator.py
- runtime/continuation_engine.py
- tests/test_ic028_operator.py

Properties:
- entry/controller binding is guarded in run_ic028;
- stage handlers may replace current state through returned dictionaries;
- the stage plan includes ADMIT, PERSIST, VERIFY, but those are handler names rather than one enforced implementation boundary.

Disposition:
CONFIGURED_CONTROL_PATH / MEDIATION_DEPENDS_ON_HANDLER_BINDINGS.

### P7 Lineage state

Path:

delta + provenance
-> LineageState.apply
-> values.update(delta)
-> version increment
-> event append

Evidence:
- runtime/lineage_state.py

Properties:
- provenance is recorded;
- no authority/admission/transition-verification object is required by apply() itself.

Disposition:
PERSISTENT_LINEAGE_PATH / DIRECT_MUTATION.

This can be legal only if callers prove that LineageState.apply receives admitted deltas exclusively. That caller-coverage proof is not established here.

### P8 Research state

Paths:

record_claim
-> claims[claim_id] = status/evidence
-> history append

discharge
-> discharged.add(work_id)
-> history append

Evidence:
- runtime/research_system.py
- tests/test_system_architecture_currentness.py

Properties:
- closure certification requires evidence for ADMITTED claims;
- record_claim() itself accepts ADMITTED as a status without an authority/admission token.

Disposition:
RESEARCH_STATE_PATH / DIRECT_MUTATION.

The state is load-bearing because history/evidence affects closure certification.

### P9 Jane supervisory state

Path:

admitted material delta by caller convention
-> update_after_admitted_delta
-> material_deltas/canonical_version/receipts mutation

Evidence:
- runtime/jane_supervisor.py
- runtime/jane_sync.py
- runtime/math_first_wrapper.py

Properties:
- wrapper only invokes Jane sync after a material/relevant admitted wrapper delta;
- update_after_admitted_delta() itself has no internal admission proof requirement.

Disposition:
SUPERVISORY_DERIVED_STATE / CALLER-GUARDED.

This is not presently treated as a primary result state, but currentness/continuity behavior can depend on it.

### P10 Fixture/dump file effects

Examples:
- runtime/closed_loop.py
- runtime/closed_loop_v2.py
- runtime/take5_dump.py

These write fixture, receipt, or dump state to files.

Disposition:
VALIDATION_OR_DERIVED_OUTPUT unless separately promoted by another authority path.

These paths do not by themselves establish canonical Take-5 state mutation.

## Effect graph result

Let protected proposal sources be P and load-bearing state sinks be Z.

Observed sinks include:

Z_A5 = A5.State
Z_IC = IC working/final packet
Z_SYS = endogenous SystemResult state/discharge state
Z_WRAP = wrapper state
Z_REC = recursive/inquiry state
Z_LINEAGE = LineageState
Z_RESEARCH = ResearchState
Z_JANE = Jane supervisory continuity state

Candidate mediation nodes include:

B_A5 = AdmissionC + UpdaterU
B_ACT = ActivationBridge / run_episode
B_TRC = closure_fn / Tool Run Closure family
B_ENTRY = EntryContract + ControllerLease
B_UPDATE = abstract U role in architecture mathematics

No single executable node currently observed dominates every path from proposal sources to every load-bearing sink.

In particular:

P_worker
-> run_episode
-> worker output
-> ImprovementCore.current.update
-> ICResult.final_packet
-> system_loop.current.update
-> Z_SYS

does not cross the current math-first wrapper's closure_fn/update_fn boundary.

And:

P_delta
-> LineageState.apply
-> Z_LINEAGE

does not intrinsically cross AdmissionC, ActivationBridge, or Tool Run Closure.

And:

P_claim
-> ResearchState.record_claim
-> Z_RESEARCH

does not intrinsically cross those boundaries either.

Therefore:

CompleteMediation(B_current) is NOT ESTABLISHED for any single current executable B.

A stronger statement that complete mediation is impossible is not licensed. Some paths may later be classified as derived/non-authoritative, or their callers may prove an upstream shared admission contract.

## Root cause candidate

The repository contains several generations of architecture preserved for takeover, rollback, comparison, and regression.

The mathematical architecture converged on a role named U / admitted update.

The executable system did not yet converge on one unique effect API implementing that role across all state species.

Thus:

one abstract update role
!=
one executable update boundary.

This is a current architecture-integration gap, not evidence that every existing path is wrong.

## Relation to the current foundation

architecture/CANONICAL_FOUNDATION_034.md describes the kernel as an always-on legality membrane.

architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md defines:

W_beta = Sync_J o U o C_TR o IC o A o G o Freeze o Phi o O_beta.

The experiment does not falsify those semantic contracts.

It shows that whole-repository executable domination by U/C_TR is not yet proved and has at least one concrete current-path counterexample candidate: runtime/system_loop.py.

## ICC-128 admission disposition

Admit the following claim as current research evidence:

WHOLE_SYSTEM_COMPLETE_MEDIATION = NOT_ESTABLISHED.

Do not admit:

WHOLE_SYSTEM_COMPLETE_MEDIATION = FALSE_IN_PRINCIPLE.

Do not admit a replacement K_exec yet.

Do not collapse all state species into one store.

Do not alter system_loop, lineage_state, research_system, Jane, IC, or the wrappers until state authority/species are typed.

## Required E5 follow-up

For every sink above, assign exactly one state role:

AUTHORITATIVE_RESULT_STATE
AUTHORITATIVE_CONTROL_STATE
PERSISTENT_LINEAGE_STATE
SUPERVISORY_DERIVED_STATE
EPISODE_WORKING_STATE
VALIDATION_DERIVED_STATE
PROJECT_LOCAL_STATE
OPEN_STATE_ROLE

Then establish for every authoritative/persistent role:

1. legal producer set;
2. required authority;
3. required evidence;
4. required admission/verification;
5. required provenance;
6. reentry consequence;
7. whether it must cross a shared K_exec boundary.

Only after this typing can a dominator analysis discriminate:

A. one shared K_exec;
B. multiple typed commit gates with a common kernel contract;
C. current bypass defects;
D. legitimate derived-state mutations outside K_exec.

## Interaction with tool/ICC lineage

Kernel-law externalization/minimality remains blocked on historical witness recovery.

A law cannot be removed from K_law merely because current code can operate without it when earlier protected configurations depended on it.

Therefore B4 tool/ICC lineage backfill and B5 effect-topology work are coupled but distinct.

## Closure of this experiment

E1 runtime mutation surfaces: COMPLETE RELATIVE TO CURRENT runtime/*.py CORPUS AND STATIC/TARGETED INSPECTION.

E2 source/sink preliminary typing: COMPLETE ENOUGH TO DISCRIMINATE CURRENT CLAIM.

E3 directed effect graph: CONSTRUCTED AT MODULE/OPERATOR LEVEL.

E4 current dominator test: WHOLE_SYSTEM_COMPLETE_MEDIATION NOT ESTABLISHED.

E5 path disposition: PARTIAL; state-role authority typing remains OPEN.

E6 K_law externalizability: BLOCKED BY E5 + B4.

E7 OPEN preservation: SATISFIED.

This experiment therefore closes RELATIVE to the question "is complete mediation already established?" with answer NO/NOT ESTABLISHED, while reentering on state-role typing and historical protected-witness recovery.
