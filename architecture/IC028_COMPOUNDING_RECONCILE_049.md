# IC-028 Compounding Full-Spectrum Correction 049

Date: 2026-09-24
Controller: IC-028
Decision: REVISE prior independent-observation default

## Rewritten prompt

Treat the user's objection as a result-sensitive challenge, not resistance to testing. Optimize for accomplishing the live job. Determine when tool outputs should immediately update the state seen by later tools, when independent frozen-state observations are useful as experiments, and whether a Reconcile operation is missing. Re-audit FullSpectrum, ScopeMode36, Sort Later/Handoff, Architect+Goal, and autonomous ownership. Do not claim 36 vs 35 behavior without experiment.

## Finding 1: sequential compounding is the live-work default

Prior Stage A overgeneralized an experimental-control technique.

For operational research:
X_0 --T1--> X_1 --T2--> X_2 ... --Tn--> X_n.

Each admitted material delta updates the working state before the next tool.

This preserves compounding gain:
Delta_i can change the referents, distinctions, architecture, candidates, and execution plan available to T_(i+1).

Frozen sibling observation remains useful for:
- matched experiments;
- attribution/ablation;
- detecting order effects;
- independent replication;
- measuring marginal contribution.

It is not the default live-work regime.

## Finding 2: Reconcile is a missing first-class operation

Sequential compounding creates its own risk: later outputs can conflict with, subsume, reinterpret, or invalidate earlier outputs.

Define:

Recon(S,{r_i}) -> <S',Conflicts,Subsumptions,Revisions,NewRelations,OPEN>.

Reconcile occurs:
- after any material tool result before downstream consumers when semantic identity changed;
- at workflow barriers;
- before persistence/strong completion;
- after parallel/independent waves.

Reconcile is distinct from Admit:
Admit asks whether a result may enter.
Reconcile asks how admitted results jointly alter the coherent state.

Candidate tool family: RECONCILE / SYNTHESIS CLOSURE.

This is a serious candidate to replace or split one of FullSpectrum20 after basis audit, not automatically tool #21.

## Finding 3: FullSpectrum becomes compounding/adaptive

Default live run:

Freeze goal/basis
-> WorkflowArchitect initial DAG
-> Architect/Goal structural preflight
-> T1
-> Admit
-> Reconcile
-> MaterialDelta/JaneSync as relevant
-> replan remaining DAG
-> T2 on updated state
-> ...
-> final Reconcile
-> Architect+Goal
-> verification/completion.

Every selected tool receives the strongest current admitted state.

The wrapper can intentionally request FROZEN_WAVE mode for experiments.

## Finding 4: Architect + Goal has a legitimate composite

Do not collapse Architect and Goal Spine semantically.

A=<roles,relations,interfaces,boundaries,authority,state,transitions>
G=<target,success conditions,dependency/commitment spine>.

But their interaction is result-sensitive:
architecture can be coherent while serving the wrong goal;
goal spine can be coherent while lacking realizable architecture.

Create configured composite candidate:
GOAL-ARCHITECT (GA).

GA(J,S) iterates:
RecoverGoal -> Architect -> GoalSpineCheck -> detect mismatch -> revise candidate architecture/workflow -> recheck.

GA is a configured composite, not evidence that Goal=Architecture.

## Finding 5: Handoff vs Sort Later

Historical Sort Later:
nonblocking capture for genuinely unresolved/unroutable discoveries; known destinations should be routed rather than parked.
Its failure mode was flat accumulation and weak guaranteed review/activation.

IdeaHandoff is broader:
it carries routing/ownership/dependency/status/receipt and can target active or deferred Work.

Therefore:
SortLater is one disposition inside Handoff, not a peer system.

Handoff(h) -> one of:
ROUTE_NOW
AUTO_EXECUTE
DEFER_OPEN
ASK_USER_AUTHORITY
REJECT_WITH_BASIS.

SortLater ~= DEFER_OPEN for nonblocking unresolved items.

This preserves the useful pressure-valve behavior without recreating a flat forgotten queue.

## Finding 6: user involvement policy

RoleAssignment adds an AuthorityNeed coordinate.

Routine internal work with existing authority:
Jane captures/monitors -> IC028 activates/executes -> receipt -> Jane update.
Do not surface merely for permission.

Surface to user when:
- new authority/permission is required;
- destructive/external action requires consent;
- protected goal/value tradeoff is unresolved;
- material ambiguity cannot be resolved from current basis;
- requested checkpoint/report is due.

Thus most handoffs can disappear from the user's cognitive workload while remaining auditable.

## Finding 7: 36 vs 35

Prior claim was too strong because no matched 35-vs-36 experiment has been run.

Current status:
OPEN_EMPIRICAL.

Hypotheses:
H_additive: marginal value of cell 36 resembles ordinary cell value.
H_closure: completing the full typed surface produces a qualitative integration/closure effect.
H_order: benefit depends on which cell is omitted and execution order.
H_interaction: full 36 enables higher-order relations unavailable from 35.

Test separately by job class:
kernel/foundation design;
architecture design;
 research discovery;
 paper outline;
 final paper;
 paragraph/prose.

Use matched ablations:
36/36 versus each 35/36 omission, with order controls and outcome measures.
Do not infer from cardinality alone.

Until evidence:
for high-stakes foundational design, default to 36/36 terminal coverage because omission cost may be high.
for small/local prose jobs, use adaptive coverage unless experiment shows closure gain.

## Finding 8: tool-use hesitation

Root cause confirmed:
pre-execution relevance gating plus cost/complexity aversion caused under-invocation.

Repair:
tools are epistemic probes, not merely actions.
A cheap configured probe can be warranted even when relevance is uncertain.

IC028 policy:
when FullSpectrum is explicitly invoked, default disposition is PROBE, not NON_APPLICABLE.
A family becomes NON_APPLICABLE only after a basis is recorded.

## Finding 9: role of Jane

Jane continuity duties:
- capture admitted deltas and receipts;
- track unresolved Handoffs;
- detect stale/orphaned work;
- maintain cross-episode connection graph;
- send candidate obligations/context to IC028.

IC028 duties:
- choose/sequence/execute research work;
- reconcile results;
- discharge routine handoffs under existing authority;
- keep Jane synchronized.

## Decision

1 Replace independent-observation default with sequential compounding for live work.
2 Preserve frozen waves as an experimental mode.
3 Admit Reconcile as a first-class candidate operation.
4 Build Goal-Architect as configured composite candidate.
5 Treat Sort Later as DEFER_OPEN disposition of Handoff.
6 Routine authorized handoffs execute without user involvement.
7 Mark 35-vs-36 synergy OPEN and run matched lab ablations.
8 For foundational architecture work pending those results, use full 36 coverage rather than assume omitted cells are harmless.
9 FullSpectrum explicit call means every family gets at least a configured PROBE.
