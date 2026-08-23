# ADR-0007: Destructive Operation Safety and Fleet Data Survivability

Status: **PROPOSED — REVIEWED DRAFT** (activates on reviewed merge)
Date: 2026-08-24
Related: ADR-0005, ADR-0006, FLEET_LAWS v1 (Law 5 lane isolation),
NO_PROMOTION_POLICY, DATA_SURVIVABILITY.md

## Context

One operator command — `docker volume rm` against two misidentified volume
names — destroyed the live persistent state of smartwatch-clank and
feature-phone-clank. Smartwatch lost ~4 days of history (recoverable from a
2026-08-18 backup); Feature Phone lost its entire history (no backup
existed). The incident proves that human/agent destructive error is an
EXPECTED failure mode, and that one mistake currently has unbounded
recovery-point loss.

## Decision 1 — Destructive operation safety law (hard rule)

No automated agent performing deployment, coherence, diagnostics,
inspection, cleanup, migration, rebuild, or onboarding may delete a
persistent database, Docker volume, state directory, or backup unless the
operator explicitly authorized THAT destructive mutation.

- Pattern-derived resource names are NEVER sufficient evidence.
- The words "cleanup", "rebuild", "redeploy", "converge", "staging",
  "temporary", "old", "unused", "backup", "experimental" provide ZERO
  destructive authorization.
- Before any destructive operation: enumerate the actual resource; identify
  its owning clank_id/instance_id/lane_id; determine persistence class;
  create or verify recovery evidence; require explicit authorization.
- Resource naming is not identity. Where practical, persistent resources
  MUST carry machine-readable metadata (Docker labels or equivalent)
  binding them to clank_id, instance_id, lane_id, environment, data_role,
  epoch_id, persistence_class.
- Guards must NOT themselves acquire fleet write authority.

## Decision 2 — Survivability is owned by Clanks, observed by Motherclank

| Concern | Owner |
|---|---|
| Backup + restore implementation | each individual Clank |
| Evidence exposure (backup posture) | Diagnostic Clank adapter plane |
| Fleet survivability evaluation | Motherclank (read-only) |
| Minimum laws, vocabulary, RPO classes | clank-architecture |

Motherclank MUST observe backup posture without owning backups:
`ABSENT | PRESENT_UNVERIFIED | INTEGRITY_VERIFIED | RESTORE_VERIFIED |
STALE | FAILED | UNKNOWN | UNSUPPORTED_BY_POLICY`, with `last_backup_at`,
`integrity_verified_at`, `restore_verified_at`, `failure_domain`,
`off_host_copy`, `current_rpo`. File existence is not backup success;
integrity_check is not application restorability. Survivability is a plane
orthogonal to operational health and is reported per instance/lane/epoch,
never per repository.

## Decision 3 — Pre-mutation checkpoint contract

Operations legitimately mutating persistent production state (schema
migration, storage relocation, volume replacement, DB repair) follow:

```
IDENTIFY → VERIFY INSTANCE/LANE → VERIFY BACKUP POSTURE
→ CREATE/VERIFY RECOVERY POINT → RECORD PRE-MUTATION STATE
→ RECEIVE AUTHORIZATION → MUTATE → VERIFY → RETAIN RECOVERY POINT
```

This is an operator/fleet law; it grants Motherclank no mutation authority.

## Decision 4 — Recovery objectives and protection classes

Protection classes and RPO/RTO targets are PROPOSED in DATA_SURVIVABILITY.md
derived from the fleet inventory; they require per-lane operator adoption
and MUST NOT be implemented by writing to live production state during this
phase. Restore drills run only against isolated temporary storage with
positive resource identification before cleanup.

## Conformance additions

Golden incidents DB-LOSS-RESTORE and DB-LOSS-NEW-EPOCH cover the continuity
semantics of this class of event. Additional mechanically checkable rules:
backup-state vocabulary validation; per-instance/lane survivability evidence
required for any production-integrated instance; least-privilege audit of
destructive capabilities tracked as an open register item.

## Non-decisions

No backup infrastructure is provisioned by this ADR. No off-host destination
is selected without an operator-reviewed design step. No permission changes
are made; the least-privilege audit (DATA_SURVIVABILITY.md §14) reports
findings separately from any implementation.
