from scope_mode_36 import *
from scope_ontology import Scope
from run_geometry import Mode,ModeFace

def test_controller_lattice_is_36():
    assert len(cells36())==36

def test_complete_runtime_mode_activates_three_faces_at_one_scope():
    active=active_cells(Scope.SYSTEM,Mode("EXPAND","OUTWARD","ISOLATE"))
    assert len(active)==3
    assert set(f for _,f in active)=={ModeFace.EXPAND,ModeFace.OUTWARD,ModeFace.ISOLATE}

def test_open_cell_blocks_claimed_closure():
    c=(Scope.SYSTEM,ModeFace.EXPAND)
    ledger={c:CoverageCell(*c,"OPEN","candidate universe unresolved")}
    assert not closure_legal((c,),ledger)

def test_typed_nonapplicable_can_close():
    c=(Scope.COMPONENT,ModeFace.OUTWARD)
    ledger={c:CoverageCell(*c,"NOT_APPLICABLE","frozen local pure function")}
    assert closure_legal((c,),ledger)
