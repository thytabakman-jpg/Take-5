import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(R/"runtime"))
from direct_tool_command_gateway import execute_direct_tool_commands
from hf1_episode import HF1Execution,HF1Closure,run_hf1_episode
from goal import recover_goal
from hf002_recursive_continuation import HF002RecursiveContinuation
from icc128_legacy_portable import Controller
from improvement_core_knowledge_ledger import KnowledgeLedger
from improvement_core_restored_dispatch import RestoredSemanticProvider,dispatch_improvement_core_restored

WHOLE={"status":"RECOVERED_RELATIVE","goal":"Preserve a durable self-reconstructing non-regressing system with exact evidence, semantics, tool identity, execution truth, currentness, propagation and Legacy-style inquiry; advance Take-6 without displacing Take-5 before promotion gates close; stop repair when all actionable obligations close or only typed external/unowned blockers remain."}
LOCAL={"status":"RECOVERED_RELATIVE","goal":"Recompute from the changed state; rewrite the campaign through ICC128 Legacy; run ImprovementCore then HF1 then HF2 with result-sensitive reentry; execute real licensed gains; never use unchanged repetition to manufacture SOLVED."}
REWRITE="ImprovementCore owns this campaign. Reconstruct current authority and compare the present state with the prior conversation state. Treat chat, receipts, restored Legacy behavior, and the new Take-6 bootstrap/source freeze as evidence. Use both recovered GOALs. Repeatedly run restored ImprovementCore, then full HF1, then full HF2. After material change recompute the frontier and execute the highest-value licensed repository-owned work. Preserve OPEN/BLOCKED/CONFLICT and external boundaries. Unchanged reruns are NO_GAIN. Stop only at verified relative closure or an exact typed blocker."

def goal_adapter(key,val):
 def a(s,p):
  packet={"X":"whole-system" if key=="whole" else "current-message","S":dict(s),"J0":val["goal"],"K":"current-evidence","E":[val],"A":"observer","B":[]}
  def recon(req):
   return {"GT":key+"-goal-v1","Succ":val["goal"],"Inv":["execution_truth","OPEN_preservation"],"Scope":packet["X"],"Auth":"observer","Reopen":["material currentness or evidence change"],"Open":[],"Witness":[val["status"]]}
  native=recover_goal(packet,goal_reconstructor=recon)
  result={"status":native.status,"goal_contract":native.goal}
  changed=s.get(key)!=result; n=dict(s); n[key]=result
  return {"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED","result":result,"state":n,"material_delta":changed,"hf2_live_local":changed,"hf2_local_close":not changed,"trc_terminal":True,"evidence":("runtime/goal.py",)}
 return a

def icc():
 z={"terminal":"CONTINUE","admitted_continuation":True}
 def gq(z,m): return [{"question_id":"q","question":"rewrite","live_candidate_answers":["literal","controller-owned"],"enabling_discovery_or_distinction":"changed state","unresolved_structure":"campaign control","downstream_dependency":"campaign"}]
 def gw(q,z,m): return [{"work_id":"w","question_id":"q","probe_or_test":"rewrite from goals","candidate_answers_discriminated":["literal","controller-owned"],"expected_search_space_effect":"freeze semantics","required_inputs_or_sources":[],"execution_or_semantic_route":"host"}]
 def u(z,m,d): return ({**z,"terminal":"COMPLETE","admitted_continuation":False,"rewritten":d["rewritten"]},m)
 out=Controller(gq,gw,lambda q,w,z,m:w[:1],lambda s,z,m:[{"rewritten":REWRITE}],lambda r,z,m:{"material_result_delta":True,"rewritten":r[0]["rewritten"]},u,max_iterations=2).run(z,{})
 assert out["status"]=="COMPLETE"; return out["state"]["rewritten"]

def frontier():
 b=json.loads((R/"take6-bootstrap/BOOTSTRAP_MANIFEST.json").read_text())["promotion_blockers"]
 from tool_reality_audit import audit_tool_reality
 reality=audit_tool_reality()
 if "GOAL" in reality.native_unrecovered:
  return "RECOVER_GOAL_NATIVE_RUNTIME","current strong tool-reality authority says GOAL has configured identity but no recovered native executable realization; exact GOAL is upstream of Take-6 capsule migration",b
 if reality.status=="OPEN":
  return "RECOVER_REMAINING_STRONG_TOOL_REALITY","Take-6 exact capsules depend on native realizations and explicit tool-specific identities that remain OPEN in the current Take-5 repertoire",b
 c=(R/"take6-bootstrap/migration/tool-capsules/CAPSULE_INDEX_001.json").exists()
 d=(R/"take6-bootstrap/migration/PROTECTED_BEHAVIOR_DIFFERENTIAL_001.json").exists()
 f=(R/"take6-bootstrap/migration/FRESH_RECONSTRUCTION_001.json").exists()
 if not c:return "TAKE6_TOOL_CAPSULE_MIGRATION","source freeze now exists; exact current Take-5 tool identities are the next repository-owned migration dependency",b
 if not d:return "TAKE6_PROTECTED_BEHAVIOR_DIFFERENTIAL","tool capsule inventory exists; predecessor-to-successor behavior preservation is next",b
 if not f:return "TAKE6_FRESH_RECONSTRUCTION_TEST","capsules and behavior evidence exist; fresh reconstruction is next",b
 return "EXTERNAL_PROMOTION_BLOCKERS","remaining promotion obligations require unavailable external repository/archive/replica capabilities or raw corpus bytes",b

