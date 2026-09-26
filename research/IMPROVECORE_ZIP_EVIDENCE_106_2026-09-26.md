# ImproveCore ZIP Evidence 106

Date: 2026-09-26
Status: EVIDENCE PACKET / NOT CANONICAL AUTHORITY

## Scope

Library inventory found 37 model-generated ZIP archives across two complete metadata pages.
This run deep-inspected 13 high-signal system/research archives and used the remaining visual/archive ZIPs as lineage metadata.
Private WhatsApp ZIP exports were intentionally excluded.

Deep-inspected archives:
- PD_AUDIT_EXPERIMENT_v0.1.zip
- PD_AUDIT_EXPERIMENT_v0.1_with_pilots.zip
- PD_AUDIT_EXPERIMENT_v0.2.zip
- PD_Canonical_Baseline_v0.1-candidate.zip
- PD_Canonical_Baseline_v0.2-candidate_20260921T121059-0400.zip
- PD_Canonical_Baseline_v0.5-candidate_20260921T122509-0400.zip
- RESEARCH_CORPUS_phase1_spine.zip
- RESEARCH_CORPUS_CORE_v1.0.zip
- RESEARCH_CORPUS_HANDOFF_CAPSULES_v1.0.zip
- Jewish_Holiday_Booklet_Canonical_State_v0_4_ACCEPTED.zip
- Sukkos_PracticalCore_Archive.zip
- Sukkos_Ideal_Booklets.zip
- Sukkos_Booklet_Image_Generation_Packet.zip

Several Discoveries/Synthese ZIPs were discoverable by metadata but their raw bytes were not materializable through the current file boundary, so they are not used as substantive evidence here.

## Evidence family A — PD audit experiments

The pilot synthesis converged on a protocol-level distinction:

artifact adequacy != method efficacy != interaction efficacy != reduction adequacy

The original D0 included prior audit descriptions and conclusions. Therefore rediscovering those conclusions inside D0 does not demonstrate independent method discovery.

Observed consequences:
- self-referential benchmarks inflate apparent overlap and bias toward over-reduction;
- output equality can hide different reasoning histories;
- a finding does not identify its generating operation without controlled ablation/execution traces;
- different representations can yield different primitive decompositions;
- PD-only test cases risk overfitting.

The v0.2 repair separates:
- Track A: artifact adequacy
- Track B: method efficacy on holdouts
- Track C: interaction efficacy via ordered compositions
- Track D: reduction adequacy

The strongest warranted reduction statement is benchmark-relative, not global.

Every run is expected to preserve immutable native output, run identity, corpus hash, method-packet hash, run type, normalization record, and normalized-to-native links.

## Evidence family B — PD canonical baselines

The canonical baseline lineage strengthened governance over time.

Recovered invariants:
- working state and immutable release snapshots are distinct;
- latest is not accepted;
- machine state and human projection are synchronized but not interchangeable;
- superseded and resolved claims remain visible with reasons and reopen conditions;
- transition types are explicit;
- stable goal identity is distinct from wording/status;
- provenance is distinct from acceptance;
- priority dimensions do not imply an unjustified total order;
- convergence is relative to corpus, admissibility, representations, and evidence;
- material basis changes reopen the smallest implicated frontier.

The goal audit preserved OPEN global completeness even after finding no known material omission in the audited window.

## Evidence family C — research corpus handoff architecture

The corpus separates two research programs rather than merging them.

Recovered invariants:
- freeze the claim under examination; objections to A do not silently replace A with A-prime;
- exact logical strength matters;
- control status, epistemic status, provenance, originator, acceptance, evidence, conflict, novelty, and publication status are independent dimensions;
- filenames do not confer authority;
- atomic discoveries and synthesis objects are distinct;
- stable IDs are not reused;
- every substantive update records prior/new wording or status, reason/evidence, sources, and controlled-copy consequences;
- bidirectional traceability and OPEN-gap preservation are validation targets.

The handoff design uses a small orientation/capsule layer first and expands into deeper files only when needed.
This reduces context load without treating the compressed capsule as independent authority.

## Evidence family D — Jewish Holiday Booklet canonical state

The accepted v0.4 state uses three layers:
1. CANONICAL structured authoritative state
2. OBJECTS/sha256 immutable content-addressed originals/artifacts
3. VIEWS generated human-readable projections

Parallel work follows:
base release -> branch -> transaction -> validate -> conflict check/merge -> explicit acceptance -> next release

Recovered invariants:
- one primary structured home per substantive object;
- generated views are not canonical;
- latest and accepted pointers are separate;
- object/field conflicts block unsafe merge;
- acceptance is an explicit boundary;
- content-addressed evidence prevents rename/copy ambiguity;
- the work queue can retain many alternatives while selecting exactly one current step;
- state machinery remains subordinate to the direct user goal.

A discovered transaction bug was repaired because canonical/view mutation had left an old release manifest. The repaired lifecycle validates the base, branch, preconditions, regenerated views, new release, and release validation before PASS.

