# Full Corpus Placement Audit 2026-09-26

Status: EXECUTABLE AUDIT SNAPSHOT
Repository: thytabakman-jpg/Take-5
Audit branch: improvecore/full-corpus-placement-audit-20260926

## Coverage

The manifest enumerates every blob reachable from this branch's recursive Git tree at audit start.

Total files: 559
Tree truncated: false

This layer is intentionally non-destructive. Historical evidence is not moved merely because its folder name is old. Physical relocation requires a semantic placement decision plus reference repair. The manifest makes every file addressable before any move.

## Placement classes

- GENERAL: 192
- EXECUTABLE: 102
- VERIFICATION: 88
- RESEARCH: 77
- ARCHITECTURE: 54
- CURRENT_CONTROL: 26
- EVIDENCE_HISTORY: 16
- STATE_CONFIG: 3
- NAVIGATION: 1

## Fail-closed rules

1. A file is not treated as obsolete because a newer file exists.
2. A historical audit can carry a strict-gain discovery even when its controller is superseded.
3. Executable code is audited against the semantic object it claims to realize.
4. UNRESOLVED_PLACEMENT is a queue, not a trash category.
5. Broken references, duplicate authority claims, stale current-state claims, and unindexed mathematical definitions are material findings.
6. Promotion into current control requires provenance, conflict checking, and verification.
7. Any material delta reopens the affected dependency cone.

## Unresolved placement queue

Count: 0

- none detected by path classifier



## Next executable pass

Run the repository-local full corpus auditor added by this campaign. It reads file contents, extracts formal definitions, status/currentness claims, references, TODO/OPEN markers, duplicate-content witnesses, and orphan candidates, then emits a content-derived report without rewriting source evidence.

The path manifest is coverage evidence, not semantic closure.
