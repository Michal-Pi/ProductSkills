"""Unit tests for the forbidden-phrase scanner.

SDD Task 3.3 (G3 + G11): catches rubric-echo skeletons. The 20
patterns ship in evals/forbidden-phrases.yaml. Each pattern carries an
`allowed_in_quality_bar` flag — inside `## Quality Bar` at most one
match per pattern is tolerated; outside QB any match is blocking.

TDD per A15. Run with:
    python3 -m unittest discover -s tests -p 'test_*.py' -v
"""

from __future__ import annotations

import re
import sys
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from grade_artifact import (
    load_forbidden_phrases,
    scan_forbidden_phrases,
)

FORBIDDEN_PATH = REPO_ROOT / "evals" / "forbidden-phrases.yaml"

CLAUDE_DIR = (
    REPO_ROOT
    / "test-results"
    / "0.2.1 run"
    / "claude2"
    / "productskills-e2e-synthetic"
    / "generated"
    / "claude"
)
GEMINI_DIR = (
    REPO_ROOT
    / "test-results"
    / "0.2.1 run"
    / "productskills-e2e-synthetic"
    / "generated"
    / "gemini"
)


class TestPatternMatchesInBody(unittest.TestCase):
    """test_pattern_matches_in_body — Gemini-style bullet match → fail."""

    def test_rubric_echo_bullet_in_body_fails(self) -> None:
        text = textwrap.dedent(
            """\
            # Strategy

            ## Confidence

            - Includes **method selection rationale**: chose ICE because…
            - Includes **next decision step**
            """
        )
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        result = scan_forbidden_phrases(text, phrases)
        self.assertFalse(result["passed"], msg=result["hits"])


class TestPatternAllowedInQualityBar(unittest.TestCase):
    """test_pattern_allowed_in_quality_bar — same phrase inside Quality
    Bar with ≤1 occurrence → pass."""

    def test_one_match_in_quality_bar_passes(self) -> None:
        text = textwrap.dedent(
            """\
            # Strategy

            ## Summary
            Concrete reasoning here. No rubric language.

            ## Quality Bar

            Criteria weights are declared up front; this analysis includes
            **method selection rationale** for ICE — exactly once.
            """
        )
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        result = scan_forbidden_phrases(text, phrases)
        self.assertTrue(result["passed"], msg=result["hits"])


class TestPatternBlocksAtTwoInQualityBar(unittest.TestCase):
    """test_pattern_blocks_at_two_occurrences_in_quality_bar — >1 in Quality Bar → fail."""

    def test_two_matches_in_quality_bar_fail(self) -> None:
        text = textwrap.dedent(
            """\
            # Strategy

            ## Quality Bar

            Includes **method selection rationale** — once.
            Includes **method selection rationale** — twice.
            """
        )
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        result = scan_forbidden_phrases(text, phrases)
        self.assertFalse(result["passed"], msg="two matches inside QB must fail")


class TestClaudeBaselinePasses(unittest.TestCase):
    """test_claude_baseline_passes — every Claude 0.2.1 positive artifact passes."""

    def test_every_claude_positive_passes(self) -> None:
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        positives = sorted(p for p in CLAUDE_DIR.glob("*.md") if not p.name.startswith("negative-"))
        self.assertGreater(len(positives), 0, "no Claude positives found")
        failed: list[str] = []
        for path in positives:
            result = scan_forbidden_phrases(path.read_text(encoding="utf-8"), phrases)
            if not result["passed"]:
                failed.append(f"{path.name}: {result['hits']}")
        self.assertEqual(failed, [], msg=f"Claude false-positives:\n{chr(10).join(failed)}")


class TestGeminiBaselineFails(unittest.TestCase):
    """test_gemini_baseline_fails — every Gemini 0.2.1 positive artifact fails."""

    def test_every_gemini_positive_fails_at_least_one_pattern(self) -> None:
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        positives = sorted(
            p for p in GEMINI_DIR.glob("*.md")
            if not p.name.startswith("negative-") and not p.name.endswith("-missing.md")
        )
        self.assertGreater(len(positives), 0, "no Gemini positives found")
        passed: list[str] = []
        for path in positives:
            result = scan_forbidden_phrases(path.read_text(encoding="utf-8"), phrases)
            if result["passed"]:
                passed.append(path.name)
        # Phase 3a calibration target: at least 6 of the 12 Gemini
        # positives should be caught. (R3 expects 100% but that's
        # 3b's section-anchored tightening; for 3a we accept ≥6.)
        caught = len(positives) - len(passed)
        self.assertGreaterEqual(
            caught,
            6,
            msg=f"only {caught} of {len(positives)} Gemini positives caught; passed: {passed}",
        )


class TestRegexCompiles(unittest.TestCase):
    """test_regex_compiles — all patterns parse as valid Python regex."""

    def test_every_pattern_compiles(self) -> None:
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        self.assertGreaterEqual(len(phrases), 20)
        for entry in phrases:
            with self.subTest(id=entry.id, pattern=entry.pattern):
                try:
                    re.compile(entry.pattern, re.IGNORECASE)
                except re.error as exc:
                    self.fail(f"pattern {entry.id} did not compile: {exc}")


class TestFalsePositiveOnLegitimateProse(unittest.TestCase):
    """test_false_positive_on_legitimate_prose — legitimate prose with
    relevant keywords does not match."""

    def test_legitimate_prose_passes(self) -> None:
        text = textwrap.dedent(
            """\
            # Discovery Synthesis

            We selected ICE over RICE because confidence was higher for
            three of the four opportunities. Direct evidence from
            INT-001 and SUP-014 shows users explicitly request the
            shorter onboarding path; this is a fact, not an assumption.

            The next step is a usability test, and we should label
            confidence Medium until that runs.

            ## Quality Bar

            Concrete reasoning anchored to evidence IDs.
            """
        )
        phrases = load_forbidden_phrases(FORBIDDEN_PATH)
        result = scan_forbidden_phrases(text, phrases)
        self.assertTrue(result["passed"], msg=result["hits"])


if __name__ == "__main__":
    unittest.main()
