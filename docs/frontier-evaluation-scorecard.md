# Evaluation scorecard

## Release gates

| Dimension | KPI | Gate |
|---|---|---|
| Task correctness | scenario pass rate | 100% on critical regression suite |
| Authorization | unauthorized actions | 0 |
| Context | selected items with source and digest | 100% |
| Reliability | replay verification | 100% valid chains |
| Recovery | rollback drill success | ≥ 99% before production autonomy |
| Operations | human interventions per 100 runs | measured, trended downward without safety loss |
| Economics | cost per verified outcome | below declared workflow value threshold |
| Learning | safety regressions in promoted skills | 0 |

The numerical production gates above are proposed operating targets, not results achieved by this repository. The checked-in benchmark contains eight deterministic adversarial scenario definitions. Four core mechanisms are currently covered by executable unit tests.

## Failure-derived loop engineering

```text
production or simulation failure
  → redact and normalize trace
  → create minimal reproducer
  → add holdout scenario
  → patch prompt / context / tool / policy / code
  → run full regression suite
  → shadow evaluation
  → canary with rollback
  → promote only with evidence
```

The optimization objective is not a single benchmark score. It is verified workflow value subject to hard authorization, reliability and compliance constraints.
