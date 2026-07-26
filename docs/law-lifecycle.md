# Law And Context Lifecycle

```text
ProseClaim
    |
    | classify authority and claim
    v
AdmittedIntent ---- unobservable ----> CapabilityPressure
    |
    | select observation and recipe
    v
BoundaryCandidate
    |
    | violating proof + clean proof + fresh projection
    v
VerifiedCandidate
    |
    | human review only
    v
AcceptedLaw ---- deterministic projection ----> GeneratedContext
    |                                         |
    | evaluate future code                    | conditions agent work
    +--------------------> Reaction <---------+
                              |
                    +---------+----------+
                    |                    |
                  Repair             Amendment
```

## Authority States

| State | Meaning | May The Skill Write? |
|---|---|---|
| `ProseClaim` | A project statement or direct human instruction | No |
| `AdmittedIntent` | Structural, authorized, and potentially observable | Candidate work only |
| `BoundaryCandidate` | Generated boundary and reason, not yet proven | Candidate work only |
| `VerifiedCandidate` | Teeth, precision, freshness, and compatibility are proven | Yes, still unaccepted |
| `AcceptedLaw` | Human-reviewed constitution code | No silent changes |
| `GeneratedContext` | Tianheng projection of accepted law | Never hand-edit |

Repository shape and generic best practice can inform investigation, but they do not promote a
claim into `AdmittedIntent`.

## Formation

Formation is the judgment-heavy loop owned by `forge-law`: eligibility, claim classification,
observation admission, recipe selection, controlled generation, and proof. A successful run stops
at `VerifiedCandidate`; human review performs the authority transition.

## Operation

Tianheng deterministically projects accepted Rust law into agent-readable context and evaluates the
workspace. Skills should consume those reactions, not wrap or imitate them.

## Evolution

A violation normally directs repair toward the accepted reason. Changing a target, rule,
parameter, scan depth, severity, or reason is an amendment and requires an explicit request.

A claim Tianheng cannot observe becomes `CapabilityPressure`: evidence for a possible upstream
capability, not a pretend boundary. It remains prose until a real observation exists.

## Prose Disposition

Prose may be removed or narrowed only after its complete enforceable meaning exists in accepted
law, the reaction has teeth and precision, and the generated projection carries the needed agent
context. Historical rationale stays in project history; procedural guidance stays in operating
docs; subjective guidance stays prose.

## Skill Admission

Name another skill only when one lifecycle transition has an independent trigger, output, and
failure mode. Deterministic projection and evaluation remain Tianheng responsibilities.
