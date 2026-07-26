# Identity Diff

Parse baseline and reaction JSON structurally. Canonicalize each identity as target, rule key, and
structured fact; never hash rendered messages.

## Sets

```text
retained = current ∩ previous
added    = current - previous
stale    = previous - current
```

| Set | Meaning | Default action |
|---|---|---|
| Retained | Known debt still observed | Preserve identity and annotations |
| Added | Current fact not previously accepted | Block until explicitly authorized or repaired |
| Stale | Accepted fact no longer observed | Eligible for pruning |

An equal count does not imply an equal set. One stale and one added identity are not neutral churn.

## Review Record

For each added identity show:

- target, semantic rule key, and structured fact;
- human reason and finding;
- severity and baselined state;
- file or faithful null;
- anchor and polarity; and
- proposed owner/tracker or repair disposition.

For retained identities verify metadata preservation. For stale identities record whether product
repair, law amendment, target movement, or identity-shape compatibility caused disappearance.

## Unsupported Data

Do not coerce numeric, unmarked, unknown-format, or malformed baselines. Preserve desired
annotations externally and follow an explicit compatibility migration.
