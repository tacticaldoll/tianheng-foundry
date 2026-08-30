# Tianheng 0.5 Recipe Index

This is a routing index, not an API authority or copy of Tianheng's cookbook. Confirm exact builder
spelling against the adopter's resolved Tianheng version.

## Static Observation: Guibiao

| Declared fact | Representative surface | Observes | Important non-observations |
|---|---|---|---|
| Crate dependencies stay in a closed set | `CrateBoundary::restrict_dependencies_to` | Declared Cargo dependency edges for one table/target | Runtime calls and resolved transitive graph |
| A crate declares no external dependencies | `deny_external_dependencies` | Declared non-workspace dependencies | Standard library and runtime loading |
| One crate dependency is forbidden | `forbid_dependency_on` | Declared Cargo edge | Imports without a dependency edge |
| Dependency features are restricted | `forbid_feature`, `restrict_features_of` | Authored feature requests and default pseudo-feature | Transitive feature unification |
| Dependency sources are restricted | `restrict_dependency_sources_to` | Declared registry/path/git kind | Resolved source after patches |
| One module must not import another | `ModuleBoundary::must_not_import` | Source `use` edges in selected depth | General call graph and proc-macro-generated imports |
| Access is allowed only through importers | `must_only_be_imported_by` | Source importers outside a closed allowlist | Reflection and runtime reachability |
| External vocabulary stays in a subtree | `confine_external_crate` | Source `use external_crate` locations | Whether the dependency may exist at all |
| Inline calls under a path are forbidden | `must_not_call_inline` with optional endings | Resolvable inline symbol-path calls | General receiver dispatch and unknown macro expansion |

## Semantic Observation: Hunyi

| Declared fact | Representative surface | Observes | Important non-observations |
|---|---|---|---|
| Public API must not expose a named type | `SignatureBoundary::must_not_expose` | Named type positions and supported re-exports in the Rust AST | Compiler-wide reachable API closure |
| Public seams avoid `dyn` | `DynTraitBoundary` | Supported public `dyn` type shapes or named operands | Runtime concrete origin |
| Public seams avoid `impl Trait` | `ImplTraitBoundary` | Supported public existential type shapes or operands | Runtime implementation choice |
| Public seams avoid async functions | `AsyncExposureBoundary` | Declared public `async fn`, optionally through subtree | Other I/O or executor use |
| Trait impls live in one module | `TraitImplBoundary::only_implemented_in` | Rust trait impl sites | Runtime registration |
| Visibility has a ceiling | `VisibilityBoundary` | Authored Rust visibility keywords | Effective reachability through every path |
| A marker is forbidden | `ForbiddenMarkerBoundary` | Supported marker acquisition in the AST | Arbitrary semantic meaning of the marker |
| Unsafe stays in named subtrees | `UnsafeBoundary::only_under` | Supported authored `unsafe` sites | Macro-generated unsafe and crate-wide compiler ban |

## Runtime Observation: Louke

| Declared fact | Representative surface | Observes | Important non-observations |
|---|---|---|---|
| Only named origins cross a runtime seam | `RuntimeBoundary::only_origins` plus Louke probes | Registered concrete origins at a probed seam | Unprobed paths and general effect reachability |

## Composed Profiles

Use `SansIoPure` only when the project explicitly declares both observable halves: selected ambient
clock reads are absent and public async functions are absent in the target subtree. It does not
imply general filesystem, network, environment, or effect purity.

Use other composed profiles only after decomposing their parts and confirming every generated
reason clause remains within the constituent observation perimeters.

## Selection Discipline

1. Select by the observed contradiction, never by a fashion label.
2. Prefer one closed allowlist over an allowlist plus redundant denials.
3. Choose scan depth deliberately; do not claim subtree governance from an anchored-only rule.
4. Treat empty, root-wide, or unknown targets as possible constitution errors, not clean results.
5. When no row observes the declared contradiction, return `DECLINE` or capability pressure.
