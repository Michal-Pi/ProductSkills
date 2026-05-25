#!/usr/bin/env python3
"""Validate the Product Operating System skill package structure."""

from __future__ import annotations

import json
import importlib.util
import re
import sys
from pathlib import Path


REQUIRED_ROOT_DIRS = ("references", "templates", "schemas", "evals", "scripts")
REQUIRED_DOC_FILES = (
    "docs/RELEASE_NOTES_0.1.0.md",
    "docs/KNOWN_LIMITATIONS_0.1.0.md",
    "docs/LOCAL_INSTALLATION.md",
    "docs/RELEASE_CANDIDATE_CHECKLIST.md",
    "docs/SCHEMA_SUBSET.md",
)
REQUIRED_EVAL_FILES = (
    "evals/trigger-tests.yaml",
    "evals/artifact-quality-rubrics.yaml",
    "scripts/run_trigger_evals.py",
    "scripts/grade_artifact.py",
    "scripts/check_tool_safety.py",
    "scripts/check_forward_tests.py",
)
REQUIRED_METHOD_CHECKLISTS = (
    "references/checklists/discovery-method-coverage.md",
    "references/checklists/prioritization-method-coverage.md",
    "references/checklists/validation-method-coverage.md",
    "references/checklists/design-method-coverage.md",
    "references/checklists/docs-quality.md",
    "references/checklists/growth-method-coverage.md",
    "references/checklists/delivery-method-coverage.md",
    "references/checklists/launch-method-coverage.md",
    "references/checklists/tooling-safety.md",
)
REQUIRED_WORKFLOW_CONTRACTS = {
    "workflow-product-operating-system": (
        "references/workflows/product-operating-system-contract.md",
        "references/workflows/workflow-lifecycle-statuses.md",
        "schemas/product-operating-system-handoff.schema.json",
    ),
    "workflow-discovery-to-prd": (
        "references/workflows/discovery-to-prd-contract.md",
        "schemas/discovery-to-prd-handoff.schema.json",
    ),
    "workflow-prd-to-linear-delivery": (
        "references/workflows/prd-to-linear-delivery-contract.md",
        "schemas/prd-to-delivery-handoff.schema.json",
    ),
}
REQUIRED_PRODUCT_OS_ASSETS = (
    "skills/workflow-product-operating-system/SKILL.md",
    "skills/workflow-product-operating-system/procedures/product-operating-system.md",
    "references/workflows/product-operating-system-contract.md",
    "references/workflows/workflow-lifecycle-statuses.md",
    "templates/workflow-stage-output.md",
    "templates/blocked-workflow.md",
    "templates/validation-decision.md",
    "templates/launch-readiness-gate.md",
    "templates/post-launch-learning-loop.md",
    "schemas/workflow-stage.schema.json",
    "schemas/workflow-stage-output.schema.json",
    "schemas/blocked-workflow.schema.json",
    "schemas/validation-decision.schema.json",
    "schemas/launch-readiness-gate.schema.json",
    "schemas/post-launch-learning.schema.json",
    "schemas/product-operating-system-handoff.schema.json",
)
REQUIRED_WORKFLOW_STATUSES = (
    "intake_received",
    "evidence_insufficient",
    "evidence_synthesized",
    "opportunity_framed",
    "needs_validation",
    "validation_not_required",
    "ready_for_prd",
    "prd_review_required",
    "prd_ready",
    "ready_for_delivery_gate",
    "approved_for_delivery",
    "delivery_review_required",
    "delivery_ready",
    "ready_for_tool_preview",
    "ready_for_human_write_confirmation",
    "ready_for_launch_review",
    "launch_ready",
    "launched_or_handed_off",
    "learning_loop_open",
    "blocked",
)
RESOURCE_REF_RE = re.compile(
    r"`((?:(?:\.\./)+|procedures/|references/|templates/|schemas/|evals/)[^`]+?\.(?:md|json|yaml))`"
)


