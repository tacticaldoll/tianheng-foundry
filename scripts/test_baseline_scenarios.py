#!/usr/bin/env python3
"""Validate baseline authority, identity-diff, and operation routing scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "baseline-scenarios"
REQUIRED_IDS = {
    "unqualified-workspace",
    "unsupported-version",
    "implicit-operation",
    "unsupported-format",
    "reaction-error",
    "authorized-adoption",
    "unauthorized-adoption",
    "refresh-retained-only",
    "refresh-new-drift-refusal",
    "authorized-refresh-acquisition",
    "prune-stale",
    "prune-with-new-drift",
    "retire-clean",
    "retire-with-debt",
    "authorized-annotation",
}


def result(
    verdict: str,
    *,
    write_baseline: bool = False,
    delete_baseline: bool = False,
    edit_annotations: bool = False,
) -> dict:
    return {
        "verdict": verdict,
        "write_baseline": write_baseline,
        "delete_baseline": delete_baseline,
        "edit_annotations": edit_annotations,
        "edit_law": False,
    }


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    request = case["request"]

    if not repository["qualified"]:
        return result("STOP_UNQUALIFIED")
    if not repository["supported_version"]:
        return result("COMPATIBILITY_REQUIRED")
    if not request["explicit"]:
        return result("AUTHORITY_REQUIRED")
    if repository["baseline_format"] == "unsupported":
        return result("UNSUPPORTED_FORMAT")
    if not repository["reaction_valid"]:
        return result("REACTION_ERROR")

    previous = set(repository["previous_identities"])
    current = set(repository["current_identities"])
    added = current - previous
    stale = previous - current
    operation = request["operation"]

    if operation == "adopt":
        if previous:
            return result("WRONG_MODE")
        if added and not request["authorize_added"]:
            return result("NEW_DRIFT")
        return result("ADOPT", write_baseline=True)

    if operation == "refresh":
        if repository["baseline_format"] != "structured":
            return result("WRONG_MODE")
        if added and not request["authorize_added"]:
            return result("NEW_DRIFT")
        return result("REFRESH", write_baseline=True)

    if operation == "prune":
        if added:
            return result("NEW_DRIFT")
        if not stale:
            return result("NO_CHANGE")
        return result("PRUNE", write_baseline=True)

    if operation == "retire":
        if current:
            return result("CURRENT_DEBT_REMAINS")
        return result("RETIRE", delete_baseline=True)

    if operation == "annotate":
        if not request["annotation_authority"]:
            return result("AUTHORITY_REQUIRED")
        return result("ANNOTATE", edit_annotations=True)

    return result("STOP_UNKNOWN_OPERATION")


def main() -> int:
    failures: list[str] = []
    seen: set[str] = set()

    for path in sorted(SCENARIOS.glob("*.json")):
        try:
            case = json.loads(path.read_text())
            case_id = case["id"]
            if case_id in seen:
                failures.append(f"{path}: duplicate scenario id {case_id}")
                continue
            seen.add(case_id)
            actual = evaluate(case)
            if actual != case["expected"]:
                failures.append(
                    f"{path}: expected {case['expected']!r}, evaluated {actual!r}"
                )
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            failures.append(f"{path}: invalid scenario: {error}")

    missing = REQUIRED_IDS - seen
    extra = seen - REQUIRED_IDS
    if missing:
        failures.append(f"missing required scenarios: {', '.join(sorted(missing))}")
    if extra:
        failures.append(f"undeclared scenarios: {', '.join(sorted(extra))}")

    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    print(f"ok: {len(seen)} baseline lifecycle scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
