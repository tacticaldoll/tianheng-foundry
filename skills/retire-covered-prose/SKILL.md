---
name: retire-covered-prose
description: Use when a user asks to retire code comments in a Rust workspace already governed by Tianheng and the open question is which comments an accepted boundary already holds; inventories structural claims in `//` and `//!` comments, admits only a claim held by an enforced and unbaselined boundary, deletes exactly those with per-deletion coverage evidence, and routes every remaining claim onward. Do not use to delete comments as a style mandate, to rewrite or narrow a human-authored sentence, to touch rustdoc on a public item, to create or amend law, or in a non-Rust or ungoverned repository.
---

# Retire Covered Prose

Delete a structural comment only when accepted Tianheng law already reacts to the same claim. The
comment is redundant because the reaction holds the claim; nothing else is redundant.

This skill creates no boundary and changes no law. It removes prose that a reaction has already
replaced, and reports every claim it did not remove.

## Load References Deliberately

- Read [coverage-criterion.md](references/coverage-criterion.md) before judging any comment.
- Read [perimeter-source.md](references/perimeter-source.md) before deciding what a boundary does
  not observe.
- Read [routing-dispositions.md](references/routing-dispositions.md) when disposing of a claim this
  skill will not retire.

## Phase 0: Gate The Sweep

Activate only when all are true:

- the work is inside a discovered Cargo workspace;
- the workspace already has accepted Tianheng law or a declared Tianheng runner; and
- the user asked which comments existing law has made redundant.

Refuse a style mandate. "Remove all comments", "we do not write comments here", and "strip the
comments from this file" are requests to judge prose by taste, not by reaction. Return
`REFUSE_STYLE_REQUEST` and say which request this skill answers instead. A sweep whose criterion is
the absence of comments is not this skill narrowed; it is a different and unprovable operation.

Those three are examples, not the test. The test is the criterion the request names: a request
naming fewer comments, tidier files, or a house style is refused; a request naming what existing law
has made redundant is answered.

**Violating the letter of this gate is violating its spirit.** A request whose criterion is fewer
comments is refused however it is worded, and that refusal is what this skill is for rather than a
limitation of it.

Red flags — stop and return `REFUSE_STYLE_REQUEST`:

- "They clearly want the comments gone; the covered-only criterion is a reasonable way to give them
  that."
- "They did not say *all* comments, so this is not a style mandate."
- "I will run the sweep and note the criterion in the report, so nothing is lost."
- "This file is objectively over-commented."
- "Refusing is unhelpful when I can do the safe subset right now."

Each is the same move: treating fewer comments as the goal and this skill's criterion as the means.
The criterion is the goal. Returning the refusal and naming the request this skill does answer is a
complete and correct answer.

A refusal ends the analysis too. Once this gate closes, do not inventory, judge, or report on
individual comments — doing so is the sweep itself, and a `HELD`/`WIDER` table produced here
manufactures the audit trail for a deletion set nobody asked for on this criterion. The findings
belong to the request this skill answers, not to the one it just refused.

Route instead:

- a declared constraint with no boundary yet to `forge-law`;
- an existing Tianheng finding to `repair-drift`;
- an explicit change to accepted law to `amend-law`;
- baseline debt to `manage-baseline`.

In a mixed-language monorepo, sweep only the Cargo workspace.

## Phase 1: Read Canonical Law

1. Locate the project-native Tianheng runner and manifest.
2. Run its `list --format json` form without editing the workspace.
3. For every boundary capture target, kind, rule and parameters, **severity**, **baseline state**,
   reason, anchor, and declared scan depth.
4. Confirm the Tianheng version is supported.

Severity and baseline state are load-bearing here, not metadata. A claim held only by a `warn`
boundary, or by a boundary whose violation is already absorbed into a baseline, is a claim with no
teeth — see `coverage-criterion.md`.

Stop on runner or constitution error, unsupported compatibility, or contradictory law sources. An
empty constitution is an observed absence of law, not permission to delete prose.

## Phase 2: Inventory Structural Claims

Collect candidate comments inside the eligible subtree:

- **In corpus**: `//` line comments anywhere in the eligible subtree, and `//!` inner comments in a
  module that is not reachable as `pub` from the crate root, that assert a structural fact about
  dependencies, imports, module relationships, public exposure, visibility, trait implementation
  sites, markers, `unsafe`, `async`, `dyn`, `impl Trait`, or a runtime seam.
- **Out of corpus**: rustdoc on a published item — every `///`, and every `//!` at a crate root or
  in a module reachable as `pub` from the crate root. The Prose Disposition table keeps API
  explanation in product docs and rustdoc, so it is never a retirement candidate even when a
  boundary happens to cover its subject, and even when it is the only claim a boundary holds whole.
  Module visibility is the test, not the comment's wording: resolve it from the `mod` declarations
  rather than from how documentary the sentence reads.
