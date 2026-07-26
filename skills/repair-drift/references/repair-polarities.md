# Repair Polarities

Polarity narrows the repair direction; the accepted `reason` remains authoritative.

## `deny_breach`

The observed fact is prohibited. Prefer:

- removing the dependency, import, exposure, marker, unsafe use, async surface, or runtime breach;
- relocating the behavior behind an already-allowed boundary;
- replacing the forbidden mechanism with a repository-native permitted one; or
- encapsulating the fact so the governed surface no longer exposes it.

Do not disguise the same fact through aliases, re-exports, textual indirection, or scanner gaps.

## `allowlist_gap`

The observed fact sits outside an allowed set. Prefer:

- moving it into an allowed crate or module;
- reversing the dependency so the governed component still depends inward;
- routing through an existing permitted interface; or
- extracting a minimal interface at the already-accepted boundary when no such interface exists.

Never widen the allowlist as an automatic repair. That changes law.

## Null Polarity

Runtime audit coverage may have no deny/allowlist polarity:

- declared seam without probe: add or restore the matching product probe;
- probe of undeclared seam: correct or remove the orphan probe;
- duplicate seam: consolidate to one declared identity;
- unauditable probe: make the existing seam literal and observable where behavior permits.

Do not add, remove, or rename an accepted declared seam in this workflow.

## Multiple Violations

Start with the change most likely to remove a shared cause:

1. wrong dependency direction;
2. misplaced ownership or implementation;
3. exposed semantic shape;
4. individual imports, markers, or probes.

Rerun after each coherent increment instead of mechanically editing every reported line.
