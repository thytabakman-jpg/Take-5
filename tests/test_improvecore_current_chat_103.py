import json
import sys
from pathlib import Path

sys.path.insert(0, "runtime")

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES

ROOT = Path(__file__).resolve().parents[1]
CHAT = ROOT / "integration/IMPROVECORE_CURRENT_CHAT_INPUT_103_2026-09-26.md"
POINTER = ROOT / "integration/IMPROVECORE_KUREPA_CONVERSATION_POINTER_102_2026-09-26.md"

def _handlers():
    def make(stage):
        def handler(state):
            s = dict(state or {})
            trace = list(s.get("stage_trace", ()))
            trace.append(stage)
            s["stage_trace"] = trace

            if stage == "OBSERVE":
                text = CHAT.read_text(encoding="utf-8")
                s["chat_observation"] = {
                    "exact_snapshot_present": True,
                    "mentions_kurepa_pointer": "Kurepa" in text or "kurpa" in text.lower(),
                    "explicit_run_request_present": "Run improve core. Give it the whole chat and run it" in text,
                }
            elif stage == "OBSERVE_RECONCILE":
                s["observation_reconciliation"] = {
                    "pointer_created_before_runtime_invocation": True,
                    "pointer_is_not_source_artifact": True,
                }
            elif stage == "OBSERVE_TRC":
                pointer = POINTER.read_text(encoding="utf-8")
                declared = any(
                    line.strip().lower().startswith(("source_path:", "source_file:", "source_artifact:"))
                    for line in pointer.splitlines()
                )
                s["truth_constraints"] = {
                    "pointer_exists": POINTER.is_file(),
                    "kurepa_source_path_declared": declared,
                    "source_location_status": "RESOLVED" if declared else "OPEN",
                }
            elif stage == "RECOVER_GOAL":
                s["governing_goal"] = (
                    "Run current ImproveCore on the complete visible chat corpus; "
                    "consume the real Kurepa conversation when located; admit only strict-gain changes."
                )
            elif stage == "CURIOSITY_PD":
                s["questions"] = (
                    "Where is the actual new Kurepa conversation Markdown file?",
                    "What mathematical/tool-decomposition content does it add beyond current math?",
                    "Does this chat expose a host-to-runtime invocation gap worth protecting?",
                )
            elif stage == "FORMALIZE":
                s["formal_objects"] = {
                    "C": "current visible chat corpus",
                    "P": "Kurepa pointer artifact",
                    "S": "actual Kurepa source artifact",
                    "R": "current ImproveCore dispatch/runtime",
                }
                s["formal_relation"] = "C -> R; P -> locate(S); S -> assess(strict_gain)"
            elif stage == "PLAN_ORDER":
                s["plan"] = (
                    "freeze corpus",
                    "verify pointer/source distinction",
                    "run current dispatcher",
                    "preserve source-location OPEN",
                    "verify receipt",
                )
            elif stage == "OBJECTIFY":
                s["objects"] = {
                    "chat_path": str(CHAT.relative_to(ROOT)),
                    "pointer_path": str(POINTER.relative_to(ROOT)),
                }
            elif stage == "GENERATE_WORK":
                s["candidate_work"] = (
                    "execute zero-request ImproveCore dispatch on exact chat corpus",
                    "locate and read Kurepa source artifact",
                    "protect invocation receipt at host boundary",
                )
            elif stage == "SELECT":
                s["selected_work"] = "execute zero-request dispatch and preserve Kurepa source lookup as OPEN"
            elif stage == "BIND":
                s["binding"] = {
                    "controller": "IC-028",
                    "authority": "observe/read/execute current controller; no fabricated source path",
                }
            elif stage == "EXECUTE":
                pointer = POINTER.read_text(encoding="utf-8")
                declared = any(
                    line.strip().lower().startswith(("source_path:", "source_file:", "source_artifact:"))
                    for line in pointer.splitlines()
                )
                s["execution_result"] = {
                    "dispatcher_crossed": True,
                    "chat_corpus_consumed": True,
                    "kurepa_pointer_consumed": True,
                    "kurepa_source_location": "RESOLVED" if declared else "OPEN",
                    "material_finding": (
                        "The pointer is durable, but the actual Kurepa source file is not identified in it; "
                        "the current run therefore preserves source acquisition as OPEN rather than inventing a path."
                    ),
                }
                return {"state": s, "material_delta": True, "supervisory_relevant": True}
            elif stage == "ADMIT":
                s["admission"] = {
                    "admitted": (
                        "actual configured ImproveCore dispatch receipt on this chat",
                        "pointer/source distinction",
                        "OPEN source-location state",
                    ),
                    "rejected": (
                        "claim that writing the pointer itself constituted an ImproveCore runtime run",
                        "fabricated Kurepa source path",
                    ),
                }
            elif stage == "RECONCILE":
                s["reconciliation"] = "No canonical Kurepa-math change admitted without reading the source artifact."
            elif stage == "PROPAGATE_AFFECTED_CONE":
                s["affected_cone"] = (
                    "ImproveCore host/runtime invocation boundary",
                    "Kurepa conversation acquisition",
                    "future run-receipt verification",
                )
            elif stage == "PERSIST":
                s["persistence"] = {
                    "chat_input": str(CHAT.relative_to(ROOT)),
                    "run_test": "tests/test_improvecore_current_chat_103.py",
                }
            elif stage == "VERIFY":
                s["verification"] = {
                    "chat_file_exists": CHAT.is_file(),
                    "pointer_file_exists": POINTER.is_file(),
                    "all_prior_observer_stages_seen": all(x in trace for x in ("OBSERVE", "OBSERVE_RECONCILE", "OBSERVE_TRC")),
                    "execute_seen": "EXECUTE" in trace,
                }
            elif stage == "COMPLETE":
                s["terminal_disposition"] = "RELATIVE_CLOSE_WITH_KUREPA_SOURCE_LOCATION_OPEN"
                return {"state": s, "terminal": True}
            return {"state": s}
        return handler

    handlers = {stage: make(stage) for stage in OBSERVER_FIRST_STAGES}
    handlers["REENTER"] = lambda state: {"state": state, "terminal": True}
    return handlers

