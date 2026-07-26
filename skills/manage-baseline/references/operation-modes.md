# Baseline Operation Modes

## `ADOPT`

Use for an existing dirty codebase that wants enforced law to reject future acquisitions now.
Review every current identity and obtain explicit debt authority before writing.

## `REFRESH`

Use when current and previous identity sets differ. Retained and stale entries may proceed under
refresh authority; each added identity requires separate acquisition authority. A blanket refresh
after CI failure is forbidden.

## `PRUNE`

Use when stale entries should be removed and `added` is empty. Rewriting through Tianheng produces
the current set and preserves annotations. With additions present, stop and split repair or
authorized refresh from pruning.

## `ANNOTATE`

Use to change only `owner` and `tracker` on existing structured entries. Parse and serialize JSON;
the identity set and semantic format must remain byte-semantically equivalent.

## `RETIRE`

Use when no current enforce debt depends on the baseline. Remove the file and CI baseline flags
together, then prove ordinary check behavior stays clean and a violating fixture still fails.

## Format Migration

Unsupported baseline formats are compatibility work, not refresh. Tianheng intentionally refuses
to overwrite them. Preserve annotations externally, remove/move old data only with explicit
authority, generate a fresh structured snapshot, and review every new identity.
