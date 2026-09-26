# Full Configured MT Audit 003 — Prior Campaign Summary as Evidence

Date: 2026-09-26
Target: the immediately preceding assistant summary of the full-system Show-Me-the-Math campaign
Basis: Take-5 main 6a1594ae8c92e8bb6ef173f51e68f1e30dd48154
Configured tool: MT
Mode: OBSERVER
Wrapper: canonical math-first wrapper
Geometry: D36_C = 6 scopes x 6 mode faces = 36 cells
Question coverage: Q01-Q22 across all 36 cells = 792 projections
Cognitive coverage: DIFFERENTIATE / RELATE / RECONSTRUCT / STRENGTHEN across all 36 cells = 144 projections
Black-box return gate: applied
Closure/reentry: applied
Use of this artifact downstream: EVIDENCE, NOT DRAFT

## 1. Frozen target claims

The prior summary asserted, in substance:

1. PR #105 was merged into Take-5.
2. full configured MT geometry was externally validated at 36 cells / 792 question projections / 144 cognitive projections;
3. ToolConductor traversed all 91 registered factors, with 60 self-contained and 31 portability-open;
4. ICC130 had no recovered identity and was typed BLOCKED(IDENTITY_UNRECOVERED);
5. ICC128 Legacy ran, its controller disposition was COMPLETE, and its mandatory learning report was committed;
6. the campaign was COMPLETE_RELATIVE.

MT evaluates those as claims requiring distinct evidence classes.

## 2. Full 36-cell quotient

The 36 cells collapse to eight non-equivalent distinctions.

### D1. PLAN_VALIDATED != SEMANTIC_TOOL_EXECUTED

The campaign regression proves that a full configured MT execution plan can be built with:

- wrapper required;
- OBSERVER mode;
- 36 cells;
- 792 question projections;
- 144 cognitive projections.

That is strong configured-plan evidence.

It is not by itself a repository-native semantic MT execution receipt for the conversation.

The campaign report itself correctly classified MT conversation semantics as host-bound configured execution.

### D2. TOOLCONDUCTOR_TRAVERSAL != ALL_FACTORS_EXECUTED

The campaign regression directly calls run_tool_conductor.

It proves:

- tool_count = 91;
- one conductor-level disposition per registered tool;
- ToolConductor self factor = EXECUTED_SELF_WITNESS;
- portability_open_set cardinality = 31.

OPEN/BLOCKED factors remain non-success dispositions.

The prior summary preserved this distinction.

### D3. PORTABLE_LEGACY_SELF_TEST != CAMPAIGN_SPECIFIC_LEGACY_RUN

The campaign regression executes:

runtime/icc128_legacy_portable.py

as its built-in self-test.

That self-test proves the standalone frozen-controller reference realization executes a
two-step fixture and preserves fail-closed behavior.

It does not prove that the campaign-specific semantic episode recorded in:

artifacts/icc128-legacy-learning/icc128-legacy-full-system-show-math-20260926-004.json

was produced by an actual Controller.run invocation over that campaign state.

### D4. REPORT_PRESENT != REPORT_DERIVED_FROM_RUNTIME_RESULT

The campaign regression verifies that the Legacy JSON report exists and contains expected
schema/run fields.

It does not establish a causal chain:

campaign Controller.run
-> run_result
-> build_learning_report(run_result)
-> report hash
-> GitHub commit receipt.

The report is evidence-bearing, but its campaign-specific runtime provenance is not
currently witnessed by the regression.

### D5. GITHUB_COMMIT_EXISTS != LEGACY_RECEIPT_VALIDATED_BY_RUNTIME

The report was committed to Take-5.

However, the campaign regression did not call either:

runtime/icc128_legacy_reporting.require_github_receipt

or the standalone portable:

take5_activation_closed(receipt)

with a receipt causally tied to the committed report hash.

Thus report persistence exists, while the exact activation-closure receipt chain is not
fully demonstrated by the campaign regression.

### D6. ICC130_ABSENCE != ICC130_NONEXISTENCE_IN_ALL_POSSIBLE_SOURCES

The campaign evidence establishes:

- no ICC130 in the current Take-5 registered repertoire;
- prior canonical searches found no ICC130 in Take-5 or Reaserch;
- no recovered exact ICC130 identity was available to the run.

Therefore the typed disposition:

ICC130 = BLOCKED(IDENTITY_UNRECOVERED)

