# Tianheng Foundry - Project

Tianheng Foundry is a portable companion skill collection for people who use, or explicitly intend
to adopt, Tianheng in their own Rust projects.

## Status

Experimental `0.1.x`. The collection currently has one skill, `forge-law`, and supports Tianheng
`>=0.3.0,<0.4.0`.

## Standing Decisions

- **Controlled writing.** Foundry may generate Rust boundary and proof code, but only after its
  eligibility and authority gates pass.
- **Declared intent.** Project prose and direct human instruction may authorize a candidate.
  Repository shape and generic best practice may not.
- **Structural scope.** The initial workflow governs observable Rust architecture. Subjective,
  procedural, and historical claims remain prose.
- **Observation before generation.** Every candidate names a Tianheng observation source, target,
  and rule before code is written.
- **Proof before replacement.** A candidate proves teeth, precision, projection freshness, and
  compatibility before suggesting that source prose be removed or narrowed.
- **Human authority.** Generated code is a `VerifiedCandidate`; only human review promotes it to
  `AcceptedLaw`.
- **No silent amendment.** Existing accepted law is repaired toward its reason. Changing it
  requires an explicit amendment request.
- **Tianheng owns reaction.** Tianheng owns its DSL, observations, projections, evaluator, and
  complete cookbook. Foundry carries only selection and adaptation knowledge.
- **Repository independence.** Tianheng, Fornax, and Foundry release independently. Compatibility
  is declared and tested; no repository is vendored or attached as a git submodule.
- **One skill until evidence.** A new skill requires an independent trigger, output, and failure
  mode. Collection size is not a goal.

## Non-goals

- Supplying architecture policy to an adopter.
- Governing non-Rust portions of a mixed-language repository.
- Replacing Tianheng's public documentation or copying its complete cookbook.
- Treating generated projection as an independently editable source of truth.
- Weakening accepted boundaries to make a reaction pass.
- Creating wrappers around deterministic Tianheng projection or evaluation.
- Promising compatibility with an untested Tianheng release line.
