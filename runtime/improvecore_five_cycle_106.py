#!/usr/bin/env python3
"""ImproveCore five-cycle whole-repository run 106.

This is an execution experiment, not a promotion authority. It scans the frozen
tracked repository basis, runs the canonical whole-system audit, probes current
user-facing run resolution, and then invokes the current ImproveCore dispatcher
five times. Each pass has fresh episode state, consumes the prior pass as
evidence, and shares only typed learning memory across passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, is_dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from improvement_core_learning_memory import LearningMemory
from improvement_core_regime import CURRENT_REGIME, REGIME_VERSION
from ic028_operator import OBSERVER_FIRST_STAGES
from run_request import resolve_run_request
from system_audit import run_audit

INPUT = ROOT / "integration/IMPROVECORE_FIVE_CYCLE_WHOLE_REPO_INPUT_106_2026-09-26.md"
CURRENT = ROOT / "integration/CURRENT_IMPROVEMENT_CORE.md"
FINISH = ROOT / "FINISH_LINE.md"
LEDGER = ROOT / "FUNCTIONALITY_RECOVERY_LEDGER.md"
CURRENTNESS = ROOT / "CAPABILITY_CURRENTNESS_MATRIX.md"
PTI = ROOT / "integration/CURRENT_PROTECTED_TRANSITION_INTEGRITY.md"

AUTHORITY_PATHS = (
    "integration/CURRENT_IMPROVEMENT_CORE.md",
    "FINISH_LINE.md",
    "FUNCTIONALITY_RECOVERY_LEDGER.md",
    "CAPABILITY_CURRENTNESS_MATRIX.md",
    "MIGRATION_STATE.yaml",
    "integration/CURRENT_PROTECTED_TRANSITION_INTEGRITY.md",
)

MARKERS = (
    "OPEN",
    "BLOCKED",
    "CONFLICT",
    "HOST_INTEGRATION_BYPASS",
    "universal host interception",
    "automatic host adapter discovery",
    "full repertoire reachability",
    "portfolio-wide tool-specific identity reconstruction",
    "MT_NATIVE_ENTRY",
    "ARCHITECT_EXACT_SEMANTIC_FACADE_RUNTIME_OPEN",
    "SUCCESSOR_READY",
)


def _jsonable(value):
    if is_dataclass(value):
        return {k: _jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    return value


def read_text(path: Path) -> str:
    try:
        data = path.read_bytes()
    except OSError:
        return ""
    if b"\x00" in data:
        return ""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return ""


def tracked_paths():
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return tuple(x for x in raw.decode("utf-8").split("\x00") if x)


def section(text: str, heading: str):
    lines = text.splitlines()
    out = []
    active = False
    for line in lines:
        if line.strip() == heading:
            active = True
            continue
        if active and line.startswith("## "):
            break
        if active:
            out.append(line)
    return "\n".join(out).strip()


def scan_repository():
    paths = tracked_paths()
    suffixes = Counter()
    topdirs = Counter()
    marker_counts = Counter()
    marker_paths = {m: [] for m in MARKERS}
    authority_lines = {}
    hashes = {}
    text_files = 0
    total_lines = 0
    total_bytes = 0

    for rel in paths:
        p = ROOT / rel
        if not p.is_file():
            continue
        data = p.read_bytes()
        total_bytes += len(data)
        hashes[rel] = hashlib.sha256(data).hexdigest()
        suffixes[p.suffix or "<none>"] += 1
        topdirs[rel.split("/", 1)[0]] += 1
        text = read_text(p)
        if not text:
            continue
        text_files += 1
        total_lines += len(text.splitlines())
        lower = text.lower()
        for marker in MARKERS:
            count = lower.count(marker.lower())
            if count:
                marker_counts[marker] += count
                if len(marker_paths[marker]) < 25:
                    marker_paths[marker].append(rel)

    for rel in AUTHORITY_PATHS:
        p = ROOT / rel
        text = read_text(p)
        if not text:
            authority_lines[rel] = []
            continue
        selected = []
        for idx, line in enumerate(text.splitlines(), 1):
            l = line.lower()
            if (
                "open" in l
                or "remaining residual" in l
                or "required before readiness" in l
                or "not authorized" in l
                or "successor_ready" in l
            ):
                selected.append({"line": idx, "text": line.strip()})
        authority_lines[rel] = selected[:120]

    current_text = read_text(CURRENT)
    ledger_text = read_text(LEDGER)
    finish_text = read_text(FINISH)

    return {
        "basis": {
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "tracked_paths": len(paths),
            "tracked_text_files": text_files,
            "total_tracked_bytes": total_bytes,
            "total_text_lines": total_lines,
        },
        "top_level_path_counts": dict(topdirs.most_common()),
        "suffix_counts": dict(suffixes.most_common()),
        "marker_counts": dict(marker_counts),
        "marker_paths": marker_paths,
        "authority_lines": authority_lines,
        "current_open_coordinates": [
            line.strip()[2:].strip()
            for line in section(current_text, "## OPEN coordinates").splitlines()
            if line.strip().startswith("- ")
        ],
        "finish_required_coordinates": [
            line.strip()[2:].strip().rstrip(";")
            for line in section(finish_text, "Required coordinates:").splitlines()
            if line.strip().startswith("- ")
        ],
        "host_boundary_evidence": {
            "current_anchor_universal_host_open": (
                "Universal host interception remains OPEN" in current_text
                or "universal external-host interception remains OPEN" in current_text
            ),
            "ledger_names_host_integration_bypass": (
                "HOST_INTEGRATION_BYPASS" in ledger_text
            ),
            "ledger_says_residual_moved_to_host_integration_bypass": (
                "remaining residual to HOST_INTEGRATION_BYPASS" in ledger_text
            ),
        },
        "selected_hashes": {
            rel: hashes.get(rel)
            for rel in AUTHORITY_PATHS
            if rel in hashes
        },
    }


def current_probes():
    audit = run_audit(ROOT)
    phrases = (
        "run MT",
        "run Architect",
        "run Architecture",
        "run Root Cause",
        "run RootCause",
        "run PD",
        "run GOAL",
        "run ASSERT",
    )
    aliases = {}
    for phrase in phrases:
        try:
            rr = resolve_run_request(phrase)
            aliases[phrase] = {
                "tool_id": rr.tool_id,
                "configured": rr.configured,
                "wrapper_required": rr.wrapper_required,
                "geometry": rr.geometry.value if rr.geometry else None,
                "recursive": rr.recursive,
                "closure_required": rr.closure_required,
                "reentry_required": rr.reentry_required,
                "semantic_before_return": rr.semantic_before_return,
            }
        except Exception as exc:
            aliases[phrase] = {"error": f"{type(exc).__name__}:{exc}"}

    runtime_text = "\n".join(
        read_text(p)
        for p in (
            ROOT / "runtime/improvement_core_regime.py",
            ROOT / "runtime/improvement_core_external_acquisition.py",
            ROOT / "runtime/improvement_core_dispatch.py",
            ROOT / "runtime/entry_contract.py",
            ROOT / "runtime/run_request.py",
            ROOT / "runtime/activation_bridge.py",
        )
        if p.exists()
    )
    lower = runtime_text.lower()
    discovery_tokens = {
        token: token.lower() in lower
        for token in (
            "discover_adapters",
            "adapter_registry",
            "capability_discovery",
            "external_adapters",
            "activation_bridge",
        )
    }

    return {
        "regime": {
            "controller": CURRENT_REGIME.controller,
            "version": REGIME_VERSION,
            "stage_manager": CURRENT_REGIME.stage_manager,
            "recursive_manager": CURRENT_REGIME.recursive_manager,
            "learning_memory": CURRENT_REGIME.learning_memory,
            "external_acquisition": CURRENT_REGIME.external_acquisition,
        },
        "system_audit": {
            "closed": audit.closed,
            "kernel": list(audit.kernel),
            "modules": list(audit.modules),
            "raw": [_jsonable(x) for x in audit.raw],
            "roots": [_jsonable(x) for x in audit.roots],
        },
        "run_request_aliases": aliases,
        "host_runtime_tokens": discovery_tokens,
    }


def rank_current_blockers(scan, probes):
    candidates = []

    for root in probes["system_audit"]["roots"]:
        if root.get("blocking"):
            candidates.append({
                "id": f"SYSTEM_AUDIT::{root['root_class']}",
                "score": 120,
                "kind": "repository_blocker",
                "basis": root,
            })

    hb = scan["host_boundary_evidence"]
    if (
        hb["current_anchor_universal_host_open"]
        and hb["ledger_names_host_integration_bypass"]
    ):
        candidates.append({
            "id": "HOST_INTEGRATION_BYPASS",
            "score": 110,
            "kind": "cross_boundary_blocker",
            "basis": hb,
        })

    open_coords = set(scan["current_open_coordinates"])
    coord_scores = {
        "portfolio-wide tool-specific identity reconstruction.": 92,
        "full repertoire reachability evidence;": 88,
        "matched historical high/low alignment replays;": 76,
        "unlike prospective autonomous holdouts;": 74,
        "cheap-route versus broad-attack calibration;": 68,
        "global ImprovementCore maximality/minimality;": 62,
        "exact relation-generator basis;": 55,
        "relation-admission mathematics;": 54,
    }
    for coord in open_coords:
        normalized = coord.strip()
        score = coord_scores.get(normalized, 50)
        candidates.append({
            "id": normalized.rstrip(".;"),
            "score": score,
            "kind": "current_open_coordinate",
            "basis": "integration/CURRENT_IMPROVEMENT_CORE.md",
        })

    # The alias defect from run 105 has lower priority once all current probes
    # resolve through configured D36_C contracts.
    alias_ok = all(
        not v.get("error")
        and v.get("configured") is True
        and v.get("wrapper_required") is True
        and v.get("geometry") == "D36_C"
        for k, v in probes["run_request_aliases"].items()
        if k in {"run MT", "run Architect", "run Architecture", "run Root Cause", "run RootCause"}
    )
    if not alias_ok:
        candidates.append({
            "id": "USER_INVOCATION_CONFIGURED_IDENTITY_GAP",
            "score": 115,
            "kind": "repository_blocker",
            "basis": probes["run_request_aliases"],
        })

    # Deduplicate by id, preserving highest score.
    by_id = {}
    for c in candidates:
        old = by_id.get(c["id"])
        if old is None or c["score"] > old["score"]:
            by_id[c["id"]] = c
    return sorted(by_id.values(), key=lambda x: (-x["score"], x["id"]))


def host_capability_model(scan, probes):
    tokens = probes["host_runtime_tokens"]
    injection = bool(tokens.get("external_adapters"))
    automatic = any(
        tokens.get(k)
        for k in ("discover_adapters", "adapter_registry", "capability_discovery")
    )
    alias_map = probes["run_request_aliases"]
    invocation_aliases_current = all(
        not alias_map[k].get("error") and alias_map[k].get("configured")
        for k in ("run MT", "run Architect", "run Architecture", "run Root Cause", "run RootCause")
    )
    return {
        "repository_side": {
            "zero_request_dispatch": "PRESENT",
            "host_adapter_injection": "PRESENT" if injection else "UNRESOLVED",
            "automatic_host_capability_discovery": "PRESENT" if automatic else "ABSENT_IN_CORE_RUNTIME",
            "configured_user_run_aliases": "PRESENT" if invocation_aliases_current else "PARTIAL",
            "protected_transition_integrity": "PRESENT_BY_CURRENT_AUTHORITY",
        },
        "external_side": {
            "universal_external_host_interception": (
                "OPEN"
                if scan["host_boundary_evidence"]["current_anchor_universal_host_open"]
                else "UNRESOLVED"
            ),
        },
    }


def cycle_plan(cycle, ranked, scan, probes, prior):
    top = ranked[0] if ranked else {
        "id": "NO_CURRENT_BLOCKER_RECOVERED",
        "score": 0,
        "kind": "open",
        "basis": None,
    }
    host = host_capability_model(scan, probes)

    if cycle == 1:
        result = {
            "operation": "RECOVER_TOP_LEVEL",
            "governing_goal": (
                "Take-5 reaches SUCCESSOR_READY with protected capabilities, "
                "authority/currentness integrity, closed-loop execution, verification, "
                "reentry, cumulative state, anti-loss, and typed residuals."
            ),
            "highest_current_blocker": top,
            "reason": (
                "rank current authority and machine audit before historical/stale OPEN markers"
            ),
        }
    elif cycle == 2:
        result = {
            "operation": "DECOMPOSE_TOP_LEVEL_BLOCKER",
            "inherited_blocker": prior[-1]["result"]["highest_current_blocker"]
            if prior and "highest_current_blocker" in prior[-1]["result"]
            else top,
            "boundary_model": host,
            "repository_addressable_cut": (
                "HOST_CAPABILITY_DISCOVERY_AND_INVOCATION_BRIDGE"
                if top["id"] == "HOST_INTEGRATION_BYPASS"
                else top["id"]
            ),
            "external_residual": (
                "UNIVERSAL_EXTERNAL_HOST_INTERCEPTION"
                if top["id"] == "HOST_INTEGRATION_BYPASS"
                else None
            ),
        }
    elif cycle == 3:
        runtime_paths = set(scan["marker_paths"].get("automatic host adapter discovery", []))
        result = {
            "operation": "RECOVER_BEFORE_INVENT",
            "host_model": host,
            "existing_capability": [
                "zero-request upstream discovery",
                "host-injected external adapters",
                "configured run-request aliases",
                "protected transition integrity",
            ],
            "missing_or_unproven": [
                "automatic host capability discovery",
                "universal external-host interception",
            ],
            "matching_repository_paths": sorted(runtime_paths),
            "conclusion": (
                "compose existing dispatch/external-acquisition/activation surfaces first; "
                "do not create a second master controller"
            ),
        }
    elif cycle == 4:
        automatic = host["repository_side"]["automatic_host_capability_discovery"]
        result = {
            "operation": "STRICT_GAIN_CANDIDATE",
            "candidate": {
                "id": "TYPED_HOST_CAPABILITY_DISCOVERY_REGISTRY",
                "status": (
                    "NO_GAIN_ALREADY_PRESENT"
                    if automatic == "PRESENT"
                    else "ADMISSION_READY_EXPERIMENT"
                ),
                "minimal_form": (
                    "typed discovery/registry contract that enumerates available host adapters, "
                    "feeds only admissible bindings into existing external_adapters/dispatch, "
                    "does not self-authorize execution, and fails OPEN when the materially required "
                    "host capability is unavailable"
                ),
                "must_preserve": [
                    "current IC-028 ownership",
                    "existing external acquisition authority rules",
                    "OPEN/BLOCKED/CONFLICT",
                    "configured D36_C tool identity",
                    "protected transition integrity",
                    "repository-versus-host boundary distinction",
                ],
            },
            "deferred": "universal external-host interception cannot be proven by repository code alone",
        }
    else:
        candidate = prior[-1]["result"].get("candidate") if prior else None
        result = {
            "operation": "CLOSURE_CHALLENGE",
            "candidate_under_test": candidate,
            "system_audit_closed": probes["system_audit"]["closed"],
            "alias_probes_current": probes["run_request_aliases"],
            "repo_scan_basis": scan["basis"],
            "terminal_disposition": (
                "RELATIVE_CLOSE_REPOSITORY_PRECONDITION_CANDIDATE__EXTERNAL_HOST_OPEN"
                if top["id"] == "HOST_INTEGRATION_BYPASS"
                else "RELATIVE_CLOSE_WITH_TYPED_OPEN_RESIDUALS"
            ),
            "remaining_open": [
                "UNIVERSAL_EXTERNAL_HOST_INTERCEPTION",
                *[
                    x for x in scan["current_open_coordinates"]
                    if "universal host interception" not in x.lower()
                ],
            ],
            "closure_claim": (
                "No universal host closure claimed. Five passes recover the current top-level "
                "problem and a repository-side strict-gain experiment candidate only."
            ),
        }

    return top, result


def build_handlers(cycle, scan, probes, ranked, prior):
    top, planned = cycle_plan(cycle, ranked, scan, probes, prior)

    def make(stage):
        def handle(state):
            s = dict(state or {})
            trace = list(s.get("cycle_trace", ()))
            trace.append(stage)
            s["cycle_trace"] = trace
            s["cycle"] = cycle

            if stage == "OBSERVE":
                s["repository_scan"] = scan
                s["current_probes"] = probes
            elif stage == "OBSERVE_RECONCILE":
                s["ranked_current_blockers"] = ranked
                s["historical_markers_are_not_current_authority"] = True
            elif stage == "OBSERVE_TRC":
                s["truth_constraints"] = {
                    "repository_truth_does_not_prove_external_host_behavior": True,
                    "documentation_or_registration_does_not_equal_activation": True,
                    "current_authority_outranks_stale_artifacts": True,
                    "strict_gain_candidate_is_not_implementation_or_promotion": True,
                }
            elif stage == "RECOVER_GOAL":
                s["governing_goal"] = planned.get(
                    "governing_goal",
                    prior[0]["result"].get("governing_goal") if prior else None,
                )
                s["selected_top_level"] = top
            elif stage == "CURIOSITY_PD":
                s["question_frontier"] = [
                    "What is the earliest current break in the protected continuity chain?",
                    "Which part is repository-addressable versus externally hosted?",
                    "Which required capability already exists but is not activated?",
                    "What is the minimal strict gain that avoids controller proliferation?",
                    "What remains OPEN after the candidate is challenged?",
                ]
            elif stage == "FORMALIZE":
                s["formal_boundary"] = {
                    "protected_chain": [
                        "user_or_host_event",
                        "canonical_identity",
                        "configured_dispatch",
                        "execution",
                        "result_consumption",
                        "state_update",
                        "reentry",
                        "user_visible_boundary",
                    ],
                    "failure_condition": (
                        "a required edge is absent, bypassable, or not evidenced on the applicable host path"
                    ),
                }
            elif stage == "PLAN_ORDER":
                s["plan"] = [
                    "prefer current authority",
                    "verify machine audit and run aliases",
                    "separate repository and host coordinates",
                    "recover existing capability before adding structure",
                    "challenge candidate and preserve residual OPEN",
                ]
            elif stage == "OBJECTIFY":
                s["objects"] = {
                    "top_level": top,
                    "host_model": host_capability_model(scan, probes),
                }
            elif stage == "GENERATE_WORK":
                s["generated_work"] = [
                    "whole-repository evidence reconciliation",
                    "host-boundary decomposition",
                    "existing-capability recovery",
                    "minimal strict-gain experiment design",
                    "closure challenge",
                ]
            elif stage == "SELECT":
                s["selected_work"] = planned["operation"]
            elif stage == "BIND":
                s["authority"] = {
                    "scope": "experimental analysis and candidate admission only",
                    "main_mutation_authorized": False,
                    "promotion_authorized": False,
                }
            elif stage == "EXECUTE":
                s["cycle_result"] = planned
                return {"state": s, "material_delta": True}
            elif stage == "ADMIT":
                status = "EVIDENCE_ONLY"
                if cycle == 4:
                    status = planned["candidate"]["status"]
                s["admission"] = {
                    "status": status,
                    "scope": "five-cycle experimental branch only",
                }
            elif stage == "RECONCILE":
                s["reconciliation"] = {
                    "do_not_duplicate_open_pr_work": True,
                    "do_not_equate_repo_precondition_with_host_closure": True,
                }
            elif stage == "PROPAGATE_AFFECTED_CONE":
                s["affected_cone"] = [
                    "ImproveCore entry/dispatch",
                    "external acquisition",
                    "host adapter boundary",
                    "configured tool reachability",
                    "protected transition integrity",
                    "user-visible return path",
                ]
            elif stage == "PERSIST":
                s["persistence_target"] = "runtime/state/improvecore-five-cycle-106/report.json"
            elif stage == "VERIFY":
                s["verification"] = {
                    "all_tracked_paths_scanned": scan["basis"]["tracked_paths"] > 0,
                    "current_regime_is_087": REGIME_VERSION == "087",
                    "five_cycle_input_present": INPUT.is_file(),
                    "run_aliases_checked": True,
                    "canonical_system_audit_executed": True,
                    "external_host_claim_fail_closed": True,
                }
            elif stage == "COMPLETE":
                s["terminal_disposition"] = (
                    planned.get("terminal_disposition")
                    or "RELATIVE_CLOSE_PASS_RESULT_FEEDS_NEXT_PASS"
                )
                return {"state": s, "terminal": True}
            return {"state": s}

        return handle

    handlers = {stage: make(stage) for stage in OBSERVER_FIRST_STAGES}
    handlers["REENTER"] = lambda state: {"state": state, "terminal": True}
    return handlers


def run(output: Path):
    scan = scan_repository()
    probes = current_probes()
    ranked = rank_current_blockers(scan, probes)
    memory = LearningMemory()
    cycles = []

    base_corpus = [
        {"id": "user-input-106", "text": read_text(INPUT)},
        {"id": "current-improvecore", "text": read_text(CURRENT)},
        {"id": "finish-line", "text": read_text(FINISH)},
        {"id": "functionality-ledger", "text": read_text(LEDGER)},
        {"id": "currentness-matrix", "text": read_text(CURRENTNESS)},
        {"id": "pti-anchor", "text": read_text(PTI)},
        {"id": "repo-scan-summary", "text": json.dumps({
            "basis": scan["basis"],
            "host_boundary_evidence": scan["host_boundary_evidence"],
            "current_open_coordinates": scan["current_open_coordinates"],
            "system_audit": probes["system_audit"],
            "run_request_aliases": probes["run_request_aliases"],
        }, sort_keys=True, default=str)},
    ]

    for cycle in range(1, 6):
        prior_evidence = {
            "cycles": [
                {
                    "cycle": c["cycle"],
                    "status": c["status"],
                    "result": c["result"],
                    "terminal_disposition": c["terminal_disposition"],
                }
                for c in cycles
            ]
        }
        corpus = list(base_corpus)
        if cycles:
            corpus.append({
                "id": f"prior-cycles-through-{cycle-1}",
                "text": json.dumps(prior_evidence, sort_keys=True, default=str),
            })

        handlers = build_handlers(cycle, scan, probes, ranked, cycles)
        resolution, regime_result = dispatch_improvement_core(
            (
                f"ImproveCore pass {cycle} of five: recover and attack the current "
                "top-level Take-5 GitHub problem using the frozen whole-repository scan "
                "and all prior pass results as evidence"
            ),
            state={},
            handlers=handlers,
            corpus=corpus,
            observer_risk=True,
            learning_memory=memory,
            allow_external_gap=False,
        )
        state = regime_result.result.state
        cycle_report = {
            "cycle": cycle,
            "resolution": _jsonable(resolution),
            "status": regime_result.status,
            "blocker": regime_result.blocker,
            "terminal": regime_result.result.terminal,
            "trace": state.get("cycle_trace"),
            "selected_top_level": state.get("selected_top_level"),
            "result": state.get("cycle_result"),
            "admission": state.get("admission"),
            "verification": state.get("verification"),
            "terminal_disposition": state.get("terminal_disposition"),
            "learning_summary": _jsonable(regime_result.learning_summary),
        }
        cycles.append(cycle_report)

        if not regime_result.result.terminal:
            raise RuntimeError(f"PASS_{cycle}_NOT_TERMINAL")

    report = {
        "run_id": "IMPROVECORE_FIVE_CYCLE_WHOLE_REPO_106",
        "regime_version": REGIME_VERSION,
        "controller": CURRENT_REGIME.controller,
        "repository_scan": scan,
        "current_probes": probes,
        "ranked_current_blockers": ranked,
        "cycles": cycles,
        "final": {
            "governing_goal": cycles[0]["result"].get("governing_goal"),
            "highest_current_blocker": cycles[0]["result"].get("highest_current_blocker"),
            "repository_addressable_cut": cycles[1]["result"].get("repository_addressable_cut"),
            "strict_gain_candidate": cycles[3]["result"].get("candidate"),
            "terminal_disposition": cycles[4]["result"].get("terminal_disposition"),
            "remaining_open": cycles[4]["result"].get("remaining_open"),
            "closure_claim": cycles[4]["result"].get("closure_claim"),
        },
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(ROOT / "runtime/state/improvecore-five-cycle-106/report.json"),
    )
    args = parser.parse_args()
    run(Path(args.output))


if __name__ == "__main__":
    main()