- **Out of corpus**: historical rationale, a measured observation that is the evidence for a
  declared bound, process or approval rules, judgment guidance, safety justification for an
  `unsafe` block, an invariant a reaction does not observe, and a `TODO` or tracker reference.

Record each candidate with its file, line span, and the claim stated in the author's own words. Do
not paraphrase a claim into the vocabulary of a boundary you already have in mind; that is how a
narrower reaction comes to look like a match.

## Phase 3: Judge Coverage Per Claim

Follow `coverage-criterion.md`. For each candidate, decide exactly one:

| Finding | Meaning |
|---|---|
| `HELD` | An enforced, unbaselined boundary observes the whole claim |
| `WIDER` | The claim asserts more than any boundary observes |
| `TOOTHLESS` | A boundary matches the claim but is `warn`-only |
| `ABSORBED` | A matching boundary's violation sits in a baseline |
| `UNGOVERNED` | No boundary observes the claim, and Tianheng could |
| `UNOBSERVABLE` | No boundary observes the claim, and Tianheng cannot |

Only `HELD` may be retired. Compare the claim against the boundary's **observed perimeter**, never
against its reason prose; `perimeter-source.md` says where the perimeter is read from.

**Default finding**: `WIDER`. A candidate becomes `HELD` only by positive demonstration that the
observed perimeter covers every fact the sentence asserts. Absence of a reason to doubt is not a
demonstration. The asymmetry is deliberate: the cost of a wrong `WIDER` is a comment that stays, and
the cost of a wrong `HELD` is a claim the project declared and no longer states anywhere.

## Phase 4: Retire Only What Is Held

Write boundary, in full:

- **May delete**: the exact line span of a `HELD` comment.
- **May not** edit, narrow, reword, relocate, or reflow any prose, including a comment this sweep is
  retaining. Delete-only means the line span goes or nothing about it changes.
- **May not** touch Rust code outside a deleted comment's line span, the Constitution, a baseline,
  a generated projection, runner wiring, or governance configuration.
- **May not** commit, stage selectively to hide a deletion, tag, or push.

Authority: a sweep request authorizes the sweep, not the deletion set. The criterion is what the
user approved; the set is not knowable until this phase computes it.

- Default, and whenever authority is ambiguous: report the proposal and write nothing.
- When the user asked for the sweep to be applied, delete into the working tree and leave it
  unstaged, so the diff is the presentation and review happens there.

A deletion whose boundary identity, rule, severity, and baseline state cannot all be cited is not
`HELD` and must not be written.

## Phase 5: Report And Route

```markdown
## Retired Prose

**Verdict**: RETIRE | NOTHING_COVERED
**Cargo scope**: <workspace root and eligible subtree>
**Projection source**: <runner command and Tianheng version>
**Applied**: <working tree | proposal only>
**Line numbers**: every location above is given as it stood before this sweep, so the set reads
consistently whether or not deletions were applied.

### Retired
- `<file>:<lines as they were before this sweep>` — <claim in the author's words>
  **Held by** (REQUIRED): <target / kind / rule / parameters>
  **Severity** (REQUIRED): <as read from the projection>
  **Baseline state** (REQUIRED): <as read from the projection>
  **Perimeter match** (REQUIRED): <why the observed perimeter covers the whole claim>
  **Perimeter source** (REQUIRED): <which source in perimeter-source.md answered>

### Retained
- `<file>:<lines as they were before this sweep>` — <claim> — `WIDER | TOOTHLESS | ABSORBED | UNGOVERNED | UNOBSERVABLE`
  **Route**: amend-law | forge-law | manage-baseline | shape-capability
  **Because**: <the observation gap, in one line>
```

The retained list is an output, not a leftover. Follow `routing-dispositions.md`: a `WIDER` or
`TOOTHLESS` claim is a candidate tightening for `amend-law`, an `UNGOVERNED` claim is a candidate
conversion for `forge-law`, an `ABSORBED` claim is debt for `manage-baseline`, and an
`UNOBSERVABLE` claim is upstream pressure for `shape-capability`.

Do not perform any routed operation inside this skill.

## Hard Stops

- Do not activate outside a Cargo workspace or without existing Tianheng governance.
- Do not delete a comment on any criterion other than an enforced, unbaselined boundary holding its
  whole claim.
- Do not accept the absence of comments as a goal, however the request is phrased.
- Do not rewrite, narrow, or relocate a human-authored sentence; a rewrite has no available proof.
- Do not delete rustdoc on a public item, a safety justification, a measured observation, or an
  invariant no reaction observes.
- Do not inventory, judge, or report per-comment findings after the gate refuses; that analysis is
  the sweep.
- Do not write law, baselines, projections, or configuration in this skill.
- Do not treat a `warn` severity or a baselined finding as coverage.
- Do not delete without citing the boundary identity, rule, severity, and baseline state.
- Do not commit or push a retirement diff.
- Do not read a boundary's reason prose as evidence of what it observes.
