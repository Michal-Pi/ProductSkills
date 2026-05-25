#!/usr/bin/env python3
"""Validate fresh-context forward-test captures."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


FORWARD_TEST_DIR = "evals/forward-tests"
LEAK_TERMS = (
    "artifact-quality-rubrics",
    "evals/expected",
    "evals/golden-cases",
    "expected fixture",
    "expected-quality",
    "golden case",
    "golden-case",
    "must_include",
    "must_not_include",
    "required_checks",
    "rubric",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry_skill_ids(root: Path) -> list[str]:
    registry = load_json(root / "registry.json")
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        raise ValueError("registry.json must contain a skills list")
    skill_ids: list[str] = []
    for entry in registry["skills"]:
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            skill_ids.append(entry["id"])
    return skill_ids


def load_trigger_runner(root: Path):
    script_path = root / "scripts/run_trigger_evals.py"
    spec = importlib.util.spec_from_file_location("product_os_run_trigger_evals", script_path)
    if spec is None or spec.loader is None:
        raise ValueError("could not load trigger eval runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_case_shape(case: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"cases[{index}]"
    required = {
        "id": str,
        "skill_id": str,
        "prompt": str,
        "fresh_context": bool,
        "required_resources": list,
        "success_signals": list,
        "prohibited_behaviors": list,
        "capture": dict,
    }
    for key, expected_type in required.items():
        if not isinstance(case.get(key), expected_type):
            errors.append(f"{prefix}.{key} must be {expected_type.__name__}")
    if isinstance(case.get("prompt"), str) and len(case["prompt"]) < 40:
        errors.append(f"{prefix}.prompt must be at least 40 characters")
    for list_key, min_items in (
        ("required_resources", 1),
        ("success_signals", 2),
        ("prohibited_behaviors", 1),
    ):
        value = case.get(list_key)
        if isinstance(value, list):
            if len(value) < min_items:
                errors.append(f"{prefix}.{list_key} must include at least {min_items} item(s)")
            if not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"{prefix}.{list_key} must contain non-empty strings")

    capture = case.get("capture")
    if isinstance(capture, dict):
        if capture.get("mode") not in {"simulated_fresh_context", "independent_agent"}:
            errors.append(f"{prefix}.capture.mode is invalid")
        if capture.get("status") not in {"pass", "flag", "fail"}:
            errors.append(f"{prefix}.capture.status is invalid")
        observations = capture.get("observations")
        if not isinstance(observations, list) or not observations:
            errors.append(f"{prefix}.capture.observations must be a non-empty list")
        gaps = capture.get("gaps")
        if capture.get("status") in {"flag", "fail"} and not gaps:
            errors.append(f"{prefix}.capture.gaps must explain flagged or failed cases")
        patched_paths = capture.get("patched_paths")
        if not isinstance(gaps, list) or not isinstance(patched_paths, list):
            errors.append(f"{prefix}.capture.gaps and patched_paths must be lists")
    return errors


def prompt_leak_errors(prompt: str, skill_ids: list[str], case_id: str) -> list[str]:
    normalized_prompt = prompt.lower()
    errors = [f"{case_id}: prompt leaks answer key term {term!r}" for term in LEAK_TERMS if term in normalized_prompt]
    for skill_id in skill_ids:
        if re.search(rf"(?<![a-z0-9-]){re.escape(skill_id)}(?![a-z0-9-])", normalized_prompt):
            errors.append(f"{case_id}: prompt must not name registered skill id {skill_id!r}")
    return errors


def validate_forward_suite(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    summaries: list[str] = []
    suite_dir = root / FORWARD_TEST_DIR
    if not suite_dir.exists():
        return summaries, [f"Missing {FORWARD_TEST_DIR}/"]

    suite_files = sorted(suite_dir.glob("*.json"))
    if not suite_files:
        return summaries, [f"No forward-test suite files found in {FORWARD_TEST_DIR}/"]

    skill_ids = load_registry_skill_ids(root)
    covered: set[str] = set()
    trigger_runner = load_trigger_runner(root)
    skill_descriptions = trigger_runner.load_skill_descriptions(root)

    for suite_file in suite_files:
        try:
            suite = load_json(suite_file)
        except json.JSONDecodeError as exc:
            errors.append(f"{suite_file.relative_to(root)} does not parse as JSON: {exc}")
            continue
        if not isinstance(suite, dict):
            errors.append(f"{suite_file.relative_to(root)} must contain a JSON object")
            continue
        cases = suite.get("cases")
        if not isinstance(cases, list):
            errors.append(f"{suite_file.relative_to(root)} missing cases list")
            continue
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                errors.append(f"{suite_file.relative_to(root)} cases[{index}] must be an object")
                continue
            errors.extend(validate_case_shape(case, index))
            case_id = str(case.get("id", f"cases[{index}]"))
            skill_id = case.get("skill_id")
            prompt = case.get("prompt")
            if isinstance(skill_id, str):
                if skill_id not in skill_ids:
                    errors.append(f"{case_id}: unknown skill_id {skill_id!r}")
                else:
                    covered.add(skill_id)
            if isinstance(prompt, str):
                errors.extend(prompt_leak_errors(prompt, skill_ids, case_id))
                selected, score, ranked = trigger_runner.route_prompt(prompt, skill_descriptions)
                if isinstance(skill_id, str) and selected != skill_id:
                    errors.append(
                        f"{case_id}: deterministic route selected {selected or 'none'} "
                        f"instead of {skill_id} ({score:.2f}); top={ranked}"
                    )
            for resource in case.get("required_resources", []) if isinstance(case.get("required_resources"), list) else []:
                if isinstance(resource, str) and not (root / resource).exists():
                    errors.append(f"{case_id}: required resource does not exist: {resource}")
            capture = case.get("capture")
            if isinstance(capture, dict):
                for patched_path in capture.get("patched_paths", []) if isinstance(capture.get("patched_paths"), list) else []:
                    if isinstance(patched_path, str) and not (root / patched_path).exists():
                        errors.append(f"{case_id}: patched path does not exist: {patched_path}")
            summaries.append(f"{case_id}: {skill_id}")

    missing = sorted(set(skill_ids) - covered)
    for skill_id in missing:
        errors.append(f"Missing forward-test coverage for registered skill: {skill_id}")

    return summaries, errors


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    summaries, errors = validate_forward_suite(root)
    if errors:
        print(f"FAIL forward tests: {len(errors)} issue(s)")
        for summary in summaries:
            print(f"- {summary}")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS forward tests")
    print(f"- Root: {root}")
    print(f"- Cases: {len(summaries)}")
    for summary in summaries:
        print(f"- {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
