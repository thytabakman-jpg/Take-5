# ImprovementCore Minimal-Prompt HF2 Repeated Campaign

Date: 2026-09-26
Status: EXECUTED / RELATIVE CLOSE
Evidence role: chat/history evidence, no structured candidate handoff
Workflow run: 36278210374
Workflow conclusion: SUCCESS

## Prompt supplied to every episode

"ImprovementCore. Here is the chat/history evidence. Figure out what needs to be done."

No target, job, or basis was supplied by the host.
Zero-request upstream discovery formed the entry seed.
The older structured handoff that previously prioritized IC-HOST-CAPABILITY-DISCOVERY was excluded from this campaign as a selection signal while remaining preserved as historical evidence.

## Campaign execution

Four full user-facing ImprovementCore episodes were executed.

Each episode used the current ImprovementCore entrypoint with HF2 enabled.

Episode 1:
- regime: COMPLETE
- HF2: RELATIVE_CLOSE
- HF2 rounds: 2
- blocker: none
- selected next candidate: IC-TRACE-EXPORT

Episode 2:
- regime: COMPLETE
- HF2: RELATIVE_CLOSE
- HF2 rounds: 2
- blocker: none
- selected next candidate: IC-TRACE-EXPORT

Episode 3:
- regime: COMPLETE
- HF2: RELATIVE_CLOSE
- HF2 rounds: 2
- blocker: none
- selected next candidate: IC-TRACE-EXPORT

Episode 4:
- regime: COMPLETE
- HF2: RELATIVE_CLOSE
- HF2 rounds: 2
- blocker: none
- selected next candidate: IC-TRACE-EXPORT

Selected sequence:

IC-TRACE-EXPORT
-> IC-TRACE-EXPORT
-> IC-TRACE-EXPORT
-> IC-TRACE-EXPORT

Convergence: TRUE.

## ImprovementCore recommendation

Test IC-TRACE-EXPORT first.

Reason returned by ImprovementCore:

"uses already-existing receipts, adds observability without changing controller semantics, and has the lowest coupling among identified strict-gain candidates"

Architecture decision returned in every episode:

"No new master controller or memory layer. Keep checkpointing distinct from learning memory. Test trace export first; keep larger runtime changes OPEN."

## Verification

Every episode verified:
- all configured tools retained full 36-cell binding;
- configured tool execution evidence was present;
- the core files were present;
- no structured handoff was loaded;
- the selected candidate did not depend on a handoff;
- trace export can reuse existing receipts;
- execution checkpointing was not conflated with learning memory.

Take-5 Validation: SUCCESS.
Capability Preservation: SUCCESS.
Campaign workflow: SUCCESS.

## Material interpretation

The earlier IC-HOST-CAPABILITY-DISCOVERY recommendation was produced in a run where an older structured handoff supplied that candidate as the uniquely strongest upstream signal.

When the user requested a minimally instructed run and that structured handoff was removed as a selection signal, four repeated ImprovementCore+HF2 episodes independently converged on IC-TRACE-EXPORT instead.

This does not invalidate host-capability discovery. It changes its current priority under the minimally instructed evidence basis.

## Current disposition

IC-TRACE-EXPORT: recommended next strict-gain experiment.
IC-HOST-CAPABILITY-DISCOVERY: remains OPEN.
IC-DURABLE-RUN-JOURNAL: remains OPEN_DESIGN_REQUIRED.
IC-RUNTIME-LIFECYCLE-FAILURE-SEMANTICS: remains OPEN_DESIGN_REQUIRED.

No larger architecture change is admitted by this campaign.
