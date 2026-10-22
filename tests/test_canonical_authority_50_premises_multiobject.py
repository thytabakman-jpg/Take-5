"""Native Take-5 MultiObject integration run for Canonical Authority 50-premise snapshot.

This test invokes runtime/multiobject.py directly, NOT a semantic observer.
The attached provider exposes documented premise co-occurrence and dependency gaps.
Its semantic/novelty status is deliberately OPEN, not a source-validation certificate.
Source: thytabakman-jpg/Reaserch/projects/canonical-authority/research/ALL_ROADS_PREMISE_INFERENCE_COMMITMENT_ATLAS.md
Source blob SHA: 046edfadd54842ff2c8fae3450193d4cf6ab98d0
"""
import sys
import json
from collections import Counter
from itertools import combinations

sys.path.insert(0, "runtime")
from multiobject import (
    FrozenObject, RelationFinding, RouteResult, ResidualJudgment,
    ViewRequest, ReconciledFinding, run_multiobject,
)

PREMISES = [["P001","Rashi and Ramban advance incompatible claims concerning the construct-state behaviour of *reishit* in the fixed Bereishis 1:1 dispute.","case","Current fixed-target contract; Rashi and Ramban on Bereishis 1:1."],["P002","Both Rashi and Ramban possess the recognized traditional standing at issue in the comparison.","case","Current approved thesis."],["P003","The traditional standing invoked for both rivals, insofar as it bears equally on their claims, does not differ between them.","analytic","Current approved thesis, conditional equal-standing premise."],["P004","The question under examination is whether a later evaluator can justifiably favour one incompatible factual claim as true, rather than merely settle practice or confer legitimacy.","analytic","Current approved thesis and question."],["P005","A reason that supports two incompatible rivals only in the same respect and to the same comparative degree does not, solely on that basis, rationally favour either rival over the other.","analytic","Comparative-support principle, analytic reconstruction."],["P006","For a later evaluator's preference to be justified, the evaluator needs adequate grounds to identify and use the consideration invoked for that preference.","analytic","Evaluator-warrant condition, approved thesis."],["P007","A source's success in its native domain does not itself establish a warranted relation to a different factual proposition without a licensed source-to-target connection.","analytic","Typed source-to-target control, SOURCE_MODULES.yaml."],["P008","On the presently admitted source and relation basis, no tested source package has established a warranted route to the fixed grammatical proposition that settles the Rashi–Ramban comparison.","bounded","Current bounded case result; §5.2 remains research-open."],["P101","Genuine incompatible factual assertions occur recurrently among recognized canonical authorities.","historical","Legacy road 1; historical exemplars require individual verification."],["P102","The specified downstream conclusion remains the same whether Rashi's grammatical assertion or Ramban's is true.","conditional","Legacy road 2; premise is restricted to the specified downstream conclusion."],["P103","A pluralist source can recognize opposed rabbinic teachings while preserving the rule that incompatible factual propositions cannot both be true in the same respect.","source-based","Eruvin 13b/Ritva as interpreted in legacy road 3; application qualified."],["P104","Two incompatible interpretations can both retain religious or canonical legitimacy.","conditional","Legacy road 4; exact legitimacy model must be source-indexed."],["P105","Two directly contradictory propositions are both true in precisely the same respect and sense.","hypothetical","Legacy road 5; hypothetical expansive pluralism, no locked historical attribution."],["P106","Ramban explicitly presents his grammatical analysis as disagreeing with Rashi's analysis.","source-based","Ramban on Bereishis 1:1."],["P107","A proposed reconciliation treats Rashi's and Ramban's disputed claims as compatible.","hypothetical","Legacy road 6; model-dependent, requires textual argument."],["P108","Some Torah-law or inferential material was forgotten after transmission and some of it was subsequently recovered through reasoning.","source-based","b. Temurah 16a; does not establish loss of the specific Hebrew grammar."],["P109","Some later authorities regard themselves or their generation as unable to independently resolve specified earlier halachic disputes on the merits.","source-based","Beit Yosef Introduction; Maharik shoresh 161, restricted domain."],["P110","A specified later evaluator has no possible truth-relevant method for knowing which earlier factual proposition is true.","unsupported","Old global unknowability proposal; direct source missing."],["P111","Traditional sources compare certain earlier rabbinic generations favourably to later generations in cognitive ability or learning.","source-based","b. Eruvin 53a; Shabbat 112b; scope limited."],["P112","An epochal hierarchy can accord an earlier authoritative corpus truth-priority over a later corpus in a defined Torah domain.","source-based","Chazon Ish, Kovetz Igrot II, letter 24; does not rank Rashi above Ramban."],["P113","Within the Rishonic period, the earlier individual is more factually reliable than the later individual merely because of chronological priority.","unsupported","Old monotonic intra-Rishon hypothesis; no publication-ready source."],["P114","Re'em proposes that Ramban may have seen a version of Rashi lacking the answer to the Yeshayahu 46:10 challenge.","source-based","Re'em (Eliyahu Mizrahi), commentary on Rashi to Bereishis 1:1."],["P115","Rambam distinguishes genuinely received Mosaic interpretation from subsequently derived interpretive conclusions, and genuine disputes do not occur within his genuinely received Mosaic category.","source-based","Rambam, Introduction to the Mishnah; Hilkhot Mamrim 1:3."],["P116","Rabbi Yehudah Halevi treats qualifying many-to-many inherited transmission as a reliability mechanism for preservation of reports.","source-based-qualified","Kuzari III; exact passage and tawatur scholarly citation still require lock."],["P117","Mesorah can be defined broadly by inherited continuity of texts, practices and traditions, independently of a guarantee that every inherited assertion is true.","pending","Modern broad-continuity model; explicit primary formulation unverified."],["P118","The particular grammatical knowledge relevant to the Rashi–Ramban dispute was never included in the invoked transmitted content.","unsupported","Legacy D2a; no direct source support."],["P119","Inherited participation in later Torah interpretation and membership in Rambam's narrowly protected Mosaic received-content category are distinct properties.","source-based-qualified","Rambam distinction supported; broad mesorah membership needs independent model."],["P120","A transmitted traditional method of Torah study can itself qualify as an element of mesorah.","pending","Attributed to R. Joseph B. Soloveitchik; primary 'Shenei Sugei Masoret' passage pending."],["P121","A specified authenticity property X can be identified independently of an appeal to the authority whose authenticity it is intended to establish.","analytic-conditional","Analytic truth-relevant-X hypothesis; not a named historical doctrine."],["P122","A proposed authentication model recognises the correct authorities solely through authentic mesorah, and the correct mesorah solely through those authorities.","analytic-conditional","Pure reciprocity test model; not a universal allegation against Jewish views."],["P123","One rival may have independently evidenced superiority in domain-specific expertise, reliability, information or access.","general-epistemic","Contemporary social epistemology; not an actual Rashi/Ramban asymmetry."],["P124","A halachic process can determine binding practice despite persisting disagreement about underlying factual or interpretive matters.","source-based-qualified","Halachic determination and contemporary Jewish-law scholarship."],["P125","Ramban recognises a wisdom-mediated mode of Ruach HaKodesh through which a sage can gain some truth after ordinary prophecy has ceased.","source-based","Ramban on b. Bava Batra 12a; episodic and domain-limited."],["P126","Rambam distinguishes sub-prophetic inspired speech or composition from full prophecy.","source-based","Guide of the Perplexed II:45."],["P127","Ramchal describes an epistemic state of divine influx in which the knowledge genuinely received is clear and without error.","source-based","Derekh Hashem, relevant Ruach HaKodesh discussion; edition/page lock useful."],["P128","The Lurianic/Vital tradition treats Ruach HaKodesh as a potential route to esoteric Torah knowledge while recognising the need to distinguish genuine from false claims of such access.","source-based","R. Chaim Vital, Shaarei Kedusha; supported esoteric domain."],["P129","Certain specified rabbinic writings possess an extraordinary divine truth-alignment beyond ordinary authorship.","pending","Reported Tummim/Divrei Chaim sources; primary verification pending."],["P130","Traditional legal sources recognise the possibility of erroneous authoritative institutional rulings and regulate their consequences.","source-based","b. Horayot 2b and associated halachic material."],["P131","Jewish sources supply criteria for authenticated prophecy and limits on what prophetic authority can decide.","source-based","Rambam, Hilkhot Yesodei HaTorah 9–10."],["P132","Ramban invokes received or esoteric knowledge about creation and separately articulates a reading of Bereishis 1:1.","source-based","Ramban on Bereishis 1:1; native receipt and peshat/sod distinction."],["P133","The currently reviewed Ramban creation-tradition sources have not established that the particular construct-state proposition is included in, or warranted by, the received esoteric knowledge.","bounded","H_R research, §5.2 source relation still open."],["P134","A specified correctness-guaranteeing tradition genuinely contains one of the disputed factual propositions within its protected domain.","hypothetical","Historical guarantee-includes-target counterfactual; not supplied by Rambam's actual disputed-content rule."],["P135","A stipulated mesorah membership rule treats transmitted content as traditional without thereby guaranteeing its factual correctness.","hypothetical","Legacy road 13, pure no-guarantee conditional."],["P136","A uniquely authenticated prophetic or otherwise privileged disclosure genuinely covers the exact disputed proposition and favours one rival.","hypothetical","Positive control conditional; not established in Rashi/Ramban."],["P137","The source who originates a faithfully transmitted report is reliable about the very proposition reported.","hypothetical","Needed source-reliability bridge for Halevi-type transmission success."],["P138","A historical disagreement can have an explanation of how it arose without thereby having an answer to which incompatible factual assertion is true.","analytic","Explanation-versus-adjudication distinction."],["P139","A source's correctness in a protected domain cannot be transferred to content outside that domain solely because the wider tradition contains both.","analytic","Scope relation; not a claim that outside content is false."],["P140","Institutional bindingness, canonical legitimacy, authenticated provenance and descriptive truth are different outputs unless a source-grounded relation makes one evidentially relevant to another.","analytic","Source-native output separation."],["P141","An assertion of extraordinary epistemic access does not independently establish that the claimant had that access concerning the proposition being assessed.","analytic","Authentication and proposition-scope constraint."],["P142","One of the two incompatible rivals meets the broad inherited-membership condition while both remain genuinely inconsistent on the fixed factual proposition.","conditional","Conditional dual-membership variant, not a historical existential assertion."]]
INFERENCES = [["I001",["P002","P003","P005"],"Shared standing, insofar as it bears equally, cannot by itself confer comparative epistemic preference.  "],["I002",["P004","P005"],"A justified comparative factual preference requires a difference bearing on which rival is true, beyond any feature that supports both only equally.  "],["I003",["P006","I002"],"A differential consideration does not justify the later evaluator's preference without adequate grounds to identify and use it.  "],["I004",["I001","I002","I003"],"The common warranted-discriminator requirement B0 follows from the declared comparison kernel; this is a common analytic dependence, not thirty-three independent proofs.  "],["I005",["P007","P140"],"A native-domain success does not become evidence for the grammar target until its source-to-target relation is warranted.  "],["I006",["P008","I005"],"On the presently tested source and relation basis, the fixed-case factual selector remains unestablished; stronger universal impossibility does not follow.  "],["I101",["P101","P001"],"A genuine canonical factual contradiction entails that at least one of the incompatible assertions is false, but recurrence alone does not identify it.  "],["I102",["P102","P004"],"Independence of the specified downstream conclusion from the grammar leaves the grammar's truth question unanswered.  "],["I103",["P103","P001"],"Preserving both sides' canonical standing under non-contradiction does not make both incompatible factual propositions true.  "],["I104",["P104","P001"],"Legitimacy of both interpretive positions need not entail truth of both incompatible factual propositions.  "],["I105",["P105","P001"],"Granting simultaneous same-respect truth for P and not-P rejects classical non-contradiction for the relevant domain and moves the disagreement to that governing principle.  "],["I106",["P106","P107"],"If the reconciliation is correct, Ramban's explicit characterization of at least one feature of the dispute must be corrected or differently interpreted.  "],["I107",["P108","P138"],"Evidence that some Torah knowledge was lost and reconstructed explains a possible mechanism of disagreement without identifying which present reconstruction is true.  "],["I108",["P109","P124"],"Restricted incapacity for independent merits-adjudication is consistent with a distinct route to binding halachic practice.  "],["I109",["P110","P004"],"If genuine global unknowability held for this target and evaluator, no currently usable factual discriminator would be available to that evaluator.  "],["I110",["P111","P005"],"Intergenerational cognitive differences alone do not establish which Rishon is more reliable about this particular grammatical proposition.  "],["I111",["P112","P139"],"Epochal corpus priority can be a differential reason across its supported corpus boundary, but cannot rank two Rishonim within the same corpus without an additional premise.  "],["I112",["P113","P001"],"If the unsupported chronological rule were established for this domain, Rashi's temporal priority could generate a candidate reliability asymmetry.  "],["I113",["P114","P138"],"The suggested missing recension can explain Ramban's treatment of Rashi without resolving which grammatical generalization is true.  "],["I114",["P115","P001","P139"],"Under Rambam's category rule, a genuine dispute places the disputed interpretation outside the protected Mosaic received-content category rather than identifying either disputant as the protected winner.  "],["I115",["P116","P137"],"A qualifying many-to-many chain preserves a source report; a justified inference from that report to the truth of P additionally requires source reliability about P.  "],["I116",["P117","P003"],"Inherited continuity as a common membership property cannot by itself distinguish the factual truth of rival inherited propositions.  "],["I117",["P118","P139"],"If the grammar was not transmitted, correctness attributed to the transmitted category cannot decide that untransmitted grammar.  "],["I118",["P115","P119"],"Participation in later inherited interpretive practice does not entail membership in the narrow category protected as genuine Mosaic reception.  "],["I119",["P120","P140"],"A transmitted study method can establish methodological traditionality while leaving the factual truth of any particular output open.  "],["I120",["P121","P005"],"An independently identifiable, truth-tracking and rival-asymmetric X can do the selecting; the label 'authentic mesorah' adds no further discriminatory evidence.  "],["I121",["P122","P005"],"A purely reciprocal authority–mesorah certification pair with no independent asymmetry can be mirrored by a competing pair and cannot discriminate between them on that basis alone.  "],["I122",["P123","P006"],"An independently grounded, proposition-relevant epistemic advantage can justify a comparative preference when the evaluator can properly identify and use it.  "],["I123",["P124","P140"],"A normatively binding decision does not, without a further truth-directed connection, establish the descriptive truth of the selected view.  "],["I124",["P125","P141"],"Possible sage-wisdom access to truth does not establish universal, continuous, or proposition-specific infallibility of a named commentator.  "],["I125",["P126","P140"],"Inspired composition below prophecy does not on its own guarantee the truth of every proposition in the composition.  "],["I126",["P127","P141"],"The guaranteed truth of an authentically errorless cognition is useful for this dispute only if the claimant, possession and proposition-specific coverage are established.  "],["I127",["P128","P141"],"Restricted access to esoteric meaning cannot automatically determine an ordinary grammatical target, and claims of access require authentication.  "],["I128",["P129","P141"],"Exceptional truth-alignment of a specified work, if established, would require proof that the relevant disputed proposition is covered by the aligned output.  "],["I129",["P130","P140"],"Institutional authority can remain operative in a system that makes provision for authoritative factual or legal error.  "],["I130",["P131","P136","P006"],"An authenticated, proposition-covering privileged disclosure could settle the rival factual comparison; the present case has no established instance of that coverage.  "],["I131",["P132","P133","P007"],"Ramban's verse-proximate received creation knowledge does not currently yield a warranted inference to his particular grammatical proposition.  "],["I132",["P134","P005"],"A genuine target-covering correctness guarantee would favour the identified protected rival only if its membership and one-sided application were warranted.  "],["I133",["P135","P142"],"Under a common transmitted-membership condition without a truth guarantee, contradictory transmitted claims could both qualify even though they cannot both be factually true.  "],["I134",["P103","P104"],"Canonical standing under a non-contradiction model and religious legitimacy are related but different grounds; neither may be silently substituted for the other.  "],["I135",["P111","P112"],"A general assertion of generational cognitive decline and a specific epochal corpus truth-priority are different claims requiring different bridge premises.  "],["I136",["P115","P116"],"Protected Mosaic received-content classification and concurrent-chain reliability are different mesorah mechanisms with different success conditions.  "]]
ROADS = [["R001",["P001","P002","P003","P004","P005","P006","P007","P101"],["I001","I002","I003","I004","I005","I101"]],["R002",["P001","P002","P003","P004","P005","P006","P007","P102"],["I001","I002","I003","I004","I005","I102"]],["R003",["P001","P002","P003","P004","P005","P006","P007","P103"],["I001","I002","I003","I004","I005","I103","I134"]],["R004",["P001","P002","P003","P004","P005","P006","P007","P104"],["I001","I002","I003","I004","I005","I104","I134"]],["R005",["P001","P002","P003","P004","P005","P006","P007","P105"],["I001","I002","I003","I004","I005","I105"]],["R006",["P001","P002","P003","P004","P005","P006","P007","P106","P107"],["I001","I002","I003","I004","I005","I106"]],["R007",["P001","P002","P003","P004","P005","P006","P007","P108"],["I001","I002","I003","I004","I005","I107"]],["R008",["P001","P002","P003","P004","P005","P006","P007","P109","P124"],["I001","I002","I003","I004","I005","I108"]],["R009",["P001","P002","P003","P004","P005","P006","P007","P110"],["I001","I002","I003","I004","I005","I109"]],["R010",["P001","P002","P003","P004","P005","P006","P007","P111"],["I001","I002","I003","I004","I005","I110","I135"]],["R011",["P001","P002","P003","P004","P005","P006","P007","P112"],["I001","I002","I003","I004","I005","I111","I135"]],["R012",["P001","P002","P003","P004","P005","P006","P007","P113"],["I001","I002","I003","I004","I005","I112"]],["R013",["P001","P002","P003","P004","P005","P006","P007","P114","P138"],["I001","I002","I003","I004","I005","I113"]],["R014",["P001","P002","P003","P004","P005","P006","P007","P115"],["I001","I002","I003","I004","I005","I114","I136"]],["R015",["P001","P002","P003","P004","P005","P006","P007","P116","P137"],["I001","I002","I003","I004","I005","I115","I136"]],["R016",["P001","P002","P003","P004","P005","P006","P007","P117"],["I001","I002","I003","I004","I005","I116"]],["R017",["P001","P002","P003","P004","P005","P006","P007","P118"],["I001","I002","I003","I004","I005","I117"]],["R018",["P001","P002","P003","P004","P005","P006","P007","P119","P115"],["I001","I002","I003","I004","I005","I118"]],["R019",["P001","P002","P003","P004","P005","P006","P007","P120"],["I001","I002","I003","I004","I005","I119"]],["R020",["P001","P002","P003","P004","P005","P006","P007","P121"],["I001","I002","I003","I004","I005","I120"]],["R021",["P001","P002","P003","P004","P005","P006","P007","P122"],["I001","I002","I003","I004","I005","I121"]],["R022",["P001","P002","P003","P004","P005","P006","P007","P123"],["I001","I002","I003","I004","I005","I122"]],["R023",["P001","P002","P003","P004","P005","P006","P007","P124"],["I001","I002","I003","I004","I005","I123"]],["R024",["P001","P002","P003","P004","P005","P006","P007","P125"],["I001","I002","I003","I004","I005","I124"]],["R025",["P001","P002","P003","P004","P005","P006","P007","P126"],["I001","I002","I003","I004","I005","I125"]],["R026",["P001","P002","P003","P004","P005","P006","P007","P127"],["I001","I002","I003","I004","I005","I126"]],["R027",["P001","P002","P003","P004","P005","P006","P007","P128"],["I001","I002","I003","I004","I005","I127"]],["R028",["P001","P002","P003","P004","P005","P006","P007","P129"],["I001","I002","I003","I004","I005","I128"]],["R029",["P001","P002","P003","P004","P005","P006","P007","P130"],["I001","I002","I003","I004","I005","I129"]],["R030",["P001","P002","P003","P004","P005","P006","P007","P131","P136"],["I001","I002","I003","I004","I005","I130"]],["R031",["P001","P002","P003","P004","P005","P006","P007","P132","P133"],["I001","I002","I003","I004","I005","I131"]],["R032",["P001","P002","P003","P004","P005","P006","P007","P134"],["I001","I002","I003","I004","I005","I132"]],["R033",["P001","P002","P003","P004","P005","P006","P007","P135","P142"],["I001","I002","I003","I004","I005","I133"]]]
P_BY_ID = {p[0]: p for p in PREMISES}
I_BY_ID = {i[0]: i for i in INFERENCES}
R_BY_ID = {r[0]: r for r in ROADS}
SUPPORT = tuple(p[0] for p in PREMISES)
KNOWN_BOUNDARIES = (
    ("P103", "P105", "noncontradiction versus expansive same-respect truth"),
    ("P109", "P110", "restricted legal merits incapacity versus global unknowability"),
    ("P111", "P113", "generational cognitive comparison versus unsupported within-Rishon chronology"),
    ("P115", "P134", "Rambam actual category rule versus hypothetical guarantee that covers the disputed target"),
    ("P116", "P137", "faithful chain versus reliability of its first source"),
    ("P118", "P119", "never transmitted versus transmitted but not protected"),
    ("P135", "P142", "membership for one rival insufficient to establish membership for two"),
)
BOUNDARY_LOOKUP = {
    tuple(sorted((a, b))): reason for a, b, reason in KNOWN_BOUNDARIES
}

