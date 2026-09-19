# Projection Source

Accepted Rust `Constitution` code is the authority. Tianheng's `list --format json` is its canonical
machine-readable projection for activation.

## Source Order

1. Read local contributor instructions to find the project-native runner.
2. Invoke that runner's `list --format json` form.
3. Resolve the Tianheng version from Cargo metadata or lockfile.
4. Use generated Markdown only as human orientation or freshness evidence, never as a second law
   source.

The published `tianheng` binary may project a demo constitution; do not mistake it for an adopter's
own runner.

## Boundary Data

Retain:

- `kind`;
- `target`;
- rule identity and parameters;
- severity;
- complete forward `reason`;
- optional anchor;
- scan-depth or observation options.

Do not derive new requirements from names or fill missing fields with conventions.

## Failure States

Stop when:

- the runner cannot list the adopter's constitution;
- JSON is malformed or disagrees with the law source;
- multiple runners project contradictory accepted law;
- the Tianheng version is outside the supported range; or
- projection freshness checks say a checked-in generated artifact is stale.

An empty boundary list is valid evidence of no accepted law, not a reason to invent one.
