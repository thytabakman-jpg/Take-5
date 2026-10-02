from pathlib import Path
import re

THEORY = Path("architecture/ICC128_GREEN_LAYOUT_THEORY_001_2026-09-25.md")
OUTPUT = Path("validation/ICC128_OUTPUT_LAYOUT_CANDIDATE_001_2026-09-25.md")

def _assert_color_commands_are_inside_math(text: str) -> None:
    lines = text.splitlines()
    in_display = False
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == r"\[":
            assert not in_display, f"nested display math at line {lineno}"
            in_display = True
            continue
        if stripped == r"\]":
            assert in_display, f"unmatched display close at line {lineno}"
            in_display = False
            continue
        if r"\color{" in line:
            assert in_display or bool(re.search(r"\\\(.*\\color\{.*\\\)", line)), (
                f"color command outside recognized math delimiters at line {lineno}: {line}"
            )
    assert not in_display, "unclosed display math block"

def test_icc128_color_commands_are_renderable():
    _assert_color_commands_are_inside_math(THEORY.read_text(encoding="utf-8"))
    _assert_color_commands_are_inside_math(OUTPUT.read_text(encoding="utf-8"))

def test_output_layout_points_to_existing_theory_file():
    text = OUTPUT.read_text(encoding="utf-8")
    ref = "architecture/ICC128_GREEN_LAYOUT_THEORY_001_2026-09-25.md"
    assert ref in text
    assert Path(ref).exists()
