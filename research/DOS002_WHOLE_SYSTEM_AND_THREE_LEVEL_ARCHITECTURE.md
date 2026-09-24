# DOS-002 — Whole System + Three-Level Architecture

Date 2026-09-24
Mode nonproduction observation
Optimization pressure suppressed during sweeps
Migration/promotion prohibited

## MTA preflight

The phrase "level one, level two, level three" has been used in more than one architecture. For this system-building episode, freeze the relevant three-level adaptive architecture as:
L1 Execution Episode
L2 TaskFrame / bounded Step-TransitionContract / observed result / CheckpointPacket
L3 HF-001 + ImprovementCore control that chooses CONTINUE, REPLAN, ESCALATE, BLOCK, COMPLETE and improves/reselects the controller.

Also preserve the newer system hierarchy:
PD/ED semantics -> T=<K,S,O,G,M,C,R,U> -> controller state Z=<FT,X,A,Cl,B,E,L,Q,P> -> capabilities/programs/controllers -> runtime execution -> verification/update -> persistence -> reselection.

The DOS must observe both without forcing them to be identical.

# Sweep A — whole system

Frozen X_A
All current Take-5 semantic architecture, A5 runtime/program registry, campaign/control protocols, historical capability recovery obligations, CI/runtime evidence, DOS, 12-before/after, zero-request requirement, migration boundary.

Boundary
No repair during observations.
No next-step optimization.
No assumption A5 is correct.
No requirement to preserve current family order.
No cross-observation steering.
Observation may return NO_DELTA/OPEN/conflict.

Independent returns

1 Goal Spine
The system has one governing build goal but several success surfaces: semantic adequacy, behavioral recovery, runtime realizability, historical preservation, autonomy, validation, readiness.

2 Architecture Analysis
There are at least three architectural axes currently superimposed: semantic roles T, controller state Z, and execution/control levels L1-L3.

3 MTA
T, Z and L1-L3 are not rival decompositions. They answer different questions: what functions exist, what state is carried, and where/when control operates.

4 PD/PDAudit
The equivalence relation between these decompositions is not formalized. Mapping by shared names would be invalid.

5 Multi-Object
A higher-order residual exists in T x Z x L: a role can be semantically present, state can record it, yet the execution level can fail to invoke it.

6 Diagnosis
This directly explains the user's repeated "IC has behaviors but does not use them" observation: capability possession and activation are separate system properties.

7 Artifact Reality
Program registry and campaign prose prove possession/description; invocation receipts prove activation.

8 Orphan/Ghost/Conflict
Behaviors can become ghosts: registered and discussed, but absent from execution trace. Conversely ad hoc behavior can execute without canonical identity.

9 Representation Attack
A linear pipeline representation hides that control can recurse upward: L1 result changes L2 frame; L2 checkpoint changes L3 controller; L3 can alter future L1/L2 selection.

10 Result Sensitivity
Activation policy is result-sensitive: removing behavior-selection/reconciliation can change discovered work even when all capabilities remain installed.

11 RTC
System improvement requires strict gain in reachable behavior under constraints, not merely a larger registry.

12 HF/Reentry
Reentry exists conceptually but activation/reselection state is not yet a first-class durable object.

13 Authority
L3 control can choose/replan but cannot thereby expand authority or promote migration.

14 Execution Truth
Need episode trace showing selected behavior -> invoked behavior -> return -> consumption -> changed/unchanged frontier.

15 Boundary Analysis
Empirical failures cluster at boundaries, and T/Z/L boundary mappings are themselves currently untested boundaries.

16 Holdout
A true unfamiliar project can test whether L3 activates useful behaviors without handcrafted family progression.

17 Ablation
Remove activation/reconciliation while keeping registry fixed. Predicted loss: discovery quality. This is a direct causal test of the new architecture claim.

18 Zero-Request
Zero-request is the strongest test of activation because no user-supplied task tells L3 which behavior to use.

19 Raise-the-Ceiling
The ceiling is not more behaviors. It is autonomous behavior activation, observation, reconciliation, and evidence consumption.

20 Consequence Closure
DOS itself belongs as a selectable observation program at L3/control level, operating on frozen representations of whole-system or sublevel objects, not as a new primitive semantic role.