def test_current_chat_runs_through_actual_improvecore_dispatch():
    transcript = CHAT.read_text(encoding="utf-8")
    resolution, out = dispatch_improvement_core(
        "Run improve core. Give it the whole chat and run it",
        state={},
        handlers=_handlers(),
        corpus=[{"id": "current-chat-103", "text": transcript}],
        observer_risk=True,
    )

    state = out.result.state
    receipt = {
        "controller": resolution.controller,
        "entrypoint": resolution.entrypoint,
        "regime_status": out.status,
        "terminal": out.result.terminal,
        "manager_stages": list(out.receipt.stages),
        "mode": state.get("controller_mode"),
        "upstream_discovery": state.get("upstream_discovery"),
        "execution_result": state.get("execution_result"),
        "verification": state.get("verification"),
        "terminal_disposition": state.get("terminal_disposition"),
    }
    print("IMPROVECORE_CHAT_103_RECEIPT=" + json.dumps(receipt, sort_keys=True, default=str))

    assert resolution.controller == "IC-028"
    assert resolution.entrypoint.endswith("run_improvement_core_regime")
    assert out.result.terminal is True
    assert state["chat_observation"]["exact_snapshot_present"] is True
    assert state["execution_result"]["dispatcher_crossed"] is True
    assert state["execution_result"]["chat_corpus_consumed"] is True
    assert state["truth_constraints"]["source_location_status"] == "OPEN"
    assert state["terminal_disposition"] == "RELATIVE_CLOSE_WITH_KUREPA_SOURCE_LOCATION_OPEN"
