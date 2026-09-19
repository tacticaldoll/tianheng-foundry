#!/usr/bin/env python3
"""Validate amend-law authority and proof routing against checked-in scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "amendment-scenarios"
REQUIRED_IDS = {
    "implicit-amendment-refusal",
    "new-boundary-routing",
    "explicit-tighten",
    "explicit-loosen",
    "explicit-removal",
    "observable-reason-correction",
    "reason-overreach",
    "unsupported-version",
    "conflicting-authority",
}
PROOF_PROFILES = {
    "tighten": "CLEAN_TO_ENFORCED",
    "loosen": "ENFORCED_TO_CLEAN_WITH_RETAINED_EDGE",
    "retarget": "OLD_AND_NEW_TARGET",
    "reason": "REACTION_STABLE_PROJECTION_CHANGED",
    "remove": "ENFORCED_TO_CLEAN_WITH_UNRELATED_CONTROL",
}


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    request = case["request"]

    if not repository["existing_boundary"]:
        return {
            "verdict": "ROUTE_FORGE",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }
    if not request["explicit_amendment"]:
        return {
            "verdict": "STOP_AUTHORITY_REQUIRED",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }
    if not repository["supported_version"]:
        return {
            "verdict": "STOP_COMPATIBILITY_REQUIRED",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }
    if request["authority_conflict"]:
        return {
            "verdict": "STOP_CONFLICTING_AUTHORITY",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }
    if not request["observable"]:
        return {
            "verdict": "STOP_CAPABILITY_PRESSURE",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }

    amendment_class = request["class"]
    if amendment_class not in PROOF_PROFILES:
        return {
            "verdict": "STOP_UNCLASSIFIED",
            "edit_law_candidate": False,
            "proof_profile": "NONE",
        }

    return {
        "verdict": "AMEND_CANDIDATE",
        "edit_law_candidate": True,
        "proof_profile": PROOF_PROFILES[amendment_class],
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

    print(f"ok: {len(seen)} amendment authority and proof scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
