# Amendment Classification

Classify by reaction semantics, not diff size.

| Class | Meaning | Required disclosure |
|---|---|---|
| `TIGHTEN` | More facts become forbidden or newly enforced | Newly observed/prohibited facts |
| `LOOSEN` | Fewer facts fail, severity drops, or perimeter narrows | Observation intentionally lost |
| `RETARGET` | Governed crate, module, type, seam, or rule identity changes | Old and new target coverage |
| `REASON` | Forward explanation changes without reaction semantics changing | Why the new text stays within the same perimeter |
| `REMOVE` | Boundary ceases to govern | Entire observation and context being retired |

Parameter, allowlist, scan-depth, severity, and baseline changes are never "just configuration."
Classify them by their effect.

## Mixed Deltas

A change that both retargets and loosens is not reason-only. Choose the dominant risk class and list
every secondary effect. Split unrelated policy changes into separate candidates.

## Observability Test

For every clause in the proposed reason, answer:

1. Which Tianheng observation produces the fact?
2. Which target and rule react?
3. Which witness demonstrates it?
4. What nearby fact remains outside observation?

If any clause has no answer, narrow the reason or route that clause to prose/capability pressure.

## Removal Test

Removal requires explicit retirement of the governed intent. Redundancy is not enough unless the
remaining boundary reacts to the same target, facts, severity, and reason perimeter. Record what
agents will no longer see in generated context.
