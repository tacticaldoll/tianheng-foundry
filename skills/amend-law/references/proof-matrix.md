# Amendment Proof Matrix

Design witnesses before editing.

| Class | Changed witness | Precision witness |
|---|---|---|
| `TIGHTEN` | Clean before, enforced after | Still-allowed neighbor remains clean |
| `LOOSEN` | Enforced before, clean after | Still-forbidden neighbor remains enforced |
| `RETARGET` | New target reacts after | Old target outcome matches declared retirement or replacement |
| `REASON` | Reaction identity/outcome unchanged | Projection contains only the corrected bounded reason |
| `REMOVE` | Enforced before, clean after | Unrelated boundary remains enforced on its own witness |

## Evidence

Capture for both accepted and candidate states:

- law projection for affected and adjacent boundaries;
- exact witness source;
- JSON outcome and process exit status;
- violation identity (`target`, `rule_key`, `fact`) when available;
- severity and baseline state; and
- projection freshness result.

Exit `2` is invalid evidence. A warn-only or baselined result is not equivalent to an enforced
result. Compilation proves API validity, not reaction semantics.

## Preventing Inert Amendments

A green workspace alone cannot prove a tightened rule bites. A failing workspace alone cannot
prove a loosen is precise. The matrix must contain both the outcome intended to change and one
outcome intended to stay stable.

For a removal with no remaining perimeter, use an unrelated accepted boundary as the stability
witness and state that no adjacent protection remains.
