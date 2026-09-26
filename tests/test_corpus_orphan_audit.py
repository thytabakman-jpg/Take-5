import sys
from pathlib import Path
sys.path.insert(0,"tools")

from corpus_orphan_audit import audit


def test_orphan_accounting_is_total_and_distinguishes_accounting_from_orphan_free(tmp_path:Path):
    (tmp_path/"architecture").mkdir()
    (tmp_path/"sort-later").mkdir()
    (tmp_path/"architecture"/"CURRENT.md").write_text(
        "# Current\nSee runtime/missing.py and architecture/KNOWN.md\nStatus CURRENT\n",
        encoding="utf-8",
    )
    (tmp_path/"architecture"/"KNOWN.md").write_text("# Known\nInvariant x\n",encoding="utf-8")
    (tmp_path/"sort-later"/"candidate.md").write_text("# Candidate\nOPEN question\n",encoding="utf-8")
    out=audit(tmp_path)
    assert out["proof"]["accounting_complete"]
    assert not out["proof"]["orphan_free"]
    assert out["proof"]["hidden_unclassified_count"]==0
    assert any(x["path"]=="runtime/missing.py" for x in out["missing_expected_references"])
    row=next(x for x in out["records"] if x["path"]=="sort-later/candidate.md")
    assert row["disposition"]=="OPEN_UNRESOLVED_PLACEMENT"


def test_formal_signal_regex_is_live_not_literal_backslash_b(tmp_path:Path):
    (tmp_path/"x.md").write_text("# X\nInvariant law and theorem.\n",encoding="utf-8")
    out=audit(tmp_path)
    row=next(x for x in out["records"] if x["path"]=="x.md")
    assert row["material_signal"]
    assert row["disposition"]=="OPEN_GENERAL_MATERIAL_REVIEW"
