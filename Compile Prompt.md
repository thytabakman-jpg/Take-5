# Compile Prompt

## Objective

Reduce unnecessary independent files. Improve information organisation, coherence and accessibility. Preserve all unique information, research, provenance, structural relationships and functionality.

Do the following steps. The instructions tell you what to do. The tools help you do it. Do not substitute running a tool, reporting its results or making recommendations for doing the actual job.

Execute directly on the intended GitHub branch (main by default). Do not create a working branch or pull request unless the user explicitly requests one. Start each group as soon as you identify it, prepare its edits in memory or locally as needed, and commit each independently verified improvement directly to the intended branch during the same execution. Do not wait for other groups or leave completed work unpublished.

## 1. Identify pairs

Identify files that are ripe for consolidation. Decide which file to keep.

**Tools that help:**
- [Discovery (discover)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)
- [GOAL](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/goal.py)
- [Knowledge Web Explorer](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/build-graph.mjs)
- [Discriminator](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/discriminator.py)

## 2. Copy everything

Copy the entire contents of one file into the other. Do not change anything. If there are more than two files in the group, copy each additional file in full into the file you are keeping. Keep the original contents of the surviving file once. Check that everything was copied.

**Tools that help:**
- Available file-reading and file-editing tools.
- [Decompiler (consolidated text view)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)

## 3. Delete the original

Delete the file whose contents you just copied as part of the consolidation. Include the deletion, surviving content and necessary dependency repairs in the same direct commit once verified. Do not create another copy of the deleted file, a redirect placeholder, a working branch or a pull request.

**Tools that help:**
- Available file-deletion tools.

### Deal with the old links

Find and fix every inbound link pointing to the deleted file. Find the affected references for all files being deleted in the group together, then apply the changes. Preserve the original section destinations and fix transferred relative links only if moving them changes their destinations. Check indexes, registries, graphs and code that use the old files. Record unresolved references and keep working on everything that can be done independently.

**Tools that help:**
- [Dependency Repair (index, prepare and audit)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_dependencies.mjs)
- [Dependency Closure](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/dependency-closure.mjs)
- [Source Path Resolver](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/source-path-resolver.mjs)

## 4. Decompile

Decompose the surviving file's combined information into independently identifiable units. Separate compound units without changing meaning. Register each unit against its original source; use the frozen-source computational registry for preservation verification. Identify load-bearing terms, definitions, predicates, quantifiers, qualifications, premises, assumptions and logical relationships.

**Tools and resources:**
- [Decompiler (decompose)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)
- [PD Semantic Preflight Candidate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROMPT_SEMANTIC_PREFLIGHT_CANDIDATE.md)
- [MT Semantic Resolution](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/mt_semantic_return_gate.py)

## 5. Layer

Classify every unit by information type. Group units of the same type. Create additional layers where necessary. Assign understood material that fits no existing category to Other; keep unresolved classifications separate.

**Tools and resources:**
- [Layering (layerByUnit, working.layered)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)
- [Discriminator](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/discriminator.py)
- [Architecture](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/architecture_analysis.py)

## 6. Deduplicate

Compare units within and across layers. Distinguish equivalence, subsumption, partial overlap, contradiction and independence. Remove redundant information; retain every distinct proposition, qualification, argument, evidence item, relationship and attribution. Map each removed unit to its surviving representation. Similarity alone is not equivalence.

**Tools and resources:**
- [Comparison (exactGroups, similar, layerComparisons)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)
- [PD](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/pd.py)
- [PDAudit](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/pd_audit.py)
- [Discriminator](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/discriminator.py)

## 7. Synthesize

Combine complementary information into coherent representations. Reconcile compatible accounts, resolve contradictions when evidence permits, and distinguish conflicting positions and historical, superseded, current and exploratory findings. Preserve every distinct contribution.

**Tools and resources:**
- [Reconciler](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/reconcile.py)
- [ASSERT](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/assert_compound.py)
- [Currentness Audit](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/currentness_audit.py)

## 8. Architect

Reconstruct the surviving file around actual information responsibilities, ownership, relationships, section hierarchy and logical sequence. Remove responsibility overlap and improve readability without losing substantive content. Finalise file destinations and section anchors; justify any independently necessary file.