def load_registry(root: Path, errors: list[str]) -> dict:
    registry_path = root / "registry.json"
    if not registry_path.exists():
        errors.append("Missing registry.json")
        return {}

    try:
        return json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"registry.json does not parse as JSON: {exc}")
        return {}


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return frontmatter
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return {}


def validate_resource_refs(root: Path, markdown_file: Path, errors: list[str]) -> None:
    text = markdown_file.read_text(encoding="utf-8")
    for ref in RESOURCE_REF_RE.findall(text):
        is_procedure = "procedures" in markdown_file.relative_to(root).parts
        if is_procedure and ref.startswith(("references/", "templates/", "schemas/", "evals/")):
            errors.append(
                f"Procedure resource reference must be relative in {markdown_file.relative_to(root)}: {ref}"
            )
            continue
        if ref.startswith(("references/", "templates/", "schemas/", "evals/")):
            ref_path = (root / ref).resolve()
        else:
            ref_path = (markdown_file.parent / ref).resolve()
        if not ref_path.exists():
            errors.append(f"Broken resource reference in {markdown_file.relative_to(root)}: {ref}")


def validate_skill(root: Path, entry: object, errors: list[str]) -> str | None:
    if not isinstance(entry, dict):
        errors.append("Registry skill entry is not an object")
        return None

    skill_id = entry.get("id")
    skill_path = entry.get("path")
    if not isinstance(skill_id, str) or not skill_id:
        errors.append(f"Registry skill missing id: {entry}")
        return None
    if not isinstance(skill_path, str) or not skill_path:
        errors.append(f"Registry skill {skill_id} missing path")
        return skill_id
    skill_type = entry.get("type")

    folder = root / skill_path
    if not folder.exists():
        errors.append(f"Registry path does not exist for {skill_id}: {skill_path}")
        return skill_id
    if not folder.is_dir():
        errors.append(f"Registry path is not a directory for {skill_id}: {skill_path}")
        return skill_id

    skill_md = folder / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md for {skill_id}: {skill_path}")
        return skill_id

    frontmatter = parse_frontmatter(skill_md)
    if not frontmatter:
        errors.append(f"{skill_md.relative_to(root)} must start with YAML-style frontmatter")
        return skill_id

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name:
        errors.append(f"{skill_md.relative_to(root)} frontmatter missing name")
    if not description:
        errors.append(f"{skill_md.relative_to(root)} frontmatter missing description")
    if name and folder.name != name:
        errors.append(
            f"{skill_md.relative_to(root)} name '{name}' does not match folder '{folder.name}'"
        )
    if name and skill_id != name:
        errors.append(f"Registry id '{skill_id}' does not match SKILL.md name '{name}'")

    if skill_type == "family":
        procedures_dir = folder / "procedures"
        if not procedures_dir.exists():
            errors.append(f"Family skill {skill_id} missing procedures/ directory")
        else:
            procedure_count = len(list(procedures_dir.glob("*.md")))
            if procedure_count < 2:
                errors.append(f"Family skill {skill_id} needs at least two procedure files")

    if skill_type == "workflow":
        procedures_dir = folder / "procedures"
        if not procedures_dir.exists():
            errors.append(f"Workflow skill {skill_id} missing procedures/ directory")
        elif not list(procedures_dir.glob("*.md")):
            errors.append(f"Workflow skill {skill_id} needs at least one procedure file")
        contract_paths = REQUIRED_WORKFLOW_CONTRACTS.get(skill_id)
        if not contract_paths:
            errors.append(f"Workflow skill {skill_id} missing required contract mapping")
        else:
            for contract_path in contract_paths:
                if not (root / contract_path).exists():
                    errors.append(f"Workflow skill {skill_id} missing contract resource: {contract_path}")

    validate_resource_refs(root, skill_md, errors)

    return skill_id


def extract_trigger_skill_ids(trigger_tests: Path) -> set[str]:
    return {case["skill_id"] for case in extract_trigger_cases(trigger_tests) if case.get("skill_id")}