def premise_closure(inference_id, visited=None):
    if visited is None:
        visited = set()
    if inference_id in visited:
        return set()
    visited.add(inference_id)
    result = set()
    for dep in I_BY_ID[inference_id][1]:
        if dep.startswith("P"):
            result.add(dep)
        else:
            result.update(premise_closure(dep, visited))
    return result

def dependency_gaps():
    output = {}
    for road_id, stated, infer_ids in ROADS:
        used = set()
        for inf_id in infer_ids:
            used.update(premise_closure(inf_id))
        missing = sorted(used - set(stated))
        if missing:
            output[road_id] = missing
    return output

def coinputs():
    index = {}
    for iid, input_ids, _ in INFERENCES:
        premises = [x for x in input_ids if x.startswith("P")]
        for a, b in combinations(premises, 2):
            index.setdefault(tuple(sorted((a, b))), []).append(iid)
    return index

COINPUT = coinputs()
CO_ROAD = {}
for rid, premids, _ in ROADS:
    # The seven common kernel premises are tagged in every road, but such
    # methodological co-occurrence does not establish source-level dependence.
    extra = [p for p in premids if p not in SUPPORT[:7]]
    for a,b in combinations(extra,2):
        CO_ROAD.setdefault(tuple(sorted((a,b))), []).append(rid)

