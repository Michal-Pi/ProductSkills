#!/usr/bin/env python3
"""Validate Notion and Linear dry-run safety fixtures."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECRET_KEY_TERMS = ("api_key", "apikey", "access_token", "auth_token", "bearer", "credential", "password", "secret", "token")
PAYLOAD_SCHEMAS = {
    "linear_issue": "schemas/linear-issue.schema.json",
    "notion_page": "schemas/notion-page.schema.json",
}
PAYLOAD_KIND_TO_TOOL = {
    "linear_issue": "linear",
    "notion_page": "notion",
}
OPERATIONS = {"create", "update", "archive", "link", "no-op"}
ROLLBACK_OVERCLAIM_PHRASES = (
    "automatic rollback",
    "auto rollback",
    "auto-rollback",
    "guaranteed rollback",
    "true rollback is available",
    "will rollback",
    "will roll back",
)
FIXTURE_DIR = "evals/tool-safety-fixtures"


@dataclass
class SchemaValidationError:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_type_matches(expected_type: str, value: Any) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def validate_schema(
    instance: Any,
    schema: dict[str, Any],
    root: Path,
    path: str = "$",
    schema_cache: dict[str, dict[str, Any]] | None = None,
) -> list[SchemaValidationError]:
    schema_cache = schema_cache if schema_cache is not None else {}
    errors: list[SchemaValidationError] = []

    ref = schema.get("$ref")
    if isinstance(ref, str):
        ref_schema = load_schema_ref(root, ref, schema_cache)
        return validate_schema(instance, ref_schema, root, path, schema_cache)

    if "const" in schema and instance != schema["const"]:
        errors.append(SchemaValidationError(path, f"expected const {schema['const']!r}"))
        return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(SchemaValidationError(path, f"expected one of {schema['enum']!r}"))

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not json_type_matches(expected_type, instance):
        errors.append(SchemaValidationError(path, f"expected type {expected_type}"))
        return errors

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in instance:
                    errors.append(SchemaValidationError(path, f"missing required property {key!r}"))

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, property_schema in properties.items():
                if key in instance and isinstance(property_schema, dict):
                    errors.extend(
                        validate_schema(instance[key], property_schema, root, f"{path}.{key}", schema_cache)
                    )

        if schema.get("additionalProperties") is False and isinstance(properties, dict):
            allowed = set(properties)
            for key in instance:
                if key not in allowed:
                    errors.append(SchemaValidationError(path, f"unexpected property {key!r}"))

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append(SchemaValidationError(path, f"expected at least {min_items} item(s)"))
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors.extend(validate_schema(item, item_schema, root, f"{path}[{index}]", schema_cache))

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            errors.append(SchemaValidationError(path, f"expected minLength {min_length}"))

    for nested_schema in schema.get("allOf", []):
        if isinstance(nested_schema, dict):
            errors.extend(validate_schema(instance, nested_schema, root, path, schema_cache))

    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matches = 0
        for nested_schema in one_of:
            if isinstance(nested_schema, dict) and not validate_schema(instance, nested_schema, root, path, schema_cache):
                matches += 1
        if matches != 1:
            errors.append(SchemaValidationError(path, f"expected exactly one oneOf match, got {matches}"))

    if_schema = schema.get("if")
    then_schema = schema.get("then")
    if isinstance(if_schema, dict) and isinstance(then_schema, dict):
        if not validate_schema(instance, if_schema, root, path, schema_cache):
            errors.extend(validate_schema(instance, then_schema, root, path, schema_cache))

    return errors


def load_schema_ref(root: Path, ref: str, schema_cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    schema_path = root / "schemas" / ref if "/" not in ref else root / ref
    cache_key = str(schema_path.resolve())
    if cache_key not in schema_cache:
        schema_cache[cache_key] = load_json(schema_path)
    return schema_cache[cache_key]


def collect_secret_issues(value: Any, path: str = "$") -> list[str]:
    issues: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            key_lower = key.lower()
            if any(term in key_lower for term in SECRET_KEY_TERMS):
                issues.append(f"{path}.{key}: secret-like key is not allowed")
            issues.extend(collect_secret_issues(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(collect_secret_issues(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        lowered = value.lower()
        if any(marker in lowered for marker in ("bearer ", "sk-", "secret_", "api_key=")):
            issues.append(f"{path}: secret-like value is not allowed")
    return issues


def external_mappings(fixture: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    mapping_data = fixture.get("external_id_map", {})
    output: dict[tuple[str, str], dict[str, Any]] = {}
    if not isinstance(mapping_data, dict):
        return output
    mappings = mapping_data.get("mappings", [])
    if not isinstance(mappings, list):
        return output
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        tool = mapping.get("tool")
        idempotency_key = mapping.get("idempotency_key")
        if isinstance(tool, str) and isinstance(idempotency_key, str):
            output[(tool, idempotency_key)] = mapping
    return output


def validate_payload_item(
    root: Path,
    fixture: dict[str, Any],
    item: dict[str, Any],
    index: int,
) -> list[str]:
    issues: list[str] = []
    kind = item.get("kind")
    tool = fixture.get("tool")
    payload = item.get("payload")
    operation = item.get("operation")
    item_path = f"payloads[{index}]"

    if kind not in PAYLOAD_SCHEMAS:
        return [f"{item_path}: unsupported payload kind {kind!r}"]
    if PAYLOAD_KIND_TO_TOOL.get(str(kind)) != tool:
        issues.append(f"{item_path}: payload kind {kind!r} does not match fixture tool {tool!r}")
    if not isinstance(payload, dict):
        return [f"{item_path}: payload must be an object"]
    if operation not in OPERATIONS:
        issues.append(f"{item_path}: operation must be create, update, archive, link, or no-op")

    schema = load_json(root / PAYLOAD_SCHEMAS[str(kind)])
    schema_errors = validate_schema(payload, schema, root)
    issues.extend(f"{item_path}.payload {error.render()}" for error in schema_errors)

    if payload.get("mode") != "dry_run":
        issues.append(f"{item_path}: eval payloads must stay in dry_run mode")
    if payload.get("confirmation_required") is not True:
        issues.append(f"{item_path}: dry-run payload must require confirmation")
    if not payload.get("dry_run_payload_hash"):
        issues.append(f"{item_path}: dry-run payload hash is required")
    idempotency_key = payload.get("idempotency_key")
    if not isinstance(idempotency_key, str) or not idempotency_key:
        issues.append(f"{item_path}: idempotency key is required")

    question = item.get("confirmation_question")
    if not isinstance(question, str) or not question.strip():
        issues.append(f"{item_path}: confirmation_question is required")
    else:
        question_lower = question.lower()
        dry_run_hash = payload.get("dry_run_payload_hash")
        target_refs = confirmation_target_refs(fixture, payload)
        has_idempotency = isinstance(idempotency_key, str) and idempotency_key.lower() in question_lower
        has_hash_and_target = (
            isinstance(dry_run_hash, str)
            and dry_run_hash.lower() in question_lower
            and any(ref.lower() in question_lower for ref in target_refs)
        )
        if not has_idempotency and not has_hash_and_target:
            issues.append(
                f"{item_path}: confirmation question must include the idempotency key or the dry-run hash plus target"
            )

    mappings = external_mappings(fixture)
    mapped = isinstance(tool, str) and isinstance(idempotency_key, str) and (tool, idempotency_key) in mappings
    if mapped and operation == "create":
        issues.append(f"{item_path}: existing external ID mapping requires update preview, not create")
    if not mapped and operation == "update":
        issues.append(f"{item_path}: update preview requires an existing external ID mapping")

    if kind == "linear_issue" and not payload.get("team_key"):
        issues.append(f"{item_path}: Linear payload must include explicit team_key")
    if kind == "notion_page":
        target = payload.get("target")
        if not isinstance(target, dict) or not target.get("id"):
            issues.append(f"{item_path}: Notion payload must include explicit target.id")

    return issues


def confirmation_target_refs(fixture: dict[str, Any], payload: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    team_key = payload.get("team_key")
    if isinstance(team_key, str) and team_key:
        refs.append(team_key)
    target = payload.get("target")
    if isinstance(target, dict) and isinstance(target.get("id"), str):
        refs.append(target["id"])
    idempotency_key = payload.get("idempotency_key")
    tool = fixture.get("tool")
    mappings = external_mappings(fixture)
    if isinstance(tool, str) and isinstance(idempotency_key, str):
        mapping = mappings.get((tool, idempotency_key))
        if isinstance(mapping, dict) and isinstance(mapping.get("external_id"), str):
            refs.append(mapping["external_id"])
    return refs


def validate_missing_workspace(fixture: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    setup = fixture.get("setup_instructions")
    if not isinstance(setup, dict):
        return ["missing workspace fixture must include setup_instructions"]
    missing = setup.get("missing_identifiers")
    next_action = setup.get("next_action")
    if not isinstance(missing, list) or not missing:
        issues.append("setup_instructions.missing_identifiers must be a non-empty list")
    if not isinstance(next_action, str) or not next_action.strip():
        issues.append("setup_instructions.next_action is required")
    for item in fixture.get("payloads", []):
        if isinstance(item, dict) and item.get("operation") not in {None, "no-op"}:
            issues.append("missing workspace fixture must not preview create/update operations")
    return issues


def validate_batch_checkpoint(fixture: dict[str, Any]) -> list[str]:
    checkpoint = fixture.get("batch_checkpoint")
    if checkpoint is None:
        return []
    if not isinstance(checkpoint, dict):
        return ["batch_checkpoint must be an object"]

    issues: list[str] = []
    state = checkpoint.get("state")
    if state not in {"dry_run", "partial_failure", "completed"}:
        issues.append("batch_checkpoint.state must be dry_run, partial_failure, or completed")
    for key in ("completed", "skipped", "failed", "retryable_items"):
        if not isinstance(checkpoint.get(key), list):
            issues.append(f"batch_checkpoint.{key} must be a list")
    if state == "partial_failure":
        if not checkpoint.get("failed"):
            issues.append("partial_failure checkpoint must include failed items")
        if not isinstance(checkpoint.get("manual_revert_plan"), str) or not checkpoint.get("manual_revert_plan", "").strip():
            issues.append("partial_failure checkpoint must include a manual_revert_plan")
        revert_plan = str(checkpoint.get("manual_revert_plan", "")).lower()
        if any(phrase in revert_plan for phrase in ROLLBACK_OVERCLAIM_PHRASES):
            issues.append("manual_revert_plan must not claim automatic or guaranteed rollback")
    return issues


def validate_workspace_and_maps(root: Path, fixture: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if "workspace" in fixture:
        errors = validate_schema(
            fixture["workspace"],
            load_json(root / "schemas/product-os-workspace.schema.json"),
            root,
        )
        issues.extend(f"workspace {error.render()}" for error in errors)
    if "external_id_map" in fixture:
        errors = validate_schema(
            fixture["external_id_map"],
            load_json(root / "schemas/external-id-map.schema.json"),
            root,
        )
        issues.extend(f"external_id_map {error.render()}" for error in errors)
    return issues


def evaluate_fixture(root: Path, fixture: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    fixture_schema_errors = validate_schema(
        fixture,
        load_json(root / "schemas/tool-safety-fixture.schema.json"),
        root,
    )
    issues.extend(f"fixture {error.render()}" for error in fixture_schema_errors)

    for key in ("case", "expected", "tool", "scenario"):
        if not isinstance(fixture.get(key), str) or not fixture.get(key):
            issues.append(f"fixture missing string field {key!r}")

    if fixture.get("expected") not in {"pass", "fail"}:
        issues.append("fixture expected must be pass or fail")
    if fixture.get("tool") not in {"notion", "linear"}:
        issues.append("fixture tool must be notion or linear")

    issues.extend(collect_secret_issues(fixture))
    issues.extend(validate_workspace_and_maps(root, fixture))

    if fixture.get("scenario") == "missing_workspace":
        issues.extend(validate_missing_workspace(fixture))

    payloads = fixture.get("payloads", [])
    if not isinstance(payloads, list):
        issues.append("payloads must be a list")
    else:
        for index, item in enumerate(payloads):
            if not isinstance(item, dict):
                issues.append(f"payloads[{index}] must be an object")
                continue
            issues.extend(validate_payload_item(root, fixture, item, index))

    issues.extend(validate_batch_checkpoint(fixture))
    return issues


def run_fixture_suite(root: Path) -> tuple[list[str], list[str]]:
    fixture_dir = root / FIXTURE_DIR
    if not fixture_dir.exists():
        return [], [f"Missing {FIXTURE_DIR}/"]

    summaries: list[str] = []
    failures: list[str] = []
    fixtures = sorted(fixture_dir.glob("*.json"))
    if not fixtures:
        return [], [f"No tool safety fixtures found in {FIXTURE_DIR}/"]

    for fixture_path in fixtures:
        try:
            fixture = load_json(fixture_path)
        except json.JSONDecodeError as exc:
            failures.append(f"{fixture_path.relative_to(root)}: invalid JSON: {exc}")
            continue
        if not isinstance(fixture, dict):
            failures.append(f"{fixture_path.relative_to(root)}: fixture must be an object")
            continue
        issues = evaluate_fixture(root, fixture)
        actual = "pass" if not issues else "fail"
        expected = fixture.get("expected")
        summaries.append(f"{fixture_path.name}: expected {expected}, got {actual}")
        if actual != expected:
            failures.append(
                f"{fixture_path.relative_to(root)} expected {expected}, got {actual}: "
                + "; ".join(issues or ["no issues"])
            )

    return summaries, failures


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    summaries, failures = run_fixture_suite(root)

    if failures:
        print(f"FAIL tool safety evals: {len(failures)} issue(s)")
        for summary in summaries:
            print(f"- {summary}")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS tool safety evals")
    print(f"- Root: {root}")
    for summary in summaries:
        print(f"- {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
