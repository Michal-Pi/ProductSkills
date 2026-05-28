#!/usr/bin/env python3
"""Validate ProductSkills scale-pack reliability scaffolding."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALES = ("scale-100", "scale-500", "scale-1000", "scale-5000")
PROMPT_SLOTS = (
    "01-scale-discovery",
    "02-scale-strategy",
    "03-scale-validation",
    "04-scale-docs",
    "05-scale-delivery",
    "06-scale-tooling-safety",
    "07-scale-full-workflow",
    "08-scale-adversarial-edge-cases",
)
RANKING_KEYS = (
    "top_by_frequency",
    "top_by_arr",
    "top_by_strategic_weight",
    "risky_minority",
    "noise_controls",
)
UNLABELED_FORBIDDEN = re.compile(r"\b(?:OPP|NOISE)-[A-Z]+-\d{3}\b|duplicate:|missing:")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_prompt_inputs(errors: list[str]) -> None:
    for prompt in sorted((ROOT / "prompts").glob("0[1-8]-*.md")):
        text = prompt.read_text(encoding="utf-8")
        rel = prompt.relative_to(ROOT)
        if "ground-truth/scale-" in text:
            fail(errors, f"{rel} exposes scale ground truth to runtime prompts")
        if "graders/scale-rubric.md" in text:
            fail(errors, f"{rel} exposes grader rubric to runtime prompts")
        if "corpus/scale-" in text:
            fail(errors, f"{rel} still points to labeled corpus")
        if "corpus-unlabeled/scale-" not in text:
            fail(errors, f"{rel} does not point to unlabeled corpus")
        if "evidence_ledger" not in text:
            fail(errors, f"{rel} does not require large-corpus evidence_ledger handling")


def validate_truth(errors: list[str]) -> None:
    for scale in SCALES:
        path = ROOT / "ground-truth" / scale / "planted-ground-truth.json"
        if not path.exists():
            fail(errors, f"Missing {path.relative_to(ROOT)}")
            continue
        truth = json.loads(path.read_text(encoding="utf-8"))
        if truth.get("ground_truth_version") != "2.0":
            fail(errors, f"{path.relative_to(ROOT)} missing ground_truth_version 2.0")
        ranking = truth.get("ranking_ground_truth")
        if not isinstance(ranking, dict):
            fail(errors, f"{path.relative_to(ROOT)} missing ranking_ground_truth")
            continue
        for key in RANKING_KEYS:
            value = ranking.get(key)
            if not isinstance(value, list) or not value:
                fail(errors, f"{path.relative_to(ROOT)} has empty ranking_ground_truth.{key}")
        if "strategic_weight_by_opportunity" not in truth:
            fail(errors, f"{path.relative_to(ROOT)} missing strategic weights")


def validate_unlabeled_corpus(errors: list[str]) -> None:
    for scale in SCALES:
        scale_dir = ROOT / "corpus-unlabeled" / scale
        if not scale_dir.exists():
            fail(errors, f"Missing {scale_dir.relative_to(ROOT)}")
            continue
        for markdown in scale_dir.glob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            if UNLABELED_FORBIDDEN.search(text):
                fail(errors, f"{markdown.relative_to(ROOT)} exposes planted labels")


def validate_output_slots(errors: list[str]) -> None:
    manifest = ROOT / "results" / "generated-outputs" / "slot-manifest.json"
    if not manifest.exists():
        fail(errors, f"Missing {manifest.relative_to(ROOT)}")
        return
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("required_prompt_slots") != list(PROMPT_SLOTS):
        fail(errors, f"{manifest.relative_to(ROOT)} prompt slots do not match required prompts")
    for slot in PROMPT_SLOTS:
        slot_dir = manifest.parent / slot
        if not slot_dir.exists():
            fail(errors, f"Missing generated output slot {slot_dir.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_prompt_inputs(errors)
    validate_truth(errors)
    validate_unlabeled_corpus(errors)
    validate_output_slots(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS scale pack validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
