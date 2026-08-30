# Tianheng Compatibility

The supported line is Tianheng `>=0.5.0,<0.6.0`; `0.5.0` is the checked representative.
`compatibility.json` is the machine-readable declaration.

The recipe index carries routing knowledge and observation bounds, not a complete API copy.
Representative public vocabulary is compiled against a local checkout:

```bash
TIANHENG_SOURCE=/path/to/tianheng python3 scripts/check_tianheng_compatibility.py
```

The runner copies its consumer fixture into a temporary directory, patches every Tianheng family
crate to the supplied checkout, uses Cargo offline, and leaves both repositories unchanged. CI may
check out the declared upstream tag before invoking the same network-free runner.

A Tianheng minor release is compatibility work, not an assumed match. Update the declared range,
recipe vocabulary, fixture, and skill version together after review.
