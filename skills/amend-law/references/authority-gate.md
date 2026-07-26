# Amendment Authority Gate

Accepted law changes only through explicit, scoped intent.

## Sufficient Candidate Authority

- A direct user request naming the boundary or exact policy delta.
- A project-approved change record that explicitly authorizes the same delta and whose workflow
  permits the agent to prepare it.
- A steward instruction within the steward's declared ownership.

This authorizes preparation of an amendment candidate only.

## Insufficient Authority

- A failing Tianheng check or CI job.
- A request to repair product code or "make it pass."
- An agent's belief that the boundary is obsolete, redundant, too strict, or badly written.
- Repository shape, a refactor plan, a dependency upgrade, or generic Rust practice.
- Permission to edit code generally.
- An issue or review comment that discusses the boundary without authorizing its change.

## Separate Authorities

Record these independently:

| Action | Required authority |
|---|---|
| Prepare law diff | Explicit amendment request |
| Migrate product code | User request or normal task scope |
| Add/change baseline | Explicit baseline decision |
| Remove source prose | Explicit replacement scope plus complete reaction proof |
| Commit/merge/release | Repository workflow and direct user authority |

## Conflict

When direct instruction and durable project governance disagree, stop and surface both. Do not
choose the more convenient authority. When ownership or acceptance is unclear, prepare no law diff.