## Reconciliation A

WA1 Three axes must be typed separately:
Functional algebra T
State algebra Z
Control/execution levels L

WA2 Missing bridge:
Activation relation A_act connecting available programs to actual episode invocation.

WA3 Missing evidence object:
ActivationReceipt=<episode,object,boundary,behavior,mode,return,consumed,effect>.

WA4 New causal hypothesis:
Registry completeness without activation completeness cannot reconstruct Improvement Core behavior.

WA5 DOS placement:
DOS is a controller-level program/composition using existing observation/representation/admission/reentry machinery. No ninth A5 role forced.

# Sweep B — L1/L2/L3 piece only

Frozen X_B
L1 Execution Episode
L2 TaskFrame + TransitionContract + observed result + CheckpointPacket
L3 HF-001 + ImprovementCore controller/reselection

Boundary
Observe architecture only.
Do not redesign during behavior returns.
Do not optimize toward current implementation.
Do not assume upward flow is sufficient.
Do not collapse levels into semantic roles.

Independent returns

1 Goal Spine
L1 acts, L2 contextualizes bounded action, L3 governs continuation/improvement. The levels have distinct jobs.

2 Architecture
Current formulation emphasizes upward reporting L1->L2->L3 more clearly than downward activation L3->L2->L1.

3 MTA
A complete cycle needs both:
upward evidence flow and downward control/activation flow.

4 PD
Level identity depends on control responsibility, not file/module location.

5 Multi-Object
The interesting behavior exists between levels. No individual level alone explains adaptive execution.

6 Diagnosis
Missing explicit downward activation is a plausible root of "knows tools but doesn't use them."

7 Artifact Reality
A checkpoint saying a behavior is available does not mean L1 executed it.

8 Orphan/Ghost
Uninvoked available behavior is a level-crossing ghost.

9 Representation Attack
The three-level ladder is misleading if drawn only vertically. It is a bidirectional control loop.

10 Result Sensitivity
Deleting L3->L2 activation while retaining L2->L3 evidence changes system behavior substantially.

11 RTC
L3 must select nondominated next action/program, not merely approve next predefined step.

12 HF/Reentry
HF-001 is naturally the upward evidence/reentry mechanism; it needs an explicit paired downward dispatch contract.

13 Authority
Downward dispatch must carry bounded authority envelope.

14 Execution Truth
L1 must return execution receipt, not merely result content.

15 Boundary
L2 is the critical membrane translating controller decision into bounded executable contract and translating L1 evidence back into checkpoint state.

16 Holdout
A novel task tests whether L2 can instantiate a valid bounded contract from L3 selection without project-specific hardcoding.

17 Ablation
Ablate L2: authority/context leak. Ablate L3: no adaptive selection. Ablate L1: no realized work. This supports distinct responsibilities.

18 Zero-Request
With no task, L3 may discover/select observation work, L2 must bind it without inventing substantive authority, L1 executes only licensed observation.

19 DOS
DOS can freeze any of L1, L2, L3, their pairwise boundaries, or the full cycle. Pairwise DOS is likely especially informative.

20 Consequence Closure
The architecture needs explicit loop closure:
L3 Select -> L2 Bind -> L1 Execute -> L2 Checkpoint -> L3 Reconcile/Reselect.

## Reconciliation B

The strongest structural result is a corrected three-level cycle:

L3 ControllerSelect
  -> L2 Bind(TaskFrame, TransitionContract, Authority)
  -> L1 Execute
  -> L2 Observe + Checkpoint
  -> L3 Reconcile + Reselect

with activation receipt across the downward edge and execution/evidence receipt across the upward edge.

This is compatible with A5 but adds a realization obligation not captured by capability registration alone.

## Immediate consequence for system build

Before merely adding more C-family adapters, test and implement the activation bridge:
Available(program) != Invoked(program).

Required trace:
Select -> Bind -> Dispatch -> Execute -> Receipt -> Consume -> Reselect.

Then use DOS on pairwise boundaries L3/L2 and L2/L1 as the next observation experiments before deciding whether architecture changes are required.
