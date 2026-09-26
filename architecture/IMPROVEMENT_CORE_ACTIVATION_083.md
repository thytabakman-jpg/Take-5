# ImprovementCore Activation Repair 083

Date: 2026-09-26
Status: IMPLEMENTED / VALIDATED / MERGED
Regime version: 083

## Defect

The maximization repair added recursive parent/child management, basis-relative
learning memory, and a cumulative-autonomous regime surface.

However, runtime/improvement_core_regime.py only delegated to the rich stage manager
and returned.

Therefore:

component present
!=
component active in normal regime execution.

This reproduced the same preservation defect seen elsewhere:
capability existence without activation.

## Repair

The regime now executes the stage manager first.

When the resulting controller state has live_continuation=true:

1. recursive manager bindings are required;
2. missing bindings return OPEN with RECURSIVE_MANAGER_HANDLERS_REQUIRED;
3. the parent-owned recursive manager executes selected child work;
4. child returns pass admission/reconciliation;
5. parent state updates;
6. recurrence continues until typed terminality or blocker.

Learning memory is now active:

- stage results may emit typed learning_events;
- recursive route selection checks prior basis-relative NO_GAIN / REJECTED / FAILED evidence;
- an unchanged blocked route returns OPEN with
  IC_MANAGER_LEARNING_BLOCKED_UNCHANGED_ROUTE;
- a relevant dependency-coordinate change can reopen the route;
- admitted material child results record GAIN evidence.

## Compatibility

ImprovementCoreRegimeResult keeps receipt and result compatibility properties so
existing dispatch consumers can continue to access the underlying stage-manager result.

## Recovery correction

Recovery currentness no longer depends on one hard-coded latest merge hash.

The live regime exports REGIME_VERSION=083.

The recovery manifest records regime_version=083.

The recovery validator requires equality between the executable regime version and the
manifest version, plus the activation contract.

Historical PR/merge/validation receipts remain provenance rather than a frozen definition
of currentness.

## Protected tests

Tests now require:

- live continuation activates recursive management;
- live continuation without recursive bindings returns OPEN;
- recursive child completion remains parent-owned;
- unchanged no-gain route is blocked by learning memory;
- normal nonrecursive dispatch remains compatible;
- recovery manifest version matches executable regime version.

## OPEN

- automatic generation of recursive handlers from the full admitted capability basis;
- zero-request upstream discovery;
- relation-generation/admission mathematics;
- universal host interception;
- broad-vs-cheap route empirical calibration;
- global maximality/minimality.

## Closure rule

Validation passed in PR #53, run 36220513144.\n\nMerged to main as 2dfe684886898f5a39ccd6c06f9a0b9e27695ff7.\n\nThis repair is current.
