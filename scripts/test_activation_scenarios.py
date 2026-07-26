#!/usr/bin/env python3
"""Validate activate-law routing and task-local selection scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "activation-scenarios"
REQUIRED_IDS = {
    "non-rust-refusal",
    "ungoverned-rust-refusal",
    "projection-error",
    "unknown-touch-set",
    "route-new-law",
    "route-repair",
    "route-amendment",
    "direct-target",
    "dependency-adjacent",
    "semantic-adjacent",
    "runtime-adjacent",
    "workspace-and-uncovered",
}
TIER_ORDER = ["direct", "dependency", "semantic", "runtime", "workspace", "uncovered"]


def result(verdict: str, tiers: list[str] | None = None) -> dict:
    return {
        "verdict": verdict,
        "selected_tiers": tiers or [],
        "write_workspace": False,
    }


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    request = case["request"]

    if not repository["rust"]:
        return result("STOP_NON_RUST")
    if not repository["tianheng"]:
        return result("STOP_UNGOVERNED")

    route = request["route"]
    if route == "new-law":
        return result("ROUTE_FORGE")
    if route == "repair":
        return result("ROUTE_REPAIR")
    if route == "amendment":
        return result("ROUTE_AMENDMENT")

    if not repository["projection_ok"]:
        return result("STOP_PROJECTION_ERROR")
    if not request["touch_set_known"]:
        return result("CLARIFY_TOUCH_SET")

    impacts = request["impacts"]
    active = {
        tier
        for tier in ["direct", "dependency", "semantic", "runtime", "workspace"]
        if impacts[tier]
    }
    if not impacts["direct"]:
        active.add("uncovered")

    tiers = [tier for tier in TIER_ORDER if tier in active]
    return result("ACTIVATE", tiers)


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

    print(f"ok: {len(seen)} law activation scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
