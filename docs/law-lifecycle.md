# Law And Context Lifecycle

```text
ProseClaim
    |
    | classify authority and claim
    v
AdmittedIntent ---- unobservable ----> CapabilityPressure
    |                                      |
    |                                      | shape observation contract
    |                                      v
    |                          +-----------+-----------+
    |                          |                       |
    |                   UpstreamCandidate      AdopterObservation
    |
    | select observation and recipe
    v
BoundaryCandidate
    |
    | violating proof + clean proof + fresh projection
    v
VerifiedCandidate
    |
    | adversarial candidate review
    v
ReviewedCandidate
    |
    | human acceptance only
    v
AcceptedLaw ---- deterministic projection ----> GeneratedContext
    |                                               |
    |                                      task-local activation
    |                                               v
    |                                           AgentChange
    |                                               |
    | evaluate future code                          |
    +--------------------> Reaction <---------------+
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
| `CapabilityPressure` | Authorized structural intent lacks a supported observer | No adopter law |
| `UpstreamCandidate` | A general capability's contract and fixture matrix are reviewable | No; Tianheng-owned |
| `AdopterObservation` | The gap is the adopter's own house rule, and its contract is theirs to implement as an `Observer` | No; adopter-owned |
| `BoundaryCandidate` | Generated boundary and reason, not yet proven | Candidate work only |
| `VerifiedCandidate` | Teeth, precision, freshness, and compatibility are proven | Yes, still unaccepted |
| `ReviewedCandidate` | Adversarial gates found no blocking defect | No; awaiting human acceptance |
| `AcceptedLaw` | Human-reviewed constitution code | No silent changes |
| `GeneratedContext` | Tianheng projection of accepted law | Never hand-edit |

Repository shape and generic best practice can inform investigation, but they do not promote a
claim into `AdmittedIntent`.

## Formation

Formation is the judgment-heavy loop owned by `forge-law`: eligibility, claim classification,
observation admission, recipe selection, controlled generation, and proof. A successful run stops
at `VerifiedCandidate`; `review-law` may reject, revise, or mark it `ReviewedCandidate`, while human
review alone performs the authority transition.

## Operation

Tianheng deterministically projects accepted Rust law into agent-readable context and evaluates the
workspace. `activate-law` selects relevant projected boundaries into task-local context without
rewriting them; activation is orientation, and the later Tianheng reaction remains binding. Skills
consume projection and reaction rather than wrapping or imitating either.

## Evolution

A violation normally directs repair toward the accepted reason. Changing a target, rule,
parameter, scan depth, severity, or reason is an amendment and requires an explicit request.

A claim Tianheng cannot observe becomes `CapabilityPressure`: evidence for a possible observation,
not a pretend boundary. `shape-capability` shapes that pressure into a contract and names its owner.

A general capability a dimension should hold becomes an `UpstreamCandidate`, and the adopter claim
remains prose until Tianheng accepts and implements a real observation. An adopter's own house rule
becomes an `AdopterObservation`: from Tianheng `0.5.0` an `Observer` outside the family can join a
run, so the adopter can own the reaction rather than wait for one. Ownership is the only thing that
differs — the named source, the perimeter, the declared bounds, and both proofs are required of
either, and neither is written by this collection.

## Baseline Debt

Baseline is a parallel gate-state lifecycle, not an authority state of law:

```text
ObservedDrift
    |
    | explicit debt adoption
    v
BaselinedDebt -- product repair --> StaleEntry -- rewrite --> PrunedDebt
    |                                                   |
    +---------------- all debt repaired ----------------+
                                                        v
                                                     Retired
```

`manage-baseline` compares structured identity sets before every write. Added identities require
new debt authority; stale identities may be pruned; retirement requires no current enforce debt.
Throughout the lifecycle, accepted law and observation remain unchanged.

## Prose Disposition

Prose may be removed or narrowed only after its complete enforceable meaning exists in accepted
law, the reaction has teeth and precision, and the generated projection carries the needed agent
context. Historical rationale stays in project history; procedural guidance stays in operating
docs; subjective guidance stays prose.

## Skill Admission

Name another skill only when one lifecycle transition has an independent trigger, output, and
failure mode. Deterministic projection and evaluation remain Tianheng responsibilities.
