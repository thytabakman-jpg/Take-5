"""Typed effectful function intermediate representation."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib, json

class NodeKind(str, Enum):
    ATOM="ATOM"
    SEQ="SEQ"
    PRODUCT="PRODUCT"
    BRANCH="BRANCH"
    LOOP="LOOP"
    TRANSFORM="TRANSFORM"

@dataclass(frozen=True)
class EffectSignature:
    names: tuple[str,...]=()
    @classmethod
    def of(cls,*names:str)->"EffectSignature":
        return cls(tuple(sorted(set(names))))
    def join(self,*others:"EffectSignature")->"EffectSignature":
        xs=set(self.names)
        for other in others: xs.update(other.names)
        return EffectSignature(tuple(sorted(xs)))

@dataclass(frozen=True)
class IRNode:
    kind: NodeKind
    name: str
    input_type: str
    output_type: str
    effects: EffectSignature
    children: tuple["IRNode",...]=()
    def canonical_payload(self)->dict:
        return {"kind":self.kind.value,"name":self.name,"input_type":self.input_type,
                "output_type":self.output_type,"effects":self.effects.names,
                "children":[c.canonical_payload() for c in self.children]}
    def semantic_hash(self)->str:
        raw=json.dumps(self.canonical_payload(),sort_keys=True,separators=(",",":")).encode()
        return hashlib.sha256(raw).hexdigest()
    def walk(self)->tuple["IRNode",...]:
        out=[self]
        for child in self.children: out.extend(child.walk())
        return tuple(out)

@dataclass(frozen=True)
class ProgramContract:
    program_id: str
    required_atoms: tuple[str,...]=()
    required_transforms: tuple[str,...]=()
    forbidden_atomic_names: tuple[str,...]=()

@dataclass(frozen=True)
class ValidationReceipt:
    program_id: str
    valid: bool
    errors: tuple[str,...]
    semantic_hash: str
    node_count: int
    effects: tuple[str,...]

def atom(name:str,*,input_type:str="State",output_type:str="State",
         effects:EffectSignature|None=None)->IRNode:
    return IRNode(NodeKind.ATOM,name,input_type,output_type,effects or EffectSignature())

def seq(name:str,*children:IRNode)->IRNode:
    if not children: raise ValueError("SEQ_REQUIRES_CHILD")
    return IRNode(NodeKind.SEQ,name,children[0].input_type,children[-1].output_type,
                  EffectSignature().join(*(c.effects for c in children)),tuple(children))

def product(name:str,*children:IRNode,output_type:str="ProductResult")->IRNode:
    if not children: raise ValueError("PRODUCT_REQUIRES_CHILD")
    return IRNode(NodeKind.PRODUCT,name,children[0].input_type,output_type,
                  EffectSignature().join(*(c.effects for c in children)),tuple(children))

def branch(name:str,selector:IRNode,*branches:IRNode)->IRNode:
    if not branches: raise ValueError("BRANCH_REQUIRES_BRANCH")
    return IRNode(NodeKind.BRANCH,name,selector.input_type,branches[0].output_type,
                  EffectSignature().join(selector.effects,*(b.effects for b in branches)),
                  (selector,*branches))

def loop(name:str,guard:IRNode,body:IRNode)->IRNode:
    return IRNode(NodeKind.LOOP,name,body.input_type,body.output_type,
                  guard.effects.join(body.effects),(guard,body))

def transform(name:str,child:IRNode,*,input_type:str|None=None,output_type:str|None=None,
              effects:EffectSignature|None=None)->IRNode:
    return IRNode(NodeKind.TRANSFORM,name,input_type or child.input_type,
                  output_type or child.output_type,
                  child.effects.join(effects or EffectSignature()),(child,))

def validate(node:IRNode,contract:ProgramContract)->ValidationReceipt:
    errors=[]
    def visit(n:IRNode):
        if n.kind is NodeKind.ATOM and n.children: errors.append(f"ATOM_HAS_CHILDREN:{n.name}")
        if n.kind in {NodeKind.SEQ,NodeKind.PRODUCT,NodeKind.BRANCH} and not n.children:
            errors.append(f"EMPTY_{n.kind.value}:{n.name}")
        if n.kind is NodeKind.TRANSFORM and len(n.children)!=1:
            errors.append(f"TRANSFORM_ARITY:{n.name}")
        if n.kind is NodeKind.LOOP and len(n.children)!=2:
            errors.append(f"LOOP_ARITY:{n.name}")
        if n.kind is NodeKind.SEQ:
            for a,b in zip(n.children,n.children[1:]):
                if a.output_type!=b.input_type:
                    errors.append(f"SEQ_TYPE_MISMATCH:{n.name}:{a.name}->{b.name}")
        if n.kind is NodeKind.PRODUCT:
            if len({c.input_type for c in n.children})!=1:
                errors.append(f"PRODUCT_INPUT_MISMATCH:{n.name}")
        if n.kind is NodeKind.BRANCH and n.children:
            selector,*branches=n.children
            if selector.output_type!="BranchKey":
                errors.append(f"BRANCH_SELECTOR_TYPE:{n.name}:{selector.output_type}")
            if any(b.input_type!=selector.input_type for b in branches):
                errors.append(f"BRANCH_INPUT_MISMATCH:{n.name}")
            if len({b.output_type for b in branches})!=1:
                errors.append(f"BRANCH_OUTPUT_MISMATCH:{n.name}")
        if n.kind is NodeKind.LOOP and len(n.children)==2:
            guard,body=n.children
            if guard.input_type!=body.input_type or guard.output_type!="Bool":
                errors.append(f"LOOP_GUARD_TYPE:{n.name}")
            if body.input_type!=body.output_type:
                errors.append(f"LOOP_NOT_ENDOMORPHIC:{n.name}")
        for child in n.children: visit(child)
    visit(node)
    nodes=node.walk()
    atoms={n.name for n in nodes if n.kind is NodeKind.ATOM}
    transforms={n.name for n in nodes if n.kind is NodeKind.TRANSFORM}
    for x in contract.required_atoms:
        if x not in atoms: errors.append(f"MISSING_REQUIRED_ATOM:{x}")
    for x in contract.required_transforms:
        if x not in transforms: errors.append(f"MISSING_REQUIRED_TRANSFORM:{x}")
    for x in sorted(set(contract.forbidden_atomic_names)&atoms):
        errors.append(f"WHOLE_TOOL_HIDDEN_AS_ATOM:{x}")
    return ValidationReceipt(contract.program_id,not errors,tuple(errors),
                             node.semantic_hash(),len(nodes),node.effects.names)

def render_tree(node:IRNode,depth:int=0)->str:
    pad="  "*depth
    head=f"{pad}{node.kind.value} {node.name}: {node.input_type}->{node.output_type} effects={list(node.effects.names)}"
    return "\n".join([head,*(render_tree(c,depth+1) for c in node.children)])
