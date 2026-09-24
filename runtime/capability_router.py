"""Capability coverage and routing for Improvement Core / Take-5.

This module does not grant authority. It creates explicit coverage dispositions and
selects among currently executable capability programs.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

try:
    from .a5_programs import REGISTRY
except ImportError:
    from a5_programs import REGISTRY

class CoverageStatus(str, Enum):
    SELECTED="SELECTED"
    NON_APPLICABLE="NON_APPLICABLE"
    UNBOUND="UNBOUND"
    BLOCKED="BLOCKED"
    OPEN="OPEN"

@dataclass(frozen=True)
class CapabilityCoverage:
    program_id: str
    status: CoverageStatus
    reason: str

@dataclass(frozen=True)
class CoverageReceipt:
    blocker_id: str
    dispositions: tuple[CapabilityCoverage,...]

    def selected(self):
        return tuple(x.program_id for x in self.dispositions if x.status==CoverageStatus.SELECTED)

    def unexplained(self):
        return tuple(x.program_id for x in self.dispositions if x.status==CoverageStatus.OPEN)

# Trigger tags are a controller-level reconstruction of the historical V4 selection contracts.
# They are not kernel semantics and do not authorize execution.
TRIGGER_TAGS={
"C01":{"ambiguous_task","ambiguous_object"},
"C02":{"identity_risk","alias_risk","version_risk"},
"C03":{"stale_version","multiple_versions"},
"C04":{"source_to_target"},
"C05":{"improvement","transfer","goal_drift_risk"},
"C06":{"external_dependency"},
"C07":{"hidden_dependency","unexplained_result"},
"C08":{"dependency_order","multiple_dependencies"},
"C09":{"layer_conflation","control_conflation"},
"C10":{"representation_sensitive"},
"C11":{"load_bearing_uncertain","result_sensitivity"},
"C12":{"multiple_representations"},
"C13":{"attribution_conflation","bridge_conflation"},
"C14":{"formal_claim","hostile_review"},
"C15":{"novelty","prior_art"},
"C16":{"proposed_change","preservation"},
"C17":{"failure","diagnosis"},
"C18":{"repeated_failure","root_cause"},
"C19":{"unresolved_frontier","recursive_discovery"},
"C20":{"model_uncertainty","explanation_uncertainty"},
"C21":{"improvement_frontier","candidate_generation"},
"C22":{"known_defect","ceiling"},
"C23":{"proposed_transfer"},
"C24":{"diagnosed_defect","repair"},
"C25":{"redundancy","complexity"},
"C26":{"system_defect","architecture"},
"C27":{"subsystem_defect"},
"C28":{"component_defect"},
"C29":{"composition_failure","interface_loss"},
"C30":{"responsibility_duplication","hidden_responsibility"},
"C31":{"cross_layer_staleness","cross_layer_mismatch"},
"C32":{"multiple_interventions","routing"},
"C33":{"candidate_successor","strict_gain"},
"C34":{"material_change","regression"},
"C35":{"partial_order_frontier","incomparability"},
"C36":{"material_delta","architecture_delta"},
"C37":{"transfer_candidate","provenance"},
"C38":{"typed_transfer","license"},
"C39":{"licensed_transfer","target_effect"},
"C40":{"claimed_new_result","coverage"},
"C41":{"invalid_source_useful_target","rescue"},
"C42":{"completed_transfer","transfer_disposition"},
"C43":{"accepted_transfer","handoff"},
"C44":{"candidate_change","verification"},
"C45":{"generalization_claim","holdout"},
"C46":{"causal_claim","ablation"},
"C47":{"closure_claim","maximality_claim"},
"C48":{"ceiling_frontier","raise_ceiling"},
"C49":{"broad_corpus","unknown_location"},
}

def coverage(blocker_id:str, tags:Iterable[str], *, licensed:Iterable[str]|None=None)->CoverageReceipt:
    tagset=set(tags)
    licensed_set=None if licensed is None else set(licensed)
    rows=[]
    for pid in sorted(REGISTRY.ids()):
        triggers=TRIGGER_TAGS.get(pid)
        if not triggers:
            rows.append(CapabilityCoverage(pid,CoverageStatus.OPEN,"missing trigger contract"))
            continue
        relevant=bool(tagset & triggers)
        if not relevant:
            rows.append(CapabilityCoverage(pid,CoverageStatus.NON_APPLICABLE,"trigger not matched"))
            continue
        spec=REGISTRY.get(pid)
        if not spec.executable:
            rows.append(CapabilityCoverage(pid,CoverageStatus.UNBOUND,"semantic capability has no runtime adapter"))
            continue
        if licensed_set is not None and pid not in licensed_set:
            rows.append(CapabilityCoverage(pid,CoverageStatus.BLOCKED,"capability not licensed for this episode"))
            continue
        rows.append(CapabilityCoverage(pid,CoverageStatus.SELECTED,"relevant, executable, and licensed"))
    return CoverageReceipt(blocker_id,tuple(rows))

def closure_allowed(receipt:CoverageReceipt)->bool:
    """Coverage closure only. Result/verification closure remains separate."""
    return not receipt.unexplained() and not any(
        x.status==CoverageStatus.UNBOUND for x in receipt.dispositions
        if x.reason.startswith("semantic capability")
    )
