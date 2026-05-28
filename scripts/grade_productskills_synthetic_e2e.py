#!/usr/bin/env python3
"""Grade captured ProductSkills synthetic E2E artifacts with existing eval harnesses."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_PACK_DIR = "test-results/productskills-e2e-synthetic"
DEFAULT_MAP = f"{DEFAULT_PACK_DIR}/eval-map.json"


@dataclass(frozen=True)
class PromptMapping:
    prompt_id: str
    prompt_path: Path
    expected_observation_path: Path
    expected_case: str
    expected_fixture: Path


def load_module(root: Path, module_name: str, relative_path: str):
    script_path = root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_mappings(root: Path, map_path: Path) -> list[PromptMapping]:
    data = read_json(map_path)
    prompts = data.get("prompts")
    if not isinstance(prompts, list) or not prompts:
        raise ValueError(f"{map_path} must contain a non-empty prompts list")

    mappings: list[PromptMapping] = []
    for index, item in enumerate(prompts):
        if not isinstance(item, dict):
            raise ValueError(f"{map_path} prompts[{index}] must be an object")
        try:
            mappings.append(
                PromptMapping(
                    prompt_id=str(item["prompt_id"]),
                    prompt_path=root / str(item["prompt_path"]),
                    expected_observation_path=root / str(item["expected_observation_path"]),
                    expected_case=str(item["expected_case"]),
                    expected_fixture=root / str(item["expected_fixture"]),
                )
            )
        except KeyError as exc:
            raise ValueError(f"{map_path} prompts[{index}] missing {exc.args[0]!r}") from exc
    return mappings


def ensure_mapping_paths(mappings: list[PromptMapping]) -> list[str]:
    missing: list[str] = []
    for mapping in mappings:
        for path in (mapping.prompt_path, mapping.expected_observation_path, mapping.expected_fixture):
            if not path.exists():
                missing.append(str(path))
    return missing


def grade_artifacts(
    root: Path,
    pack_dir: Path,
    runtime: str,
    mappings: list[PromptMapping],
    allow_missing: bool,
) -> tuple[list[dict[str, Any]], list[str]]:
    grade_artifact = load_module(root, "productskills_grade_artifact", "scripts/grade_artifact.py")
    generated_dir = pack_dir / "generated" / runtime
    graded_dir = pack_dir / "graded" / runtime
    graded_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    failures: list[str] = []

    for mapping in mappings:
        artifact_path = generated_dir / f"{mapping.prompt_id}.md"
        output_path = graded_dir / f"{mapping.prompt_id}.json"
        if not artifact_path.exists():
            message = f"missing generated artifact: {artifact_path.relative_to(root)}"
            results.append(
                {
                    "runtime": runtime,
                    "prompt_id": mapping.prompt_id,
                    "prompt_path": str(mapping.prompt_path.relative_to(root)),
                    "expected_observation_path": str(mapping.expected_observation_path.relative_to(root)),
                    "expected_case": mapping.expected_case,
                    "expected_fixture": str(mapping.expected_fixture.relative_to(root)),
                    "artifact_path": str(artifact_path.relative_to(root)),
                    "status": "missing",
                    "passed": False,
                    "message": message,
                }
            )
            if not allow_missing:
                failures.append(message)
            continue

        artifact_text = artifact_path.read_text(encoding="utf-8")
        try:
            result = grade_artifact.grade_artifact(
                root=root,
                case_id=mapping.expected_case,
                artifact_text=artifact_text,
                artifact_path=artifact_path,
                expected_path=mapping.expected_fixture,
            )
        except grade_artifact.ArtifactEvalError as exc:
            result = {
                "runtime": runtime,
                "prompt_id": mapping.prompt_id,
                "prompt_path": str(mapping.prompt_path.relative_to(root)),
                "expected_observation_path": str(mapping.expected_observation_path.relative_to(root)),
                "expected_case": mapping.expected_case,
                "expected_fixture": str(mapping.expected_fixture.relative_to(root)),
                "artifact_path": str(artifact_path.relative_to(root)),
                "status": "error",
                "passed": False,
                "message": str(exc),
            }
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            results.append(result)
            failures.append(f"{mapping.prompt_id}: artifact grade error: {exc}")
            continue
        result.update(
            {
                "runtime": runtime,
                "prompt_id": mapping.prompt_id,
                "prompt_path": str(mapping.prompt_path.relative_to(root)),
                "expected_observation_path": str(mapping.expected_observation_path.relative_to(root)),
                "status": "graded",
            }
        )
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        results.append(result)
        if not result.get("passed"):
            failures.append(f"{mapping.prompt_id}: artifact grade failed")

    return results, failures


def grade_tool_safety(root: Path, pack_dir: Path, runtime: str) -> tuple[dict[str, Any] | None, list[str]]:
    fixture_dir = pack_dir / "generated" / runtime / "tool-safety-fixtures"
    if not fixture_dir.exists():
        return None, []

    check_tool_safety = load_module(root, "productskills_check_tool_safety", "scripts/check_tool_safety.py")
    graded_dir = pack_dir / "graded" / runtime
    graded_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, Any]] = []
    failures: list[str] = []
    for fixture_path in sorted(fixture_dir.glob("*.json")):
        try:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{fixture_path.relative_to(root)}: invalid JSON: {exc}")
            continue
        if not isinstance(fixture, dict):
            failures.append(f"{fixture_path.relative_to(root)}: fixture must be an object")
            continue
        issues = check_tool_safety.evaluate_fixture(root, fixture)
        actual = "pass" if not issues else "fail"
        expected = fixture.get("expected")
        passed = actual == expected
        summaries.append(
            {
                "fixture_path": str(fixture_path.relative_to(root)),
                "case": fixture.get("case"),
                "tool": fixture.get("tool"),
                "scenario": fixture.get("scenario"),
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "issues": issues,
            }
        )
        if not passed:
            failures.append(f"{fixture_path.relative_to(root)} expected {expected}, got {actual}")

    result = {
        "runtime": runtime,
        "fixture_dir": str(fixture_dir.relative_to(root)),
        "passed": not failures,
        "fixtures": summaries,
    }
    (graded_dir / "tool-safety.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result, failures


def write_summary(root: Path, pack_dir: Path, runtime: str, results: list[dict[str, Any]], tool_result: dict[str, Any] | None) -> None:
    graded_dir = pack_dir / "graded" / runtime
    passed = sum(1 for result in results if result.get("passed"))
    graded = sum(1 for result in results if result.get("status") == "graded")
    missing = sum(1 for result in results if result.get("status") == "missing")
    summary = {
        "runtime": runtime,
        "generated_dir": str((pack_dir / "generated" / runtime).relative_to(root)),
        "graded_dir": str(graded_dir.relative_to(root)),
        "artifact_results": {
            "total_prompts": len(results),
            "graded": graded,
            "missing": missing,
            "passed": passed,
            "failed": graded - passed,
        },
        "tool_safety": tool_result,
        "pass_requires_generated_artifact_and_grader_result": True,
    }
    (graded_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Grade ProductSkills synthetic E2E generated artifacts into test-results graded JSON."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--runtime", required=True, help="Runtime directory name, such as codex, claude, gemini, or manual.")
    parser.add_argument("--pack-dir", default=DEFAULT_PACK_DIR, help=f"Pack directory. Defaults to {DEFAULT_PACK_DIR}.")
    parser.add_argument("--map", default=DEFAULT_MAP, help=f"Prompt eval map. Defaults to {DEFAULT_MAP}.")
    parser.add_argument("--allow-missing", action="store_true", help="Grade existing artifacts and report missing artifacts without failing.")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    root = Path(args.root).resolve()
    pack_dir = (root / args.pack_dir).resolve()
    map_path = (root / args.map).resolve()

    try:
        mappings = load_mappings(root, map_path)
        missing_mapping_paths = ensure_mapping_paths(mappings)
    except (OSError, ValueError) as exc:
        print(f"FAIL synthetic E2E grading setup: {exc}", file=sys.stderr)
        return 2
    if missing_mapping_paths:
        print("FAIL synthetic E2E grading setup: missing mapped files", file=sys.stderr)
        for path in missing_mapping_paths:
            print(f"- {path}", file=sys.stderr)
        return 2

    artifact_results, artifact_failures = grade_artifacts(
        root=root,
        pack_dir=pack_dir,
        runtime=args.runtime,
        mappings=mappings,
        allow_missing=args.allow_missing,
    )
    tool_result, tool_failures = grade_tool_safety(root, pack_dir, args.runtime)
    write_summary(root, pack_dir, args.runtime, artifact_results, tool_result)

    failures = [*artifact_failures, *tool_failures]
    status = "PASS" if not failures else "FAIL"
    print(f"{status} synthetic E2E grading for runtime {args.runtime}")
    print(f"- Graded artifacts: {sum(1 for result in artifact_results if result.get('status') == 'graded')}/{len(artifact_results)}")
    print(f"- Missing artifacts: {sum(1 for result in artifact_results if result.get('status') == 'missing')}")
    if tool_result is not None:
        print(f"- Tool-safety fixtures: {len(tool_result['fixtures'])}")
    if failures:
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
