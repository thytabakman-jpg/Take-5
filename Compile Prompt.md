# Compile

## 1. Binding execution contract

Reduce redundant files and information while preserving distinct substantive research, evidence, provenance, required functionality and dependencies. Compilation means actual elimination of approved redundant files, not creation of compatibility placeholders. The prompt owns the methodology; three independent operators perform bounded mathematical work.

Execute the applicable stages exactly in their dependency order. Retrieve the current authoritative mathematical specification and executable tools, execute them on the actual frozen target, retain their real outputs and use them to complete the authorized work. Do not substitute a plan, source retrieval, manually approximated tool, synthetic example, similarity score or plausible result for target-specific execution. Do not bypass a required verification gate, manufacture receipts or certify incomplete work. The host performs semantic judgments and publication; the three operators do not authorize or perform durable writes.

Do not invoke the Repair battery or bootstrap the general Take-5 runtime merely to compile. Optional resources are not additional mandatory tool runs. If the user separately authorizes a registered Take-5 tool, follow its own governing invocation contracts; never confuse a standalone Compile operator or bounded diagnostic with full configured execution.

## 2. Execution sequence

| Stage | Operation | Required predecessor | Exit evidence |
| --- | --- | --- | --- |
| C-S01 | Scope and freeze | User authorization | Frozen scope, revisions, authority and intended output |
| C-S02 | Retrieve and verify operators | C-S01 | Exact source identities, execution route and fixture result |
| C-S03 | Discover and select survivors | C-S01 | Candidate groups, justified dispositions, historical basis |
| C-S04 | Consolidate and decompile | C-S02, C-S03 | Actual target decomposition and source coverage |
| C-S05 | Layer and map | C-S04 | Information layers, ownership, file/anchor map |
| C-S06 | Prepare dependencies | C-S02, C-S05 | Actual preparation output and resolved affected mappings |
| C-S07 | Deduplicate, synthesize, reconstruct | C-S04–C-S06 | Candidate content and preservation dispositions |
| C-S08 | Repair and audit | C-S06–C-S07 | Candidate-bound dependency audit and functional evidence |
| C-S09 | Verify candidate | C-S04, C-S07–C-S08 | Actual verifier receipt and admissible candidate |
| C-S10 | Publish | C-S09 plus current authority/revisions | Guarded commit(s) or evidenced no-write disposition |
| C-S11 | Verify publication | C-S10 | Independently retrieved state, verified elimination and closure |
| C-S12 | Record and continue | Recorded stage dispositions | Recoverable checkpoint or explicit terminal status |

Independent work may proceed only when its own prerequisites hold. Reapply affected stages when a frozen input, mapping or relevant dependency changes. At every failure, apply C-S12; a blocker is not successful exit evidence. For a discovery-only request, end after C-S03 with a justified candidate inventory, performing C-S04 only if needed for comparison; no deletion or publication is authorized. For recommendations-only compilation, complete the applicable candidate analysis and verification without publication; identify unexecuted write stages as not authorized, not passed.

## 3. Scope, authorization and target freeze (C-S01)

Verify repository identities, branches, commit SHAs and authorized targets. Distinguish candidate discovery from permission to delete. Inventory all potentially affected repositories, files, references, history and functional entry points. Record binary/unavailable/unsupported content and scope gaps. Recommendations-only requests do not write. Never modify unrelated files. Freeze the exact source and dependency snapshot and record authorization for each proposed retired file and each affected write.

