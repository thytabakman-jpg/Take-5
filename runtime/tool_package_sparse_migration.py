"""Evidence-first migration of Take-5's empty 36-cell package pages.

This module only *audits* and plans. It deliberately does not delete files or
change the current package contract or accepted project goal. Physical removal
requires separate approved governance and matching generator/consumer changes.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import hashlib
import json
import re

from tool_project_packages import (
    all_project_specs, package_relroot, coverage_cells, coverage_name,
    render_coverage_cell, SPARSE_COVERAGE_PILOT,
)

PACKAGE_ROOT = Path("projects/tool-system")
LINK_ONLY_GOAL_ENDING = (
    "Canonical semantic changes route through "
    "[AUTHORITY_REGISTRY.md](../AUTHORITY_REGISTRY.md) and "
    "[CHANGE_CONTROL.md](../CHANGE_CONTROL.md)."
)
BASE_ENDING = (
    "Canonical semantic changes route through "
    "AUTHORITY_REGISTRY.md and CHANGE_CONTROL.md."
)


@dataclass(frozen=True)
class CellObservation:
    path: str
    object_id: str
    index: int
    disposition: str
    sha256: str
    reason: str


def _canonical_empty_texts(spec, index, scope, mode) -> tuple[str, ...]:
    canonical = render_coverage_cell(spec, index, scope, mode)
    if spec.object_id == "GOAL":
        # GOAL's curated link-format difference is not scientific content.
        return (canonical, canonical.replace(BASE_ENDING, LINK_ONLY_GOAL_ENDING))
    return (canonical,)


def audit_coverage(root: Path) -> tuple[CellObservation, ...]:
    """Produce exhaustive, byte-strict observations; never mutate the tree."""
    root = Path(root)
    findings = []
    for spec in all_project_specs():
        folder = PACKAGE_ROOT / package_relroot(spec) / "coverage"
        found = set()
        for index, scope, mode in coverage_cells():
            fname = coverage_name(index, scope, mode)
            rel = folder / fname
            file = root / rel
            found.add(fname)
            if not file.is_file():
                pilot = spec.object_id in SPARSE_COVERAGE_PILOT
                findings.append(CellObservation(
                    str(rel), spec.object_id, index,
                    "VIRTUAL_EMPTY_PILOT" if pilot else "MISSING", "",
                    "pilot logical slot with no admitted evidence" if pilot
                    else "expected cell is absent"))
                continue
            content = file.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            # Compare actual bytes, not a heuristic such as file length or keyword.
            candidates = tuple(s.encode("utf-8") for s in
                               _canonical_empty_texts(spec, index, scope, mode))
            if content in candidates:
                disposition, reason = "EMPTY_TEMPLATE", "exact generated empty template"
            else:
                disposition, reason = "PRESERVE", "differs from known empty template"
            findings.append(CellObservation(
                str(rel), spec.object_id, index, disposition, digest, reason))
        if (root / folder).exists():
            for file in sorted((root / folder).glob("*.md")):
                if file.name == "README.md" or file.name in found:
                    continue
                rel = folder / file.name
                findings.append(CellObservation(
                    str(rel), spec.object_id, 0, "UNKNOWN_CELL",
                    hashlib.sha256(file.read_bytes()).hexdigest(),
                    "unrecognized file: preserve and investigate"))
    return tuple(findings)


def affected_markdown_readers(root: Path, candidate_paths: Iterable[str]) -> tuple[str, ...]:
    """Find linked readers of proposed empty-cell paths before any removal.

    A linked source outside a soon-to-be-deleted cell needs a migrated target,
    even when the target is presently an empty placeholder.
    """
    root = Path(root)
    proposed = {str((root / p).resolve()) for p in candidate_paths}
    consumers: set[str] = set()
    link_re = re.compile(r"\]\(([^)]+)\)")
    for source in (root / PACKAGE_ROOT).rglob("*.md"):
        if str(source.resolve()) in proposed:
            continue
        body = source.read_text(encoding="utf-8")
        for match in link_re.finditer(body):
            ref = match.group(1).split("#", 1)[0].strip()
            if not ref or "://" in ref or ref.startswith(("mailto:", "/", "#")):
                continue
            link = (source.parent / ref).resolve()
            if str(link) in proposed:
                consumers.add(str(source.relative_to(root)))
    return tuple(sorted(consumers))


def proposed_sparse_core_updates(root: Path) -> dict[str, str]:
    """Build minimal *in-memory* core-page changes; never write repository state.

    Original object-specific documentation and native regression clauses survive.
    Only the physical-page assertions and links to disappearing placeholders
    change. This does not change the accepted GOAL.md on main.
    """
    root = Path(root)
    edits: dict[str, str] = {}
    for spec in all_project_specs():
        folder = PACKAGE_ROOT / package_relroot(spec)
        manifest = folder / "MANIFEST.md"
        text = (root / manifest).read_text(encoding="utf-8")
        if "Coverage cells: 36" not in text:
            raise ValueError(f"MISSING_36_COORDINATE_IDENTITY:{manifest}")
        if ("## Coverage pages" not in text and
            "## Reserved logical coverage coordinates" not in text):
            raise ValueError(f"MISSING_MANIFEST_COVERAGE_HEADING:{manifest}")
        text = text.replace("## Coverage pages",
                            "## Reserved logical coverage coordinates (36; physical pages optional)")
        for index, scope, face in coverage_cells():
            name = coverage_name(index, scope, face)
            # Linked authored manifests are still preserved, but blank page
            # links cannot be left dangling.
            text = text.replace(f"- [coverage/{name}](coverage/{name})",
                                f"- coverage/{name}")
            if f"- coverage/{name}" not in text:
                raise ValueError(f"MISSING_RESERVED_COORDINATE:{manifest}:{name}")
        edits[str(manifest)] = text

        regression = folder / "REGRESSION_CONTRACT.md"
        text = (root / regression).read_text(encoding="utf-8")
        assertion = "- exactly 36 Scope x ModeFace coverage pages exist"
        if text.count(assertion) != 1:
            raise ValueError(f"UNEXPECTED_REGRESSION_CONTRACT:{regression}")
        edits[str(regression)] = text.replace(
            assertion, "- exactly 36 logical Scope x ModeFace coordinates exist; "
            "physical cell files are reserved for admitted evidence")

        coverage_index = folder / "coverage/README.md"
        text = (root / coverage_index).read_text(encoding="utf-8")
        text = re.sub(
            r"\[(\d{2}) ([A-Z]+)\]\(\./\d{2}_[A-Z_]+__[A-Z]+\.md\)",
            r"\1 \2 (reserved logical coordinate)",
            text,
        )
        # The basic coverage index already names the exact 36-coordinate
        # surface. Readers that used numbered links now receive nonbroken
        # coordinate names, while actual admitted evidence remains independent.
        edits[str(coverage_index)] = text
    return edits


def candidate_plan(root: Path) -> dict:
    """Lossless plan: only exact blank templates qualify for future retirement."""
    rows = audit_coverage(root)
    dispositions = {name: sum(r.disposition == name for r in rows)
                    for name in ("EMPTY_TEMPLATE", "VIRTUAL_EMPTY_PILOT", "PRESERVE", "MISSING", "UNKNOWN_CELL")}
    readers = affected_markdown_readers(root, (r.path for r in rows if r.disposition == "EMPTY_TEMPLATE"))
    return {
        "status": "CANDIDATE_ONLY_GOAL_CHANGE_APPROVAL_REQUIRED",
        "existing_markdown_readers_requiring_migration": readers,
        "source": "runtime/tool_package_sparse_migration.py",
        "total_logical_coordinates": len(all_project_specs()) * len(coverage_cells()),
        "dispositions": dispositions,
        "candidate_empty_file_paths": [r.path for r in rows
                                       if r.disposition == "EMPTY_TEMPLATE"],
        "virtual_empty_pilot_paths": [r.path for r in rows
                                      if r.disposition == "VIRTUAL_EMPTY_PILOT"],
        "protected_paths": [r.path for r in rows
                            if r.disposition in {"PRESERVE", "UNKNOWN_CELL"}],
        "missing_coordinates": [r.path for r in rows
                                if r.disposition == "MISSING"],
        "delete_authorized": False,
        "current_project_goal_unchanged": True,
        "note": ("No physical deletion is licensed. Any future schema migration "
                 "must preserve 36 logical cells, native consumers, curated "
                 "manifests/regressions and separately admitted goal approval."),
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="existing Take-5 repository checkout")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    plan = candidate_plan(Path(args.root))
    if args.summary_only:
        plan.pop("candidate_empty_file_paths")
        plan.pop("protected_paths")
        plan.pop("virtual_empty_pilot_paths")
        plan.pop("missing_coordinates")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
