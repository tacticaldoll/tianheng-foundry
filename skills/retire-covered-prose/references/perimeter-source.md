# Perimeter Source

A boundary's **observed perimeter** is what its reaction actually examines. It is not its reason,
its name, or its target. Coverage is judged against the perimeter, so the perimeter must come from
a source that cannot drift away from the implementation.

## Resolution Order

Resolve the adopter's Tianheng **version and source kind** from `cargo metadata` or the lockfile
before reading any perimeter, then take the first source that resolves:

1. **The adopter's own Tianheng source**, when the dependency is a path, a git checkout, or a
   patched source. Whatever governs this workspace is the only correct authority for it, including
   a fork.
2. **The upstream `docs/observation-bounds.md` at the tag matching the resolved version**, when the
   dependency comes from a registry. Name that document and no other. It is generated from the
   specs and held fresh by an upstream test, so a stale copy fails upstream instead of misleading
   here. It sits at the repository root, not inside the published crate, so read it from the
   upstream repository at that tag rather than from the registry copy.

   A resolved version whose tag ships no such document has **no source 2**. A README table, crate
   rustdoc, an unpublished normative document, and a perimeter assembled by reading the
   implementation are not substitutes, however carefully written: each can drift from the code, and
   not drifting is the single property this source exists to supply. Do not assemble a perimeter
   from them, and do not read their silence about a shape as a bound on it.
3. **The bundled routing knowledge** in `forge-law`'s recipe index, as a last resort. It is a local
   summary carried for recipe selection, it is version-stamped, and it is the only source in this
   list that can silently disagree with the code. Using it lowers confidence: a claim judged
   against this source alone may not be `HELD`, only *not yet shown to be wider*.

Never mix sources for one judgement. Record which source answered, beside the finding.

## Fallback And Refusal

The first two sources may require reading outside the workspace, and a host may offer no way to do
it. Treat that capability as optional:

- Say which source answered and which were unreachable.
- When only source 3 is reachable, `HELD` is unavailable. Judge `WIDER`, `UNGOVERNED`, and
  `UNOBSERVABLE` as usual — those retain the comment and are safe under a weaker source — and
  return `WIDER` wherever a claim would otherwise have been `HELD`, recording that perimeter
  authority was unreachable. A summary that can silently disagree with the code cannot demonstrate
  coverage, and this skill deletes only on demonstration.
- When no source is reachable, stop. A sweep with no perimeter authority is a style sweep wearing a
  criterion.

## What A Perimeter Statement Looks Like

A usable perimeter names what the reaction reads and what it declines to read: *observes declared
Cargo dependency edges for one table and target; does not observe runtime loading or the resolved
transitive graph*. Both halves matter. The second half is what decides `WIDER`, and a source that
states only the first half cannot answer this skill's question.
