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


def resolved_family_roots(
    work: Path, patches: list[str], environment: dict[str, str]
) -> dict[str, Path] | None:
    """Where Cargo actually resolved each Tianheng family crate for this check.

    `--config patch.crates-io.<crate>.path` is advisory: when the patched version does not
    satisfy the fixture's requirement, Cargo drops the patch, resolves the registry copy
    instead, and reports it as a warning on a successful exit. Reading the resolved graph
    turns that silent substitution into an observable fact.
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
    graph = json.loads(result.stdout)
    family = set(METADATA["crate_family"])
    return {
        package["name"]: Path(package["manifest_path"]).parent
        for package in graph["packages"]
        if package["name"] in family
    }


def report_substitutions(source: Path, resolved: dict[str, Path]) -> list[str]:
    """Every family crate the fixture did not take from the supplied checkout."""
    failures: list[str] = []
    for crate in METADATA["crate_family"]:
        root = resolved.get(crate)
        if root is None:
            failures.append(f"{crate}: absent from the resolved graph")
        elif not root.is_relative_to(source):
            failures.append(f"{crate}: resolved to {root}, not under {source}")
    return failures


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
        substitutions = report_substitutions(source, resolved)
        if substitutions:
            print(
                f"error: the fixture did not compile against {source}; Cargo dropped the "
                "injected patch and resolved elsewhere:",
                file=sys.stderr,
            )
            for substitution in substitutions:
                print(f"  {substitution}", file=sys.stderr)
            print(
                "hint: the fixture's declared Tianheng requirement must admit the supplied "
                "checkout's version; declared range, fixture, and vocabulary move together.",
                file=sys.stderr,
            )
            return 1

        command = [
            "cargo",
            "check",
            "--manifest-path",
            str(work / "Cargo.toml"),
            "--offline",
            *patches,
        ]
        result = subprocess.run(command, env=environment, check=False)
        if result.returncode:
            return result.returncode

    print(
        "ok: representative Tianheng Foundry vocabulary compiles against "
        f"{source}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