def extract_trigger_cases(trigger_tests: Path) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in trigger_tests.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- id:"):
            if current:
                cases.append(current)
            current = {"id": stripped.split(":", 1)[1].strip().strip('"').strip("'")}
            continue
        if current is None:
            continue
        if stripped.startswith("skill_id:"):
            current["skill_id"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
        elif stripped.startswith("should_trigger:"):
            value = stripped.split(":", 1)[1].strip().lower()
            current["should_trigger"] = value == "true"

    if current:
        cases.append(current)
    return cases


def validate_golden_expected(root: Path, errors: list[str]) -> None:
    golden_dir = root / "evals/golden-cases"
    expected_dir = root / "evals/expected"
    if not golden_dir.exists():
        errors.append("Missing evals/golden-cases/ directory")
        return
    if not expected_dir.exists():
        errors.append("Missing evals/expected/ directory")
        return

    grade_artifact = load_artifact_grader(root, errors)
    try:
        rubrics = (
            grade_artifact.parse_rubric_file(root / "evals/artifact-quality-rubrics.yaml")
            if grade_artifact
            else {}
        )
    except Exception as exc:
        errors.append(f"Artifact grader/rubric validation failed to load: {exc}")
        rubrics = {}

    for golden_case in sorted(golden_dir.glob("*.md")):
        expected = expected_dir / f"{golden_case.stem}.yaml"
        if not expected.exists():
            errors.append(f"Missing expected-quality fixture for golden case: {golden_case.name}")
            continue
        try:
            fixture = grade_artifact.parse_expected_file(expected)
        except Exception as exc:
            errors.append(f"Invalid expected-quality fixture {expected.relative_to(root)}: {exc}")
            continue
        if fixture.case != golden_case.stem:
            errors.append(f"Expected fixture case name does not match golden case: {expected.name}")
        for rubric_id in fixture.rubrics:
            if rubric_id not in rubrics:
                errors.append(
                    f"Expected fixture {expected.relative_to(root)} references unknown rubric: {rubric_id}"
                )

    if grade_artifact:
        validate_artifact_fixture_smoke_tests(root, grade_artifact, errors)


def load_artifact_grader(root: Path, errors: list[str]):
    script_path = root / "scripts/grade_artifact.py"
    if not script_path.exists():
        errors.append("Missing artifact grader script: scripts/grade_artifact.py")
        return None
    spec = importlib.util.spec_from_file_location("product_os_grade_artifact", script_path)
    if spec is None or spec.loader is None:
        errors.append("Could not load artifact grader module spec")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    except Exception as exc:
        errors.append(f"Could not import artifact grader: {exc}")
        return None
    return module


def validate_artifact_fixture_smoke_tests(root: Path, grade_artifact, errors: list[str]) -> None:
    smoke_cases = (
        ("prd-generation", "evals/artifact-fixtures/passing-prd-generation.md", True),
        ("prd-generation", "evals/artifact-fixtures/failing-prd-generation.md", False),
        ("delivery-breakdown", "evals/artifact-fixtures/passing-delivery-breakdown.md", True),
        (
            "skill-versioning-no-evidence",
            "evals/artifact-fixtures/passing-skill-versioning-no-evidence.md",
            True,
        ),
        (
            "product-os-no-evidence-blocked",
            "evals/artifact-fixtures/passing-product-os-no-evidence-blocked.md",
            True,
        ),
        (
            "product-os-approved-prd-reentry",
            "evals/artifact-fixtures/passing-product-os-approved-prd-reentry.md",
            True,
        ),
        (
            "product-os-post-launch-learning",
            "evals/artifact-fixtures/passing-product-os-post-launch-learning.md",
            True,
        ),
    )
    for case_id, fixture_name, should_pass in smoke_cases:
        fixture_path = root / fixture_name
        if not fixture_path.exists():
            errors.append(f"Missing artifact grader smoke fixture: {fixture_name}")
            continue
        try:
            result = grade_artifact.grade_artifact(
                root=root,
                case_id=case_id,
                artifact_text=fixture_path.read_text(encoding="utf-8"),
                artifact_path=fixture_path,
            )
        except Exception as exc:
            errors.append(f"Artifact grader smoke fixture errored for {fixture_name}: {exc}")
            continue
        if bool(result.get("passed")) is not should_pass:
            expected = "pass" if should_pass else "fail"
            actual = "pass" if result.get("passed") else "fail"
            errors.append(
                f"Artifact grader smoke fixture {fixture_name} should {expected} but got {actual}"
            )


def validate_json_files(root: Path, errors: list[str]) -> None:
    for json_file in sorted((root / "schemas").glob("*.json")):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{json_file.relative_to(root)} does not parse as JSON: {exc}")


def validate_product_os_assets(root: Path, errors: list[str]) -> None:
    for filename in REQUIRED_PRODUCT_OS_ASSETS:
        if not (root / filename).exists():
            errors.append(f"Missing Product OS workflow asset: {filename}")

    status_schema = root / "schemas/workflow-stage.schema.json"
    if status_schema.exists():
        try:
            parsed = json.loads(status_schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        statuses = parsed.get("enum", [])
        if not isinstance(statuses, list):
            errors.append("schemas/workflow-stage.schema.json must define an enum")
            return
        for status in REQUIRED_WORKFLOW_STATUSES:
            if status not in statuses:
                errors.append(f"Canonical workflow status missing from schema: {status}")

    validation_schema = root / "schemas/validation-decision.schema.json"
    if validation_schema.exists():
        text = validation_schema.read_text(encoding="utf-8")
        for decision in (
            "validation_not_required",
            "proceed_to_prd",
            "run_validation_first",
            "stop_for_missing_evidence",
        ):
            if decision not in text:
                errors.append(f"Validation decision schema missing decision: {decision}")


def validate_tool_safety_fixtures(root: Path, errors: list[str]) -> None:
    script_path = root / "scripts/check_tool_safety.py"
    if not script_path.exists():
        errors.append("Missing tool safety evaluator: scripts/check_tool_safety.py")
        return
    spec = importlib.util.spec_from_file_location("product_os_check_tool_safety", script_path)
    if spec is None or spec.loader is None:
        errors.append("Could not load tool safety evaluator module spec")
        return
    module = importlib.util.module_from_spec(spec)
    try:
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _, failures = module.run_fixture_suite(root)
    except Exception as exc:
        errors.append(f"Tool safety fixture validation errored: {exc}")
        return
    for failure in failures:
        errors.append(f"Tool safety fixture validation failed: {failure}")


def validate_forward_tests(root: Path, errors: list[str]) -> None:
    script_path = root / "scripts/check_forward_tests.py"
    if not script_path.exists():
        errors.append("Missing forward-test evaluator: scripts/check_forward_tests.py")
        return
    spec = importlib.util.spec_from_file_location("product_os_check_forward_tests", script_path)
    if spec is None or spec.loader is None:
        errors.append("Could not load forward-test evaluator module spec")
        return
    module = importlib.util.module_from_spec(spec)
    try:
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _, failures = module.validate_forward_suite(root)
    except Exception as exc:
        errors.append(f"Forward-test validation errored: {exc}")
        return
    for failure in failures:
        errors.append(f"Forward-test validation failed: {failure}")


def validate_package_router(root: Path, skill_ids: list[str], errors: list[str]) -> None:
    package_path = root / "package.yaml"
    if not package_path.exists():
        return
    lines = package_path.read_text(encoding="utf-8").splitlines()
    in_entry_workflows = False
    for line in lines:
        if not line.startswith("default_router:"):
            if line.startswith("entry_workflows:"):
                in_entry_workflows = True
                continue
            if in_entry_workflows and line.startswith("  - "):
                workflow_id = line.split("-", 1)[1].strip().strip('"').strip("'")
                if workflow_id not in skill_ids:
                    errors.append(f"package.yaml entry_workflows item is not registered: {workflow_id}")
                continue
            if line and not line.startswith(" "):
                in_entry_workflows = False
            continue
        value = line.split(":", 1)[1].strip().strip('"').strip("'")
        if value and value not in {"null", "~"} and value not in skill_ids:
            errors.append(f"package.yaml default_router points to unregistered skill: {value}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    if not (root / "package.yaml").exists():
        errors.append("Missing package.yaml")

    for dirname in REQUIRED_ROOT_DIRS:
        path = root / dirname
        if not path.exists():
            errors.append(f"Missing required root directory: {dirname}/")
        elif not path.is_dir():
            errors.append(f"Required root path is not a directory: {dirname}/")

    for filename in REQUIRED_DOC_FILES:
        if not (root / filename).exists():
            errors.append(f"Missing required doc file: {filename}")

    for filename in REQUIRED_EVAL_FILES:
        if not (root / filename).exists():
            errors.append(f"Missing required eval file: {filename}")

    for filename in REQUIRED_METHOD_CHECKLISTS:
        if not (root / filename).exists():
            errors.append(f"Missing required method checklist: {filename}")

    registry = load_registry(root, errors)
    skills = registry.get("skills", []) if isinstance(registry, dict) else []
    if not isinstance(skills, list):
        errors.append("registry.json field 'skills' must be a list")
        skills = []

    skill_ids: list[str] = []
    for entry in skills:
        skill_id = validate_skill(root, entry, errors)
        if skill_id:
            skill_ids.append(skill_id)

    validate_package_router(root, skill_ids, errors)

    trigger_path = root / "evals/trigger-tests.yaml"
    if trigger_path.exists():
        trigger_cases = extract_trigger_cases(trigger_path)
        covered_ids = {case["skill_id"] for case in trigger_cases if case.get("skill_id")}
        for skill_id in skill_ids:
            if skill_id not in covered_ids:
                errors.append(f"Missing trigger coverage for registered skill: {skill_id}")
            if not any(
                case.get("skill_id") == skill_id and case.get("should_trigger") is True
                for case in trigger_cases
            ):
                errors.append(f"Missing positive trigger case for registered skill: {skill_id}")
            if not any(
                case.get("skill_id") == skill_id and case.get("should_trigger") is False
                for case in trigger_cases
            ):
                errors.append(f"Missing negative trigger case for registered skill: {skill_id}")

    for markdown_file in (root / "skills").glob("**/*.md"):
        if markdown_file.name != "SKILL.md":
            validate_resource_refs(root, markdown_file, errors)

    validate_golden_expected(root, errors)
    validate_json_files(root, errors)
    validate_product_os_assets(root, errors)
    validate_tool_safety_fixtures(root, errors)
    validate_forward_tests(root, errors)

    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    errors = validate(root)

    if errors:
        print(f"FAIL package validation: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS package validation")
    print(f"- Root: {root}")
    print("- package.yaml exists")
    print("- registry.json parses")
    print("- registered skills are loadable")
    print("- default router is absent or registered")
    print("- skill frontmatter is valid")
    print("- family skills include procedure baselines")
    print("- workflow skills include procedures and handoff contracts")
    print("- SKILL.md resource references resolve")
    print("- method coverage checklists exist")
    print("- golden cases have expected-quality fixtures")
    print("- required root directories exist")
    print("- release-candidate docs exist")
    print("- trigger coverage includes positive and negative cases for every registered skill")
    print("- trigger eval runner exists")
    print("- artifact grader exists")
    print("- expected-quality fixtures reference existing rubrics")
    print("- artifact grader smoke fixtures behave as expected")
    print("- tool safety evaluator and fixtures behave as expected")
    print("- forward-test coverage exists for every registered skill")
    print("- schema JSON files parse")
    print("- Product OS workflow assets and lifecycle statuses exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
