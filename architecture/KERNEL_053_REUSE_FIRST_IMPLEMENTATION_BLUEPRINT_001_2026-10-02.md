# Kernel 053 Reuse-First Implementation Blueprint 001

Date: 2026-10-02
Status: NON-AUTHORITATIVE IMPLEMENTATION BLUEPRINT
Parent: architecture/KERNEL_MATH_CONTRACT_053.yaml
Branch: kernel-053-implementation-prototype

## Governing rule

Before new code is admitted, classify the requirement as one of:

1. USE_EXISTING_TAKE5
2. ADAPT_EXISTING_PATTERN
3. USE_EXTERNAL_LIBRARY
4. NEW_CODE_REQUIRED

Custom code is the last category, not the default.

## Reuse map

| 053 responsibility | Classification | Source / target |
| --- | --- | --- |
| ICC128 endogenous loop | USE_EXISTING_TAKE5 | runtime/icc128_autonomous_controller.py |
| rho_128 state-relative selector | USE_EXISTING_TAKE5 | runtime/rho128_policy.py |
| semantic G_Q/G_W schema | USE_EXISTING_TAKE5 | runtime/icc128_semantic_generator_adapter.py |
| Jane continuity handoff | USE_EXISTING_TAKE5 | runtime/jane_icc128_bridge.py |
| ASSERT -> GOAL bootstrap | USE_EXISTING_TAKE5 | runtime/icc_bootstrap.py |
| configured HF2 execution | USE_EXISTING_TAKE5 | runtime/configured_hf2_execution.py |
| formal tool binding/execution receipts | USE_EXISTING_TAKE5 | runtime/improvement_core_tool_bridge.py |
| protected state commit | USE_EXISTING_TAKE5 | runtime/state_commit.py |
| PTI | USE_EXISTING_TAKE5 | runtime/protected_transition_integrity.py |
| current ICC128 adapter pattern | ADAPT_EXISTING_PATTERN | runtime/improvement_core_legacy_candidate.py |
| canonical ICC128 entry binding | NEW_CODE_REQUIRED | runtime/icc128_entry_binding.py |
| Packetize no-selection enforcement | NEW_CODE_REQUIRED | runtime/kernel053_packetize.py |
| delegated child -> ICC128 delta projection | NEW_CODE_REQUIRED | runtime/kernel053_child_result.py |
| pluggable D_exec protocol | NEW_CODE_REQUIRED | runtime/kernel053_durable_execution.py |
| canonical candidate ICC128 episode adapter | ADAPT_EXISTING_PATTERN | runtime/icc128_episode_adapter.py |
| candidate wrapper entry with no arbitrary ic_fn | NEW_CODE_REQUIRED | runtime/icc_entry_053_candidate.py |
| retries/checkpoint/replay/child lifecycle | USE_EXTERNAL_LIBRARY | D_exec backend, not ICC128 |
| durable backend candidate A | USE_EXTERNAL_LIBRARY | DBOS |
| durable backend candidate B | USE_EXTERNAL_LIBRARY | Temporal |
| durable backend candidate C | USE_EXTERNAL_LIBRARY | Restate |

## External-code rule

External durable engines may own durability mechanics only.

They may not own:
- G_Q;
- G_W;
- rho_128;
- governing GOAL;
- authority expansion;
- Commit_sigma admission;
- ICC128 parent terminality.

## Prototype sequence

1. Build the four missing seams around existing Take-5 code.
2. Prove controller ownership and parent/child isolation with holdouts.
3. Keep Take5InlineBackend as the baseline D_exec realization.
4. Add external backend adapters only behind D_exec.
5. Compare external engines on the same crash/replay/idempotency fixture.
6. Promote only after PTI/currentness/runtime holdouts close.

## External evidence snapshot

As of 2026-10-02:
- Temporal Python SDK is MIT-licensed and provides deterministic workflows, child workflows, activities, replay, retries and durable execution history.
- DBOS is MIT-licensed, Python-native, supports SQLite for testing and Postgres for production, and resumes workflows from durable step checkpoints.
- Restate Python SDK is MIT-licensed and offers durable workflows plus keyed single-writer state semantics.

Detailed external comparisons remain evidence, not mathematical identity.
