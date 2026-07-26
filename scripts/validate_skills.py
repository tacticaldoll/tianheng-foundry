#!/usr/bin/env python3
"""Network-free structural validation for the Tianheng Foundry distribution."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
NAME = "tianheng-foundry"
VERSION = "0.1.0"

JSON_MANIFESTS = [
    "distribution.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "gemini-extension.json",
    "compatibility.json",
]

REQUIRED_FILES = [
    "PROJECT.md",
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "docs/identity.md",
    "docs/law-lifecycle.md",
    "docs/host-packaging.md",
    "docs/skill-yaml-schema.md",
    "docs/tianheng-compatibility.md",
    "skills/forge-law/SKILL.md",
    "skills/forge-law/skill.yaml",
    "skills/forge-law/agents/openai.yaml",
    "skills/forge-law/references/claim-classification.md",
    "skills/forge-law/references/recipe-index.md",
    "skills/forge-law/references/reaction-proof.md",
    "skills/forge-law/references/authority-transition.md",
    "tests/compatibility/consumer/Cargo.toml",
    "tests/compatibility/consumer/src/lib.rs",
]


def fail(failures: list[str], message: str) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    parsed: dict[str, dict] = {}

    for relative in REQUIRED_FILES + JSON_MANIFESTS:
        if not (ROOT / relative).is_file():
            fail(failures, f"missing required file: {relative}")

    for relative in JSON_MANIFESTS:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            parsed[relative] = json.loads(path.read_text())
        except json.JSONDecodeError as error:
            fail(failures, f"{relative}: invalid JSON: {error}")

    for relative in [
        ".claude-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
        "gemini-extension.json",
        "distribution.json",
    ]:
        data = parsed.get(relative, {})
        if data.get("name") != NAME:
            fail(failures, f"{relative}: name must be {NAME!r}")
        if data.get("version") != VERSION:
            fail(failures, f"{relative}: version must be {VERSION!r}")

    codex = parsed.get(".codex-plugin/plugin.json", {})
    if codex.get("name") != NAME:
        fail(failures, f".codex-plugin/plugin.json: name must be {NAME!r}")
    codex_version = codex.get("version", "")
    if codex_version != VERSION and not codex_version.startswith(f"{VERSION}+codex."):
        fail(
            failures,
            ".codex-plugin/plugin.json: version must match the release or use a Codex cachebuster",
        )

    distribution = parsed.get("distribution.json", {})
    if distribution.get("skills_directory") != "skills":
        fail(failures, "distribution.json: skills_directory must be 'skills'")

    if codex.get("skills") != "./skills/":
        fail(failures, ".codex-plugin/plugin.json: skills must be './skills/'")

    cursor = parsed.get(".cursor-plugin/plugin.json", {})
    if cursor.get("skills") != "./skills/":
        fail(failures, ".cursor-plugin/plugin.json: skills must be './skills/'")

    for relative in [
        ".claude-plugin/marketplace.json",
        ".agents/plugins/marketplace.json",
    ]:
        plugins = parsed.get(relative, {}).get("plugins", [])
        if len(plugins) != 1 or plugins[0].get("name") != NAME:
            fail(failures, f"{relative}: expected one {NAME!r} plugin entry")

    compatibility = parsed.get("compatibility.json", {})
    if compatibility.get("tianheng", {}).get("supported") != ">=0.3.0,<0.4.0":
        fail(failures, "compatibility.json: expected Tianheng 0.3.x support range")
    if compatibility.get("tianheng", {}).get("source_env") != "TIANHENG_SOURCE":
        fail(failures, "compatibility.json: local source input must be TIANHENG_SOURCE")

    skill_path = ROOT / "skills/forge-law/SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text()
        if "[TODO" in skill:
            fail(failures, "skills/forge-law/SKILL.md contains TODO placeholders")
        if not skill.startswith("---\nname: forge-law\n"):
            fail(failures, "skills/forge-law/SKILL.md has invalid frontmatter")
        if "Do not use for non-Rust repositories" not in skill:
            fail(failures, "forge-law description must exclude non-Rust repositories")
        for reference in re.findall(r"\(references/([^)]+)\)", skill):
            if not (skill_path.parent / "references" / reference).is_file():
                fail(failures, f"forge-law links missing reference: {reference}")

    skill_yaml = ROOT / "skills/forge-law/skill.yaml"
    if skill_yaml.is_file():
        text = skill_yaml.read_text()
        for required in ["name: forge-law", f"version: {VERSION}", "entrypoint: SKILL.md"]:
            if required not in text:
                fail(failures, f"skill.yaml missing {required!r}")

    if (ROOT / ".gitmodules").exists():
        fail(failures, "git submodules are forbidden")

    openai_yaml = ROOT / "skills/forge-law/agents/openai.yaml"
    if openai_yaml.is_file() and "allow_implicit_invocation: true" not in openai_yaml.read_text():
        fail(failures, "forge-law must explicitly permit implicit invocation")

    scenario_count = len(list((ROOT / "tests" / "scenarios").glob("*.json")))
    if scenario_count < 9:
        fail(failures, f"expected at least 9 scenarios, found {scenario_count}")

    if failures:
        for message in failures:
            print(f"error: {message}", file=sys.stderr)
        return 1

    print("ok: repository structure, manifests, references, and compatibility metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
