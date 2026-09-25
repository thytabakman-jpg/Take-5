from run_geometry import Mode,ModeFace,scope_edges,face_cells,full_mode_cells,RunCoordinate
from scope_ontology import Scope,Handoff

def test_directed_scope_surface_is_36():
    assert len(scope_edges())==36

def test_six_by_six_by_six_face_surface_is_216():
    assert len(face_cells())==216

def test_full_cube_modes_are_eight_per_scope_edge():
    assert len(full_mode_cells())==36*8

def test_complete_mode_has_three_active_faces():
    assert Mode("EXPAND","OUTWARD","ISOLATE").faces()=={
        ModeFace.EXPAND,ModeFace.OUTWARD,ModeFace.ISOLATE}

def test_scope_direction_and_mode_are_separate():
    r=RunCoordinate("ROOT_CAUSE",Scope.COMPONENT,Scope.SYSTEM,
                    Mode("CONTRACT","INWARD","COUPLE"))
    assert r.transition_kind==Handoff.LIFT
    assert ModeFace.CONTRACT in r.mode.faces()
