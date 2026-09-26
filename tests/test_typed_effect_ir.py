from function_ir_holdouts import CONTRACTS,PROGRAMS,tool_conductor_program,validate_holdouts
from tool_run_registry import MATERIAL_TOOLS
from typed_effect_ir import NodeKind,atom,validate

def test_all_heterogeneous_holdouts_validate():
    receipts=validate_holdouts()
    assert set(receipts)==set(PROGRAMS)
    assert all(r.valid for r in receipts.values()),{k:r.errors for k,r in receipts.items() if not r.valid}

def test_no_holdout_hides_whole_tool_as_atom():
    for name,builder in PROGRAMS.items():
        node=builder()
        receipt=validate(node,CONTRACTS[name])
        assert receipt.valid
        atom_names={n.name for n in node.walk() if n.kind is NodeKind.ATOM}
        assert not (atom_names & set(CONTRACTS[name].forbidden_atomic_names))

def test_tool_conductor_product_covers_current_registry_exactly_once():
    node=tool_conductor_program()
    products=[n for n in node.walk() if n.kind is NodeKind.PRODUCT]
    assert len(products)==1
    refs=[c.name.removeprefix("ToolRef:") for c in products[0].children]
    assert tuple(refs)==tuple(MATERIAL_TOOLS)
    assert len(refs)==len(set(refs))

def test_wrapper_omission_changes_hash_and_fails_contract():
    node=PROGRAMS["MT"]()
    baseline=validate(node,CONTRACTS["MT"])
    assert baseline.valid
    def strip_ftw(n):
        if n.kind is NodeKind.TRANSFORM and n.name=="FTW":
            return strip_ftw(n.children[0])
        return type(n)(n.kind,n.name,n.input_type,n.output_type,n.effects,
                       tuple(strip_ftw(c) for c in n.children))
    stripped=strip_ftw(node)
    receipt=validate(stripped,CONTRACTS["MT"])
    assert not receipt.valid
    assert "MISSING_REQUIRED_TRANSFORM:FTW" in receipt.errors
    assert receipt.semantic_hash!=baseline.semantic_hash

def test_whole_tool_atom_is_rejected():
    receipt=validate(atom("ICC123"),CONTRACTS["ICC123"])
    assert not receipt.valid
    assert "WHOLE_TOOL_HIDDEN_AS_ATOM:ICC123" in receipt.errors

def test_branch_selector_and_loop_guard_are_explicit():
    ic=PROGRAMS["ImprovementCore"]()
    nodes=ic.walk()
    branches=[n for n in nodes if n.kind is NodeKind.BRANCH]
    loops=[n for n in nodes if n.kind is NodeKind.LOOP]
    assert len(branches)==1
    assert branches[0].children[0].name=="ImprovementCoreEntryModeSelector"
    assert branches[0].children[0].output_type=="BranchKey"
    assert len(loops)==1
    assert loops[0].children[0].name=="ImprovementCoreContinuationGuard"
    assert loops[0].children[0].output_type=="Bool"
