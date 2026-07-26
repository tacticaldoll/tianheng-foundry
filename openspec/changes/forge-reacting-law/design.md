## Context

Tianheng makes Rust `Constitution` code authoritative and projects that law into readable agent
context. The missing adopter workflow begins one step earlier: an agent asked to add or edit
normative architecture prose should first determine whether the project already declares that
intent and whether Tianheng can observe it. If so, the agent should materialize candidate boundary
code and prove its reaction instead of adding another unenforced restatement.

Semantic skill activation is host-dependent and probabilistic. It therefore cannot authorize a
write. The workflow needs a deterministic structural eligibility gate after activation, explicit
authority states, and failure paths that decline unsupported claims.

## Goals / Non-Goals

**Goals:**

- Provide one portable `forge-law` workflow for Rust/Tianheng adopters.
- Convert only project-declared, observable architecture constraints.
- Keep claim classification, generation, proof, and prose disposition in one transaction.
- Produce candidate law that fails on a violating case and remains clean on a precision case.
- Keep Tianheng as the sole reaction engine and the adopter's `Constitution` as the sole law source.
- Validate the skill, scenario corpus, plugin manifests, and representative Tianheng `0.3.x`
  declaration vocabulary without git submodules.

**Non-Goals:**

- Discover or recommend generic Rust architecture best practices.
- Govern non-Rust parts of a mixed-language repository.
- Replace process documentation, API documentation, or historical rationale with boundaries.
- Automatically accept, merge, weaken, remove, or amend an established law.
- Copy the complete Tianheng cookbook or provide a second Tianheng API reference.
- Add review, reaction-triage, or context-loader skills before their separate value is proven.

## Decisions

### One skill owns the initial transaction

`forge-law` owns eligibility, classification, observation admission, controlled edits, proof, and
prose disposition. Splitting these phases now would create handoff ambiguity and named surfaces
without independent consumers. Future skills may reuse concepts only after real usage demonstrates
a separate trigger and output.

### Semantic activation is followed by structural eligibility

The description may auto-trigger when an agent is about to write normative architecture prose, but
the skill must inspect the repository before editing. It proceeds only when:

1. a Cargo workspace root is discoverable;
2. edits can be scoped to that workspace;
3. Tianheng is already present, or the user explicitly requested first adoption; and
4. the Tianheng version is supported or the user accepts a compatibility investigation.

A mixed-language monorepo is narrowed to the Cargo workspace. A non-Rust repository stops without
writing.

### Claims have explicit authority states

The workflow treats prose as evidence, not automatic authority:

```text
ProseClaim -> AdmittedIntent -> BoundaryCandidate -> VerifiedCandidate
```

Human review alone moves a `VerifiedCandidate` into the project's accepted `Constitution`.
Generated edits and successful tests never grant that authority themselves.

### Observation admission precedes recipe selection

The workflow first identifies an observable fact and only then chooses a recipe. A recipe reference
contains a compact selection key, observation source, representative Tianheng surface, and explicit
non-observations. It does not mirror the cookbook narrative.

Unsupported, subjective, cross-language, or broader-than-observed claims are narrowed, clarified,
or declined before edits. The generated `.because(...)` reason may describe only the shape the
selected boundary reacts to.

### Proof is bidirectional

A compiling declaration is insufficient. The candidate must have:

- a violating fixture or existing case that produces an enforced reaction;
- a clean precision case that does not react;
- a projection freshness path when the project publishes an agent-law artifact; and
- verification commands recorded in the result.

The exact test form follows the adopter repository's existing patterns. The skill must not weaken
the boundary, add a warning, or baseline the new violation merely to make verification green.

### Prose disposition is last

Normative prose is removed only when the accepted candidate covers the same claim. Historical
rationale moves to the project's provenance surface; process and judgment prose remain documented;
partially covered claims are narrowed rather than deleted wholesale. Before human acceptance, the
workflow reports proposed prose disposition but preserves the source text unless the user
explicitly asked for the complete candidate diff.

### Compatibility is explicit and locally injectable

`compatibility.json` declares the supported Tianheng line and vocabulary used by the recipe index.
A network-free compatibility script accepts a local Tianheng checkout through
`TIANHENG_SOURCE`, patches the crate family into a representative consumer fixture, and compiles
the referenced declaration forms. CI may check out the declared upstream tag before invoking the
script; the script itself never clones or downloads.

### Fornax is a structural precedent, not a dependency

The repository adopts the portable skill/distribution layout and host manifest separation proven
by Fornax. It does not import Fornax, inherit its read-only identity, or use a submodule.

## Risks / Trade-offs

- **Semantic auto-trigger may not fire** -> Keep a clear manual invocation and make reaction, not
  invocation, the correctness backstop.
- **The skill may infer policy from repository shape** -> Require a cited prose or direct-human
  intent source before admission.
- **A reason may overclaim coverage** -> Recipe references state non-observations and the workflow
  compares every reason clause to the selected perimeter.
- **Generated tests may fit one repository poorly** -> Follow local test conventions and require
  observable outcomes rather than one fixed fixture layout.
- **Recipe knowledge may drift from Tianheng** -> Declare compatibility, compile representative
  vocabulary against a supplied checkout, and reject unsupported versions.
- **Automatic prose deletion could destroy rationale** -> Separate normative claim, history,
  process, and API explanation before proposing disposition.
- **A writing skill can weaken accepted law** -> Existing-law changes require an explicit amendment
  request and remain outside the automatic materialization path.
