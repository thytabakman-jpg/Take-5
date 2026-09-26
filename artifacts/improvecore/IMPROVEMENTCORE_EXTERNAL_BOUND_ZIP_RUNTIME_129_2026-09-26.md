# ImprovementCore — Finish Every Actionable ZIP Job 129

Date: 2026-09-26
Controller: ImprovementCore / IC-028
Regime: 091
Instruction: finish every currently actionable job on the two-ZIP problem; do not stop at description
Starting main: 895bbd2eb6bc1a8b2a70ac01ab1491662f29e967
Resulting merge: c67ca2999039ee6e25578f92732887a08c4326dd

## Evidence re-executed

The two exact previously bound GitHub Actions artifacts remained available in the active host runtime.

Artifact 10901131588
- workflow run 36226293888
- branch improvecore/chat-export-github-105
- byte count 1547
- SHA-256 7dca0a234c5cd2c5ef0eb894f4582162231fe3901aa806b7b2f933059b28d3ba
- declared members 3
- all 3 text-routable
- unresolved members 0

Artifact 10899752487
- workflow run 36223410136
- branch improvecore/chat-history-4mo-2026-09-26
- byte count 1548
- SHA-256 66afbc7d3a694b3711239b8281f65d8770504686de100df0af089910987954a7
- declared members 3
- all 3 text-routable
- unresolved members 0

Shared member hashes
- closed_loop_receipt.json: 9886ab40f59f8c9b6b420beb2cff2e33aaf3858e4558de1f4a565ef6bd2d720f
- state/example-zero/result.json: b8068f446df68dd7a1a0e7d342551f40fa4b6aa79cb831792d0bebbdd450a196

The events.jsonl members differ only in event timestamp/hash.

## ImprovementCore frontier

Already closed before this pass
- exact ZIP byte/hash binding primitive
- in-memory ZIP traversal
- member accounting
- ArtifactRecord creation
- binary/unreadable preservation
- recovery visibility of archive_artifact_intake

New actionable residual

The normal ImprovementCore regime acquired external outputs and merged them as generic evidence, but did not execute the new bound-ZIP adapter or artifact_intake automatically before controller stages.

Therefore:

documented capability != normal-path activation.

## Repair executed

PR #126 implemented the missing transition inside runtime/improvement_core_external_acquisition.py.

Typed host output contract:

artifact_kind = BOUND_ZIP
artifact_ref = immutable GitHub artifact reference
archive_bytes = exact bytes
artifact_generators = optional semantic generators
require_semantic_extraction = optional fail-closed semantic requirement

Normal path now performs:

external acquisition
-> exact bound-ZIP verification
-> archive expansion/member accounting
-> ArtifactRecord creation
-> artifact_intake traversal/generator execution
-> WorkItem generation
-> obligations
-> ImprovementCore manager stages.

Raw archive bytes, unsanitized refs, and generator callables are removed before persistent controller evidence is formed.

Any binding/intake OPEN/BLOCKED/CONFLICT condition makes the external acquisition OPEN_GAP so ImprovementCore cannot close over failed outside evidence.

## Regression

Added tests prove:
- successful bound ZIP crosses archive and artifact intake before manager stages;
- material candidate work reaches obligations;
- raw bytes/generators/ref do not survive into external_evidence;
- hash mismatch becomes EXTERNAL_ACQUISITION_GAP.

Validation
- Take-5 Validation 36277387131: SUCCESS
- Capability Preservation 36277387413: SUCCESS

Merge
c67ca2999039ee6e25578f92732887a08c4326dd

## Initial-pass disposition

Repository-owned normal-path external ZIP activation:
CLOSED_RELATIVE.

Exact identity of any still-unbound substantive external archive:
OPEN_WITH_REENTRY / external evidence requirement.

The successor state is now handed to HF2 with the same instruction:
finish every currently actionable job.
