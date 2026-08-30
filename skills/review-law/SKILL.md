---
name: review-law
description: Use when a diff, branch, patch, or working tree adds or changes Tianheng Constitution boundaries, reasons, baselines, proof fixtures, or generated projections and needs adversarial review before human acceptance; verifies intent authority, observability, reaction evidence, minimality, amendment scope, compatibility, and projection freshness, then returns findings-first ACCEPT_CANDIDATE, REVISE, or REJECT without editing. Do not use to create or repair law, review product-code-only changes, accept policy on a human's behalf, or perform a general Rust code review.
---

# Review Tianheng Law

Review a candidate as an adversarial acceptance gate. This workflow is read-only: identify what the
candidate proves and where it fails, but do not repair the diff or grant authority.

## Load References Deliberately

- Read [review-gates.md](references/review-gates.md) before evaluating the candidate.
- Read [evidence-audit.md](references/evidence-audit.md) when inspecting reaction claims.
- Read [minimality-and-overlap.md](references/minimality-and-overlap.md) for redundant or diluted
  reactions.
- Read [verdict-contract.md](references/verdict-contract.md) before assigning severity or verdict.

These references target Tianheng `0.5.x`. Inspect the candidate's actual dependency and project
review policy when compatibility or authority differs.

## Phase 0: Resolve The Review Scope

Resolve the user-provided diff, commit, branch, patch, or working tree without modifying it. Include:

- accepted and candidate Constitution source;
- all changed targets, rules, parameters, depths, severities, reasons, and anchors;
- proof fixtures and recorded commands;
- baseline changes;
- generated projection changes;
- source prose disposition; and
- manifest or Tianheng-version changes.

Compare against the actual accepted base. Do not review only the new file when an amendment's risk
is the semantic delta from existing law.

If there is no law candidate, stop as `OUT_OF_SCOPE`. Route product-only violations to
`repair-drift` and general code quality to the host's normal review workflow.

## Phase 1: Classify The Candidate

Classify every changed boundary:

- `FORMATION`: new candidate from declared prose;
- `AMENDMENT`: target, rule, parameter, depth, severity, reason, or removal changes accepted law;
- `BASELINE`: gating identity or accepted-current-fact state changes;
- `PROJECTION`: generated context changes with no intended source-law delta.

One diff may contain several classes. A change presented as reason-only is still an amendment.
Severity reduction, allowlist growth, scan-depth reduction, baseline acquisition, and boundary
removal are policy changes even when mechanically small.

## Phase 2: Run Sequential Review Gates

Apply `review-gates.md` in order. Stop trusting downstream evidence after a gate invalidates its
premise, but continue inspecting enough to report independent findings.

### Gate 1: Authority

Find the exact declared intent for formation, explicit request and local protocol for amendment,
and separate authority for baseline changes. Repository shape, generic architecture practice,
green-CI pressure, and the candidate author's inference are not authority.

### Gate 2: Observability

Map every normative clause to target, observation source, rule, parameters, and scan depth. Each
reason clause must remain inside what the candidate reaction can observe. Identify important facts
the prose or name suggests but the boundary does not see.

### Gate 3: Reaction Evidence

Use `evidence-audit.md`. Verify violating and precision directions from actual commands, outcomes,
and identities. For amendment, verify the before/after direction appropriate to tighten, loosen,
retarget, reason correction, or removal.

### Gate 4: Minimality And Integrity

Use `minimality-and-overlap.md`. Look for redundant reactions, diluted severity, opportunistic
baselines, inert targets, overbroad scan, duplicate law sources, and unrelated policy bundled into
the candidate.

### Gate 5: Projection, Prose, And Compatibility

Confirm generated projection came from the declared command and is fresh. Check that source prose
was preserved, narrowed, or removed according to what reaction now covers. Verify the Tianheng
version and referenced public API against the declared support range.

## Phase 3: Verify Claims Without Repairing

Run repository-native read/check/test commands when available and safe. Preserve exit status and
structured output. Tests may produce ordinary build artifacts; do not edit source, regenerate
projection, rewrite baselines, or update lockfiles as part of review.

When evidence is missing, report the missing proof and exact verification needed. Do not create the
fixture yourself, because doing so would collapse reviewer independence into implementation.

## Phase 4: Report Findings First

Order findings by severity, then by gate:

```markdown
## Findings

### [REJECT|REVISE] <concise title>
**Location**: <path:line or candidate surface>
**Gate**: <authority | observability | reaction | minimality | projection | compatibility>
**Evidence**: <what the diff/report actually shows>
**Impact**: <policy or reaction failure>
**Required disposition**: <redesign, explicit authority, or specific missing proof>
```

Do not bury a blocking finding under a summary. Distinguish observed evidence from inference and
state when a source or command was unavailable.

## Phase 5: Assign One Verdict

Use `verdict-contract.md`:

- `REJECT`: authority is invented/missing for a policy change, the claim is not observable, an
  amendment is silent, or the candidate's basic policy/reaction shape requires redesign.
- `REVISE`: the shape may be valid but proof, precision, minimality, projection freshness, prose
  disposition, or compatibility evidence is incomplete.
- `ACCEPT_CANDIDATE`: no blocking findings remain and every gate has concrete evidence.

Return:

```markdown
## Review Verdict

**Verdict**: ACCEPT_CANDIDATE | REVISE | REJECT
**Candidate class**: <FORMATION | AMENDMENT | BASELINE | PROJECTION>
**Authority evidence**: <source>
**Observation perimeter**: <observed and unobserved>
**Reaction evidence**: <commands and both directions>
**Minimality**: <result>
**Projection / prose**: <result>
**Compatibility**: <result>
**Residual risk**: <untested or judgment-dependent risk>
**Acceptance authority**: Human/steward review remains required.
```

If there are no findings, say so explicitly before the verdict and name residual test gaps.

## Hard Stops

- Do not edit candidate, product, law, baseline, projection, or test files.
- Do not infer policy authority from a passing test or clean CI.
- Do not accept warn-only, baselined, exit `2`, compilation, or projection as violating proof.
- Do not approve a reason that claims facts outside the reaction perimeter.
- Do not treat redundant reactions as harmless documentation.
- Do not let a reason-only label hide a semantic amendment.
- Do not call a candidate accepted law or perform commit/merge/approval actions.
- Do not soften findings because the candidate is nearly complete or expensive to revise.
