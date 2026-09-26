# ImproveCore Self-Study 104 Receipt

Date: 2026-09-26
Status: EXECUTED / VERIFIED / RELATIVE_CLOSE_WITH_STRICT_GAIN_CANDIDATES
Repository: thytabakman-jpg/Take-5
Controller: IC-028
Regime: 087
Mode: EXPAND_OBSERVE_DECOUPLED

## Execution evidence

Self-study workflow:
- workflow: ImproveCore Self Study 104
- run id: 36225561523
- conclusion: success
- head commit: b3949216eb620528882bf0d0312516d4640e2bfb

Repository validation:
- workflow: Take-5 Validation
- run id: 36225561339
- conclusion: success

Input:
integration/IMPROVECORE_SELF_STUDY_INPUT_104_2026-09-26.md

External research:
research/IMPROVECORE_EXTERNAL_ARCHITECTURE_RESEARCH_104_2026-09-26.md

Executable self-study:
runtime/improvement_core_self_study.py

## Reconstructed current architecture

Current execution chain:

user invocation
-> improvement_core_dispatch
-> zero-request upstream discovery when coordinates are absent
-> improvement_core_regime
-> external-acquisition preflight
-> improvement_core_manager / IC-028
-> recursive parent-child management when continuation remains live
-> basis-relative learning memory
-> verification / relative close

Verified present:
- basis-relative route learning;
- recursive parent-child management;
- CapabilityFoundry;
- structured in-memory operator receipts and manager traces;
- host-injected external adapters;
- OPEN/BLOCKED/CONFLICT preservation;
- observer-first mode geometry.

## Material gaps / candidates

### IC-TRACE-EXPORT
Classification: STRICT_GAIN_CANDIDATE
Disposition: ADMISSION_READY_CANDIDATE
Risk: LOW

Current runtime already emits typed receipts and recursive traces but has no first-class normalized durable trace-export surface.

Minimal candidate:
pure projection from existing receipts into a stable structured trace schema.

### IC-DURABLE-RUN-JOURNAL
Classification: STRICT_GAIN_CANDIDATE
Disposition: OPEN_DESIGN_REQUIRED
Risk: MEDIUM

Current core runtime does not expose durable execution checkpoints/event history/replay.

LearningMemory records route outcomes, not the execution cursor.

Minimal candidate:
append-only run event journal plus checkpoint cursor, kept separate from learning memory.

### IC-HOST-CAPABILITY-DISCOVERY
Classification: STRICT_GAIN_CANDIDATE
Disposition: OPEN_HOST_BOUNDARY
Risk: MEDIUM

External acquisition accepts host-injected adapters but does not automatically discover available host capabilities.

Minimal candidate:
typed adapter registry/discovery contract without self-authorizing use.

### IC-RUNTIME-LIFECYCLE-FAILURE-SEMANTICS
Classification: STRICT_GAIN_CANDIDATE
Disposition: OPEN_DESIGN_REQUIRED
Risk: MEDIUM_HIGH

Recursive child management validates returns and no-progress, but has no explicit retry, cancellation, or resume policy.

Minimal candidate:
typed child execution lifecycle policy composed with durable run journaling.

### IC-INTERFACE-QUALITY-BENCHMARK
Classification: STRICT_GAIN_CANDIDATE
Disposition: EXPERIMENT_READY
Risk: LOW_MEDIUM

No standardized matched ablation of alternative tool/adapter interfaces was found in the core runtime.

Minimal candidate:
matched benchmark of equivalent tasks across alternative tool/adapter interfaces.

### IC-REFLECTION-EVIDENCE-SCHEMA
Classification: COMPOSE_EXISTING_FIRST

LearningMemory already stores arbitrary evidence, so a new memory layer is not justified.

Minimal candidate:
test richer reflective evidence conventions inside the existing memory object first.

### IC-CAPABILITY-SKILL-PROMOTION
Classification: PARTIAL_EXISTING
Disposition: EXPERIMENT_BEFORE_ARCHITECTURE

CapabilityFoundry and ToolManifest already cover typed capability creation/admission.

Minimal candidate:
test whether repeated successful child routes can be promoted through existing foundry/manifest machinery before adding a new skill-library architecture.

## Architecture decision

No new master controller or memory layer was admitted.

Execution checkpointing remains distinct from learning memory.

IC-TRACE-EXPORT is the only candidate admitted for the next implementation experiment.

Larger runtime changes remain OPEN pending design evidence.
