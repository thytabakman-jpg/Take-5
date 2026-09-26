# ImprovementCore Evidence Run 113

Date: 2026-09-26
Controller: IC-028
Regime: 090
Target: prior full-system Show-Me-the-Math campaign closure
Input role: EVIDENCE_NOT_DRAFT
Source evidence:
artifacts/full-system-campaign/MT_AUDIT_PRIOR_CAMPAIGN_SUMMARY_003_2026-09-26.md
Machine-readable packet:
artifacts/improvecore/MT_EVIDENCE_PACKET_113_2026-09-26.json

## Governing constraint

The MT output is evidence.

It is not treated as:
- a draft;
- a patch;
- a candidate architecture;
- a mandatory plan;
- an authorized mutation.

ImprovementCore owns the inference and next-work choice.

## Entry

Mode:
OBSERVE_DECOUPLED.

Reason:
the target is a claim/evidence audit where outcome-directed mutation before evidence
reconciliation would contaminate the inference.

Current controller path:

dispatch_improvement_core
-> run_improvement_core_regime
-> run_improvement_core_manager
-> run_ic028.

## Evidence consumed

Verified:
E1-E8 from MT Evidence Packet 113.

Unresolved:
U1-U3.

The unresolved coordinates all concern one causal chain:

campaign-specific ICC128 Legacy Controller.run
-> exact run_result
-> admitted learning report
-> report hash
-> GitHub commit receipt
-> Take-5 activation closure.

## Controller reconstruction

### OBSERVE

The controller sees eight verified evidence items and three unresolved evidence items.

### OBSERVE_RECONCILE

Verified positives are preserved.

No unresolved item is collapsed to false or treated as satisfied.

### OBSERVE_TRC

The only licensed transition is:

evidence
-> controller inference.

Input evidence does not self-authorize a system mutation.

### RECOVER_GOAL

Determine the evidence-supported campaign status and choose any next work without treating
the MT result as a draft or mandated plan.

### CURIOSITY_PD

Recovered generator:

EXECUTION_TRUTH_RECEIPT_GAP.

### FORMALIZE

The evidence-supported campaign status is:

VERIFY_REQUIRED.

The unsupported completion coordinate is:

CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED.

### GENERATE_WORK

ImprovementCore generates its own frontier rather than inheriting one from MT.

Candidate A:

OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT

Coverage:
U1, U2, U3.

Candidate B:

DOWNGRADE_LABEL_ONLY

Coverage:
none of U1-U3.

### SELECT

Selected:

OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT.

Basis:

it directly covers the entire live unresolved evidence set.

### EXECUTE

Because this run is evidence-evaluation in observer-first mode, EXECUTE performs the
analytical selection/receipt decision only.

No repository architecture mutation is performed in this run.

### ADMIT

Admitted controller decision:

REOPEN_PRIOR_CAMPAIGN_CLOSURE.

Supported prior campaign state:

VERIFY_REQUIRED.

Residual:

CAMPAIGN_SPECIFIC_ICC128_LEGACY_CONTROLLER_EXECUTION_RECEIPT_REQUIRED.

### RECONCILE

Preserved:
- PR #105 merge receipt;
- MT/GOAL configured-plan validation;
- ToolConductor 91-factor traversal;
- ICC130 typed blocker;
- standalone ICC128 Legacy reference self-test;
- report-file persistence;
- CI pass.

Removed:
- inference from those facts to campaign-specific Legacy controller COMPLETE.

New architecture admitted:

none.

### PROPAGATE_AFFECTED_CONE

Affected cone only:

ICC128_LEGACY_CAMPAIGN_EXECUTION_TRUTH
CAMPAIGN_CLOSURE_STATUS.

### PERSIST

This run record and its evidence packet are the durable evidence receipt.

### VERIFY

Required assertions:

- MT input role remains EVIDENCE_NOT_DRAFT;
- selected next work was generated from live evidence gaps;
- no mutation was performed;
- verified positive claims were preserved;
- unsupported completion was removed;
- no architecture was admitted from the MT artifact.

Expected verification:

PASS.

## ImprovementCore disposition before external CI

Controller run:
COMPLETE relative to evidence-evaluation job.

Prior campaign:
VERIFY_REQUIRED.

Licensed next work:

OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT.

Mutation performed:

false.

## Why this is not a draft-driven run

The MT artifact does not contain an authorized repair sequence.

ImprovementCore reconstructs:
- the goal;
- the generator;
- the work frontier;
- the selected next work;
- the admissible state transition.

The MT artifact supplies facts and unresolved coordinates only.

## External verification

Executable regression:

tests/test_improvement_core_mt_evidence_20260926.py

The regression directly runs the current ImprovementCore dispatcher/regime/IC-028 path
against the machine-readable MT evidence packet and checks the observer-first stage
receipts and final evidence-based decision.

## Basis transport

MT evidence target basis:

6a1594ae8c92e8bb6ef173f51e68f1e30dd48154.

Current ImprovementCore validation base:

9bfc10803c048d53f5cb21c27c494a972d4431fa.

The newer base includes the function-first PD discovery integration.

The evidence conclusion survives transport to that current controller basis.

## External verification receipt

Take-5 Validation:

workflow run 36265231391
conclusion: SUCCESS.

Capability Preservation:

workflow run 36265231408
conclusion: SUCCESS.

The executable regression directly ran the current:

dispatch_improvement_core
-> run_improvement_core_regime
-> run_improvement_core_manager
-> run_ic028

path in OBSERVE_DECOUPLED mode.

It verified:

- full MT configured plan remains 36 / 792 / 144;
- the mandatory black-box spine remains PD -> PDAudit -> MTA -> MT -> PDAudit -> C47;
- the MT packet is admitted as EVIDENCE_NOT_DRAFT;
- ImprovementCore generates its own work frontier;
- ImprovementCore selects OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT;
- no repository mutation occurs in this evidence-evaluation run;
- verified positive campaign claims remain preserved;
- prior campaign closure is reopened to VERIFY_REQUIRED;
- no new architecture is admitted from the MT artifact.

## Final disposition

ImprovementCore evidence-evaluation run:

COMPLETE.

MT audit:

CLOSED_RELATIVE.

Prior campaign execution-truth status:

VERIFY_REQUIRED.

Licensed next work:

OBTAIN_CAMPAIGN_SPECIFIC_LEGACY_EXECUTION_RECEIPT.

Mutation performed:

false.

Input treatment:

EVIDENCE_NOT_DRAFT.
