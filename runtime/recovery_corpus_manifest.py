"""Content-addressed recovery-corpus manifest.

This layer sits after exact archive expansion and before semantic reconstruction.
It preserves every source/member identity while allowing identical bytes to share
one content-equivalence class. Deduplication never deletes provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from archive_artifact_intake import ZipExpansionResult


@dataclass(frozen=True)
class RecoveryCorpusItem:
    source_stable_id: str
    member_index: int
    member_name: str
    disposition: str
    sha256: str
    uncompressed_size: int
    artifact_id: str | None

    @property
    def content_key(self) -> str | None:
        return self.sha256 or None


@dataclass(frozen=True)
class ContentEquivalenceClass:
    sha256: str
    members: tuple[tuple[str, int, str], ...]


@dataclass(frozen=True)
class RecoveryCorpusManifest:
    source_archives: tuple[str, ...]
    items: tuple[RecoveryCorpusItem, ...]
    equivalence_classes: tuple[ContentEquivalenceClass, ...]
    unresolved: tuple[str, ...]
    archive_traversal_complete: bool

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def text_item_count(self) -> int:
        return sum(1 for x in self.items if x.artifact_id is not None)

    @property
    def semantic_complete(self) -> bool:
        return self.archive_traversal_complete and not self.unresolved


def build_recovery_corpus(
    expansions: Iterable[ZipExpansionResult],
) -> RecoveryCorpusManifest:
    """Merge exact ZIP expansions into one lossless provenance manifest."""
    expansions = tuple(expansions)
    items: list[RecoveryCorpusItem] = []
    unresolved: list[str] = []
    source_archives: list[str] = []
    by_hash: dict[str, list[tuple[str, int, str]]] = {}

    for expansion in expansions:
        sid = str(expansion.source.stable_id)
        source_archives.append(sid)

        text_by_index = {}
        for artifact in expansion.text_artifacts:
            idx = None
            for prov in artifact.provenance:
                if str(prov).startswith("member_index:"):
                    idx = int(str(prov).split(":", 1)[1])
                    break
            if idx is not None:
                text_by_index[idx] = artifact.artifact_id

        for receipt in expansion.member_receipts:
            artifact_id = text_by_index.get(receipt.member_index)
            item = RecoveryCorpusItem(
                source_stable_id=sid,
                member_index=int(receipt.member_index),
                member_name=str(receipt.member_name),
                disposition=str(receipt.disposition),
                sha256=str(receipt.sha256),
                uncompressed_size=int(receipt.uncompressed_size),
                artifact_id=artifact_id,
            )
            items.append(item)
            if item.content_key:
                by_hash.setdefault(item.content_key, []).append(
                    (sid, item.member_index, item.member_name)
                )

        unresolved.extend(
            f"{sid}:{value}" for value in expansion.unresolved
        )

    classes = tuple(
        ContentEquivalenceClass(sha, tuple(members))
        for sha, members in sorted(by_hash.items())
    )

    return RecoveryCorpusManifest(
        source_archives=tuple(source_archives),
        items=tuple(items),
        equivalence_classes=classes,
        unresolved=tuple(unresolved),
        archive_traversal_complete=all(
            x.traversal_complete for x in expansions
        ) if expansions else False,
    )


def duplicate_content_classes(
    manifest: RecoveryCorpusManifest,
) -> tuple[ContentEquivalenceClass, ...]:
    """Return byte-identical content classes without collapsing their provenance."""
    return tuple(
        group for group in manifest.equivalence_classes
        if len(group.members) > 1
    )
