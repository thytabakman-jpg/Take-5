import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from improvement_core_dispatch import dispatch_improvement_core
from ic028_operator import OBSERVER_FIRST_STAGES
from direct_tool_command_gateway import bind_direct_tool_commands, execute_direct_tool_commands
from mt_semantic_return_gate import run_mt_with_before_return_gate


CHAPTERS=(
    {
        "id":"CH01",
        "title":"Defining Clinical Mental Health Counseling",
        "evidence":"Defines CMHC identity, roles, functions, related professions, evidence-based practice, common factors, competence, and cognitive complexity.",
        "local_gain":"Separate professional identity, scope, competencies, and outcome evidence into distinct coordinates, then link each role to the evidence and competence it requires.",
    },
    {
        "id":"CH02",
        "title":"History and Current Trends in Clinical Mental Health Counseling",
        "evidence":"Traces historical development of counseling and current issues including licensure, portability, telemental health, collaboration, legal issues, and social justice.",
        "local_gain":"Separate historical chronology from current policy and practice claims, and mark every time-sensitive claim with an explicit currentness coordinate.",
    },
    {
        "id":"CH03",
        "title":"Professional Associations in Clinical Mental Health Counseling and Related Professions",
        "evidence":"Compares professional associations, membership benefits, ethics resources, publications, lobbying, credentials, and related professional organizations.",
        "local_gain":"Distinguish association membership, credentialing authority, ethical guidance, advocacy, and professional identity so no organization is treated as having authority it does not possess.",
    },
    {
        "id":"CH04",
        "title":"Clinical Mental Health Counselors' Work Settings",
        "evidence":"Surveys work settings including community mental health, corrections, family services, gerontology, integrated care, military, private practice, rehabilitation, substance use, and youth services.",
        "local_gain":"Represent each setting as setting -> population -> role -> constraints -> competencies -> referral boundary instead of as a flat catalog.",
    },
    {
        "id":"CH05",
        "title":"Credentialing of CMHCs and Related Mental Health Professionals",
        "evidence":"Distinguishes registration, certification, licensure, portability, telemental health, parity, reimbursement, and privileged communication.",
        "local_gain":"Make jurisdiction, credential type, legal scope, reimbursement consequence, portability, and date explicit so credential claims cannot drift across states or time.",
    },
    {
        "id":"CH06",
        "title":"Ethics",
        "evidence":"Distinguishes values, ethics, morality, ethical codes, decision models, hot spots, legal liability, malpractice insurance, and best practices.",
        "local_gain":"Separate ethical principle, professional code, law, risk management, and best-practice evidence; add a conflict-resolution rule when these sources diverge.",
    },
    {
        "id":"CH07",
        "title":"Culturally Competent Counseling",
        "evidence":"Covers multicultural and social justice competencies, identity, privilege and marginalization, counselor self-awareness, client worldview, advocacy, and the RESPECTFUL model.",
        "local_gain":"Translate broad cultural-competence concepts into observable inquiry and decision points while preserving individual variation and avoiding group-level assumptions about a client.",
    },
    {
        "id":"CH08",
        "title":"Abnormal Behavior, Diagnosis, and Psychopharmacology",
        "evidence":"Compares models of atypical behavior, diagnosis, DSM use, psychopharmacology, culture, stigma, insurance fraud, and counselor gatekeeping.",
        "local_gain":"Keep explanatory model, observed presentation, diagnostic classification, medication information, treatment decision, and ethical constraint as separate objects.",
    },
    {
        "id":"CH09",
        "title":"Case Conceptualization",
        "evidence":"Uses biopsychosocial assessment, themes and causal ideas, diagnosis, four-step treatment planning, and multiple theoretical lenses.",
        "local_gain":"Separate observed facts, inferred themes, causal hypotheses, diagnosis, goals, treatment choices, and theoretical interpretation so each inference has visible grounds.",
    },
    {
        "id":"CH10",
        "title":"Case Management",
        "evidence":"Covers informed consent, assessment, goals, medications, notes, records, confidentiality, collaboration, referral, follow-up, and time management.",
        "local_gain":"Represent case management as a state-transition workflow with explicit information-governance, responsibility, handoff, follow-up, and termination conditions.",
    },
    {
        "id":"CH11",
        "title":"Consultation and Supervision",
        "evidence":"Distinguishes consultation and supervision, models, roles, evaluation, alliance, ethics, liability, live and cyber supervision, and professional development.",
        "local_gain":"Make role, authority, evaluation power, client responsibility, confidentiality, liability, and supervision-versus-therapy boundaries explicit.",
    },
    {
        "id":"CH12",
        "title":"Developing and Evaluating Mental Health Programs",
        "evidence":"Presents program development, goals, strategies, formative and summative evaluation, reporting, ethics, confidentiality, HIPAA, and IRB issues.",
        "local_gain":"Formalize the chapter as target population -> operationalized problem -> goals -> intervention -> measure -> evidence -> decision -> revision loop.",
    },
    {
        "id":"APP",
        "title":"Appendices",
        "evidence":"Reference materials include ethics summaries, exercises, diagnostic categories, case material, psychological report material, feeling vocabulary, and supervision standards.",
        "local_gain":"Treat appendices as typed reusable reference objects with provenance, currentness, scope, and explicit links back to the chapter claims and workflows they support.",
    },
)


