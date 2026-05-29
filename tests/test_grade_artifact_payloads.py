"""Unit tests for scripts/grade_artifact_payloads.py.

SDD Task 3.1 (G1 + G5: JSON payload extraction + schema validation +
realism checks) and Task 3.4 (G4: hash format validation).

TDD per A15.

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

from grade_artifact_payloads import (
    PayloadGradeError,
    extract_payloads,
    grade_payloads,
)


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


class TestClaudeToolingExtractsLinearBatch(unittest.TestCase):
    """test_claude_09_extracts_linear_payload_with_items_6 — Claude's 09
    tool-dry-run-preview extracts ≥1 Linear payload with items[] = 6."""

    def test_claude_09_passes_linear_check(self) -> None:
        text = (CLAUDE_DIR / "09-pm-tooling.md").read_text(encoding="utf-8")
        payloads = extract_payloads(text)
        linear = [p for p in payloads if p.kind in ("linear_issue", "linear_issue_batch")]
        self.assertGreaterEqual(len(linear), 1)
        self.assertEqual(len(linear[0].body.get("items", [])), 6)

        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch", "notion_page_batch"],
            root=REPO_ROOT,
        )
        self.assertTrue(result["passed"], msg=result["failures"])


class TestGeminiToolingFails(unittest.TestCase):
    """test_gemini_09_fails — Gemini's 09 has no parseable batch envelope
    that satisfies the realism checks."""

    def test_gemini_09_fails_linear_check(self) -> None:
        text = (GEMINI_DIR / "09-pm-tooling.md").read_text(encoding="utf-8")
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch", "notion_page_batch"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"], msg="Gemini 09 should fail")


class TestSparseLinearPayloadFails(unittest.TestCase):
    """test_sparse_linear_fails — {"kind": "linear_issue", "dry_run": true}
    is too sparse — fails items[] ≥3."""

    def test_two_key_linear_payload_fails(self) -> None:
        text = textwrap.dedent(
            """\
            # Sparse case
            ```json
            {"kind": "linear_issue", "dry_run": true}
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"])
        joined = " ".join(result["failures"])
        self.assertTrue(
            "items" in joined.lower() or "min" in joined.lower(),
            msg=f"expected items[]-count failure in: {result['failures']}",
        )


class TestBlockedWorkflowEmptyMissingInputs(unittest.TestCase):
    """test_blocked_workflow_empty_missing_inputs_fails — missing_inputs[]
    must have ≥1 item per the blocked-workflow contract."""

    def test_blocked_workflow_with_empty_missing_inputs_fails(self) -> None:
        text = textwrap.dedent(
            """\
            # Bad blocked envelope
            ```json
            {
              "kind": "blocked_workflow",
              "status": "blocked",
              "missing_inputs": []
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["blocked_workflow"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"])
        joined = " ".join(result["failures"])
        self.assertTrue(
            "missing_inputs" in joined.lower() or "blocked_workflow" in joined.lower(),
            msg=f"expected blocked_workflow / missing_inputs failure: {result['failures']}",
        )


class TestUnknownKindFails(unittest.TestCase):
    """test_unknown_kind_fails — an unknown `kind` value returns a
    structured "no matching schema" error rather than a silent pass."""

    def test_unknown_kind_returns_explicit_error(self) -> None:
        text = textwrap.dedent(
            """\
            ```json
            {"kind": "not_a_real_kind", "anything": 1}
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["not_a_real_kind"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"])
        joined = " ".join(result["failures"])
        self.assertIn("unknown", joined.lower())


class TestConfirmationRequiredAlias(unittest.TestCase):
    """test_confirmationRequired_is_alias — camelCase
    `confirmationRequired: true` accepted as equivalent to snake_case
    `confirmation_required: true`."""

    def test_camelCase_confirmation_required_accepted(self) -> None:
        text = textwrap.dedent(
            """\
            ```json
            {
              "kind": "linear_issue_batch",
              "dryRun": true,
              "confirmationRequired": true,
              "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
              "items": [
                {"externalId": "a", "title": "A"},
                {"externalId": "b", "title": "B"},
                {"externalId": "c", "title": "C"}
              ]
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch"],
            root=REPO_ROOT,
        )
        self.assertTrue(result["passed"], msg=result["failures"])


# --- Task 3.4: hash format validation ---


class TestTruncatedHashFails(unittest.TestCase):
    """test_truncated_hash_fails — `sha256:7f8e9a1b...` fails."""

    def test_truncated_hash_caught(self) -> None:
        text = textwrap.dedent(
            """\
            ```json
            {
              "kind": "linear_issue_batch",
              "dryRun": true,
              "confirmationRequired": true,
              "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
              "payloadHash": "sha256:7f8e9a1b...",
              "items": [
                {"externalId": "a", "title": "A"},
                {"externalId": "b", "title": "B"},
                {"externalId": "c", "title": "C"}
              ]
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"])
        joined = " ".join(result["failures"])
        self.assertIn("hash", joined.lower())


class TestSyntheticHashPasses(unittest.TestCase):
    """test_synthetic_hash_passes — `sha256:synthetic-linear-preview-001`
    passes."""

    def test_synthetic_placeholder_hash_passes(self) -> None:
        text = textwrap.dedent(
            """\
            ```json
            {
              "kind": "linear_issue_batch",
              "dryRun": true,
              "confirmationRequired": true,
              "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
              "payloadHash": "sha256:synthetic-linear-preview-001",
              "items": [
                {"externalId": "a", "title": "A"},
                {"externalId": "b", "title": "B"},
                {"externalId": "c", "title": "C"}
              ]
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch"],
            root=REPO_ROOT,
        )
        self.assertTrue(result["passed"], msg=result["failures"])


class TestShortHashFails(unittest.TestCase):
    """test_short_hash_fails — `sha256:abc` fails (under 8 chars)."""

    def test_under_8_char_hash_fails(self) -> None:
        text = textwrap.dedent(
            """\
            ```json
            {
              "kind": "linear_issue_batch",
              "dryRun": true,
              "confirmationRequired": true,
              "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
              "payloadHash": "sha256:abc",
              "items": [
                {"externalId": "a", "title": "A"},
                {"externalId": "b", "title": "B"},
                {"externalId": "c", "title": "C"}
              ]
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["linear_issue_batch"],
            root=REPO_ROOT,
        )
        self.assertFalse(result["passed"])
        joined = " ".join(result["failures"])
        self.assertIn("hash", joined.lower())


class TestBlockedWorkflowSpellingAliases(unittest.TestCase):
    """Codex P3 regression: required_kinds=['blocked-workflow'] must
    accept payloads inferred as 'blocked_workflow' from `status:blocked`,
    and vice versa."""

    def test_blocked_workflow_dash_required_accepts_underscore_inferred(self) -> None:
        # Schema constraints: resume_status is a workflow-stage string
        # (enum), blocked-workflow.schema has additionalProperties:false.
        text = textwrap.dedent(
            """\
            ```json
            {
              "status": "blocked",
              "blocked_stage": "evidence",
              "reason": "no interviews, no usage data, no sales notes — cannot proceed",
              "missing_inputs": ["interviews"],
              "risk_if_continued": "fabrication risk",
              "safe_partial_output": "research plan",
              "recommended_next_action": ["recruit candidates"],
              "questions_for_user": ["which segment?"],
              "resume_status": "evidence_insufficient",
              "handoff_target": "pm-discovery"
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["blocked-workflow"],
            root=REPO_ROOT,
        )
        self.assertTrue(result["passed"], msg=result["failures"])

    def test_blocked_workflow_underscore_required_accepts_dash(self) -> None:
        # No `kind` field — schema is additionalProperties:false so
        # status:blocked alone routes via _coerce_kind to blocked_workflow.
        text = textwrap.dedent(
            """\
            ```json
            {
              "status": "blocked",
              "blocked_stage": "x",
              "reason": "long enough reason text that satisfies minLength",
              "missing_inputs": ["one"],
              "risk_if_continued": "risk",
              "safe_partial_output": "out",
              "recommended_next_action": ["a"],
              "questions_for_user": ["q"],
              "resume_status": "blocked",
              "handoff_target": "pm-discovery"
            }
            ```
            """
        )
        result = grade_payloads(
            artifact_text=text,
            required_kinds=["blocked_workflow"],
            root=REPO_ROOT,
        )
        self.assertTrue(result["passed"], msg=result["failures"])


if __name__ == "__main__":
    unittest.main()
