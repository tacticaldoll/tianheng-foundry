# Verification

Verification proves that product code returned to accepted law without changing the law.

## Required Evidence

1. Capture the pre-repair JSON report and exit status.
2. Record the targeted `(target, rule, fact)` identities.
3. Run focused behavioral tests after the edit.
4. Rerun the identical Tianheng invocation.
5. Confirm targeted identities disappeared rather than becoming warned, baselined, or unobserved.
6. Inspect remaining `violations`, `stale_baseline`, and `coverage`.
7. Run the repository's normal completion gates.
8. Diff or hash frozen authority files and confirm they are unchanged.

## Interpreting The Result

- Exit `0` with no violations: reaction is clean.
- Exit `0` with warnings or baselined findings: enforced drift is clear, advisory state remains.
- Exit `1`: repair is incomplete or exposed another enforced fact.
- Exit `2`: verification is invalid; resolve the runner/constitution/scan problem separately.

Do not use compilation alone as reaction proof. Do not call a changed finding string a repair when
its structured identity remains. Do not report full cleanliness when the run only passed because
the finding was already baselined.