is supported for that basis.

The stronger metaphysical claim that no ICC130 could exist anywhere is neither made nor needed.

### D7. CI_PASS != EVERY_NARRATIVE_CLAIM_VERIFIED

Take-5 Validation and Capability Preservation passed.

Those workflows externally verify the tests they execute.

They do not automatically convert narrative claims outside the tested predicates into execution receipts.

### D8. CAMPAIGN_ARTIFACT_COMPLETE != CAMPAIGN_EXECUTION_TRUTH_COMPLETE

The campaign successfully created its required durable artifacts.

But one load-bearing execution-truth coordinate remains unsupported:

campaign-specific ICC128 Legacy controller execution.

Therefore artifact completion and execution-truth completion diverge.

## 3. Mandatory black-box decomposition

Material black box:

LEGACY_CAMPAIGN_EXECUTION_TRUTH.

Configured semantic-resolution spine:

PD/Q03 Difference Math
-> PDAudit/Q18 Verify Math
-> MTA/Q01 Basic Math
-> MT/Q02 Change Math
-> PDAudit/Q18 Verify Math
-> C47/Q19 Completion Check.

### PD / Difference Math

Separate:

A. portable reference self-test;
B. campaign-specific controller execution;
C. report serialization;
D. GitHub persistence;
E. exact Take-5 activation closure.

These are five different objects.

### PDAudit / Verify Math

The prior campaign regression directly witnesses A and report presence.

It does not directly witness B -> C -> D -> E as one causal chain.

### MTA / Basic Math

Required receipt structure for the missing coordinate:

R_legacy
=
<
RunID,
InitialState,
InitialMemory,
ControllerRuntime,
Trace,
Terminal,
ReportHash,
GitHubCommit
>.

The current evidence includes RunID, declared state/memory, declared trace, terminal, and
GitHub commit, but lacks a runtime execution receipt binding the declared trace to
Controller.run.

### MT / Change Math

The smallest correction is not to discard the campaign.

It is to change the campaign completion classification from:

COMPLETE_RELATIVE

to:

VERIFY_REQUIRED

with one precise residual:

CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED.

### second PDAudit

This correction preserves every already-verified positive claim:

- PR merge;
- configured-plan geometry;
- ToolConductor exhaustive traversal;
- ICC130 typed blocker;
- artifact persistence;
- standalone Legacy portability self-test;
- CI success.

It removes only an unsupported inference.

### C47 / Completion Check

The MT audit itself is complete relative to the current evidence.

The underlying campaign execution truth is not fully closed.

## 4. Evidence ledger

### VERIFIED_NATIVE / EXTERNAL

E1.
PR #105 merge commit:
6a1594ae8c92e8bb6ef173f51e68f1e30dd48154.

E2.
Take-5 Validation passed on the campaign branch.

E3.
Capability Preservation passed on the campaign branch.

E4.
Campaign regression constructs complete configured MT and GOAL plans.

E5.
Campaign regression directly invokes ToolConductor and verifies 91-factor coverage.

E6.
Campaign regression directly executes the standalone ICC128 Legacy reference self-test.

E7.
Legacy learning-report file exists in canonical Take-5.

### VERIFIED_HOST_BOUND / SEMANTIC

E8.
The conversation-level MT and GOAL analyses were explicitly classified as host-bound
configured semantic execution rather than repository-native semantic workers.

### NOT YET VERIFIED

U1.
The specific campaign Legacy trace was generated by Controller.run over the campaign's
initial state and memory.

U2.
The committed Legacy report was generated from that exact runtime result by the admitted
report builder.

U3.
The committed report hash and GitHub commit were passed through the exact Legacy closure
receipt validator as one causal chain.

## 5. MT final disposition

Audit of the prior summary:

MATERIAL_YIELD
-> CORRECTION_REQUIRED
-> CLOSED_RELATIVE.

Corrected prior-campaign state:

VERIFY_REQUIRED.

Single residual:

CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED.

## 6. Downstream handoff rule

This MT result is evidence.

It is not:

- a patch;
- a candidate architecture;
- a requested mutation;
- a preselected ImprovementCore plan.

ImprovementCore receives:

- verified evidence E1-E8;
- unresolved evidence U1-U3;
- the corrected claim boundary;
- no mandated repair sequence.

ImprovementCore owns the next-work decision.
