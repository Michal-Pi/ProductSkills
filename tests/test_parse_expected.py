"""Unit tests for the upgraded YAML parser in scripts/grade_artifact.py.

SDD Task 3.0 (per external review A3): the homegrown YAML parser must
handle nested expected-fixture structures up to 3 levels deep so that
Phase 3a/3b grader extensions (min_content, must_include_in_section,
section-anchored prose) can land without rewriting fixtures.

Tests are written first (TDD per A15); the implementation in
scripts/grade_artifact.py is updated to satisfy them.

Run with:
    python3 -m unittest discover -s tests -p 'test_*.py' -v
"""

from __future__ import annotations

import sys
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from grade_artifact import ArtifactEvalError, parse_simple_fixture


def _write_fixture(tmp_path: Path, contents: str) -> Path:
    target = tmp_path / "fixture.yaml"
    target.write_text(textwrap.dedent(contents), encoding="utf-8")
    return target


class TestParseFlatYAML(unittest.TestCase):
    """test_parse_flat_yaml — current 0.2.1 shape must still pass."""

    def test_existing_simple_fixture_shape_preserved(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: discovery-synthesis
                skill_ids:
                  - pm-discovery
                rubrics:
                  - evidence_backed_artifact
                expected_sections:
                  - sources
                  - themes
                must_include:
                  - separates direct evidence from inference
                must_not_include:
                  - invented customer quotes
            """)
            parsed = parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

        self.assertEqual(parsed["case"], "discovery-synthesis")
        self.assertEqual(parsed["skill_ids"], ["pm-discovery"])
        self.assertEqual(parsed["rubrics"], ["evidence_backed_artifact"])
        self.assertEqual(parsed["expected_sections"], ["sources", "themes"])
        self.assertEqual(parsed["must_include"], ["separates direct evidence from inference"])
        self.assertEqual(parsed["must_not_include"], ["invented customer quotes"])


class TestParseNestedMinContent(unittest.TestCase):
    """test_parse_nested_min_content — new shape parses correctly."""

    def test_min_content_block_parses_as_nested_dict(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: pm-discovery-direct-evidence
                skill_ids:
                  - pm-discovery
                min_content:
                  evidence_id_count: 12
                  opportunities_table_rows: 4
                  options_compared: 3
                  themes_with_confidence: 3
                  bullets_per_section_min: 2
            """)
            parsed = parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

        self.assertIn("min_content", parsed)
        self.assertIsInstance(parsed["min_content"], dict)
        self.assertEqual(parsed["min_content"]["evidence_id_count"], 12)
        self.assertEqual(parsed["min_content"]["opportunities_table_rows"], 4)
        self.assertEqual(parsed["min_content"]["options_compared"], 3)
        self.assertEqual(parsed["min_content"]["themes_with_confidence"], 3)
        self.assertEqual(parsed["min_content"]["bullets_per_section_min"], 2)


class TestParseNestedMustIncludeInSection(unittest.TestCase):
    """test_parse_nested_must_include_in_section — new shape parses correctly."""

    def test_section_anchored_phrase_dicts_parse_as_list_of_dicts(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: pm-strategy-prioritization
                must_include_in_section:
                  - section: scores
                    phrase: opportunity
                    anchored: prose
                  - section: criteria
                    phrase: weights table
                    anchored: bullet
            """)
            parsed = parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

        self.assertIn("must_include_in_section", parsed)
        items = parsed["must_include_in_section"]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["section"], "scores")
        self.assertEqual(items[0]["phrase"], "opportunity")
        self.assertEqual(items[0]["anchored"], "prose")
        self.assertEqual(items[1]["section"], "criteria")
        self.assertEqual(items[1]["phrase"], "weights table")
        self.assertEqual(items[1]["anchored"], "bullet")


class TestParseDeeplyNestedAnchored(unittest.TestCase):
    """test_parse_deeply_nested_anchored — 3-level nesting."""

    def test_three_level_nesting_with_scalar_leaves(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: deep-nesting
                anchored_phrases:
                  scores:
                    opportunity:
                      anchored: prose
                      min_words_in_context: 30
                    sensitivity:
                      anchored: bullet
                      min_words_in_context: 20
            """)
            parsed = parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

        self.assertIn("anchored_phrases", parsed)
        root = parsed["anchored_phrases"]
        self.assertIsInstance(root, dict)
        self.assertIn("scores", root)
        scores = root["scores"]
        self.assertIsInstance(scores, dict)
        self.assertIn("opportunity", scores)
        opportunity = scores["opportunity"]
        self.assertIsInstance(opportunity, dict)
        self.assertEqual(opportunity["anchored"], "prose")
        self.assertEqual(opportunity["min_words_in_context"], 30)
        sensitivity = scores["sensitivity"]
        self.assertEqual(sensitivity["anchored"], "bullet")
        self.assertEqual(sensitivity["min_words_in_context"], 20)


class TestMalformedYAMLRaises(unittest.TestCase):
    """test_malformed_yaml_raises — bad input yields clear error, not silent fail."""

    def test_orphan_list_item_raises(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                - orphan
                case: thing
            """)
            with self.assertRaises(ArtifactEvalError):
                parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

    def test_mixed_indent_raises(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: x
                min_content:
                  evidence_id_count: 12
                   opportunities_table_rows: 4
            """)
            with self.assertRaises(ArtifactEvalError):
                parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()

    def test_line_without_key_value_raises(self) -> None:
        tmp = Path(self.id().replace(".", "_") + "_dir")
        tmp.mkdir(exist_ok=True)
        try:
            path = _write_fixture(tmp, """\
                case: x
                this is just text
            """)
            with self.assertRaises(ArtifactEvalError):
                parse_simple_fixture(path)
        finally:
            path.unlink()
            tmp.rmdir()


class TestBackwardCompatAgainstExistingFixtures(unittest.TestCase):
    """test_backward_compat_against_existing_fixtures — every existing
    evals/expected/*.yaml still loads."""

    def test_all_existing_expected_fixtures_load(self) -> None:
        expected_dir = REPO_ROOT / "evals" / "expected"
        self.assertTrue(expected_dir.is_dir(), f"missing dir: {expected_dir}")
        fixtures = sorted(expected_dir.glob("*.yaml"))
        self.assertGreater(len(fixtures), 0, "expected at least one fixture")
        for path in fixtures:
            with self.subTest(fixture=path.name):
                parsed = parse_simple_fixture(path)
                self.assertIsInstance(parsed, dict)
                # Every existing fixture has a "case" scalar.
                self.assertIn("case", parsed)
                self.assertIsInstance(parsed["case"], str)
                self.assertGreater(len(parsed["case"]), 0)


if __name__ == "__main__":
    unittest.main()
