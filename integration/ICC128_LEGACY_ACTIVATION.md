# ICC128 Legacy activation contract

Status: FROZEN / ACTIVATABLE

Canonical phrase:

`activate ICC128 Legacy`

That phrase resolves to the immutable snapshot at:

`thytabakman-jpg/Reaserch@e4c76c595b44a35fd9efc02cde8979e656ef54e8`

Activation rules:

1. Resolve through `runtime/legacy_tool_registry.py`.
2. Load through `runtime/icc128_legacy.py`.
3. Use only `legacy/icc128-legacy/snapshot/` as the tool definition.
4. Do not substitute current ICC-128, current ImprovementCore, or Reaserch main.
5. Do not write to Reaserch.
6. Do not silently apply later Take-5 wrapper semantics to this legacy controller.
7. The current host can instantiate the frozen semantic-model and execution interfaces without redefining them.
8. External state-changing actions remain bounded by current host authority.
9. Every Legacy run requires a learning report under `artifacts/icc128-legacy-learning/`, including zero-learning and failed runs.
10. The run is not closed until a GitHub commit receipt exists for that report.
11. Final within-run learned memory is discarded after report submission; the next activation starts fresh.

Ordinary `ICC128` remains the current system object. `ICC128 Legacy` is explicit opt-in.
