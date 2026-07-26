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
        shutil.copytree(ROOT / "compatibility" / "consumer", work)
        environment = os.environ.copy()
        environment["CARGO_TARGET_DIR"] = str(Path(temporary) / "target")
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