**Tools and resources:**
- [Architecture](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/architecture_analysis.py)
- [GOAL](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/goal.py)
- [Prose](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/prose.py)

## 9. Verify Dependencies

Audit the Step 3 changes against the frozen originals and final file/anchor mappings. Repair references affected by subsequent reorganisation, including induced downstream consequences. Independently inspect unsupported reference forms and native consumers; run applicable tests. Confirm necessary relationships, navigation and functions remain intact.

**Tools and resources:**
- [Dependency Repair (prepare and audit)](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_dependencies.mjs)
- [Dependency Closure](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/dependency-closure.mjs)
- [Architecture](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/architecture_analysis.py)
- [TRC](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/tool_run_closure.py)

## 10. Verify and Adjudicate

Compare the reconstructed state directly against the original state across every relevant dimension.

- **GO:** At least one meaningful dimension improves and none deteriorates. Accept the improvement.
- **TWEAK:** Repair a regression or missed gain and reassess.
- **NO-GO:** No meaningful gain or an unresolvable regression. Restore the better arrangement.
- **OPEN:** Obtain missing evidence and reassess; withhold only affected publication.

Verify unique current and historical information, attribution, provenance, logical integrity, structural relationships and functionality. Recover missing historical contributions at their rightful homes rather than retaining redundant files. Run the verifier with actual decomposition and independent dependency-audit receipts.

**Tools and resources:**
- [Compilation Verifier](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_verify.mjs)
- [RTC](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/raise_the_ceiling.py)
- [Diagnosis](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/diagnosis.py)
- [PDAudit](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/pd_audit.py)
- [PD Integrity Protocol](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROTOCOL.md)

## 11. Publish and Confirm

Immediately commit every independently verified GO change set directly to the intended GitHub branch (main by default), including physical deletions. Do not create a branch or pull request as a substitute for direct publication. If direct writes are prohibited, report the exact restriction and continue independent permitted work; do not silently switch to a branch or pull request. Guard against intervening revisions and preserve concurrent changes. Store the required provenance durably; do not create redirect placeholders instead of eliminating redundant files. Independently retrieve the published state and run publication verification. Confirm retired paths are absent, actual content matches and applicable downstream tests remain valid.

**Tools and resources:**
- [Publication Verifier](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_verify.mjs)
- [Currentness Audit](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/currentness_audit.py)
- [TRC](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/tool_run_closure.py)
 
## Execution Requirements