def frozen_objects():
    return tuple(
        FrozenObject(
            object_id=id,
            semantic_type="PREMISE_"+kind.upper().replace("-", "_"),
            scope="reconstructed Canonical Authority 2026-10-22 snapshot",
            target="B0 structural condition and route-native outputs",
            primitives=(statement,),
            dependencies=tuple(
                iid for iid,inputs,_ in INFERENCES if id in inputs
            ),
            role="SOURCE_OR_ANALYTIC_PREMISE",
            outputs=tuple(
                rid for rid,stated,_ in ROADS if id in stated
            ),
            open_coordinates=("primary source / logical sufficiency" if
                              kind in ("pending","unsupported","hypothetical")
                              else (),) if kind in ("pending","unsupported","hypothetical") else (),
        )
        for id,statement,kind,basis in PREMISES
    )

class PremiseRelationProvider:
    """Scope-limited provider. No model generated claim is certified as historical truth."""

    def joint(self, objects, *, route_id):
        ids=tuple(o.object_id for o in objects)
        statuses=Counter(p[2] for p in PREMISES)
        gaps=dependency_gaps()
        findings=(
            RelationFinding(
                "J50_SOURCE_TYPED_INVENTORY", ids, "JOINT_CENSUS",
                ("distinct premises "+str(len(ids)),
                 "status distribution "+json.dumps(dict(sorted(statuses.items())),sort_keys=True)),
                ("Reaserch source snapshot SHA 046edfadd54842ff2c8fae3450193d4cf6ab98d0",)),
            RelationFinding(
                "J50_UNDISCLOSED_PREMISE_DEPENDENCIES", ids, "JOINT_DEPENDENCY_GAP",
                ("roads with non-closed declared premise dependencies "+str(len(gaps)),
                 "P140 missing from "+str(sum("P140" in g for g in gaps.values()))+" roads"),
                ("full closure over original declared inference DAG",)),
        )
        return RouteResult(route_id, "FULL_JOINT", ids, findings,
            isolation_receipt="NATIVE_INDEPENDENT_FULL_JOINT_FROM_50_FROZEN_PREMISE_PACKETS")

    def pair(self,left,right,*,route_id):
        a,b=left.object_id,right.object_id
        key=tuple(sorted((a,b)))
        relation="NO_LICENSED_RELATION"
        grounds=()
        if key in BOUNDARY_LOOKUP:
            relation="SEMANTIC_BOUNDARY_CHALLENGE"
            grounds=(BOUNDARY_LOOKUP[key], "review, not established contradiction")
        elif key in COINPUT:
            relation="SHARED_EXPLICIT_INFERENCE_INPUT"
            grounds=tuple(COINPUT[key])
        elif key in CO_ROAD:
            relation="CO_OCCURS_IN_ONE_ROAD"
            grounds=tuple(CO_ROAD[key])
        finding=RelationFinding("PAIR_"+a+"_"+b,(a,b),relation,grounds,
            ("Reaserch atlas stated IDs; no free semantic inference",))
        return RouteResult(route_id,"PAIR",(a,b),(finding,),
            isolation_receipt="ISOLATED_"+a+"_"+b+"_FROM_FROZEN_PAIR_PACKET")

    def synthesize_pairs(self,pair_routes):
        classes=Counter(f.relation_type for r in pair_routes for f in r.findings)
        finding=RelationFinding("S50_PAIRWISE_NETWORK",SUPPORT,"PAIRWISE_SYNTHESIS",
            ("complete pair basis "+str(len(pair_routes)),
             "classes "+json.dumps(dict(sorted(classes.items())),sort_keys=True)),
            ("complete native unordered pair route census",))
        return RouteResult("S50_PAIRS","PAIR_SYNTHESIS",SUPPORT,(finding,),
            isolation_receipt="NATIVE_SYNTHESIS_AFTER_1225_ISOLATED_PAIR_ROUTES")

    def challenge_reducibility(self,joint_route,pair_routes,pair_synthesis):
        return (
            ResidualJudgment("J50_SOURCE_TYPED_INVENTORY","PAIRWISE_RECOVERABLE",
                ("individual object types and complete pair coverage preserve census",)),
            ResidualJudgment("J50_UNDISCLOSED_PREMISE_DEPENDENCIES","OPEN_REDUCIBILITY",
                ("the road-and-inference incidence hypergraph is external to 2-object co-occurrence",
                 "no minimal 3-plus witness or mathematical irreducibility proof supplied")),
        )

    def triggered_views(self,objects,joint_route,pair_routes,pair_synthesis,residuals):
        return (
            ViewRequest("P140_CLOSURE","INFERENCE_CLOSURE",("P007","P140"),
                "P140 required by the common I005 while absent in every printed road"),
            ViewRequest("ONE_V_TWO_MEMBERSHIP","LOGICAL_QUANTIFIER",("P135","P142"),
                "P142 supplies membership for one rival, I133 claims both qualify"),
            ViewRequest("RECEPTION_COUNTERFACTUAL","HISTORICAL_SCOPE",("P115","P134"),
                "Rambam actual received-content classification differs from a target-covering guarantee hypothetical"),
        )

    def analyze_view(self,request,objects):
        return RouteResult("VIEW:"+request.view_id,"VIEW",tuple(request.support),
            (RelationFinding("VIEW_FINDING_"+request.view_id,tuple(request.support),
               "REQUIRES_SUBSTANTIVE_REVIEW",(request.reason,),
               ("typed view request from source-bound explicit relation",)),),
            isolation_receipt="ISOLATED_VIEW_"+request.view_id)

    def reconcile(self,pair_routes,pair_synthesis,joint_route,residuals,view_results):
        out=[
            ReconciledFinding("J50_SOURCE_TYPED_INVENTORY","CONVERGENT",
                ("full joint and all pair routes agree on 50 identifiers",)),
            ReconciledFinding("J50_UNDISCLOSED_PREMISE_DEPENDENCIES","OPEN",
                ("all road dependencies require repair before proof certificates",)),
            ReconciledFinding("S50_PAIRWISE_NETWORK","PAIRWISE_ONLY",
                ("summary only; no higher-order proof asserted",)),
        ]
        for r in pair_routes:
            for f in r.findings:
                if f.relation_type!="NO_LICENSED_RELATION":
                    out.append(ReconciledFinding(f.finding_id,"REFINEMENT",
                        ("source-declared co-input/co-road/boundary only",)))
        for r in view_results:
            for f in r.findings:
                out.append(ReconciledFinding(f.finding_id,"OPEN",
                    ("requires further logical or philological inspection",)))
        return tuple(out)

