---
name: manage-baseline
description: Use when a Tianheng-governed Rust workspace needs an explicitly authorized baseline adoption, refresh, stale-entry prune, annotation update, or retirement; compares structured violation identities before writing, prevents new drift from being silently absorbed, preserves owner/tracker metadata, and verifies gate and stale behavior without changing accepted law. Do not use to repair product drift, weaken or amend a Constitution, automatically rebaseline CI failures, handle unsupported baseline formats as if compatible, or create baseline debt without explicit human authority.
---

# Manage Tianheng Baseline

Manage accepted-current drift as a ratchet. A baseline changes which observed identities fail the
gate; it never changes what the Constitution declares or what Tianheng observes.

## Load References Deliberately

- Read [baseline-contract.md](references/baseline-contract.md) before inspecting or writing a file.
- Read [identity-diff.md](references/identity-diff.md) before authorizing any rewrite.
- Read [operation-modes.md](references/operation-modes.md) to classify adoption, refresh, prune,
  annotation, or retirement.
- Read [verification.md](references/verification.md) before reporting completion.

These references target Tianheng `0.3.x` structured-fact baselines. Inspect the adopter's resolved
runner and format identifier before acting.

## Phase 0: Gate Baseline Authority

Require:

- a discovered Cargo workspace with accepted Tianheng law;
- a supported Tianheng version and project-native runner;
- a direct request or durable project decision authorizing the exact baseline operation; and
- the baseline path used by the project's gate.

Separate authority to:

- adopt current identities;
- acquire newly observed identities during refresh;
- change `owner` or `tracker` annotations;
- remove stale identities;
- retire the baseline and change CI wiring; and
- commit or merge the result.

General edit permission, a red CI run, or a request to "make it green" authorizes none of these.
Freeze Constitution source, reasons, severity, scan depth, generated projection, and product code.

## Phase 1: Capture Current Reaction

Run the project-native check without baseline gating and capture structured JSON plus real process
status. Exit `1` is expected when enforce violations exist; exit `2` invalidates the snapshot.

Then run gate mode against the existing baseline, when present:

```bash
status=0
report=$(<project-check> --baseline <path> --format json) || status=$?
```

Record current violations, their `baselined` flags, `stale_baseline`, and `stale_disallowed`. Do not
pipe away Tianheng's status.

Validate that an existing file declares `format: "tianheng.baseline/structured-facts"`. An
unsupported or malformed file is compatibility work; write mode intentionally exits `2` rather
than overwriting it.

## Phase 2: Diff Structured Identities

Use `identity-diff.md`. Compare sets by exactly:

```text
(target, rule_key, structured fact)
```

Compute:

- `retained = current ∩ baseline`;
- `added = current - baseline`;
- `stale = baseline - current`.

Human `rule`/`finding` wording, reason, severity, file, anchor, polarity, owner, and tracker do not
re-key an identity. Never diff by rendered messages or array position.

Present every `added` identity with its reason, finding, file, severity, owner, and tracker decision
before writing. An authorization to remove `stale` entries does not authorize any `added` entry.

## Phase 3: Classify The Operation

Use `operation-modes.md`:

- `ADOPT`: no supported baseline exists; snapshot reviewed current identities.
- `REFRESH`: rewrite retained current identities and possibly separately authorized additions.
- `PRUNE`: remove stale identities only; `added` must be empty.
- `ANNOTATE`: update `owner`/`tracker` only; identity set must remain unchanged.
- `RETIRE`: current enforce debt is empty and CI will stop passing `--baseline`.

Stop as `NEW_DRIFT` when a rewrite would acquire an unauthorized identity. Route product repair to
`repair-drift`; route law changes to `amend-law`.

## Phase 4: Prepare The Baseline Transaction

Before writing, produce:

```markdown
## Baseline Transaction

**Mode**: ADOPT | REFRESH | PRUNE | ANNOTATE | RETIRE
**Authority**: <source>
**Path / format**: <baseline path and semantic format>
**Retained identities**: <count and owners>
**Added identities**: <each identity and explicit disposition>
**Stale identities**: <each identity>
**Annotation changes**: <owner/tracker only>
**Frozen law**: <constitution/projection paths>
**CI effect**: <gate and --disallow-stale behavior>
```

Do not continue until every added identity is explicitly authorized or removed from current code.

## Phase 5: Execute Through Tianheng

For `ADOPT`, `REFRESH`, or `PRUNE`, use the project runner's `--write-baseline <path>` command.
Do not hand-edit identity fields. The supported writer preserves `owner` and `tracker` annotations
for retained identities.

For `ANNOTATE`, parse the structured JSON and change only authorized `owner`/`tracker` fields while
preserving identity and format. Use a structured JSON editor, never textual substitution.

For `RETIRE`, first prove no current enforce identity relies on the baseline, then remove the
baseline file and its CI `--baseline`/`--disallow-stale` arguments in the same candidate.

Keep a reviewable pre-write diff or git state so the candidate can be reverted. Do not invoke
write mode against an unsupported existing file.

## Phase 6: Verify The Ratchet

Follow `verification.md`:

1. Parse the written file and verify its semantic format.
2. Recompute retained, added, and stale sets.
3. Confirm no unauthorized identity was acquired.
4. Confirm retained annotations survived and authorized annotation changes are exact.
5. Run gate mode with `--baseline` and structured output.
6. Run with `--disallow-stale` when the project uses stale enforcement.
7. Demonstrate one unbaselined enforce fixture still exits `1`.
8. Confirm Constitution and projection sources remain unchanged.
9. Run repository-native format, test, and governance gates.

Exit `0` in gate mode means no unbaselined enforce finding remains; report baselined and warn
observations rather than calling the workspace architecture clean.

## Phase 7: Report

Return:

```markdown
## Baseline Result

**Mode / authority**: <operation and source>
**Identity diff**: <retained, authorized added, stale removed>
**Annotations**: <preserved/changed>
**Gate result**: <command and exit>
**Stale result**: <command and exit>
**New-drift proof**: <unbaselined fixture exits 1>
**Frozen law**: <unchanged>
**Changed files**: <baseline and CI wiring only>
**Remaining debt**: <identities with owner/tracker>
```

When stopped, report `AUTHORITY_REQUIRED`, `REACTION_ERROR`, `UNSUPPORTED_FORMAT`, `NEW_DRIFT`,
`CURRENT_DEBT_REMAINS`, or `ROUTE_REPAIR`.

## Hard Stops

- Do not baseline automatically after a failed check.
- Do not treat stale removal as authority to acquire new identities.
- Do not compare identity using diagnostic text, file, reason, or array position.
- Do not hand-edit target, rule key, structured fact, or format.
- Do not weaken Constitution law, severity, depth, or reasons.
- Do not overwrite unsupported or malformed baseline data.
- Do not retire a baseline while current enforce debt remains.
- Do not call a fully baselined workspace architecture-clean.
