#!/usr/bin/env python3
"""Network-free structural validation for the Tianheng Foundry distribution."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
NAME = "tianheng-foundry"
VERSION = json.loads((ROOT / "distribution.json").read_text())["version"]
SKILLS = {
    "forge-law": {
        "description_boundary": "Do not use for non-Rust repositories",
        "references": {
            "claim-classification.md",
            "recipe-index.md",
            "reaction-proof.md",
            "authority-transition.md",
        },
    },
    "repair-drift": {
        "description_boundary": "Do not use to create a new boundary",
        "references": {
            "reaction-contract.md",
            "repair-polarities.md",
            "law-protection.md",
            "verification.md",
        },
    },
    "amend-law": {
        "description_boundary": "Do not use for new prose-to-law conversion",
        "references": {
            "authority-gate.md",
            "amendment-classification.md",
            "proof-matrix.md",
            "migration-and-projection.md",
        },
    },
    "activate-law": {
        "description_boundary": "Do not use for non-Rust repositories",
        "references": {
            "projection-source.md",
            "task-envelope.md",
            "relevance-routing.md",
            "implementation-handoff.md",
        },
    },
    "review-law": {
        "description_boundary": "Do not use to create or repair law",
        "references": {
            "review-gates.md",
            "evidence-audit.md",
            "minimality-and-overlap.md",
            "verdict-contract.md",
        },
    },
    "shape-capability": {
        "description_boundary": "Do not use when an existing recipe fits",
        "references": {
            "gap-classification.md",
            "observation-contract.md",
            "feasibility-and-risk.md",
            "upstream-handoff.md",
        },
    },
    "manage-baseline": {
        "description_boundary": "Do not use to repair product drift",
        "references": {
            "baseline-contract.md",
            "identity-diff.md",
            "operation-modes.md",
            "verification.md",
        },
    },
}

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

# Every upstream this repository pins, and the two places each pin is written: the
# declaration a reader trusts, and the workflow step that actually fetches it. Nothing
# made the two agree, so a bumped declaration could ship while CI kept validating the
# previous release — the failure mode the compatibility runner cannot see, because it
# only ever inspects the checkout it is handed.
# A skill naming a Tianheng line other than the declared one routes an adopter by a surface this
# repository no longer supports. Nine such lines survived a supported-line move that changed every
# machine-readable declaration, because nothing compared the instructions to it.
SKILL_VERSION_LINE = re.compile(r"`(\d+\.\d+)\.x`")
DECLARED_LINE = re.compile(r">=(\d+\.\d+)\.")

DEPLOYER_REPOSITORY = "tacticaldoll/agent-skill-deployer"
TIANHENG_REPOSITORY = "tacticaldoll/tianheng"
DEPLOYER_PIN = re.compile(
    r'"agent-skill-deployer @ git\+[^"]*?agent-skill-deployer\.git@(v\d+\.\d+\.\d+)"'
)
WORKFLOW_CHECKOUT = re.compile(
    r"repository:\s*(\S+)\s*\n\s*ref:\s*(\S+)\s*\n"
)

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
    "tests/compatibility/consumer/Cargo.toml",
    "tests/compatibility/consumer/src/lib.rs",
    ".github/workflows/validate.yml",
    "tools/th-foundry-cli/pyproject.toml",
    "tools/th-foundry-cli/README.md",
    "tools/th-foundry-cli/th_foundry_cli/cli.py",
    "tools/th-foundry-cli/tests/test_cli.py",
]

for skill_name, contract in SKILLS.items():
    REQUIRED_FILES.extend(
        [
            f"skills/{skill_name}/SKILL.md",
            f"skills/{skill_name}/skill.yaml",
            f"skills/{skill_name}/agents/openai.yaml",
            *[
                f"skills/{skill_name}/references/{reference}"
                for reference in sorted(contract["references"])
            ],
        ]
    )


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
    if compatibility.get("tianheng", {}).get("supported") != ">=0.5.0,<0.6.0":
        fail(failures, "compatibility.json: expected Tianheng 0.5.x support range")
    if compatibility.get("tianheng", {}).get("source_env") != "TIANHENG_SOURCE":
        fail(failures, "compatibility.json: local source input must be TIANHENG_SOURCE")

    declared_line = DECLARED_LINE.match(
        compatibility.get("tianheng", {}).get("supported", "")
    )
    if declared_line:
        expected = declared_line.group(1)
        for markdown in sorted((ROOT / "skills").rglob("*.md")):
            for named in SKILL_VERSION_LINE.findall(markdown.read_text()):
                if named != expected:
                    fail(
                        failures,
                        f"{markdown.relative_to(ROOT)}: names Tianheng `{named}.x` but the "
                        f"declared supported line is `{expected}.x`",
                    )

    for skill_name, contract in SKILLS.items():
        skill_path = ROOT / "skills" / skill_name / "SKILL.md"
        if skill_path.is_file():
            skill = skill_path.read_text()
            if "[TODO" in skill:
                fail(failures, f"skills/{skill_name}/SKILL.md contains TODO placeholders")
            if not skill.startswith(f"---\nname: {skill_name}\n"):
                fail(failures, f"skills/{skill_name}/SKILL.md has invalid frontmatter")
            if contract["description_boundary"] not in skill:
                fail(
                    failures,
                    f"{skill_name} description must contain its negative trigger boundary",
                )
            linked_references = set(re.findall(r"\(references/([^)]+)\)", skill))
            if linked_references != contract["references"]:
                fail(
                    failures,
                    f"{skill_name} must link exactly its declared references",
                )

        skill_yaml = ROOT / "skills" / skill_name / "skill.yaml"
        if skill_yaml.is_file():
            text = skill_yaml.read_text()
            for required in [
                f"name: {skill_name}",
                f"version: {VERSION}",
                "entrypoint: SKILL.md",
            ]:
                if required not in text:
                    fail(failures, f"{skill_name}/skill.yaml missing {required!r}")

            status_match = re.search(r"(?m)^status: (\S+)$", text)
            if not status_match or status_match.group(1) not in {
                "draft",
                "stable",
                "deprecated",
            }:
                fail(
                    failures,
                    f"{skill_name}/skill.yaml missing a valid 'status' "
                    "(draft|stable|deprecated)",
                )

            family_match = re.search(r"(?m)^family: (\S+)$", text)
            if not family_match or family_match.group(1) not in {
                "implementation",
                "analysis",
            }:
                fail(
                    failures,
                    f"{skill_name}/skill.yaml missing a valid 'family' "
                    "(implementation|analysis)",
                )

            description_match = re.search(r"(?m)^description: (.+)$", text)
            if not description_match or not description_match.group(1).strip():
                fail(
                    failures,
                    f"{skill_name}/skill.yaml missing a non-empty 'description'",
                )

            triggers_match = re.search(r"(?ms)^triggers:\n((?:  - .+\n)+)", text)
            if not triggers_match:
                fail(
                    failures,
                    f"{skill_name}/skill.yaml missing a 'triggers' list with at "
                    "least one item",
                )

    if (ROOT / ".gitmodules").exists():
        fail(failures, "git submodules are forbidden")

    for skill_name in SKILLS:
        openai_yaml = ROOT / "skills" / skill_name / "agents" / "openai.yaml"
        if (
            openai_yaml.is_file()
            and "allow_implicit_invocation: true" not in openai_yaml.read_text()
        ):
            fail(failures, f"{skill_name} must explicitly permit implicit invocation")

    scenario_count = len(list((ROOT / "tests" / "scenarios").glob("*.json")))
    if scenario_count < 9:
        fail(failures, f"expected at least 9 scenarios, found {scenario_count}")

    repair_scenario_count = len(
        list((ROOT / "tests" / "repair-scenarios").glob("*.json"))
    )
    if repair_scenario_count < 7:
        fail(
            failures,
            f"expected at least 7 repair scenarios, found {repair_scenario_count}",
        )

    amendment_scenario_count = len(
        list((ROOT / "tests" / "amendment-scenarios").glob("*.json"))
    )
    if amendment_scenario_count < 9:
        fail(
            failures,
            f"expected at least 9 amendment scenarios, found {amendment_scenario_count}",
        )

    activation_scenario_count = len(
        list((ROOT / "tests" / "activation-scenarios").glob("*.json"))
    )
    if activation_scenario_count < 12:
        fail(
            failures,
            f"expected at least 12 activation scenarios, found {activation_scenario_count}",
        )

    review_scenario_count = len(
        list((ROOT / "tests" / "review-scenarios").glob("*.json"))
    )
    if review_scenario_count < 15:
        fail(
            failures,
            f"expected at least 15 review scenarios, found {review_scenario_count}",
        )

    capability_scenario_count = len(
        list((ROOT / "tests" / "capability-scenarios").glob("*.json"))
    )
    if capability_scenario_count < 12:
        fail(
            failures,
            f"expected at least 12 capability scenarios, found {capability_scenario_count}",
        )

    baseline_scenario_count = len(
        list((ROOT / "tests" / "baseline-scenarios").glob("*.json"))
    )
    if baseline_scenario_count < 15:
        fail(
            failures,
            f"expected at least 15 baseline scenarios, found {baseline_scenario_count}",
        )

    workflow_path = ROOT / ".github" / "workflows" / "validate.yml"
    if workflow_path.is_file():
        fetched = dict(
            (repository, ref)
            for repository, ref in WORKFLOW_CHECKOUT.findall(workflow_path.read_text())
        )

        pyproject = ROOT / "tools" / "th-foundry-cli" / "pyproject.toml"
        declared_deployer = None
        if pyproject.is_file():
            match = DEPLOYER_PIN.search(pyproject.read_text())
            if not match:
                fail(
                    failures,
                    "tools/th-foundry-cli/pyproject.toml must pin agent-skill-deployer "
                    "to an exact vX.Y.Z tag",
                )
            else:
                declared_deployer = match.group(1)

        fetched_deployer = fetched.get(DEPLOYER_REPOSITORY)
        if fetched_deployer is None:
            fail(
                failures,
                f"validate.yml must check out {DEPLOYER_REPOSITORY} to exercise the CLI binding",
            )
        elif declared_deployer is not None and fetched_deployer != declared_deployer:
            fail(
                failures,
                f"validate.yml fetches {DEPLOYER_REPOSITORY}@{fetched_deployer} but the CLI "
                f"binding pins {declared_deployer}",
            )

        fetched_tianheng = fetched.get(TIANHENG_REPOSITORY)
        tested = compatibility.get("tianheng", {}).get("tested", [])
        if fetched_tianheng is None:
            fail(
                failures,
                f"validate.yml must check out {TIANHENG_REPOSITORY} for the compatibility gate",
            )
        elif fetched_tianheng.removeprefix("v") not in tested:
            fail(
                failures,
                f"validate.yml fetches {TIANHENG_REPOSITORY}@{fetched_tianheng} but "
                f"compatibility.json declares tested={tested}",
            )

    if failures:
        for message in failures:
            print(f"error: {message}", file=sys.stderr)
        return 1

    print(
        "ok: repository structure, manifests, references, upstream pins, and "
        "compatibility metadata"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
