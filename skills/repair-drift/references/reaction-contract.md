# Reaction Contract

Use the adopter's actual Tianheng runner. For supported `0.3.x`, `check --format json` is the
machine contract.

## Exit Classes

| Exit | Meaning | Repair-drift action |
|---|---|---|
| `0` | Clean, warn-only, or fully baselined | Inspect the report; do not assume no findings |
| `1` | At least one unbaselined enforce violation | Repair eligible product drift |
| `2` | Constitution, scan, or usage error | Stop; the reaction is invalid |

Preserve the runner's exit status when capturing output. A pipeline ending in `jq` can otherwise
replace Tianheng's status with the formatter's status.

## Violation Fields

Read fields in this order:

1. `reason`: the accepted repair direction;
2. `target` and `rule`: the governed boundary;
3. `finding`: the observed fact;
4. `file`: the actionable location when observation yields one;
5. `polarity`: `deny_breach`, `allowlist_gap`, or null;
6. `severity` and `baselined`: whether this finding gates the current run;
7. `anchor`: optional durable governance context.

`file: null` is a faithful absence for graph edges and seam-level facts. Locate those through the
target and finding; never manufacture a path.

Group findings by `(target, rule)`. Structured `rule_key` and `fact` are stable identity data when
present; human wording alone is not identity.

## Non-violation Data

- `stale_baseline` is baseline maintenance pressure, not permission to rewrite product code or law.
- `coverage` is informational and does not decide the exit code.
- Warnings and baselined findings remain real observations even though they may exit `0`.
