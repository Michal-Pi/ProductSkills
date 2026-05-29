"""Unit tests for conditional skill declaration extraction.

SDD Task 3.5 (G6, per A13): the grader checks declared-skills ⊇
expected-skill-ids ONLY when the expected fixture sets
`provenance_required: true`. Default behavior (flag absent or false)
is "declaration optional, absent declaration not a fail" — so Gemini's
in-conversation chat outputs are not penalized for missing it.

TDD per A15. Run with:
    python3 -m unittest discover -s tests -p 'test_*.py' -v
"""

from __future__ import annotations

import sys
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from grade_artifact import (
    check_provenance,
    extract_declared_skills,
    parse_simple_fixture,
)


class TestExtractDeclaredSkills(unittest.TestCase):
    """test_extract_returns_union_of_inline_and_frontmatter — finds both
    `Skill: <name>` lines (and Skills:) and YAML frontmatter
    `skill_ids: [...]`."""

    def test_inline_Skill_line(self) -> None:
        text = "Skill: `pm-discovery`. Synthetic only.\n\nBody."
        self.assertEqual(extract_declared_skills(text), {"pm-discovery"})

    def test_plural_Skills_line_with_comma(self) -> None:
        text = "Skills: `pm-discovery`, `pm-strategy`.\n\nBody."
        self.assertEqual(
            extract_declared_skills(text), {"pm-discovery", "pm-strategy"}
        )

    def test_yaml_frontmatter_skill_ids(self) -> None:
        text = textwrap.dedent(
            """\
            ---
            skill_ids:
              - pm-docs
              - pm-stakeholder-comms
            ---

            # Body
            """
        )
        self.assertEqual(
            extract_declared_skills(text), {"pm-docs", "pm-stakeholder-comms"}
        )

    def test_union_of_inline_and_frontmatter(self) -> None:
        text = textwrap.dedent(
            """\
            ---
            skill_ids:
              - pm-discovery
            ---

            Skill: `pm-strategy`. Synthetic.
            """
        )
        self.assertEqual(
            extract_declared_skills(text), {"pm-discovery", "pm-strategy"}
        )


class TestProvenanceFalseAllowsAbsent(unittest.TestCase):
    """test_absent_declaration_with_provenance_false_passes."""

    def test_absent_when_not_required_passes(self) -> None:
        result = check_provenance(
            artifact_text="No skill declaration anywhere.",
            expected_skill_ids=["pm-discovery"],
            provenance_required=False,
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["missing"], [])


class TestProvenanceTrueRequires(unittest.TestCase):
    """test_absent_declaration_with_provenance_true_fails."""

    def test_absent_when_required_fails_with_clear_error(self) -> None:
        result = check_provenance(
            artifact_text="No skill declaration anywhere.",
            expected_skill_ids=["pm-discovery", "pm-validation"],
            provenance_required=True,
        )
        self.assertFalse(result["passed"])
        self.assertIn("pm-discovery", result["missing"])
        self.assertIn("pm-validation", result["missing"])


class TestProvenanceSupersetAllowed(unittest.TestCase):
    """test_declared_superset_of_expected_passes — extra declared
    skills are not a fail."""

    def test_extra_declared_skills_pass(self) -> None:
        text = "Skill: `pm-discovery`. Skill: `pm-validation`. Skill: `pm-design`."
        result = check_provenance(
            artifact_text=text,
            expected_skill_ids=["pm-discovery"],
            provenance_required=True,
        )
        self.assertTrue(result["passed"])
        self.assertEqual(result["missing"], [])


class TestEveryExpectedFixtureHasProvenanceFlag(unittest.TestCase):
    """All evals/expected/*.yaml fixtures declare provenance_required."""

    def test_every_fixture_declares_provenance(self) -> None:
        expected_dir = REPO_ROOT / "evals" / "expected"
        missing: list[str] = []
        for path in sorted(expected_dir.glob("*.yaml")):
            parsed = parse_simple_fixture(path)
            if "provenance_required" not in parsed:
                missing.append(path.name)
        self.assertEqual(missing, [], msg=f"missing provenance_required in: {missing}")


if __name__ == "__main__":
    unittest.main()
