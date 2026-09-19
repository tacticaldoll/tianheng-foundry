"""Bind the generic deployment engine to the Tianheng Foundry workspace policy.

Unlike Fornax's own CLI, this binding does not fix a `source_provider`. Fornax requires
a tagged, pushed release before any deploy (a deliberate formal-release-only policy);
Tianheng Foundry has not cut a tagged release yet, so `th-foundry` deploys from a local
checkout instead (via `--source`, a configured default, or the current directory). Native
plugin hosts still require a clean working tree and a valid remote origin URL
(`Source.require_formal_checkout`), just not a matching tag. Revisit this choice once the
project starts cutting tagged releases.
"""

from __future__ import annotations

import json
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

from agent_skill_deployer.cli import main as engine_main  # noqa: E402
from agent_skill_deployer.core import DistributionPolicy  # noqa: E402


def workspace_version() -> str:
    try:
        return version("th-foundry-cli")
    except PackageNotFoundError:
        pass
    manifest = WORKSPACE_ROOT / "distribution.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    manifest_version = data.get("version")
    if not isinstance(manifest_version, str) or not manifest_version:
        raise RuntimeError(f"workspace version is missing from {manifest}")
    return manifest_version


FOUNDRY_POLICY = DistributionPolicy(
    identity="tianheng-foundry",
    prefix="tianheng-foundry-",
    provenance_file=".tianheng-foundry-install.json",
    display_name="Tianheng Foundry",
    marketplace="tianheng-foundry",
    plugin="tianheng-foundry",
    validation_commands=(
        ("python3", "scripts/validate_skills.py"),
        ("python3", "scripts/test_scenarios.py"),
        ("python3", "scripts/test_repair_scenarios.py"),
        ("python3", "scripts/test_amendment_scenarios.py"),
        ("python3", "scripts/test_activation_scenarios.py"),
        ("python3", "scripts/test_review_scenarios.py"),
        ("python3", "scripts/test_capability_scenarios.py"),
        ("python3", "scripts/test_baseline_scenarios.py"),
    ),
)


def main(argv: list[str] | None = None) -> int:
    return engine_main(
        argv,
        program="th-foundry",
        version=workspace_version(),
        distribution_policy=FOUNDRY_POLICY,
        source_provider=None,
    )
