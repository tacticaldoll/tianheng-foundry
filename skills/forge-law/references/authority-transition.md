# Authority Transition

The workflow changes representation before it changes authority.

```text
ProseClaim
  -> AdmittedIntent
  -> BoundaryCandidate
  -> VerifiedCandidate
  -> AcceptedLaw
  -> GeneratedProjection
```

| State | Meaning | Who may advance it |
|---|---|---|
| ProseClaim | Evidence that a constraint may be intended | Project author or direct user |
| AdmittedIntent | Claim mapped to an honest observation perimeter | Skill analysis |
| BoundaryCandidate | Rust law and proof edits exist | Skill execution |
| VerifiedCandidate | Violating and clean proofs pass | Deterministic checks |
| AcceptedLaw | Project recognizes the Constitution change as binding | Human review/merge |
| GeneratedProjection | Readable context derived from accepted code | Tianheng renderer + freshness test |

Tests prove behavior; they do not grant policy authority.

## Prose Disposition

| Prose content | After a verified candidate |
|---|---|
| Fully duplicated live structural claim | Preserve by default; candidate removal is allowed only in an explicit replacement diff |
| Structural claim broader than observation | Narrow prose to the ungoverned remainder |
| Historical rationale | Keep in project decisions or commit provenance |
| Process or approval rule | Keep in contributor/agent governance |
| Judgment guidance | Keep for human review |
| API explanation | Keep in product docs or rustdoc |
| Generated projection body | Never hand-edit; regenerate from Constitution |

## Accepted Law

Changing target, rule, parameters, depth, severity, or reason of an accepted boundary may be an
amendment. Require explicit user intent and inspect the project's amendment/review policy.

Never treat an unrelated feature request, a failing build, or a desire for a green check as
authority to weaken or remove the law.
