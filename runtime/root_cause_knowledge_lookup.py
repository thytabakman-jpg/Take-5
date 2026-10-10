"""Read-only, source-backed RootCause discovery lookup.

This is a retrieval projection, not a causal selector or a second knowledge
ledger. The caller freezes the current failure before consulting history.
Only a supplied local Reaserch checkout is read; no network or writes.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable

BASE = Path("projects/improvement-core/research/consolidations/knowledge")
SUBJECTS = (
    "ARTIFACT_AUTHORITY_AND_FIDELITY.md",
    "CAUSAL_INFERENCE_AND_ROOTNESS.md",
    "CONTINUATION_AND_LIVENESS.md",
    "DISCOVERY_METHODS_AND_EXPERIMENTAL_CONTROLS.md",
    "EVIDENCE_STATUS_AND_TESTS.md",
    "EXECUTION_AND_TRANSITION_INTEGRITY.md",
    "INQUIRY_STATE_AND_EPISTEMIC_CONTINUATION.md",
    "SEMANTIC_ADMISSION_AND_BIAS_GENERATORS.md",
    "TYPED_INTERFACES_AND_OWNERSHIP.md",
    "WORK_FRONTIER_AND_CLOSURE.md",
)
COMMON = frozenset({
    "and", "the", "with", "that", "this", "from", "into", "when",
    "failure", "failures", "root", "cause", "causes", "audit", "report",
    "research", "system", "current", "historical", "source", "status",
    "evidence", "test", "tests", "original", "knowledge", "problem",
    "what", "where", "which", "without", "under", "after", "before",
    "have", "does", "need", "that", "their", "ours", "your", "were",
})
CITATION = re.compile(r"\]\((evidence/[A-Za-z0-9_./-]+\.md)#([a-h]\d{1,2})\)", re.I)
WORDS = re.compile(r"[a-z][a-z0-9]+", re.I)


def _words(value: str) -> set[str]:
    tokens: set[str] = set()
    for word in WORDS.findall(value.lower().replace("_", " ").replace("-", " ")):
        if len(word) < 4 or word in COMMON:
            continue
        tokens.add(word)
        if len(word) > 5 and word.endswith("ing"):
            tokens.add(word[:-3])
        if len(word) > 5 and word.endswith("ed"):
            tokens.add(word[:-2])
        if len(word) > 5 and word.endswith("s"):
            tokens.add(word[:-1])
    return tokens


def consult_root_cause_knowledge(
    *,
    observed_failure: Iterable[str],
    research_root: str | Path | None,
    limit: int = 3,
) -> dict:
    """Return candidate locations, never an admitted diagnosis or repair.

    Results contain source identities and text fingerprints. They cannot
    establish source currentness, causal applicability, or private access.
    """
    observed = tuple(str(s).strip() for s in observed_failure if str(s).strip())
    if not observed:
        return {"status": "SKIPPED_NO_OBSERVATION", "candidates": []}
    if research_root is None:
        return {"status": "NO_ACCESS", "reason": "REASERCH_CHECKOUT_NOT_BOUND",
                "candidates": []}
    base = Path(research_root) / BASE
    if not base.is_dir() or any(not (base / name).is_file() for name in SUBJECTS):
        return {"status": "NO_ACCESS", "reason": "RESEARCH_SOURCE_INCOMPLETE",
                "candidates": []}
    query = _words(" ".join(observed))
    if len(query) < 2:
        return {"status": "NO_MATCH", "reason": "INSUFFICIENT_DISTINCTIVE_QUERY",
                "candidates": []}
    candidates = []
    try:
        for filename in SUBJECTS:
            content = (base / filename).read_text(encoding="utf-8")
            title = next((line[2:] for line in content.splitlines()
                          if line.startswith("# ")), filename)
            headings = " ".join(line for line in content.splitlines()
                                if line.startswith("## "))
            # Keywords in the finding's body are necessary; headings alone
            # cannot be treated as evidence for a diagnosis.
            matches = query & _words(content)
            if len(matches) < 2:
                continue
            score = len(matches) + 2 * len(query & _words(title + " " + headings))
            refs = list(dict.fromkeys(
                (name, sid.lower()) for name, sid in CITATION.findall(content)
            ))
            if not refs:
                continue
            candidates.append({
                "subject": filename,
                "title": title,
                "score": score,
                "matched_terms": sorted(matches),
                "source_path": str(BASE / filename),
                "source_sha256": sha256(content.encode("utf-8")).hexdigest(),
                "source_refs": [
                    {"path": str(BASE / name), "anchor": sid,
                     "access": "PRIVATE_LIBRARY_ORIGINAL_UNVERIFIED"
                     if Path(name).name == "LIBRARY_ROOT_CAUSE_SOURCE_REGISTER.md"
                     else "HISTORICAL_ARCHIVE_NOT_REVALIDATED"}
                    for name, sid in refs
                ],
                "effect": "READ_ONLY_CANDIDATE_NOT_CAUSAL_ADMISSION",
                "reference_scope": "ALL_SUBJECT_REFERENCES_NOT_CASE_ADMITTED",
            })
    except (OSError, UnicodeError):
        return {"status": "NO_ACCESS", "reason": "RESEARCH_SOURCE_UNREADABLE",
                "candidates": []}
    candidates.sort(key=lambda x: (-x["score"], x["subject"]))
    if not candidates:
        return {"status": "NO_MATCH", "candidates": []}
    return {
        "status": "CANDIDATES",
        "observed_failure": observed,
        "candidates": candidates[:max(1, min(int(limit), 10))],
        "admission": "NOT_ADMITTED",
        "decision_owner": "CURRENT_DIAGNOSIS_AND_REPAIR_AUTHORITY",
        "required_next_step": "CHECK_ORIGINAL_AND_RIVALS_AGAINST_CURRENT_FAILURE",
    }


def main(argv: list[str] | None = None) -> int:
    """CLI for governed callers; stdout is data, not a repair decision."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-root", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("observed_failure", nargs="+")
    args = parser.parse_args(argv)
    out = consult_root_cause_knowledge(
        observed_failure=args.observed_failure,
        research_root=args.research_root,
        limit=args.limit,
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 2 if out["status"] == "NO_ACCESS" else 0


if __name__ == "__main__":
    raise SystemExit(main())


def record_verified_root_cause_outcome(
    *,
    owner_admitted: bool,
    verification_refs: Iterable[str],
    outcome: str,
    source_episode: str,
    basis_id: str,
    route_id: str,
    consultation: dict,
    dependency_footprint: Iterable[str] = (),
    knowledge_ledger=None,
    negative_learning_memory=None,
) -> dict:
    """Explicit post-repair capture into existing owners, never during lookup.

    The caller owns permission, actual target-effect verification and basis
    currentness. This function rejects incomplete receipts before any writes;
    it never promotes historical source claims into repair authority.
    """
    refs = tuple(str(x) for x in verification_refs if str(x).strip())
    basis_id, source_episode, route_id = (str(x).strip() for x in
                                          (basis_id, source_episode, route_id))
    if owner_admitted is not True:
        return {"status": "NOT_ADMITTED", "written": False}
    if not (refs and basis_id and source_episode and route_id):
        return {"status": "BLOCKED", "reason": "VERIFIED_CURRENT_EVIDENCE_REQUIRED",
                "written": False}
    if outcome not in {"VERIFIED_GAIN", "NO_GAIN", "FAILED", "REJECTED", "CYCLE_NO_GAIN"}:
        return {"status": "BLOCKED", "reason": "OUTCOME_DISPOSITION_NOT_SUPPORTED",
                "written": False}
    prior = tuple(x.get("subject", "") for x in consultation.get("candidates", ())
                  if isinstance(x, dict) and x.get("subject"))
    footprint = tuple(str(x) for x in dependency_footprint if str(x))
    if outcome == "VERIFIED_GAIN":
        if knowledge_ledger is None:
            return {"status": "BLOCKED", "reason": "MATERIAL_LEDGER_NOT_BOUND",
                    "written": False}
        node = knowledge_ledger.record(
            kind="MATERIAL_TRANSITION",
            statement="Verified RootCause repair outcome for route " + route_id,
            basis_id=basis_id,
            source_episode=source_episode,
            source_route=route_id,
            disposition="CAPTURED",
            dependency_footprint=footprint,
            evidence_refs=refs,
            metadata={"outcome": outcome, "consulted_subjects": prior,
                      "target_effect_verified": True},
        )
        return {"status": "CAPTURED", "written": True,
                "destination": "EXISTING_MATERIAL_KNOWLEDGE_LEDGER",
                "knowledge_id": node.knowledge_id}
    if negative_learning_memory is None:
        return {"status": "BLOCKED", "reason": "NEGATIVE_MEMORY_NOT_BOUND",
                "written": False}
    negative_learning_memory.record(
        route_id=route_id,
        basis_id=basis_id,
        disposition=outcome,
        dependency_footprint=frozenset(footprint),
        evidence={"verification_refs": refs, "source_episode": source_episode,
                  "consulted_subjects": prior, "target_effect_verified": True},
    )
    return {"status": "NEGATIVE_ROUTE_RECORDED", "written": True,
            "destination": "EXISTING_DURABLE_NEGATIVE_LEARNING_MEMORY"}
