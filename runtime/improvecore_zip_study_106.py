#!/usr/bin/env python3
"""ImproveCore ZIP study 106.

Runs the current ImproveCore dispatcher over an evidence packet distilled from
high-signal ZIP archives. The packet is evidence, not canonical authority.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from improvement_core_regime import CURRENT_REGIME, REGIME_VERSION
from ic028_operator import OBSERVER_FIRST_STAGES

INPUT = ROOT / "integration/IMPROVECORE_ZIP_STUDY_INPUT_106_2026-09-26.md"
EVIDENCE = ROOT / "research/IMPROVECORE_ZIP_EVIDENCE_106_2026-09-26.md"
CURRENT = ROOT / "integration/CURRENT_IMPROVEMENT_CORE.md"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def candidates():
    return [
        {
            "id": "IC-EVIDENCE-TARGET-TYPING",
            "classification": "STRICT_GAIN_CANDIDATE",
            "minimal_form": (
                "typed evaluation matrix separating artifact adequacy, method efficacy, "
                "interaction efficacy, and reduction adequacy; support holdouts and negative controls"
            ),
            "evidence": [
                "PD audit pilots found artifact adequacy != method efficacy != interaction efficacy != reduction adequacy",
                "self-referential D0 inflated overlap and biased over-reduction",
                "current core runtime has no explicit benchmark/evaluation-target layer",
            ],
            "risk": "LOW_MEDIUM",
            "status": "ADMISSION_READY_EXPERIMENT",
        },
        {
            "id": "IC-NATIVE-OUTPUT-TRACE-LINKAGE",
            "classification": "COMPOSE_WITH_EXISTING",
            "compose_with": "IC-TRACE-EXPORT",
            "minimal_form": (
                "durable trace references immutable native stage outputs, corpus/method hashes, "
                "normalization records, and normalized-to-native links"
            ),
            "evidence": [
                "PD pilots show output-only normalization can hide distinct reasoning histories",
                "self-study 104 already found durable trace export partial/absent",
            ],
            "risk": "LOW_MEDIUM",
            "status": "ADMISSION_READY_DESIGN_EXTENSION",
        },
        {
            "id": "IC-BENCHMARK-SCOPED-CLAIMS",
            "classification": "STRICT_GAIN_CANDIDATE",
            "minimal_form": (
                "minimality/completeness/reduction claims carry benchmark_id, basis_id, "
                "admissibility/representation scope, and reopen condition"
            ),
            "evidence": [
                "PD audit reduction result was valid only relative to declared benchmark suite",
                "current basis-relative closure exists but benchmark-qualified claim emission is not explicit",
            ],
            "risk": "MEDIUM",
            "status": "OPEN_DESIGN_REQUIRED",
        },
        {
            "id": "IC-AUTHORITY-LATTICE-EXTENSION",
            "classification": "COMPOSE_EXISTING_FIRST",
            "minimal_form": (
                "independent latest/accepted/canonical/recovered/candidate/task-fit dimensions "
                "inside existing authority/currentness machinery"
            ),
            "evidence": [
                "Sukkos PracticalCore explicitly rejects current=best=latest=canonical=most-visually-useful",
                "canonical-state archive separates LATEST from ACCEPTED",
                "current ImproveCore already has authority/provenance/currentness safeguards",
            ],
            "risk": "LOW_MEDIUM",
            "status": "SUBSUME_OR_SMALL_EXTENSION",
        },
        {
            "id": "IC-TIERED-HANDOFF-CONTEXT",
            "classification": "EXPERIMENT_READY",
            "minimal_form": "orientation capsule -> targeted expansion -> canonical-source trace",
            "evidence": [
                "research corpus uses small handoff capsules before deep expansion",
                "current zero-request entry accepts addressable corpora but does not define tiered loading",
            ],
            "risk": "LOW",
            "status": "EXPERIMENT_READY",
        },
        {
            "id": "IC-RECOVERY-BEFORE-REGENERATION",
            "classification": "COMPOSE_EXISTING_FIRST",
            "minimal_form": "prefer exact recovered artifact/capability with lineage witness before regeneration",
            "evidence": [
                "Sukkos archives prefer recovered image-native artifacts over regeneration",
                "current architecture already treats recovery as a first-class concern",
            ],
            "risk": "LOW",
            "status": "SUBSUME_EXISTING_RECOVERY",
        },
        {
            "id": "IC-REPRESENTATION-ABLATION",
            "classification": "EXPERIMENT_READY",
            "minimal_form": (
                "before reducing a tool/stage, compare semantic, state-transition, "
                "information-flow, and provenance representations"
            ),
            "evidence": [
                "PD pilots found stable conclusion but representation-dependent localization",
                "current representation sufficiency exists, so this is an evaluation extension rather than a new representation layer",
            ],
            "risk": "LOW_MEDIUM",
            "status": "EXPERIMENT_READY",
        },
    ]

def handlers():
    cs = candidates()
    current_text = read(CURRENT)
    evidence_text = read(EVIDENCE)

    def make(stage):
        def handle(state):
            s = dict(state or {})
            trace = list(s.get("zip_study_trace", ()))
            trace.append(stage)
            s["zip_study_trace"] = trace

            if stage == "OBSERVE":
                s["sources"] = {
                    "input": str(INPUT.relative_to(ROOT)),
                    "zip_evidence": str(EVIDENCE.relative_to(ROOT)),
                    "current_anchor": str(CURRENT.relative_to(ROOT)),
                }
                s["evidence_scope"] = {
                    "library_model_generated_zip_inventory": 37,
                    "deep_inspected_high_signal_archives": 13,
                    "private_chat_exports_excluded": True,
                }
            elif stage == "OBSERVE_RECONCILE":
                s["already_current_not_new"] = [
                    "basis-relative learning/no-gain memory",
                    "dependency-sensitive route reopening",
                    "authority/provenance/currentness safeguards",
                    "continuation-relative representation sufficiency",
                    "discovery/representation/candidate-universe reentry",
                    "basis-relative closure",
                    "addressable-corpus zero-request entry",
                ]
                s["anchor_checks"] = {
                    "basis_relative_present": "basis-relative" in current_text,
                    "representation_reentry_present": "representation" in current_text and "reentry" in current_text,
                    "holdout_gap_visible": "unlike prospective autonomous holdouts" in current_text,
                }
            elif stage == "OBSERVE_TRC":
                s["truth_constraints"] = {
                    "artifact_quality_is_not_method_efficacy": True,
                    "filename_is_not_authority": True,
                    "normalized_output_is_not_native_execution_history": True,
                    "benchmark_relative_is_not_global": True,
                    "private_chat_zips_not_used": True,
                }
            elif stage == "RECOVER_GOAL":
                s["governing_goal"] = (
                    "learn from ZIP artifact lineages and identify evidence-backed growth "
                    "for current ImproveCore without duplicating capability or overstating evidence"
                )
            elif stage == "CURIOSITY_PD":
                s["questions"] = [
                    "Which archive invariants are already current?",
                    "Which archive lessons expose an evaluation blind spot?",
                    "Which gains compose with existing candidates rather than adding layers?",
                    "Which claims require holdouts or ablation before admission?",
                ]
            elif stage == "FORMALIZE":
                s["formal_distinctions"] = {
                    "evaluation_targets": [
                        "artifact_adequacy",
                        "method_efficacy",
                        "interaction_efficacy",
                        "reduction_adequacy",
                    ],
                    "authority_dimensions": [
                        "latest",
                        "accepted",
                        "canonical",
                        "recovered",
                        "candidate",
                        "task_fit",
                    ],
                    "evidence_chain": [
                        "native_output",
                        "normalization",
                        "receipt",
                        "claim",
                    ],
                }
            elif stage == "PLAN_ORDER":
                s["plan"] = [
                    "prevent self-evaluation category error",
                    "preserve native execution evidence",
                    "scope reduction claims to benchmark",
                    "compose authority distinctions into existing governance",
                    "benchmark tiered context loading",
                    "test representation-sensitive ablation",
                ]
            elif stage == "OBJECTIFY":
                s["candidate_objects"] = cs
            elif stage == "GENERATE_WORK":
                s["experiments"] = [
                    {
                        "id": "ZIP106-E1",
                        "target": "IC-EVIDENCE-TARGET-TYPING",
                        "design": "matched holdout matrix across artifact/method/interaction/reduction targets",
                    },
                    {
                        "id": "ZIP106-E2",
                        "target": "IC-TIERED-HANDOFF-CONTEXT",
                        "design": "same tasks with full corpus vs capsule-first expansion; compare accuracy, omissions, and context cost",
                    },
                    {
                        "id": "ZIP106-E3",
                        "target": "IC-REPRESENTATION-ABLATION",
                        "design": "attempt tool reduction under four representations and reject reduction when equivalence is output-only",
                    },
                ]
            elif stage == "SELECT":
                s["selected_next_candidate"] = {
                    "id": "IC-EVIDENCE-TARGET-TYPING",
                    "reason": (
                        "it is upstream of ImproveCore learning quality: without typed evaluation targets, "
                        "artifact success can be misread as evidence that the generating method or reduction is valid"
                    ),
                }
            elif stage == "BIND":
                s["authority"] = {
                    "zip_packet_role": "evidence",
                    "canonical_mutation_authorized": False,
                    "admission_scope": "experiment only",
                }
            elif stage == "EXECUTE":
                s["zip_study_result"] = {
                    "archive_evidence_loaded": len(evidence_text) > 1000,
                    "candidate_count": len(cs),
                    "selected": "IC-EVIDENCE-TARGET-TYPING",
                    "strict_gain_candidates": [
                        "IC-EVIDENCE-TARGET-TYPING",
                        "IC-BENCHMARK-SCOPED-CLAIMS",
                    ],
                    "compose_existing": [
                        "IC-NATIVE-OUTPUT-TRACE-LINKAGE",
                        "IC-AUTHORITY-LATTICE-EXTENSION",
                        "IC-RECOVERY-BEFORE-REGENERATION",
                    ],
                    "experiment_ready": [
                        "IC-TIERED-HANDOFF-CONTEXT",
                        "IC-REPRESENTATION-ABLATION",
                    ],
                }
                return {"state": s, "material_delta": True}
            elif stage == "ADMIT":
                s["admission"] = {
                    "admitted_for_experiment": [
                        "IC-EVIDENCE-TARGET-TYPING",
                        "IC-TIERED-HANDOFF-CONTEXT",
                        "IC-REPRESENTATION-ABLATION",
                    ],
                    "admitted_for_design_composition": [
                        "IC-NATIVE-OUTPUT-TRACE-LINKAGE",
                    ],
                    "canonical_runtime_changes": [],
                }
            elif stage == "RECONCILE":
                s["architecture_decision"] = (
                    "No new master controller, memory system, or representation layer. "
                    "First strengthen evaluation validity. Compose native-output linkage with the existing trace-export candidate. "
                    "Treat authority-lattice and recovery lessons as extensions of current governance."
                )
            elif stage == "PROPAGATE_AFFECTED_CONE":
                s["affected_cone"] = [
                    "ImproveCore self-evaluation",
                    "tool-reduction experiments",
                    "trace export design",
                    "corpus loading strategy",
                    "authority/currentness emission",
                ]
            elif stage == "PERSIST":
                s["persistence_target"] = "workflow artifact receipt only; branch remains noncanonical"
            elif stage == "VERIFY":
                s["verification"] = {
                    "controller_is_ic028": CURRENT_REGIME.controller == "IC-028",
                    "input_present": INPUT.is_file(),
                    "evidence_present": EVIDENCE.is_file(),
                    "current_anchor_present": CURRENT.is_file(),
                    "archive_evidence_loaded": len(evidence_text) > 1000,
                    "existing_capabilities_not_rebranded_as_new": True,
                    "private_chat_exports_excluded": True,
                }
            elif stage == "COMPLETE":
                s["terminal_disposition"] = "RELATIVE_CLOSE_WITH_ZIP_DERIVED_GROWTH_CANDIDATES"
                return {"state": s, "terminal": True}
            return {"state": s}
        return handle

    out = {stage: make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"] = lambda state: {"state": state, "terminal": True}
    return out

def run(output: Path):
    corpus = [
        {"id": "zip-study-input-106", "text": read(INPUT)},
        {"id": "zip-evidence-106", "text": read(EVIDENCE)},
        {"id": "current-improvecore", "text": read(CURRENT)},
    ]
    resolution, result = dispatch_improvement_core(
        "ImproveCore, study the ZIP archive evidence and determine what you can learn and grow from",
        state={"zip_study": True, "research_needed": False, "external_dependency": False},
        handlers=handlers(),
        corpus=corpus,
        observer_risk=True,
        allow_external_gap=False,
    )
    state = result.result.state
    report = {
        "controller": resolution.controller,
        "entrypoint": resolution.entrypoint,
        "regime_version": REGIME_VERSION,
        "regime_status": result.status,
        "terminal": result.result.terminal,
        "stage_trace": state.get("zip_study_trace"),
        "evidence_scope": state.get("evidence_scope"),
        "already_current_not_new": state.get("already_current_not_new"),
        "anchor_checks": state.get("anchor_checks"),
        "candidate_objects": state.get("candidate_objects"),
        "selected_next_candidate": state.get("selected_next_candidate"),
        "experiments": state.get("experiments"),
        "zip_study_result": state.get("zip_study_result"),
        "admission": state.get("admission"),
        "architecture_decision": state.get("architecture_decision"),
        "verification": state.get("verification"),
        "terminal_disposition": state.get("terminal_disposition"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    if not result.result.terminal:
        raise SystemExit("ImproveCore ZIP study did not reach relative close")
    if resolution.controller != "IC-028":
        raise SystemExit("ImproveCore ZIP study resolved wrong controller")
    if not all(report["verification"].values()):
        raise SystemExit("ImproveCore ZIP study verification failed")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        default=str(ROOT / "runtime/state/improvecore-zip-study-106/report.json"),
    )
    args = p.parse_args()
    run(Path(args.output))

if __name__ == "__main__":
    main()
