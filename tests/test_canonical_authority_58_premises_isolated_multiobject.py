"""Isolated 58-premise MultiObject investigation. No downstream objects are read.

Source: https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/canonical-authority/research/ALL_ROADS_PREMISE_INFERENCE_COMMITMENT_ATLAS.md
Source blob: 5d1a2404f5b51ca4e6db969b9e836f09d298f49d
The frozen premise-only matrix is a bounded, typed discovery screen: absence of a
licensed pair relation means OPEN. C36 face probes are structured OPEN inspections;
they are not 2,088 certified deep semantic validations.
"""
import json
import sys
from collections import Counter
from itertools import combinations

sys.path.insert(0, "runtime")
from multiobject import (FrozenObject, RelationFinding, RouteResult,
    ResidualJudgment, ViewRequest, ReconciledFinding, run_multiobject)
from global_tool_execution import build_tool_execution_plan
from tool_run_registry import CONFIGURED_RUNS

SOURCE_BLOB = "5d1a2404f5b51ca4e6db969b9e836f09d298f49d"
PREMISES = json.loads("[[\"P001\",\"Rashi and Ramban disagree about the grammatical status of *reishis* in Bereishis 1:1.\",\"case\"],[\"P002\",\"Rashi and Ramban are recognized authorities within the Jewish interpretive tradition.\",\"case\"],[\"P003\",\"Rashi and Ramban possess equal traditional standing as commentators on Bereishis.\",\"comparative hypothesis; equal standing is unverified\"],[\"P004\",\"The factual accuracy of a rabbinic interpretation is distinct from its religious authority and canonical legitimacy.\",\"analytic principle; truth/status distinction\"],[\"P005\",\"Equal support for incompatible factual claims cannot by itself justify preferring either claim as true.\",\"analytic comparative-support principle\"],[\"P006\",\"A justified preference between factual claims requires adequate grounds for identifying evidence in favor of the preferred claim.\",\"analytic evaluator-warrant principle\"],[\"P007\",\"Evidence of a source's reliability in one domain does not establish its reliability in another domain.\",\"analytic source-to-target principle\"],[\"P008\",\"The evidence examined in this project has not established which rival grammatical claim about *reishis* is correct.\",\"bounded project-evidence observation; not a theological doctrine\"],[\"P101\",\"Recognized canonical authorities have made incompatible factual assertions.\",\"historical\"],[\"P102\",\"The claim that God created the heavens and the earth remains true under either grammatical interpretation of *reishis* in Bereishis 1:1.\",\"proposed concrete downstream-content hypothesis; unverified\"],[\"P103\",\"Canonical recognition of incompatible rabbinic teachings does not entail that both teachings are factually true.\",\"source-based\"],[\"P104\",\"Two incompatible Torah interpretations can each possess religious legitimacy.\",\"conditional\"],[\"P105\",\"Two contradictory factual propositions are both true in the same respect.\",\"hypothetical\"],[\"P106\",\"Ramban disagrees with Rashi about the grammar of *reishis* in Bereishis 1:1.\",\"source-based\"],[\"P107\",\"Rashi's and Ramban's competing grammatical interpretations of *reishis* are compatible.\",\"hypothetical\"],[\"P108\",\"Some knowledge transmitted as Torah law was forgotten.\",\"source-based\"],[\"P109\",\"There are disputes among earlier halachic authorities that later halachic authorities cannot independently resolve on their merits.\",\"restricted historical/halachic hypothesis; scope remains source-qualified\"],[\"P110\",\"The later evaluator has no truth-relevant method for determining which of Rashi's and Ramban's grammatical claims is correct.\",\"unsupported global incapacity hypothesis\"],[\"P111\",\"Earlier rabbinic generations had greater learning capacities than later rabbinic generations.\",\"source-based generalization; historical scope review open\"],[\"P112\",\"An earlier authoritative rabbinic corpus has greater epistemic authority than a later corpus addressing the same Torah-law question.\",\"source-based corpus-level hypothesis; truth versus normative authority unresolved\"],[\"P113\",\"Among Rishonim, earlier scholars are more factually reliable solely because they lived earlier.\",\"unsupported\"],[\"P114\",\"Ramban encountered a version of Rashi's commentary that lacked Rashi's response to the Yeshayahu 46:10 challenge.\",\"historical hypothesis attributed to Re'em; not established history\"],[\"P115\",\"Interpretations received from Moses at Sinai are not subject to genuine disagreement among the sages.\",\"Rambam-associated source-based claim; exact scope source-qualified\"],[\"P116\",\"Independent, mutually corroborating chains of transmission preserve the content of a received report accurately.\",\"Halevi-associated transmission hypothesis; corroboration requirements source-qualified\"],[\"P117\",\"Inherited continuity of texts, practices, and teachings is sufficient for membership in mesorah.\",\"pending\"],[\"P118\",\"The grammatical knowledge needed to resolve the Rashi–Ramban dispute was not transmitted.\",\"unsupported\"],[\"P119\",\"Participation in inherited Torah interpretation does not establish that an interpretation was received from Moses at Sinai.\",\"source-based-qualified\"],[\"P120\",\"Methods of Torah study can themselves be transmitted as part of mesorah.\",\"pending\"],[\"P121\",\"A test of religious authority can be justified without relying on the authority it evaluates.\",\"analytic-conditional\"],[\"P122\",\"The authenticity of mesorah depends solely on rabbinic authority, while that rabbinic authority depends solely on mesorah.\",\"analytic-conditional\"],[\"P123\",\"Differences in subject-specific expertise, reliability, information, or access can justify preferring one commentator's factual judgment.\",\"general-epistemic\"],[\"P124\",\"A halachic ruling can establish binding practice while the underlying factual or interpretive dispute remains unresolved.\",\"source-based-qualified\"],[\"P125\",\"Wisdom-mediated Ruach HaKodesh can give a sage knowledge after ordinary prophecy has ceased.\",\"source-based\"],[\"P126\",\"Inspired speech and writing can occur below the level of full prophecy.\",\"source-based\"],[\"P127\",\"Knowledge genuinely received through divine influx is free from error.\",\"source-based\"],[\"P128\",\"Ruach HaKodesh can provide access to esoteric Torah knowledge.\",\"source-based\"],[\"P129\",\"Some rabbinic writings possess extraordinary divine protection against factual error.\",\"source-pending extraordinary truth-guarantee hypothesis\"],[\"P130\",\"Authoritative institutional halachic rulings can be erroneous.\",\"source-based\"],[\"P131\",\"Authenticating a claim to prophecy requires criteria for recognition.\",\"source-based prophetic-authentication requirement\"],[\"P132\",\"Ramban's commentary on Bereishis 1:1 draws on teachings about creation passed down through tradition.\",\"Ramban-associated creation-knowledge claim; exact attribution to be checked\"],[\"P133\",\"Received teachings about creation do not, by themselves, establish the grammatical interpretation of *reishis*.\",\"bounded project-evidence observation; not a traditional doctrine\"],[\"P134\",\"One of the rival grammatical claims belongs to a transmitted category guaranteed to be factually correct.\",\"hypothetical\"],[\"P135\",\"Membership in mesorah does not by itself guarantee the factual truth of a transmitted claim.\",\"hypothetical\"],[\"P136\",\"An authenticated privileged disclosure about the disputed grammatical proposition favors one rival.\",\"hypothetical\"],[\"P137\",\"The original source of a faithfully transmitted report is reliable about the proposition it reports.\",\"hypothetical\"],[\"P138\",\"Explaining the historical origin of a disagreement does not establish which factual claim is correct.\",\"analytic\"],[\"P139\",\"A truth guarantee confined to one domain does not extend automatically to claims outside that domain.\",\"analytic\"],[\"P140\",\"Institutional bindingness, canonical legitimacy, authenticated provenance, and factual truth are different properties of an assertion.\",\"analytic\"],[\"P141\",\"A claim to extraordinary knowledge does not establish access to the disputed grammatical fact.\",\"analytic\"],[\"P142\",\"At least one of Rashi's and Ramban's grammatical interpretations belongs to mesorah.\",\"hypothetical inherited-membership claim\"],[\"P143\",\"Both competing grammatical claims satisfy the transmitted-membership condition.\",\"hypothetical dual-membership claim\"],[\"P144\",\"An independently justified test of religious authority is reliable about the disputed grammar of *reishis*.\",\"analytic-conditional\"],[\"P145\",\"A later evaluator can establish that an independent test favors exactly one of the two competing grammatical interpretations.\",\"analytic-conditional\"],[\"P146\",\"A later evaluator can identify a faithfully transmitted report that favors exactly one rival on the disputed grammatical claim.\",\"hypothetical\"],[\"P147\",\"Rashi's and Ramban's grammatical teachings belong to the same inherited interpretive tradition.\",\"hypothetical shared-tradition claim\"],[\"P148\",\"Rashi lived before Ramban.\",\"historical\"],[\"P149\",\"Reasoning recovered some Torah-law knowledge that had been forgotten.\",\"source-based; split from P108\"],[\"P150\",\"Prophecy cannot independently settle a disputed halachic interpretation.\",\"source-based; split from P131\"]]")
PAIR_SCREENS = json.loads("[[\"P001\",\"P106\",\"DIRECTIONAL_ENTAILMENT\",\"P106 identifies the grammatical disagreement and thus entails the weaker P001 grammatical-disagreement description.\"],[\"P108\",\"P149\",\"TRANSMISSION_ORIGIN_BRIDGE_OPEN\",\"P149 establishes forgotten Torah-law knowledge recovered by reasoning; P108 additionally asserts prior transmission as Torah law. The latter needs an origin bridge.\"],[\"P142\",\"P143\",\"DIRECTIONAL_ENTAILMENT\",\"Both rival claims being members entails at least one is a member, but the converse fails.\"],[\"P004\",\"P140\",\"OVERLAPPING_TYPE_DISTINCTION\",\"P140 separates more types; religious authority and institutional bindingness are not automatically identical.\"],[\"P007\",\"P139\",\"SPECIALIZATION_CANDIDATE\",\"P139 is a domain-specific guarantee-boundary counterpart to P007; their logical equivalence is unproved.\"],[\"P003\",\"P005\",\"MISSING_EQUAL_EVIDENCE_BRIDGE\",\"Equal traditional standing is not identical to equal truth-relevant evidential support.\"],[\"P003\",\"P123\",\"INDEPENDENT_AXES\",\"Equal traditional standing can coexist with unequal domain-specific expertise or factual access.\"],[\"P001\",\"P107\",\"RECONCILIATION_SCOPE_OPEN\",\"Disagreement does not by itself establish incompatible truth-conditions; reconciliation requires a precise proposition alignment.\"],[\"P005\",\"P105\",\"LOGIC_REGIME_CHALLENGE\",\"Simultaneously true contradictions require a non-classical truth treatment; P005 remains a comparative-support claim.\"],[\"P103\",\"P104\",\"NON_EQUIVALENT_STATUS\",\"Recognition and religious legitimacy are distinct predicates; neither gives factual truth by definition.\"],[\"P109\",\"P110\",\"SCOPE_STRENGTH_DIFFERENCE\",\"Some halachic disputes cannot be resolved by later decisors versus no available factual method for this grammar.\"],[\"P111\",\"P112\",\"NON_EQUIVALENT_GENERATION_CORPUS\",\"Greater learning in earlier generations does not automatically give epistemic priority to an earlier corpus.\"],[\"P111\",\"P113\",\"UNLICENSED_GENERALIZATION\",\"An intergenerational learning generalization does not establish monotonic factual reliability among individual Rishonim.\"],[\"P112\",\"P113\",\"UNLICENSED_SCOPE_TRANSFER\",\"Corpus-level Torah-law priority does not give within-Rishon grammatical factual ranking.\"],[\"P113\",\"P148\",\"CONDITIONAL_RANKING_PACKAGE\",\"Chronological ordering could activate P113 only if P113's unsupported blanket rule is accepted.\"],[\"P115\",\"P134\",\"CATEGORY_MEMBERSHIP_BRIDGE\",\"A protected Mosaic category is not identical to an instantiated guarantee that covers one current grammatical claim.\"],[\"P116\",\"P137\",\"SOURCE_TRUTH_SEPARATION\",\"Faithful report transmission does not establish reliability of the report's originating source.\"],[\"P116\",\"P146\",\"REPORT_IDENTITY_GAP\",\"Generic chain fidelity does not establish that the particular identified grammar report is covered by that chain.\"],[\"P117\",\"P135\",\"MEMBERSHIP_TRUTH_SEPARATION\",\"Sufficient membership by continuity is different from a no-guarantee truth policy.\"],[\"P117\",\"P147\",\"MEMBERSHIP_APPLICATION_OPEN\",\"Sharing an inherited interpretive tradition does not specify whether each particular grammatical claim meets the membership criterion.\"],[\"P118\",\"P132\",\"NON_CONFLICT_DIFFERENT_SUBJECT\",\"Claim of untransmitted grammar can coexist with transmitted teachings concerning creation.\"],[\"P119\",\"P115\",\"CATEGORY_BOUNDARY\",\"Received-from-Sinai status is narrower than participation in inherited interpretive practice.\"],[\"P121\",\"P122\",\"CIRCULARITY_SCOPE_COMPARISON\",\"An independent authentication test is not supplied by a purely reciprocal certification model alone.\"],[\"P121\",\"P144\",\"SAME_TEST_UNLICENSED\",\"An available independent test and an independently justified reliable test need not be the same witness.\"],[\"P144\",\"P145\",\"SAME_TEST_UNLICENSED\",\"A truth-reliable test and a later evaluator's asymmetrically favoring test need not refer to the same test.\"],[\"P123\",\"P145\",\"TARGET_APPLICATION_GAP\",\"Potential epistemic advantages do not assert an actual accessible test favoring one rival.\"],[\"P124\",\"P130\",\"BINDINGNESS_ERROR_COMPATIBILITY\",\"Binding practice and possibility of erroneous rulings are compatible attributes of law.\"],[\"P125\",\"P127\",\"NOT_EQUIVALENT_INSPIRATION\",\"Wisdom-mediated access and genuinely errorless divine influx are different strength claims.\"],[\"P126\",\"P127\",\"NOT_EQUIVALENT_INSPIRATION\",\"Inspired speech below prophecy does not identify errorless cognitions.\"],[\"P128\",\"P133\",\"DOMAIN_BOUNDARY\",\"Special Torah knowledge and the disputed grammatical proposition are not automatically identical targets.\"],[\"P131\",\"P150\",\"AUTHENTICATION_VS_AUTHORITY\",\"Criteria for recognizing prophecy and limits on legal determination by prophecy address separate matters.\"],[\"P132\",\"P133\",\"TRANSMISSION_TARGET_GAP\",\"Received creation teaching does not itself entail a particular syntactic analysis.\"],[\"P134\",\"P135\",\"COMPATIBLE_CATEGORY_EXCEPTION\",\"Membership in mesorah is not automatically a guarantee, yet a narrower protected category may have one.\"],[\"P136\",\"P150\",\"FACTUAL_VS_HALACHIC_SCOPE\",\"Privileged disclosure of a grammatical fact is not the same as prophetic legal determination.\"],[\"P137\",\"P146\",\"SAME_REPORT_UNLICENSED\",\"Reliability of the original source of one faithfully transmitted report and identification of a report require a co-reference witness.\"],[\"P138\",\"P114\",\"EXPLANATION_VS_TRUTH\",\"A historical recension account can explain disagreement without establishing which grammatical view is correct.\"],[\"P139\",\"P141\",\"TRUTH_SCOPE_VS_ACCESS_SCOPE\",\"Guarantee-domain restrictions and claimed extraordinary access are independent safeguards.\"],[\"P142\",\"P147\",\"TRADITION_VS_CLAIM_MEMBERSHIP\",\"Shared inherited tradition of teachings does not trivially establish which exact disputed claims are members.\"],[\"P143\",\"P147\",\"TRADITION_VS_CLAIM_MEMBERSHIP\",\"Both interpretations meeting a transmitted-membership condition differs from their participation in a common inherited tradition.\"],[\"P110\",\"P145\",\"CONDITIONAL_COMPATIBILITY_CHALLENGE\",\"Having a one-sided test could contradict absolute no-method only when this test is warranted and truth-relevant for the same evaluator.\"]]")
RUBRICS = json.loads("[[\"SYSTEM\",[\"alternative consistent premise worlds\",\"global overstrong claims\",\"overall comparison target\",\"unexamined external assumptions\",\"independent global premise support\",\"whole-set co-reference and consistency\"]],[\"SUBSYSTEM\",[\"separate topical premise clusters\",\"overlapping category compression\",\"within-cluster scope\",\"cross-cluster relations\",\"cluster independence\",\"bridges between premise clusters\"]],[\"COMPONENT\",[\"quantifier and subject variants\",\"atomic proposition content\",\"premise's own truth conditions\",\"source-status vs asserted claim\",\"standalone claim identity\",\"compound or existential witness structure\"]],[\"INTERFACE\",[\"candidate relations between premises\",\"only licensed links\",\"source-to-fact transition\",\"premise-category translation\",\"keep relation direction explicit\",\"shared witness across premises\"]],[\"BOUNDARY_DECOMPOSITION\",[\"counterexample classes\",\"limits of modal language\",\"time and evaluator boundaries\",\"external evidence conditions\",\"scope of negation and guarantee\",\"special cases and exceptions\"]],[\"CROSS_LAYER\",[\"historical vs analytic categories\",\"collapse apparent same-property claims\",\"epistemic vs normative boundaries\",\"text tradition vs factual proposition\",\"status provenance truth separation\",\"cross-category joint constraints\"]]]")
IDS = tuple(p[0] for p in PREMISES)
SCREENS = {tuple(sorted((a,b))):(typ,reason) for a,b,typ,reason in PAIR_SCREENS}
assert len(SCREENS) == len(PAIR_SCREENS)

