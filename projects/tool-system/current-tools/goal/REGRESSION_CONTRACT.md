# Regression contract: GOAL

A valid package keeps all of these true:

- required core files exist
- exactly 36 Scope x ModeFace coverage pages exist
- coverage pages are audit evidence, not semantic authority
- the distinct SourceScope x TargetScope surface is not merged into coverage
- decisions, lessons, runs, and evidence are append-only
- package generation never overwrites changed existing files
- current configured tools have one package each
- aliases do not create duplicate mutable authority
- missing semantics/runtime/evidence remain typed OPEN


## GOAL-specific non-regression gates

The package-level checks above are necessary but do not certify a GOAL run.
For the current Take-5 configured GOAL tool, preserve the following additional
executable/source contracts. Resolve selectors from code, not from the newest
file date, a copied specification, or an external source-map link.

- **One active specification:** `manifest_for("GOAL").lineage_contract` in [`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py) selects the current GOAL full mathematical identity, and [SOURCE_MAP.md](SOURCE_MAP.md) agrees. Earlier numbered versions remain historical evidence.
- **One configured entrypoint:** `compilation_witness("GOAL").entrypoint` in [`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py) selects `goal.recover_goal_configured`; [RUNTIME.md](RUNTIME.md) must not conflate it with native `goal.recover_goal`.
- **Fail-open MT prerequisite:** without a valid robust-MT receipt, the configured entrypoint in [`runtime/goal.py`](../../../../runtime/goal.py) returns `OPEN` with `MT_PREREQUISITE_REQUIRED`; a successful bare native recovery is not an equivalent configured execution.
- **Dependency and HF2 visibility:** [DEPENDENCIES.md](DEPENDENCIES.md) must retain `runtime/goal.py`, the MT semantic-return gate, and both configured-HF2/recurrence components in the impact cone.
- **Evidence-bound CURRENT:** [CURRENT_STATE.md](CURRENT_STATE.md) distinguishes package registration from a witnessed run; [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) preserves genuinely unresolved cross-repository transfers without reopening a resolved Take-5 configured-tool selector.

Affected executable regression owners are
[`tests/test_goal.py`](../../../../tests/test_goal.py) and
[`tests/test_goal_fullmath_identity.py`](../../../../tests/test_goal_fullmath_identity.py).
A green pointer or a static test is not proof that an external host executed the
full configured GOAL path. When a condition above fails, retain `OPEN` for the
affected runtime/currentness claim and repair the real owner and consumer before
claiming renewed closure.
