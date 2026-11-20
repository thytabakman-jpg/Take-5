"""Open immutable legacy inputs from this repository's Git history."""

from functools import cache
from io import BytesIO
from pathlib import Path
from subprocess import CalledProcessError, run
from tarfile import open as open_tar
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_COMMIT = "d7416cfae3bb31128cd627b87059a3aa7222aba3"


@cache
def _snapshot(relative_path):
    try:
        archive = run(
            ["git", "archive", REFERENCE_COMMIT, "--", relative_path],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
    except CalledProcessError as error:
        raise RuntimeError(
            f"Cannot read {relative_path} at {REFERENCE_COMMIT}. "
            "Fetch this repository's Git history if the checkout is shallow."
        ) from error

    directory = TemporaryDirectory(prefix="legacy-reference-")
    with open_tar(fileobj=BytesIO(archive)) as source:
        source.extractall(directory.name, filter="data")
    return directory


def legacy_reference(relative_path):
    """Return a path to the requested historical file or directory."""
    return Path(_snapshot(relative_path).name) / relative_path
