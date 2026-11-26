# ChatGPT runtime bootstrap

This isolated integration branch packages the authoritative Take-5 **main** commit for a read-only, ephemeral ChatGPT Python execution environment. Use the GitHub connector and existing packaging workflow; no additional API key, model subscription, machine, scheduled job or paid runner is required. The branch does not alter governing main or ICC-System.

## Retrieve, verify and execute

1. Read the current main commit via GitHub's refs API and remember the full SHA.
2. Find the latest successful **ChatGPT runtime bootstrap** workflow run on this branch. Download its `take5-chatgpt-runtime` Actions artifact through the GitHub connector (download_workflow_artifact). That operation materializes the file in the conversation's Python working container without a user upload.
3. If the packaged commit is stale or the artifact expired, create or update `chatgpt-runtime-request.txt` on this branch with a unique request value, and obtain the new successful run and artifact. The existing workflow starts on that path's push. Do not alter main or a research repository to refresh the runtime. Reuse the existing artifact if current.
4. Unpack the [bootstrap scripts](bootstrap.py), then run `python bootstrap.py <artifact.zip> --expected-commit <main SHA> --destination <fresh directory> --receipt <receipt.json>`. The loader hashes the raw commit object against the independently fetched main SHA, reconstructs its root Git tree from the workflow manifest, verifies every archived blob against that tree, checks the archive checksum, rejects missing or unsafe paths, runs native regression tests and the current configured routing audit, and writes a machine-readable receipt. Artifacts predating the commit-object verification require refresh. A failed loader or missing dependency is OPEN/BLOCKED, not success. Source and test scripts are separate from host integration scripts.
5. Prepare the admitted packet using the schemas below and the host workflow. Invoke the authoritative gateway from the recovered runtime with [run_packet.py](run_packet.py). For explicitly specified finite PD/PDAudit or syntactic Prose cases use `python run_packet.py --runtime <verified runtime path> --bootstrap-receipt <receipt.json> --packet <packet.json> --receipt <run.json>`. The runner verifies the bootstrap receipt, commit/tree binding and tracked runtime bytes before loading tools. The receipt is not a substitute for independently selecting the current main commit. Optional trusted local adapter modules must export `bind_adapters(packet)`, mapping exact native tool IDs to callable `(state, plan)` adapters. External providers may not silently override requested built-in bindings: pass `--allow-adapter-override TOOL` explicitly for each intended replacement. The runner records provider initialization failures and per-tool binding dispositions; unrelated built-in tools retain independent execution receipts.

## Evidence, execution and security boundaries

