# Feasibility And Risk

Capability pressure is ready only when the proposed measure can be tested honestly.

## Feasibility Checks

- The observation source exists in normal Tianheng evaluation.
- Collection does not require arbitrary adopter code execution unless it is explicitly a runtime
  probe.
- Facts can be canonicalized independently of formatting and diagnostic prose.
- Target, rule key, and structured fact form stable baseline identity.
- Positive and clean fixtures can isolate the intended fact.
- Invalid targets and unreadable sources can fail loudly as exit `2`.
- Scan cost is bounded by declared workspace/target/depth.

## Risk Record

Document:

- known false positives;
- known false negatives;
- macro and generated-code behavior;
- aliases, re-exports, and type canonicalization;
- feature and `cfg` sensitivity;
- platform dependence;
- deduplication rules;
- interaction with severity and baseline; and
- compatibility impact on JSON/SARIF/projection.

## Readiness

- `READY_PRESSURE`: source, identity, perimeter, fixtures, and limitations are concrete.
- `DEFER_OBSERVATION`: no source or stable fact exists.
- `DEFER_FEASIBILITY`: source exists, but precision, identity, cost, or composition remains unclear.

Defer is preferable to creating an inert boundary or empty observation dimension.
