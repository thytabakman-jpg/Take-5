# CURRENT HF1 — Recovery Anchor 084

Date: 2026-09-26
Status: CURRENT MATHEMATICAL RECOVERY AUTHORITY

## Identity

Current formal object:
HF1 / HF001

Current mathematical surface:
architecture/HF1_MATHEMATICS_084.md

Current runtime:
runtime/hf1_episode.py

Historical compatibility:
runtime/hf_controller.py

Canonical configured identity:
runtime/tool_manifest.py
runtime/tool_run_registry.py

## Current equation

HF1 is the governed recurrence:

x_t
-> K_PD(x_t)
-> O_t
-> P*_t
-> m_t
-> Exec
-> C_TR
-> x_(t+1)
-> (Delta_W,Delta_D,Delta_R)
-> rho
-> close / OPEN / BLOCKED / reenter.

Exact sufficient package:

P* in argmin_P (sum c_i, |P|, lexical(P))

subject to:

union C_i covers all live obligations.

Delta signatures:

Delta_W iff world_state changes.
Delta_D iff discovery_state changes.
Delta_R iff result_sensitive_state changes.

Reentry:

world or discovery delta -> REENTER_OBSERVE
result-sensitive-only delta -> REVERIFY
no delta -> NO_REENTRY.

Relative closure requires:
- Tool Run Closure CLOSED;
- no live K_PD obligations;
- required reverification succeeded.

## Architectural resolution

The historical activation loop is not a rival HF1 loop.

It is the execution sub-transition inside the governed HF1 recurrence.

Tool Run Closure remains distinct and owns consequence closure.

HF1 owns the episode-level question:
where does the system go next after admitted execution/closure state?

## Fail-closed coordinates

HF1 returns OPEN/BLOCKED rather than guessing when:
- no sufficient package exists;
- mode is unresolved;
- execution is not consumed;
- Tool Run Closure is OPEN/BLOCKED;
- delta signatures are absent;
- reverification is required but unavailable/fails;
- live obligations remain with no reentry;
- resource bound is reached.

## Recovery verification

runtime/hf1_recovery.py
tests/test_hf1_recovery.py
tests/test_hf1_episode.py

## Load order

1. integration/CURRENT_HF1.md
2. architecture/HF1_MATHEMATICS_084.md
3. runtime/hf1_episode.py
4. runtime/hf_controller.py
5. runtime/kpd_projection.py
6. runtime/mode_selector.py
7. runtime/tool_run_closure.py
8. runtime/tool_manifest.py
9. runtime/tool_run_registry.py
10. tests/test_hf1_episode.py

## Scope

HF1 mathematics is complete relative to the typed packet interface.

Construction of world_state, discovery_state, and result_sensitive_state is upstream.
HF1 requires them for delta classification and fails OPEN when they are missing.

Global minimality of the entire Take-5 controller is not part of the HF1 job.
