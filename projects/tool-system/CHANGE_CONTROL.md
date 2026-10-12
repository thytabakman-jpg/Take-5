# Tool System Change Control

Status: CURRENT

Delta = <request, owner, old_state, proposed_state, reason, dependencies, tests, decision, receipt>.

Change the smallest owner that actually owns the property.
Do not rebuild every package because one tool changes.
After an admitted material change compute and inspect its affected package/dependency cone.
Retain old evidence; supersede explicitly rather than rewriting historical records.
A new current tool requires package creation in the same admitted change.

## Exact owner and impact boundary

1. Bind the requested change to its **current** owner: configured identity in [tool_run_registry.py](../../runtime/tool_run_registry.py), protected behavior in [tool_manifest.py](../../runtime/tool_manifest.py), native execution in [portable_tool_conductor.py](../../runtime/portable_tool_conductor.py), package template in [tool_project_packages.py](../../runtime/tool_project_packages.py), or derived [index](TOOL_INDEX.md) / [crosswalk](SOURCE_MAP.md). A navigation edit alone cannot activate a new runtime edge.
2. Freeze the source blob and accepted working route. Trace the affected tool's package and immediate consumer; keep independently owned or historical semantics untouched.
3. On **new, removed or renamed** configured identities, reconcile registry membership, package materialization, index parity, crosswalk identity/classification, protected manifest and native compilation; do not infer one from another. A missing external Reaserch match is recorded as `UNMAPPED` or `OPEN`, not invented.
4. Preserve original evidence, generated-versus-curated source-map ownership, old working behavior, explicit environment dependencies, and the two different 36-cell structures.
5. Run native positive and adversarial checks for the affected contract. For tool identity/conductor changes require an exact registered-ID census, missing/duplicate/incorrect-ID controls, and OPEN/BLOCKED preservation; for source-map changes require link identity and generator idempotence/collision controls. Check the actual [regression contract](REGRESSION_CONTRACT.md).
6. Commit on the authorized branch, read the committed bytes and check the matching CI/workflow result. If a mandatory check cannot run or fails, leave that **specific** Level 4 claim `INCOMPLETE` instead of treating an approved plan or historical successful receipt as a pass.
7. Reconcile cross-repository changes under each repository's own authority. A link to Reaserch is provenance and navigation, not a new Take-5 runtime selector.

The change record is the existing commit/test/evidence trail; do not create a duplicate registry, per-file report or copy of substantive mathematics solely for administrative convenience.