def test_canonical_authority_50_premises_1225_native_pairs():
    assert len(PREMISES)==50
    assert len(INFERENCES)==42
    assert len(ROADS)==33
    assert len(set(SUPPORT))==50
    assert set("P001 P002 P003 P004 P005 P006 P007".split()) <= set(SUPPORT)
    assert set("P139 P140 P141".split()) <= set(SUPPORT)
    assert sum("P140" in x for x in dependency_gaps().values())==33
    assert len(dependency_gaps())==33
    result=run_multiobject(frozen_objects(),PremiseRelationProvider())
    assert result.status=="OPEN", (result.status,result.blocker)
    assert result.blocker=="MULTIOBJECT_OPEN_PRESERVED"
    assert len(result.state.objects)==50
    assert result.state.joint_route.status=="EXECUTED"
    assert len(result.state.pair_routes)==1225
    assert all(r.status=="EXECUTED" and r.isolation_receipt for r in result.state.pair_routes)
    assert result.state.pair_synthesis.status=="EXECUTED"
    assert len(result.state.residuals)==2
    assert len(result.state.view_results)==3
    assert all(r.status=="EXECUTED" for r in result.state.view_results)
    assert result.material_delta
    recurrence=run_multiobject(frozen_objects(),PremiseRelationProvider(),
                               previous_signature=result.recurrence_signature)
    assert recurrence.status=="OPEN"
    assert not recurrence.material_delta
    assert recurrence.state==result.state
