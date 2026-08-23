# Audit Action Register — archaeology follow-up

Status: **Open control register**
As-of basis: 2026-08-22 fleet snapshot and 2026-08-24 audit reviews
Authority: ADR-0005

These are control actions, not claims that the underlying runtime is fixed.
Every item must be refreshed with evidence before its horizon expires.

| ID | Action | Owner role | Status | Evidence required | Horizon/gate |
|---|---|---|---|---|---|
| ACT-001 | Refresh all instance/lane rows with live SHA, data store, host, lock, scheduler, notification, backup, and semantic probe | Platform maintainer | OPEN | Signed/current inventory evidence | Before any profile transition |
| ACT-002 | Rotate CTW credentials and complete historical secret-scan review | CTW maintainer + security reviewer | OPEN | Scan report, rotation record, host verification | Before network-exposed adapter |
| ACT-003 | Resolve SemInt direct-cron bypass of OperationalScheduler | SemInt maintainer + platform operator | OPEN | Invocation-path probe and one-authority proof | Before scheduler health can be HEALTHY |
| ACT-004 | Prove retired/disabled timers are inert | Each lane owner | OPEN | Scheduler inventory and no-fire evidence | Before lane aggregation |
| ACT-005 | Produce durable baseline checkpoint and identity-alias handover for each Clank | Each Clank maintainer | OPEN | baseline_id, key version, hash, migration record | Before candidate ingestion |
| ACT-006 | Define cross-Clank global identity/alias authority | Architecture maintainer | BLOCKING ADR | Accepted ADR with ownership, provenance, merge/review semantics | Before participant profile |
| ACT-007 | Implement observer probes and capability-state evidence | Adapter maintainer | PENDING | probe_identity, probe_health, baseline cursor, candidate pagination | Before observer acceptance |
| ACT-008 | Convert the golden register into executable fixtures | Conformance maintainer | PENDING | Deterministic fixture tests and reports | Before participant profile |
| ACT-009 | Define common semantic/coverage probe contract | Architecture + adapter maintainers | PENDING | Versioned probe schema and per-Clank mappings | Before cross-Clank health comparison |
| ACT-010 | Define append-only feedback backfill and lock evidence | QC/platform maintainer | PENDING | actor/source/policy/import provenance plus lock proof | Before Motherclank feedback writes |
| ACT-011 | Protect feature-phone fpc-epoch-2 and restored smartwatch DB with SQLite-safe Layer A+B backups; confirm smartwatch post-restore backup cadence | Lane owners + platform operator | OPEN | verified recovery point evidence with as_of | Immediately (INC-20260823 exposure) |
| ACT-012 | Least-privilege audit of destructive capabilities (volume deletion, prod DB writes, container control, backup access) | Platform operator + security reviewer | OPEN | audit report; changes require separate approval | Before next agent-run host operation |

Snapshot-derived statuses expire. A later verified record supersedes this table;
it must not silently edit the historical archaeology report.
