# ADR-0006: Observational Continuity and Epoch Semantics

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0002 (Motherclank stages), ADR-0005 (integration gates),
Fleet Laws v1 (Laws 1, 2, 3, 6), CANONICAL_CLANK_ARCHITECTURE_v0.2 §4

## Context

On 2026-08-23 a destructive operator error deleted live Docker volumes for
smartwatch-clank (restored from a 2026-08-18 backup) and feature-phone-clank
(no backup; hard epoch discontinuity at 2026-08-23T21:36:11Z). Motherclank
M0–M4 has no way to represent known destructive discontinuities, so missing
DBs, empty recreated state, restored older state, fresh baselines, apparent
source disappearance/reappearance, and scheduler outages can all masquerade
as organic fleet behaviour in snapshots, syntheses, anomaly ledgers,
recommendations, and QC corpora.

## Decision

Adopt observational continuity as a general fleet capability, not a
special case for two Clanks.

### Ownership (verified against ADR-0001/0002 boundaries)

| Concern | Owner |
|---|---|
| Continuity law, event contract, conformance gates | clank-architecture (this ADR) |
| Epoch/backup/discontinuity EVIDENCE exposure | Diagnostic Clank adapter plane |
| Consumption, derivation, qualification | Motherclank (observer only) |

### ContinuityEvent contract

Events live in an APPEND-ONLY registry (`<var>/continuity/continuity-events.jsonl`,
seeded per incident). Required fields: `event_id`, `clank_id`, `instance_id`,
`lane_id`, `event_type`, `effective_start`, `effective_end|null`,
`discovered_at`, `evidence_refs`, `previous_epoch_id`, `new_epoch_id`,
`origin (operator|system)`, `notes`, `content_hash`. Event types:
`DATA_LOSS | RESTORE_FROM_BACKUP | NEW_BASELINE | EPOCH_BOUNDARY |
OBSERVATION_GAP | SCHEDULER_OUTAGE | UNKNOWN_CONTINUITY`.
Every record is content-hashed; tampering is detectable.

### Binding behaviour

1. **Append-only.** Historical M0–M4 artifacts are never edited. Later
   knowledge appends evidence; synthesis qualifies historical interpretation
   at derive time.
2. **UNKNOWN means UNKNOWN.** An open `effective_end` stays open. Absence is
   never zero. Restoration never implies uninterrupted continuity.
3. **Epoch identity.** Every derived claim can name its epoch. Pre/post
   boundary histories MUST NOT silently merge. A fresh baseline is never
   novelty.
4. **Orthogonality.** `continuity_state`
   (`CONTINUOUS | GAP_KNOWN | RESTORED_HISTORY | NEW_EPOCH |
   UNKNOWN_CONTINUITY`) is independent of operational health. Operational
   HEALTHY + continuity GAP_KNOWN must be representable, and continuity
   never upgrades or downgrades the M1 rule machine.
5. **M2 honesty.** Known incidents appear as explicit CONTINUITY_EVENT
   ledger records; anomalies derived inside discontinuity windows carry
   additive qualification (`continuity_qualified`, event ids) — evidence is
   explained, never deleted.
6. **M3 honesty.** Recommendations generated solely from destroyed/restored
   state MUST NOT advise upstream collector repair; they cite the incident.
7. **M4/QC.** QC records link to their ingestion snapshot's continuity
   context via snapshot hash; historical QC absence across an epoch boundary
   is never negative feedback.
8. **Soak.** The QC soak clock is not reset by this incident. Gates that
   become unmeasurable for affected lanes report UNKNOWN / NOT-YET-MATURE,
   never zero.

### Conformance

Executable fixtures DB-LOSS-RESTORE and DB-LOSS-NEW-EPOCH (golden incidents
register; implemented on motherclank branch `f6-continuity-f2`, commit
`6dc4c99`) are mandatory regression targets for any future refactor of
M0–M4 derivation.

## Non-decisions

No participant authority is created. Motherclank still cannot write to any
Clank, schedule anything, or send anything. The registry records incidents;
it does not authorize remediation of them.
