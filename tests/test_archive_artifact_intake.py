from hashlib import sha256
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from archive_artifact_intake import (
    ArchiveBindingError,
    GitHubArtifactRef,
    expand_bound_zip,
)
from artifact_intake import intake


def _zip(entries):
    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
        for name, payload in entries:
            zf.writestr(name, payload)
    return buf.getvalue()


def _ref(data, stable_id="10901131588"):
    return GitHubArtifactRef(
        repository="thytabakman-jpg/Take-5",
        object_class="actions_artifact",
        stable_id=stable_id,
        source_ref="workflow_run:36226293888",
        observed_name="take5-validation-receipts",
        expected_byte_count=len(data),
        expected_sha256=sha256(data).hexdigest(),
        observed_at="2026-09-26T17:23:00-04:00",
    )


def test_binding_fails_closed_on_size_or_hash_mismatch():
    data = _zip([("a.txt", b"a")])
    ref = _ref(data)
    wrong_size = GitHubArtifactRef(
        ref.repository,
        ref.object_class,
        ref.stable_id,
        ref.source_ref,
        ref.observed_name,
        len(data) + 1,
        ref.expected_sha256,
        ref.observed_at,
    )
    with pytest.raises(ArchiveBindingError, match="ARCHIVE_BYTE_COUNT_MISMATCH"):
        expand_bound_zip(data, wrong_size)

    wrong_hash = GitHubArtifactRef(
        ref.repository,
        ref.object_class,
        ref.stable_id,
        ref.source_ref,
        ref.observed_name,
        ref.expected_byte_count,
        "0" * 64,
        ref.observed_at,
    )
    with pytest.raises(ArchiveBindingError, match="ARCHIVE_SHA256_MISMATCH"):
        expand_bound_zip(data, wrong_hash)


def test_every_declared_member_is_accounted_and_text_is_routed():
    data = _zip([
        ("dir/", b""),
        ("dir/a.json", b'{"x":1}'),
        ("binary.bin", b"\xff\xfe\x00"),
    ])
    out = expand_bound_zip(data, _ref(data))
    assert out.traversal_complete
    assert out.declared_members == 3
    assert [r.disposition for r in out.member_receipts] == [
        "DIRECTORY_ACCOUNTED",
        "TEXT_ROUTED",
        "BINARY_ACCOUNTED_UNROUTED",
    ]
    assert len(out.text_artifacts) == 1
    assert out.text_artifacts[0].content == '{"x":1}'
    assert out.unresolved == ("2:binary.bin:BINARY_UNROUTED",)


def test_duplicate_names_remain_distinct_by_member_index():
    data = _zip([("same.txt", b"one"), ("same.txt", b"two")])
    out = expand_bound_zip(data, _ref(data))
    assert len(out.text_artifacts) == 2
    assert out.text_artifacts[0].artifact_id != out.text_artifacts[1].artifact_id
    assert out.text_artifacts[0].content == "one"
    assert out.text_artifacts[1].content == "two"


def test_total_uncompressed_size_guard_fails_closed():
    data = _zip([("large.txt", b"x" * 1000)])
    with pytest.raises(ArchiveBindingError, match="ARCHIVE_UNCOMPRESSED_LIMIT"):
        expand_bound_zip(
            data,
            _ref(data),
            max_total_uncompressed_bytes=100,
        )


def test_expanded_text_members_enter_existing_intake_with_source_provenance():
    data = _zip([("events.jsonl", b'{"event":"ok"}\n')])
    out = expand_bound_zip(data, _ref(data))

    def generator(artifact):
        return [{
            "candidate_id": "event-ok",
            "candidate_type": "STATUS_OR_AUTHORITY_CHANGE",
            "source_span": "line:1",
            "load_bearing": True,
        }]

    intake_result = intake(out.text_artifacts, {"events": generator})
    assert intake_result.traversal_complete
    candidate = intake_result.candidates[0]
    assert "stable_id:10901131588" in candidate.provenance
    assert "member_name:events.jsonl" in candidate.provenance
