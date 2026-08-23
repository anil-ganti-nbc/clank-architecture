# OPERATOR HANDOFF — for Claude (privileged operator)

Date: 2026-08-24. Author: ox-alpha (architect/implementer, no host access).
Everything below assumes the transferable bundles described in
TRANSFER.md have been applied/merged to canonical GitHub first.

## 0. What this work is

Observer-tier Motherclank capability (continuity + execution-liveness +
survivability evidence), governance ADRs 0006–0009, golden fixtures G1–G8
plus DB-LOSS pair, and operator-verified incident registry seeds.
Motherclank remains observer-only; nothing here mutates Clanks.

## 1. Apply the work

1. Fetch bundles from the transfer directory (see TRANSFER.md).
2. Review, then push branches to GitHub:
   - `motherclank` branch `f6-continuity-f2` (commits through bb58dfd)
   - `clank-architecture` branch `f6-adr0006-adr0007-continuity` (through current head)
3. Run test suites after merge: `python -m pytest tests` in motherclank
   (expect 137 passed / 4 skipped).

## 2. Host actions required (in priority order)

| # | Action | Why | Gate |
|---|---|---|---|
| H-1 | Install expectations + continuity + survivability registries into Motherclank's var dir (`liveness/`, `continuity/`, `survivability/`) from the shipped seeds; adjust cadence values to real schedules | enables MATERIALIZATION_GAP and dormancy semantics on live harvests | after merge |
| H-2 | Provide durable off-host destination for the two ACT-011 recovery points (currently temporary_scratch) — NAS share or other reviewed destination; re-transfer with durable metadata recorded | closes BLOCKER B-1; scratch copies are not redundancy | ASAP |
| H-3 | Schedule recurring SQLite-safe backups for fpc-epoch-2 + smartwatch restored DB per proposed CRITICAL RPO (≤6h) once ratified | keeps RPO ≈ 0 posture from decaying | H-2 |
| H-4 | Read-only export of Motherclank host `var/` JSONL batches intersecting 2026-08-22T09:00Z→2026-08-24T00:00Z so Phase I row-level impact confirmation can complete | completes INCIDENT_IMPACT_MAP | any time |
| H-5 | ACT-001 refresh: deployed SHA/data-store/scheduler/notification/backup facts per lane with fresh as_of; feed into adapter matrix rows | unblocks profile transitions | next convergence pass |
| H-6 | Least-privilege audit of destructive capabilities (ACT-012): which identities can delete volumes/prune/write prod DBs | ADR-0009 §Decision 3 report | before next agent-run host operation |
| H-7 | Diagnostic-clank F1 disposition is RESOLVED upstream (adapter plane already on default @10bf0c8) — no merge needed; optionally retire stale containment-branch assumptions in docs | prevents future confusion | trivial |

## 3. Blocker ledger

- B-1 Durable off-host storage undecided (blocks survivability class CRITICAL completion). Owner: operator.
- B-2 ADR-0006..0009 are PROPOSED drafts; require reviewed merge to activate canonically. Owner: architecture maintainer.
- B-3 Row-level incident reconciliation blocked on host artifacts (H-4).
- B-4 ACT-002 CTW credentials, ACT-003 SemInt scheduler-path residual, ACT-005 baseline handover records, ACT-006 cross-Clank identity ADR (participant gate), ACT-007 full v0.2 probe quartet, ACT-008 remaining fixtures, ACT-009 probe schema contract, ACT-010 feedback backfill — all OPEN/PENDING as registered.
- B-5 Cadence values in expectations seed are placeholders pending real schedule inventory.

## 4. Acceptance answers (evidence-based, see completion report §25)

Scenario A (delete FPC volume again): newest verified RP = ACT-011 epoch2-RP1
(RESTORE_VERIFIED); proven loss bounded by backup cadence since capture;
durable off-host NOT yet proven (scratch only); Motherclank WILL distinguish
the new discontinuity (continuity machinery implemented + tested).

Scenario B (root stash -u again): detection latency = one harvest cycle
beyond the expected window (grace ×2 of declared cadence); pre-exec failure
distinguished from application failure via stage evidence; Tablet emits
nothing (RETIRED policy); missing evidence = per-invocation scheduler-fire
records for lanes whose schedulers leave no queryable traces (cron log mtimes
not yet ingested by any observer contract).
