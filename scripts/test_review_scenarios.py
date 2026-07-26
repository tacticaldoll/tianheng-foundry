#!/usr/bin/env python3
"""Validate review-law gate ordering and verdict scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "review-scenarios"
REQUIRED_IDS = {
    "out-of-scope",
    "missing-authority",
    "silent-amendment",
    "unauthorized-baseline",
    "unobservable-claim",
    "reason-overreach",
    "compatibility-unknown",
    "missing-violating-proof",
    "warn-only-proof",
    "exit-two-proof",
    "missing-precision-proof",
    "redundant-reaction",
    "stale-projection",
    "complete-formation",
    "complete-amendment",
}


def result(verdict: str, finding: str) -> dict:
    return {
        "verdict": verdict,
        "blocking_finding": finding,
        "acceptance_authority": "HUMAN",
    }


def evaluate(case: dict) -> dict:
    candidate = case["candidate"]

    if not candidate["law_candidate"]:
        return result("OUT_OF_SCOPE", "NONE")
    if not candidate["authority"]:
        return result("REJECT", "AUTHORITY")
    if candidate["existing_law_change"] and not candidate["explicit_amendment"]:
        return result("REJECT", "SILENT_AMENDMENT")
    if candidate["baseline_change"] and not candidate["baseline_authority"]:
        return result("REJECT", "BASELINE_AUTHORITY")
    if not candidate["observable"]:
        return result("REJECT", "UNOBSERVABLE")
    if not candidate["reason_bounded"]:
        return result("REJECT", "REASON_OVERREACH")
    if not candidate["compatibility_evidence"]:
        return result("REVISE", "COMPATIBILITY")

    proof = candidate["violating_proof"]
    if proof == "missing":
        return result("REVISE", "MISSING_VIOLATING_PROOF")
    if proof == "warn":
        return result("REVISE", "WARN_IS_NOT_ENFORCEMENT")
    if proof == "exit2":
        return result("REVISE", "INVALID_REACTION")
    if proof != "enforced":
        return result("REVISE", "UNKNOWN_PROOF")

    if not candidate["clean_precision"]:
        return result("REVISE", "MISSING_PRECISION_PROOF")
    if candidate["redundant"]:
        return result("REVISE", "REDUNDANT_REACTION")
    if not candidate["projection_fresh"]:
        return result("REVISE", "STALE_PROJECTION")

    return result("ACCEPT_CANDIDATE", "NONE")


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

    print(f"ok: {len(seen)} adversarial law review scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
