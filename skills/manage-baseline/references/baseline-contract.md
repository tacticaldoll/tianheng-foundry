# Structured Baseline Contract

Supported Tianheng `0.3.x` baselines declare:

```json
{"format": "tianheng.baseline/structured-facts"}
```

## Commands

- `check --write-baseline <file>` records current observed identities and exits `0`.
- `check --baseline <file>` gates only unbaselined enforce findings.
- `check --baseline <file> --disallow-stale` also exits `1` when baseline entries no longer match
  current findings.
- Combining `--baseline` and `--write-baseline`, omitting a flag value, or reading malformed data
  exits `2`.

Write mode never overwrites an unsupported existing file.

## Identity

Identity is exactly:

```text
(target, semantic rule_key, structured fact)
```

The following remain diagnostic or governance metadata and do not affect matching:

- human rule/finding wording;
- complete signature diagnostics;
- reason and severity;
- file, anchor, and polarity;
- `owner` and `tracker`.

## Rewrite Behavior

Rewriting removes entries whose identities are no longer observed and preserves `owner`/`tracker`
for retained identities. New observations become new entries, which is why every rewrite requires
an identity diff before authorization.

A baselined observation remains a violation; it is accepted-current debt that no longer fails the
gate.
