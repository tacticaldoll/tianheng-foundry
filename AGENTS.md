# AGENTS.md - Tianheng Foundry

Read `PROJECT.md` before changing this repository, then the relevant `openspec/specs/*`, then the
skill or validation code being changed.

## Workflow

Capability changes follow OpenSpec: propose, apply, sync. Do not implement a capability before its
proposal, design, delta spec, and tasks are ready.

Keep skills portable and host-neutral. Host-specific manifests belong at the repository root;
host-specific instructions do not belong inside `SKILL.md`.

## Skill Discipline

- A skill description names both its positive trigger and its negative boundary.
- `SKILL.md` contains only the core workflow. Detailed Tianheng concepts and recipe selection live
  in directly linked `references/`.
- Do not duplicate the full Tianheng cookbook or specifications.
- A writing workflow must run its structural eligibility gate before editing.
- A generated boundary is a candidate, never an accepted law.
- Do not invent project policy, widen a reason beyond the observable perimeter, or weaken an
  accepted boundary to pass.
- Do not create a skill, reference layer, or shared abstraction before a second real consumer
  demonstrates the need.

## Verification

Before reporting work complete, run:

```bash
python3 scripts/validate_repository.py
python3 scripts/run_scenarios.py
python3 /home/tnaic/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/forge-law
python3 /home/tnaic/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
openspec validate --all
```

Tests must remain network-free. Compatibility fixtures validate declared public vocabulary and
workflow decisions without downloading Tianheng or embedding another repository.

## Git

Use Conventional Commits with a concise body explaining the preserved contract. Do not add AI
attribution. Do not use git submodules.
