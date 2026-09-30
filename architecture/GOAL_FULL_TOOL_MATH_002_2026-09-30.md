# GOAL Full Tool Mathematical Identity 002

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Parent: architecture/GOAL_FULL_TOOL_MATH_001_2026-09-27.md
Controller: Raise the Ceiling / RTC
Tool: GOAL

## Preserved identity

This successor preserves the five-coordinate GOAL identity recovered in 001:

```
FullMath_(J,K)(GOAL)
=
<N_GOAL,W_GOAL,G_GOAL,P_GOAL,L_GOAL>
```

The native operator remains governing-goal recovery over supplied candidates.
GOAL still does not manufacture arbitrary prose candidates and still does not
authorize object mutation.

## Ceiling defect

The standing execution rule requires robust MT before GOAL, including the
black-box semantic return gate. The 001 identity described GOAL's configured
wrapper but did not make an MT execution receipt a fail-closed prerequisite.

Therefore a repository-owned GOAL entrypoint could be reconstructed without
proof that robust MT had actually run first.

## Strengthened configured wrapper

Let r be the supplied MT preflight receipt.

```
ValidMTPreflight(r)
iff
r.tool_id = MT
and r.invocation_profile = FULL_CONFIGURED_HF2_V1
and r.black_box_gate = MT_BLACK_BOX_SEMANTIC_RETURN_GATE
and r.status in {CLOSED_RELATIVE, OPEN}
and Evidence(r) != empty.
```

OPEN is admissible as an MT status because robust MT is allowed to preserve
unresolved black-box residue. The prerequisite is execution plus preservation
of residue, not forced semantic closure.

Define the configured GOAL boundary:

```
ConfiguredGOAL(candidates,r)
=
OPEN(MT_PREREQUISITE_REQUIRED)
    when not ValidMTPreflight(r);

ConfiguredGOAL(candidates,r)
=
recover_goal(candidates)
    when ValidMTPreflight(r).
```

The MT receipt is carried into the configured result evidence so the GOAL run
cannot be truthfully reported without a preflight witness.

## Preserved native semantics

`runtime/goal.py::recover_goal` (`goal.recover_goal`) remains the native semantic operator from 001.

A new configured entrypoint may wrap it, but no successor may:
- merge protected constraints into G=<X,T,I,Sigma>;
- silently rank plural admissible goals;
- fabricate candidate evidence;
- convert OPEN into closure;
- treat MT as a goal selector.

## New protected behavior

```
GOAL_ROBUST_MT_PREREQUISITE
```

This behavior belongs to the configured wrapper boundary, not to N_GOAL.

## Portability

A host that cannot supply a valid robust-MT receipt leaves configured GOAL OPEN.
That is preferable to silently degrading GOAL to a one-shot native call.

## Strict-gain test

The successor is admissible because:
1. every behavior protected by 001 remains unchanged;
2. native GOAL remains independently testable;
3. configured GOAL gains a non-bypassable receipt requirement for the standing
   robust-MT prerequisite;
4. missing MT evidence now fails open instead of being silently ignored.

No broader arbitrary-prose autonomy claim is introduced.


## Inherited protected behavior set

This successor retains the protected behaviors established by 001:

```
GOAL_EVIDENCE_GROUNDED_ADMISSION
GOAL_CONSTRAINT_SEPARATION
GOAL_OBJECT_X_T_I_SIGMA
GOAL_PLURALITY_FAIL_OPEN
GOAL_FULL_TOOL_IDENTITY
```

The configured geometry remains `D36_C`. Ordinary configured recurrence remains
`HF002` under `FULL_CONFIGURED_HF2_V1`.

## Historical process defect

The historical process defect recorded in 001 remains part of the retained
lineage. Earlier implementation existed before this dedicated mathematical
identity was frozen. This successor does not erase that chronology; it only
closes the newly localized MT-prerequisite gap prospectively.

## External boundary

Repository-owned configured GOAL is strengthened by this successor.
Universal interception by an unrelated external host remains
`EXTERNAL_NOT_OWNED`.
