"""Typed effectful function intermediate representation.

This module is intentionally small.  It separates:
- structural program syntax;
- effect signatures;
- higher-order named transforms;
- tool/library names;
- executable realization.

The IR does not claim every mathematical object is a function.  It gives every
configured executable/semantic behavior a typed functional surface over
explicit state/effect carriers.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Iterable


class NodeKind(str, Enum):
    ATOM = "ATOM"
    SEQ = "SEQ"
    PRODUCT = "PRODUCT"
    CHOICE = "CHOICE"
    LOOP = "LOOP"
    TRANSFORM = "TRANSFORM"


@dataclass(frozen=True)
class EffectSignature:
    names: tuple[str, ...] = ()

    @classmethod
    def of(cls, *names: str) -> "EffectSignature":
        return cls(tuple(sorted(set(names))))

    def join(self, *others: "EffectSignature") -> "EffectSignature":
        names = set(self.names)
        for other in others:
            names.update(other.names)
        return EffectSignature(tuple(sorted(names)))


@dataclass(frozen=True)
class IRNode:
    kind: NodeKind
    name: str
    input_type: str
    output_type: str
    effects: EffectSignature
    children: tuple["IRNode", ...] = ()

    def canonical_payload(self) -> dict:
        return {
            "kind": self.kind.value,
            "name": self.name,
            "input_type": self.input_type,
            "output_type": self.output_type,
            "effects": self.effects.names,
            "children": [c.canonical_payload() for c in self.children],
        }

    def semantic_hash(self) -> str:
        blob = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    def walk(self) -> tuple["IRNode", ...]:
        out = [self]
        for child in self.children:
            out.extend(child.walk())
        return tuple(out)


@dataclass(frozen=True)
class ProgramContract:
    program_id: str
    required_atoms: tuple[str, ...] = ()
    required_transforms: tuple[str, ...] = ()
    forbidden_atomic_names: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationReceipt:
    program_id: str
    valid: bool
    errors: tuple[str, ...]
    semantic_hash: str
    node_count: int
    effects: tuple[str, ...]


def atom(
    name: str,
    *,
    input_type: str = "State",
    output_type: str = "State",
    effects: EffectSignature | None = None,
) -> IRNode:
    return IRNode(
        NodeKind.ATOM,
        name,
        input_type,
        output_type,
        effects or EffectSignature(),
    )


def seq(name: str, *children: IRNode) -> IRNode:
    if not children:
        raise ValueError("SEQ_REQUIRES_CHILD")
    effects = EffectSignature().join(*(c.effects for c in children))
    return IRNode(
        NodeKind.SEQ,
        name,
        children[0].input_type,
        children[-1].output_type,
        effects,
        tuple(children),
    )


def product(
    name: str,
    *children: IRNode,
    output_type: str = "ProductResult",
) -> IRNode:
    if not children:
        raise ValueError("PRODUCT_REQUIRES_CHILD")
    effects = EffectSignature().join(*(c.effects for c in children))
    return IRNode(
        NodeKind.PRODUCT,
        name,
        children[0].input_type,
        output_type,
        effects,
        tuple(children),
    )


def choice(name: str, *children: IRNode) -> IRNode:
    if not children:
        raise ValueError("CHOICE_REQUIRES_CHILD")
    effects = EffectSignature().join(*(c.effects for c in children))
    return IRNode(
        NodeKind.CHOICE,
        name,
        children[0].input_type,
        children[0].output_type,
        effects,
        tuple(children),
    )


def loop(name: str, child: IRNode) -> IRNode:
    return IRNode(
        NodeKind.LOOP,
        name,
        child.input_type,
        child.output_type,
        child.effects,
        (child,),
    )


def transform(
    name: str,
    child: IRNode,
    *,
    input_type: str | None = None,
    output_type: str | None = None,
    effects: EffectSignature | None = None,
) -> IRNode:
    return IRNode(
        NodeKind.TRANSFORM,
        name,
        input_type or child.input_type,
        output_type or child.output_type,
        child.effects.join(effects or EffectSignature()),
        (child,),
    )


def validate(node: IRNode, contract: ProgramContract) -> ValidationReceipt:
    errors: list[str] = []

    def visit(n: IRNode) -> None:
        if n.kind is NodeKind.ATOM and n.children:
            errors.append(f"ATOM_HAS_CHILDREN:{n.name}")
        if n.kind in {NodeKind.SEQ, NodeKind.PRODUCT, NodeKind.CHOICE} and not n.children:
            errors.append(f"EMPTY_{n.kind.value}:{n.name}")
        if n.kind in {NodeKind.LOOP, NodeKind.TRANSFORM} and len(n.children) != 1:
            errors.append(f"{n.kind.value}_ARITY:{n.name}")

        if n.kind is NodeKind.SEQ:
            for left, right in zip(n.children, n.children[1:]):
                if left.output_type != right.input_type:
                    errors.append(
                        f"SEQ_TYPE_MISMATCH:{n.name}:{left.name}:{left.output_type}"
                        f"->{right.name}:{right.input_type}"
                    )

        if n.kind is NodeKind.PRODUCT:
            input_types = {c.input_type for c in n.children}
            if len(input_types) != 1:
                errors.append(f"PRODUCT_INPUT_MISMATCH:{n.name}:{sorted(input_types)}")

        if n.kind is NodeKind.CHOICE:
            types = {(c.input_type, c.output_type) for c in n.children}
            if len(types) != 1:
                errors.append(f"CHOICE_TYPE_MISMATCH:{n.name}:{sorted(types)}")

        if n.kind is NodeKind.LOOP and n.children:
            child = n.children[0]
            if child.input_type != child.output_type:
                errors.append(
                    f"LOOP_NOT_ENDOMORPHIC:{n.name}:{child.input_type}->{child.output_type}"
                )

        for child in n.children:
            visit(child)

    visit(node)

    nodes = node.walk()
    atoms = {n.name for n in nodes if n.kind is NodeKind.ATOM}
    transforms = {n.name for n in nodes if n.kind is NodeKind.TRANSFORM}

    for name in contract.required_atoms:
        if name not in atoms:
            errors.append(f"MISSING_REQUIRED_ATOM:{name}")
    for name in contract.required_transforms:
        if name not in transforms:
            errors.append(f"MISSING_REQUIRED_TRANSFORM:{name}")
    forbidden = set(contract.forbidden_atomic_names) & atoms
    for name in sorted(forbidden):
        errors.append(f"WHOLE_TOOL_HIDDEN_AS_ATOM:{name}")

    return ValidationReceipt(
        program_id=contract.program_id,
        valid=not errors,
        errors=tuple(errors),
        semantic_hash=node.semantic_hash(),
        node_count=len(nodes),
        effects=node.effects.names,
    )


def render_tree(node: IRNode, depth: int = 0) -> str:
    pad = "  " * depth
    line = (
        f"{pad}{node.kind.value} {node.name}: "
        f"{node.input_type}->{node.output_type} effects={list(node.effects.names)}"
    )
    return "\n".join([line, *(render_tree(c, depth + 1) for c in node.children)])
