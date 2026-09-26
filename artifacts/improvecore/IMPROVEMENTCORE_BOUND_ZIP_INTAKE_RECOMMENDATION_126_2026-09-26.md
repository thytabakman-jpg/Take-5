# ImprovementCore Recommendation — Bound ZIP Intake 126

Date: 2026-09-26
Controller: ImprovementCore / IC-028
Regime: 091
Mode: OBSERVE_DECOUPLED recommendation pass
Input role: all current two-ZIP evidence plus current Take-5 runtime
HF2: deferred until implementation successor exists

## Evidence admitted

- GOAL_TWO_GITHUB_ZIPS_HF2_RUN_123_2026-09-26.md
- IMPROVEMENTCORE_TWO_GITHUB_ZIPS_OBSERVER_HF2_124_2026-09-26.md
- IMPROVEMENTCORE_TWO_GITHUB_ZIPS_AUTONOMOUS_HF2_125_2026-09-26.md
- TWO_ZIP_LOGIC_ASSERT_GOAL_HF2_PROBLEM_IC_RUN_2026-09-26_1723ET.md
- current Artifact-to-Work Intake Contract
- current artifact_intake.py
- current external-acquisition policy
- configured-tool durable-knowledge repair
- current ImprovementCore / HF2 / full-invocation recovery anchors

## Reconstructed current state

The earlier identity-only diagnosis is no longer the whole problem.

Host-side work has now demonstrated that GitHub Actions ZIP objects can be positively bound,
downloaded, hashed, inventoried, and traversed.

However the repository-owned intake path still begins with:

ArtifactRecord(artifact_id, content: str, provenance)

There is no repository-owned transition from exact ZIP bytes plus immutable GitHub object identity
into per-member ArtifactRecord objects and complete member-accounting receipts.

Therefore the documented route:

exact GitHub ZIP
-> no-skip member traversal
-> artifact_intake
-> Work/currentness
-> ImprovementCore

contains an implementation gap before artifact_intake.

## Candidate frontier

A. Add another archive controller.
Reject: duplicates ImprovementCore ownership.

B. Treat host-side Markdown receipts as sufficient forever.
Reject: preserves evidence but does not make the promised intake path executable or reusable.

C. Extend ArtifactRecord itself to accept arbitrary binary payloads.
Reject for now: broad type expansion is unnecessary for the demonstrated ZIP-to-text-corpus case.

D. Add a narrow bound-ZIP adapter in front of existing artifact_intake.
Select.

## Selected repair

Introduce a small adapter that accepts:

GitHubArtifactRef
=
<repository,
 object_class,
 stable_id,
 source_ref,
 observed_name,
 expected_byte_count,
 expected_sha256,
 observed_at>

plus exact ZIP bytes.

The adapter must:

1. fail closed when byte count or SHA-256 differs from the bound GitHub object;
2. parse the ZIP in memory without filesystem extraction;
3. produce one receipt for every declared member, including directories, duplicate names,
   encrypted/unreadable entries, text entries, and binary entries;
4. preserve member index so duplicate filenames remain distinct;
5. enforce member-count and total-uncompressed-byte limits;
6. route UTF-8/UTF-8-SIG text members into the existing ArtifactRecord pipeline with immutable
   source provenance;
7. retain binary/unreadable members as typed unresolved extraction rather than silently dropping them;
8. make traversal completeness distinct from semantic completeness.

## Strict-gain basis

Before repair:
exact ZIP bytes cannot enter the repository-owned artifact-intake path without an external,
unmodeled preprocessing step.

After repair:
an exact bound ZIP can be deterministically transformed into accounted member receipts and existing
ArtifactRecord objects with provenance, without adding a peer controller.

This is a strict capability gain and directly closes a claimed but non-executable edge.

## Remaining OPEN

- which two external ZIP objects are the user's intended substantive pair;
- semantic parsing of arbitrary binary archive members;
- host acquisition itself;
- universal ChatGPT-host interception.

## Recommendation

IMPLEMENT_BOUND_ZIP_TO_ARTIFACT_INTAKE_ADAPTER.

ImprovementCore recommendation status:
CLOSED_RELATIVE.