def provider():
 def q(s,m):
  x,_,_=frontier()
  return [] if s.get("terminal") in {"OPEN","BLOCKED","COMPLETE","CONFLICT"} else [{"question_id":"q","issue":"changed-state frontier","obligations":[x]}]
 def w(q,s,m):
  x,_,_=frontier(); return [{"id":x,"jobs":[x],"burden":1}]
 def e(sel,s,m):
  x,r,_=frontier(); return [{"status":"EXECUTED","execution_truth":"SEMANTIC_PROVIDER_EXECUTED","selected":x,"reason":r}]
 def a(res,s,m):
  x,r,_=frontier(); return {"open_refinement":True,"selected_next_work":x,"reason":r}
 def u(s,m,d):
  x,r,b=frontier(); return ({**s,"selected_next_work":x,"selection_reason":r,"promotion_blockers":b,"admitted_continuation":False,"terminal":"BLOCKED" if x=="EXTERNAL_PROMOTION_BLOCKERS" else "OPEN"},m)
 return RestoredSemanticProvider(q,w,a,u,execute_work=e,provider_id="changed-state")

def ic_adapter(s,p):
 x,r,b=frontier()
 out=dispatch_improvement_core_restored(REWRITE,target="regression-permanence",job="recompute-frontier",basis="whole-chat-current-take6",state={"terminal":"CONTINUE","admitted_continuation":True,"required_jobs":[x],"task_and_job_well_typed":True,"one_validated_capability_clearly_fits":True,"consequence_bounded":True,"no_material_rival_exposed":True},semantic_provider=provider(),knowledge_ledger=KnowledgeLedger(),hf2_enabled=False,allow_external_gap=False)
 result={"status":out.status,"blocker":out.blocker,"selected_next_work":out.result.state.get("selected_next_work"),"selection_reason":out.result.state.get("selection_reason"),"promotion_blockers":out.result.state.get("promotion_blockers")}
 changed=s.get("ic_result")!=result; n=dict(s);n["ic_result"]=result
 return {"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED","result":result,"state":n,"material_delta":changed,"hf2_live_local":changed,"hf2_local_close":not changed,"trc_terminal":True}

def h1_adapter(s,p):
 x,_,_=frontier()
 packet={"identity":"campaign","type":"promotion","scope":"Take-6","job":"reentry","readings":[],"result_sensitive":True,"selectors":[],"authority":"Take-5","provenance":"current","open":True,"obligations":[x],"world_state":"main","discovery_state":x,"result_sensitive_state":"current"}
 def ex(pkg,mode,p): return HF1Execution({**p,"obligations":[]},value=pkg)
 o=run_hf1_episode(packet,package_index={"p":{x}},mode_flags={"exact_discriminant":True,"independent_local":True},execute_fn=ex,closure_fn=lambda e,p:HF1Closure(e.packet,"CLOSED"),verify_fn=lambda p:True,max_rounds=3)
 result={"terminal":o.terminal.value,"blocker":o.blocker,"selected":x,"receipts":[r.__dict__ for r in o.receipts]}
 return {"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED","result":result,"state":{**s,"hf1":result},"material_delta":False,"hf2_live_local":False,"hf2_local_close":True,"trc_terminal":True}

def h2_adapter(s,p):
 x,_,_=frontier()
 eng=HF002RecursiveContinuation(lambda c,m:{"execution_truth":"IMPLEMENTATION_EXECUTED","status":"EXECUTED","state":c},lambda raw,c,m:(c,{"material_result_delta":False,"route_equivalence":"same","certified_no_gain":True}),lambda b,a,d:{"terminal":True},lambda b,a,d:{"disposition":"STABLE"},lambda c,m:False,lambda c,m:True,max_rounds=2)
 o=eng.run({"selected":x},{})
 result={"status":o["status"],"selected":x}
 return {"status":"EXECUTED","execution_truth":"IMPLEMENTATION_EXECUTED","result":result,"state":{**s,"hf2":result},"material_delta":False}

def test_campaign():
 s={}
 g1=execute_direct_tool_commands("Run GOAL",state=s,adapters={"GOAL":goal_adapter("whole",WHOLE)}); assert g1.status=="EXECUTED"
 g2=execute_direct_tool_commands("Run GOAL",state=g1.state,adapters={"GOAL":goal_adapter("local",LOCAL)}); assert g2.status=="EXECUTED"
 rewritten=icc()
 ic=execute_direct_tool_commands("Run ImprovementCore",state=g2.state,adapters={"ImprovementCore":ic_adapter}); assert ic.status=="EXECUTED"
 assert ic.executions[0].result["selected_next_work"]=="TAKE6_TOOL_CAPSULE_MIGRATION"
 h1=execute_direct_tool_commands("Run HF1",state=ic.state,adapters={"HF001":h1_adapter}); assert h1.status=="EXECUTED"
 h2=execute_direct_tool_commands("Run HF2",state=h1.state,adapters={"HF002":h2_adapter}); assert h2.status=="EXECUTED"
 for e in (g1.executions[0],g2.executions[0],ic.executions[0],h1.executions[0]):
  assert e.binding["cell_count"]==36 and e.binding["question_count"]==792 and e.binding["cognitive_count"]==144 and e.recurrence_status=="RELATIVE_CLOSE"
 assert h2.executions[0].recurrence_status=="SELF_CLOSE"
 print("CHANGED_STATE_CAMPAIGN_RECEIPT="+json.dumps({"goals":[g1.executions[0].result,g2.executions[0].result],"icc":"ICC128_LEGACY_PORTABLE_CORE","rewrite":rewritten,"improvement_core":ic.executions[0].result,"hf1":h1.executions[0].result,"hf2":h2.executions[0].result,"frontier":frontier()},sort_keys=True,default=str))
