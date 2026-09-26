# Capability and Currentness Preservation Matrix 002

Date: 2026-09-25
Status: CURRENT-BASIS WORKING MATRIX
Architecture basis: EWG-ARCH-001

| Protected behavior | Current realization | Status |
|---|---|---|
| architecture-first reflexive currentness | reflexive_currentness.py | implemented + tested |
| endogenous work generation/regeneration | endogenous_work.py + system_loop.py | implemented + tested |
| Improvement Core as policy/controller, not whole system | improvement_core.py inside system_loop.py | implemented + tested |
| JOB_CONDITIONED and ZERO_REQUEST distinction | endogenous_work.py | implemented + tested |
| OPEN/INCOMPARABLE preservation | endogenous_work.py + admission/controller guards | implemented + tested |
| claim lifecycle and evidence-bearing admission | research_system.py | implemented + tested |
| history reconstructibility/workflow faithfulness closure | research_system.py | implemented + tested |
| configured-run identity | configured_run.py + tool_run_registry.py | implemented + tested |
| compound ASSERT orchestration | assert_compound.py + tool_run_registry.py | implemented + validated in PR #22 |
| recursive closure/reentry | recursive_episode.py + HF/TRC | implemented + tested |
| K_PD projection/obligation exposure | kpd_projection.py | implemented + tested |
| mode cube breadth x direction x coupling | mode_selector.py | implemented + tested |
| Reconciler / Discriminator / Delegated Executor | mode_centers.py | implemented + tested |
| activation truth | activation_bridge.py + controller_episode.py | implemented + tested |
| bounded delegation/authority preservation | delegation.py | implemented + tested |
| persistent lineage | lineage_state.py | implemented + tested |
| emergent load-bearing object admission | emergent_admission.py | implemented + tested |
| capability generation without self-authorization | capability_foundry.py + admission guards | implemented + tested |
| C01-C49 runtime binding | a5_programs.py + capability_runtime.py | implemented + all-C execution test |
| C01-C49 configured-run identity | tool_run_registry.py | implemented + tested |
| B01-B58 semantic coverage | A5/GDOS crosswalk evidence | reconstructed; not equated with execution |
| CAP001-CAP033 historical preservation | HISTORICAL_RECONSTRUCTION_WITNESSES_015.md | compositional evidence; claim remains scoped |
| unfamiliar prospective holdout | test_unfamiliar_holdout.py | implemented + tested |
| currentness audit revalidation | currentness_audit.py | implemented + tested |
| takeover runtime independence | foundation_snapshot.py + takeover test | implemented + tested |
| migration/promotion | independent authority boundary | NOT AUTHORIZED |

## Currentness law

Component CURRENT is not meaningful until the architecture basis is current.

Architecture-first order:
A_latest -> compare A_built -> propagate material role/ownership/closure deltas -> component audit -> dependent revalidation.

## Evidence discipline

Specified != executable.
Semantic coverage != activation.
Activation != historical reconstruction.
Passing regression != global closure.
Historical compositional reconstruction is not universal equivalence.

## Supersession note

Matrix 001 is superseded because it predated C20-C48 bindings, prospective holdout, persistent lineage, emergent admission, configured-run identity, the mode cube, and EWG-ARCH-001.


## 2026-09-25 ICC-128 closure delta

Validated and merged through PR #24. Validation run 36203721183 concluded SUCCESS:
- common typed protected state commit contract: implemented;
- SYSTEM_CONTROL mutation/discharge gate: implemented;
- persistent LINEAGE commit gate: implemented;
- ADMITTED RESEARCH_CONTROL gate: implemented;
- SUPERVISORY admitted-delta gate: implemented;
- RESULT commit gate in math-first wrapper: implemented;
- unique default RESULT path registry: implemented;
- pre-math object hypothesis recovery: implemented.

These rows are implemented + tested on the validated PR head and merged to main.
