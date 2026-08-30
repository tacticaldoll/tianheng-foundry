#!/usr/bin/env python3
"""Validate capability-pressure classification and ownership scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "capability-scenarios"
REQUIRED_IDS = {
    "non-rust-refusal",
    "unqualified-rust-refusal",
    "unsupported-version",
    "missing-authority",
    "non-structural-claim",
    "cross-language-claim",
    "existing-recipe",
    "missing-observation-source",
    "infeasible-observation",
    "static-pressure",
    "semantic-pressure",
    "runtime-pressure",
    "adopter-house-rule",
    "adopter-rule-without-source",
}
DIMENSIONS = {
    "cargo_metadata": "static",
    "source_tokens": "static",
    "syn_ast": "semantic",
    "runtime_probe": "runtime",
}


def result(verdict: str, candidate: bool = False, owner: str = "none") -> dict:
    return {
        "verdict": verdict,
        "pressure_candidate": candidate,
        "observation_owner": owner,
        "write_upstream": False,
    }


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    claim = case["claim"]

    if not repository["rust"]:
        return result("STOP_NON_RUST")
    if not repository["tianheng_or_adoption"]:
        return result("STOP_UNQUALIFIED")
    if not repository["supported_version"]:
        return result("COMPATIBILITY_REQUIRED")
    if not claim["authority"]:
        return result("STOP_AUTHORITY_REQUIRED")
    if not claim["structural"]:
        return result("DOCUMENT_ONLY")
    if repository["cross_language"]:
        return result("CROSS_LANGUAGE")
    if claim["existing_recipe"]:
        return result("ROUTE_FORGE")

    source = claim["observation_source"]
    if source is None:
        return result("DEFER_OBSERVATION")
    if not claim["feasible"]:
        return result("DEFER_FEASIBILITY")
    if source not in DIMENSIONS:
        return result("DEFER_OBSERVATION")

    # The fork sits *after* the source and feasibility gates, never beside them: an
    # adopter-owned observation is differently owned, not more cheaply earned. A house rule
    # with no named source defers exactly as a general capability with none does.
    if not claim["general_capability"]:
        return result("ADOPTER_OBSERVER", True, "adopter")

    return result("SHAPE_CAPABILITY", True, DIMENSIONS[source])


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

    print(f"ok: {len(seen)} capability pressure scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
