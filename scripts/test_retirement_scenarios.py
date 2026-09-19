#!/usr/bin/env python3
"""Validate retire-covered-prose coverage findings, retirement, and routing scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "retirement-scenarios"
REQUIRED_IDS = {
    "non-rust-refusal",
    "ungoverned-rust-refusal",
    "projection-error",
    "style-mandate-refusal",
    "fully-covered-retirement",
    "apply-authority-write",
    "claim-broader-than-perimeter",
    "warn-only-coverage-refusal",
    "baselined-coverage-refusal",
    "rustdoc-out-of-corpus",
    "non-structural-comment",
    "uncovered-observable-claim",
    "unobservable-claim",
}
ROUTE_KEYS = ["amend", "forge", "baseline", "capability"]
ROUTE_OF = {
    "WIDER": "amend",
    "TOOTHLESS": "amend",
    "ABSORBED": "baseline",
    "UNGOVERNED": "forge",
    "UNOBSERVABLE": "capability",
}


def result(
    verdict: str,
    retire: list[str] | None = None,
    routes: dict[str, list[str]] | None = None,
    write_workspace: bool = False,
) -> dict:
    routed = routes or {}
    return {
        "verdict": verdict,
        "retire": sorted(retire or []),
        "routes": {key: sorted(routed.get(key, [])) for key in ROUTE_KEYS},
        "write_workspace": write_workspace,
    }


def finding(comment: dict) -> str:
    """Classify one comment. Out-of-corpus prose is retained without a route."""
    if comment["form"] == "rustdoc-public":
        return "KEEP_OUT_OF_CORPUS"
    if comment["claim"] != "structural":
        return "KEEP_OUT_OF_CORPUS"

    perimeter = comment["perimeter"]
    if perimeter == "none":
        return "UNGOVERNED" if comment["observable"] else "UNOBSERVABLE"
    if perimeter == "narrower-than-claim":
        return "WIDER"

    # A matching perimeter still needs teeth. Severity is read before baseline state: raising a
    # `warn` boundary is the repair, and a warn finding is not what a baseline records.
    if comment["severity"] != "enforce":
        return "TOOTHLESS"
    if comment["baselined"]:
        return "ABSORBED"
    return "HELD"


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    request = case["request"]

    if not repository["rust"]:
        return result("STOP_NON_RUST")
    if not repository["tianheng"]:
        return result("STOP_UNGOVERNED")
    if request["kind"] == "style-mandate":
        return result("REFUSE_STYLE_REQUEST")
    if not repository["projection_ok"]:
        return result("STOP_PROJECTION_ERROR")

    retire: list[str] = []
    routes: dict[str, list[str]] = {key: [] for key in ROUTE_KEYS}

    for comment in case["comments"]:
        verdict = finding(comment)
        if verdict == "HELD":
            retire.append(comment["id"])
        elif verdict in ROUTE_OF:
            routes[ROUTE_OF[verdict]].append(comment["id"])

    return result(
        "RETIRE" if retire else "NOTHING_COVERED",
        retire,
        routes,
        write_workspace=bool(retire) and request["kind"] == "apply",
    )


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

    print(f"ok: {len(seen)} prose retirement scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
