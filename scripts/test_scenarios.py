#!/usr/bin/env python3
"""Validate the authority and eligibility policy against checked-in scenarios."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "scenarios"

# compatibility.json is the only place the supported Tianheng line is written
# down. A scenario states which side of that line an adopter sits on, never a
# literal version, so moving the line does not edit the fixtures.
TIANHENG = json.loads((ROOT / "compatibility.json").read_text())["tianheng"]
REPRESENTATIVE = TIANHENG["representative"]
SUPPORTED_PREFIX = REPRESENTATIVE.rsplit(".", 1)[0] + "."
UNSUPPORTED_VERSION = f"{int(REPRESENTATIVE.split('.')[0]) + 1}.0.0"

REQUIRED_IDS = {
    "existing-adoption",
    "explicit-first-adoption",
    "non-rust-refusal",
    "unqualified-rust-refusal",
    "mixed-language-narrowing",
    "subjective-claim-decline",
    "unobservable-claim-decline",
    "accepted-law-amendment-refusal",
    "explicit-amendment",
    "unsupported-tianheng-refusal",
}


def resolve_version(declared: str | None) -> str | None:
    """Turn a scenario's stated side of the supported line into a version."""
    if declared is None:
        return None
    if declared == "supported":
        return REPRESENTATIVE
    if declared == "unsupported":
        return UNSUPPORTED_VERSION
    raise SystemExit(
        f"error: tianheng_version must be null, 'supported', or 'unsupported', "
        f"not {declared!r}"
    )


def evaluate(case: dict) -> dict:
    repository = case["repository"]
    request = case["request"]
    scope = "cargo-workspace-only" if repository["mixed_language"] else "cargo-workspace"

    if not repository["rust"]:
        return {
            "verdict": "STOP_NON_RUST",
            "write_candidate": False,
            "scope": "none",
            "authority": "ProseClaim",
        }

    version = resolve_version(repository["tianheng_version"])
    if version is None and not request["explicit_adoption"]:
        return {
            "verdict": "STOP_UNQUALIFIED",
            "write_candidate": False,
            "scope": scope,
            "authority": "ProseClaim",
        }
    if version is not None and not version.startswith(SUPPORTED_PREFIX):
        return {
            "verdict": "STOP_COMPATIBILITY",
            "write_candidate": False,
            "scope": scope,
            "authority": "ProseClaim",
        }

    if request["accepted_law_change"]:
        verdict = "AMENDMENT_PATH" if request["explicit_amendment"] else "STOP_AMENDMENT_REQUIRED"
        return {
            "verdict": verdict,
            "write_candidate": False,
            "scope": scope,
            "authority": "AcceptedLaw",
        }

    if request["claim_authority"] == "none":
        return {
            "verdict": "DECLINE_NO_AUTHORITY",
            "write_candidate": False,
            "scope": scope,
            "authority": "ProseClaim",
        }

    if request["claim_class"] != "structural":
        return {
            "verdict": "DOCUMENT_ONLY",
            "write_candidate": False,
            "scope": scope,
            "authority": "ProseClaim",
        }

    if not request["observable"]:
        return {
            "verdict": "DECLINE_UNOBSERVABLE",
            "write_candidate": False,
            "scope": scope,
            "authority": "AdmittedIntent",
        }

    return {
        "verdict": "ADMIT",
        "write_candidate": True,
        "scope": scope,
        "authority": "VerifiedCandidate",
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

    print(f"ok: {len(seen)} authority and eligibility scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