Resolve the goal, target, referents, requested operation, selectors, protected constraints, authority and success condition before acting. Distinguish candidate discovery, recommendations and execution. An explicit request to compile identified files authorizes validated consolidation and necessary, verified reference-only collateral edits within the established repository scope; it does not authorize unrelated improvements, uncertain retirements, or writes to additional repositories. Record the basis for each retirement and edit; obtain further authority only where genuinely absent. A folder is not blanket permission to delete every file. Preserve material ambiguity as OPEN and proceed with independent authorized work. Use the preflight principles in [C14](#c14) as design guidance, not as a promoted mandatory PD run.

## 4. Standalone retrieval, verification and recovery (C-S02)

Retrieve [C01](#c01)–[C05](#c05) from the [authoritative Take-5 repository](https://github.com/thytabakman-jpg/Take-5) at one independently resolved current revision; record paths and Git blob identities. Read the mathematics and inspect the exact tool input/output contracts. Cache verified bytes and successful fixture evidence for the same revision and execution environment. Do not retrieve unrelated Take-5 files.

Prefer Node.js 18+ with no third-party packages. Preserve the relative `runtime/` and `tests/` paths. Run:

```sh
node tests/test_compile.mjs
node runtime/compile_decompiler.mjs < decompile-input.json > decomposition.json
node runtime/compile_dependencies.mjs < dependency-input.json > dependency-report.json
node runtime/compile_verify.mjs < verifier-input.json > verification.json
```

Each operator consumes one JSON input and emits one JSON output. Retain exact input/output identities, tool revision, runtime, command or function, result and error status. Use the dependency executable for both preparation and audit; use the verifier again for publication. Do not infer a target-specific result from successful fixtures.

If an authenticated checkout is unavailable, retrieve the exact file bytes via the connected GitHub API at the frozen revision; use base64 or exact UTF-8 transport, verify Git blob SHA-1 (hash of `blob <byte-length>\0<bytes>`), and stage only the required files locally. If connector output is limited, use small batches and numbered base64 chunks; use [C06](#c06) or equivalent local hash-checked transfer. [C07](#c07) provides recovery principles only; its full-runtime assembly, integration manifest, archive and regression obligations do not apply to these standalone operators. Do not route data through Google Drive, email or unrelated services, dispatch Actions runners or require an API key.

If the Node CLI is unavailable but an actual JavaScript execution environment can run the exact retrieved operator function bodies and all current fixture assertions without altering their computational logic, the direct-function route is admissible for these operators only. Verify source identity, record the exact extraction (omit only CLI/module import/export wrappers), run the complete fixture suite against those bodies, execute the real target JSON-equivalent inputs, and retain the actual results. Label this DIRECT_FUNCTION_EXECUTED, never NODE_CLI_VERIFIED. No hand-translated or simulated implementation qualifies. If source identity, complete fixture execution or actual target execution cannot be established, record the precise missing prerequisite as OPEN/BLOCKED. Continue independent authorized work without claiming computational completion.

## 5. Discovery and survivor selection (C-S03)

Use document purpose, responsibilities, informational overlap, history and dependencies. Exact duplicates are candidates, not automatically redundant files. Retain functional navigation or compatibility surfaces where genuinely needed. Establish survivor paths and proposed final ownership before repairing links. Inspect material history; record immutable revision and source IDs.

Return candidate groups, content/responsibility overlap, distinct information, historical residuals, relevant dependencies and proposed survivor(s). Classify GO (justified consolidation), NO-GO (retain separately), or TWEAK (resolve a specific missing distinction or mapping before admission). Do not execute NO-GO or unresolved TWEAK retirements. Investigate material historical versions by exact Git revision and preserve useful evidence without indiscriminately copying superseded conclusions. Prefer batch decisions that establish all destinations before reference repair.

## 6. Compilation methodology (C-S04–C-S07)

### C-S04: Consolidate losslessly and decompile

Supply the complete admitted text snapshot as `{"files":{"owner/repo:path":"text"},"targets":["owner/repo:target.md"],"history":[{"id":"immutable source identity","text":"historical text"}],"maxPairs":50000,"threshold":0.7}`. Omit targets only for intentional whole-snapshot decomposition. Select all files being substantively changed or retired, not every unchanged dependency file. Run Decompiler. Keep the raw source occurrences, exact groups, candidate overlaps, and source spans. Do not interpret truncated candidate comparisons as exhaustive. A partial inventory or unsupported file is an explicit scope limitation.

Use the actual [C02](#c02) result as the source-unit registry. Preserve every source occurrence until its disposition is verified. Retain source locators, original ordering and exact bytes where protected.

### C-S05: Layer and plan

Group information by definitions, claims, evidence, inferences, mathematics, methods, architecture, historical information, unresolved questions and additional actual responsibilities. Classify each semantic unit within its structural source span; preserve attribution, qualifications and cross-layer relationships. Determine survivor sections and anchor mapping. Use temporary holding sections for unresolved information. No destructive edits yet.

For load-bearing formal research, assess symbol/object identity, types, domains and codomains, quantifier scope, composition, proof prerequisites and evidence integrity using the applicable controls in [C15](#c15)–[C17](#c17); preserve unsupported or unresolved objects without treating them as stable mathematical primitives. These are conditional integrity controls, not permission to claim a native PDAudit run or require the historical experimental campaign.

### C-S06: Prepare dependencies before material is moved

Run Dependency with `{"mode":"prepare","before":FILES,"moves":{"owner/repo:old.md":"owner/repo:survivor.md"},"anchors":{"owner/repo:old.md#old-heading":"owner/repo:survivor.md#new-heading"}}`. Use returned `edits` as rebased original texts (keys are original sources); unchanged text comes from the frozen snapshot. Resolve OPEN mappings; retain source if ambiguous. This prevents losing relative-link context during merging. All mapped destinations must be established before coordinated repair. No writes occur in the operator.

Execute [C03](#c03). Before merging, preserve relative reference context and explicitly map renamed section anchors. When later synthesis changes a destination or anchor, refresh the mapping, rerun affected preparation and audit, and invalidate affected receipts.

### C-S07: Deduplicate, synthesize and reconstruct

Host resolves exact and semantic equivalence, subsumption, partial overlap and contradictions within layers, preserving all distinct material and source identity. Never infer semantic equivalence from similarity. Synthesize after layering; reorganize by actual responsibilities, not by original file. Preserve conflicting views as attributed positions. Historical material stays separate from current conclusions. Produce candidate snapshot, retired-file list, affected edits and per-unit preservation dispositions.

Remove exact redundancy only when context, provenance and responsibility are preserved. Semantic similarity is not equivalence. Distinguish equivalent material, subsumption, partial overlap, contradiction and independence; keep unresolved distinctions. Establish the authoritative home for each information type and preserve legitimately distinct navigation, operational and historical roles. Host judgments must be source-located and explicitly distinguished from computational receipts.

## 7. Dependency repair and audit (C-S08)

Integrate prepared references into final texts; apply coordinated changes to incoming references, indexes, inventories, registries and manifests. Run Dependency in audit mode with the same before, moves and anchors, plus `after` candidate. Resolve reported issues and explicitly inspect unchecked references. A benign retired-path literal may be dispositioned with `literalReviews:[{source,target,contentDigest,reviewed:true,rationale}]`, using the exact issue digest and source-located evidence; do not use this for an operative or dangling reference. Independently search retired paths, filenames, encoded paths, section anchors, code/config references and cross-repository links not supported by the operator. Verify actual functional dependencies and run relevant tests. Do not ignore residuals merely because the destination exists. If scope or unsupported-reference coverage cannot be established, remain OPEN.

Run [C03](#c03) against the exact candidate and recorded mappings. The operator is bounded: supported reference syntax is not the complete dependency universe. Use [C08](#c08)–[C11](#c11) when the relevant paths, graph or relationship coverage requires them; use [C12](#c12)–[C13](#c13) only for their actual Canonical Authority scope. Inspect each selected resource's current contract and prerequisites; do not treat a link in this catalogue as evidence that a tool ran. Where a dependency cannot be resolved within scope, withhold the affected retirement or publication; do not force a reference to a merely existing destination.

## 8. Preservation and candidate verification (C-S09)

Run Verifier with `before,after,decomposition,dependencyReport,history,dispositions,retire,allowedChanges,scopeReview`. The disposition map is keyed by unit ID. Exact: `{kind:"exact",target,start,end}`; semantic: same span with `kind:"semantic",reviewed:true,rationale`; historical: `{kind:"historical",reference:immutableGitHubBlobURL,reviewed:true,rationale}`; authorized removal: `{kind:"authorized-removal",reviewed:true,authorization,rationale}`. All offsets are UTF-16 code units. Unique literal spans in the same survivor or declared mapped survivor can be automatically matched; exact mechanical reference-only changes are checked against preparation output. Review these receipts for changed meaning or attribution; provide explicit dispositions where exact spans are not adequate. `scopeReview:{complete:true,evidence:"source-located coverage and functional test evidence"}` is allowed only after actual independent review of scope and unsupported references. A reported semantic review is not a proof. Maintain source provenance even for exact duplicates. Require READY_FOR_PUBLICATION plus actual semantic/functional evidence and no affected OPEN obligations.

Execute [C04](#c04) and retain its actual output. Assess candidate-specific semantic preservation, responsibility fulfilment, historical evidence and operational regressions independently of automatic exact-span matches. A computational pass does not prove semantic equivalence, authorize a mutation, or certify unscanned dependencies. Apply the scope, evidence, authority and continuation principles of [C18](#c18) at the host/operator boundary; its registered-tool ABI is not required for Compile. Recheck all changed inputs before relying on a receipt.

## 9. Publication (C-S10)

Recheck frozen Git revisions and source identities. Use one guarded commit per affected repository (or isolated branch and PR if branch rules require); never overwrite intervening changes. Cross-repository publication is not atomic: coordinate ordering, avoid transient broken live paths, record partial publication and recover explicitly. Only delete approved files once replacement content and dependencies are ready. In execution mode implement validated GO consolidations, including physical deletion; do not stop at a recommendation or substitute a redirect stub. If authorization, verified preservation or dependency closure is incomplete, withhold affected writes. Record commit and blob identities or the legitimate reason for no write.

## 10. Post-publication verification (C-S11)

Re-fetch each committed snapshot from the intended branch and compare exact content. Re-run verifier with `publication:{revision,baseDigest,files}` for a single verified snapshot; record per-repository commit identities for multi-repository runs. Verify retired paths are absent, surviving destinations and intended relationships are current, concurrent work is preserved, and applicable functional checks remain valid. Re-run affected dependency or preservation checks when the published state differs from the candidate. A commit alone is not completion.

## 11. Continuation, reporting and closure (C-S12)

Maintain one compact execution ledger, reusing the operator outputs rather than duplicating their contents.

| Record | Minimum required evidence |
| --- | --- |
| Run | Scope, mode, target revisions, authorization, current stage |
| Stage | ID, inputs, predecessor evidence, disposition, output or blocker |
| Operator | Exact version, execution route, input/output identity, fixture evidence, actual result |
| Candidate | Retired/survivor paths, GO/NO-GO/TWEAK, source and dependency mappings, preservation evidence |
| Publication | Commits, verified state, actual deletions, residuals |
| Continuation | Last verified checkpoint, outstanding obligations, next operation, storage location if available |

Persist a recoverable checkpoint in authorized storage when needed, without creating unnecessary repository reports or inventing durable state. After a blocker, record the exact unmet requirement, recovery attempts and affected work; continue independent authorized stages or groups. Do not repeatedly ask for authorization already granted. Resume only for the same authorized scope and current revisions; invalidate stale evidence and reconcile intervening changes. Continue until applicable obligations close or an actual limit prevents further progress. Report incomplete execution explicitly, including affected retirements withheld and precise remaining work.

Completion requires actual authorized deletions, preserved information and provenance, coherent ownership, repaired dependencies within admitted scope, independently verified functional consequences, and verified publication. The three operators never independently authorize destructive edits. Their finite outputs are evidence, not a substitute for semantic or operational review. No tool count, similarity score or partial result constitutes completion.

Report the actual before/after file counts, surviving and retired paths, semantic and dependency residuals, verified operator dispositions, tests and commit links; distinguish discovery-only, recommendations-only, verified execution, partial and blocked outcomes. For no-write modes report only the authorized deliverable, never completed physical compilation.

**Do not substitute a plan for execution. Start C-S01 immediately.**

## 12. Technical references

### Required for ordinary computational execution
<a id="c01"></a>
- **C01:** [Mathematical specification](https://github.com/thytabakman-jpg/Take-5/blob/main/Compile%20Mathematics.md)

<a id="c02"></a>
- **C02:** [Decompiler](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_decompiler.mjs)

<a id="c03"></a>
- **C03:** [Dependency preparation and audit](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_dependencies.mjs)

<a id="c04"></a>
- **C04:** [Preservation and publication verifier](https://github.com/thytabakman-jpg/Take-5/blob/main/runtime/compile_verify.mjs)

<a id="c05"></a>
- **C05:** [Executable fixture tests](https://github.com/thytabakman-jpg/Take-5/blob/main/tests/test_compile.mjs)

### Conditional retrieval recovery
Retrieve only when the ordinary route is blocked. Do not bootstrap the full Repair runtime to run standalone Compile.
<a id="c06"></a>
- **C06:** [Connector-to-local source transfer helper](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/connector_source_transfer.py)

<a id="c07"></a>
- **C07:** [GitHub-only retrieval and recovery reference](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md#github-only-connector-to-local-transfer)

### Conditional dependency and project resources
Use when the actual reference scope or project requires them.
<a id="c08"></a>
- **C08:** [Research Sorter](https://github.com/thytabakman-jpg/Reaserch/blob/main/.github/skills/research-sorter/scripts/sort_research.py)

<a id="c09"></a>
- **C09:** [Knowledge Web dependency closure](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/dependency-closure.mjs)

<a id="c10"></a>
- **C10:** [Knowledge Web graph builder](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/build-graph.mjs)

<a id="c11"></a>
- **C11:** [Knowledge Web source path resolver](https://github.com/thytabakman-jpg/Reaserch/blob/main/Tools%20and%20Workflows/Individual%20Tools/Knowledge%20Web%20Explorer/source-path-resolver.mjs)

<a id="c12"></a>
- **C12:** [Canonical Authority cross-repository validator](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Philosophy/Jewish%20Philosophy/tools-and-validation/tools/check_canonical_authority_cross_repo_links.py)

<a id="c13"></a>
- **C13:** [Canonical Authority Markdown validator](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Philosophy/Jewish%20Philosophy/tools-and-validation/tools/check_canonical_authority_markdown_links.py)

### Methodological and integrity resources
Use the applicable principles and gates as specified above. C14 is a candidate protocol, not a promoted universal runtime requirement.
<a id="c14"></a>
- **C14:** [Semantic Preflight Candidate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROMPT_SEMANTIC_PREFLIGHT_CANDIDATE.md)

<a id="c15"></a>
- **C15:** [PD integrity protocol](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Mathematics%20and%20Formal%20Methods/PD/protocol/PROTOCOL.md)

<a id="c16"></a>
- **C16:** [Mathematical object-integrity gate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Tool%20and%20System%20Research/ImprovementCore/tool-ecosystem/MATHEMATICAL_OBJECT_INTEGRITY_GATE_001_2026-10-06.yaml)

<a id="c17"></a>
- **C17:** [Mathematical prerequisite-integrity gate](https://github.com/thytabakman-jpg/Reaserch/blob/main/Projects/Tool%20and%20System%20Research/ImprovementCore/tool-ecosystem/MATHEMATICAL_PREREQUISITE_INTEGRITY_GATE_001_2026-10-06.yaml)

<a id="c18"></a>
- **C18:** [Semantic Worker Contract](https://github.com/thytabakman-jpg/Take-5/blob/main/architecture/Semantic%20Worker%20Contract.md)

### Separately authorized registered-tool execution and precedent
C19–C21 govern only separately authorized configured Take-5 tools. C22 provides procedural precedent; it does not import Repair's mandatory battery into Compile.
<a id="c19"></a>
- **C19:** [Registered Tool Execution Guide](https://github.com/thytabakman-jpg/Take-5/blob/main/integration/Tool%20Execution%20Guide.md)

<a id="c20"></a>
- **C20:** [Registered Tool Execution Architecture](https://github.com/thytabakman-jpg/Take-5/blob/main/architecture/Tool%20Execution%20Architecture.md)

<a id="c21"></a>
- **C21:** [Registered runtime bootstrap and bindings](https://github.com/thytabakman-jpg/Take-5/blob/chatgpt-runtime-bootstrap/chatgpt-integration/README.md)

<a id="c22"></a>
- **C22:** [Repair Prompt (procedural precedent, not an execution dependency)](https://github.com/thytabakman-jpg/Take-5/blob/main/Repair%20Prompt.md)