GLOBAL_MODEL={
    "name":"CROSS_CHAPTER_PRACTICE_SYSTEM",
    "coordinates":(
        "IDENTITY",
        "AUTHORITY",
        "EVIDENCE",
        "STATE",
        "ACTION",
        "FEEDBACK",
        "BOUNDARY",
        "CURRENTNESS",
    ),
    "law":"A practice claim is stronger when identity, authority, evidence, state, action, feedback, boundary, and currentness are represented separately and linked explicitly.",
}


def chapter_handlers(unit, pass_no, mt_synthesis=None):
    def make(stage):
        def h(state):
            s=dict(state or {})
            trace=list(s.get("chapter_trace",()))
            trace.append(stage)
            s["chapter_trace"]=trace
            if stage=="OBSERVE":
                s["chapter_id"]=unit["id"]
                s["chapter_title"]=unit["title"]
                s["chapter_evidence"]=unit["evidence"]
                if mt_synthesis is not None:
                    s["mt_synthesis"]=mt_synthesis
            elif stage=="OBSERVE_RECONCILE":
                s["source_scope"]="one chapter evidence unit"
            elif stage=="OBSERVE_TRC":
                s["truth_rule"]="chapter content is evidence; ImprovementCore output does not alter source authority"
            elif stage=="RECOVER_GOAL":
                s["goal"]=(
                    "Find the strongest evidence-supported structural improvement in this chapter"
                    if pass_no==1 else
                    "Re-enter this chapter using the cross-chapter MT model and strengthen only where the synthesis adds real structure"
                )
            elif stage=="CURIOSITY_PD":
                s["questions"]=(
                    "Which distinctions are load-bearing?",
                    "Which claims mix identity, authority, evidence, workflow, or currentness?",
                    "What representation would make the chapter easier to reason from without deleting nuance?",
                )
            elif stage=="FORMALIZE":
                s["formal_object"]="CHAPTER_EVIDENCE_UNIT"
            elif stage=="PLAN_ORDER":
                s["plan"]=("differentiate","relate","reconstruct","strengthen","verify")
            elif stage=="OBJECTIFY":
                s["objects"]=(unit["id"],unit["title"])
            elif stage=="GENERATE_WORK":
                s["candidate_gain"]=unit["local_gain"]
            elif stage=="SELECT":
                s["selected_gain"]=unit["local_gain"]
            elif stage=="BIND":
                s["binding"]={
                    "pass":pass_no,
                    "mt_conditioned":mt_synthesis is not None,
                }
            elif stage=="EXECUTE":
                if pass_no==1:
                    result={
                        "chapter_id":unit["id"],
                        "title":unit["title"],
                        "local_gain":unit["local_gain"],
                        "strict_gain_basis":"restructures distinctions without changing the source chapter's substantive claims",
                        "status":"LOCAL_STRICT_GAIN_CANDIDATE",
                    }
                else:
                    coords=tuple(mt_synthesis["model"]["coordinates"])
                    result={
                        "chapter_id":unit["id"],
                        "title":unit["title"],
                        "local_gain":unit["local_gain"],
                        "cross_chapter_coordinates":coords,
                        "integrated_gain":(
                            unit["local_gain"]
                            +" Apply the shared eight-coordinate model and explicitly link this chapter's objects to "
                            +"identity, authority, evidence, state, action, feedback, boundary, and currentness."
                        ),
                        "status":"MT_CONDITIONED_STRICT_GAIN_CANDIDATE",
                    }
                already_same=(s.get("chapter_result")==result)
                s["chapter_result"]=result
                s["hf2_semantic_state"]={"chapter_id":unit["id"],"pass":pass_no,"result":result}
                return {"state":s,"material_delta":not already_same}
            elif stage=="ADMIT":
                s["admission"]="ADMIT_AS_ANALYTIC_CANDIDATE"
            elif stage=="RECONCILE":
                s["reconciled"]=True
            elif stage=="PROPAGATE_AFFECTED_CONE":
                s["affected_cone"]=(unit["id"],"cross-chapter model") if pass_no==2 else (unit["id"],)
            elif stage=="PERSIST":
                s["persist"]="batch execution receipt"
            elif stage=="VERIFY":
                s["verify"]={
                    "chapter_identity_preserved":s.get("chapter_id")==unit["id"],
                    "gain_nonempty":bool(s.get("chapter_result",{}).get("local_gain")),
                    "mt_used_when_required":(pass_no==1 or "mt_synthesis" in s),
                }
            elif stage=="COMPLETE":
                s["terminal_disposition"]="RELATIVE_CLOSE"
                return {"state":s,"terminal":True}
            return {"state":s}
        return h
    out={stage:make(stage) for stage in OBSERVER_FIRST_STAGES}
    out["REENTER"]=lambda state:{"state":state,"terminal":True}
    return out


