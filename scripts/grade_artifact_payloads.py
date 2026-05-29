#!/usr/bin/env python3
"""Extract and grade JSON payloads embedded in PM artifacts.

SDD Task 3.1 (G1 + G5: JSON payload extraction + schema validation +
extra-schema realism checks) and Task 3.4 (G4: hash format validation).

Scans every fenced ` ```json ` block in an artifact. Each block is
routed by `kind` (or `workflow_id`, or `status` for blocked-workflow
envelopes) to one of:

- linear_issue / linear_issue_batch — Linear dry-run preview
- notion_page / notion_page_batch — Notion dry-run preview
- discovery-to-prd-handoff — discovery → PRD workflow handoff
- prd-to-delivery-handoff — PRD → delivery workflow handoff
- workflow-chain-handoff — adapter-routed chain handoff
- blocked_workflow / blocked-workflow — blocked envelope

For each payload we run kind-appropriate checks. The grader returns a
structured PASS/FAIL result.

Reuses scripts/check_tool_safety.validate_schema.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from check_tool_safety import validate_schema  # noqa: E402


# Synthetic-but-realistic hash pattern per Task 3.4 / R3 G4. Must not
# end with `...` (truncation). Anchored to whole-string match.
HASH_PATTERN = re.compile(r"^sha256:[a-z0-9-]{8,128}$")
HASH_FIELD_NAMES = ("dry_run_payload_hash", "payloadHash", "payload_hash")

# Recognized payload kinds. The fixture's required_json_payloads field
# must use these literal strings.
KNOWN_KINDS = frozenset(
    [
        "linear_issue",
        "linear_issue_batch",
        "notion_page",
        "notion_page_batch",
        "discovery-to-prd-handoff",
        "prd-to-delivery-handoff",
        "workflow-chain-handoff",
        "blocked_workflow",
        "blocked-workflow",
    ]
)

_FENCED_JSON_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


class PayloadGradeError(ValueError):
    """Raised on malformed input or missing schemas."""


@dataclass(frozen=True)
class Payload:
    kind: str
    body: dict
    raw: str


def _coerce_kind(body: object) -> str | None:
    if not isinstance(body, dict):
        return None
    explicit = body.get("kind")
    if isinstance(explicit, str):
        return explicit
    workflow_id = body.get("workflow_id")
    if isinstance(workflow_id, str):
        if workflow_id == "workflow-discovery-to-prd":
            return "discovery-to-prd-handoff"
        if workflow_id == "workflow-prd-to-linear-delivery":
            return "prd-to-delivery-handoff"
        return "workflow-chain-handoff"
    if isinstance(workflow_id, list):
        return "workflow-chain-handoff"
    if body.get("status") == "blocked":
        return "blocked_workflow"
    # Infer kind from tool + container shape: a dryRun envelope with
    # tool:"linear" + items[] is a linear_issue_batch even when the
    # explicit `kind` field is omitted (see Claude artifact 10).
    tool = body.get("tool")
    if tool == "linear" and isinstance(body.get("items"), list):
        return "linear_issue_batch"
    if tool == "notion" and isinstance(body.get("pages"), list):
        return "notion_page_batch"
    return None


def extract_payloads(artifact_text: str) -> list[Payload]:
    """Find every fenced JSON block; parse; return Payload(kind, body, raw).

    Blocks that fail to parse are skipped silently (the grader treats
    them as "no envelope")."""
    payloads: list[Payload] = []
    for match in _FENCED_JSON_RE.finditer(artifact_text):
        raw = match.group(1)
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            continue
        kind = _coerce_kind(body) or ""
        payloads.append(Payload(kind=kind, body=body if isinstance(body, dict) else {}, raw=raw))
    return payloads


# --- per-kind realism checks -------------------------------------------------


def _has_alias(body: dict, *names: str) -> bool:
    return any(name in body for name in names)


def _has_truthy(body: dict, *names: str) -> bool:
    return any(body.get(name) is True for name in names)


def _list_len(body: dict, name: str) -> int:
    value = body.get(name)
    return len(value) if isinstance(value, list) else 0


def _check_linear_envelope(payload: Payload, artifact_text: str) -> list[str]:
    failures: list[str] = []
    body = payload.body
    if not _has_truthy(body, "confirmationRequired", "confirmation_required"):
        failures.append(
            f"linear envelope: missing confirmationRequired:true (or confirmation_required:true)"
        )
    if not _has_alias(body, "workspaceId", "workspace_id", "team_key", "teamId", "team_id"):
        failures.append("linear envelope: missing workspaceId or team_key")
    items_len = _list_len(body, "items")
    if items_len < 3:
        failures.append(f"linear envelope: items[] length {items_len} < 3")
    if "UNRESOLVED_LINEAR_" not in artifact_text:
        failures.append("linear envelope: artifact lacks any UNRESOLVED_LINEAR_* placeholder token")
    return failures


def _check_notion_envelope(payload: Payload, artifact_text: str) -> list[str]:
    failures: list[str] = []
    body = payload.body
    if not _has_truthy(body, "confirmationRequired", "confirmation_required"):
        failures.append(
            "notion envelope: missing confirmationRequired:true (or confirmation_required:true)"
        )
    target = body.get("target") if isinstance(body.get("target"), dict) else {}
    has_target = bool(target.get("id")) or "databaseId" in body or "workspaceId" in body or "parentPageId" in body
    if not has_target:
        failures.append("notion envelope: missing target.id / databaseId / workspaceId / parentPageId")
    pages_len = _list_len(body, "pages")
    if pages_len < 2:
        failures.append(f"notion envelope: pages[] length {pages_len} < 2")
    if "UNRESOLVED_NOTION_" not in artifact_text:
        failures.append("notion envelope: artifact lacks any UNRESOLVED_NOTION_* placeholder token")
    return failures


def _check_blocked_workflow(payload: Payload, root: Path) -> list[str]:
    failures: list[str] = []
    body = payload.body
    schema = json.loads((root / "schemas" / "blocked-workflow.schema.json").read_text())
    schema_errors = validate_schema(body, schema, root)
    for err in schema_errors:
        failures.append(f"blocked_workflow schema error: {err.render()}")
    # Per R3 + execution-prompt: missing_inputs[] must be non-empty
    # (a blocked workflow has at least one missing input).
    missing_inputs = body.get("missing_inputs", [])
    if not (isinstance(missing_inputs, list) and len(missing_inputs) >= 1):
        failures.append("blocked_workflow: missing_inputs[] must have ≥1 item")
    return failures


def _check_handoff_envelope(payload: Payload, schema_filename: str, root: Path) -> list[str]:
    failures: list[str] = []
    schema_path = root / "schemas" / schema_filename
    if not schema_path.exists():
        raise PayloadGradeError(f"missing schema: {schema_path}")
    schema = json.loads(schema_path.read_text())
    schema_errors = validate_schema(payload.body, schema, root)
    for err in schema_errors:
        failures.append(f"{schema_filename}: {err.render()}")
    return failures


def _check_hash_fields(payload: Payload) -> list[str]:
    failures: list[str] = []

    def visit(obj: object, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                child_prefix = f"{prefix}.{key}" if prefix else key
                if key in HASH_FIELD_NAMES and isinstance(value, str):
                    if value.endswith("..."):
                        failures.append(f"{child_prefix}: hash is truncated ({value!r})")
                    elif not HASH_PATTERN.match(value):
                        failures.append(
                            f"{child_prefix}: hash {value!r} does not match {HASH_PATTERN.pattern}"
                        )
                visit(value, child_prefix)
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                visit(item, f"{prefix}[{index}]")

    visit(payload.body)
    return failures


# --- top-level grader --------------------------------------------------------


def grade_payloads(
    artifact_text: str,
    required_kinds: list[str],
    root: Path,
) -> dict:
    """Validate that every kind in `required_kinds` is satisfied by at
    least one extracted payload that passes its per-kind realism checks.
    """
    for kind in required_kinds:
        if kind not in KNOWN_KINDS:
            return {
                "passed": False,
                "failures": [
                    f"required_json_payloads kind {kind!r} is unknown — not in {sorted(KNOWN_KINDS)}"
                ],
                "kinds_found": [],
            }

    payloads = extract_payloads(artifact_text)
    kinds_found = [p.kind for p in payloads]

    # Always run hash-format checks across every payload — Task 3.4.
    aggregate_failures: list[str] = []
    for payload in payloads:
        aggregate_failures.extend(_check_hash_fields(payload))

    # Track which required kinds have a passing candidate.
    satisfied: dict[str, bool] = {kind: False for kind in required_kinds}
    per_kind_failures: dict[str, list[str]] = {kind: [] for kind in required_kinds}

    for payload in payloads:
        kind = payload.kind
        if kind not in required_kinds and kind not in KNOWN_KINDS:
            # Unknown kind anywhere in the artifact is a structured fail
            # if the contract required it — but if it's an extra
            # payload (not in required_kinds), it's not the grader's
            # concern here.
            continue

        if kind in ("linear_issue", "linear_issue_batch"):
            check_failures = _check_linear_envelope(payload, artifact_text)
            if kind in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                per_kind_failures.setdefault(kind, []).extend(check_failures)
        elif kind in ("notion_page", "notion_page_batch"):
            check_failures = _check_notion_envelope(payload, artifact_text)
            if kind in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                per_kind_failures.setdefault(kind, []).extend(check_failures)
        elif kind in ("blocked_workflow", "blocked-workflow"):
            check_failures = _check_blocked_workflow(payload, root)
            if "blocked_workflow" in required_kinds or "blocked-workflow" in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                key = "blocked_workflow" if "blocked_workflow" in required_kinds else "blocked-workflow"
                per_kind_failures.setdefault(key, []).extend(check_failures)
        elif kind == "discovery-to-prd-handoff":
            check_failures = _check_handoff_envelope(payload, "discovery-to-prd-handoff.schema.json", root)
            if kind in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                per_kind_failures.setdefault(kind, []).extend(check_failures)
        elif kind == "prd-to-delivery-handoff":
            check_failures = _check_handoff_envelope(payload, "prd-to-delivery-handoff.schema.json", root)
            if kind in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                per_kind_failures.setdefault(kind, []).extend(check_failures)
        elif kind == "workflow-chain-handoff":
            check_failures = _check_handoff_envelope(payload, "workflow-chain-handoff.schema.json", root)
            if kind in required_kinds:
                if not check_failures:
                    satisfied[kind] = True
                per_kind_failures.setdefault(kind, []).extend(check_failures)

    for kind, ok in satisfied.items():
        if not ok:
            details = per_kind_failures.get(kind) or [
                f"no JSON block recognized as kind={kind!r}"
            ]
            aggregate_failures.append(f"required_kind {kind}: {details}")

    return {
        "passed": not aggregate_failures,
        "failures": aggregate_failures,
        "kinds_found": kinds_found,
        "per_kind_failures": per_kind_failures,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Grade JSON payloads embedded in a PM artifact."
    )
    parser.add_argument("artifact", help="Path to the artifact markdown.")
    parser.add_argument(
        "--required-kinds",
        nargs="+",
        required=True,
        help="Space-separated list of required payload kinds.",
    )
    parser.add_argument("--root", default=".", help="Package root.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv[1:])

    artifact_path = Path(args.artifact).resolve()
    text = artifact_path.read_text(encoding="utf-8")
    result = grade_payloads(text, args.required_kinds, Path(args.root).resolve())

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} payload grade — {artifact_path}")
        if not result["passed"]:
            for failure in result["failures"]:
                print(f"  - {failure}")
        print(f"kinds found: {result['kinds_found']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
