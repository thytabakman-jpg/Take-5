# ImproveCore Anti-Repeat and Durable Progress 110

Date: 2026-09-26
Status: IMPLEMENTED / VALIDATED / MERGED
Target regime: 090

## Root defect

The repeated regression loop was not one missing tool. Three already-built protections were separated:

1. basis-relative learning memory blocked no-gain routes only inside one live Python object;
2. candidate frontiers were formed before learned no-gain routes were removed;
3. the stronger semantic strict-progress relation existed on an unpromoted branch and therefore did not govern recurrence.

A fresh invocation could therefore forget a prior no-gain proof, admit the same route again, and produce a new artifact without a new continuation-relevant effect.

## Repair

Regime 090 makes one path authoritative:

durable ledger -> admission filter -> execution -> parent update -> canonical progress comparison -> learning record -> durable persistence -> reentry.

Negative route evidence is stored by route, basis, dependency footprint, and evidence. Retry is licensed only by a relevant dependency/basis change or another explicit defeat condition.

Plural candidate frontiers are filtered through learned no-gain memory before nondominated routing. A blocked route can no longer crowd out a fresh route.

Recursive parent updates are evaluated by runtime/improvement_core_progress_relation.py. Raw material-delta labels become typed effect witnesses at the parent-state boundary; protected regression prevents a strict-progress claim.

Explicit semantic-class recurrence with no net effect is recorded as CYCLE_NO_GAIN and blocked on the same basis.

## Persistence boundary

runtime/improvement_core_learning_memory.py loads integration/IMPROVEMENT_CORE_DURABLE_LEARNING_110.json by default and atomically writes newly certified negative learning records. Positive GAIN traces remain run-local because they do not need to prohibit future work.

Repository commits remain a host responsibility. The runtime guarantee is that a persistent checkout cannot silently forget certified negative learning between processes; the recovery anchor makes the durable ledger a mandatory recovery surface.

## Protected behaviors added

- CANONICAL_PROGRESS_RELATION_GOVERNS_RECURSIVE_GAIN
- DURABLE_NEGATIVE_ROUTE_MEMORY
- LEARNED_NO_GAIN_FILTERS_BEFORE_FRONTIER
- SEMANTIC_CYCLE_NO_GAIN_BLOCKING
- RETRY_REQUIRES_RELEVANT_CHANGE

## Closure rule

A new file, timestamp, wording change, or repeated audit is not progress by itself. Reentry requires a typed effect at the claimed boundary or a licensed change that invalidates the prior no-gain record.


## Validation evidence

PR #87
- merge commit 44cea13bdcd1e2c06fe44699d4152d653180daa9
- Take-5 Validation 36249459966
- Capability Preservation 36249459971
- full test suite, canonical whole-system audit, closed-loop fixture, zero-request dump, and capability-preservation gate passed on the exact PR head before merge.
