# HF2 #1 — Finish Every Actionable ZIP Job 130

Date: 2026-09-26
Capability reapplied: ImprovementCore
Recurrence: HF002
Instruction preserved unchanged: finish every currently actionable job on this problem
Input successor: c67ca2999039ee6e25578f92732887a08c4326dd

## Round 0

Reapply ImprovementCore to the merged runtime successor.

Material change from prior state:
typed BOUND_ZIP external evidence now executes binding, archive expansion, artifact_intake, and work lifting before controller stages.

Question:
what actionable job exists only because this successor now exists?

Finding:
the runtime behavior is active and tested, but current recovery surfaces still describe only the existence of the archive adapter. They do not yet preserve the stronger normal-path activation or fail-closed external-gap behavior.

This creates a regression risk:
a future recovery can restore archive_artifact_intake.py while silently losing the external-acquisition call path.

HF2 disposition:
REAPPLY_C.

## Round 1 — repair

Promote the actual behavior into the existing recovery system.

1. CURRENT_IMPROVEMENT_CORE invocation path now records:
external acquisition
-> typed BOUND_ZIP verification/expansion
-> artifact_intake
-> obligations
-> manager.

2. Protected behavior now includes:
- BOUND_ZIP external output executes intake before manager;
- ZIP processing failure preserves external OPEN_GAP;
- raw bytes/generator callables do not persist into controller evidence.

3. IMPROVEMENT_CORE_RECOVERY_MANIFEST_082 now names the external bound-ZIP runtime behavior and this execution evidence.

4. improvement_core_recovery.py now fails when:
- the current anchor omits the normal-path execution behavior;
- the fail-closed OPEN_GAP rule disappears;
- the protected-behavior manifest drops any of the three new invariants;
- the external acquisition regression test disappears.

## Remaining live frontier

Repository-local:
validation of this recovery promotion.

External:
positive identity of any still-unbound substantive archive remains outside what repository code can manufacture.

HF2 has not declared terminal closure before validation.


## Final validation and merge

Branch validation:
- Take-5 Validation 36277491072: SUCCESS
- Capability Preservation 36277491021: SUCCESS

Merged through PR #127.

Merge:
12339480846336ceabc16e6f33716d5395e20ba8

Post-merge validation:
- Take-5 Validation 36277515519: SUCCESS
- ImproveCore Self Study 104 36277515523: SUCCESS

## HF2 #1 terminal disposition

All repository-owned work discovered by this recurrence was implemented, recovery-protected, validated, and merged.

HF2[ImprovementCore]:
RELATIVE_CLOSE.

Remaining external archive-identity coordinate:
OPEN_WITH_REENTRY.
