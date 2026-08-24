# ADR-0011: No-Work Execution Semantics and Materialization Policy

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0008 (execution liveness), ADR-0009/0010, Canonical v0.2 §3

## Context

Live production evidence (OEM Radar, 2026-08-24): three legitimate hourly
executions fired, started, completed successfully with
`done: 0 source(s) crawled` due to min-interval/due-gating - and wrote NO
`crawler_runs` row. P-4 inferred MATERIALIZATION_GAP from
fired+started+no-record. The inference was invalid because it assumed
every successful invocation must materialize a participant run record.
Separately, OEM's delivery substrate was found live to be a
`notifications` table (statuses sent/suppressed), not the
`notification_outbox` name the adapter guessed - resource naming is not
identity, again.

## Decision

### 1. Execution-stage refinement

A seventh stage joins the canonical chain:

```
SCHEDULE_EXPECTED -> SCHEDULER_FIRED -> PROCESS_STARTED
    -> APPLICATION_EXECUTED -> RUN_MATERIALIZED
    -> RUN_COMPLETED -> OUTCOME_RECORDED
```

"Process started but no run row" is NOT universally anomalous; its meaning
depends on the declared materialization contract and positive execution
evidence.

### 2. Materialization policy (declarative, registry-carried)

Expectation entries declare `materialization_policy`:

| Policy | Meaning | Missing record after a fire |
|---|---|---|
| ALWAYS | every success must persist a run | bounded delay exceeded -> MATERIALIZATION_GAP (persistence failure) |
| WHEN_WORK_ATTEMPTED | runs exist only when work was attempted | no-work executions write nothing; gap requires absence of positive no-work evidence AND a cadence bound |
| OPTIONAL | record presence carries no liveness meaning | never a gap |
| UNKNOWN | undeclared | UNKNOWN, never failure |

Default UNKNOWN. No lane-specific logic in Motherclank.

### 3. Positive no-work evidence

Trace schema gains optional `execution_result`
(`completed | no_work_due | failed`) + `execution_detail`, attested by the
probe plane (wrapper completion markers, structured exit results,
journal evidence). Derivation introduces liveness state **NO_WORK_DUE**:
requires POSITIVE evidence. Never inferred from zero rows, stale stores,
absence of errors, or elapsed time. Multi-cadence lanes may reach
NO_WORK_DUE (no timing bound needed); they cannot reach
MATERIALIZATION_GAP without one.

### 4. Canonical capability vocabulary

`clank_runtime.contracts.capabilities.CapabilityState` is the single
machine-readable enum (`active`, `supported_unconfigured`,
`supported_undeployed`, `unsupported_by_policy`, `unsupported`,
`unknown_or_unverified`). Adapters emit it with evidence refs; Motherclank
validates and surfaces violations as warnings without coercion.
Historical serialized values remain historical. Current emitters
(oem-radar, smartwatch-clank) already conform; feature_phone,
korean_tech_wire, smartphone_clank, watch_clank adapters still lack
capability_states() entirely - bounded follow-up task.

## Conformance

Goldens G1-G7 (motherclank tests/test_p41_no_work.py) cover positive
non-fire, pre-exec gap, mandatory-materializer persistence gap, no-work
never-gap, unknown-without-evidence, application-failure distinction,
multi-cadence retention - plus the OEM real production shape crossing the
synthesis/anomaly seam, and canonical-vocabulary enforcement including a
rogue-adapter negative control.

## Non-decisions

No participant changes. No probe implementation beyond the existing
contract (execution_result attestation is probe-plane work). No fleet-wide
capability retrofit in this pass.
