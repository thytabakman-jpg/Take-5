from hashlib import sha256
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from archive_artifact_intake import GitHubArtifactRef, expand_bound_zip
from recovery_corpus_manifest import (
    build_recovery_corpus,
    duplicate_content_classes,
)


def _zip(entries):
    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
        for name, payload in entries:
            zf.writestr(name, payload)
    return buf.getvalue()


def _expansion(stable_id, entries):
    data = _zip(entries)
    ref = GitHubArtifactRef(
        repository="thytabakman-jpg/Take-5",
        object_class="actions_artifact",
        stable_id=stable_id,
        source_ref=f"test:{stable_id}",
        observed_name=f"archive-{stable_id}",
        expected_byte_count=len(data),
        expected_sha256=sha256(data).hexdigest(),
        observed_at="2026-09-26T18:40:00-04:00",
    )
    return expand_bound_zip(data, ref)


def test_manifest_preserves_every_member_and_archive_identity():
    a = _expansion("A", [
        ("chat.md", b"same"),
        ("notes.txt", b"alpha"),
    ])
    b = _expansion("B", [
        ("copy.md", b"same"),
        ("binary.bin", b"\xff\xfe"),
    ])

    manifest = build_recovery_corpus([a, b])

    assert manifest.archive_traversal_complete
    assert manifest.item_count == 4
    assert manifest.text_item_count == 3
    assert manifest.source_archives == ("A", "B")
    assert any(x.startswith("B:1:binary.bin:BINARY_UNROUTED") for x in manifest.unresolved)


def test_identical_content_is_grouped_without_deleting_paths():
    a = _expansion("A", [("first.md", b"same")])
    b = _expansion("B", [("second.md", b"same")])

    manifest = build_recovery_corpus([a, b])
    duplicates = duplicate_content_classes(manifest)

    assert len(duplicates) == 1
    assert duplicates[0].sha256 == sha256(b"same").hexdigest()
    assert duplicates[0].members == (
        ("A", 0, "first.md"),
        ("B", 0, "second.md"),
    )
    assert manifest.item_count == 2


def test_semantic_complete_is_stronger_than_traversal_complete():
    a = _expansion("A", [
        ("text.md", b"text"),
        ("opaque.bin", b"\xff"),
    ])

    manifest = build_recovery_corpus([a])

    assert manifest.archive_traversal_complete
    assert not manifest.semantic_complete
