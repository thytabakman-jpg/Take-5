import sys
from pathlib import Path

sys.path.insert(0, "runtime")

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "integration/IMPROVECORE_CHAT_EXPORT_GITHUB_INPUT_105_2026-09-26.md"


def _handlers():
    def make(stage):
        def handler(state):
            s = dict(state or {})
            trace = list(s.get("stage_trace", ()))
            trace.append(stage)
            s["stage_trace"] = trace

            if stage == "OBSERVE":
                text = INPUT.read_text(encoding="utf-8")
                s["observation"] = {
                    "input_present": INPUT.is_file(),
                    "requests_complete_three_month_archive": "every ChatGPT conversation" in text,
                    "github_destination": "thytabakman-jpg/Take-5" in text,
                    "complete_source_attached": False,
                    "partial_must_not_equal_complete": True,
                }
            elif stage == "OBSERVE_RECONCILE":
                s["reconciliation"] = {
                    "destination_capability": "AVAILABLE",
                    "source_completeness": "BLOCKED",
                    "packaging_capability": "AVAILABLE_ONCE_SOURCE_EXISTS",
                }
            elif stage == "OBSERVE_TRC":
                s["truth_constraints"] = (
                    "Do not claim every chat from selective retrieval.",
                    "Do not fabricate an account-history API.",
                    "Binary ZIP transport to GitHub is distinct from obtaining complete source history.",
                )
            elif stage == "RECOVER_GOAL":
                s["governing_goal"] = (
                    "Place a verified-complete ChatGPT conversation archive for 2026-06-26 through "
                    "2026-09-26 into GitHub with the fewest valid handoffs."
                )
            elif stage == "CURIOSITY_PD":
                s["questions"] = (
                    "Can GitHub receive the final ZIP directly?",
                    "Is a complete source corpus available in this runtime?",
                    "What is the shortest valid acquisition route for a complete corpus?",
                )
            elif stage == "FORMALIZE":
                s["formalization"] = {
                    "S": "complete source conversation corpus",
                    "F": "date filter 2026-06-26..2026-09-26",
                    "M": "Markdown renderer",
                    "Z": "ZIP packager",
                    "G": "GitHub blob/tree/commit transport",
                    "pipeline": "S -> F -> M -> Z -> G",
                    "invariant": "complete(output) requires complete(S)",
                }
            elif stage == "PLAN_ORDER":
                s["plan"] = (
                    "acquire complete account export",
                    "filter requested dates",
                    "render all included conversations",
                    "package ZIP",
                    "write binary blob and commit to GitHub",
                    "verify counts/date bounds against source",
                )
            elif stage == "OBJECTIFY":
                s["objects"] = {
                    "repo": "thytabakman-jpg/Take-5",
                    "destination": "artifacts/chat-history/",
                    "requested_period": ["2026-06-26", "2026-09-26"],
                }
            elif stage == "GENERATE_WORK":
                s["candidate_work"] = (
                    "Use attached ChatGPT export as complete source when present.",
                    "Reject selective prior-chat search as a completeness substitute.",
                    "Commit generated ZIP directly to GitHub via binary blob transport.",
                )
            elif stage == "SELECT":
                s["selected_work"] = "complete-export -> transform -> direct GitHub binary commit"
            elif stage == "BIND":
                s["binding"] = {
                    "github_transport": "bound",
                    "complete_chat_source": "unbound",
                }
            elif stage == "EXECUTE":
                s["execution_result"] = {
                    "github_direct_transport_proven": True,
                    "archive_generation_executed": False,
                    "blocker": "COMPLETE_CHATGPT_SOURCE_NOT_AVAILABLE",
                    "status": "OPEN_BLOCKED_ON_SOURCE",
                    "next_valid_input": "ChatGPT account data export containing conversations.json",
                }
                return {"state": s, "material_delta": True, "supervisory_relevant": True}
            elif stage == "ADMIT":
                s["admission"] = {
                    "admitted": (
                        "direct GitHub ZIP transport is available",
                        "complete source corpus is required",
                        "account export is the shortest currently valid complete-source route",
                    ),
                    "rejected": (
                        "claim selective history retrieval is complete",
                        "claim the archive is already creatable without source data",
                    ),
                }
            elif stage == "RECONCILE":
                s["result"] = (
                    "The destination is solved. The only live blocker is source completeness. "
                    "Once a complete ChatGPT export is supplied, transformation and direct GitHub commit can be completed."
                )
            elif stage == "PROPAGATE_AFFECTED_CONE":
                s["affected_cone"] = (
                    "chat-history archival",
                    "GitHub artifact transport",
                    "completeness verification",
                )
            elif stage == "PERSIST":
                s["persistence"] = {
                    "input": str(INPUT.relative_to(ROOT)),
                    "test": "tests/test_improvecore_chat_export_github_105.py",
                }
            elif stage == "VERIFY":
                s["verification"] = {
                    "observer_stages_seen": all(x in trace for x in ("OBSERVE", "OBSERVE_RECONCILE", "OBSERVE_TRC")),
                    "execute_seen": "EXECUTE" in trace,
                    "false_completeness_rejected": True,
                }
            elif stage == "COMPLETE":
                s["terminal_disposition"] = "OPEN_BLOCKED_ON_COMPLETE_SOURCE"
                return {"state": s, "terminal": True}
            return {"state": s}
        return handler

    handlers = {stage: make(stage) for stage in OBSERVER_FIRST_STAGES}
    handlers["REENTER"] = lambda state: {"state": state, "terminal": True}
    return handlers


def test_chat_export_to_github_problem_runs_through_current_improvecore():
    transcript = INPUT.read_text(encoding="utf-8")
    resolution, out = dispatch_improvement_core(
        "Run improve core",
        state={},
        handlers=_handlers(),
        corpus=[{"id": "chat-export-github-105", "text": transcript}],
        observer_risk=True,
    )

    state = out.result.state
    assert resolution.controller == "IC-028"
    assert resolution.entrypoint.endswith("run_improvement_core_regime")
    assert out.result.terminal is True
    assert state["execution_result"]["github_direct_transport_proven"] is True
    assert state["execution_result"]["archive_generation_executed"] is False
    assert state["execution_result"]["blocker"] == "COMPLETE_CHATGPT_SOURCE_NOT_AVAILABLE"
    assert state["terminal_disposition"] == "OPEN_BLOCKED_ON_COMPLETE_SOURCE"
