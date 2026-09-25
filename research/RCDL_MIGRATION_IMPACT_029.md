# RCDL Migration Impact and Six-Scope Repair 029

Date 2026-09-24
Target Take-5 migration readiness after PR129 breakthrough
Status BLOCKING ARCHITECTURE DELTA UNDER TEST

## Breakthrough

The protected discovery behavior is better modeled as controlled representation-coupled endogenous discovery.

Core interaction:
admitted discovery -> representation/view update -> changed candidate universe -> recursive discovery.

This is stronger than static G_relation.

## Root cause against Take-5

Take-5 has endogenous work regeneration, relation semantics, multi-object analysis, GDOS, ImproveCore reentry, currentness, and closure.

But the top-level lifecycle does not yet make view regeneration and candidate-universe change first-class reentry triggers.

Therefore the current implementation can legally close after exhausting work generated from an impoverished representation.

Root cause:
REPRESENTATION-COUPLED CANDIDATE-UNIVERSE REGENERATION GAP.

## Six-scope Architecture pass

SYSTEM
ResearchSystem must own controlled representation-coupled endogenous discovery, not only endogenous work regeneration.

SUBSYSTEM
WorkLifecycle needs a View/Representation subsystem and candidate-universe coverage state.

COMPONENT
Add active-view family, view generator, candidate-universe snapshot/delta, relational saturation basis, Observe/Refocus state.

INTERFACE
Required cycle:
State -> Views -> Generators -> CandidateAudit -> Worker -> Admission -> StateUpdate -> ViewRegeneration -> CandidateUniverseDelta -> Reentry.

BOUNDARY/DECOMPOSITION
Views are lossy generative projections, not authoritative state.
Generators propose; admission governs truth/authority.
ImproveCore remains controller, not state or view identity.
No new primitive O required.

CROSS-LAYER
A material relation/view delta at local/project/cross-project/meta scale must propagate to every affected candidate generator and closure certificate.

## Six-scope Transfer pass

SOURCE
Take-2 discovery/update/reentry behavior and PR129 RCDL synthesis.

TARGET
Take-5 EWG architecture.

TRANSFER OBJECT
Behavioral invariant: admitted discoveries can change representation, which can expose previously unavailable consequential candidates.

PRESERVATION
Preserve goal/referent continuity, authority, execution truth, OPEN/BLOCKED, evidence admission, bounded search, persistence, rollback.

ADAPTATION
Do not copy Take-2 implementation. Realize behavior through Take-5 typed state/views/generators/admission/reentry.

VERIFICATION
Require prospective mixed-corpus holdout and ablation:
A current discovery
B static G_relation
C G_relation + dynamic view regeneration
D full RCDL Observe/Refocus.
Measure true discovery, false relations, downstream result change, search cost, path dependence, closure quality.

## Migration consequence

Previous GO is invalidated because this is result-sensitive to a protected predecessor behavior: the connection-discovery behavior was explicitly part of the migration target.

Current migration state:
NO-GO pending implementation and prospective validation.

This is not grounds to discard Take-5.
The architecture is extensible enough to absorb the breakthrough as a controller/lifecycle extension without a new primitive operator or new controller.
