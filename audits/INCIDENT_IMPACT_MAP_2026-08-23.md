# INCIDENT IMPACT MAP — 2026-08-23 volume-loss event

Status: **PARTIAL — structure complete; artifact-level confirmation blocked**
Incident registry seed: `motherclank` `continuity/seeds/INC-20260823-volume-loss.jsonl`
(registry_hash `sha256:a0918815…f05b327`)
Authority: ADR-0006 (draft); append-only annotation principle applies

## Established timeline (from operator-provided evidence)

| Instant (UTC) | Event |
|---|---|
| 2026-08-22T10:00Z | last known live observation, both affected DBs; scheduler outage begins |
| 2026-08-23T21:22:08Z | `smartwatch_clank_staging_data` destroyed |
| 2026-08-23T21:22:11Z | `feature_phone_clank_staging_data` destroyed |
| 2026-08-23T21:36:11Z | Feature Phone fresh DB created by collector → NEW EPOCH (baseline, suppressed) |
| 2026-08-23T22:09:00Z | Smartwatch restored from 2026-08-18T20:50:37Z backup (integrity ok) |

Permanently missing Smartwatch history: ≈2026-08-18T20:13Z → 2026-08-22T10:00Z.
Feature Phone pre-incident history: entirely irrecoverable. No observations
may be inferred during 2026-08-22T10:00Z → 2026-08-23T22:09Z.

## Artifact-class impact matrix

Motherclank writes dated append-only JSONL batches per stage. Any batch whose
`harvested_at_utc` / `generated_from` falls in or after the incident window
is potentially interpretive of states A–E below. The map below defines what
must be checked per class; actual row-level confirmation requires the host's
`var/` directory, which this audit could not access.

| Observed DB state | Expected in window | Interpretation Motherclank would have made | Validity after ADR-0006 | Required qualification |
|---|---|---|---|---|
| A original pre-loss | ≤ 2026-08-23T21:22Z | healthy/staged lanes normal | VALID as knowledge-at-the-time | none |
| B missing/unavailable DB | 21:22Z–21:36Z (FPC) / –22:09Z (SW) | FAILED_ADAPTER block → R0 UNKNOWN synthesis | VALID (UNKNOWN was honest) | annotate: absence = known destructive loss, not outage mystery |
| C empty/recreated state | FPC 21:36Z onward | fresh catalogue discovery — **risk of false novelty/recovery narrative** | INVALID as organic reading | NEW_EPOCH context; baseline suppression holds |
| D restored SW state | ≥ 22:09Z | apparent history rewind / mass source recovery | INVALID as organic reading | RESTORED_HISTORY + GAP_KNOWN; epoch id distinct |
| E new FPC epoch | ≥ 21:36:11Z | "all sources disappeared then reappeared" style M2 records | INVALID as organic reading | CONTINUITY_EVENT records + anomaly qualification; M3 cites incident |

Stage-specific obligations once host artifacts are available:

- **M0 snapshots**: every snapshot with harvest time ≥ 2026-08-22T10:00Z for
  the two clank_ids must be listed with its content_hash and re-derived
  continuity context (derive-time only; lines untouched).
- **M1 syntheses**: any HEALTHY/DEGRADED claim on the affected lanes between
  B/C/D windows must be paired with its continuity qualification.
- **M2 anomaly batches**: SOURCE_HEALTH_TRANSITION /
  SOURCE_DEGRADED_AT_FIRST_OBSERVATION / recovery records on these lanes in
  the window are expected to be retroactively flagged
  `continuity_qualified=true` by re-running detect with the registry.
- **M3 recommendations**: any UPSTREAM_CLANK_REMEDIATION recommendation
  citing only window anomalies is superseded by incident citation.
- **QC corpus / soak**: no gate reset; affected-lane metrics that became
  unmeasurable report UNKNOWN, not zero. Feature Phone QC absence across the
  epoch boundary is not negative feedback.

## Blocked items (STOP-condition compliant)

1. Host `var/` artifacts (snapshots/syntheses/anomalies/qc_corpus/soak
   JSONL) were not reachable from this environment; row-level confirmation
   requires an operator-supplied read-only copy or in-host run of:
   `motherclank validate-continuity --var-dir <var>` plus a listing of
   batch files with timestamps intersecting the window above.
2. No historical artifacts were modified anywhere (none were present to
   modify locally; the contract forbids it regardless).

The registry seed shipped with this repository encodes states A–E so that
the FIRST post-merge harvest/detect run produces the correct qualified view
without touching any historical line.
