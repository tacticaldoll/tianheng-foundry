# AGENTS.md - Tianheng Foundry

Working agreement for humans and agents authoring this skill collection. Read `PROJECT.md` first,
then this file, then the skill or validation surface being changed.

## Core Principles

- Foundry generates candidate law from declared intent; it never invents project policy.
- Rust and Tianheng eligibility are structural gates, not assumptions.
- No observable claim becomes code without a named observation source, target, and rule.
- Generated law remains a candidate until human review accepts it.
- Never weaken accepted law to make a check pass.
- Keep Tianheng, Fornax, and Foundry independent. Do not add git submodules or vendor another repo.
- Prefer one complete skill over several thin workflow fragments.

## Skill Layout

Each skill lives under `skills/<name>/`:

```text
skills/<name>/
├── SKILL.md
├── skill.yaml
├── agents/openai.yaml
└── references/
```

`SKILL.md` owns trigger boundaries, control flow, stop conditions, and output contract. Put detailed
classification tables, recipe routing, and proof criteria in directly linked `references/`.
Host-specific manifests stay outside the core instructions unless a host requires a local adapter.

Do not add shared templates, maps, or abstractions until a second real consumer demonstrates the
shared shape.

## Authoring Rules

- Write descriptions as `Use when ...` and name the negative boundary.
- Make implicit triggers precise enough to avoid generic Rust work.
- State every write boundary before the first editing step.
- Separate authority evidence from architectural inference.
- Use forward voice for generated `because(...)` reasons.
- Keep each reason inside the perimeter the proposed reaction actually observes.
- Require one violating proof and one clean precision proof.
- Treat projection freshness as generated-output verification, not prose maintenance.
- Decline or narrow unobservable claims; never simulate enforcement with stronger wording.
- Route changes to accepted law through an explicit amendment path.

## Language And Naming

Repository control language is English. Examples may preserve adopter terminology when fidelity
requires it.

Skill names are lowercase kebab-case verbs with a concrete object. A name must describe a distinct
agent transaction, not a theme. References are lowercase kebab-case nouns. Scenario file names
describe the policy case they prove.

Use Tianheng public vocabulary exactly as declared for the supported version. Do not rename public
types for stylistic consistency.

## Inputs And Outputs

A writing skill must declare:

- positive and negative triggers;
- evidence accepted as project intent;
- structural eligibility checks;
- files it may inspect and edit;
- stop and refusal conditions;
- candidate output and proof artifacts;
- the authority transition that remains human-owned.

Outputs should be reviewable diffs and verification results. Do not create hidden state, mutate
generated projections by hand, or report a candidate as accepted law.

## Authoring Lifecycle

1. **Propose.** Name the real trigger, output, observation source, and failure mode.
2. **Draft.** Keep the entrypoint compact and move decision detail into linked references.
3. **Adversarial review.** Test accidental invocation, invented authority, unobservable claims,
   silent amendment, weak proofs, and compatibility drift.
4. **Validate.** Run all local structural, scenario, skill, plugin, and compatibility gates.
5. **Release.** Update versions and compatibility declarations together.
6. **Deprecate.** Preserve a migration path; do not silently repurpose a published skill name.

No OpenSpec ceremony is required for this repository. The durable design decisions live in
`PROJECT.md`, focused docs, tests, and git history.

## Compatibility

`compatibility.json` is the machine-readable Tianheng support declaration. The recipe index carries
only the public vocabulary needed to choose and adapt a boundary; it must not become a fork of
Tianheng's cookbook.

When Tianheng changes:

1. inspect the upstream public API and release contract;
2. update the declared range and representative fixture;
3. verify every referenced recipe and observation limit;
4. run the compatibility fixture against the selected checkout;
5. version the skill and distribution together.

Tests remain network-free. CI may fetch a declared upstream checkout before invoking the offline
compatibility runner.

## Verification

Before reporting work complete, run:

```bash
python3 scripts/validate_skills.py
python3 scripts/test_scenarios.py
python3 scripts/test_repair_scenarios.py
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/forge-law
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" .
TIANHENG_SOURCE=/path/to/tianheng python3 scripts/check_tianheng_compatibility.py
```

Also run `bash -n .githooks/pre-commit` after changing the hook and parse every edited YAML file
with an available YAML parser.

## Review Checklist

- Does the description trigger only for the intended Rust and Tianheng context?
- Does the workflow distinguish prose evidence, candidate code, and accepted law?
- Can every generated claim be observed by the selected Tianheng boundary?
- Do tests prove both reaction and precision?
- Does any copied Tianheng detail exceed the minimum routing knowledge?
- Are all paths, manifests, versions, and host instructions consistent?
- Is a new abstraction justified by more than one real consumer?
- Does a repair workflow prove accepted law and baselines stayed unchanged?

## Git And Repository Hygiene

Use Conventional Commits with a concise body explaining why the change exists and which contract
it preserves. Do not add AI or tool attribution.

Keep generated caches, build outputs, editor state, and local credentials out of git. Do not modify
installed plugin caches directly; update the source plugin, advance its Codex cachebuster with the
plugin-creator helper, then reinstall.

Do not publish, tag, force-push, delete a repository, or change remote visibility without explicit
human approval.
