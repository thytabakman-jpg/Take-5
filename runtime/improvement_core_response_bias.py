"""Response-preference and bias-control surface for governed ImprovementCore runs.

This module separates response preference from truth authority.  Preferences control
projection and interaction style; they cannot promote a claim, force closure, or
override execution/currentness evidence.

Bias findings are typed as operating risks, not claims about a person's character.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResponsePreferenceProfile:
    profile_id:str
    protected_behaviors:tuple[str,...]
    anti_behaviors:tuple[str,...]


@dataclass(frozen=True)
class BiasAuditReceipt:
    system_risks:tuple[str,...]
    input_framing_risks:tuple[str,...]
    corrections:tuple[str,...]


CURRENT_RESPONSE_PROFILE=ResponsePreferenceProfile(
    profile_id="TZVI-IMPROVECORE-RESPONSE-001",
    protected_behaviors=(
        "RESULT_FIRST",
        "REPORT_ACTUAL_ACTIONS_NOT_INTENTIONS",
        "CONTROLLER_OWNS_INTERNAL_SEQUENCE_AFTER_REQUIRED_ENTRY_STEPS",
        "REGENERATE_AFTER_MATERIAL_DELTA",
        "PERSIST_MATERIAL_RESULTS_BEFORE_CLOSURE",
        "DISTINGUISH_EXECUTED_FROM_ANALYZED",
        "KEEP_OPEN_blocked_conflict_VISIBLE",
        "USE_EXACT_CURRENT_OBJECT_IDENTITY",
        "CONCISE_RELEASE_OF_MATERIAL_RESULTS",
    ),
    anti_behaviors=(
        "HOST_AUTHORED_FIXED_TOOL_CHOREOGRAPHY",
        "PROCESS_DUMP_WITHOUT_RESULT",
        "SEMANTIC_ONLY_TOOL_INVOCATION",
        "MANUAL_CONTINUATION_WHEN_CONTROLLER_HAS_LIVE_WORK",
        "FALSE_CLOSURE",
        "PREFERENCE_AS_EVIDENCE_OF_FACT",
    ),
)


SYSTEM_BIAS_GUARDS=(
    "HOST_SUBSTITUTION_BIAS",
    "FAMILIAR_TOOL_SELECTION_BIAS",
    "RECENCY_CURRENTNESS_BIAS",
    "ACTION_AND_CLOSURE_BIAS",
    "ARCHITECTURE_PRESERVATION_BIAS",
    "TOOL_SALIENCE_BIAS",
    "GOAL_LEAKAGE",
    "SELF_AUDIT_EXPRESSIVITY_BIAS",
    "INTERNAL_BRUTE_FORCE_BIAS",
)


def scan_bias_risks(user_text:str, state:Any=None)->BiasAuditReceipt:
    """Return bias-sensitive coordinates and the correction that governs them.

    Input findings describe pressure in the current framing.  They do not diagnose
    stable cognitive traits of the user.
    """
    t=" ".join(str(user_text).lower().split())
    input_risks=[]
    if any(x in t for x in ("every single","everything","solve all","all of my projects")):
        input_risks.append("CLOSURE_SCOPE_PRESSURE")
    if any(x in t for x in ("six different","6 different","six markdown","6 markdown")):
        input_risks.append("REMEMBERED_NUMERIC_ANCHOR")
    if "first" in t and "then" in t:
        input_risks.append("SEQUENCE_ANCHOR_AFTER_EXPLICITLY_REQUIRED_PREFIX")
    if any(x in t for x in ("create a tool","wanted to create a tool","make a tool")):
        input_risks.append("SOLUTION_FORM_ANCHOR")
    if any(x in t for x in ("always","forever","every time")):
        input_risks.append("UNIVERSALITY_PRESSURE")

    corrections=(
        "TREAT_USER_FRAMING_AS_EVIDENCE_EXCEPT_EXPLICIT_REQUIRED_PREFIX",
        "OBSERVER_BEFORE_GOAL_CONDITIONED_COMPRESSION_WHEN_REPRESENTATION_RISK_EXISTS",
        "CHECK_CURRENT_REPOSITORY_AND_LINEAGE_BEFORE_MEMORY",
        "GENERATE_RIVAL_FRAMINGS_AND_TEST_RESULT_SENSITIVITY",
        "SEPARATE_USER_PREFERENCE_FROM_TRUTH_AUTHORITY",
        "PRESERVE_TYPED_OPEN_BLOCKED_CONFLICT",
        "PREFER_EXTERNAL_OR_EXISTING_CAPABILITY_BEFORE_BRUTE_FORCE_REBUILD",
        "RESELECT_AFTER_MATERIAL_DELTA",
    )
    return BiasAuditReceipt(
        system_risks=SYSTEM_BIAS_GUARDS,
        input_framing_risks=tuple(input_risks),
        corrections=corrections,
    )


def response_release_contract()->dict:
    return {
        "profile_id":CURRENT_RESPONSE_PROFILE.profile_id,
        "required":CURRENT_RESPONSE_PROFILE.protected_behaviors,
        "forbidden":CURRENT_RESPONSE_PROFILE.anti_behaviors,
        "truth_precedence":"EVIDENCE_AND_TYPED_STATUS_OVERRIDES_STYLE_PREFERENCE",
    }
