# ImprovementCore External Acquisition 090

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE
Target: current ImprovementCore regime

## Defect

ImprovementCore could detect external dependence but still route the job through
internal capabilities.  The router had no first-class action for:

- live internet search;
- connected/private source lookup;
- repository research/provenance retrieval;
- outside execution tools;
- explicit refusal to brute-force internally when the outside capability is unavailable.

This made the controller systematically prefer internal reconstruction even when
the missing information existed outside the current state.

## Governing repair

External acquisition is now a first-class preflight of the current regime.

For state Z and available outside capability set E:

ExternalDecision(Z,E)
in
{NOT_NEEDED, ACQUIRE, OPEN_GAP}.

ACQUIRE is selected when:

1. a material external-information/tool signal is live;
2. at least one host-bound outside adapter is available;
3. expected uncertainty/cost reduction exceeds acquisition cost.

OPEN_GAP is selected when outside acquisition is materially required but no
adequate adapter is available and gap preservation is allowed.

The controller does not silently replace OPEN_GAP with expensive internal
guessing.

## External capability classes

Host adapters are intentionally abstract so repository code does not pretend it
owns internet or connector execution.

Preferred classes:

1. connected_sources
2. repository_research
3. web_search
4. external_tools

The priority list is only a default.  The first adapter that certifies the need
satisfied stops further acquisition.  This prevents tool-smash.

## Expected-value rule

The current compact policy uses:

EV_external
=
uncertainty_reduction
+
internal_cost_avoided
-
external_acquisition_cost.

When the external need is live and EV_external > 0, ACQUIRE is preferred.

This is deliberately compatible with later richer cost models for latency,
privacy, money, trust, and context load.

## Signals

Current first-class signals include:

- external_dependency
- currentness_unknown
- fresh_information_required
- outside_evidence_required
- prior_art_required
- literature_required
- research_needed
- external_tool_candidate
- tool_gap
- unknown_external_fact

Relevant tags such as external_dependency, novelty, prior_art, stale_version,
and currentness also activate the preflight.

## Gap law

The user's requested behavior is explicit:

outside capability required
+
outside capability unavailable
=>
OPEN_GAP

not

outside capability required
+
outside capability unavailable
=>
brute-force internal reconstruction
=>
false completion.

Internal fallback remains possible only when the route explicitly licenses it.

## Host boundary

Repository code cannot itself create internet access, plugin access, or private
connector access.

The host binds adapters.

Therefore:

semantic/runtime policy = implemented here;
actual outside capability availability = host-relative.

This gap remains explicit rather than hidden.

## External trust boundary

Outside outputs are evidence, not authority.

They enter the normal ImprovementCore admission, reconciliation, verification,
currentness, HF1/HF2, and persistence path.

No web page, connector result, or outside tool output self-promotes into
authoritative state.

## Research comparison

The repair is consistent with external tool-using-agent practice:

- attach search when current information is needed rather than relying on model memory;
- make overlapping tool decision rules explicit;
- avoid exposing or invoking every tool blindly;
- retrieve a task-specific toolchain when large tool inventories would overload context;
- use cost-aware stopping rather than treating relevance ranking as an obligation to keep acquiring.

These comparisons motivate the routing form but do not define repository authority.

## Protected behaviors

- external need is detectable before substantive internal work;
- available outside capability can be invoked before the manager;
- outside evidence is visible to manager stages;
- unavailable required capability leaves OPEN;
- ordinary jobs with no external signal do not pay the acquisition cost;
- adapter success can stop additional outside calls;
- host-relative availability is not misrepresented as repository-owned execution.

## Current files

- runtime/improvement_core_external_acquisition.py
- runtime/improvement_core_regime.py
- runtime/improvement_core_dispatch.py
- tests/test_improvement_core_external_acquisition.py
- architecture/IMPROVEMENT_CORE_RECOVERY_MANIFEST_082.json

## Remaining OPEN

- learned/calibrated cost model;
- automatic discovery of host tool inventory;
- trust/reliability scoring by source class;
- privacy-budget integration;
- dynamic plugin/MCP installation authority;
- empirical comparison against the prior internal-only strategy;
- universal host interception.
