# CTW Observer Evidence Inventory

Status: **PARTICIPANT ARCHAEOLOGY COMPLETE / ADAPTER IMPLEMENTATION BLOCKED**
Blocker: Motherclank Adapter Contract v0.3 (`883b586`) not yet canonical —
see AUDIT_ACTION_REGISTER addition ACT-013.
Evidence basis: chinese-tech-wire @ `9eec9f0` (canonical default branch,
shallow-inspected 2026-08-25); NO live host access.

## Identity
- clank_id: `chinese-tech-wire` (fleet.yaml classification CLANK)
- store: SQLite, config default `sqlite:///data/ctw.db` (`config.py:60`)
- schema mechanism: custom `migrate_schema()` column-adds (database/db.py);
  NO alembic_version / schema_version table observed → schema revision
  evidence = UNKNOWN until operator confirms migration state
- layers inside ONE deployment: NEWS | COMMUNITY | DOCUMENTARY
  (`source_runs.layer`, pre-V0.5.5.1 rows honestly NEWS)

## Native execution substrate — RICHER THAN FGT
`source_runs` table (per-attempt, append-only):
`id, source, layer, started_at, finished_at?, success(bool),
articles_found, articles_new, parse_errors, request_errors,
response_time_ms`

- NATIVE RUN ROW EXISTS (unlike FGT/smartwatch-style derived MAX)
- every attempted source attempt persists a row regardless of findings
- successful-zero cycle ⇒ rows with success=true, articles_new=0
- zero-source-eligible cycles do NOT occur by design: the pipeline
  attempts all enabled sources each invocation (no min-interval gating)
  → **materialization_policy = ALWAYS (attempt-level)**

## Semantic clocks present (native)
| Clock | Column |
|---|---|
| SOURCE_ATTEMPT_AT | source_runs.started_at |
| NATIVE_RUN_COMPLETED_AT | source_runs.finished_at |
| ARTICLE_PUBLISHED_AT | articles.promotion_start etc. |
| PARTICIPANT_INGEST_AT | articles discovered/ingested timestamps |
| DELIVERY_SENT_AT | notifications.sent_at |

All must stay distinct in the adapter; publication time must never be used
for operational recency.

## Delivery
`notifications` persists SENT notifications only (article_id,
priority_score, sent_at, discord_message_id, is_high_priority).
Suppressed/failed deliveries are NOT persisted here → delivery accounting
is PARTIAL: capability `active` with explicit limitation, or split claims:
sent-count = native; suppressed/failed = unsupported (log-only).

## QC / reviews
No review/alert_reviews substrate observed → `unsupported`.

## Continuity
CONTIGUOUS presumed (no destructive incident recorded for CTW);
presumed ≠ proven — registry entry to be added at onboarding with
operator confirmation.

## Scheduler
External hourly invocation of `main.py --full-once --scheduled`
(deploy crontab per prior fleet snapshot — REQUIRES live re-verification).
No native scheduler table → fire evidence via P-4 probe plane only.

## Known real incidents (corpus candidates)
- SK hynix RSS 403 host-block since 2026-08-10: source-level BLOCKED state,
  correctly NOT a parser fault — matches existing GIC handling; no new
  corpus class required.
- No genuinely NEW fleet-wide incident class surfaced by this archaeology.