- BOOTSTRAP_VERIFIED certifies source loading and regression tests, not the correctness of a substantive document analysis. The portfolio audit tests routing with synthetic witnesses. Native registry availability is not semantic completeness.
- Each tool retains its original requirements. PD needs an admitted case frame, result mapping/equivalence and coordinate representations; PDAudit requires audit controls. The finite packet binding is equality-based, not unrestricted semantic PD. Prose performs its explicit native checks but remains OPEN without separately evidenced semantic preservation, earned claim strength and no unsupported inflation. No fabricated PASS evidence.
- MT, GOAL, Architecture, MultiObject, ImprovementCore and other provider-dependent tools need task-appropriate adapters and admitted inputs under the [worker contract](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/WORKER_ADAPTER_CONTRACT.md). The [ToolConductor](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/portable_tool_conductor.py) distinguishes available and unresolved bindings. Missing adapters remain OPEN; binding alone is not semantic input readiness. This bootstrap supplies neither independently authenticated semantic reasoning nor general source authentication. A bounded result does not certify all 36 cells, 792 question projections or 144 cognitive projections. Host prose is not a native run.
- The packet runner follows the [current invocation guide](https://github.com/thytabakman-jpg/Take-5/blob/main/integration/CURRENT_FULL_TOOL_INVOCATION.md), binds the original gateway, retains the HF2 result and reports each requested tool separately. It is a read-only integration, not an alternate controller or independent semantic adjudicator. An execution receipt alone authorizes neither repair nor document writes; independently verify authorized changes and preserve unresolved gates before writing research data back.
- Artifacts expire; refresh only on demand using the [packaging workflow](../.github/workflows/chatgpt-runtime-bootstrap.yml), which owns runner, timeout, trigger and retention configuration. The public branch and artifacts contain reusable code only. Never add private research data, packets, receipts or credentials; keep them in the conversation's working environment.
- The standard Python sandbox may use versions different from pinned development requirements; the receipt records observed versions. If a test or dependency fails, stop and report the failure. Do not silently install paid services.

## Packet shape (finite, explicitly labelled example)

```json
{
  "command": "run PD; run PDAudit; run Prose; run MT",
  "pd_frame": {
    "cases": [
      {"id":"a","result":false,"coordinates":{"x":false,"y":false}},
      {"id":"b","result":false,"coordinates":{"x":true,"y":false}},
      {"id":"c","result":false,"coordinates":{"x":false,"y":true}},
      {"id":"d","result":true,"coordinates":{"x":true,"y":true}}
    ],
    "representations":{"truth-frame":["x","y"]}
  },
  "prose":{"text":"The example contains a claim.","contract":{"contract_id":"example","constraints":["AFFIRMATIVE_FIRST"]}}
}
```

Expect PD and PDAudit to return bounded native results, Prose to preserve OPEN for missing semantic evidence, and MT to remain OPEN without its adapter. The execution receipts identify the frozen packet and current source revision.


## Read-only document-analysis bindings

[document_adapters.py](document_adapters.py) provides host bindings for explicitly admitted classification matrices, finite integer-threshold comparisons, and structured Diagnosis/RTC evidence. It is packaged with the runtime on demand. Run the existing packet runner with `--adapter-module <bootstrap-directory>/document_adapters.py`. PD, PDAudit and Prose continue to use the packet runner's native bindings.

Admission is per registered tool. A combined packet may supply multiple input groups.

| Registered tool ID(s) | Required evidence groups |
| --- | --- |
| GDOS, BiasPerturbation, MultiObject | Matrix and source references; only fields used by the selected algorithm |
| Architecture | Matrix or explicit architecture graph, plus source references |
| Discriminator, Reconciler | Threshold model and source references; only fields used by the selected algorithm |
| Diagnosis, RTC | Threshold model or their respective structured document evidence, plus source references |
| MT, GOAL | Both matrix and threshold model, plus source references |
| ASSERT | Matrix and threshold model, or exact quotation claims, plus source references |
| CurrentnessAudit, TRC | Source references and applicable currentness or open-obligation coordinates |

A missing required group or field produces an OPEN receipt; malformed admitted input produces BLOCKED. Neither disposition claims a native invocation. Unused groups are not validated, so an unrelated missing or malformed group cannot block an independent tool.

Complete packet field definitions:
- `sources`: path, authenticated connector blob SHA (`sha`) and a subsequent independently fetched `latest_sha` for every source;
- `expected_ids`: authoritative inventory;
- `matrix`: `axes`, `raw` (one whitespace-separated case identifier and one slash-separated label field per axis per line), `transfer_fnv` (eight-digit FNV-1a over Unicode code points), `declared_counts`, `exclusive_axis`;
- `threshold`: nonempty unique source-supported integer `values`, inclusive integer `lower` and `upper` with lower ≤ upper, distinct integer `baseline_probes` within those bounds, nonnegative integer `declared_pair_count`, exact `proof`, `proof_fnv`;
- `open_coordinates`: unresolved source/semantic obligations; and optional `goal_candidates` (id, goal X/T/I/Sigma, constraints, evidence, grounded, authority_typed, determinate_enough).

GOAL's MT preflight is recovered from an actual gateway invocation. MT runs a limited observation over the packet; unresolved semantic-stage bindings remain OPEN. MultiObject runs an independent algorithmic full-joint membership route before pair routes, then tests exact pair recoverability. It does not infer scholarly relationships from shared tags. ASSERT is the bounded compound core, not full-36 ASSERT certification. In the threshold route RTC tests additional probes in the fixed finite model; the structured route evaluates host-supplied candidates. Currentness verifies revision identity, not source truth. Prose requires separately evidenced semantic preservation, reader load and claim strength.

### Explicit Architecture graph input

For Architecture alone, `architecture_graph` is an alternative to `matrix`; supplying both is BLOCKED. It contains a nonempty list of unique text `expected_units` and a `units` list. Each unit has a unique nonempty `id`, `source` path and exact Git blob `sha` matching a declared source, nonempty `role` and `locator`, and `internal_dependencies` (a list of unique text unit IDs). Optional `external_dependencies` and `information_ownership` are lists of declared text identities. Source paths must be unique. Missing required fields remain OPEN; malformed fields are BLOCKED before the native entrypoint. Other tool bindings ignore this group.

The native Architecture core reports missing or unexpected units, dangling internal dependencies, reverse internal consumers, declared roles and ownership, and source provenance. The host supplies and authenticates the graph facts; the adapter does not independently derive relationships or certify source truth, semantic ownership, external consumers or dynamic dependencies. The result intentionally retains OPEN for these unverified obligations, including on a structurally clean graph.

### Exact quotation ASSERT input

For ASSERT, `assert_quotes` provides an alternative to the matrix and threshold model; supplying either finite-model group alongside it is BLOCKED. It contains a nonempty `claims` list of unique nonempty text `id`, `source` path and nonblank exact `quote`. Sources use the existing list, with unique paths and valid Git blob SHA; additionally supply exact UTF-8 `text`, independently refetched `refetched_text`, and `latest_sha` for each available source. Do not normalize whitespace, Unicode or line endings. SHA-1 and SHA-256 Git blob identity are supported.

The seven-stage native compound ASSERT checks exact substring presence against the frozen text and then the refetched bytes. TRUE and FALSE report correspondence; unavailable evidence or an invalid frozen text/hash match is UNKNOWN, and a changed revision or inconsistent refetched text/hash match is CONFLICT. Malformed inputs are BLOCKED; false or unresolved claims prevent closure. The adapter verifies supplied bytes against supplied hashes but cannot authenticate the host's fetches, establish independent model evaluation, test paraphrases or infer semantic support for a claim.

### Structured Diagnosis and RTC input

These bindings also accept an explicit evidence inventory instead of a threshold model; a matrix is not required. Use top-level `diagnosis` with `failures`, or `rtc` with `candidates`. Each object includes nonempty `inventory_evidence`; a deliberately empty inventory is allowed only with that evidence. Each row has a unique nonempty string `id` and nonempty `evidence`. Every evidence list consists of objects with `source_path`, `source_sha`, `locator` and `basis`. The path and exact lowercase Git blob SHA (40 or 64 hexadecimal digits) must match an entry in `sources`. Locators identify the relevant passages; basis explains the observation or inference. Source authentication and semantic interpretation remain the host's responsibility.

- Diagnosis rows contain an optional Boolean `material` and an optional textual `mechanism`. Null or absent mechanism remains unresolved; a non-null mechanism requires `mechanism_evidence`.
- RTC rows contain `strict_gain` and `preserves`, each Boolean or null (absent is unresolved). For each explicit Boolean, supply the corresponding `gain_evidence` or `preservation_evidence`.
- Do not include a threshold model in a packet invoking a structured route for the same tool: ambiguity is BLOCKED. Missing evidence stays OPEN. A mixed RTC result retains both admitted candidates and unresolved candidates, and its adapter disposition remains OPEN.
- The provider validates the declared evidence references and input types, then invokes the original native tools. It does not independently authenticate the references, establish the proposed mechanism, prove gain/preservation or authorize edits. The receipt is bounded to the supplied inventory. Other tools retain their original input requirements.

### Host workflow for document requests

1. Establish the exact requested tool IDs, then retrieve and verify the current runtime using the procedure above.
2. Read the actual target through its authenticated connector; freeze exact source and version references.
3. As semantic host, derive the admitted case frame, source excerpts, candidate objects, question and protected constraints. Record how inputs were derived, what is modelled, what remains unverified and why each coordinate belongs to the tool's actual job. Transfer only the required packet to the Python sandbox and check it against the connector extraction. Do not reuse old scores as source evidence.
4. Select the applicable schema and adapter above. For arbitrary prose PD/PDAudit, explicitly construct a finite admitted frame; for Prose, supply its explicit contract and evidence. Other task-specific tools require their own actual provider, or remain OPEN. Retain full native receipts.
5. Independently recompute deterministic claims using a different algorithm where available. Separate same-model semantic judgement from genuine independent evaluation and preserve the execution and authorization boundaries above.
