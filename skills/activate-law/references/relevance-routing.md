# Relevance Routing

Select by observable impact, not keyword similarity.

## Direct

Activate when the boundary target equals or contains a touched crate, module, type anchor, or
runtime seam according to its declared scan depth.

## Dependency Adjacent

Activate boundaries at both ends of a possible dependency/import change:

- a touched crate may acquire a forbidden or unlisted dependency;
- a touched module may import a protected subtree;
- another component may newly depend on or import the touched target;
- feature or dependency-kind changes may alter an observed edge.

File locality alone is insufficient for graph observations.

## Semantic Adjacent

Activate when touched implementation can change an observed public or type-level surface:

- visibility and signature coupling;
- re-exports;
- trait-implementation locality or exposure;
- forbidden markers;
- async exposure;
- `dyn Trait` or `impl Trait` shapes and operands.

Private implementation details are relevant only when the declared semantic scan observes them.

## Runtime Adjacent

Activate when behavior can cross a declared seam or change probe coverage. A seam-level finding may
have no single file, so trace callers and probes from the accepted seam identity.

## Workspace

Activate composed audits and workspace-member rules when the touched member contributes to them.
Informational coverage is not a boundary and must be reported separately.

## Exclusion Test

Exclude a boundary only when the task cannot change any fact inside its declared observation
perimeter. Record uncertain near-misses under Adjacent rather than silently treating them as
irrelevant.
