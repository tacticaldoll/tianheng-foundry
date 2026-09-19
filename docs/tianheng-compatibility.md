# Tianheng Compatibility

The supported line is Tianheng `>=0.6.0,<0.7.0`; `0.6.0` is the checked representative.
`compatibility.json` is the machine-readable declaration and the only place either is written
down — CI resolves its upstream checkout from it, and every other surface is checked against it.

The recipe index carries routing knowledge and observation bounds, not a complete API copy.
Representative public vocabulary is compiled against a local checkout:

```bash
TIANHENG_SOURCE=/path/to/tianheng python3 scripts/check_tianheng_compatibility.py
```

The runner copies its consumer fixture into a temporary directory, patches every Tianheng family
crate to the supplied checkout, then asserts through `cargo metadata` that every declared family
crate really resolved under that checkout before compiling. A patch Cargo silently dropped is a
failure, not a pass.

It then drives the fixture's own runner binary, because compiling the vocabulary says nothing about
the invocation surface the skills instruct an agent to use. `list --format json` must project
boundaries carrying `kind`, `target`, `rule`, `severity`, and `reason`; and three declarations —
one satisfied, one violated, one naming a crate that does not exist — must produce exit classes
`0`, `1`, and `2` with the matching outcome, alongside a usage error that must also exit `2`. A
renamed subcommand, a moved projection field, or a changed exit class fails here rather than
reaching an adopter as a stale instruction.

It uses Cargo offline and leaves both repositories unchanged. CI resolves the declared upstream tag
from this file before invoking the same network-free runner.

A Tianheng minor release is compatibility work, not an assumed match. Update the declared range,
recipe vocabulary, fixture, and skill version together after review.
