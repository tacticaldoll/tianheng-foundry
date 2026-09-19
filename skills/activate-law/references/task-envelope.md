# Change Envelope

Activation needs the architectural effects of the task, not a final implementation plan.

## Direct Touch Set

Identify:

- Cargo manifests and workspace members;
- Rust crates and modules;
- public types, traits, impls, functions, and signatures;
- runtime seams and probe sites; and
- generated or governance files that must remain read-only.

Use code search and control/data-flow tracing to expand beyond filenames named in the request.

## Effect Axes

| Axis | Questions |
|---|---|
| Dependency | Will an edge, import, feature, build dependency, or ownership direction move? |
| Semantic | Will visibility, signature shape, trait placement, markers, async, `dyn`, or `impl Trait` change? |
| Runtime | Will clocks, I/O, executor origins, seam declarations, or probes change? |
| Workspace | Will membership, composition, or cross-crate coverage change? |

Record uncertainty explicitly. If a likely effect cannot yet be placed, inspect more code or return
`CLARIFY_TOUCH_SET`.

## Scope Discipline

A mixed-language request may have one Rust envelope and separate ungoverned effects. Keep them
separate. Do not claim Tianheng governs files merely because they participate in the same feature.
