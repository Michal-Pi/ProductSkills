#!/usr/bin/env python3
"""Grade generated PM artifacts against golden-case expectations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


EXPECTED_LIST_KEYS = ("skill_ids", "rubrics", "expected_sections", "must_include", "must_not_include")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "before",
    "for",
    "from",
    "in",
    "includes",
    "into",
    "is",
    "or",
    "that",
    "the",
    "to",
    "uses",
    "with",
}
NEGATION_WORDS = {
    "absence",
    "avoid",
    "avoids",
    "blocked",
    "disabled",
    "exclude",
    "excludes",
    "excluding",
    "forbid",
    "forbids",
    "free",
    "lacks",
    "never",
    "no",
    "not",
    "prevent",
    "prevented",
    "prevents",
    "prohibit",
    "prohibited",
    "prohibits",
    "without",
}


class ArtifactEvalError(ValueError):
    """Raised when grader input files are missing or invalid."""


@dataclass(frozen=True)
class ExpectedFixture:
    case: str
    skill_ids: list[str]
    rubrics: list[str]
    expected_sections: list[str]
    must_include: list[str]
    must_not_include: list[str]


@dataclass(frozen=True)
class Rubric:
    rubric_id: str
    required_checks: list[str]


def unquote(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_simple_fixture(path: Path) -> dict[str, str | list[str]]:
    """Parse the simple YAML subset used by eval expected fixtures."""
    parsed: dict[str, str | list[str]] = {}
    current_key: str | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            if current_key is None:
                raise ArtifactEvalError(f"{path}: line {line_number} has a list item without a key")
            existing = parsed.setdefault(current_key, [])
            if not isinstance(existing, list):
                raise ArtifactEvalError(f"{path}: line {line_number} mixes scalar and list values")
            existing.append(unquote(stripped[2:]))
            continue
        if ":" not in stripped:
            raise ArtifactEvalError(f"{path}: line {line_number} is not a supported key/value line")
        key, value = stripped.split(":", 1)
        current_key = key.strip()
        parsed[current_key] = unquote(value) if value.strip() else []

    return parsed


def parse_expected_file(path: Path) -> ExpectedFixture:
    if not path.exists():
        raise ArtifactEvalError(f"Missing expected fixture: {path}")
    parsed = parse_simple_fixture(path)

    case = parsed.get("case")
    if not isinstance(case, str) or not case:
        raise ArtifactEvalError(f"{path}: missing scalar case")

    values: dict[str, list[str]] = {}
    for key in EXPECTED_LIST_KEYS:
        value = parsed.get(key)
        if not isinstance(value, list) or not value:
            raise ArtifactEvalError(f"{path}: missing non-empty list {key}")
        values[key] = value

    return ExpectedFixture(
        case=case,
        skill_ids=values["skill_ids"],
        rubrics=values["rubrics"],
        expected_sections=values["expected_sections"],
        must_include=values["must_include"],
        must_not_include=values["must_not_include"],
    )


def parse_rubric_file(path: Path) -> dict[str, Rubric]:
    """Parse rubric IDs and required checks from the package rubric file."""
    if not path.exists():
        raise ArtifactEvalError(f"Missing rubric file: {path}")

    rubrics: dict[str, Rubric] = {}
    in_rubrics = False
    current_id: str | None = None
    current_section: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0:
            in_rubrics = stripped == "rubrics:"
            current_id = None
            current_section = None
            continue
        if not in_rubrics:
            continue
        if indent == 2 and stripped.endswith(":"):
            current_id = stripped[:-1].strip()
            rubrics[current_id] = Rubric(rubric_id=current_id, required_checks=[])
            current_section = None
            continue
        if indent == 4 and current_id:
            current_section = stripped.split(":", 1)[0].strip()
            continue
        if indent == 6 and current_id and current_section == "required_checks" and stripped.startswith("- "):
            existing = rubrics[current_id]
            rubrics[current_id] = Rubric(
                rubric_id=current_id,
                required_checks=[*existing.required_checks, unquote(stripped[2:])],
            )

    if not rubrics:
        raise ArtifactEvalError(f"{path}: no rubrics found")
    return rubrics


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


def normalize_heading(text: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", text.lower())).strip("_")


def concept_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    }


def extract_sections(markdown: str) -> set[str]:
    sections: set[str] = set()
    for line in markdown.splitlines():
        heading_match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading_match:
            sections.add(normalize_heading(heading_match.group(1)))
            continue
        bold_label_match = re.match(r"^\s{0,3}\*\*(.+?)\*\*\s*:", line)
        if bold_label_match:
            sections.add(normalize_heading(bold_label_match.group(1)))
            continue
        plain_label_match = re.match(r"^\s{0,3}([A-Z][A-Za-z0-9 /_-]{2,60})\s*:\s*$", line)
        if plain_label_match:
            sections.add(normalize_heading(plain_label_match.group(1)))
    return sections


def has_section(sections: set[str], expected_section: str) -> bool:
    normalized = normalize_heading(expected_section)
    return any(
        section == normalized or section.endswith(f"_{normalized}")
        for section in sections
    )


def contains_concept(markdown: str, concept: str) -> bool:
    normalized_markdown = normalize_text(markdown)
    normalized_concept = normalize_text(concept)
    if normalized_concept and normalized_concept in normalized_markdown:
        return True

    tokens = concept_tokens(concept)
    if not tokens:
        return True
    markdown_tokens = concept_tokens(markdown)
    coverage = len(tokens & markdown_tokens) / len(tokens)
    return coverage >= 0.65


def contains_any_clause(markdown: str, concept: str) -> bool:
    clauses = [clause.strip() for clause in re.split(r"\bor\b", concept, flags=re.IGNORECASE) if clause.strip()]
    return any(contains_concept(markdown, clause) for clause in clauses)


def is_negated_context(normalized_markdown: str, start_index: int) -> bool:
    before = normalized_markdown[max(0, start_index - 90) : start_index]
    return bool(set(before.split()[-10:]) & NEGATION_WORDS)


def contains_forbidden(markdown: str, concept: str) -> bool:
    normalized_markdown = normalize_text(markdown)
    normalized_concept = normalize_text(concept)
    if normalized_concept:
        found_exact_match = False
        start = 0
        while True:
            index = normalized_markdown.find(normalized_concept, start)
            if index == -1:
                break
            found_exact_match = True
            if not is_negated_context(normalized_markdown, index):
                return True
            start = index + len(normalized_concept)
        if found_exact_match:
            return False

    tokens = concept_tokens(concept)
    markdown_tokens = concept_tokens(markdown)
    return bool(tokens) and len(tokens & markdown_tokens) / len(tokens) >= 0.85


def infer_case_id(root: Path, artifact_path: Path | None) -> str | None:
    if artifact_path is None:
        return None
    stem = artifact_path.stem
    for prefix in ("passing-", "failing-", "pass-", "fail-"):
        if stem.startswith(prefix):
            stem = stem[len(prefix) :]
            break
    if (root / "evals" / "expected" / f"{stem}.yaml").exists():
        return stem
    return None


def score_from_ratio(ratio: float, has_forbidden: bool) -> int:
    if has_forbidden:
        return 1
    if ratio >= 1.0:
        return 4
    if ratio >= 0.8:
        return 3
    if ratio >= 0.5:
        return 2
    return 1


def grade_artifact(
    root: Path,
    case_id: str,
    artifact_text: str,
    artifact_path: Path | None = None,
    expected_path: Path | None = None,
    rubric_path: Path | None = None,
) -> dict[str, object]:
    expected_path = expected_path or root / "evals" / "expected" / f"{case_id}.yaml"
    rubric_path = rubric_path or root / "evals" / "artifact-quality-rubrics.yaml"
    expected = parse_expected_file(expected_path)
    if expected.case != case_id:
        raise ArtifactEvalError(f"{expected_path}: case {expected.case!r} does not match {case_id!r}")

    rubrics = parse_rubric_file(rubric_path)
    unknown_rubrics = [rubric_id for rubric_id in expected.rubrics if rubric_id not in rubrics]
    if unknown_rubrics:
        raise ArtifactEvalError(f"{expected_path}: unknown rubric IDs: {', '.join(unknown_rubrics)}")

    sections = extract_sections(artifact_text)
    missing_sections = [
        section for section in expected.expected_sections if not has_section(sections, section)
    ]
    missing_must_include = [
        concept for concept in expected.must_include if not contains_concept(artifact_text, concept)
    ]
    forbidden_found = [
        concept for concept in expected.must_not_include if contains_forbidden(artifact_text, concept)
    ]
    rubric_missing: dict[str, list[str]] = {}
    for rubric_id in expected.rubrics:
        missing_checks = [
            check
            for check in rubrics[rubric_id].required_checks
            if not contains_any_clause(artifact_text, check)
        ]
        if missing_checks:
            rubric_missing[rubric_id] = missing_checks

    total_checks = (
        len(expected.expected_sections)
        + len(expected.must_include)
        + sum(len(rubrics[rubric_id].required_checks) for rubric_id in expected.rubrics)
    )
    failed_checks = len(missing_sections) + len(missing_must_include) + sum(
        len(checks) for checks in rubric_missing.values()
    )
    ratio = 1.0 if total_checks == 0 else (total_checks - failed_checks) / total_checks
    overall_score = score_from_ratio(ratio, bool(forbidden_found))

    rubric_scores: dict[str, int] = {}
    for rubric_id in expected.rubrics:
        checks = rubrics[rubric_id].required_checks
        missing_count = len(rubric_missing.get(rubric_id, []))
        rubric_ratio = 1.0 if not checks else (len(checks) - missing_count) / len(checks)
        rubric_scores[rubric_id] = score_from_ratio(rubric_ratio, bool(forbidden_found))

    passed = (
        overall_score >= 3
        and not missing_sections
        and not missing_must_include
        and not forbidden_found
        and not rubric_missing
    )

    return {
        "case": case_id,
        "artifact_path": str(artifact_path) if artifact_path else None,
        "expected_path": str(expected_path),
        "rubric_path": str(rubric_path),
        "golden_case_path": str(root / "evals" / "golden-cases" / f"{case_id}.md"),
        "golden_case_exists": (root / "evals" / "golden-cases" / f"{case_id}.md").exists(),
        "passed": passed,
        "overall_score": overall_score,
        "max_score": 4,
        "rubric_scores": rubric_scores,
        "sections_found": sorted(sections),
        "missing_sections": missing_sections,
        "missing_must_include": missing_must_include,
        "forbidden_found": forbidden_found,
        "missing_rubric_checks": rubric_missing,
    }


def print_text_result(result: dict[str, object]) -> None:
    status = "PASS" if result["passed"] else "FAIL"
    print(f"{status} artifact grade")
    print(f"- Case: {result['case']}")
    if result.get("artifact_path"):
        print(f"- Artifact: {result['artifact_path']}")
    print(f"- Overall score: {result['overall_score']}/{result['max_score']}")
    print(f"- Rubrics: {result['rubric_scores']}")
    print(f"- Golden case exists: {result['golden_case_exists']}")

    for key, label in (
        ("missing_sections", "Missing sections"),
        ("missing_must_include", "Missing must-include concepts"),
        ("forbidden_found", "Forbidden content found"),
    ):
        values = result.get(key)
        if values:
            print(f"- {label}:")
            for value in values if isinstance(values, list) else []:
                print(f"  - {value}")

    missing_rubric_checks = result.get("missing_rubric_checks")
    if isinstance(missing_rubric_checks, dict) and missing_rubric_checks:
        print("- Missing rubric checks:")
        for rubric_id, checks in missing_rubric_checks.items():
            print(f"  - {rubric_id}:")
            for check in checks:
                print(f"    - {check}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Grade a generated artifact against evals/expected and artifact rubrics."
    )
    parser.add_argument("artifact", nargs="?", help="Path to the generated artifact markdown file")
    parser.add_argument("--root", default=".", help="Package root. Defaults to current directory.")
    parser.add_argument("--case", help="Golden-case ID. Defaults to the artifact filename stem.")
    parser.add_argument("--expected", help="Override expected fixture path.")
    parser.add_argument("--rubrics", help="Override rubric file path.")
    parser.add_argument("--text", help="Artifact text to grade instead of reading a file.")
    parser.add_argument("--text-file", help="Read artifact text from this file.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    root = Path(args.root).resolve()
    artifact_path = Path(args.artifact).resolve() if args.artifact else None

    if args.text is not None:
        artifact_text = args.text
    elif args.text_file:
        artifact_path = Path(args.text_file).resolve()
        artifact_text = artifact_path.read_text(encoding="utf-8")
    elif artifact_path:
        artifact_text = artifact_path.read_text(encoding="utf-8")
    else:
        parser.error("provide an artifact path, --text, or --text-file")

    case_id = args.case or infer_case_id(root, artifact_path)
    if not case_id:
        parser.error("could not infer case ID; pass --case")

    try:
        result = grade_artifact(
            root=root,
            case_id=case_id,
            artifact_text=artifact_text,
            artifact_path=artifact_path,
            expected_path=Path(args.expected).resolve() if args.expected else None,
            rubric_path=Path(args.rubrics).resolve() if args.rubrics else None,
        )
    except ArtifactEvalError as exc:
        print(f"FAIL artifact grade: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text_result(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
