# Fleet Capability Matrix

Status: evidence snapshot at motherclank@local / diagnostic-clank@p41-capability-contract.
Generated from the adapters' `capability_states()` implementations plus
registry/expectation facts. This is EVIDENCE, not a score - no maturity,
quality, readiness, or promotion percentages exist anywhere in this file.
UNKNOWN stays visible by design.

States are the canonical `CapabilityState` vocabulary (ADR-0011):
active / supported_unconfigured / supported_undeployed /
unsupported_by_policy / unsupported / unknown_or_unverified.

| Lane | collection | health | events | delivery | qc | scheduler_trace | continuity | survivability | baseline/run-kind |
|---|---|---|---|---|---|---|---|---|---|
| watch-clank | active | active | active | unknown_or_unverified | active | supported_unconfigured | active | unknown_or_unverified | unknown_or_unverified |
| smartphone-clank | active | active | active | active | active | supported_unconfigured | active | unknown_or_unverified | unknown_or_unverified |
| korean-tech-wire | active | active | unsupported_by_policy | unsupported_by_policy | active | supported_unconfigured | active | unknown_or_unverified | unknown_or_unverified |
| feature-phone-clank | active | active | active | supported_undeployed | unknown_or_unverified | supported_unconfigured | active (fpc-epoch-2) | active (RP restore-verified; durable off-host UNPROVEN) | unknown_or_unverified |
| smartwatch-clank | active | active | unsupported_by_policy | unsupported_by_policy | unknown_or_unverified | supported_unconfigured | active (sw-epoch-1-restored…; known gap) | active (RP restore-verified; durable off-host UNPROVEN) | unsupported_by_policy |
| oem-radar | active | active | active | active (notifications table) | active (alert_reviews) | supported_unconfigured | active (CONTIGUOUS) | unknown_or_unverified | unknown_or_unverified |
| free-game-tracker | active* | active* | active* | unsupported (log-only outcomes) | unsupported (no substrate) | supported_unconfigured | active (CONTIGUOUS) | unknown_or_unverified | unsupported_by_policy (no run table) |

\* FGT marked active-by-code-evidence; REAL_STATE_VALIDATION = BLOCKED until
Claude validates against a live read-only copy (commands in OPERATOR_HANDOFF).

Execution-liveness expectations live in the liveness registry (per-instance
cadence/grace/materialization_policy), NOT in this matrix; they are lane
configuration, not adapter capability.

## Known gaps (explicit)

- All lanes' scheduler_trace is supported_unconfigured: probe-plane
  attestation of execution_result is designed but not yet deployed.
- Survivability is proven only for smartwatch + feature-phone recovery
  points; DURABLE OFF-HOST REMAINS BLOCKED for both and for every other
  lane.
- baseline/run-kind exists in no onboarded schema except by future design.

| semiconductor-intelligence/staging | semintel staging store (SQLite/alembic) | UNKNOWN | UNKNOWN | UNKNOWN | NO evidence | unknown_or_unverified (ACT-003) | OperationalScheduler + deploy-cron | PERIODIC (unverified) | STANDARD | low |

## Architecture Freeze

**v0.3 FROZEN** (2026-08-25). No speculative core redesign. No v0.4 until a real participant or incident proves the contract insufficient. Bug fixes, new adapters, new GICs, and operational improvements are permitted.

