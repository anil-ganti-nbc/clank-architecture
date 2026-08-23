# ADR-0008: Execution-Liveness and the Materialization Gap

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0002 (Motherclank stages), ADR-0006 (continuity),
Fleet Laws v1 (Law 3 health honesty, Law 5 scheduler authority)

## Context

Incident family A (2026-08-22, operator-verified): an interactive root
redeploy ran `git stash -u` / `git stash pop` for oem-radar,
smartwatch-clank, and feature-phone-clank. Untracked `logs/` directories
were recreated `root:root`; cron shell redirects (`>> logs/cron-*.log`)
failed BEFORE collector execution. Result: scheduler invocations existed,
zero application runs materialized, no failure records were written
(application logic never executed), and the outage stayed silent ~36 hours.

Lesson codified:

    SCHEDULE_EXPECTED ≠ SCHEDULER_FIRED ≠ PROCESS_STARTED
        ≠ RUN_MATERIALIZED ≠ RUN_COMPLETED ≠ OUTCOME_RECORDED

Motherclank previously had only run-recency evidence; it could not
distinguish "collector failing" from "collector never started" from
"scheduler silent" from "intentionally dormant".

## Decision

### 1. Six-stage observable model

Each stage carries YES / NO / UNKNOWN / NOT_APPLICABLE plus provenance:

```
SCHEDULE_EXPECTED → SCHEDULER_FIRED → PROCESS_STARTED
    → RUN_MATERIALIZED → RUN_COMPLETED → OUTCOME_RECORDED
```

Absence of evidence is UNKNOWN, never NO. NO requires positive contrary
evidence (e.g., invocation evidence NEWER than the newest run row proves
the expected run did not materialize).

### 2. MATERIALIZATION_GAP (canonical term)

Expected execution without a materialized run. Chosen over EXECUTION_GAP
(ambiguous about which plane failed) and EXPECTED_RUN_MISSING (describes
nothing about causality). It is an EXECUTION-plane fact and MUST NOT be
diagnosed as collector regression: when pre-exec steps fail, application
logic never ran and cannot have failed. Recommendations derived from it
belong to DEPLOYMENT_SCHEDULER_INSPECTION and must name the pre-exec
failure possibility explicitly.

### 3. Execution-expectations registry

Append-only, operator-owned `<var>/liveness/execution-expectations.jsonl`.
Policies: `PERIODIC | FINITE_SOAK | MANUAL | ON_DEMAND | DISABLED |
RETIRED | UNKNOWN`, each optionally with cadence_seconds and declared
scheduler authority. Runtime authority and this registry outrank abandoned
artifacts: a stale unit file on disk proves nothing (Tablet case:
`tablet-clank-soak.service` exists but the application refuses retired
configuration — correct output is INTENTIONALLY_DORMANT, never MISSING_RUN).

Scheduler-neutral by construction: cron, systemd timers, manual/on-demand,
finite soaks, and Windows experimental lanes are all expressible as policy
entries. **Grace is per-expectation** (`grace_multiplier` on each registry
entry); no universal multiplier exists and none may be codified. Until each
lane's grace is calibrated against its real scheduler authority, gap/stale
determinations are investigative signals for operator review — not alarms
and never automated actions. Expectation cadences MUST be verified against
live scheduling authority before activation; placeholder cadences produce
confidently wrong MATERIALIZATION_GAPs (register item B-5).

### 4. Derived liveness dimension (orthogonal)

`CURRENT | MATERIALIZATION_GAP | EXECUTION_STALE | SCHEDULER_SILENT |
INTENTIONALLY_DORMANT | UNKNOWN`. Orthogonal to operational health AND to
continuity_state; one Clank may simultaneously be HEALTHY + GAP_KNOWN +
CURRENT (Smartwatch post-restore). Liveness never upgrades or downgrades
the M1 rule machine.

### 5. SCHEDULER_SILENT discipline

Derived ONLY when the block positively declares its scheduler-evidence
plane current-and-empty. Observer blindness (unreadable DBs, FAILED_ADAPTER)
yields UNKNOWN across all stages — never "missing execution".

## Conformance

Golden fixtures G1–G8 (`motherclank` tests/test_golden_incidents_g1_g8.py)
pin: restore lineage vs new epoch (G1/G2), pre-exec gap semantics (G3),
dormancy suppression (G4), observer-outage honesty (G5), backup evidence
discipline (G6–G8). New golden register rows:
PRE-EXEC-MATERIALIZATION-GAP, ROOT-STASH-RUNTIME-PATH (see ADR-0009).

## Non-decisions

No participant authority. Motherclank does not install heartbeats, modify
cron/timers, or restart anything; the ad-hoc `/tmp/check-cron-heartbeat.sh`
PoC remains superseded-by-design until its capability exists inside the
observer plane with proper evidence contracts.