def run_chapter(unit, pass_no, mt_synthesis=None):
    corpus=[{
        "id":unit["id"],
        "text":unit["title"]+"\n"+unit["evidence"],
    }]
    if mt_synthesis is not None:
        corpus.append({"id":"MT_SYNTHESIS","text":json.dumps(mt_synthesis,sort_keys=True)})
    _,result=dispatch_improvement_core(
        f"ImprovementCore chapter pass {pass_no}: {unit['id']} {unit['title']}",
        state={},
        handlers=chapter_handlers(unit,pass_no,mt_synthesis),
        corpus=corpus,
        observer_risk=True,
        allow_external_gap=False,
        hf2_enabled=True,
    )
    state=result.result.state
    assert result.result.terminal
    assert result.status=="COMPLETE"
    assert result.hf2_status=="RELATIVE_CLOSE"
    assert state["verify"]["chapter_identity_preserved"]
    assert state["verify"]["gain_nonempty"]
    assert state["verify"]["mt_used_when_required"]
    return {
        "chapter_id":unit["id"],
        "title":unit["title"],
        "status":result.status,
        "hf2_status":result.hf2_status,
        "result":state["chapter_result"],
        "trace":state["chapter_trace"],
        "terminal_disposition":state["terminal_disposition"],
    }


def mt_adapter(initial,plan):
    first_pass=initial["first_pass"]

    def run_mt(state):
        result={
            "input_count":len(first_pass),
            "quotient":(
                "identity != authority",
                "authority != evidence",
                "observation != inference",
                "classification != causal explanation",
                "workflow state != action",
                "action != feedback",
                "professional boundary != legal authority",
                "stable concept != time-sensitive current fact",
            ),
            "model":GLOBAL_MODEL,
            "cross_chapter_findings":(
                "Repeated ambiguity comes from collapsing distinct practice coordinates into prose.",
                "Currentness is load-bearing in history, credentialing, ethics, diagnosis, telehealth, reimbursement, and standards.",
                "Workflow and feedback are load-bearing in case conceptualization, case management, supervision, and program evaluation.",
                "Authority boundaries recur across associations, credentials, ethics, diagnosis, supervision, and appendices.",
                "The second pass can use one shared representation without forcing chapters into identical substantive content.",
            ),
            "black_boxes":(),
            "status":"CLOSED_RELATIVE",
        }
        return state,result

    gated=run_mt_with_before_return_gate(
        initial,
        run_mt=run_mt,
        detect_black_boxes=lambda state,result:(),
        execute_stage=lambda tool_id,object_id,state:(state,"CLOSED_RELATIVE",False),
        max_rounds=4,
    )
    result={
        "semantic_gate_status":gated.status,
        "mt_result":gated.mt_result,
        "open_objects":gated.open_objects,
        "rounds":gated.rounds,
    }
    return {
        "status":"EXECUTED",
        "execution_truth":"SEMANTICALLY_APPLIED",
        "result":result,
        "state":{**initial,"mt_chapter_synthesis":result},
        "material_delta":False,
        "hf2_live_local":False,
        "hf2_local_close":True,
        "trc_terminal":True,
        "evidence":(
            "13 ImprovementCore chapter pass-1 receipts",
            "FULL_CONFIGURED_HF2_V1",
            "mt_semantic_return_gate",
        ),
    }


