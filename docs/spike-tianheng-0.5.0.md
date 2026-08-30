# Spike: Tianheng 0.5.0

Whether to move the supported line from `>=0.3.0,<0.4.0` to `>=0.5.0,<0.6.0`, what it costs, and
what it buys. Recorded because the answer turned on something no changelog reading would have
settled, and because one of its findings is deferred rather than closed.

## What the gate said before anything was measured

Pointed at a 0.5.0 checkout, `scripts/check_tianheng_compatibility.py` printed `ok`. The fixture
does not compile against 0.5.0 at all. `--config patch.crates-io.<crate>.path` is advisory: the
fixture required `=0.3.0`, the patch offered 0.5.0, and Cargo dropped the patch, resolved the
registry copy, and warned on a zero exit.

Every conclusion below rests on that being fixed first. A spike run against a lying gate measures
the gate.

## Cost: one rename

`SemanticBoundary` became `SignatureBoundary` in 0.4.0 — the only 0.3.0 → 0.5.0 break the
representative fixture meets. With that one substitution the fixture compiles clean against 0.5.0
across two minor releases.

Across the whole repository the same rename appears exactly once outside the fixture:
`forge-law`'s recipe index. The other twelve names in `recipe_vocabulary` all survive.

## What 0.4.0 changed that no signature shows

Three 0.4.0 entries are marked BREAKING without moving a type:

- 圭表 and 渾儀 now govern **every** compiled root of a package — a `main.rs` beside a `lib.rs` is
  no longer skipped.
- An outbound rule's finding now carries its **importing module**, so two importers of one path are
  two findings rather than one.
- 漏刻 no longer relativizes the identity label of a file reached through an absolute `#[path]`.

None of these invalidate a sentence in this repository. `repair-drift`, `amend-law`,
`manage-baseline` and `review-law` describe the *shape* `(target, rule_key, fact)` and the exit
classes `0`/`1`/`2`, and both survive. That is a property of where those skills were written, not
luck: they route on the identity's shape rather than on any particular fact.

They do reach an adopter. The first two make a **recorded baseline stale** — work an adopter did
not choose, which is why the release marked them. `manage-baseline` already treats a stale entry as
an ordinary lifecycle state, so the workflow needs no change; the adopter needs a regeneration.

## What 0.5.0 adds

0.5.0 is the first release in which an `Observer` outside the family can exist. The prelude gains
the protocol (`Observer`, `Run`, the three dimension observers) and the typed bound model
(`BoundDecl`, `BoundId`, `Extent`, `Reached`, `Owner`, `Defence`, `Demonstrates`,
`FactGranularity`), plus `Subject`.

Two things were built against it to find out what that is worth here. Both compile against
`tianheng::prelude` alone — an adopter's reach, not a family member's.

### Every dimension's declared limits are now machine-readable

`observation_bounds()` is **not** re-exported by the shell, but the bounds are reachable anyway:
each dimension's observer delegates `Observer::bounds()` to it, and the observers are re-exported.
An adopter depending only on `tianheng` gets the list.

It returns **42 declared bounds** — 11 static, 25 semantic, 6 runtime — each carrying an id, the
shape it stops at, and a typed extent:

| extent | meaning | count |
|---|---|---|
| `OutOfReach` | the source never sees the shape | 18 |
| `Reached(OverReacts)` | reacts wider than the truth | 5 |
| `Reached(UnderReacts)` | a **declared false negative**, with a named `Owner` | 11 |
| `Reached(NotAViolation)` / `AsIntended` / `DeclinesToRefuse` | deliberate, not a gap | 8 |

`UnderReacts` is the only extent that must name an owner, because a declared false negative with
nobody responsible for closing it is how one outlives its usefulness. Of the eleven: seven are
`Owner::Engine`, one is `Owner::Inherited`, and **three carry `Owner::Adopter`** —
Tianheng stating that the gap is the adopter's to close by narrowing their own declaration.

