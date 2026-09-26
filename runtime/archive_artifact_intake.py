"""Exact external ZIP binding and expansion into the existing artifact-intake path.

This is an adapter, not a controller. It verifies that the supplied bytes match an
immutable external object reference, accounts for every declared ZIP member, and
converts text members into ArtifactRecord objects for the existing intake system.

Traversal/accounting completeness is deliberately distinct from semantic completeness.
Binary or unreadable members remain explicit unresolved evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from zipfile import BadZipFile, ZipFile
from artifact_intake import ArtifactRecord


class ArchiveBindingError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitHubArtifactRef:
    repository: str
    object_class: str
    stable_id: str
    source_ref: str
    observed_name: str
    expected_byte_count: int
    expected_sha256: str
    observed_at: str

    @property
    def provenance(self) -> tuple[str, ...]:
        return (
            "provider:github",
            f"repository:{self.repository}",
            f"object_class:{self.object_class}",
            f"stable_id:{self.stable_id}",
            f"source_ref:{self.source_ref}",
            f"observed_name:{self.observed_name}",
            f"expected_byte_count:{self.expected_byte_count}",
            f"expected_sha256:{self.expected_sha256.lower()}",
            f"observed_at:{self.observed_at}",
        )


@dataclass(frozen=True)
class ArchiveMemberReceipt:
    archive_stable_id: str
    member_index: int
    member_name: str
    compressed_size: int
    uncompressed_size: int
    sha256: str
    disposition: str


@dataclass(frozen=True)
class ZipExpansionResult:
    source: GitHubArtifactRef
    archive_byte_count: int
    archive_sha256: str
    declared_members: int
    member_receipts: tuple[ArchiveMemberReceipt, ...]
    text_artifacts: tuple[ArtifactRecord, ...]
    unresolved: tuple[str, ...]

    @property
    def traversal_complete(self) -> bool:
        return self.declared_members == len(self.member_receipts)


def _verify_binding(data: bytes, source: GitHubArtifactRef) -> tuple[int, str]:
    actual_count = len(data)
    actual_sha = sha256(data).hexdigest()
    if actual_count != int(source.expected_byte_count):
        raise ArchiveBindingError(
            f"ARCHIVE_BYTE_COUNT_MISMATCH:{source.stable_id}:"
            f"{actual_count}!={source.expected_byte_count}"
        )
    if actual_sha.lower() != str(source.expected_sha256).lower():
        raise ArchiveBindingError(
            f"ARCHIVE_SHA256_MISMATCH:{source.stable_id}:"
            f"{actual_sha}!={source.expected_sha256.lower()}"
        )
    return actual_count, actual_sha


def _member_artifact_id(source: GitHubArtifactRef, index: int, name: str) -> str:
    return f"github:{source.repository}:{source.object_class}:{source.stable_id}:member:{index}:{name}"


def expand_bound_zip(
    data: bytes,
    source: GitHubArtifactRef,
    *,
    max_members: int = 10_000,
    max_total_uncompressed_bytes: int = 100_000_000,
) -> ZipExpansionResult:
    """Verify and account for an exact ZIP, routing text members to ArtifactRecord.

    The function never extracts to the filesystem. Duplicate member names remain
    distinct because member index participates in identity.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise ArchiveBindingError("ARCHIVE_BYTES_REQUIRED")
    raw = bytes(data)
    archive_count, archive_sha = _verify_binding(raw, source)

    try:
        with ZipFile(BytesIO(raw), "r") as zf:
            infos = zf.infolist()
            if len(infos) > int(max_members):
                raise ArchiveBindingError(
                    f"ARCHIVE_MEMBER_LIMIT:{len(infos)}>{max_members}"
                )
            declared_members = len(infos)
            total_uncompressed = sum(int(info.file_size) for info in infos)
            if total_uncompressed > int(max_total_uncompressed_bytes):
                raise ArchiveBindingError(
                    "ARCHIVE_UNCOMPRESSED_LIMIT:"
                    f"{total_uncompressed}>{max_total_uncompressed_bytes}"
                )

            receipts: list[ArchiveMemberReceipt] = []
            text_artifacts: list[ArtifactRecord] = []
            unresolved: list[str] = []

            for index, info in enumerate(infos):
                name = str(info.filename)

                if info.is_dir():
                    receipts.append(
                        ArchiveMemberReceipt(
                            source.stable_id,
                            index,
                            name,
                            int(info.compress_size),
                            int(info.file_size),
                            sha256(b"").hexdigest(),
                            "DIRECTORY_ACCOUNTED",
                        )
                    )
                    continue

                if info.flag_bits & 0x1:
                    receipts.append(
                        ArchiveMemberReceipt(
                            source.stable_id,
                            index,
                            name,
                            int(info.compress_size),
                            int(info.file_size),
                            "",
                            "ENCRYPTED_UNREADABLE",
                        )
                    )
                    unresolved.append(f"{index}:{name}:ENCRYPTED_UNREADABLE")
                    continue

                try:
                    payload = zf.read(info)
                except Exception as exc:
                    receipts.append(
                        ArchiveMemberReceipt(
                            source.stable_id,
                            index,
                            name,
                            int(info.compress_size),
                            int(info.file_size),
                            "",
                            "READ_ERROR",
                        )
                    )
                    unresolved.append(
                        f"{index}:{name}:READ_ERROR:{type(exc).__name__}"
                    )
                    continue

                member_sha = sha256(payload).hexdigest()
                try:
                    text = payload.decode("utf-8-sig")
                except UnicodeDecodeError:
                    receipts.append(
                        ArchiveMemberReceipt(
                            source.stable_id,
                            index,
                            name,
                            int(info.compress_size),
                            len(payload),
                            member_sha,
                            "BINARY_ACCOUNTED_UNROUTED",
                        )
                    )
                    unresolved.append(f"{index}:{name}:BINARY_UNROUTED")
                    continue

                receipts.append(
                    ArchiveMemberReceipt(
                        source.stable_id,
                        index,
                        name,
                        int(info.compress_size),
                        len(payload),
                        member_sha,
                        "TEXT_ROUTED",
                    )
                )
                text_artifacts.append(
                    ArtifactRecord(
                        artifact_id=_member_artifact_id(source, index, name),
                        content=text,
                        provenance=source.provenance
                        + (
                            f"archive_sha256:{archive_sha}",
                            f"member_index:{index}",
                            f"member_name:{name}",
                            f"member_sha256:{member_sha}",
                        ),
                    )
                )

    except BadZipFile as exc:
        raise ArchiveBindingError(
            f"ARCHIVE_INVALID_ZIP:{source.stable_id}"
        ) from exc

    return ZipExpansionResult(
        source=source,
        archive_byte_count=archive_count,
        archive_sha256=archive_sha,
        declared_members=declared_members,
        member_receipts=tuple(receipts),
        text_artifacts=tuple(text_artifacts),
        unresolved=tuple(unresolved),
    )
