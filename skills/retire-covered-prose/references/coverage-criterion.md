# Coverage Criterion

A comment is retired only when accepted law **holds its whole claim with teeth**. Three conditions,
all required:

1. **Whole claim.** Every structural fact the sentence asserts lies inside one boundary's observed
   perimeter. A claim split across two boundaries is held only if together they observe all of it,
   and each part is cited.
2. **Enforced.** The holding boundary's severity is enforcing. A `warn` boundary reports and
   proceeds; deleting a comment it merely warns about converts a stated intention into nothing.
3. **Unbaselined.** No violation of the holding boundary sits in a baseline. A baselined finding is
   accepted-current debt, so at this moment the boundary is not holding the claim against the code
   in front of it.

## Findings

| Finding | Condition | Disposition |
|---|---|---|
| `HELD` | Whole claim, enforced, unbaselined | Retire |
| `WIDER` | The claim asserts more than any perimeter observes | Retain, route to `amend-law` |
| `TOOTHLESS` | Perimeter matches, severity is `warn` | Retain, route to `amend-law` |
| `ABSORBED` | Perimeter matches, a violation is baselined | Retain, route to `manage-baseline` |
| `UNGOVERNED` | No perimeter observes the claim, Tianheng could | Retain, route to `forge-law` |
| `UNOBSERVABLE` | No perimeter observes the claim, Tianheng cannot | Retain, route to `shape-capability` |

## The Wider Test

The failure this criterion exists to prevent is **silently narrowing intent the project already
declared**. It happens when a sentence says more than the reaction sees, and the sentence is the
only place the surplus was ever written.

Worked case. The comment says *domain never touches infra, by any route*. The boundary is
`ModuleBoundary::in_crate("app").module("crate::domain").must_not_import("crate::infra")`, whose
perimeter observes source `use` edges at the declared depth and **declares** that it does not
observe a fully-qualified call written inline, a macro-generated import, or a re-export path. So the
sentence asserts a reachability claim and the boundary observes an import claim. The finding is
`WIDER`: delete the comment and the project has quietly stopped claiming the stronger thing.

The same case shows what silence does. That perimeter says nothing at all about a call reached
through a trait object — it neither claims nor disclaims it. **Silence is not a declared
non-observation, and it is not coverage either.** A shape the perimeter does not mention is surplus
the sentence still asserts, so it drives the finding to `WIDER` exactly as a declared
non-observation does. Never fill a silence by reading the implementation; that is a perimeter you
assembled, and `perimeter-source.md` excludes it.

The test is not "does the reason sound like the comment". Two sentences can agree completely and
still fail, because a reason is also prose and is bounded to what its own reaction observes.
Compare the claim to the **perimeter**, which is read as `perimeter-source.md` describes.

## Uncertainty

When it is unclear whether the perimeter covers the whole claim, the finding is `WIDER`.

This is deliberately asymmetric. A wrong `WIDER` leaves a comment in the tree, which a later sweep
or a human corrects at no cost. A wrong `HELD` deletes the last written record of a claim, and
nothing downstream will report its absence — no check fails, no reaction fires, and the diff looks
like tidying.

## Rationalization Check

| Temptation | What It Actually Means |
|---|---|
| "The boundary's reason says almost the same thing." | The reason is prose too. Two bounded sentences agreeing does not widen either perimeter. |
| "The comment is vague, so the boundary must cover it." | A vague claim has an unbounded surplus. Vagueness argues for `WIDER`, not for `HELD`. |
| "It is only a `warn` for now, the intent is clearly there." | Intent with no reaction is exactly the prose this comment was carrying. Deleting it removes the last thing carrying it. |
| "The violation is baselined, so the team already accepted it." | They accepted the debt, not the removal of the claim. The baseline is the record that the claim is currently unmet. |
| "Every other comment in this file went, so this one is inconsistent." | Consistency of comment density is a style goal. This skill has no style goal. |
| "I can narrow the sentence to the part that is covered." | A narrowed sentence has no proof that it still says the right thing. Retain and route instead. |
| "The sweep was authorized, so the deletions are authorized." | The criterion was authorized. The set is computed here and was not visible when the request was made. |
| "The user's real goal is fewer comments; my criterion just makes it safe." | Fewer comments as a goal has no criterion at all. Borrowing this criterion to serve it produces deletions nobody can audit. |
| "Refusing the style mandate and then running the covered-only sweep in the same reply is helpful." | The refusal was the answer. Running it unasked is the style sweep, performed once the objection is on record. |
| "They will ask again with better wording, so I may as well proceed." | Then it will be asked for the operation this skill performs, and answered. Predicting a request is not receiving one. |