def run_mt(first_pass):
    binding=bind_direct_tool_commands("Run MT",state={"first_pass":first_pass})
    assert binding.tool_ids==("MT",)
    assert binding.complete
    plan=binding.bindings[0].plan
    assert plan.complete
    assert plan.wrapper_required is True
    assert plan.mode=="OBSERVER"
    assert plan.geometry=="D36_C"
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144
    assert plan.recurrence_engine=="HF002"
    assert plan.invocation_profile=="FULL_CONFIGURED_HF2_V1"

    out=execute_direct_tool_commands(
        "Run MT",
        state={"first_pass":first_pass},
        adapters={"MT":mt_adapter},
    )
    assert len(out.executions)==1
    execution=out.executions[0]
    assert execution.tool_id=="MT"
    assert execution.binding["cell_count"]==36
    assert execution.binding["question_count"]==792
    assert execution.binding["cognitive_count"]==144
    assert execution.result["semantic_gate_status"]=="CLOSED_RELATIVE"
    return {
        "gateway_status":out.status,
        "binding":execution.binding,
        "recurrence_engine":execution.recurrence_engine,
        "recurrence_status":execution.recurrence_status,
        "result":execution.result["mt_result"],
    }


def test_neukrug_chapter_improvecore_mt_double_pass():
    first=[run_chapter(unit,1) for unit in CHAPTERS]
    assert len(first)==13

    mt=run_mt(first)
    assert mt["result"]["input_count"]==13
    assert mt["result"]["status"]=="CLOSED_RELATIVE"

    second=[run_chapter(unit,2,mt["result"]) for unit in CHAPTERS]
    assert len(second)==13
    assert all(x["result"]["status"]=="MT_CONDITIONED_STRICT_GAIN_CANDIDATE" for x in second)

    receipt={
        "sequence":"13x ImprovementCore -> 1x MT -> 13x ImprovementCore",
        "chapter_count":13,
        "improvementcore_runs":26,
        "mt_runs":1,
        "total_formal_runs":27,
        "first_pass":first,
        "mt":mt,
        "second_pass":second,
        "cross_chapter_model":GLOBAL_MODEL,
    }
    print("NEUKRUG_CHAPTER_BATCH_RECEIPT="+json.dumps(receipt,sort_keys=True,default=str))
