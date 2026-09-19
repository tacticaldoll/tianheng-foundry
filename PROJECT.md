# Tianheng Foundry - Project

Tianheng Foundry is a portable companion skill collection for people who use, or explicitly intend
to adopt, Tianheng in their own Rust projects.

## Status

Experimental `0.1.x`. The collection currently has eight skills: `forge-law` forms a
reaction-proven candidate from declared prose, `activate-law` selects accepted law into task-local
context, `repair-drift` restores product code after accepted law reacts, and `amend-law` prepares
an explicitly authorized change to accepted law. `review-law` adversarially checks candidates
before human acceptance; `shape-capability` turns demonstrated observation gaps into bounded
upstream pressure; `manage-baseline` governs accepted-current drift as a separate ratchet;
`retire-covered-prose` deletes only the comments an enforced boundary already holds. All
support the Tianheng line declared in `compatibility.json`.

## Standing Decisions

- **Controlled writing.** Foundry may generate Rust boundary and proof code, but only after its
  eligibility and authority gates pass.
- **Declared intent.** Project prose and direct human instruction may authorize a candidate.
  Repository shape and generic best practice may not.
- **Structural scope.** The initial workflow governs observable Rust architecture. Subjective,
  procedural, and historical claims remain prose.
- **Observation before generation.** Every candidate names a Tianheng observation source, target,
  and rule before code is written.
- **Proof before replacement.** A candidate proves teeth, precision, projection freshness, and
  compatibility before suggesting that source prose be removed or narrowed.
- **Human authority.** Generated code is a `VerifiedCandidate`; only human review promotes it to
  `AcceptedLaw`.
- **No silent amendment.** Existing accepted law is repaired toward its reason. Changing it
  requires an explicit amendment request.
- **Law stays frozen during repair.** Drift repair may change product code and tests, never the
  constitution, baseline, projection, severity, depth, reason, or allowed set.
- **Amendment direction is proven.** Tightening, loosening, retargeting, reason correction, and
  removal each require before/after witnesses that expose the intended reaction delta.
- **Activation is orientation.** Task-local selection may focus generated context before coding,
  but only Tianheng's post-change reaction verifies the result.
- **Review blocks but does not accept.** Adversarial review may reject or require revision of a
  candidate; only a human or steward promotes verified code to accepted law.
- **Pressure is not pretend law.** A missing observation becomes a source-, identity-, perimeter-,
  and fixture-backed upstream candidate, never a no-op boundary in the adopter.
- **Baseline is debt, not law.** Baseline operations compare structured identities and require
  separate authority; they never alter the Constitution or make observed violations clean.
- **Prose leaves only when a reaction holds it.** A comment may be retired when an enforced,
  unbaselined boundary observes its whole claim. Comment density is never a goal, a claim wider
  than its perimeter is retained rather than narrowed, and a sweep request authorizes the criterion
  rather than the computed deletion set.
- **Tianheng owns reaction.** Tianheng owns its DSL, observations, projections, evaluator, and
  complete cookbook. Foundry carries only selection and adaptation knowledge.
- **Repository independence.** Tianheng, Fornax, and Foundry release independently. Compatibility
  is declared and tested; no repository is vendored or attached as a git submodule.
- **One skill until evidence.** A new skill requires an independent trigger, output, and failure
  mode. Collection size is not a goal.
- **One declaration for the supported line.** `compatibility.json` is the only place the Tianheng
  range, representative, and upstream coordinate are written. CI resolves its checkout from it; the
  fixture, the canonical doc, and every prose surface are checked against it rather than repeating
  it.
- **A gate proves what it claims.** The compatibility runner asserts the injected checkout is what
  actually compiled, and drives the invocation surface the skills instruct an agent to use. A check
  that cannot fail for the reason it names is treated as absent.
- **Every routed recipe is proven.** The declared vocabulary, the recipe index, and the fixture
  agree in both directions. The index may not route to a recipe the fixture does not compile.
- **Linear, single-lineage history.** Changes land as commits on `main`; a second lineage is a
  hazard, not a workflow. `0.1.0` starts a fresh single-commit history. The pre-release history was
  discarded rather than archived, so every durable decision it carried lives in this file,
  `AGENTS.md`, the focused docs, and the tests.

## Non-goals

- Supplying architecture policy to an adopter.
- Governing non-Rust portions of a mixed-language repository.
- Replacing Tianheng's public documentation or copying its complete cookbook.
- Treating generated projection as an independently editable source of truth.
- Weakening accepted boundaries to make a reaction pass.
- Creating wrappers around deterministic Tianheng projection or evaluation.
- Promising compatibility with an untested Tianheng release line.