def frozen_objects():
    return tuple(FrozenObject(
        object_id=pid, semantic_type="PREMISE_ONLY", scope="independent source premise statement",
        target="own truth conditions and other premises ONLY",
        primitives=(claim,), dependencies=(), role="STANDALONE_DECLARATIVE_CLAIM",
        outputs=(), open_coordinates=(kind, "source and modal adequacy not certified")
    ) for pid,claim,kind in PREMISES)

class PremiseOnlyProvider:
    def joint(self,objects,*,route_id):
        witnesses=[
            ("J58_INDEPENDENT_OBJECTS",IDS,"PREMISE_ONLY_CENSUS",
             ("58 frozen premise statements; no external graph",)),
            ("J58_SAME_TEST_WITNESS",("P121","P144","P145"),"HIGHER_ARITY_COREFERENCE_GAP",
             ("Individual existence/availability/truth-reliability/warrant statements do not existentially bind the same test",)),
            ("J58_SAME_REPORT_WITNESS",("P116","P137","P146"),"HIGHER_ARITY_COREFERENCE_GAP",
             ("Report-chain preservation, originating reliability and later one-sided identification require one common report witness",)),
            ("J58_NO_METHOD_CONDITIONAL",("P110","P121","P144","P145"),"CONDITIONAL_COMPATIBILITY_TEST",
             ("No method conflicts with an accessible truth-reliable discriminator only if the witness, evaluator and target coincide",)),
            ("J58_MEMBERSHIP_SCOPES",("P115","P117","P134","P135","P142","P143","P147"),"CATEGORY_PARTITION",
             ("Membership, a privileged subclass, ordinary continuity, one-member and both-member conditions are nonidentical",)),
            ("J58_HISTORY_VS_FACT",("P108","P114","P118","P132","P133","P138","P149"),"EXPLANATORY_TARGET_BOUNDARY",
             ("Forgetting, recovery, textual provenance, creation teaching and factual grammar require typed distinctions",)),
            ("J58_AUTHENTICATION_VS_FACT",("P125","P126","P127","P128","P129","P131","P136","P141","P150"),"SCOPE_PARTITION",
             ("Kinds of inspiration, authentication, legal limits and fact coverage are not one universal reliability claim",))
        ]
        return RouteResult(route_id,"FULL_JOINT",tuple(o.object_id for o in objects),
            tuple(RelationFinding(k,tuple(s),t,tuple(g),
                ("frozen explicit premise wording",SOURCE_BLOB)) for k,s,t,g in witnesses),
            isolation_receipt="JOINT_ONLY_FROZEN_58_NO_PAIR_INPUTS")

    def pair(self,left,right,*,route_id):
        support=(left.object_id,right.object_id)
        key=tuple(sorted(support))
        typ,reason=SCREENS.get(key,("NO_LICENSED_RELATION","Pair not adjudicated beyond frozen statement comparison; OPEN, not independence"))
        f=RelationFinding("PAIR_"+support[0]+"_"+support[1],support,typ,
                          (reason,),("premise-only bounded relation screen",SOURCE_BLOB))
        return RouteResult(route_id,"PAIR",support,(f,),
                          isolation_receipt="ISOLATED_"+support[0]+"_"+support[1])

    def synthesize_pairs(self,pair_routes):
        counts=Counter(f.relation_type for r in pair_routes for f in r.findings)
        return RouteResult("SYNTH58","PAIR_SYNTHESIS",IDS,
            (RelationFinding("SYNTH58_TYPED_NETWORK",IDS,"BOUNDED_PAIR_SYNTHESIS",
                tuple(f"{k}={v}" for k,v in sorted(counts.items())),
                ("No default relation assertion for unreviewed pairs",)),),
            isolation_receipt="AFTER_1653_PAIRS_ONLY")

    def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
        return tuple(ResidualJudgment(f.finding_id,
              "PAIRWISE_RECOVERABLE" if f.finding_id=="J58_INDEPENDENT_OBJECTS" else "OPEN_REDUCIBILITY",
              ("Joint witness hypotheses are NOT independently proven irreducible",))
              for f in joint_route.findings)

    def triggered_views(self,objects,joint_route,pair_routes,pair_synthesis,residuals):
        faces=("EXPAND","CONTRACT","INWARD","OUTWARD","ISOLATE","COUPLE")
        return tuple(ViewRequest(f"{scope}_{face}",scope+"|"+face,IDS,
            description) for scope,questions in RUBRICS for face,description in zip(faces,questions))

    def analyze_view(self,request,objects):
        # Every addressed premise is examined as a separate inspectable record.
        # These are OPEN facet probes, not false source/theorem certificates.
        scope,index=request.view_id.rsplit("_",1)
        findings=tuple(RelationFinding(
            "FACE_"+request.view_id+"_"+o.object_id,(o.object_id,),"OPEN_FACE_PROBE",
            (request.reason,"Exact claim: "+o.primitives[0],
             "Kind/status: "+o.open_coordinates[0]),
            ("component premise text frozen at "+SOURCE_BLOB,))
            for o in objects)
        return RouteResult("VIEW:"+request.view_id,"VIEW",IDS,findings,
            isolation_receipt="FACE_"+request.view_id+"_58_PREMISES")

    def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
        rec=[
           ReconciledFinding("J58_INDEPENDENT_OBJECTS","CONVERGENT",
               ("independent joint and complete pair ID coverage",)),
           ReconciledFinding("SYNTH58_TYPED_NETWORK","PAIRWISE_ONLY",
               ("only screened explicit relations licensed",)),
        ]
        rec.extend(ReconciledFinding(f.finding_id,"OPEN",
               ("semantic witness or source verification still required",))
               for f in joint_route.findings if f.finding_id!="J58_INDEPENDENT_OBJECTS")
        rec.extend(ReconciledFinding(r.findings[0].finding_id,"REFINEMENT",
              ("relation type explicitly bounded; not theorem certification",))
              for r in pair_routes if r.findings[0].relation_type!="NO_LICENSED_RELATION")
        rec.extend(ReconciledFinding(f.finding_id,"OPEN",
            ("facet probe recorded for exact premise; substantive closure withheld",))
            for v in view_results for f in v.findings)
        return tuple(rec)

