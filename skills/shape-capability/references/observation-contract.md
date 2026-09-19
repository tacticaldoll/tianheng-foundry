# Observation Contract

Design the measure before the builder name.

## Required Elements

| Element | Question |
|---|---|
| Target | What stable crate, module, type, or runtime seam is governed? |
| Source | Which Cargo/source/AST/probe data contains the fact? |
| Perimeter | Which anchor, descendants, dependency kinds, or public seams are scanned? |
| Rule key | What stable semantic prohibition/restriction identifies the rule? |
| Fact | Which canonical fields distinguish one finding? |
| File | Is a source location faithfully derivable, or must it be null? |
| Polarity | Is repair removal (`deny_breach`), relocation (`allowlist_gap`), or audit-specific? |
| Reason | What forward claim fits entirely inside the measure? |

## Observation Ownership

- Cargo metadata and authored lexical source facts normally belong to static observation.
- Parsed Rust type/signature/impl facts normally belong to semantic observation.
- Concrete behavior at declared seams belongs to runtime observation.
- Shared identity or projection changes may touch core contracts but do not justify a new dimension.

Choose ownership by data source and reaction behavior, not by a desired crate name.

## Honest Absence

Use `file: null` when a graph edge or seam has no single faithful source location. Declare macro,
alias, re-export, conditional-compilation, runtime-path, and cross-language limits explicitly.

Never expand a reason to compensate for a narrow observer.
