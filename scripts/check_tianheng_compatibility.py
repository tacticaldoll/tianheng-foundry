#!/usr/bin/env python3
"""Compile representative declarations against an injected local Tianheng checkout."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
METADATA = json.loads((ROOT / "compatibility.json").read_text())


RUNNER_BIN = "foundry-compatibility-runner"

# The fields Foundry's skills read out of `list --format json`. activate-law selects
# on them, amend-law snapshots them, and repair-drift reads a reason back from them.
PROJECTION_FIELDS = {"kind", "target", "rule", "severity", "reason"}

# The exit classes the skills route on: 0 clean, 1 enforced violation, 2 never proof.
# Each case names the declaration that produces it, so the contract is exercised rather
# than described.
REACTION_CASES = [
    ("clean", ["check", "--manifest-path", "{manifest}", "--format", "json"], 0, "clean"),
    (
        "violating",
        ["check", "--manifest-path", "{manifest}", "--format", "json"],
        1,
        "violations",
    ),
    (
        "representative",
        ["check", "--manifest-path", "{manifest}", "--format", "json"],
        2,
        "constitution_error",
    ),
]


def run_fixture(
    runner: Path, arguments: list[str], environment: dict[str, str], mode: str
) -> subprocess.CompletedProcess:
    """Invoke the fixture runner under one declared constitution."""
    env = dict(environment)
    env["FOUNDRY_FIXTURE_CONSTITUTION"] = mode
    return subprocess.run(
        [str(runner), *arguments], env=env, check=False, capture_output=True, text=True
    )


def check_runner_contract(
    runner: Path, work: Path, environment: dict[str, str]
) -> list[str]:
    """Exercise the invocation surface the skills tell an agent to drive.

    The fixture proves the vocabulary compiles. It said nothing about the runner an
    agent actually calls, so a renamed subcommand, a dropped `--format json`, a moved
    projection field, or a changed exit class would have reached the skills as stale
    instructions with nothing failing first.
    """
    failures: list[str] = []
    manifest = str(work / "Cargo.toml")

    listing = run_fixture(runner, ["list", "--format", "json"], environment, "representative")
    if listing.returncode != 0:
        failures.append(
            f"`list --format json` exited {listing.returncode}, expected 0"
        )
    else:
        try:
            document = json.loads(listing.stdout)
        except json.JSONDecodeError as error:
            failures.append(f"`list --format json` did not emit JSON: {error}")
        else:
            entries = [
                entry
                for value in document.values()
                if isinstance(value, list)
                for entry in value
                if isinstance(entry, dict)
            ]
            if not entries:
                failures.append("`list --format json` projected no boundary entries")
            for entry in entries:
                missing = PROJECTION_FIELDS - set(entry)
                if missing:
                    failures.append(
                        f"a projected boundary omits {sorted(missing)}, which the "
                        "skills read from every entry"
                    )
                    break

    for mode, template, expected_exit, expected_outcome in REACTION_CASES:
        arguments = [part.format(manifest=manifest) for part in template]
        result = run_fixture(runner, arguments, environment, mode)
        if result.returncode != expected_exit:
            failures.append(
                f"the {mode} declaration exited {result.returncode}, expected exit "
                f"class {expected_exit}"
            )
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            failures.append(f"the {mode} declaration did not emit a JSON report: {error}")
            continue
        if report.get("outcome") != expected_outcome:
            failures.append(
                f"the {mode} declaration reported outcome {report.get('outcome')!r}, "
                f"expected {expected_outcome!r}"
            )
        if "violations" not in report:
            failures.append(f"the {mode} report omits 'violations'")

    usage = run_fixture(runner, ["--not-a-real-flag"], environment, "representative")
    if usage.returncode != 2:
        failures.append(
            f"a usage error exited {usage.returncode}, expected exit class 2"
        )

    return failures


def resolved_family_roots(
    work: Path, patches: list[str], environment: dict[str, str]
) -> dict[str, Path] | None:
    """Where Cargo actually resolved each Tianheng family crate.

    `--config patch.crates-io.<crate>.path` is advisory. When the patched version does
    not satisfy the fixture's requirement, Cargo drops the patch, resolves the registry
    copy instead, and reports that as a warning on a successful exit. Reading the
    resolved graph turns the silent substitution into an observable fact.
    """
    command = [
        "cargo",
        "metadata",
        "--format-version",
        "1",
        "--manifest-path",
        str(work / "Cargo.toml"),
        "--offline",
        *patches,
    ]
    result = subprocess.run(
        command, env=environment, check=False, capture_output=True, text=True
    )
    if result.returncode:
        sys.stderr.write(result.stderr)
        return None
    family = set(METADATA["crate_family"])
    return {
        package["name"]: Path(package["manifest_path"]).parent
        for package in json.loads(result.stdout)["packages"]
        if package["name"] in family
    }


def substituted_crates(source: Path, resolved: dict[str, Path]) -> list[str]:
    """Every family crate the fixture did not take from the supplied checkout."""
    substitutions: list[str] = []
    for crate in METADATA["crate_family"]:
        root = resolved.get(crate)
        if root is None:
            substitutions.append(f"{crate}: absent from the resolved graph")
        elif not root.is_relative_to(source):
            substitutions.append(f"{crate}: resolved to {root}, not under {source}")
    return substitutions


def main() -> int:
    variable = METADATA["tianheng"]["source_env"]
    value = os.environ.get(variable)
    if not value:
        print(f"error: set {variable} to a local Tianheng checkout", file=sys.stderr)
        return 2

    source = Path(value).expanduser().resolve()
    if not (source / "Cargo.toml").is_file():
        print(f"error: {variable} does not name a Tianheng workspace: {source}", file=sys.stderr)
        return 2

    patches: list[str] = []
    for crate in METADATA["crate_family"]:
        crate_path = source / "crates" / crate
        if not (crate_path / "Cargo.toml").is_file():
            print(f"error: missing Tianheng crate source: {crate_path}", file=sys.stderr)
            return 2
        patches.extend(
            ["--config", f'patch.crates-io.{crate}.path="{crate_path.as_posix()}"']
        )

    with tempfile.TemporaryDirectory(prefix="tianheng-foundry-compat-") as temporary:
        work = Path(temporary) / "consumer"
        shutil.copytree(ROOT / "tests" / "compatibility" / "consumer", work)
        environment = os.environ.copy()
        environment["CARGO_TARGET_DIR"] = str(Path(temporary) / "target")

        resolved = resolved_family_roots(work, patches, environment)
        if resolved is None:
            return 1
        substitutions = substituted_crates(source, resolved)
        if substitutions:
            print(
                f"error: the fixture did not compile against {source}; Cargo dropped "
                "the injected patch and resolved elsewhere:",
                file=sys.stderr,
            )
            for substitution in substitutions:
                print(f"  {substitution}", file=sys.stderr)
            print(
                "hint: the fixture's declared Tianheng requirement must admit the "
                "supplied checkout's version; declared range, fixture, and vocabulary "
                "move together.",
                file=sys.stderr,
            )
            return 1

        command = [
            "cargo",
            "build",
            "--manifest-path",
            str(work / "Cargo.toml"),
            "--offline",
            *patches,
        ]
        result = subprocess.run(command, env=environment, check=False)
        if result.returncode:
            return result.returncode

        runner = Path(environment["CARGO_TARGET_DIR"]) / "debug" / RUNNER_BIN
        failures = check_runner_contract(runner, work, environment)
        if failures:
            print(
                f"error: the {source} runner does not honour the invocation contract "
                "Foundry's skills instruct an agent to drive:",
                file=sys.stderr,
            )
            for failure in failures:
                print(f"  {failure}", file=sys.stderr)
            return 1

    print(
        "ok: representative Tianheng Foundry vocabulary compiles, and the runner "
        f"contract holds, against {source}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