Freeze the authorised scope and Git revisions. Use [Compile Mathematics](https://github.com/thytabakman-jpg/Take-5/blob/main/Compile%20Mathematics.md) and its [execution contract](https://github.com/thytabakman-jpg/Take-5/blob/main/Compile%20Mathematics.md#execution-contract) for technical procedures and verification. Verify the three standalone executables and run the [Compile Test Suite](https://github.com/thytabakman-jpg/Take-5/blob/main/tests/test_compile.mjs) before relying on native operator results. Run required computational checks at their applicable stages; do not import Repair's mandatory tool battery or treat a tool result as a substitute for making the requested change. If a tool is unavailable, perform independently executable actions using available file operations and record the outstanding tool obligation. Do not publish changes whose required verification is incomplete.

### Stage admission and exit evidence

| Stage | Required actual exit evidence |
|---|---|
| 1 | Frozen source identities, authorized group, provisional survivor and dependency obligations |
| 2 | Actual working survivor containing every original source block, exact-transfer verification |
| 3 | Retired paths absent in the working map; prepared inbound and transferred-reference changes applied; OPEN mappings recorded |
| 4–6 | Original unit registry, classified actual working units and explicit reduction dispositions |
| 7–8 | Reconstructed working file, final owner and anchor maps, retained unique information |
| 9 | Fresh candidate-bound dependency audit and independent functional/scope evidence |
| 10 | Actual verifier result plus candidate-specific semantic GO adjudication |
| 11 | Guarded commit, re-fetched surviving content, absent retired paths and publication verification |

A stage may proceed only with its actual prerequisites; independent groups advance without waiting on unrelated obligations. A completed computational invocation is not a completed transformation.

Maintain the actual proposed contents and deletions for each group in memory or local files only as needed for verification. Do not substitute operator views for actual edits. Commit the verified group directly to the intended branch as soon as its own requirements are met. Never make a temporary GitHub branch, pull request, or staged candidate the deliverable of an execution request.

Complete and directly publish each independently verified group as its inputs become available. Do not accumulate completed groups awaiting a portfolio-wide publication step. Coordinate coupled edits. Apply each gate only to the operation it protects. Continue independent work while resolving affected publication requirements. Reuse frozen inputs and actual receipts; do not simulate tools or substitute discovery, reports or recommendations for execution. Follow authorised discovery-only or recommendations-only scope when requested. Recover failed operations and retain a compact continuation record. Stop only at verified completion or an evidenced execution limit/exhaustion of independent work; report exact remaining obligations.

Measure success by actual information improvements, preserved functionality and eliminated unnecessary files.

## Further Resources and Navigation

- [Compile Mathematics and execution contracts](https://github.com/thytabakman-jpg/Take-5/blob/main/Compile%20Mathematics.md)
- [Computational Test Suite](https://github.com/thytabakman-jpg/Take-5/blob/main/tests/test_compile.mjs)
- [Authoritative Take-5 Repository](https://github.com/thytabakman-jpg/Take-5)
- [Semantic Worker Contract](https://github.com/thytabakman-jpg/Take-5/blob/main/architecture/Semantic%20Worker%20Contract.md) (applicable host/operator principles)

### Additional technical resources

Use these resources for their actual functions. The registered Repair runtime is not a prerequisite for standalone Compile.

### Mathematical and semantic integrity

- [PD Semantic Preflight Candidate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROMPT_SEMANTIC_PREFLIGHT_CANDIDATE.md)
- [PD Audit and Integrity Protocol](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROTOCOL.md)
- [Mathematical Object Integrity Gate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Tool%20and%20System%20Research/ImprovementCore/tool-ecosystem/MATHEMATICAL_OBJECT_INTEGRITY_GATE_001_2026-10-06.yaml)
- [Mathematical Prerequisite Integrity Gate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Tool%20and%20System%20Research/ImprovementCore/tool-ecosystem/MATHEMATICAL_PREREQUISITE_INTEGRITY_GATE_001_2026-10-06.yaml)

### Dependency and repository operations

- [Research Sorter](https://github.com/thytabakman-jpg/Reaserch/blob/main/.github/skills/research-sorter/scripts/sort_research.py)
- [Knowledge Web Graph Builder](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/build-graph.mjs)
- [Dependency Closure](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/dependency-closure.mjs)
- [Source Path Resolver](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/source-path-resolver.mjs)
- [Canonical Authority Cross-Repository Link Validator](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Philosophy/Jewish%20Philosophy/tools-and-validation/tools/check_canonical_authority_cross_repo_links.py)
- [Canonical Authority Markdown Link Validator](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Philosophy/Jewish%20Philosophy/tools-and-validation/tools/check_canonical_authority_markdown_links.py)

### Tool execution and runtime recovery

- [Repair Prompt](https://github.com/thytabakman-jpg/Take-5/blob/main/Repair%20Prompt.md)
- [Tool Manifest](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/tool_manifest.py)
- [Tool Run Registry](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/tool_run_registry.py)
- [Tool Execution Guide](https://github.com/thytabakman-jpg/Take-5/blob/main/integration/Tool%20Execution%20Guide.md)
- [Tool Execution Architecture](https://github.com/thytabakman-jpg/Take-5/blob/main/architecture/Tool%20Execution%20Architecture.md)
- [Configured Invocation Gateway](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/direct_tool_command_gateway.py)
- [Runtime Bootstrap and Recovery](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md)
- [Source Transfer Helper](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/connector_source_transfer.py)
- [GitHub-only Connector Transfer](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md#github-only-connector-to-local-transfer)
- [Read-Only Analysis Bindings](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md#read-only-document-analysis-bindings)
- [Runtime Source Cache](https://api.github.com/repos/thytabakman-jpg/Take-5/actions/artifacts/15104764333/zip)
- [Runtime Artifact Discovery](https://api.github.com/repos/thytabakman-jpg/Take-5/actions/runs?branch=chatgpt-runtime-bootstrap&status=success)

**Execute, verify and publish.**
