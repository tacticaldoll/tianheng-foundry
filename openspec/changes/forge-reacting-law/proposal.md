## Why

Rust adopters often record architectural constraints as prose that an agent can overlook and no
build can enforce. Tianheng can react to observable drift, but adopters still need a disciplined
translation from an already-declared constraint to candidate boundary code without inventing
policy, overstating observation coverage, or deleting prose before the reaction has proven itself.

## What Changes

- Add a portable `forge-law` skill that activates only for a Cargo workspace already using
  Tianheng, or for an explicit Tianheng adoption request.
- Classify a prose claim before editing and admit only structural constraints with a real
  Tianheng observation source, target, and supported recipe.
- Generate a candidate Rust boundary with a forward-looking reason, then require a violating proof,
  a clean precision proof, and projection freshness before treating redundant prose as replaceable.
- Preserve human authority: generated code remains a candidate, accepted law is never weakened
  implicitly, and unobservable or ambiguous claims are narrowed, declined, or returned for
  clarification.
- Package the skill for multiple agent hosts with explicit Tianheng `0.3.x` compatibility and
  network-free structural and scenario validation.

## Capabilities

### New Capabilities

- `reacting-law-forging`: Convert a project-declared Rust architecture claim into a
  reaction-proven Tianheng law candidate while enforcing eligibility, observability, authority,
  and prose-disposition boundaries.

### Modified Capabilities

None.

## Impact

The change introduces the `forge-law` skill, focused Tianheng references, portable plugin
manifests, repository validators, and scenario fixtures. It has no runtime dependency on Tianheng
or Fornax, uses no git submodule, and does not modify Tianheng's API or repository.
