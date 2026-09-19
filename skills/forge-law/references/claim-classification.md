# Claim Classification

Classify before selecting a Tianheng recipe. One paragraph may contain several classes.

| Class | Test | Destination |
|---|---|---|
| Structural | Names code shape that a concrete source can observe | Candidate Tianheng boundary |
| Process | Says how people or agents work, review, release, or approve | `AGENTS.md` or contribution process |
| Judgment | Requires taste or qualitative evaluation | Human review guidance |
| History | Explains why a past decision was made | Project decisions or commit provenance |
| API explanation | Explains behavior or usage to a consumer | Rustdoc or product documentation |

## Authority Evidence

Admit a claim only when at least one source explicitly states it:

- the user's current instruction;
- a project contract or architecture document;
- an agent/contributor guide;
- normative code documentation; or
- an accepted law under an explicit amendment request.

File layout, crate naming, common practice, and an agent's preferred architecture are not evidence.

## Classification Tests

Ask:

1. What exact subject must retain what exact shape?
2. Who declared that shape?
3. What observable event would contradict it?
4. Does Tianheng currently observe that event?
5. Would a clean result mean the prose claim holds, or only a narrower fact?

If question 2 has no answer, decline policy invention. If question 4 has no answer, keep the claim
documented or record capability pressure. If question 5 reveals a narrower perimeter, narrow the
candidate reason and preserve the uncovered prose.

## Examples

| Claim | Classification |
|---|---|
| "`domain` declares dependencies only on `ports`" | Structural: Cargo manifest dependency |
| "Only maintainers approve law amendments" | Process |
| "Keep this module easy to understand" | Judgment |
| "We split this crate after the 0.2 incident" | History |
| "Call `run` with process arguments" | API explanation |
| "The whole polyglot system depends inward" | Too broad until decomposed into observable parts |
