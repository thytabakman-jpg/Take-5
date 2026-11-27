"""Bounded Compile/ICC binding: working-map operations only, not a new controller.

Run as a Python 3.10+ JSON CLI with the standalone Node 18+ operators beside it.
Semantic decisions, frozen-source acquisition and guarded Git publication remain
with the Compile caller. No registered full-HF2 invocation is claimed here.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from project_manager import WorkPackage, executable_frontier
from tool_run_closure import Consequence, Disposition, StageResult, run_tool_run_closure

ROOT = Path(__file__).resolve().parent


def operator(name, payload):
    if name not in {"decompiler", "dependencies", "verify"}:
        raise ValueError("Unknown Compile operator")
    p = subprocess.run(
        ["node", str(ROOT / f"compile_{name}.mjs")],
        input=json.dumps(payload, ensure_ascii=True), text=True,
        encoding="utf-8", capture_output=True, check=True,
    )
    return json.loads(p.stdout)


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def frontier(groups, completed):
    """Only evidence-ready bounded stages; caller authenticates completion IDs."""
    completed = set(completed)
    packages = []
    for group in groups:
        gid = group["id"]
        if not isinstance(gid, str) or not gid or ":" in gid:
            raise ValueError("Invalid group ID")
        # Only mechanical stages are implemented by this adapter.
        # Discovery, semantic reconstruction, and publication are host-owned.
        for stage, pred, coord, effect in [
            ("prepare", "discovered", "changes", "TARGET_TRANSFORM"),
            ("verify", "reconstructed", "verification", "EVIDENCE_ONLY"),
        ]:
            wid = f"{gid}:{stage}"
            deps = [f"{gid}:{pred}"]
            if stage == "verify":
                deps.append(f"{gid}:prepare")
            deps.extend(group.get(f"{stage}_dependencies", []))
            packages.append(WorkPackage(
                work_id=wid, target_coordinate=coord, target_object=gid,
                operation_class="MODIFY" if stage == "prepare" else "VERIFY",
                effect_class=effect, dependencies=tuple(deps),
                success="Actual stage result and receipt",
                tests=("Exact working-state or candidate verification",),
                authority_ref=group.get("authority"),
                status="COMPLETE" if wid in completed else "OPEN",
            ))
    ready, blocked = executable_frontier(packages, completed=completed)
    return {"ready": [p.work_id for p in ready], "blocked": list(blocked)}


def prepare_group(packet):
    """Materialize steps 2–4 for an admitted many-to-one group.

    A provisional OPEN dependency report permits reversible working changes,
    never publication. All copied original bytes are retained in source blocks
    before mechanical rebasing. No files on disk or Git refs are mutated.
    """
    before = packet["before"]
    moves = packet["moves"]
    survivor = packet["survivor"]
    if not packet.get("authority") or not packet.get("revision"):
        raise ValueError("Authority and frozen revision required")
    if not moves or survivor not in before or survivor in moves:
        raise ValueError("Existing surviving path and nonempty retirements required")
    if any(old not in before or dst != survivor for old, dst in moves.items()):
        raise ValueError("Only admitted many-to-one mappings are supported")
    if any(not isinstance(t, str) for t in before.values()):
        raise ValueError("Text snapshot required")
    sources = [survivor, *moves]

    def join(texts):
        # Separators are new material, not source text; keep exact original
        # bytes and source identities separately to avoid ambiguous boundaries.
        return "\n\n".join(texts[k] for k in sources)

    step2 = dict(before)
    step2[survivor] = join(before)
    # UTF-16 offsets match the standalone operator source-coordinate contract.
    cursor = 0
    boundaries = []
    for source in sources:
        size = len(before[source].encode("utf-16-le")) // 2
        boundaries.append({"source": source, "start": cursor, "end": cursor + size,
                           "sha256": digest(before[source])})
        cursor += size + 2
    prep = operator("dependencies", {
        "mode": "prepare", "before": before, "moves": moves,
        "anchors": packet.get("anchors", {}),
    })
    if prep.get("status") not in {"PREPARED", "OPEN"}:
        raise ValueError("Unexpected preparation status")
    rebased = {**before, **prep["edits"]}
    desired = dict(rebased)
    desired[survivor] = join(rebased)
    for old in moves:
        del desired[old]
    # TRC operates on the actual working map and independently reads each
    # changed path after realization. It cannot certify unscanned dependencies.
    affected = sorted(k for k in step2.keys() | desired.keys()
                      if (k in step2) != (k in desired) or step2.get(k) != desired.get(k))
    consequences = [
        Consequence(k, "WORKING_PATH", digest(desired[k]) if k in desired else "ABSENT",
                    packet["authority"], packet["revision"], "WORKING_ONLY")
        for k in affected
    ]

    def realize(c, state):
        state = dict(state)
        if c.referent in desired:
            state[c.referent] = desired[c.referent]
        else:
            state.pop(c.referent, None)
        return StageResult(state, "REALIZED")

    def verify(c, state):
        k = c.referent
        ok = (k in state and digest(state[k]) == c.target_state
              if k in desired else k not in state)
        return StageResult(state, "VERIFIED" if ok else "OPEN",
                           evidence=(f"{k}:{c.target_state}",) if ok else ())

    def consume(c, state):
        return StageResult(state, "CONSUMED")

    closure = run_tool_run_closure(
        tool_result=prep, pre_state=before, post_state=step2,
        harvest_fn=lambda *_: consequences,
        disposition_fn=lambda *_: Disposition.REALIZE,
        realize_fn=realize, verify_fn=verify, consume_fn=consume,
        harvest_basis="Exact admitted working-map delta only", harvest_complete=True,
        max_consequences=max(1, len(consequences)),
    )
    if closure.certificate.status != "CLOSED" or closure.state != desired:
        raise RuntimeError("Working transformation incomplete")
    decomp = operator("decompiler", {
        "files": before, "targets": sources,
        "history": packet.get("history", []), "includeWorking": False,
    })
    return {
        "status": "WORKING_PREPARED", "publication": "NOT_AUTHORIZED_BY_THIS_RESULT",
        "step2": step2, "after": closure.state, "source_order": sources, "source_boundaries": boundaries,
        "preparation": prep, "decomposition": decomp,
        "working_closure": asdict(closure.certificate),
        "open_dependencies": prep.get("issues", []),
    }


def verify_group(packet):
    """Run actual steps 9–10 against the final host-reconstructed candidate."""
    if not packet.get("authority") or not packet.get("requireProvenance"):
        raise ValueError("Authority and durable provenance requirement mandatory")
    before, after = packet["before"], packet["after"]
    audit = operator("dependencies", {
        "mode": "audit", "before": before, "after": after,
        "moves": packet["moves"], "anchors": packet.get("anchors", {}),
        "literalReviews": packet.get("literalReviews", []),
        "relationshipReviews": packet.get("relationshipReviews", []),
    })
    # No supplied dependency receipt can override this fresh audit.
    inputs = {**packet, "dependencyReport": audit}
    result = operator("verify", inputs)
    return {"dependency": audit, "verification": result,
            "publication": "HOST_GUARDED_PUBLICATION_REQUIRED"}


def main():
    p = json.load(sys.stdin)
    mode = p.pop("mode")
    if mode == "frontier":
        result = frontier(p["groups"], p.get("completed", []))
    elif mode == "prepare":
        result = prepare_group(p)
    elif mode == "verify":
        result = verify_group(p)
    else:
        raise ValueError("Unsupported mode")
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
