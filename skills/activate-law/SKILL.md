---
name: activate-law
description: Use when an agent is about to inspect or change Rust code in an existing Tianheng-governed workspace and needs the accepted law relevant to the current task before editing; reads the canonical list projection, maps the intended touch set and architectural effects to direct and adjacent boundaries, and emits a task-local Active Law Set for the implementation workflow. Do not use for non-Rust repositories, Tianheng adoption, creating or amending law, repairing an already-reported violation, or replacing full repository orientation.
---

# Activate Tianheng Law

Select accepted Tianheng law into task-local working context before code changes begin. This is a
read-only activation workflow; Tianheng remains the projection authority.

## Load References Deliberately

- Read [projection-source.md](references/projection-source.md) before obtaining law.
- Read [task-envelope.md](references/task-envelope.md) when scoping the intended change.
- Read [relevance-routing.md](references/relevance-routing.md) while selecting boundaries.
- Read [implementation-handoff.md](references/implementation-handoff.md) before returning control
  to the user's coding workflow.

These references target Tianheng `0.5.x`. Use the adopter's runner and local governance commands
when they differ from the published binary.

## Phase 0: Gate Activation

Activate only when all are true:

- the work is inside a discovered Cargo workspace;
- the workspace already has accepted Tianheng law or a declared Tianheng runner;
- the user is asking for code inspection, planning, implementation, refactoring, or review; and
- no application-code edit has begun for this task.

Route instead:

- new declared architecture constraint to `forge-law`;
- an existing Tianheng finding to `repair-drift`;
- an explicit change to accepted law to `amend-law`.

In a mixed-language monorepo, activate only for the Cargo workspace and effects crossing its Rust
boundary. Do not claim coverage for unrelated languages.

## Phase 1: Read Canonical Law

Follow `projection-source.md`.

1. Locate the project-native Tianheng runner and manifest.
2. Run its `list --format json` form without editing the workspace.
3. Capture target, kind, rule and parameters, severity, reason, anchor, and declared scan depth for
   every boundary.
4. Confirm the Tianheng version is supported.

Do not scrape a generated Markdown projection when canonical JSON is available. Do not hand-edit,
rewrite, summarize away, or supplement the declared reasons.

Stop on runner/constitution error, unsupported compatibility, or contradictory law sources. An
empty constitution or uncovered crate is an observed absence of law, not permission to invent it.

## Phase 2: Form The Change Envelope

Use `task-envelope.md`. Establish from the user request and code inspection:

```markdown
**Requested outcome**: <behavioral or structural result>
**Direct touch set**: <crates, modules, types, seams, manifests>
**Dependency effects**: <edges/imports/features likely added, removed, or reversed>
**Semantic effects**: <public signatures, visibility, trait impls, markers, async/dyn/impl Trait>
**Runtime effects**: <declared seams, probes, clocks, I/O, executor origins>
**Unknowns**: <touches not yet resolvable>
```

The touch set is a hypothesis, not authorization to edit. Trace enough code to include likely
architectural effects, not only files named by the user.

If the task is too vague to establish a touch set, return `CLARIFY_TOUCH_SET`. Do not activate the
whole constitution merely to avoid the scoping work.

## Phase 3: Select Relevant Boundaries

Use `relevance-routing.md`. Select a boundary when the proposed change may alter a fact it observes:

- **Direct**: the touched crate, module, type, or runtime seam is the target.
- **Dependency**: the change may add, remove, move, or reverse a dependency/import edge governed
  from either endpoint.
- **Semantic**: public exposure, visibility, trait implementation, marker, async, `dyn`, or
  `impl Trait` shape may change inside the observed scope.
- **Runtime**: behavior or probe coverage may cross a declared runtime seam.
- **Workspace**: a composed audit or workspace-level rule observes the affected member/change.

Include an adjacent boundary when uncertainty is inside its observable perimeter. Record why it is
adjacent rather than silently dropping it. Do not include boundaries solely because their prose
sounds thematically related.

## Phase 4: Build The Active Law Set

Preserve each selected boundary's accepted wording:

```markdown
## Active Law Set

**Task**: <requested outcome>
**Cargo scope**: <workspace root and eligible subtree>

### Direct
- **Target / rule**: ...
  **Reason**: ...
  **Change exposure**: ...

### Adjacent
- **Target / rule**: ...
  **Reason**: ...
  **Why active**: dependency | semantic | runtime | workspace

### Uncovered Effects
- <effect for which no accepted boundary exists; no policy inferred>

### Implementation Guard
- <concrete constraint the coding workflow must preserve>

**Projection source**: <runner command and Tianheng version>
```

An implementation guard paraphrases only enough to connect the task to the boundary; the exact
reason remains beside it. Do not turn uncovered effects into new rules or generic best practice.

## Phase 5: Check Activation Completeness

Before handing off:

1. Every direct touch maps to a selected boundary or `Uncovered Effects`.
2. Every predicted dependency, semantic, and runtime effect was considered.
3. Each selected boundary cites an observable connection to the task.
4. No selected reason was strengthened, weakened, or historically embellished.
5. Law source, generated projection, baseline, and configuration remain unchanged.

If two active laws appear to conflict, report both reasons and stop for resolution. Activation does
not choose which accepted law yields.

## Phase 6: Hand Off To Implementation

Follow `implementation-handoff.md`. Return the Active Law Set as working context and continue the
user's requested coding workflow under it. Do not ask for confirmation merely because activation
succeeded.

After implementation, the surrounding workflow must run the project-native Tianheng check:

- clean or advisory exit `0`: report remaining warning/baseline state accurately;
- enforced exit `1`: route the structured report to `repair-drift`;
- exit `2`: stop as a constitution, scan, usage, or harness failure;
- requested change to active law: require `amend-law`.

Activation predicts relevant law; only reaction verifies the completed code.

## Hard Stops

- Do not activate outside a Cargo workspace or without existing Tianheng governance.
- Do not write application code, law, baselines, projections, or configuration in this skill.
- Do not replace canonical projection with agent-authored governance prose.
- Do not treat an uncovered effect as implicitly allowed, forbidden, or governed.
- Do not omit adjacent law merely because it does not target the edited file.
- Do not route a known violation through activation to avoid `repair-drift`.
- Do not route an explicit law change through activation to avoid `amend-law`.
- Do not claim compliance before the post-change reaction runs.