## Evidence family E — Sukkos practical/ideal archives

The PracticalCore readme explicitly rejects equating:
current = best = latest = canonical = most visually useful

Task-fit can differ from canonical authority.

Recovered invariants:
- exact recovered artifacts outrank regeneration when the task is artifact recovery;
- image-native sources can outrank PDF derivatives for image work;
- best-available can be used without falsely promoting it to canonical/accepted;
- strong unused alternatives remain preserved separately;
- complete internally coherent booklets outrank fragments for booklet-selection tasks;
- recovery is preferred to reinvention when lineage is available.

## Evidence family F — visual benchmark structure

The Yom Kippur benchmark and Sukkos visual references repeatedly use:
formal/scientific structure -> human meaning -> embodied application -> concrete next action

The same small stage spine is reused across contexts instead of inventing a new framework for each page.

Transferable lesson:
stable structure can support domain transfer when mappings are explicit and source roles remain distinguishable.

## Comparison against current ImproveCore

Current anchor already contains:
- basis-relative learning/no-gain memory;
- dependency-sensitive route reopening;
- authority/provenance/currentness safeguards;
- continuation-relative representation sufficiency;
- discovery/representation/candidate-universe reentry;
- basis-relative closure;
- addressable-corpus zero-request entry;
- external evidence admission controls.

Therefore those are not counted as new capabilities merely because the ZIPs also contain them.

The archives add stronger evidence for the following not-yet-explicit or incomplete coordinates:

1. EVIDENCE TARGET TYPING
Current self-study can distinguish evidence and basis, but no core runtime benchmark layer explicitly separates artifact adequacy, method efficacy, interaction efficacy, and reduction adequacy.

2. NATIVE OUTPUT PROVENANCE
Current runtime has typed in-memory receipts. Self-study 104 already found durable trace export partial/absent.
The ZIP evidence adds a concrete strict-gain requirement: preserve native outputs and link normalized receipts back to them with corpus/method hashes.

3. BENCHMARK-RELATIVE CLAIM STRENGTH
Basis-relative closure exists. The ZIPs strengthen the requirement that minimality/completeness/reduction claims carry the declared benchmark/admissibility/representation scope rather than being emitted unqualified.

4. AUTHORITY LATTICE EXTENSION
Current governance has authority/provenance/currentness. ZIPs show a recurring practical distinction among latest, accepted, canonical, recovered, candidate, and best-for-task.
This is likely a composition/extension of current governance rather than a new master layer.

5. TIERED HANDOFF CONTEXT
Current zero-request entry accepts an addressable corpus. The ZIP corpus demonstrates a compact-capsule-first loader as a potential efficiency gain, with deep expansion on demand and traceability back to canonical sources.

6. RECOVERY BEFORE REGENERATION
Current architecture values recovery. ZIP evidence gives a concrete acquisition preference: when exact prior artifacts/capabilities are available and fit the task, recover them before regeneration.

7. REPRESENTATION-SENSITIVE NONREDUCTION
Current representation sufficiency exists. ZIP evidence adds an experiment rule: output-only equivalence cannot by itself license tool/stage reduction; compare method, transition, information-flow, and provenance representations.

## Candidate growth directions

A. IC-EVIDENCE-TARGET-TYPING
Classification: STRICT_GAIN_CANDIDATE
Minimal form: typed evaluation matrix for artifact/method/interaction/reduction targets; holdout and negative-control support.
Risk: LOW_MEDIUM

B. IC-NATIVE-OUTPUT-TRACE-LINKAGE
Classification: COMPOSE_WITH_EXISTING_TRACE_EXPORT_CANDIDATE
Minimal form: immutable native stage output + hashes + normalization map referenced by durable trace schema.
Risk: LOW_MEDIUM

C. IC-BENCHMARK-SCOPED-CLAIMS
Classification: STRICT_GAIN_CANDIDATE / MATH-SPINE EXTENSION
Minimal form: reduction/minimality/completeness claims carry benchmark_id, basis_id, admissibility/representation scope, and reopen condition.
Risk: MEDIUM

D. IC-AUTHORITY-LATTICE-EXTENSION
Classification: COMPOSE_EXISTING_FIRST
Minimal form: independent status dimensions for latest/accepted/canonical/recovered/candidate/task-fit rather than a single current flag.
Risk: LOW_MEDIUM

E. IC-TIERED-HANDOFF-CONTEXT
Classification: EXPERIMENT_READY
Minimal form: orientation capsule -> targeted expansion -> source trace.
Risk: LOW

F. IC-RECOVERY-BEFORE-REGENERATION
Classification: COMPOSE_EXISTING_FIRST
Minimal form: acquisition preference plus exact-lineage witness; never self-authorizes acceptance.
Risk: LOW

G. IC-REPRESENTATION-ABLATION
Classification: EXPERIMENT_READY
Minimal form: before reducing a tool/stage, compare equivalent jobs across semantic, state-transition, information-flow, and provenance representations.
Risk: LOW_MEDIUM
