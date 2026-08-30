---
name: forge-law
description: Use when an agent is about to add or change normative architecture prose in a Rust workspace that already uses Tianheng, or when the user explicitly asks to adopt Tianheng; classifies the declared claim, admits only Tianheng-observable structure, writes candidate boundary code, proves violation and precision reactions, and proposes safe prose disposition without inventing policy or silently amending accepted law. Do not use for non-Rust repositories, generic documentation, subjective design preferences, or cross-language claims outside a Cargo workspace.
---

# Forge Tianheng Law

Turn a project-declared architecture constraint into a tested Tianheng law candidate. This is a
controlled writing workflow: it may edit an eligible adopter repository, but its result remains a
candidate until human review accepts it.

Tianheng owns reaction semantics. The adopter's Rust `Constitution` is the law source. This skill is
neither.

## Load References Deliberately

- Read [claim-classification.md](references/claim-classification.md) after eligibility succeeds.
- Read [recipe-index.md](references/recipe-index.md) only for an admitted structural claim.
- Read [reaction-proof.md](references/reaction-proof.md) before designing or running verification.
- Read [authority-transition.md](references/authority-transition.md) before editing accepted law or
  changing the source prose.

The references are selection and safety guidance for Tianheng `0.5.x`, not a replacement for the
adopter's dependency docs or Tianheng's upstream cookbook. Inspect the actual dependency surface
when exact API spelling matters.

## Phase 0: Gate Eligibility Before Any Write

Semantic activation is only an invitation to inspect. Establish all of the following before editing:

1. Locate the Cargo workspace without changing it. Prefer `cargo locate-project --workspace
   --message-format plain`; otherwise walk upward to the governing `Cargo.toml`.
2. Establish the writable Rust scope from the workspace root. In a mixed-language monorepo, treat
   everything outside that Cargo workspace as read-only and out of claim coverage.
3. Inspect manifests and Rust sources with structured TOML/Cargo data where available.
4. Qualify Tianheng:
   - existing dependency, `tianheng::Constitution`, law runner, or generated projection; or
   - a direct user request to adopt Tianheng for the first time.
5. Resolve the Tianheng version from the manifest or lockfile. Proceed directly only for the
   supported line; otherwise stop for a compatibility investigation.

Stop without writing when the repository is not Rust, Tianheng is absent without an adoption
request, the workspace cannot be scoped, or the relevant source is outside the writable area.

## Phase 1: Establish Claim Authority

Find the exact normative claim and cite its source:

- direct user instruction in the current request;
- project contract, architecture document, agent guide, or code documentation; or
- an existing accepted Tianheng law when the user explicitly asks for an amendment.

Repository shape, conventional crate names, and generic Rust practice are not authority. Never
invent a law because the code "looks layered."

Classify the claim using `claim-classification.md`. Only a structural claim continues
automatically. Keep process, judgment, history, and API explanation in documentation. If one
paragraph mixes categories, separate them before deciding what can move.

An existing accepted boundary is not a prose-to-law conversion. Require an explicit amendment
request before changing or removing it.

## Phase 2: Admit An Observable Fact

Translate the claim into one concrete observed fact before choosing an API:

```text
authority source
  -> target
  -> observation source
  -> forbidden or restricted fact
  -> honest non-observations
```

Use `recipe-index.md` to choose the instrument and rule family. Decompose fashion labels such as
"clean," "hexagonal," or "sans I/O" into the actual dependency, import, exposure, async, clock,
unsafe, or runtime-origin facts the project declared.

Produce a Boundary Card before editing:

```markdown
**Intent source**: <path:line or direct user instruction>
**Target**: <crate, module, type seam, or runtime seam>
**Observation source**: <Cargo metadata, Rust source tokens, syn AST, or runtime probe>
**Candidate recipe**: <Tianheng rule family>
**Observable perimeter**: <what can react>
**Not observed**: <important exclusions>
**Verdict**: ADMIT | NARROW | CLARIFY | DECLINE
```

