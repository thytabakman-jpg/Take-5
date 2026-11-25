# ChatGPT runtime bootstrap

This is an isolated integration branch, not a change to Take-5's governing main branch or to ICC-System. It packages the authoritative **main** commit for a read-only, ephemeral ChatGPT Python execution environment. No extra plugin, API key, model subscription, machine, scheduled job or external paid runner is required for packaging.

## Reusable retrieval route

1. Read the current main commit via GitHub's refs API and remember the full SHA.
2. Find the latest successful **ChatGPT runtime bootstrap** workflow run on this branch. Download its `take5-chatgpt-runtime` Actions artifact through the GitHub connector (download_workflow_artifact). That operation materializes the file in the conversation's Python working container without a user upload.
3. If the packaged commit is stale or the artifact expired, create or update `chatgpt-runtime-request.txt` on this branch with a unique request value, and obtain the new successful run and artifact. The existing workflow starts on that path's push. Do not alter main or a research repository to refresh the runtime. Reuse the existing artifact if current.
4. Unpack the bootstrap scripts, then run `python bootstrap.py <artifact.zip> --expected-commit <main SHA> --destination <fresh directory> --receipt <receipt.json>`. The loader checks every archived Git blob against the workflow tree manifest, checks the archive checksum and exact independently fetched main SHA, rejects missing or unsafe paths, runs native regression tests and the original 95-identity configured routing audit, and writes a machine-readable receipt. A failed loader or missing dependency is OPEN/BLOCKED, not success. Source and test scripts are separate from host integration scripts.
5. Invoke the authoritative gateway from the recovered runtime. For explicitly specified finite PD/PDAudit or syntactic Prose cases use `python run_packet.py --runtime <verified runtime path> --packet <packet.json> --receipt <run.json>`. Optional trusted local adapter modules must export `bind_adapters(packet)`, mapping exact native tool IDs to callable `(state, plan)` adapters. Supply all semantic inputs and validate their provenance. Missing adapters remain OPEN. The packet runner neither edits the documents nor performs independent semantic adjudication.

## Evidence and execution boundaries

- BOOTSTRAP_VERIFIED certifies source loading and regression tests, not the correctness of a substantive document analysis. The portfolio audit tests routing with synthetic witnesses. Native registry availability is not semantic completeness.
- Each tool retains its original requirements. PD needs an admitted case frame, result mapping/equivalence and coordinate representations; PDAudit requires audit controls. The finite packet binding is equality-based, not unrestricted semantic PD. Prose performs its explicit native checks but remains OPEN without separately evidenced semantic preservation, earned claim strength and no unsupported inflation. No fabricated PASS evidence.
- MT, GOAL, Architecture, MultiObject, ImprovementCore, and other provider-dependent tools need task-specific semantic workers/adapters. See the runtime's WORKER_ADAPTER_CONTRACT.md and portable_tool_conductor.py. A separate independent evaluator has not been established by this bootstrap. Do not label host prose as a native run. A native core run with an explicit limited input does not certify all configured semantic layers.
- The packet runner binds the original direct command gateway, retains the HF2 result and reports each requested tool separately. It is a read-only host integration, not an alternate ImprovementCore controller. No automatic repair or document write is authorized by any execution receipt alone.
- Artifacts expire after their retention period; refresh only on demand. Take-5 is public; standard GitHub-hosted Actions are free for public repositories. This workflow uses the standard Ubuntu runner, has a five-minute timeout and no schedule or external paid services. Never add research data or credentials to this public branch or artifact.
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

Expect PD and PDAudit to return bounded native results, Prose to preserve OPEN for missing semantic evidence, and MT to remain OPEN without its adapter. No document changes follow. The execution receipts must identify the frozen packet and current source revision.
