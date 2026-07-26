# Tianheng Foundry - Project Contract

Tianheng Foundry is a portable companion skill collection for Rust projects that use, or
explicitly intend to adopt, Tianheng.

## Purpose

The collection turns an already-declared architectural prose constraint into a candidate
Tianheng law: Rust boundary code, a forward-looking reason, and proof that the boundary reacts
on a violating fixture while remaining clean on a precision fixture.

It does not invent architecture policy. It does not become a second source of law. A generated
diff remains a candidate until a human accepts it; the adopter's Rust `Constitution` is the
authority, its generated projection is context, and Tianheng's evaluator is the reaction.

## Context Lifecycle

```text
prose claim
  -> classified claim
  -> observable intent
  -> boundary candidate
  -> reaction-proven candidate
  -> human-accepted Constitution
  -> generated projection
  -> code change
  -> reaction
  -> repair or deliberate amendment
```

Skills belong only where a transition needs domain judgment or controlled edits. Deterministic
projection, evaluation, and exit classification remain Tianheng's work.

## Laws

- **Rust-only eligibility.** A writing workflow acts only inside a discovered Cargo workspace.
  A non-Rust repository is out of scope. In a mixed-language monorepo, only the Cargo workspace
  subtree is eligible.
- **Tianheng qualification.** An existing Tianheng dependency or law source qualifies a
  workspace. Initial adoption requires an explicit user request; a generic Rust repository is
  never silently enrolled.
- **Declared intent only.** Project prose and direct human instruction are evidence of intent.
  Repository shape or generic best practice is not authority to create a law.
- **Observation before generation.** A claim becomes code only when it maps to a real Tianheng
  observation source, target, and rule. Otherwise the workflow declines or narrows the claim.
- **Proof before replacement.** Generated law does not replace prose until a violating case
  reacts, a clean case stays clean, the projection is fresh, and a human accepts the change.
- **No silent amendment.** A failing law is repaired toward its reason. Weakening, removing, or
  replacing an accepted law requires an explicit amendment request.
- **No copied authority.** Tianheng owns its public API, specifications, and complete cookbook.
  This collection carries only the selection and adaptation knowledge needed for supported
  versions.
- **No repository coupling.** Tianheng, Fornax, and this collection remain independent
  repositories. Compatibility is explicit and tested; git submodules are not used.

## Initial Scope

The first release contains one skill: `forge-law`. It covers eligibility, claim classification,
observation admission, recipe selection, controlled candidate edits, reaction proof, projection
freshness, and safe prose disposition as one transaction.

Review, reaction triage, and task-local law activation remain unnamed future candidates until
their independent inputs, outputs, and failure modes are demonstrated.

## Compatibility

The initial compatibility target is Tianheng `0.3.x`. Compatibility means the skill's referenced
public concepts and representative generated boundary forms remain valid; it does not make the
skill a dependency of Tianheng or Tianheng a vendored dependency of this repository.
