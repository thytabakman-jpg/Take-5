#!/usr/bin/env python3
"""Repeated minimal-prompt ImprovementCore + HF2 campaign.

The host supplies no target/job/basis. Each episode receives only an addressable
evidence corpus and the minimal user instruction. Prior episode output is added
as evidence for the next episode. Older structured-handoff candidate signals are
not injected into selection for this campaign.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from improvement_core_self_study import handlers, configured_tool_adapters

CHAT_EVIDENCE=ROOT/"artifacts/improvecore/IMPROVEMENTCORE_MINIMAL_CHAT_EVIDENCE_2026-09-26.md"
CURRENT=ROOT/"integration/CURRENT_IMPROVEMENT_CORE.md"
ANTI_LOSS_GOAL=ROOT/"artifacts/improvecore/GOAL_WHOLE_EVIDENCE_ANTI_LOSS_2026-09-26.md"
ANTI_LOSS_RUN=ROOT/"artifacts/improvecore/IMPROVEMENTCORE_CONFIGURED_TOOL_DURABLE_KNOWLEDGE_2026-09-26.md"
MT_EVIDENCE=ROOT/"artifacts/improvecore/IMPROVEMENTCORE_MT_PERSISTENCE_EVIDENCE_RUN_2026-09-26.md"

MINIMAL_PROMPT="ImprovementCore. Here is the chat/history evidence. Figure out what needs to be done."


def read(path:Path)->str:
    return path.read_text(encoding="utf-8")


def base_corpus():
    paths=(
        CHAT_EVIDENCE,
        CURRENT,
        ANTI_LOSS_GOAL,
        ANTI_LOSS_RUN,
        MT_EVIDENCE,
    )
    return [
        {"id":p.stem,"text":read(p)}
        for p in paths
        if p.is_file()
    ]


def compact_episode(index,resolution,result):
    state=result.result.state if isinstance(result.result.state,dict) else {}
    return {
        "episode":index,
        "controller":resolution.controller,
        "entrypoint":resolution.entrypoint,
        "regime_status":result.status,
        "blocker":result.blocker,
        "terminal":result.result.terminal,
        "hf2_status":result.hf2_status,
        "hf2_rounds":len(tuple(result.hf2_trace or ())),
        "hf2_trace":tuple(result.hf2_trace or ()),
        "mode":state.get("controller_mode"),
        "selected_next_candidate":state.get("selected_next_candidate"),
        "admission":state.get("admission"),
        "architecture_decision":state.get("architecture_decision"),
        "terminal_disposition":state.get("terminal_disposition"),
        "verification":state.get("verification"),
        "knowledge_summary":result.knowledge_summary,
    }


def run(output:Path,episodes:int=4):
    corpus=base_corpus()
    reports=[]

    for i in range(1,episodes+1):
        resolution,result=dispatch_improvement_core(
            MINIMAL_PROMPT,
            corpus=tuple(corpus),
            state={},
            handlers=handlers(handoffs_override=()),
            observer_risk=True,
            allow_external_gap=True,
            configured_tool_adapters=configured_tool_adapters(),
            hf2_enabled=True,
            hf2_max_rounds=6,
        )
        report=compact_episode(i,resolution,result)
        reports.append(report)
        corpus.append({
            "id":f"prior-improvecore-episode-{i}",
            "text":json.dumps(report,sort_keys=True,default=str),
        })

    selected=[
        (row.get("selected_next_candidate") or {}).get("id")
        for row in reports
    ]
    campaign={
        "prompt":MINIMAL_PROMPT,
        "episodes_requested":episodes,
        "episodes_completed":len(reports),
        "all_used_hf2":all(row.get("hf2_status") for row in reports),
        "selected_sequence":selected,
        "converged_same_selection":len(set(selected))==1 if selected else False,
        "episodes":reports,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(
        json.dumps(campaign,indent=2,sort_keys=True,default=str),
        encoding="utf-8",
    )
    print(json.dumps(campaign,indent=2,sort_keys=True,default=str))

    if len(reports)!=episodes:
        raise SystemExit("ImprovementCore campaign did not complete all requested episodes")
    if not all(row.get("hf2_status") for row in reports):
        raise SystemExit("An ImprovementCore episode did not cross HF2")
    return campaign


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--episodes",type=int,default=4)
    p.add_argument(
        "--output",
        default=str(ROOT/"runtime/state/improvecore-minimal-chat-campaign/report.json"),
    )
    args=p.parse_args()
    run(Path(args.output),episodes=args.episodes)


if __name__=="__main__":
    main()
