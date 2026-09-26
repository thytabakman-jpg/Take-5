# ImprovementCore Legacy Restoration Closure 133

Date: 2026-09-26
Status: CLOSED_RELATIVE / REPOSITORY-OWNED RESTORATION
Controller: IC-028
Recurrence: HF002

## Terminal execution receipt

ImprovementCore Legacy Restoration 130:
- GitHub Actions run: 36279580480
- result: SUCCESS
- artifact: improvecore-legacy-restoration-130
- artifact id: 10918900119
- artifact digest: sha256:4eea181cee28fc1f7d98bb3f226761a8a52d750eda2456f89b6457b121510753

Final ImprovementCore result:
- status: COMPLETE
- HF2: RELATIVE_CLOSE
- HF2 rounds: 5
- repository_restoration_status: CLOSED_RELATIVE

## Recovered controller behavior

Repository-owned restored path:

runtime/improvement_core_restored_dispatch.py
->
runtime/improvement_core_legacy_restored.py
->
runtime/improvement_core_legacy_candidate.py
->
frozen ICC128 Legacy endogenous loop and rho_128 policy.

Protected restored loop:

G_Q -> G_W -> S -> E -> A -> U -> G_Q.

Restored behaviors include:
- endogenous question generation;
- discriminating work generation;
- CHEAP_DIRECT routing;
- nondominated plural routing;
- result-sensitive reselection;
- no premature terminality;
- configured-tool execution truth;
- typed OPEN/BLOCKED/CONFLICT;
- entry/authority binding;
- external acquisition;
- durable material knowledge capture;
- observer fail-closed behavior;
- outer HF002 local recurrence.

## Validation basis

Control holdouts:
artifacts/improvecore/LEGACY_CANDIDATE_CONTROL_HOLDOUT_131_2026-09-26.md

Result:
- four unlike control holdouts PASS;
- two causal ablations PASS.

Semantic routing holdouts:
artifacts/improvecore/LEGACY_RESTORED_SEMANTIC_HOLDOUT_132_2026-09-26.md

Result:
- four unlike semantic-routing holdouts PASS;
- user supplied no tool sequence;
- evidence class is explicitly HOST_MODEL_SUPPLIED_SEMANTIC_FRONTIER + REPOSITORY_CONTROL_EXECUTION;
- this is not independent-agent replication.

The existing FDR prospective holdout remains separate supporting evidence.

## Governed dispatch boundary

The restored repository dispatch requires an explicit semantic provider.

When no semantic provider is bound:

RESTORED_SEMANTIC_PROVIDER_REQUIRED
->
OPEN.

It must not silently substitute the older fixed-stage controller while reporting restored execution.

The older runtime/improvement_core_dispatch.py path remains a compatibility/debug surface until an external host can supply the restored semantic binding automatically.

## Remaining external boundaries

1. MASTER_THREE_MONTH_ARCHIVE_NOT_YET_ADDRESSABLE

The requested complete recent ChatGPT history/file archive has not become addressable to this repository/chat execution path. No completeness claim is made for unrecovered source material.

2. AUTOMATIC_UNIVERSAL_CHAT_HOST_SEMANTIC_BINDING_EXTERNAL_NOT_OWNED

Repository code cannot force every unrelated ChatGPT host session to bind its active reasoning model into the restored semantic-provider interface.

These are typed external boundaries, not licensed internal controller-repair tasks.

## Anti-churn terminal rule

No further controller repair is licensed without:
- a failing protected behavioral witness;
- newly recovered historical evidence that changes the target;
- an execution/currentness/provenance break;
- or a real project exposing a material controller failure.

Unchanged repair routes are NO_GAIN.

Ordinary project work may resume on the current repository basis.