Continue only on `ADMIT`. Apply `NARROW` only when the narrower form still preserves an explicit
part of the declared intent. Ask on `CLARIFY`; make no edits on `DECLINE`.

## Phase 3: Design The Candidate Transaction

Follow the adopter repository's existing law-source, test, and projection patterns. For first
adoption, create only the smallest viable path:

- one Tianheng dependency at the repository's chosen dependency authority;
- one `Constitution` containing the admitted boundary;
- one existing or focused runner/test entrypoint;
- one violating proof and one clean precision proof; and
- a generated projection only when the project chooses an agent-law artifact.

Do not create an exhaustive constitution, coverage policy, baseline, or extra crate merely because
the APIs exist.

Draft the `.because(...)` reason in forward voice. Every clause must stay inside the Boundary Card's
observable perimeter. Keep historical provenance out of the live reason.

Before editing, identify:

- exact files to change;
- existing accepted law that must remain untouched;
- the violating and clean cases;
- verification commands;
- source prose disposition; and
- rollback as reverting the candidate diff.

## Phase 4: Write Candidate Law

Make the smallest repository-native edits that materialize the admitted fact:

1. Add or extend the project's existing `Constitution`; do not create a parallel law source.
2. Use the selected Tianheng rule with explicit target, parameters, depth, and reason.
3. Avoid redundant rules. A closed allowlist already enforces exclusions outside it.
4. Add the focused reaction proofs alongside existing architecture tests or in a small governed
   fixture that follows local conventions.
5. Update the generated projection through the project's declared regeneration path, never by
   hand-editing its boundary body.

Label the working result `BoundaryCandidate`. Do not describe it as accepted project law.

## Phase 5: Prove Teeth And Precision

Follow `reaction-proof.md`.

- The violating case must produce an enforced violation or exit class `1`.
- The clean case must remain clean with exit class `0`.
- Exit class `2` is a constitution, usage, or scan failure, never proof of enforcement.
- A warning, a fully baselined violation, compilation alone, or projection alone does not prove the
  new law reacts.
- Run the repository's normal formatting, lint, test, and governance gates after focused proof.

If proof fails, repair code or declaration toward the cited intent. Never add `.warn()`, baseline
the new fact, remove depth, broaden an allowlist, or weaken accepted law merely to make the run
green. Stop when the observation model cannot support the claim honestly.

After both directions pass, label the result `VerifiedCandidate`.

## Phase 6: Dispose Of Prose Last

Use `authority-transition.md`.

- Default: preserve the source prose and report the proposed disposition for human review.
- When the user explicitly requested a complete replacement diff, remove only the redundant live
  structural sentence after proof succeeds; the diff remains a candidate until review.
- Preserve or relocate historical rationale, process, judgment, and API explanation.
- When Tianheng reacts to only part of a paragraph, narrow the prose to the ungoverned remainder
  rather than deleting it.
- Never hand-edit a generated law projection.

## Phase 7: Report The Candidate

Return:

```markdown
## Verified Candidate

**Intent authority**: <source>
**Boundary**: <target and rule>
**Reaction perimeter**: <observed and explicitly unobserved>
**Changed files**: <paths>
**Violating proof**: <command and observed class>
**Clean proof**: <command and observed class>
**Projection**: <fresh | not used>
**Prose disposition**: <preserved | candidate removal | narrowed | relocated>
**Authority**: Awaiting human review; not yet accepted law.
```

If stopped, report the last completed state, the blocking gate, and whether the correct disposition
is `CLARIFY`, `DECLINE`, compatibility work, or deliberate amendment.

## Hard Stops

- Do not act outside a Cargo workspace.
- Do not enroll a Rust project into Tianheng without direct user intent.
- Do not convert generic best practice into project law.
- Do not claim observation beyond the selected Tianheng perimeter.
- Do not silently change an accepted boundary.
- Do not replace prose before reaction proof.
- Do not use git submodules or vendor Tianheng.
- Do not merge, commit, or otherwise claim human acceptance unless explicitly requested.
