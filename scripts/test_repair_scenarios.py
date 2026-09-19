#!/usr/bin/env python3
"""Validate repair-drift routing against checked-in reaction scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "repair-scenarios"
REQUIRED_IDS = {
    "enforced-deny-breach",
    "enforced-allowlist-gap",
    "constitution-error",
    "warn-only-observation",
    "explicit-advisory-repair",
    "implicit-law-change-refusal",
    "explicit-amendment-routing",
}


def evaluate(case: dict) -> dict:
    reaction = case["reaction"]
    request = case["request"]

    if reaction["exit_code"] == 2:
        return {
            "verdict": "STOP_REACTION_ERROR",
            "edit_product": False,
            "edit_law": False,
        }

    if request["explicit_amendment"]:
        return {
            "verdict": "ROUTE_AMENDMENT",
            "edit_product": False,
            "edit_law": False,
        }

    if request["asks_to_change_law"]:
        return {
            "verdict": "STOP_AMENDMENT_REQUIRED",
            "edit_product": False,
            "edit_law": False,
        }

    violations = reaction["violations"]
    if reaction["exit_code"] == 1:
        if not violations:
            return {
                "verdict": "STOP_MALFORMED_REACTION",
                "edit_product": False,
                "edit_law": False,
            }
        return {
            "verdict": "REPAIR_PRODUCT",
            "edit_product": True,
            "edit_law": False,
        }

    if violations:
        if request["explicit_advisory_repair"]:
            return {
                "verdict": "REPAIR_PRODUCT",
                "edit_product": True,
                "edit_law": False,
            }
        return {
            "verdict": "REPORT_ADVISORY",
            "edit_product": False,
            "edit_law": False,
        }

    return {
        "verdict": "NO_DRIFT",
        "edit_product": False,
        "edit_law": False,
    }


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

    print(f"ok: {len(seen)} repair routing scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
