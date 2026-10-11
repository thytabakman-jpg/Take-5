# Source map: RootCause

## Direct sources

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py
- integration/CURRENT_TOOL_REALITY.md

## Shared current authorities

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- integration/CURRENT_TOOL_REALITY.md
- projects/tool-system/AUTHORITY_REGISTRY.md

## Opt-in external historical evidence (non-authoritative)

- `runtime/root_cause_managed.py` — RootCause child attachment and conditional historical consultation
- `runtime/root_cause_knowledge_lookup.py` — read-only, current-file projection over a separately bound Reaserch checkout
- `tests/test_root_cause_knowledge_lookup.py` — match, near-miss, private/no-access, no-match and non-interference tests
- [Reaserch question-first Root Cause knowledge entry](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/research/consolidations/ROOT_CAUSE_ROLLING_DISCOVERY_KNOWLEDGE.md) — discover original investigations without adopting their claims as current authority

The external research checkout is an optional historical source, not a source of canonical tool identity, executable repair permissions or causal ranking. No default payload change occurs without an explicit `research_root` binding. Approved consumers can invoke `python runtime/root_cause_knowledge_lookup.py --research-root /path/to/Reaserch "current observed failure"` and parse candidate/NO_MATCH/NO_ACCESS JSON. `record_verified_root_cause_outcome(...)` is an explicitly invoked post-repair connector to existing material or negative-learning memory, with required owner admission and verified current evidence; it is not a globally installed event hook.

## Rule

Pointers preserve provenance. This package does not copy legacy evidence merely
to make the folder look complete.