def test_isolated_58_premise_multiobject_full36():
    assert len(IDS)==58 and len(set(IDS))==58
    assert all(x[0].startswith("P") for x in PREMISES)
    assert all(o.dependencies==() and o.outputs==() for o in frozen_objects())
    plan=build_tool_execution_plan(CONFIGURED_RUNS["MultiObject"])
    assert plan.complete and len(plan.cells)==36
    assert len(plan.questions)==22*36 and len(plan.cognitive)==4*36
    out=run_multiobject(frozen_objects(),PremiseOnlyProvider())
    assert out.status=="OPEN" and out.blocker=="MULTIOBJECT_OPEN_PRESERVED",(out.status,out.blocker)
    assert len(out.state.pair_routes)==1653
    assert len(out.state.view_results)==36
    assert sum(len(v.findings) for v in out.state.view_results)==58*36
    assert len(out.state.joint_route.findings)==7
    assert len(out.state.residuals)==7
    assert len(out.state.pair_synthesis.findings)==1
    assert sum(r.findings[0].relation_type!="NO_LICENSED_RELATION" for r in out.state.pair_routes)==len(SCREENS)
    assert sum(r.findings[0].relation_type=="NO_LICENSED_RELATION" for r in out.state.pair_routes)==1653-len(SCREENS)
    assert len([r for r in out.state.pair_routes if r.findings[0].relation_type=="DIRECTIONAL_ENTAILMENT"])==2
    second=run_multiobject(frozen_objects(),PremiseOnlyProvider(),previous_signature=out.recurrence_signature)
    assert not second.material_delta and second.status=="OPEN" and second.state==out.state
    print("PREMISE_ONLY_58_PAIR_1653_FACE_36_OBJECT_FACE_2088_OPEN_PRESERVED")
