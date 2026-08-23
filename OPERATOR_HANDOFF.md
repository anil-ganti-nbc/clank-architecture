# OPERATOR HANDOFF - for Claude (privileged operator)

Date: 2026-08-24 (pass 2 revision). Author: ox-alpha (architect/implementer,
no host access). Assumes the transfer bundles described in TRANSFER.md
(clank-transfer directory) have been applied to canonical GitHub first.

## 0. What this work is

Observer-tier Motherclank capability (continuity + execution-liveness +
survivability evidence), governance ADRs 0006-0009, golden fixtures G1-G8
plus the DB-LOSS pair, and operator-verified incident registry seeds.
Motherclank remains observer-only; nothing here mutates Clanks.

## 1. Apply the work

1. Fetch bundles from the transfer directory; verify against stated bases.
2. Review, then push branches to GitHub:
   - `motherclank` branch `f6-continuity-f2` (base cb57e9e, head bb58dfd+)
   - `clank-architecture` branch `f6-adr0006-adr0007-continuity`
     (base e16d48b)
3. Run test suites after merge: `python -m pytest tests` in motherclank
   (expect 139 passed / 4 skipped).

## 2. Host actions required (operator-set priorities, in order)

Database mutation PROHIBITED throughout. All backup creation uses
consistent-snapshot mechanics against disposable verification targets.

| # | Action | Why | Gate |
|---|---|---|---|
| P-1 | Review + apply bundles, run suites, push/merge. Do NOT recreate the work by hand unless bundle application fails. | canonicalisation; ends the transferability gap | first |
| P-2 | Install expectations registry ONLY AFTER verifying every cadence/grace against live cron/systemd authority per lane. Seed cadences are placeholders (B-5); wrong values manufacture confident false MATERIALIZATION_GAPs. Continuity + survivability registries can install immediately (their evidence is incident-derived, not cadence-derived). | honest liveness activation | before enabling gap detection |
| P-3 | Close the durable-backup hole: recurring SQLite-safe recovery-point creation for fpc-epoch-2 + smartwatch restored DB, plus a real durable off-host destination (scratch copies are not redundancy). RPO/RTO numbers in DATA_SURVIVABILITY 17.3 are NOT RATIFIED - derive per-lane targets from measured collection cadence and value inventory. | largest remaining exposure: FPC survives another deletion only as well as its single recovery point | highest operational priority |
| P-4 | Build the observation side of liveness: scheduler-fire traces inside the adapter plane, superseding /tmp/check-cron-heartbeat.sh, so Scenario B detection rests on evidence rather than absence-of-run heuristics | next development target after convergence | after P-1..P-3 |
| H-4 | Read-only export of Motherclank host var/ JSONL batches intersecting 2026-08-22T09:00Z..2026-08-24T00:00Z | completes row-level incident reconciliation | any time |
| H-5 | ACT-001 refresh: deployed SHA / data-store / scheduler / notification / backup facts per lane with fresh as_of | unblocks profile transitions | next convergence pass |
| H-6 | Least-privilege audit of destructive capabilities (ACT-012): which identities can delete volumes, prune, write prod DBs | ADR-0009 report | before next agent-run host operation |
| H-7 | Diagnostic-clank F1 disposition RESOLVED upstream (adapter plane already on default @10bf0c8) - no merge needed; retire stale containment assumptions in docs | prevents confusion | trivial |

## 3. Blocker ledger

- B-1 Durable off-host storage undecided (blocks CRITICAL-class completion).
  Owner: operator. Addressed by P-3.
- B-2 ADR-0006..0009 are PROPOSED drafts; require reviewed merge to activate
  canonically. Owner: architecture maintainer.
- B-3 Row-level incident reconciliation blocked on host artifacts (H-4).
- B-4 ACT-002 CTW credentials, ACT-003 SemInt scheduler-path residual,
  ACT-005 baseline handover records, ACT-006 cross-Clank identity ADR
  (participant gate), ACT-007 full v0.2 probe quartet, ACT-008 remaining
  fixtures, ACT-009 probe schema contract, ACT-010 feedback backfill -
  all OPEN/PENDING as registered.
- B-5 Cadence placeholders in expectations seed MUST be verified against
  live scheduler authority before gap detection activates (P-2).

## 4. Acceptance answers (evidence-based)

Scenario A (delete FPC volume again): newest verified RP = ACT-011 epoch2
RP1 (RESTORE_VERIFIED); proven loss bounded by backup cadence since capture
- currently ad-hoc, so honestly: everything since the last backup, and
backups are not yet recurring. Durable off-host NOT proven (scratch only).
Restoration HAS been tested once. Motherclank WILL distinguish the new
discontinuity (implemented + fixture-tested).

Scenario B (root stash -u again): detection latency = one harvest cycle past
the lane's declared grace window once expectations are installed and
verified (P-2). Pre-exec failure distinguished from application failure via
stage evidence; MATERIALIZATION_GAP recommendations explicitly forbid
collector-regression diagnosis; Tablet emits nothing (RETIRED policy, grace
now per-expectation rather than universal). Missing evidence: per-invocation
scheduler-fire traces for schedulers that leave none (P-4 target).
