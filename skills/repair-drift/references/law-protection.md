# Law Protection

Freeze every authority-bearing or reaction-configuring surface before repair:

- Rust `Constitution` declarations and their `.because(...)` reasons;
- boundary targets, rules, parameters, scan depths, and severities;
- baseline files and baseline-writing commands;
- generated law projections;
- runner wiring and governance configuration.

Changing any frozen surface is an amendment, not drift repair.

## Common Evasions

Reject these even when they make CI green:

- changing `.enforce()` to `.warn()`;
- adding the finding to a baseline;
- broadening `restrict_*_to` or another allowlist;
- removing a rule that overlaps another;
- reducing scan depth or disabling semantic/runtime observation;
- editing a generated projection instead of its source;
- excluding the offending workspace member or file;
- changing a reason so the existing code appears compliant.

## Rationalization Check

| Temptation | What It Actually Means |
|---|---|
| "Widening this allowlist is the smallest diff." | The diff is small because it changes authority instead of repairing architecture. |
| "The boundary looks wrong." | That may justify an amendment proposal, never an implicit amendment. |
| "Baselines are a supported Tianheng feature." | They govern adoption and gating; adding one is not product-code repair. |
| "The generated projection will be regenerated later." | Hand editing it creates a knowingly stale projection now. |
| "The user only asked to make CI green." | Green-CI authority does not imply permission to rewrite accepted law. |
| "Another boundary still catches most cases." | Partial overlap does not authorize removing or weakening this boundary. |

Any thought that the law is too strict, inconvenient, redundant, or probably unintended is a
red flag to stop product repair and surface the architectural decision. Preserve the spirit and the
letter: a mechanically different edit that makes the same forbidden fact invisible is still
evasion.

## Amendment Boundary

An explicit request to amend law routes out of `repair-drift`; it does not allow this skill to mix
product repair and legislation in one transaction. Report:

- the accepted reason and boundary;
- why product-only repair is impossible or undesirable;
- the exact law surface that would need deliberate review; and
- any conflict with other accepted boundaries.

A vague request such as "fix CI", "make it pass", or "update whatever is needed" is not explicit
amendment authority.
