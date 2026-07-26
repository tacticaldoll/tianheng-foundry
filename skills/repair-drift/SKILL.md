---
name: repair-drift
description: Use when an agent has a Tianheng check violation or reported Tianheng warning/baselined finding in a Rust workspace and needs to repair product code toward the accepted boundary reason; reads the structured reaction, freezes the constitution, makes the smallest code repair, and reruns the reaction without weakening law. Do not use to create a new boundary, amend a Constitution, handle exit-class 2 configuration or scan failures as drift, or fix unrelated Rust diagnostics.
---

# Repair Tianheng Drift

Restore product code to an accepted Tianheng law after the law reacts. Treat the boundary and its
reason as fixed authority throughout this workflow.

## Load References Deliberately

- Read [reaction-contract.md](references/reaction-contract.md) before classifying a captured check.
- Read [repair-polarities.md](references/repair-polarities.md) when choosing a code repair.
- Read [law-protection.md](references/law-protection.md) before touching any file that may contain
  law, baseline, projection, or governance configuration.
- Read [verification.md](references/verification.md) before claiming the drift is repaired.

These references describe the supported Tianheng `0.3.x` reaction contract. Inspect the adopter's
actual dependency and runner when exact invocation details differ.

## Phase 0: Establish The Reaction

Work only inside a discovered Cargo workspace that already uses Tianheng. Find the project's
declared check runner and preserve its real exit status when capturing JSON:

```bash
status=0
report=$(<project-check-command> --format json) || status=$?
```

Do not infer a Tianheng violation from a compiler error, test failure, stale prose, or repository
shape. Prefer the report from the user's failing invocation; reproduce it before editing when the
checkout is available.

Classify the result:

- exit `1` with violations: continue;
- exit `0` with no reported violations: stop, because there is no observed drift;
- exit `0` with warn or baselined violations: report them, and edit only when the user directly
  asked to repair advisory or legacy drift;
- exit `2`, malformed JSON, or an exit/report mismatch: stop as a constitution, scan, usage, or
  harness problem. Do not repair product architecture from an invalid reaction.

## Phase 1: Freeze Accepted Law

Locate the constitution source, optional baseline, generated projection, and the command that
produced the report. Mark all of them read-only for this transaction.

Read the declared law with the project's runner, normally `list --format json` or
`list --format markdown`. Confirm that each reported `(target, rule)` exists and read its `reason`
before inspecting the mechanical finding.

If satisfying the user request requires changing a boundary's target, rule, parameters, scan depth,
severity, reason, or baseline, stop and route to deliberate amendment. Even a direct request to
"make CI green" is not amendment authority.

## Phase 2: Build Repair Cards

Group violations by `(target, rule)` so one boundary's reason governs all of its findings. Build one
card per group:

```markdown
**Reason**: <accepted forward reason>
**Target / rule**: <governed target and rule>
**Findings**: <facts reported by Tianheng>
**Files**: <reported actionable files, preserving null faithfully>
**Polarity**: <deny_breach | allowlist_gap | null>
**Severity / baseline**: <enforce or warn; current or baselined>
**Code repair direction**: <remove, relocate, invert, encapsulate, or restore probe coverage>
**Frozen authority files**: <constitution, baseline, projection, configuration>
```

Never invent a file when the report carries `null`. Trace graph edges, seams, and declarations from
the finding and target instead.

## Phase 3: Choose A Product-Code Repair

Use `repair-polarities.md`.

- For `deny_breach`, remove, relocate, or replace the prohibited occurrence.
- For `allowlist_gap`, move the occurrence into an allowed location, invert the dependency, or
  introduce an already-supported inward-facing abstraction. Do not widen the allowlist.
- For runtime audit findings with null polarity, align product probes and declared seams without
  changing the accepted seam set.

Prefer the smallest repair that makes the whole reason true, not merely a textual edit that hides
one finding. Follow existing repository boundaries and abstractions; do not introduce a new layer
unless the repair actually requires one.

For multiple groups, repair likely upstream causes first and rerun the reaction after each coherent
increment. One dependency inversion may remove several downstream findings.

## Phase 4: Edit Within The Frozen Set

Before editing, record:

- product and test files allowed to change;
- authority files that must remain byte-for-byte unchanged;
- focused checks for the affected behavior;
- the exact Tianheng reaction command; and
- repository-wide completion gates.

Make the product-code repair and its necessary tests. Do not edit generated projection text by
hand, add a baseline entry, change severity to warn, reduce scan depth, remove a boundary, broaden
an allowed set, or bypass the project runner.

If the only plausible repair violates another accepted boundary, stop with the conflicting reasons
and request a deliberate architectural decision. Do not choose which law loses.

## Phase 5: Verify The Reaction

Follow `verification.md`:

1. Run focused tests for the changed behavior.
2. Rerun the same Tianheng command and capture both JSON and exit status.
3. Confirm the targeted finding identities disappeared for the intended code reason.
4. Inspect all remaining warnings, baselined findings, stale baseline entries, and coverage data.
5. Run the adopter repository's normal format, lint, test, and governance gates.
6. Prove frozen authority files did not change.

Exit `0` proves only that no unbaselined enforce violation remains. It does not erase advisory,
baselined, or uncovered facts; report those explicitly.

## Phase 6: Report The Repair

Return:

```markdown
## Drift Repair

**Accepted reason**: <reason>
**Violation identity**: <target, rule, findings>
**Product repair**: <what changed and why it restores the reason>
**Changed files**: <product/test paths>
**Frozen law**: <constitution/baseline/projection unchanged>
**Reaction**: <command and resulting exit class>
**Remaining advisory state**: <none | warnings | baselined | uncovered>
**Verification**: <focused and repository gates>
```

When stopped, name the exact outcome: `NO_DRIFT`, `REACTION_ERROR`, `AMENDMENT_REQUIRED`,
`CONFLICTING_LAW`, or `UNREPAIRABLE_WITH_CURRENT_STRUCTURE`.

## Hard Stops

- Do not use this skill without an actual Tianheng reaction.
- Do not treat exit `2` as architecture drift.
- Do not change accepted law, baselines, projections, or governance configuration.
- Do not widen an allowlist or lower severity as a repair.
- Do not fabricate a source location absent from the report.
- Do not claim clean merely from exit `0` without inspecting advisory and baseline state.
- Do not repair outside the Cargo workspace in a mixed-language repository.
- Do not commit or merge unless the user requested those repository actions.
