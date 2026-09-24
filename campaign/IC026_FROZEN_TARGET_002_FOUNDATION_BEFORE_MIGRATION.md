# IC-026 Frozen Target Correction 002 — Foundation Before Migration

Date: 2026-09-24
Status: FROZEN TARGET SUPERSEDES campaign/IC026_ACTUAL_GOAL_001.md where inconsistent
Authority change: none

## Actual goal

Build and validate the best foundation for the eventual autonomous goal-to-completion system before any migration.

Migration is explicitly outside the active execution target until the foundation passes a user-controlled readiness review.

## Required sequence

1. Recover all strongest demonstrated functionality and foundational invariants from Reaserch, Take-2, Take-3, Take-4, ICC/IC lineage, PD, runtime/backend, map system, and relevant experiments.
2. Run PD on the concept CORE. Freeze its extension/intension, role, success conditions, dependencies, and distinctions from kernel/controller/runtime/state/capability/interface.
3. Run PD independently on the concept KERNEL. Freeze its extension/intension, role, success conditions, dependencies, and distinctions from core/controller/runtime/state/capability/interface.
4. Reclassify every candidate foundation component against those corrected concepts. Do not inherit old placement merely from historical labels.
5. Build a candidate foundation from the strongest surviving functions/invariants.
6. Research external scientific/engineering literature and established systems on kernels, agent architectures, control loops, operating-system abstractions, planning/tool-use/memory/verification, orchestration, and adjacent architectures. Borrow before inventing.
7. Compare our candidate against external alternatives by function and protected behavior, not vocabulary or prestige.
8. Revise the foundation where external evidence exposes a better mechanism, missing invariant, unnecessary primitive, or superior decomposition.
9. Validate internally and prospectively until foundation readiness is supported.
10. STOP BEFORE MIGRATION. Produce a migration-readiness packet for the user.
11. Migration occurs only after the user explicitly launches the all-tools readiness attack and then explicitly authorizes migration.

## Frozen Target Token

user_goal: validated_best_foundation_before_migration
requested_mode: autonomous_research_build_validate_then_stop_before_migration
completion_gate:
  - CORE_PD_complete_enough_for_architecture
  - KERNEL_PD_complete_enough_for_architecture
  - historical_best_functionality_recovered
  - historical_best_foundations_recovered
  - component_placement_reclassified
  - external_research_program_completed_to_saturation_or_named_OPEN
  - candidate_compared_against_external_architectures
  - external_lessons_integrated_or_rejected_with_reason
  - foundation_candidate_implemented_as_nonproduction_successor_artifact
  - internal_regression_and_holdout_evidence
  - no_known_foundational_blocker_hidden_by_migration
  - migration_readiness_packet_ready
terminal_boundary: USER_REVIEW_BEFORE_MIGRATION
supersession_condition: explicit_user_goal_change

## Prohibitions

- no migration
- no production promotion
- no treating Take-5 SUCCESSOR_READY as permission to migrate
- no assuming historical use of CORE or KERNEL fixes their meaning
- no equating kernel with the entire foundation
- no equating core with controller
- no architecture choice solely because an earlier Take used it
- no stopping at an external literature survey; findings must feed back into the candidate foundation

## Target effect

Semantic-worker/runtime migration work is SUPPORT or META_ONLY until the foundation is ready.
CORE/KERNEL PD, historical recovery, external comparison, component reclassification, foundation construction, and validation are DIRECT.
