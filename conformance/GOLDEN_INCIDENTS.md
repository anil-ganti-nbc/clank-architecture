# Golden Incident Register — Archaeology-derived conformance seeds

Status: **Required register; fixture implementation pending**
Authority: ADR-0005 and Canonical Standard v0.2

These are not anecdotal bug notes. Each item is a regression target. A fixture
must state setup, expected status, forbidden upgrade, evidence reference, and
rollback/cleanup behavior.

| ID | Incident class | Source evidence | Required invariant |
|---|---|---|---|
| L-WATCH-001 | shared SQLite writer contention | DiagnosticBench seed; 3fd9a04/2d15275 | lock contention cannot corrupt or cross-fail Clanks |
| L-WATCH-002 | historical article treated as novelty | seed; f9a401a | publication time and baseline prevent false freshness |
| L-PHONE-001 | stale app/build vs owner acceptance | seed | build/CI success is not field acceptance |
| L-FLEET-001 | directory sweep omits Tablet | seed | registry/manifest is fleet membership |
| L-SMART-001 | traversal succeeds, extraction yields zero | seed | HTTP success cannot upgrade semantic health |
| L-FGT-001 | catalogue path misses entitlement path | seed | source/category coverage is explicit and separate |
| L-OEM-001 | first scheduler fire mistaken for cadence | seed | recurrence is proved by observed cadence |
| L-OEM-002 | dual-host delivery canary | seed | one notification authority per lane |
| L-OEM-003 | operational health but recall gap | seed | intelligence/coverage health is independent |
| L-OEM-004 | Beelink miss without exposure evidence | seed | UNKNOWN root cause remains UNKNOWN |
| DB-002 | baseline events pollute analytics | DiagnosticBench DB-002 | baseline mode is carried and excluded by policy |
| ZOMBIE-AUTHORITY | disabled timer still fires | Smartwatch fleet snapshot | disabled component is provably inert |
| AUTHORITY-BYPASS | cron bypasses registered scheduler | SemInt fleet snapshot | invocation path is auditable and matched |
| STALE-STORE | local DB mistaken for production volume | FGT fleet snapshot | data-store identity is registered |
| AMBIENT-HOST | container hostname fabricates migrations | Smartwatch bc948a3 | host identity is pinned |
| SILENT-OBSERVABILITY | DB reinit swallows logs | FGT 840641f | successful run without logs is unevidenced |
| CAPABILITY-ABSENCE | policy/config/deploy/unknown collapsed | KTW, CTW, Feature Phone | capability state is evidence-bearing |
| LANE-LEAK | experimental records cross production boundary | Feature Phone/OEM/Smartwatch | lane_id and environment fence state |
| BASELINE-HANDOVER | replacement changes entity keys | Watch/Smartphone report | alias migration precedes live candidates |
| CROSS-CLANK-IDENTITY | same entity discovered by two Clanks | open architecture issue | no silent merge before identity ADR |
| SCHEDULER-MISMATCH | declared authority differs from live path | Smartwatch/SemInt/OEM | quarantine or UNKNOWN, never healthy |
| DB-LOSS-RESTORE | live volume deleted; older backup restored; ~4 days history missing | INC-20260823 volume loss, Smartwatch lane | continuity gap + restored-epoch represented; no invented organic transitions; health and continuity separate |
| DB-LOSS-NEW-EPOCH | live volume deleted; NO backup; hard new epoch via fresh baseline | INC-20260823 volume loss, Feature Phone lane | epoch boundary preserved; baseline suppresses novelty; absence never zero; M2/M3 cite the incident, never collector-repair advice |

Executable fixtures for DB-LOSS-RESTORE / DB-LOSS-NEW-EPOCH:
`motherclank` repository, `tests/test_golden_db_loss.py` (branch
`f6-continuity-f2`, commit `6dc4c99`); incident registry seed
`continuity/seeds/INC-20260823-volume-loss.jsonl`.

The fixture suite must be executable and versioned; this register alone is not
conformance evidence.
