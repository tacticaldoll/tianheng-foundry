---
name: amend-law
description: Use when a user explicitly requests a deliberate change to an existing accepted Tianheng Constitution boundary in a Rust workspace; classifies the amendment as tighten, loosen, retarget, reason correction, or removal, preserves before-state evidence, writes a minimal law candidate, and proves the intended reaction delta before human review. Do not use for new prose-to-law conversion, ordinary Tianheng violations, vague requests to make CI pass, baseline maintenance alone, or any law change lacking explicit amendment authority.
---

# Amend Tianheng Law

Produce a verified candidate change to accepted Tianheng law. Explicit authority opens the
amendment workflow; it does not make the resulting diff accepted automatically.

## Load References Deliberately

- Read [authority-gate.md](references/authority-gate.md) before any write.
- Read [amendment-classification.md](references/amendment-classification.md) when defining the
  requested delta.
- Read [proof-matrix.md](references/proof-matrix.md) before designing fixtures or editing law.
- Read [migration-and-projection.md](references/migration-and-projection.md) before sequencing code,
  baseline, or generated-context changes.

These references target Tianheng `0.3.x`. Inspect the adopter's actual law source, runner, and local
amendment protocol before relying on exact API spelling.

## Phase 0: Qualify Existing Law

Work only in a discovered Cargo workspace with:

- an existing Tianheng dependency on the supported line;
- an accepted Rust `Constitution`;
- a resolvable boundary named by the request; and
- a local review or amendment path that the candidate can follow.

If the request concerns a new constraint that is not yet accepted law, route to `forge-law`. If it
concerns product code violating unchanged law, route to `repair-drift`.

Stop before writing when the boundary cannot be identified, Tianheng compatibility is unknown, the
workspace scope is ambiguous, or the local authority source conflicts with the request.

## Phase 1: Establish Explicit Amendment Authority

Apply `authority-gate.md`. Require a direct request to change, weaken, strengthen, retarget, rewrite,
or remove the identified accepted boundary. A feature request, failing check, review comment,
architectural inconvenience, or "make CI green" request is not enough.

Read the project's amendment protocol and required steward/reviewer ownership. Record the request
verbatim and distinguish:

- authority to prepare a candidate;
- authority to modify product code for migration;
- authority to change a baseline; and
- authority to accept, commit, merge, or release the candidate.

Do not infer one authority from another.

## Phase 2: Snapshot The Accepted State

Before editing:

1. Read the boundary source and generated projection.
2. Capture `list --format json` for the accepted target, rule, parameters, severity, reason, anchor,
   and observable perimeter.
3. Run `check --format json` and preserve its exit status.
4. Record relevant proof fixtures and current baseline state.
5. Identify source prose or project decisions that still carry non-enforced intent.

Build an Amendment Card:

```markdown
**Authority**: <direct request and local protocol>
**Accepted boundary**: <target, rule, parameters, severity, reason>
**Current observation**: <what reacts and what does not>
**Requested delta**: <exact change>
**Class**: TIGHTEN | LOOSEN | RETARGET | REASON | REMOVE
**Lost observation**: <none or facts no longer governed>
**Migration scope**: <product/test files or none>
**Baseline scope**: <unchanged or separately authorized>
**Acceptance owner**: <human/steward>
```

Do not continue until one exact class and delta are stated.

## Phase 3: Check Observability And Conflicts

Use `amendment-classification.md`.

- Every new or retained reason clause must stay inside the amended boundary's real observation.
- A loosen or removal must state the observation intentionally lost.
- A retarget must state what happens to both the old and new target.
- A reason correction must not smuggle in a rule, parameter, or perimeter change.
- A requested amendment that conflicts with another accepted boundary stops for a human decision.

Decline prose-only preferences and unobservable additions. Route missing Tianheng capability to
documented capability pressure rather than pretending a reason enforces it.

## Phase 4: Design The Proof Before The Diff

Use `proof-matrix.md` to name exact before and after outcomes.

At minimum:

- preserve a before-state projection and reaction;
- choose a witness whose outcome must change;
- choose a precision witness whose outcome must remain stable;
- predict both outcomes under accepted and amended law; and
- name repository-wide gates and projection freshness checks.

For loosening and removal, the same previously forbidden witness must become clean after amendment,
and an adjacent still-forbidden witness must continue to react when any perimeter remains. For
tightening, a newly forbidden witness must change from clean to enforced.

Do not edit until the proof would distinguish the intended amendment from an accidentally inert or
overbroad law.

## Phase 5: Write The Amendment Candidate

Follow repository-native law and test patterns:

1. Change only the boundary surface named in the Amendment Card.
2. Keep unrelated boundaries byte-for-byte unchanged.
3. Draft reasons in forward voice and within the observable perimeter.
4. Add or update focused reaction fixtures for the proof matrix.
5. Sequence required product migration according to `migration-and-projection.md`.
6. Regenerate projections through the declared command; never hand-edit their body.
7. Change a baseline only when the request separately and explicitly authorizes that baseline
   transition.

Label the result `AmendmentCandidate`, not accepted law.

## Phase 6: Prove The Reaction Delta

Run the before/after matrix and verify:

- the intended witness changes outcome in the declared direction;
- precision witnesses retain their predicted outcomes;
- `check` exit `2` never counts as proof;
- warnings and baselines are reported distinctly from enforced outcomes;
- the generated projection exactly reflects the candidate source;
- unrelated boundary projections and reactions remain stable; and
- repository format, lint, test, and governance gates pass.

If the candidate passes only by weakening more law than requested, restore the accepted state and
stop. If Tianheng cannot express the requested delta, report capability pressure.

After proof, label the result `VerifiedAmendmentCandidate`.

## Phase 7: Report For Human Acceptance

Return:

```markdown
## Verified Amendment Candidate

**Explicit authority**: <request>
**Accepted boundary**: <before>
**Amendment**: <after and class>
**Observation gained/lost**: <facts>
**Migration**: <product/baseline changes and authority>
**Reaction delta**: <before/after witness outcomes>
**Precision proof**: <stable adjacent outcomes>
**Projection**: <fresh>
**Changed files**: <paths>
**Verification**: <commands>
**Authority**: Awaiting required human/steward review; not yet accepted law.
```

When stopped, report `AUTHORITY_REQUIRED`, `BOUNDARY_NOT_FOUND`, `ROUTE_FORGE`,
`ROUTE_REPAIR`, `COMPATIBILITY_REQUIRED`, `CONFLICTING_LAW`, or `CAPABILITY_PRESSURE`.

## Hard Stops

- Do not amend law without an explicit request naming the accepted boundary or exact policy delta.
- Do not treat permission to prepare a candidate as permission to accept, commit, or merge it.
- Do not combine unrelated boundary changes into one amendment.
- Do not hide a loosen or removal behind a reason-only edit.
- Do not add baseline entries without separate explicit authority.
- Do not hand-edit generated projection text.
- Do not claim a new reason beyond the amended observation perimeter.
- Do not count exit `2`, compilation alone, or a single green check as amendment proof.
