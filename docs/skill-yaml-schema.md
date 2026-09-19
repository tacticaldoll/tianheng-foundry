# Skill Metadata Schema

`skills/<name>/skill.yaml` is portable collection metadata. It complements, but does not replace,
the host-readable frontmatter in `SKILL.md`.

```yaml
name: lowercase-kebab-case
version: semver
status: draft | stable | deprecated
family: implementation | analysis
description: one-line trigger and outcome
triggers:
  - concrete invocation condition
entrypoint: SKILL.md
resources:
  references: references/
compatibility:
  - host-identifier
```

`name`, `version`, `status`, `family`, `description`, `triggers`, and `entrypoint` are required.
Resource and compatibility entries must correspond to checked-in paths and declared host
packaging. The skill version advances with any behavioral contract change.
