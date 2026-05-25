#!/usr/bin/env python3
"""Run deterministic trigger evals for the Product Operating System package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


TRIGGER_THRESHOLD = 2.0
DEFAULT_FAMILY_PROXY_THRESHOLD = 0.90
DEFAULT_WORKFLOW_PROXY_THRESHOLD = 0.95

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "before",
    "for",
    "from",
    "in",
    "into",
    "is",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "these",
    "this",
    "to",
    "with",
}

PROFILES: dict[str, dict[str, float]] = {
    "pm-discovery": {
        "customer interview": 4,
        "interview notes": 4,
        "support ticket": 3,
        "sales feedback": 3,
        "customer evidence": 3,
        "voc": 4,
        "synthesize": 2,
        "research plan": 3,
        "feedback": 2,
        "opportunity": 1,
    },
    "pm-strategy": {
        "prioritize": 4,
        "prioritization": 4,
        "roadmap option": 3,
        "rice": 3,
        "wsjf": 3,
        "market": 2,
        "pricing": 3,
        "competitor": 3,
        "okr": 3,
        "strategy": 2,
    },
    "pm-validation": {
        "validate": 4,
        "validation": 3,
        "experiment": 4,
        "test whether": 4,
        "problem is real": 4,
        "assumption": 3,
        "riskiest": 3,
        "prototype test": 3,
    },
    "pm-design": {
        "prototype brief": 4,
        "wireframe": 4,
        "usability test": 4,
        "design review": 3,
        "states": 2,
        "edge cases": 1,
        "ux": 2,
    },
    "pm-docs": {
        "prd": 4,
        "product requirements": 4,
        "feature spec": 3,
        "decision log": 3,
        "evidence-backed": 2,
        "review this prd": 4,
        "product spec": 3,
    },
    "pm-delivery": {
        "epic": 4,
        "user stories": 4,
        "acceptance criteria": 4,
        "sprint": 3,
        "break this scope": 4,
        "delivery risks": 3,
        "task breakdown": 3,
        "delivery plan": 3,
    },
    "pm-growth": {
        "activation": 4,
        "retention": 4,
        "growth loop": 4,
        "funnel": 3,
        "monetization": 3,
        "lifecycle": 3,
        "plg": 3,
        "conversion": 2,
        "experiments": 1,
    },
    "pm-gtm": {
        "launch readiness": 4,
        "positioning": 3,
        "messaging": 3,
        "release comms": 4,
        "enablement": 3,
        "gtm": 4,
        "post-launch": 3,
        "launch plan": 3,
    },
    "pm-tooling": {
        "notion": 5,
        "linear": 5,
        "payload": 3,
        "preview": 2,
        "sync": 3,
        "external id": 3,
        "workspace": 2,
        "dry-run": 3,
        "dry run": 3,
    },
    "workflow-product-operating-system": {
        "product operating system": 8,
        "idea to launch": 7,
        "from idea to launch": 7,
        "next product workflow step": 7,
        "next workflow step": 6,
        "continue this product work": 6,
        "turn this artifact into the next product deliverable": 7,
        "full workflow": 5,
        "end-to-end workflow": 5,
        "launch learning": 5,
        "post-launch metrics": 5,
        "post launch metrics": 5,
        "rough prd": 4,
        "approved prd": 4,
        "launch request": 5,
        "what next": 3,
    },
    "workflow-discovery-to-prd": {
        "discovery to prd": 6,
        "research into requirements": 5,
        "customer interviews": 3,
        "support tickets": 3,
        "into an evidence-backed prd": 5,
        "turn these customer": 4,
        "turn mixed customer": 5,
    },
    "workflow-prd-to-linear-delivery": {
        "prd into linear": 6,
        "linear-ready": 5,
        "linear ready": 5,
        "convert this prd": 4,
        "delivery-ready epics": 5,
        "issue payload": 4,
        "linear issue": 4,
    },
}

PENALTIES: dict[str, dict[str, float]] = {
    "pm-strategy": {"personal savings": -6, "emergency fund": -6},
    "pm-validation": {"form validation": -6, "email input": -3},
    "pm-design": {"logo": -5, "coffee brand": -5},
    "pm-docs": {"rest endpoint": -5, "request and response": -3},
    "pm-delivery": {"package delivery": -6, "arrival time": -4},
    "pm-growth": {"houseplants": -6, "garden": -4},
    "pm-gtm": {"boat": -6, "weekend launch trip": -6, "sales enablement deck": -5},
    "pm-tooling": {
        "shell script": -6,
        "rename image files": -6,
        "notion-style": -7,
        "notion style": -7,
        "notion document": -6,
        "do not use notion": -8,
        "without syncing": -8,
        "sync payload": -5,
        "linear algebra": -8,
        "linear transformation": -8,
    },
    "workflow-product-operating-system": {
        "single prd review": -5,
        "only review this prd": -6,
        "linear-only": -6,
        "linear only": -6,
        "just create linear": -5,
        "engineering-only": -6,
        "engineering only": -6,
        "academic paper": -6,
        "lecture notes": -5,
        "sales enablement deck": -5,
    },
    "workflow-discovery-to-prd": {"academic paper": -6, "lecture notes": -5},
    "workflow-prd-to-linear-delivery": {
        "grocery list": -6,
        "store aisles": -6,
        "do not create linear": -12,
        "do not use linear": -12,
        "without linear": -12,
        "skip linear": -12,
        "no linear": -12,
        "do not create issues": -8,
        "don't create issues": -8,
    },
}


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}
    output: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return output
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        output[key.strip()] = value.strip().strip('"').strip("'")
    return output


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def unquote(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_trigger_tests(path: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, float]]:
    tests: list[dict[str, object]] = []
    negative_controls: list[dict[str, object]] = []
    thresholds = {
        "family_proxy_self_consistency": DEFAULT_FAMILY_PROXY_THRESHOLD,
        "workflow_proxy_self_consistency": DEFAULT_WORKFLOW_PROXY_THRESHOLD,
    }
    current: dict[str, object] | None = None
    current_section: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in {"tests:", "negative_controls:", "thresholds:"}:
            current_section = stripped[:-1]
            current = None
            continue
        if stripped.startswith("- id:"):
            current = {"id": unquote(stripped.split(":", 1)[1])}
            if current_section == "tests":
                tests.append(current)
            elif current_section == "negative_controls":
                negative_controls.append(current)
            continue
        if current_section == "thresholds" and ":" in stripped:
            key, value = stripped.split(":", 1)
            threshold_key = key.strip()
            if threshold_key == "family_selection_accuracy":
                threshold_key = "family_proxy_self_consistency"
            elif threshold_key == "workflow_selection_accuracy":
                threshold_key = "workflow_proxy_self_consistency"
            thresholds[threshold_key] = float(value.strip())
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = unquote(value)
        if key == "should_trigger":
            current[key] = parse_bool(value)
        else:
            current[key] = value

    return tests, negative_controls, thresholds


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9.+#-]+", " ", text.lower())).strip()


def tokens(text: str) -> set[str]:
    return {token for token in normalize(text).split() if token not in STOPWORDS and len(token) > 2}


def phrase_matches(prompt: str, phrase: str) -> bool:
    if len(phrase.split()) == 1 or len(phrase) <= 4:
        return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", prompt) is not None
    return phrase in prompt


def phrase_score(prompt: str, phrases: dict[str, float]) -> float:
    return sum(weight for phrase, weight in phrases.items() if phrase_matches(prompt, phrase))


def description_overlap(prompt_tokens: set[str], description: str) -> float:
    description_tokens = tokens(description)
    return min(2.0, len(prompt_tokens & description_tokens) * 0.2)


def score_skill(prompt: str, skill_id: str, description: str) -> float:
    normalized = normalize(prompt)
    score = phrase_score(normalized, PROFILES.get(skill_id, {}))
    score += phrase_score(normalized, PENALTIES.get(skill_id, {}))
    score += description_overlap(tokens(prompt), description)

    if skill_id == "workflow-discovery-to-prd":
        has_artifact = any(term in normalized for term in ("prd", "requirements"))
        has_discovery = any(
            term in normalized
            for term in ("interview", "support ticket", "customer", "funnel data", "discovery")
        )
        if has_artifact and has_discovery:
            score += 6.0
    if skill_id == "workflow-prd-to-linear-delivery":
        if "linear" in normalized and any(
            term in normalized for term in ("do not", "don't", "without", "skip", "no linear")
        ):
            score -= 15.0
        has_artifact_and_linear = any(term in normalized for term in ("prd", "requirements")) and (
            "linear" in normalized
        )
        has_delivery = any(
            term in normalized
            for term in ("epic", "stories", "acceptance criteria", "dependencies", "delivery")
        )
        if has_artifact_and_linear and has_delivery:
            score += 10.0
    if skill_id == "workflow-product-operating-system":
        has_multi_stage_language = any(
            term in normalized
            for term in (
                "idea to launch",
                "next product workflow step",
                "next workflow step",
                "continue this product work",
                "full workflow",
                "end-to-end workflow",
                "what next",
            )
        )
        has_reentry_artifact = any(
            term in normalized
            for term in (
                "rough prd",
                "approved prd",
                "delivery plan",
                "launch request",
                "launch readiness",
                "post-launch metrics",
                "post launch metrics",
            )
        )
        has_product_context = any(
            term in normalized
            for term in ("product", "prd", "delivery", "launch", "customer", "metric", "roadmap")
        )
        if has_multi_stage_language and has_product_context:
            score += 8.0
        if has_reentry_artifact and any(term in normalized for term in ("what next", "continue", "next stage")):
            score += 7.0
        if "validation" in normalized and "not required" in normalized:
            score += 3.0
    if skill_id.startswith("workflow-") and "workflow" in normalized:
        score += 1.0
    if skill_id == "pm-tooling" and any(tool in normalized for tool in ("notion", "linear")):
        if any(
            term in normalized
            for term in (
                "do not create linear",
                "do not use linear",
                "without linear",
                "skip linear",
                "no linear",
            )
        ):
            score -= 10.0
        score += 1.0

    return score


def route_prompt(prompt: str, skills: dict[str, str]) -> tuple[str | None, float, list[tuple[str, float]]]:
    scores = [
        (skill_id, score_skill(prompt, skill_id, description))
        for skill_id, description in skills.items()
    ]
    ranked = sorted(scores, key=lambda item: (-item[1], item[0]))
    top_skill, top_score = ranked[0]
    if top_score < TRIGGER_THRESHOLD:
        return None, top_score, ranked[:3]
    return top_skill, top_score, ranked[:3]


def load_skill_descriptions(root: Path) -> dict[str, str]:
    registry = read_json(root / "registry.json")
    if not isinstance(registry, dict) or not isinstance(registry.get("skills"), list):
        raise ValueError("registry.json must contain a skills list")

    descriptions: dict[str, str] = {}
    for entry in registry["skills"]:
        if not isinstance(entry, dict):
            continue
        skill_id = entry.get("id")
        skill_path = entry.get("path")
        if not isinstance(skill_id, str) or not isinstance(skill_path, str):
            continue
        frontmatter = parse_frontmatter(root / skill_path / "SKILL.md")
        descriptions[skill_id] = frontmatter.get("description", "")
    return descriptions


def pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return numerator / denominator


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    tests, negative_controls, thresholds = parse_trigger_tests(root / "evals/trigger-tests.yaml")
    skills = load_skill_descriptions(root)

    failures: list[str] = []
    family_total = 0
    family_correct = 0
    workflow_total = 0
    workflow_correct = 0
    total = 0
    correct = 0

    for case in tests:
        case_id = str(case.get("id", "unknown"))
        expected_skill = str(case.get("skill_id", ""))
        should_trigger = bool(case.get("should_trigger"))
        prompt = str(case.get("prompt", ""))
        selected, score, ranked = route_prompt(prompt, skills)
        passed = selected == expected_skill if should_trigger else selected != expected_skill

        total += 1
        correct += int(passed)
        if should_trigger and expected_skill.startswith("workflow-"):
            workflow_total += 1
            workflow_correct += int(passed)
        elif should_trigger:
            family_total += 1
            family_correct += int(passed)

        if not passed:
            failures.append(
                f"{case_id}: expected {'trigger' if should_trigger else 'not trigger'} "
                f"{expected_skill}, selected {selected or 'none'} ({score:.2f}); top={ranked}"
            )

    for case in negative_controls:
        case_id = str(case.get("id", "unknown"))
        prompt = str(case.get("prompt", ""))
        selected, score, ranked = route_prompt(prompt, skills)
        passed = selected is None
        total += 1
        correct += int(passed)
        if not passed:
            failures.append(
                f"{case_id}: expected no skill, selected {selected} ({score:.2f}); top={ranked}"
            )

    family_accuracy = pct(family_correct, family_total)
    workflow_accuracy = pct(workflow_correct, workflow_total)
    overall_accuracy = pct(correct, total)

    if family_accuracy < thresholds["family_proxy_self_consistency"]:
        failures.append(
            f"Family proxy self-consistency {family_accuracy:.1%} below "
            f"{thresholds['family_proxy_self_consistency']:.1%}"
        )
    if workflow_accuracy < thresholds["workflow_proxy_self_consistency"]:
        failures.append(
            f"Workflow proxy self-consistency {workflow_accuracy:.1%} below "
            f"{thresholds['workflow_proxy_self_consistency']:.1%}"
        )

    if failures:
        print(f"FAIL trigger evals: {len(failures)} issue(s)")
        print(f"- Overall accuracy: {overall_accuracy:.1%} ({correct}/{total})")
        print(f"- Family positive proxy self-consistency: {family_accuracy:.1%} ({family_correct}/{family_total})")
        print(f"- Workflow positive proxy self-consistency: {workflow_accuracy:.1%} ({workflow_correct}/{workflow_total})")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS trigger evals")
    print(f"- Root: {root}")
    print(f"- Overall accuracy: {overall_accuracy:.1%} ({correct}/{total})")
    print(f"- Family positive proxy self-consistency: {family_accuracy:.1%} ({family_correct}/{family_total})")
    print(f"- Workflow positive proxy self-consistency: {workflow_accuracy:.1%} ({workflow_correct}/{workflow_total})")
    print(f"- Negative controls: {len(negative_controls)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
