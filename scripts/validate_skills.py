#!/usr/bin/env python3
"""Network-free structural validation for the Tianheng Foundry distribution."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tomllib


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
    "retire-covered-prose": {
        "description_boundary": "Do not use to delete comments as a style mandate",
        "references": {
            "coverage-criterion.md",
            "perimeter-source.md",
            "routing-dispositions.md",
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
    "tests/compatibility/consumer/src/main.rs",
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

    # Every host manifest distributes the whole skills/ directory, so a directory
    # present there but absent from SKILLS would ship to every host unvalidated.
    # The reverse direction is already held by the REQUIRED_FILES sweep above.
    present_skills = {
        path.name
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    for undeclared in sorted(present_skills - set(SKILLS)):
        fail(
            failures,
            f"skills/{undeclared} ships to every host but declares no contract in "
            "validate_skills.py",
        )

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

    # compatibility.json is the single source of the supported Tianheng line, the
    # way distribution.json is for the release version. Nothing here asserts a
    # literal version: it checks the declaration is well formed, then that every
    # surface deriving from it still agrees.
    tianheng = parsed.get("compatibility.json", {}).get("tianheng", {})
    if tianheng.get("source_env") != "TIANHENG_SOURCE":
        fail(failures, "compatibility.json: local source input must be TIANHENG_SOURCE")

    supported = tianheng.get("supported", "")
    tested = tianheng.get("tested", [])
    representative = tianheng.get("representative", "")

    if not re.fullmatch(r">=\d+\.\d+\.\d+,<\d+\.\d+\.\d+", supported):
        fail(
            failures,
            "compatibility.json: 'supported' must be a '>=X.Y.Z,<A.B.C' range",
        )
    if not tested:
        fail(failures, "compatibility.json: 'tested' must name at least one version")
    elif representative not in tested:
        fail(
            failures,
            f"compatibility.json: representative {representative!r} is not in 'tested'",
        )
    if not tianheng.get("repository"):
        fail(failures, "compatibility.json: 'repository' must name the upstream repo")
    if tianheng.get("tag_format", "").count("{version}") != 1:
        fail(
            failures,
            "compatibility.json: 'tag_format' must contain exactly one {version}",
        )

    # recipe_vocabulary is the public surface this collection routes to. Both ends
    # are held: the fixture must exercise every declared name, so an upstream
    # rename breaks the build rather than the routing table; and the routing table
    # may not name a recipe the declaration has not put under that proof.
    vocabulary = parsed.get("compatibility.json", {}).get("recipe_vocabulary", [])
    if not vocabulary:
        fail(failures, "compatibility.json: 'recipe_vocabulary' must not be empty")

    fixture_source = ROOT / "tests" / "compatibility" / "consumer" / "src" / "lib.rs"
    if fixture_source.is_file():
        fixture_text = fixture_source.read_text()
        for name in vocabulary:
            if not re.search(rf"\b{re.escape(name)}\b", fixture_text):
                fail(
                    failures,
                    f"compatibility.json declares {name!r} but the compatibility "
                    "fixture never uses it, so nothing proves it still exists",
                )

    recipe_index = ROOT / "skills" / "forge-law" / "references" / "recipe-index.md"
    if recipe_index.is_file():
        routed = set(
            re.findall(r"\b[A-Z][A-Za-z]*(?:Boundary|Pure)\b", recipe_index.read_text())
        )
        for name in sorted(routed - set(vocabulary)):
            fail(
                failures,
                f"recipe-index.md routes to {name!r}, which compatibility.json does "
                "not declare and the fixture therefore does not prove",
            )

    # The compatibility gate can only compile the injected checkout when the
    # fixture's requirement admits it, so the fixture tracks the representative.
    fixture = ROOT / "tests" / "compatibility" / "consumer" / "Cargo.toml"
    if fixture.is_file() and representative:
        requirement = f'tianheng = "={representative}"'
        if requirement not in fixture.read_text():
            fail(
                failures,
                f"tests/compatibility/consumer/Cargo.toml must require {requirement!r} "
                "so the declared representative is what actually compiles",
            )

    # CI resolves the upstream checkout from the declaration rather than a pin.
    workflow = ROOT / ".github" / "workflows" / "validate.yml"
    if workflow.is_file() and re.search(r"(?m)^\s*ref:\s*v?\d+\.\d+\.\d+\s*$", workflow.read_text()):
        fail(
            failures,
            ".github/workflows/validate.yml pins a literal upstream ref; resolve it "
            "from compatibility.json instead",
        )

    # The version is written once in the declaration and quoted once in the
    # canonical compatibility doc. No other prose restates it.
    canonical_doc = ROOT / "docs" / "tianheng-compatibility.md"
    if canonical_doc.is_file() and supported and representative:
        canonical_text = canonical_doc.read_text()
        for quoted in [supported, representative]:
            if quoted not in canonical_text:
                fail(
                    failures,
                    f"docs/tianheng-compatibility.md must quote {quoted!r} from "
                    "compatibility.json",
                )

    for relative in ["README.md", "PROJECT.md"]:
        path = ROOT / relative
        if path.is_file() and supported and supported in path.read_text():
            fail(
                failures,
                f"{relative} restates the supported Tianheng range; point at "
                "compatibility.json or docs/tianheng-compatibility.md instead",
            )

    for skill_doc in sorted((ROOT / "skills").rglob("*.md")):
        if re.search(r"Tianheng\s+`?\d+\.\d+", skill_doc.read_text()):
            fail(
                failures,
                f"{skill_doc.relative_to(ROOT)} hardcodes a Tianheng line; refer to "
                "the declared supported line instead",
            )

    # The advertised license must be the one actually shipped, in every surface a
    # consumer reads before depending on the collection.
    license_path = ROOT / "LICENSE"
    if license_path.is_file() and not license_path.read_text().startswith("MIT License"):
        fail(failures, "LICENSE: expected the MIT License text")

    for relative in [
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
    ]:
        if parsed.get(relative, {}).get("license") != "MIT":
            fail(
                failures,
                f"{relative}: license must be 'MIT' to match the shipped LICENSE",
            )

    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        section = re.search(
            r"(?ms)^## License\n+(.+?)(?=\n## |\Z)", readme_path.read_text()
        )
        if not section or section.group(1).strip() != "MIT.":
            fail(
                failures,
                "README.md: the License section must state 'MIT.' because MIT is the "
                "only license this repository ships",
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

    # The CLI binding claims to derive its version from distribution.json rather
    # than carrying its own. Nothing checked that the derivation still resolves, so
    # the single release-version source could have quietly stopped covering it.
    cli_manifest = ROOT / "tools" / "th-foundry-cli" / "pyproject.toml"
    if cli_manifest.is_file():
        cli = tomllib.loads(cli_manifest.read_text())
        version_source = cli.get("tool", {}).get("hatch", {}).get("version", {})
        declared_path = version_source.get("path", "")
        if (cli_manifest.parent / declared_path).resolve() != (
            ROOT / "distribution.json"
        ):
            fail(
                failures,
                "tools/th-foundry-cli/pyproject.toml must take its version from "
                "distribution.json, the single release-version source",
            )
        else:
            pattern = version_source.get("pattern", "")
            match = re.search(pattern, (ROOT / "distribution.json").read_text())
            if not match or match.group("version") != VERSION:
                fail(
                    failures,
                    "tools/th-foundry-cli/pyproject.toml: its version pattern no longer "
                    f"resolves distribution.json to {VERSION!r}",
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
    if scenario_count < 10:
        fail(failures, f"expected at least 10 scenarios, found {scenario_count}")

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

    retirement_scenario_count = len(
        list((ROOT / "tests" / "retirement-scenarios").glob("*.json"))
    )
    if retirement_scenario_count < 13:
        fail(
            failures,
            f"expected at least 13 retirement scenarios, found {retirement_scenario_count}",
        )

    if failures:
        for message in failures:
            print(f"error: {message}", file=sys.stderr)
        return 1

    print("ok: repository structure, manifests, references, and compatibility metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
