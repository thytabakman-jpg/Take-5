import sys
sys.path.insert(0,"runtime")

from configured_hf2_execution import execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from raise_the_ceiling import raise_the_ceiling
from tool_run_registry import CONFIGURED_RUNS


def test_prose_plain_language_rtc36_runs_under_hf2_to_relative_close():
    plan=build_tool_execution_plan(CONFIGURED_RUNS["RTC"])
    assert plan.tool_id=="RTC"
    assert plan.recurrence_engine=="HF002"
    assert len(plan.cells)==36
    assert len(plan.questions)==22*36
    assert len(plan.cognitive)==4*36

    calls=[]

    def adapter(current,current_plan):
        round_index=int(current.get("round",0))
        calls.append(round_index)

        if round_index==0:
            result=raise_the_ceiling({
                "candidates":(
                    {
                        "id":"G1_CONFIGURED_RUN_PROTECTION",
                        "strict_gain":True,
                        "preserves":True,
                    },
                    {
                        "id":"G2_REGRESSION_TEST_ISOLATION",
                        "strict_gain":True,
                        "preserves":True,
                    },
                    {
                        "id":"G3_CLARITY_OVER_BREVITY",
                        "strict_gain":True,
                        "preserves":True,
                    },
                    {
                        "id":"REJECT_WORD_BLACKLIST",
                        "strict_gain":False,
                        "preserves":False,
                    },
                ),
            })
            assert result["status"]=="ACCEPT"
            assert tuple(x["id"] for x in result["strict_gain_or_failure"])==(
                "G1_CONFIGURED_RUN_PROTECTION",
                "G2_REGRESSION_TEST_ISOLATION",
                "G3_CLARITY_OVER_BREVITY",
            )
            return {
                "status":"EXECUTED",
                "execution_truth":"IMPLEMENTATION_EXECUTED",
                "state":{
                    "round":1,
                    "accepted":tuple(
                        x["id"] for x in result["strict_gain_or_failure"]
                    ),
                },
                "result":result,
                "material_delta":True,
                "hf2_live_local":True,
                "hf2_local_close":False,
                "hf2_delta":{
                    "material_result_delta":True,
                    "route_equivalence":"prose-plain-language-rtc36-round1",
                },
                "trc_terminal":True,
                "hf1_disposition":"STABLE",
            }

        result=raise_the_ceiling({
            "candidates":(
                {
                    "id":"NO_ADDITIONAL_STRICT_GAIN",
                    "strict_gain":False,
                    "preserves":True,
                },
            ),
        })
        assert result["status"]=="NOOP"
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "state":current,
            "result":result,
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "certified_no_gain":True,
            "hf2_delta":{
                "material_result_delta":False,
                "route_equivalence":"prose-plain-language-rtc36-round2",
            },
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
        }

    out=execute_configured_with_hf2(
        tool_id="RTC",
        plan=plan,
        state={"round":0},
        adapter=adapter,
    )

    assert calls==[0,1]
    assert out.call_count==2
    assert out.rounds==2
    assert out.status=="RELATIVE_CLOSE"
    assert out.closed
    assert out.state["accepted"]==(
        "G1_CONFIGURED_RUN_PROTECTION",
        "G2_REGRESSION_TEST_ISOLATION",
        "G3_CLARITY_OVER_BREVITY",
    )
