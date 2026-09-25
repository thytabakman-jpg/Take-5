from kernel_f1 import *

def packet(**kw):
    d=dict(referent="foundation",protected_job="preserve migration behavior",family="DIAGNOSE",
           source_scope="SYSTEM",target_scope="COMPONENT",transition_kind="PROJECT",
           breadth="CONTRACT",direction="INWARD",coupling="COUPLE",
           provenance="witness",authority="nonproduction",open_state="CLEAR")
    d.update(kw); return RunPacket(**d)

def test_legal_factored_packet():
    assert admit_run(packet()).legal

def test_transfer_or_reduction_requires_behavior_attribution():
    v=admit_run(packet(),reduction_or_transfer=True)
    assert not v.legal and "ATTRIBUTION_REQUIRED" in v.reasons
    a=Attribution("reentry","PD","HOST","matched-host-witness")
    assert admit_run(packet(attribution=a),reduction_or_transfer=True).legal

def test_open_is_preserved_as_typed_state():
    assert admit_run(packet(open_state="OPEN")).legal

def test_mode_is_three_axes_not_six_value():
    assert not admit_run(packet(breadth="EXPAND_OUTWARD")).legal

def test_material_view_or_basis_delta_forces_reentry():
    assert reentry_required(view_delta=True)
    assert reentry_required(basis_delta=True)
    assert not reentry_required()
