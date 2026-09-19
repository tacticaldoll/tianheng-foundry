# Reaction Proof

A candidate law needs evidence in both directions.

## Required Matrix

| Case | Governed fact | Required outcome |
|---|---|---|
| Violating | Present at the declared target and depth | Enforced violation / exit class `1` |
| Clean precision | Absent while nearby legitimate code remains | Clean / exit class `0` |

Exit class `2` means usage, constitution, or scan failure. It never proves the boundary has teeth.

Warning severity, a fully baselined finding, successful construction, projection output, and
compilation alone are not an enforced violating proof.

## Choose The Repository-Native Harness

Prefer, in order:

1. the adopter's existing `GovernanceTest` architecture-test pattern;
2. its existing pure standalone or composed check function;
3. its checked-in law runner against a focused fixture; or
4. one minimal governed fixture crate when no suitable harness exists.

Do not invent a second constitution solely for the test. Reuse the same boundary builder or law
source the project intends to accept.

## Verification Record

For each direction record:

- fixture or source path;
- exact command;
- expected exit class or structured outcome;
- observed result; and
- rule identity or target that proves the intended boundary caused the result.

Avoid pinning complete human-readable diagnostics when structured identity is available.

## Failure Discipline

When the violating case stays clean:

- confirm the target and scan depth;
- confirm the observation source actually sees the authored fact;
- confirm the selected evaluator includes that boundary family;
- check fixture reachability and manifest scope; and
- decline an observation gap rather than broadening the reason.

When the clean case reacts:

- narrow target, parameters, or operand to the declared intent;
- do not baseline the false positive;
- do not switch to warning merely to pass; and
- revisit whether the chosen recipe observes the right fact.

After focused proof, run the adopter repository's normal format, lint, test, projection-freshness,
and Tianheng gates.
