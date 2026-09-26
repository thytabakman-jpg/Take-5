# ImprovementCore MT Persistence Evidence Run

Date: 2026-09-26
Controller: ImprovementCore / IC-028
Regime: 091
Default local recurrence: HF2
Mode: OBSERVE_DECOUPLED
Input role: EVIDENCE_NOT_DIRECTIVE
Mutation: none

## Evidence presented

Treat the following proposition only as evidence. Do not assume it is true, do not optimize toward confirming it, and do not treat it as a requested architecture:

One key reason for MT to exist may be to create a durable artifact for everything material it discovers or reconstructs, so that the result is not lost to chat-history compression, and that durable capture may need to be interconnected with the rest of the system.

The controller owns the interpretation, decomposition, acceptance, rejection, and next-work choice.

## Current repository evidence inspected

### MT recovered semantics

The current configured MT surfaces are primarily transformation, recovery, relation-discovery, 36-cell scope/mode coverage, DCC/TRC, HF1/HF2, and black-box decomposition.

Relevant surface:
- research/MT_FULL_WRAPPED_SEMANTIC_LIFECYCLE_068_2026-09-25.md

The recovered MT definition does not currently make "create a persistent interconnected artifact for every material result" a native defining clause.

### ImprovementCore anti-loss semantics

Current ImprovementCore has a validated durable material-knowledge ledger:

- runtime/improvement_core_knowledge_ledger.py
- integration/IMPROVEMENT_CORE_KNOWLEDGE_LEDGER_113.json
- architecture/IMPROVEMENT_CORE_MATERIAL_KNOWLEDGE_CAPTURE_113.md

Its knowledge nodes include:
- identity;
- kind;
- statement;
- basis;
- disposition;
- related objects;
- dependency footprint;
- evidence references;
- provenance;
- metadata.

This is already an interconnected durable graph rather than merely an unlinked file dump.

The repository-governed anti-loss law is basis-relative:

material governed knowledge event -> durable knowledge capture.

Universal record-everything outside supplied/governed inputs remains outside repository authority.

### Configured-tool persistence boundary

The configured-tool bridge:

- runtime/improvement_core_tool_bridge.py

places configured tool results into transient controller state under `configured_tool_outputs`.

The ImprovementCore regime:

- runtime/improvement_core_regime.py

automatically sends to the durable knowledge ledger:
1. explicit `knowledge_events` present in stage state; and
2. admitted recursive material traces.

The generic configured-tool bridge itself does not establish that every material configured-tool output is converted into a durable knowledge event.

Therefore a distinct persistence-coverage seam exists:

material configured tool output
-> configured_tool_outputs
-?> durable interconnected knowledge node.

That seam applies to MT unless another handler or adapter emits the corresponding knowledge event.

## ImprovementCore observer recurrence

### Round 0

Observation:

The proposed evidence contains two separable claims:

A. anti-loss persistence is a key system purpose around MT;
B. artifact creation is a native defining responsibility of MT itself.

Disposition:

Do not conflate them.

Material change:

ROLE_DECOMPOSITION_REQUIRED.

HF2:

REAPPLY.

### Round 1

Observation:

Claim A has strong current-system support.

The system already treats durable capture, provenance, dependency linkage, recoverability, and anti-regression as load-bearing.

Claim B is not established by current MT semantics.

Persistence currently belongs primarily to the governed ImprovementCore persistence/knowledge layer rather than to MT's native transformation semantics.

Material change:

ANTI_LOSS_GOAL_SUPPORTED__MT_NATIVE_OWNERSHIP_UNRESOLVED.

HF2:

REAPPLY.

### Round 2

Observation:

The configured-tool bridge reveals a real system gap that is narrower and more concrete than the original wording.

A material MT result can be implementation-executed and stored in `configured_tool_outputs` without the bridge itself proving durable interconnected knowledge capture.

This means the important invariant is not "one standalone file per thing."

The important invariant is closer to:

Every material MT yield that crosses the governed execution path must have a durable recoverable representation plus explicit graph links to its basis, provenance, dependencies, evidence, affected objects, and disposition before the episode can claim persistence closure.

A standalone Markdown/JSON run artifact can be one representation of that record, but durable knowledge-node capture can satisfy the anti-loss role without multiplying files for every atomic fact.

Material change:

MT_MATERIAL_OUTPUT_TO_DURABLE_KNOWLEDGE_SEAM_IDENTIFIED.

HF2:

RELATIVE_CLOSE for the evidence-evaluation job.

## Independent disposition

The evidence is materially important.

It does not establish that persistent artifact creation is presently one of MT's native defining functions.

It does establish that preserving MT's material output outside chat history is a load-bearing system requirement.

Current architecture already contains much of the correct destination structure in ImprovementCore's durable knowledge ledger.

The unresolved system question is ownership and coverage at the configured-tool boundary:

Does every material MT/configured-tool yield necessarily produce durable interconnected knowledge before closure?

Current generic bridge evidence does not prove that invariant.

## Selected live question

MT_PERSISTENCE_COVERAGE:

For every material configured MT execution result m,

MaterialMT(m)
=>
DurableCapture(m)
AND
Linked(m, basis, provenance, dependencies, evidence, affected_objects, disposition)

before persistence/verification closure.

Status:

OPEN / NOT YET PROVED BY THE GENERIC CONFIGURED-TOOL PATH.

## Non-conclusions

This run does not conclude:
- that every atomic datum needs its own standalone file;
- that MT must own persistence internally;
- that existing ImprovementCore knowledge persistence is absent;
- that all chat history can be captured by repository code;
- that the proposed evidence is true merely because it was supplied.

## Related system objects

- MT
- ImprovementCore / IC-028
- HF2
- configured-tool bridge
- knowledge ledger
- artifact-to-work intake
- provenance/currentness
- persistence closure
- chat-history compression/regression problem

## Final observer disposition

Evidence treatment: EVIDENCE_NOT_DIRECTIVE
ImprovementCore result: MATERIAL_DISTINCTION_FOUND
Recovered anti-loss objective: SUPPORTED
MT-native artifact-role claim: NOT ESTABLISHED
Configured-tool-to-durable-knowledge coverage: OPEN
Repository mutation: NONE
Architecture admission: NONE
