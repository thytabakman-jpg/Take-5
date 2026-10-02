# Current ICC128 Conversation Control

Date: 2026-10-02
Status: VALIDATED CURRENT REPOSITORY STATE

## Current controller

ICC128 is again a registered current configured tool in Take-5.

Active runtime:
- runtime/icc_entry.py
- runtime/icc128_entry_binding.py
- runtime/icc_entry_053_candidate.py
- runtime/icc128_episode_adapter.py
- runtime/icc128_autonomous_controller.py
- runtime/icc128_semantic_generator_adapter.py
- runtime/rho128_policy.py
- runtime/kernel053_packetize.py
- runtime/kernel053_child_result.py
- runtime/kernel053_durable_execution.py

The frozen ICC128 Legacy snapshot remains separate and unchanged.

## Jane handoff

Jane owns continuity/currentness supervision, not substantive action selection.

Active bridge:
- runtime/jane_icc128_bridge.py

A READY Jane continuity packet becomes explicit ICC128 controller state and memory.
Missing continuity fails OPEN rather than silently inventing state.

## Conversation response selection

Active response gate:
- runtime/adaptive_response_selector.py

Admissible responses must match requested artifact identity and requested format, be exact and complete, contain no unsupported claims or abstraction drift, and not reproduce rejected candidates.

Among admissible responses, choose minimum extra output.

AFFIRMATIVE_FIRST is also a hard admissibility coordinate. A response candidate marked negative-first is rejected before ranking, so brevity cannot outrank the protected prose order.

User rejection updates durable episode state and forces reselection.

## Host ingress identity

Host-facing repository-backed ICC execution is now gated by:

- runtime/icc_host_ingress.py
- runtime/icc_host_gateway.py
- architecture/ICC_HOST_INGRESS_CONTRACT_001_2026-09-27.md

The prefix ICC expresses routing intent. It does not establish that ICC ran.

A host may claim repository-backed ICC identity only with a HOST_INGRESS_ADMITTED
receipt bound to the exact request and a concrete canonical Take-5/main commit.
Admission also requires explicit evidence-receipt identifiers for repository
verification, currentness verification, entry binding, the complete ASSERT then
GOAL observer bootstrap, and current ICC128 registration.

Hosted ICC emission requires the same receipt and projects the formal ICC128 and
Take-5 identities through the mathematical color gate.

## Historical recovery guard

Active recovery gate:
- runtime/exact_equation_recovery.py

Exact historical recovery requires an external source receipt.
Derived reconstruction is not exact recovery.
Rejected candidates cannot silently return unless explicitly reopened.

The invented four-family big-union recovery was retracted in:
- provenance/EXACT_FOUR_FAMILY_36_UNION_RECOVERY_REPORT_001_2026-09-27.md

The 36x4 configured-run expression is retained only as a source-backed prior-assistant candidate, not as user-confirmed historical identity:
- provenance/RECOVERED_36X4_IMPROVEMENT_CORE_EQUATION_001_2026-09-27.md

## Validation

Take-5 Validation run 36298980965: SUCCESS.

Host-ingress PR #159 validation before final documentation delta:
- Take-5 Validation run 36300397075: SUCCESS.
- Capability Preservation run 36300397054: SUCCESS.

The active repository path now covers:
Jane continuity -> ICC128 state-relative selection -> execution/reselection -> exact recovery gate -> minimal response selection.

## External boundary

Repository code cannot force a ChatGPT host to display a separate ICC128 UI identity or green presence dot and cannot universally intercept a host that bypasses Take-5.

Do not claim that external host state from repository evidence alone.


## Kernel 053 canonical promotion

On 2026-10-02, PR #198 promoted the Kernel 053 ICC128 control path to main.

Current merge commit:
- b5bd2ba25bdde8c947a70e9d234b7a41f9dde563

Canonical control ownership:
- ICC128 owns top-level substantive question/work selection and continuation.
- ImprovementCore owns controller decisions only inside an ICC128-delegated improvement episode.
- Jane owns continuity/currentness supervision and does not select substantive work.
- D_exec owns durability/execution infrastructure and does not own rho_128 selection.

Canonical run_icc:
- constructs ICC128 internally from typed ICC128RuntimeBindings;
- accepts no arbitrary ic_fn or caller-supplied parent controller;
- anchors its operational goal to the configured bootstrap GOAL receipt;
- applies Packetize as a non-selecting evidence/dependency boundary;
- blocks TARGET_TRANSFORM until a typed Commit_sigma execution adapter exists.

The former arbitrary injected-controller wrapper survives only as:
- runtime/icc_entry.py::run_icc_debug_injected

That debug surface is not evidence of canonical repository-backed ICC128 execution.

Promotion validation:
- Take-5 Validation: PASS
- Capability Preservation: PASS
- Tool System Every-Tool Sweep: PASS
- Kernel 053 Durable Backend Bakeoff: PASS
- ImproveCore Legacy Restoration 130: PASS
- ImproveCore Legacy Semantic Holdouts 132: PASS
