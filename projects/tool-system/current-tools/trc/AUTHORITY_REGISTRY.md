# Authority registry: TRC

Status: CURRENT PACKAGE ROUTING

| Object | Owner |
|---|---|
| package identity/status routing | this package |
| current configured-tool identity | runtime/tool_run_registry.py |
| current protected tool identity | runtime/tool_manifest.py |
| current executable realization | runtime/portable_tool_conductor.py |
| historical/lineage evidence | SOURCE_MAP.md pointers |
| package current projection | CURRENT_STATE.md |
| unresolved package questions | OPEN_QUESTIONS.md |
| decisions | DECISION_LOG.md, append-only |
| lessons | LESSONS_LEDGER.md, append-only |
| run evidence | runs/, append-only |
| evidence entries | evidence/, append-only |
| coverage findings | coverage/*.md, audit evidence only |

## Collision rule

A package file does not acquire authority merely by repeating content from an
external canonical source. When two locations appear to own the same mutable
truth, fix the routing before editing either one.
