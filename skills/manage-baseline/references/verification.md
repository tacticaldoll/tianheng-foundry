# Baseline Verification

## File Integrity

- Semantic format is `tianheng.baseline/structured-facts`.
- Written identity set equals the authorized current set.
- No duplicate identities exist.
- Retained `owner`/`tracker` values survive.
- Only authorized annotations changed.

## Gate Directions

1. Current baselined findings do not fail ordinary gate mode.
2. A new unbaselined enforce fixture exits `1`.
3. Malformed/unsupported data exits `2`, never clean.
4. Stale entries appear in `stale_baseline`.
5. `--disallow-stale` exits `1` when stale exists and returns to the expected gate outcome after
   pruning.

Capture structured JSON and real process status for each applicable direction.

## Retirement

After retirement:

- ordinary check runs without `--baseline`;
- no current enforce violations remain;
- CI no longer references the removed file;
- warning and coverage state is reported accurately; and
- a focused violating fixture still proves law reaction.

## Frozen Surfaces

Diff Constitution source, reasons, severity, scan depth, and generated projection. Baseline work
must not change accepted law. Product-code repair belongs in a separate `repair-drift` transaction.