This is the same knowledge `forge-law`'s recipe index carries by hand in its *Important
non-observations* column, and the comparison is not close. That column has 18 one-phrase entries
against 42 declared bounds, and the omissions are load-bearing. For signature coupling it says
"Compiler-wide reachable API closure"; upstream declares seven separate re-export, glob and alias
bounds, including:

> a non-public `type` alias holding a `dyn`, named by a public signature — `OutOfReach`, because
> the resolver does not expand `type` aliases

An adopter claiming "no public signature exposes the database pool" gets a candidate from
`forge-law` today with no indication that a private alias defeats it. In 0.5.0 that limit is data,
available at candidate-formation time.

`shape-capability`'s central judgement — *is this gap Tianheng's to close?* — is answered outright
for every bound upstream has already declared.

### An adopter-owned observation composes into a run

A participant enforcing "no `todo!` or `unimplemented!` marker in a governed subtree" — structural,
statically observable, and covered by no dimension of 三儀 — was written against the prelude and
joined a run:

```text
violating fixture                    -> Violations (1)
clean fixture                        -> Clean (Subject { declared: 1, reached: 1 })
composed with a built-in dimension   -> Violations (1)
```

Teeth and precision, which is this repository's own proof standard, for a claim it would today
route to `SHAPE_CAPABILITY` and hand upstream.

`Observer::bounds()` has **no default body**, deliberately: a participant that will not say what it
cannot see cannot be written. `Subject::of` refuses to report clean when subtrees were declared and
no file was read, so a failed walk cannot pass as a sound workspace.

One real limit, recorded rather than worked around: `BoundaryKind` has no variant an outside
participant owns, so an adopter's finding must borrow one of the family's four. Upstream records
the same finding against its own example. The kind is a report label, not part of the recorded
`(target, rule_key, fact)` identity, so a borrowed kind misleads a consumer filtering by dimension
without making anyone's baseline stale.

## Headroom

None. `v0.5.0..main` is empty upstream, the changelog's `[Unreleased]` section is empty, and no
newer tag exists on the remote. 0.5.0 is the ceiling, not a waypoint.

The new `kanhe` and `shengmo` crates are `publish = false`, so `crate_family` is unchanged.

## Verdict

Move to 0.5.0. The rename is the whole mechanical cost, and the two 0.4.0 reaction changes reach
an adopter's baseline rather than this repository's prose.

But version currency is not the reason. `observation_bounds()` puts the judgement this collection
exists to make — *can Tianheng observe this claim, and whose gap is it if not* — on a machine-readable
footing for the first time. That judgement is currently a hand-maintained table which this spike
measured as materially incomplete.

## Deferred, deliberately

Whether an adopter may **own** an observation is a standing decision, not a version bump.
`PROJECT.md` says a missing observation becomes upstream pressure, "never a no-op boundary in the
adopter". That was a true statement about 0.3.0, where no third path existed. In 0.5.0 one does,
and `Owner::Adopter` is upstream's own vocabulary for it.

`shape-capability`'s `observation_owner` axis admits `none | static | semantic | runtime` — every
value naming a Tianheng dimension. The question is whether it gains a fourth. That is left open
here; the second proof above exists to make it decidable on evidence.

## What the supported line turned out to cost

It is written in more places than the declaration, and most of them had nothing comparing them to
it: the literal `validate_skills.py` asserts, `test_scenarios.py`'s `SUPPORTED_PREFIX`, the workflow
ref, six scenario fixtures, and — found last, after every machine-readable declaration had already
moved — **nine instructional lines** across seven skills and two references, each telling an adopter
that the guidance targets `0.3.x`.

That last set is the one that matters: a skill naming a line this repository no longer supports
routes an adopter by a surface that no longer exists, and it is invisible to every gate that reads
JSON. It is now checked — a Tianheng line named anywhere under `skills/` must equal the declared
one. The pin-agreement gate already covers the workflow ref.

`SUPPORTED_PREFIX` remains an unguarded copy.
