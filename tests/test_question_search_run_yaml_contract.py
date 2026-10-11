"""Strict source integrity for the immutable Question Search research run.

This validates serialization and declared identity; it does not turn its
basis-relative findings into current MultiObject runtime proof.
"""
from pathlib import Path

import pytest
import yaml
from yaml.constructor import ConstructorError


SOURCE = Path(__file__).resolve().parents[1] / "research" / "QUESTION_SEARCH_RUN_001.yaml"


class NoDuplicateKeysLoader(yaml.SafeLoader):
    """Treat duplicate YAML mapping keys as invalid rather than overwriting them."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError(
                "mapping", node.start_mark,
                f"duplicate mapping key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


NoDuplicateKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def test_duplicate_yaml_mapping_keys_are_rejected():
    with pytest.raises(ConstructorError):
        yaml.load("key: old\nkey: replacement\n", Loader=NoDuplicateKeysLoader)


def test_question_search_run_parses_and_preserves_declared_registry():
    record = yaml.load(SOURCE.read_text(encoding="utf-8"), Loader=NoDuplicateKeysLoader)
    assert isinstance(record, dict)
    assert record["object_id"] == "QUESTION-SEARCH-RUN:001"
    assert record["status"] == "BASIS_RELATIVE_FIXED_POINT"
    assert record["global_unknown_history"] == "OPEN"
    assert record["closure"]["status"] == "BASIS_RELATIVE_FIXED_POINT"
    assert record["closure"]["global_completeness"] == "OPEN"
    families = record["question_families"]
    assert isinstance(families, dict)
    assert set(families) == {f"Q{i:02d}" for i in range(1, 23)}
    assert families["Q04"]["name"] == "Together Math"
    for question_id, entry in families.items():
        assert isinstance(entry, dict), question_id
        for key in ("name", "question", "math"):
            assert isinstance(entry.get(key), str) and entry[key].strip(), (question_id, key)
